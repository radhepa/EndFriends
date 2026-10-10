"""Development checks for Citadel buildings (not used by the planner).

  python tools/buildings/citadel/_checks.py [names...]     light + clearance report

Light: a rough block-light flood fill (no sky light in the End, so a walkable cell at block light 0
lets Endermen spawn). Clearance: open arches/doorways the Court walks through are at least 4 high.
"""
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import kit  # noqa: E402

EMIT = {'end_rod': 14, 'crying_obsidian': 10, 'lantern': 15, 'soul_lantern': 10, 'sea_lantern': 15,
        'glowstone': 15, 'beacon': 15, 'end_gateway': 15, 'amethyst_cluster': 5, 'large_amethyst_bud': 4,
        'medium_amethyst_bud': 2, 'small_amethyst_bud': 1, 'end_portal_frame': 1, 'magma_block': 3,
        'pearlescent_froglight': 15, 'ochre_froglight': 15, 'verdant_froglight': 15, 'shroomlight': 15}


def emission(state):
    name = kit.bid(state)
    if name.endswith('candle'):
        p = kit.props(state)
        return 3 * int(p.get('candles', 1)) if p.get('lit') == 'true' else 0
    return EMIT.get(name, 0)


def opaque(state):
    if kit.is_air(state):
        return False
    name = kit.bid(state)
    if 'glass' in name and name != 'tinted_glass':
        return False
    if name.endswith(('_stairs', '_slab')):
        return True  # conservative
    return kit.full_cube(state)


def cell(b, x, y, z):
    """The block at a cell, treating undrawn ground inside the footprint as end stone."""
    s = b.grid.get((x, y, z))
    if s is None and y <= b.ground and b.inside(x, y, z):
        return ('minecraft:end_stone', ())
    return s if s is not None else kit.AIR


def light_map(b, pad=4):
    level = {}
    q = deque()
    for pos, s in b.grid.items():
        e = emission(s)
        if e:
            level[pos] = e
            q.append(pos)
    while q:
        x, y, z = q.popleft()
        lv = level[(x, y, z)] - 1
        if lv <= 0:
            continue
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            n = (x + dx, y + dy, z + dz)
            if not (-pad <= n[0] < b.w + pad and -pad <= n[1] < b.h + pad and -pad <= n[2] < b.d + pad):
                continue
            if opaque(cell(b, *n)):
                continue
            if level.get(n, 0) < lv:
                level[n] = lv
                q.append(n)
    return level


def walkable(b):
    """Air cells inside the footprint with a full block below and air above."""
    out = []
    for z in range(b.d):
        for x in range(b.w):
            for y in range(b.ground + 1, b.h):
                here, below, above = cell(b, x, y, z), cell(b, x, y - 1, z), cell(b, x, y + 1, z)
                if kit.is_air(here) and kit.is_air(above) and kit.full_cube(below) and 'glass' not in below[0]:
                    out.append((x, y, z))
    return out


NO_COLLIDE = ('_carpet', '_pressure_plate', '_button', '_sign', '_banner', 'end_rod_x')


def passable(state):
    if kit.is_air(state):
        return True
    name = kit.bid(state)
    return name.endswith(NO_COLLIDE) or name in ('ladder', 'light', 'vine')


def floor(state):
    if kit.is_air(state) or passable(state):
        return False
    name = kit.bid(state)
    return kit.full_cube(state) or name.endswith(('_stairs', '_slab')) or name in (
        'end_portal_frame', 'lectern', 'stonecutter', 'chest', 'barrel', 'target', 'anvil', 'grindstone')


def reach(b, start, height=4, outside=1):
    """Cells an agent ``height`` blocks tall can walk to from ``start`` (stepping up or down one block
    at a time, falling up to three). The search may leave the footprint by ``outside`` cells over open
    ground (y = ground) so it can walk round to another door."""
    def ok(x, y, z):
        if not (-outside <= x < b.w + outside and -outside <= z < b.d + outside and 0 < y < b.h + 4):
            return False
        inside = b.inside(x, y, z)
        below = cell(b, x, y - 1, z) if b.inside(x, y - 1, z) else (('minecraft:end_stone', ()) if y - 1 == b.ground else kit.AIR)
        if not floor(below):
            return False
        for k in range(height):
            c = cell(b, x, y + k, z) if b.inside(x, y + k, z) else kit.AIR
            if not passable(c):
                return False
        return inside or y == b.ground + 1
    seen = {start}
    q = deque([start])
    while q:
        x, y, z = q.popleft()
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            for dy in (1, 0, -1, -2, -3):
                n = (x + dx, y + dy, z + dz)
                if n in seen or not ok(*n):
                    continue
                seen.add(n)
                q.append(n)
                break
    return seen


