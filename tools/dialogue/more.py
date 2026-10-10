"""New dialogue arrives as fragment files, merged into the banks by this script.

    python tools/dialogue/more.py check tools/dialogue/more/shulkin/chat_01.json   check one fragment (merged in memory)
    python tools/dialogue/more.py status                                          new lines per bank, every fragment
    python tools/dialogue/more.py merge                                           write every fragment into the banks

A fragment lives in tools/dialogue/more/<bank>/<anything>.json and holds more lines for a bank, in the bank's
own shape (see check.py):

    {
      "topics": {"chat": {"0": ["line", ...], "3": [...]}, ...},
      "jobs":   {"archivist": {"0": [...]}, ...},                      shulkin and chorrin
      "ranks":  {"lord": {"chat": {"0": [...]}}, ...}                  court
    }

Lines are appended to the pools that already exist. Only level keys a pool already has may be used (a new key
would hide the lines below it), with one exception: a Court rank may take over a topic it doesn't override yet
if the fragment gives it every level key the shared topic has, with at least 12 lines under each.
Lines already in the bank are skipped, so merging twice changes nothing. Every check runs check.py's rules
(placeholders, length, no gendered words, single quotes, no duplicates) on the merged bank.

Lines nobody can hear are refused: the shared "work" pool (every resident has a job, whose own pool
replaces it), and shared Court topics that every rank overrides.
"""
import copy
import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check  # noqa: E402

MORE = Path(__file__).parent / 'more'
BANKS = list(check.REQUIRED)
OVERRIDE_MIN = 12


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def bank_lines(bank):
    out = []
    for table in bank.get('topics', {}).values():
        for lines in table.values():
            out += lines
    for table in bank.get('jobs', {}).values():
        for lines in table.values():
            out += lines
    for rank in bank.get('ranks', {}).values():
        for table in rank.values():
            for lines in table.values():
                out += lines
    return out


def unreachable(bank, name, topic):
    if name in check.JOBS and topic == 'work':
        return 'every resident has a job: write job lines ("jobs") instead of the shared "work" pool'
    if name == 'court':
        ranks = bank.get('ranks', {})
        if all(topic in ranks.get(r, {}) for r in check.RANKS):
            return f'every rank overrides "{topic}": write rank lines ("ranks") instead'
    return None


def merge(bank, name, frag, where, problems):
    """Adds a fragment to a bank in place. Returns (lines added, duplicates skipped)."""
    seen = set(bank_lines(bank))
    added = skipped = 0

    def add(target, lines, at):
        nonlocal added, skipped
        if not isinstance(lines, list) or not all(isinstance(s, str) for s in lines):
            problems.append(f'{where}: {at}: must be a list of strings')
            return
        for s in lines:
            if s in seen:
                skipped += 1
                continue
            seen.add(s)
            target.append(s)
            added += 1

    def tables(kind, frag_tables, bank_tables, at, allow_new_topic=None):
        if not isinstance(frag_tables, dict):
            problems.append(f'{where}: {at} must be an object')
            return
        for key, levels in frag_tables.items():
            here = f'{at}.{key}'
            if not isinstance(levels, dict):
                problems.append(f'{where}: {here} must be {{"<min level>": [lines]}}')
                continue
            old = bank_tables.get(key)
            if old is None:
                if allow_new_topic is None or not allow_new_topic(key, levels, here):
                    continue
                bank_tables[key] = {k: [] for k in levels}
                old = bank_tables[key]
            for lv, lines in levels.items():
                if lv not in old:
                    problems.append(f'{where}: {here} has no level key "{lv}" (it has {", ".join(sorted(old, key=int))}): '
                                    'use one of those')
                    continue
                add(old[lv], lines, f'{here}.{lv}')

    for k in frag:
        if k not in ('topics', 'jobs', 'ranks', 'bank'):
            problems.append(f'{where}: unknown key {k} (only topics, jobs, ranks)')
    if 'bank' in frag and frag['bank'] != name:
        problems.append(f'{where}: "bank" is {frag["bank"]!r} but the fragment is in more/{name}/')

    def no_new_topic(kind):
        def refuse(key, levels, here):
            problems.append(f'{where}: {here}: no such {kind} in {name}')
            return False
        return refuse

    topics = frag.get('topics', {})
    for t in topics:
        why = unreachable(bank, name, t)
        if why:
            problems.append(f'{where}: topics.{t}: nobody hears these lines: {why}')
    tables('topics', {t: v for t, v in topics.items() if not unreachable(bank, name, t)}, bank.setdefault('topics', {}),
           'topics', no_new_topic('topic'))
    if 'jobs' in frag:
        if name not in check.JOBS:
            problems.append(f'{where}: {name} has no jobs')
        else:
            tables('jobs', frag['jobs'], bank.setdefault('jobs', {}), 'jobs', no_new_topic('job'))
    if 'ranks' in frag:
        if name != 'court':
            problems.append(f'{where}: only the court has ranks')
        else:
            for rank, rtables in frag['ranks'].items():
                if rank not in check.RANKS:
                    problems.append(f'{where}: unknown rank {rank}')
                    continue

                def take_over(topic, levels, here, rank=rank):
                    shared = bank['topics'].get(topic)
                    if shared is None:
                        problems.append(f'{where}: {here}: no such topic')
                        return False
                    if set(levels) != set(shared) or any(len(v) < OVERRIDE_MIN for v in levels.values()):
                        problems.append(f'{where}: {here}: {rank} does not override "{topic}" yet; to take it over give '
                                        f'every level key the shared topic has ({", ".join(sorted(shared, key=int))}) '
                                        f'with at least {OVERRIDE_MIN} lines each')
                        return False
                    return True

                tables('ranks', rtables, bank.setdefault('ranks', {}).setdefault(rank, {}), f'ranks.{rank}', take_over)
    return added, skipped


