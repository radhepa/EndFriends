"""Check the story books: src/main/resources/data/endexpansion/stories/*.json.

    python tools/stories/check.py            check every book, print counts
    python tools/stories/check.py chorrin    check one

The game reads the same files (dev.endexpansion.talk.StoryBook). One book per dialogue bank
(shulkin, chorrin, shulkin_child, chorrin_child, court):

    {
      "bank": "<file name>",
      "locked": ["what they say if you open Story before they know you", ...],   at least 3
      "personalities": [
        {"id": "patient", "label": "Patient", "about": "One sentence for the Journal.",
         "manner": "steady", "weight": 3, "jobs": []}
      ],
      "stories": [
        {
          "id": "unlit_lamp", "title": "The Unlit Lamp", "jobs": ["lamplighter"],
          "intro": "They bring it up (Story tab, chapter 1).",
          "requests": [
            {"id": "rods", "title": "New light", "item": "minecraft:end_rod", "count": 4,
             "prompt": "What they ask for.", "thanks": "What they say when you bring it."}
          ],
          "waiting": "After the first request, before they are ready to say more.",
          "ready": "When they are ready to tell you the rest.",
          "confide": "The heart of the story.",
          "endings": [
            {"id": "relight", "label": "Light it again", "text": "What they decide.", "memory": "For the Journal."},
            {"id": "let_rest", "label": "Let it rest", "text": "...", "memory": "..."}
          ],
          "gift": {"item": "minecraft:shulker_shell", "count": 1}
        }
      ]
    }

Grown-ups' stories have three requests (the first opens the story, the other two can be done any
time after), "waiting", "ready", "confide" and two "endings". Children's stories are short: one
request, then the gift; no waiting, ready, confide or endings.

Manners (how they behave while you talk to them):
    steady    stands still for as long as you like
    shy       keeps a step of distance; backs off if you crowd them
    restless  paces a step or two while talking, but stays
    busy      after a while excuses themselves and goes back to what they were doing
              (not once you are close friends: level 6+)
    flighty   Chorrin only: blinks a short hop now and then while talking
    proud     the Court only: ends the audience after a while unless your Favor is 4+
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'dialogue'))
from check import GENDERED, ITEMS  # noqa: E402  same gender rule and item list as the dialogue bank

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / 'src' / 'main' / 'resources' / 'data' / 'endexpansion' / 'stories'
BOOKS = ['shulkin', 'chorrin', 'shulkin_child', 'chorrin_child', 'court']
CHILD = {'shulkin_child', 'chorrin_child'}
MANNERS = {'steady', 'shy', 'restless', 'busy', 'flighty', 'proud'}
MUST_MANNERS = {
    'shulkin': {'steady', 'shy', 'restless', 'busy'},
    'chorrin': {'steady', 'restless', 'busy', 'flighty'},
    'shulkin_child': {'restless', 'shy', 'busy'},
    'chorrin_child': {'restless', 'flighty', 'busy'},
    'court': {'steady', 'restless', 'busy', 'proud'},
}
ONLY = {'flighty': {'chorrin', 'chorrin_child'}, 'proud': {'court'}}
JOBS = {
    'shulkin': ['archivist', 'lamplighter', 'weaver', 'shellwright', 'wayfinder', 'keeper', 'hallkeeper', 'trader'],
    'chorrin': ['grove_tender', 'kiln_keeper', 'stonecutter', 'cook', 'blinker', 'brewer', 'herder', 'gatherer',
                'hallkeeper', 'trader'],
    'court': ['lord', 'marshal', 'riftguard', 'herald', 'seer', 'steward'],
}
# how many stories each book needs, and how many of a grown-up book's must be tied to jobs
MIN_STORIES = {'shulkin': 8, 'chorrin': 8, 'shulkin_child': 5, 'chorrin_child': 5, 'court': 8}
MIN_JOB_STORIES = {'shulkin': 4, 'chorrin': 4}
COURT_JOB_STORIES = {'lord': 1, 'herald': 1, 'seer': 1, 'steward': 1, 'marshal': 2, 'riftguard': 2}
PLACEHOLDERS = {'player', 'name', 'village', 'neighbour', 'lord', 'title', 'job'}
# things nobody should ask for or hand over: creative-only, one of a kind, or far too much
NOT_ASKED = {'bedrock', 'barrier', 'command_block', 'chain_command_block', 'repeating_command_block',
             'command_block_minecart', 'structure_block', 'structure_void', 'jigsaw', 'light', 'debug_stick',
             'knowledge_book', 'petrified_oak_slab', 'end_portal_frame', 'reinforced_deepslate', 'budding_amethyst',
             'spawner', 'trial_spawner', 'vault', 'dragon_egg', 'player_head', 'test_block', 'test_instance_block',
             'farmland', 'dirt_path', 'frogspawn', 'infested_stone', 'suspicious_sand', 'suspicious_gravel'}
NOT_GIVEN = NOT_ASKED | {'elytra', 'nether_star', 'beacon', 'totem_of_undying', 'enchanted_golden_apple', 'netherite_block',
                         'netherite_ingot', 'netherite_scrap', 'ancient_debris', 'heavy_core', 'mace', 'dragon_head',
                         'trident', 'conduit', 'heart_of_the_sea', 'diamond_block', 'emerald_block', 'enchanted_book'}
LIMITS = {'label': 32, 'about': 120, 'title': 40, 'intro': 420, 'prompt': 240, 'thanks': 240, 'waiting': 300,
          'ready': 300, 'confide': 480, 'text': 420, 'memory': 120, 'locked': 200}
ID = re.compile(r'[a-z0-9_]{1,40}')


def text(where, s, kind, problems):
    if not isinstance(s, str) or not s.strip():
        problems.append(f'{where}: missing text')
        return
    if len(s) > LIMITS[kind]:
        problems.append(f'{where}: {len(s)} chars (max {LIMITS[kind]}): {s[:60]}...')
    for p in re.findall(r'\{([^}]*)\}', s):
        if p not in PLACEHOLDERS:
            problems.append(f'{where}: unknown placeholder {{{p}}}')
    if s.count('{') != s.count('}'):
        problems.append(f'{where}: unbalanced braces')
    m = GENDERED.search(s)
    if m:
        problems.append(f'{where}: gendered word "{m.group(0)}" (all End peoples are "they"): {s}')
    if '"' in s or '“' in s or '”' in s:
        problems.append(f'{where}: use single quotes inside text')
    if '\n' in s:
        problems.append(f'{where}: no line breaks')


def item(where, value, banned, problems):
    if not isinstance(value, str) or not value.startswith('minecraft:'):
        problems.append(f'{where}: item ids are "minecraft:<id>": {value!r}')
        return
    iid = value.removeprefix('minecraft:')
    if iid not in ITEMS:
        problems.append(f'{where}: unknown item "{value}"')
    if iid in banned or iid.endswith('_spawn_egg'):
        problems.append(f'{where}: "{value}" is not allowed here')


def check(name):
    path = DIR / f'{name}.json'
    problems = []
    try:
        book = json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:  # noqa: BLE001
        return [f'{path.name}: {e}'], 0, 0
    if book.get('bank') != name:
        problems.append(f'"bank" must be "{name}"')
    child = name in CHILD
    jobs = JOBS.get(name, [])

    locked = book.get('locked', [])
    if len(locked) < 3:
        problems.append('"locked" needs at least 3 lines')
    for i, s in enumerate(locked):
        text(f'locked[{i}]', s, 'locked', problems)

    persons = book.get('personalities', [])
    if len(persons) < (6 if name == 'court' else 3 if child else 5):
        problems.append(f'"personalities": too few ({len(persons)})')
    seen, manners, covered = set(), set(), set()
    for i, p in enumerate(persons):
        where = f'personalities[{i}]'
        pid = p.get('id', '')
        if not ID.fullmatch(pid) or pid in seen:
            problems.append(f'{where}: bad or repeated id {pid!r}')
        seen.add(pid)
        text(f'{where}.label', p.get('label'), 'label', problems)
        text(f'{where}.about', p.get('about'), 'about', problems)
        m = p.get('manner')
        if m not in MANNERS:
            problems.append(f'{where}: manner {m!r} must be one of {sorted(MANNERS)}')
        elif m in ONLY and name not in ONLY[m]:
            problems.append(f'{where}: manner "{m}" is only for {sorted(ONLY[m])}')
        manners.add(m)
        w = p.get('weight', 1)
        if not isinstance(w, int) or not 1 <= w <= 10:
            problems.append(f'{where}: weight must be 1..10')
        for j in p.get('jobs', []):
            if j not in jobs:
                problems.append(f'{where}: unknown job "{j}"')
            covered.add(j)
        if not p.get('jobs'):
            covered.update(jobs)
    for m in sorted(MUST_MANNERS[name] - manners):
        problems.append(f'"personalities": needs one with manner "{m}"')
    if name == 'court':
        for j in jobs:
            if j not in covered:
                problems.append(f'"personalities": no personality for job "{j}"')
        if not any(p.get('manner') == 'proud' and 'lord' in p.get('jobs', []) for p in persons):
            problems.append('"personalities": the lord needs a proud one')

    stories = book.get('stories', [])
    if len(stories) < MIN_STORIES[name]:
        problems.append(f'"stories": needs at least {MIN_STORIES[name]} (has {len(stories)})')
    ids, words = set(), 0
    job_stories = {j: 0 for j in jobs}
    tied = 0
    for i, s in enumerate(stories):
        sid = s.get('id', '')
        where = f'stories[{i}:{sid}]'
        if not ID.fullmatch(sid) or sid in ids:
            problems.append(f'{where}: bad or repeated id')
        ids.add(sid)
        text(f'{where}.title', s.get('title'), 'title', problems)
        text(f'{where}.intro', s.get('intro'), 'intro', problems)
        sj = s.get('jobs', [])
        if sj:
            tied += 1
        for j in sj:
            if j not in jobs:
                problems.append(f'{where}: unknown job "{j}"')
            else:
                job_stories[j] += 1
        if name == 'court' and not sj:
            problems.append(f'{where}: Court stories must name their jobs')
        reqs = s.get('requests', [])
        if len(reqs) != (1 if child else 3):
            problems.append(f'{where}: needs {1 if child else 3} request(s)')
        rids = set()
        for k, r in enumerate(reqs):
            rw = f'{where}.requests[{k}]'
            if not ID.fullmatch(r.get('id', '')) or r.get('id') in rids:
                problems.append(f'{rw}: bad or repeated id')
            rids.add(r.get('id'))
            text(f'{rw}.title', r.get('title'), 'title', problems)
            text(f'{rw}.prompt', r.get('prompt'), 'prompt', problems)
            text(f'{rw}.thanks', r.get('thanks'), 'thanks', problems)
            item(f'{rw}.item', r.get('item'), NOT_ASKED, problems)
            c = r.get('count')
            if not isinstance(c, int) or not 1 <= c <= 64:
                problems.append(f'{rw}: count must be 1..64')
            words += sum(len(str(r.get(f, '')).split()) for f in ('prompt', 'thanks'))
        if child:
            for f in ('waiting', 'ready', 'confide', 'endings'):
                if f in s:
                    problems.append(f'{where}: children\'s stories have no "{f}"')
        else:
            for f in ('waiting', 'ready', 'confide'):
                text(f'{where}.{f}', s.get(f), f, problems)
                words += len(str(s.get(f, '')).split())
            ends = s.get('endings', [])
            if len(ends) != 2:
                problems.append(f'{where}: needs exactly 2 endings')
            eids = set()
            for k, e in enumerate(ends):
                ew = f'{where}.endings[{k}]'
                if not ID.fullmatch(e.get('id', '')) or e.get('id') in eids:
                    problems.append(f'{ew}: bad or repeated id')
                eids.add(e.get('id'))
                text(f'{ew}.label', e.get('label'), 'label', problems)
                text(f'{ew}.text', e.get('text'), 'text', problems)
                text(f'{ew}.memory', e.get('memory'), 'memory', problems)
                words += len(str(e.get('text', '')).split())
        g = s.get('gift', {})
        item(f'{where}.gift', g.get('item'), NOT_GIVEN, problems)
        gc = g.get('count')
        if not isinstance(gc, int) or not 1 <= gc <= 16:
            problems.append(f'{where}.gift: count must be 1..16')
        words += len(str(s.get('intro', '')).split())
    if name in MIN_JOB_STORIES and tied < MIN_JOB_STORIES[name]:
        problems.append(f'"stories": at least {MIN_JOB_STORIES[name]} must be tied to jobs (has {tied})')
    if name in MIN_JOB_STORIES and len(stories) - tied < 3:
        problems.append('"stories": at least 3 must be for anyone (no "jobs")')
    if name == 'court':
        for j, n in COURT_JOB_STORIES.items():
            if job_stories.get(j, 0) < n:
                problems.append(f'"stories": the {j} needs at least {n} (has {job_stories.get(j, 0)})')
    titles = [s.get('title') for s in stories]
    for t in {t for t in titles if titles.count(t) > 1}:
        problems.append(f'repeated title: {t}')
    return problems, len(stories), words


def main():
    names = sys.argv[1:] or BOOKS
    bad = 0
    for name in names:
        problems, count, words = check(name)
        print(f'{name}: {count} stories, {words} words' + (f', {len(problems)} problems' if problems else ', ok'))
        for p in problems[:80]:
            print('   ', p)
        bad += len(problems)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
