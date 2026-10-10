"""Check the dialogue bank: src/main/resources/data/endexpansion/dialogue/*.json.

    python tools/dialogue/check.py            check every bank, print counts
    python tools/dialogue/check.py chorrin    check one

The game reads the same files (dev.endexpansion.talk.DialogueBank). A bank is

    {
      "bank": "<file name>",
      "levels": [11 names, for friendship (or Favor) levels 0..10],      adult banks only
      "names":  [first names, one pool for the whole people],          adult banks only
      "places": [village names],                                       adult banks only
      "topics": {"<topic>": {"<min level>": ["line", ...]}},
      "jobs":   {"<job>": {"<min level>": [...]}},                      folk adult banks only
      "ranks":  {"<rank>": {"<topic>": {"<min level>": [...]}}},        court only
      "gifts":  {"loved": [item ids], "liked": [...], "disliked": [...]}
    }

For a level L the game uses the lines under the largest key <= L, so every topic needs "0".
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / 'src' / 'main' / 'resources' / 'data' / 'endexpansion' / 'dialogue'
ITEMS = set((Path(__file__).parent / 'item_ids.txt').read_text().split())

GIFTS = ['gift_loved', 'gift_liked', 'gift_neutral', 'gift_disliked', 'gift_limit']
FOLK = ['first_meeting', 'greeting', 'night', 'hurt', 'chat', 'dragon', 'village', 'other', 'court',
        'overworld', 'shulker_box', 'eyes', 'level_up', 'walk_off', 'busy_off', 'apology_accepted', 'apology_wary'] + GIFTS
TRIBUTE = ['tribute_loved', 'tribute_liked', 'tribute_neutral', 'tribute_disliked', 'tribute_limit']
COURT = ['first_meeting', 'greeting', 'chat', 'law', 'dragon', 'thralls', 'secret', 'shulkin', 'chorrin',
         'service_offer', 'service_waiting', 'service_done', 'level_up', 'alarm', 'broken_law', 'eyes_lost',
         'battle', 'thrall', 'hound_offer', 'hound_given', 'hound_already', 'hound_low', 'dismissed'] + TRIBUTE
REQUIRED = {
    'shulkin': FOLK + ['work', 'ancestors'],
    'chorrin': FOLK + ['work', 'void'],
    'shulkin_child': FOLK + ['play', 'ancestors'],
    'chorrin_child': FOLK + ['play', 'void'],
    'court': COURT,
}
JOBS = {
    'shulkin': ['archivist', 'lamplighter', 'weaver', 'shellwright', 'wayfinder', 'keeper', 'hallkeeper', 'trader'],
    'chorrin': ['grove_tender', 'kiln_keeper', 'stonecutter', 'cook', 'blinker', 'brewer', 'herder', 'gatherer',
                'hallkeeper', 'trader'],
}
RANKS = ['lord', 'marshal', 'riftguard', 'herald', 'seer', 'steward']
RANK_MUST = {'lord': ['greeting', 'chat', 'hound_offer', 'hound_given', 'dismissed'], 'herald': ['greeting', 'alarm', 'first_meeting'],
             'marshal': ['greeting', 'chat', 'dismissed'], 'riftguard': ['greeting', 'chat'], 'seer': ['greeting', 'chat', 'secret'],
             'steward': ['greeting', 'chat', 'service_offer', 'dismissed']}
PLACEHOLDERS = {'player', 'name', 'village', 'neighbour', 'job', 'task', 'lord', 'title'}
# No genders for any End people: everyone is "they".
GENDERED = re.compile(r"\b(he|she|him|her|hers|his|himself|herself|mother|father|brother|sister|son|daughter|husband|"
                      r"wife|king|queen|lady|ladies|sir|madam|man|woman|men|women|boy|girl|boys|girls|mr|mrs|ms|"
                      r"mum|mom|dad|grandmother|grandfather|grandma|grandpa|aunt|uncle|niece|nephew|prince|princess|"
                      r"lordship|ladyship|gentleman|gentlemen|maiden|fellow)\b", re.IGNORECASE)
MAX_LEN = 200


def lines_of(table, where, problems):
    """A {"<min level>": [lines]} table: returns its lines, reporting shape problems."""
    out = []
    if not isinstance(table, dict) or not table:
        problems.append(f'{where}: must be a non-empty {{"<min level>": [lines]}} object')
        return out
    if '0' not in table:
        problems.append(f'{where}: needs a "0" level')
    for key, lines in table.items():
        if not key.isdigit() or not 0 <= int(key) <= 10:
            problems.append(f'{where}: level key {key!r} must be 0..10')
        if not isinstance(lines, list) or not lines or not all(isinstance(s, str) for s in lines):
            problems.append(f'{where}.{key}: must be a non-empty list of strings')
            continue
        out += [(f'{where}.{key}', s) for s in lines]
    return out


def check_line(where, s, problems):
    if not s.strip():
        problems.append(f'{where}: empty line')
    if len(s) > MAX_LEN:
        problems.append(f'{where}: {len(s)} chars (max {MAX_LEN}): {s[:60]}...')
    for p in re.findall(r'\{([^}]*)\}', s):
        if p not in PLACEHOLDERS:
            problems.append(f'{where}: unknown placeholder {{{p}}} in: {s}')
    if s.count('{') != s.count('}'):
        problems.append(f'{where}: unbalanced braces: {s}')
    m = GENDERED.search(s)
    if m:
        problems.append(f'{where}: gendered word "{m.group(0)}" (all End peoples are "they"): {s}')
    if '"' in s or '“' in s:
        problems.append(f'{where}: use single quotes inside lines: {s}')


def check(name):
    path = DIR / f'{name}.json'
    problems = []
    try:
        bank = json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:  # noqa: BLE001
        return [f'{path.name}: {e}'], 0
    if bank.get('bank') != name:
        problems.append(f'"bank" must be "{name}"')
    adult = name in ('shulkin', 'chorrin', 'court')
    if adult:
        if len(bank.get('levels', [])) != 11:
            problems.append('"levels" needs 11 names (levels 0..10)')
        names = bank.get('names', [])
        if len(names) < 60 or len(set(names)) != len(names):
            problems.append(f'"names" needs at least 60 different names (has {len(set(names))})')
        if len(bank.get('places', [])) < 24:
            problems.append('"places" needs at least 24 village names')
        for n in names:
            if not re.fullmatch(r"[A-Z][a-z']+", n):
                problems.append(f'name {n!r}: one capitalised word')
    lines = []
    topics = bank.get('topics', {})
    for t in REQUIRED[name]:
        if t not in topics:
            problems.append(f'missing topic "{t}"')
    for t, table in topics.items():
        if t not in REQUIRED[name]:
            problems.append(f'unknown topic "{t}"')
        lines += lines_of(table, f'topics.{t}', problems)
    if name in JOBS:
        jobs = bank.get('jobs', {})
        for j in JOBS[name]:
            if j not in jobs:
                problems.append(f'missing job "{j}"')
        for j, table in jobs.items():
            if j not in JOBS[name]:
                problems.append(f'unknown job "{j}"')
            lines += lines_of(table, f'jobs.{j}', problems)
    if name == 'court':
        ranks = bank.get('ranks', {})
        for r in RANKS:
            for t in RANK_MUST[r]:
                if t not in ranks.get(r, {}):
                    problems.append(f'rank "{r}" must override "{t}"')
        for r, table in ranks.items():
            if r not in RANKS:
                problems.append(f'unknown rank "{r}"')
            for t, levels in table.items():
                if t not in COURT:
                    problems.append(f'ranks.{r}: unknown topic "{t}"')
                lines += lines_of(levels, f'ranks.{r}.{t}', problems)
    gifts = bank.get('gifts', {})
    seen = set()
    for kind in ('loved', 'liked', 'disliked'):
        ids = gifts.get(kind, [])
        if len(ids) < 3:
            problems.append(f'gifts.{kind}: at least 3 item ids')
        for i in ids:
            iid = i.removeprefix('minecraft:')
            if iid not in ITEMS:
                problems.append(f'gifts.{kind}: unknown item "{i}"')
            if iid in seen:
                problems.append(f'gifts: "{i}" listed twice')
            seen.add(iid)
    for where, s in lines:
        check_line(where, s, problems)
    texts = [s for _, s in lines]
    dupes = {s for s in texts if texts.count(s) > 1}
    for s in sorted(dupes):
        problems.append(f'duplicate line: {s}')
    return problems, len(lines)


def main():
    names = sys.argv[1:] or list(REQUIRED)
    bad = 0
    for name in names:
        problems, count = check(name)
        print(f'{name}: {count} lines' + (f', {len(problems)} problems' if problems else ', ok'))
        for p in problems[:80]:
            print('   ', p)
        bad += len(problems)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
