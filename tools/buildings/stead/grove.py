"""The Stead's growing ground: the Grove Terraces, stepped beds of planted chorus climbing away from the
path, and the Groveback Pen, a round walled pasture with a feeding trough and a lean-to for the herd."""
import math

from kit import building
from stead._parts import chorus_tree, sprout, hanging_lantern, lantern_post, pot, stone_seat, ES, ESB, SLAB, STAIRS, WALL


# ------------------------------------------------------------------------------------ grove_terraces
@building('grove_terraces', people='chorrin', role='work', size=(15, 11, 13), ground=0, door=7, job='grove_tender',
          about='Three stepped beds of planted chorus climbing away from the path, a stair up the middle, '
                'lamps at the bed ends and the tender\'s composter by the gate.')
def grove_terraces(b):
    # the apron at the foot: paving, the composter (the tender's bench) and seed barrels
    b.fill(4, 0, 0, 10, 0, 1, ESB)
    b.set(5, 1, 1, 'composter', level=7)
    b.set(4, 1, 1, 'composter', level=3)
    b.spot('work', 6, 1, 1)
    b.barrel(9, 1, 1, facing='up')
    b.barrel(10, 1, 1, facing='west')
    b.barrel(9, 2, 1, facing='up')
    lantern_post(b, 3, 1, 0)
    lantern_post(b, 11, 1, 0)
    # three terraces, each one block higher: a walk along the front, a bed of end stone, a walk behind
    for k in (1, 2, 3):
        s = 2 + 3 * (k - 1)
        x0, x1 = k - 1, 14 - (k - 1)          # each bed a little narrower than the one below
        for z in range(s, 13):
            for x in range(x0, x1 + 1):
                b.fill(x, 0, z, x, k - 1, z, ESB)
                b.set(x, k, z, ESB)
        for x in range(x0, x1 + 1):
            b.set(x, k, s + 1, ES)
        # rounded ends: stairs down the sides of each bed
        for z in range(s, 13):
            for x, f in ((x0, 'east'), (x1, 'west')):
                if not b.solid(x, k + 1, z):
                    b.set(x, k, z, STAIRS, facing=f, half='bottom')
        # the stair up the middle
        b.set(7, k, s, STAIRS, facing='south', half='bottom')
        # chorus along the bed, leaving the middle clear: bushy plants (their arms start above head
        # height, clear of the walks) between short sprouts, taller toward the top
        for i, x in enumerate(range(x0 + 1, x1, 2)):
            if abs(x - 7) <= 1:
                continue
            if i % 2 == 0:
                chorus_tree(b, x, k + 1, s + 1, height=k + 3, arms=3, depth=1, low=2)
            else:
                sprout(b, x, k + 1, s + 1, 1 + (k > 1))
        # lamps at the ends of each front walk
        lantern_post(b, x0 + 1, k + 1, s)
        lantern_post(b, x1 - 1, k + 1, s)
    # the top: a stone bench under the back wall to look out over the grove
    for x in range(3, 12):
        b.set(x, 4, 12, WALL)
    for x in (5, 9):
        stone_seat(b, x, 4, 11, 'south')
    b.set(7, 4, 11, SLAB, type='top')
    b.candles(7, 5, 11, 3, color='white')
    pot(b, 4, 4, 11, 'north')
    b.barrel(10, 4, 11, facing='up')


# ------------------------------------------------------------------------------------- groveback_pen
def _ellipse(cx, cz, rx, rz):
    return {(x, z) for x in range(math.floor(cx - rx), math.ceil(cx + rx) + 1)
            for z in range(math.floor(cz - rz), math.ceil(cz + rz) + 1)
            if ((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2 <= 1.0}


@building('groveback_pen', people='chorrin', role='work', size=(15, 7, 13), ground=0, door=7,
          about='A round pasture walled in low end-stone wall, with a pale oak gate, a long stone feeding '
                'trough, patches of chorus to graze and a lean-to for the Groveback herd.')
def groveback_pen(b):
    cx, cz = 7, 6
    inside = _ellipse(cx, cz, 7.0, 6.0)
    # the wall: every inside cell touching the outside (8 ways), so the ring has no diagonal gaps
    ring = {(x, z) for (x, z) in inside
            if any((x + dx, z + dz) not in inside for dx in (-1, 0, 1) for dz in (-1, 0, 1))}
    for (x, z) in ring:
        b.set(x, 1, z, WALL)
    b.set(cx, 1, 0, 'pale_oak_fence_gate', facing='north', in_wall=True, open=False, powered=False)
    # posts with lamps round the ring
    for deg in range(0, 360, 45):
        a = math.radians(deg + 22.5)
        x, z = round(cx + 7 * math.sin(a)), round(cz - 6 * math.cos(a))
        best = min(ring, key=lambda c: (c[0] - x) ** 2 + (c[1] - z) ** 2)
        b.set(best[0], 2, best[1], WALL)
        b.lantern(best[0], 3, best[1])
    for x in (cx - 1, cx + 1):          # the gateposts stand a block taller
        if (x, 0) in ring:
            b.set(x, 2, 0, WALL)
    # the floor of the pen: worn end stone with brick paving by the gate and round the trough
    for (x, z) in inside - ring:
        b.set(x, 0, z, ES)
    b.fill(cx - 1, 0, 1, cx + 1, 0, 2, ESB)
    # the feeding trough along the east side: a stone channel with fodder in it
    for z in range(4, 9):
        b.set(12, 0, z, ESB)
        b.set(11, 1, z, STAIRS, facing='west', half='bottom')
        b.set(12, 1, z, 'brown_carpet')
        if (13, z) not in ring:
            b.set(13, 1, z, ESB)
    b.set(12, 1, 3, STAIRS, facing='north', half='bottom')
    b.set(12, 1, 9, STAIRS, facing='south', half='bottom')
    b.spot('work', 10, 1, 6)
    # the lean-to against the south wall: open to the north, a sloped stone roof with chorus on it,
    # bedding of brown fibre underneath
    for x in range(4, 11):
        for z in range(9, 12):
            if (x, z) in inside:
                b.set(x, 0, z, ESB)
    for x, z in ((5, 9), (9, 9)):
        b.fill(x, 1, z, x, 2, z, WALL)
    for x in range(5, 10):
        b.fill(x, 1, 11, x, 2, 11, ESB)
    for x in (4, 10):
        b.fill(x, 1, 10, x, 2, 10, ESB)
    for x in range(4, 11):
        b.set(x, 3, 8, STAIRS, facing='south', half='bottom')
        for z in range(9, 12):
            if 5 <= x <= 9:
                b.set(x, 3, z, ES)
            else:
                b.set(x, 3, z, STAIRS, facing='east' if x == 4 else 'west', half='bottom')
    for x in range(6, 9):
        for z in (9, 10):
            b.set(x, 1, z, 'brown_carpet')
    hanging_lantern(b, 7, 2, 10, chain=0)
    sprout(b, 6, 4, 10, 2)
    sprout(b, 8, 4, 11, 1)
    # grazing: patches of low chorus
    for x, z, h in ((5, 3, 1), (4, 4, 2), (9, 3, 1), (10, 10, 1), (6, 7, 2), (3, 6, 1), (2, 8, 2)):
        if (x, z) in inside and not b.solid(x, 1, z):
            b.set(x, 0, z, ES)
            sprout(b, x, 1, z, h)