def check_paths(b, routes, height=4):
    """``routes``: list of (label, start, goal). Prints whether each goal is reachable."""
    ok = True
    for label, start, goal in routes:
        got = goal in reach(b, start, height)
        ok &= got
        print(f'   path {label}: {"ok" if got else "BLOCKED"} {start} -> {goal} (height {height})')
    return ok


FORBIDDEN = ('_bed', 'water', 'lava', 'spawner', 'trial_spawner')


def safety(b):
    """No portal-capable eye rings, no beds/water/lava/spawners, every spot standable. Returns problems."""
    problems = []
    frames = {}
    for (x, y, z), s in b.grid.items():
        name = kit.bid(s) if not kit.is_air(s) else ''
        if any(f in name for f in FORBIDDEN):
            problems.append(f'forbidden block {name} at {(x, y, z)}')
        if name == 'end_portal_frame':
            frames.setdefault(y, set()).add((x, z))
    for y, cells in frames.items():
        # a portal needs 12 frames on one layer round a 3x3 hole; flag any 5x5 window holding 9+ frames
        for x0 in range(-4, b.w):
            for z0 in range(-4, b.d):
                n = sum(1 for (x, z) in cells if x0 <= x < x0 + 5 and z0 <= z < z0 + 5)
                if n >= 9:
                    problems.append(f'{n} eye frames in one 5x5 window on layer {y} near {(x0, z0)}')
    for spot in b.meta.get('spots', []):
        x, y, z = spot['pos']
        if not (passable(cell(b, x, y, z)) and floor(cell(b, x, y - 1, z))):
            problems.append(f"spot {spot['kind']} at {(x, y, z)} is not standable ({kit.bid(cell(b, x, y, z)) if not kit.is_air(cell(b, x, y, z)) else 'air'} over {kit.bid(cell(b, x, y - 1, z)) if not kit.is_air(cell(b, x, y - 1, z)) else 'air'})")
    return problems


def report(b, show=12):
    lv = light_map(b)
    spots = walkable(b)
    dark = [p for p in spots if lv.get(p, 0) == 0]
    dim = [p for p in spots if 0 < lv.get(p, 0) < 6]
    print(f'{b.name}: {len(spots)} walkable cells, {len(dark)} dark (light 0), {len(dim)} dim (<6)')
    if dark:
        print('   dark:', ' '.join(f'{p}' for p in sorted(dark, key=lambda p: (p[1], p[2], p[0]))[:show]))
    return dark


MINE = ('citadel_wall', 'citadel_tower', 'gate_of_eyes', 'throne_hall', 'lords_spire', 'war_hall',
        'riftguard_barracks', 'seers_spire', 'thrall_yards', 'voidhound_kennels')

# (label, start, goal) per building; starts are just inside a door
ROUTES = {
    'citadel_tower': [('door to wall-walk room', (8, 1, 10), (5, 11, 8)),
                      ('wall-walk room to east opening', (5, 11, 8), (9, 11, 5)),
                      ('east door to south opening', (10, 1, 8), (5, 11, 9))],
    'throne_hall': [('door to the foot of the throne', (13, 1, 0), (13, 4, 25)),
                    ('door to the west aisle', (13, 1, 0), (5, 1, 13)),
                    ('door to the east aisle end', (13, 1, 0), (21, 1, 26))],
    'lords_spire': [('door to the sanctum', (5, 1, 0), (5, 34, 5))],
    'seers_spire': [('door to the observatory', (5, 1, 1), (3, 23, 4))],
    'riftguard_barracks': [('gate to the armoury', (8, 1, 0), (8, 1, 10)), ('gate to the targets', (8, 1, 0), (2, 1, 4))],
    'war_hall': [('door to the war table', (9, 1, 0), (9, 1, 11)), ('door to the racks', (9, 1, 0), (3, 1, 7))],
    'thrall_yards': [('gate to the shelters', (10, 1, 0), (4, 1, 13)), ('gate to the dais', (10, 1, 0), (10, 2, 7)),
                     ('gate to the far shelter', (10, 1, 0), (18, 1, 14))],
    'voidhound_kennels': [('door to the handler', (6, 1, 0), (6, 1, 8)), ('door into a stall', (6, 1, 0), (2, 1, 2)),
                          ('door into the far stall', (6, 1, 0), (10, 1, 8))],
    'gate_of_eyes': [('through the tunnel', (13, 1, 0), (13, 1, 10)),
                     ('wall-walk west to east', (0, 11, 5), (26, 11, 5)),
                     ('wall-walk to Herald balcony', (0, 11, 5), (13, 11, 1))],
}


if __name__ == '__main__':
    kit.load_all()
    names = sys.argv[1:] or [n for n, s in kit.CATALOG.items() if s['people'] == 'court' and n in MINE]
    for n in names:
        b = kit.make(n)
        report(b)
        if n in ROUTES:
            check_paths(b, ROUTES[n])
        for p in safety(b):
            print('   SAFETY:', p)