def fragments(name):
    return sorted(glob.glob(str(MORE / name / '*.json')))


def run_checks(name, bank):
    """check.py's rules on an in-memory bank."""
    import os
    import shutil
    # check.check reads from disk: point it at a temporary copy (one folder per process: writers check at once)
    real_dir = check.DIR
    tmpdir = Path(__file__).parent / 'more' / '.tmp' / str(os.getpid())
    try:
        tmpdir.mkdir(parents=True, exist_ok=True)
        (tmpdir / f'{name}.json').write_text(json.dumps(bank, ensure_ascii=False), encoding='utf-8')
        check.DIR = tmpdir
        return check.check(name)
    finally:
        check.DIR = real_dir
        shutil.rmtree(tmpdir, ignore_errors=True)


def name_of(path):
    name = Path(path).resolve().parent.name
    if name not in BANKS:
        sys.exit(f'{path}: a fragment lives in tools/dialogue/more/<bank>/ (one of {", ".join(BANKS)})')
    return name


def cmd_check(paths):
    bad = 0
    for path in paths:
        name = name_of(path)
        bank, problems = load(check.DIR / f'{name}.json'), []
        try:
            frag = load(path)
        except json.JSONDecodeError as e:
            print(f'{path}: not valid JSON: {e}')
            bad += 1
            continue
        added, skipped = merge(bank, name, frag, Path(path).name, problems)
        more, _ = run_checks(name, bank)
        problems += more
        print(f'{path}: +{added} lines' + (f', {skipped} duplicates skipped' if skipped else '')
              + (', ok' if not problems else f', {len(problems)} problems'))
        for p in problems[:60]:
            print('   ', p)
        bad += len(problems)
    return 1 if bad else 0


def dump(bank):
    """The banks' own layout: one line of dialogue per line of the file."""
    out = ['{']
    keys = list(bank)
    for i, key in enumerate(keys):
        comma = ',' if i < len(keys) - 1 else ''
        v = bank[key]
        if key in ('topics', 'jobs'):
            out.append(f'  "{key}": {{')
            out += tables(v, '    ')
            out.append('  }' + comma)
        elif key == 'ranks':
            out.append('  "ranks": {')
            rs = list(v)
            for j, r in enumerate(rs):
                out.append(f'    "{r}": {{')
                out += tables(v[r], '      ')
                out.append('    }' + (',' if j < len(rs) - 1 else ''))
            out.append('  }' + comma)
        elif isinstance(v, list) and len(json.dumps(v, ensure_ascii=False)) > 100:
            out.append(f'  "{key}": [')
            for j, s in enumerate(v):
                out.append('    ' + json.dumps(s, ensure_ascii=False) + (',' if j < len(v) - 1 else ''))
            out.append('  ]' + comma)
        else:
            out.append(f'  "{key}": ' + json.dumps(v, ensure_ascii=False) + comma)
    out.append('}')
    return '\n'.join(out) + '\n'


def tables(topics, pad):
    out = []
    names = list(topics)
    for i, t in enumerate(names):
        out.append(f'{pad}"{t}": {{')
        levels = list(topics[t])
        for j, lv in enumerate(levels):
            lines = topics[t][lv]
            out.append(f'{pad}  "{lv}": [')
            for k, s in enumerate(lines):
                out.append(f'{pad}    ' + json.dumps(s, ensure_ascii=False) + (',' if k < len(lines) - 1 else ''))
            out.append(f'{pad}  ]' + (',' if j < len(levels) - 1 else ''))
        out.append(f'{pad}}}' + (',' if i < len(names) - 1 else ''))
    return out


def cmd_status(write=False):
    bad, total = 0, 0
    for name in BANKS:
        path = check.DIR / f'{name}.json'
        bank, problems = load(path), []
        start = len(bank_lines(bank))
        rows = []
        for f in fragments(name):
            try:
                added, skipped = merge(bank, name, load(f), Path(f).name, problems)
            except json.JSONDecodeError as e:
                problems.append(f'{Path(f).name}: not valid JSON: {e}')
                continue
            rows.append(f'    {Path(f).name}: +{added}' + (f' ({skipped} duplicates skipped)' if skipped else ''))
        more, _ = run_checks(name, bank)
        problems += more
        now = len(bank_lines(bank))
        total += now - start
        print(f'{name}: {start} -> {now} lines (+{now - start})' + (f', {len(problems)} problems' if problems else ''))
        print('\n'.join(rows)) if rows else None
        for p in problems[:40]:
            print('   ', p)
        bad += len(problems)
        if write and not problems:
            assert json.loads(dump(bank)) == bank
            path.write_text(dump(bank), encoding='utf-8')
    print(f'all: +{total} new lines')
    if write and bad:
        print('nothing written for banks with problems')
    return 1 if bad else 0


def main(argv):
    if not argv or argv[0] not in ('check', 'status', 'merge'):
        print(__doc__)
        return 2
    if argv[0] == 'check':
        return cmd_check(argv[1:])
    return cmd_status(write=argv[0] == 'merge')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
