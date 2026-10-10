"""Who lives in a planned village: one entry per resident or animal, from the building catalogue.

An entry is {"type": entity id (no namespace), "job": job id or "", "home": [x, y, z], "work": [x, y, z] (optional)},
in layout space (x, z from the village centre, y from the village floor), like the catalogue spots.
The game spawns each entry when the chunk holding its home generates (``ResidentPiece``).

Shulkin and Chorrin homes give one resident per sleep spot; the last one or two in a big home are
children. Every job building takes an adult of its people (the Crossing Hall takes one of each,
trade stalls take turns); adults left over keep shells (Shulkin) or gather (Chorrin). Pens and roosts
get their animals. A Citadel gets its Court by building: the Lord on the throne, the Herald at the
gate, Voidmarshals in the War Hall, a Seer, a Steward, Riftguards, thralls and hounds.
"""
import random
import zlib

# Job buildings: building -> (job, people or None for the building's own)
JOBS = {
    'archive': 'archivist', 'lamp_tower': 'lamplighter', 'weavers_loft': 'weaver', 'shellwright': 'shellwright',
    'driftray_roost': 'wayfinder', 'shell_nursery': 'keeper',
    'popping_kiln': 'kiln_keeper', 'grove_terraces': 'grove_tender', 'brewhouse': 'brewer',
    'stonecutters_yard': 'stonecutter', 'cooks_hearth': 'cook', 'blinkers_post': 'blinker', 'groveback_pen': 'herder',
}
IDLE = {'shulkin': 'keeper', 'chorrin': 'gatherer'}
ANIMALS = {'groveback_pen': ('groveback', 3), 'driftray_roost': ('driftray', 2)}
# Court posts: building -> [(type, job, spot kind, spot index)]
COURT = {
    'throne_hall': [('endarch_lord', 'lord', 'work', 0), ('endarch_marshal', 'steward', 'stand', 0),
                    ('endarch_riftguard', 'riftguard', 'stand', 1), ('endarch_riftguard', 'riftguard', 'stand', 2)],
    'gate_of_eyes': [('endarch_marshal', 'herald', 'work', 0), ('endarch_riftguard', 'riftguard', 'stand', 0),
                     ('endarch_riftguard', 'riftguard', 'stand', 1)],
    'war_hall': [('endarch_marshal', 'marshal', 'work', 0), ('endarch_marshal', 'marshal', 'work', 1)],
    'seers_spire': [('endarch_marshal', 'seer', 'work', 0)],
    'riftguard_barracks': [('endarch_riftguard', 'riftguard', 'work', i) for i in range(3)],
    'thrall_yards': [('enderman_thrall', 'thrall', 'work', i) for i in range(5)],
    'voidhound_kennels': [('voidhound', '', 'work', 0), ('voidhound', '', 'stand', 0), ('voidhound', '', 'work', 0)],
    'lords_spire': [('endarch_riftguard', 'riftguard', 'stand', 0)],
}


def spots(b, kind):
    return [s['pos'] for s in b['spots'] if s['kind'] == kind]


def anchor(b):
    """Somewhere to stand in a building: a work spot, else a stand or sit spot, else its middle."""
    for kind in ('work', 'stand', 'sit'):
        found = spots(b, kind)
        if found:
            return found[0]
    w, _, d = b['size']
    return [b['x'] + w // 2, b['top'] + 1, b['z'] + d // 2]


def entry(kind, job, home, work=None):
    out = {'type': kind, 'job': job, 'home': list(home)}
    if work:
        out['work'] = list(work)
    return out


def court(catalogue):
    out = []
    for b in catalogue['buildings']:
        for kind, job, spot, index in COURT.get(b['building'], []):
            found = spots(b, spot) or spots(b, 'stand') or spots(b, 'work')
            if not found:
                continue
            pos = found[min(index, len(found) - 1)]
            out.append(entry(kind, job, pos, pos))
    return out


def folk(catalogue, seed):
    rng = random.Random(seed)
    buildings = catalogue['buildings']
    plaza = next((anchor(b) for b in buildings if b['role'] == 'plaza'), [0, 1, 0])
    out, adults = [], {'shulkin': [], 'chorrin': []}
    # homes: a resident per sleep spot, children last in the bigger homes
    for b in buildings:
        if b['role'] != 'home':
            continue
        beds = spots(b, 'sleep')
        children = 2 if len(beds) >= 5 else 1 if len(beds) >= 3 else 1 if rng.random() < 0.25 else 0
        for i, bed in enumerate(beds):
            if i >= len(beds) - children:
                out.append(entry(f'{b["people"]}_child', '', bed, plaza))
            else:
                adults[b['people']].append(entry(b['people'], '', bed))
    # the Crossing Hall's two keepers live there: a Shulkin, then a Chorrin
    for b in buildings:
        if b['building'] == 'crossing_hall':
            beds, post = spots(b, 'sleep'), anchor(b)
            for bed, people in zip(beds, ('shulkin', 'chorrin')):
                out.append(entry(people, 'hallkeeper', bed, post))
    # job buildings take adults of their people; trade stalls alternate
    for people in adults:
        rng.shuffle(adults[people])
    turn = 0
    for b in buildings:
        job = JOBS.get(b['building'])
        people = b['people']
        if b['building'].startswith('trade_stall'):
            job, people = 'trader', ('shulkin', 'chorrin')[turn % 2]
            turn += 1
        if not job or people not in adults:
            continue
        free = [a for a in adults[people] if not a['job']]
        if not free:
            continue
        free[0]['job'] = job
        free[0]['work'] = anchor(b)
    for people, group in adults.items():
        for a in group:
            if not a['job']:
                a['job'] = IDLE[people]
                a['work'] = list(plaza)
        out += group
    # animals
    for b in buildings:
        if b['building'] in ANIMALS:
            kind, count = ANIMALS[b['building']]
            places = spots(b, 'stand') + spots(b, 'work') + spots(b, 'sit') or [anchor(b)]
            for i in range(count):
                out.append(entry(kind, '', places[i % len(places)]))
    return out


def roster(catalogue):
    seed = zlib.crc32(catalogue['layout'].encode())
    if catalogue['layout'].startswith('citadel'):
        return court(catalogue)
    return folk(catalogue, seed)
