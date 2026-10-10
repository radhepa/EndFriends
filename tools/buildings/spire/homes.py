"""Shulkin homes: lidded towers shaped like a shulker's shell (a drum, the glowing gap, the lid).

Shulkin stand 2.6 blocks tall: doorways are three high (door plus open transom), every room has at
least three clear blocks, and stairs (not ladders) join the floors so residents can reach their niches.
They sleep in lidded niches (carpet under a slab canopy), never beds.
"""
import math

from kit import building

from spire._parts import (DIRS4, OPP, band, column, doorway, edge, facing_out, gap_band, hang, heightfield, lip, octo, put,
                          rect, rings, shrink, stair_path, stair_roof)


def octagon(b, cx, cz, r, y, spec, hollow=False, **kw):
    """An octagon of 'radius' r (cells with |dx|,|dz| <= r and |dx|+|dz| <= r*1.45)."""
    cells = octo(cx, cz, r)
    put(b, edge(cells) if hollow else cells, y, spec, **kw)


def ring_level(cx, cz, x, z, rmax):
    """The smallest octagon radius containing (x, z) (0 = centre)."""
    for r in range(rmax + 1):
        if (x, z) in octo(cx, cz, r):
            return r
    return rmax + 1


def dome(b, cx, cz, r, y, profile, block='purpur_block', slab='purpur_slab'):
    """A lid: octagon of radius r whose ring i (0 = outermost) spans half-blocks from
    2*y + profile[i][0] to 2*y + profile[i][1]."""
    cols = {}
    for x, z in octo(cx, cz, r):
        i = r - ring_level(cx, cz, x, z, r)
        lo, hi = profile[min(i, len(profile) - 1)]
        cols[(x, z)] = (2 * y + lo, 2 * y + hi)
    heightfield(b, cols, block, slab)


def window(b, x, y, z, tall=2, pane='magenta_stained_glass_pane'):
    for h in range(tall):
        b.set(x, y + h, z, pane)


def face_windows(b, c, r, y, tall=2, skip=()):
    for d, (dx, dz) in DIRS4.items():
        if d in skip:
            continue
        window(b, c + dx * r, y, c + dz * r, tall)


def face_pillars(b, c, r, y0, y1):
    """Pillar pairs framing the middle of each octagon face."""
    for x, z in ((c - r, c - 1), (c - r, c + 1), (c + r, c - 1), (c + r, c + 1),
                 (c - 1, c - r), (c + 1, c - r), (c - 1, c + r), (c + 1, c + r)):
        for y in range(y0, y1 + 1):
            b.set(x, y, z, 'purpur_pillar', axis='y')


def plinth_lights(b, c, r, y=0):
    """Froglights set into the plinth on the four diagonals: they light the ground round the tower."""
    k = r + math.floor(r * 0.45)
    for sx in (-1, 1):
        for sz in (-1, 1):
            dx = (k + 1) // 2
            dz = k - dx
            b.set(c + sx * dx, y, c + sz * dz, 'pearlescent_froglight')


@building('spire_home', people='shulkin', role='home', size=(11, 24, 11), residents=2, door=5,
          about='A lidded tower for two: a purpur drum, the glowing gap where the shell opens, and an overhanging lid.')
def spire_home(b):
    c = 5
    R = 4
    plan = octo(c, c, R)
    inner = shrink(plan)
    # plinth: end stone bricks with a purpur floor, froglights on the diagonals
    octagon(b, c, c, 5, 0, 'end_stone_bricks')
    put(b, inner, 0, 'purpur_block')
    plinth_lights(b, c, 5)
    for x, z, f in ((c, c - 5, 'south'), (c, c + 5, 'north'), (c - 5, c, 'east'), (c + 5, c, 'west')):
        b.set(x, 0, z, 'end_stone_brick_slab', type='top')
    # the drum
    column(b, edge(plan), 1, 14, 'purpur_block')
    face_pillars(b, c, R, 1, 14)
    # the floors; their courses of plain block break the face pillars into storeys outside
    for y in (6, 11):
        put(b, edge(plan), y, 'purpur_block')
        put(b, inner, y, 'purpur_block')
    # windows on the faces of each floor (the north face has the door below)
    face_windows(b, c, R, 2, 2, skip=('north',))
    face_windows(b, c, R, 8, 2)
    face_windows(b, c, R, 13, 1)
    # the gap: an open shadow line with the glowing band set back in it
    gap_band(b, plan, 15, 16, every=2)
    # the lid: overhanging dome, a moulded lip under the overhang and a crest
    dome(b, c, c, 5, 17, [(0, 3), (0, 5), (0, 6), (0, 7), (0, 8), (0, 10)])
    lip(b, octo(c, c, 5), 17)
    b.set(c, 22, c, 'purpur_pillar', axis='y')
    b.end_rod(c, 23, c, 'up')
    # buttresses on the four diagonal faces carry the lid's overhang down to the plinth
    for sx in (-1, 1):
        for sz in (-1, 1):
            x, z = c + 3 * sx, c + 3 * sz
            for y in range(1, 17):
                b.set(x, y, z, 'purpur_pillar', axis='y')
            b.set(x, 0, z, 'end_stone_bricks')
            b.set(x + sx, 16, z, 'end_rod', facing='east' if sx > 0 else 'west')
            b.set(x, 16, z + sz, 'end_rod', facing='south' if sz > 0 else 'north')
    # a sloped skirt of end-stone-brick stairs where the drum meets the plinth
    for x, z in edge(octo(c, c, 5)):
        if not b.solid(x, 1, z) and (x, z) != (c, c - 5) and b.get(x, 0, z)[0] != 'minecraft:pearlescent_froglight':
            b.set(x, 1, z, 'end_stone_brick_slab', type='bottom')
    # the door (three blocks high) and its step
    doorway(b, c, 1, c - R, 'north')
    b.set(c, 0, c - 5, 'end_stone_brick_slab', type='top')
    # stairs: ground -> first floor up the south-east, first -> top floor up the north-west
    path1 = [(c - 1, c + 2), (c, c + 2), (c + 1, c + 2), (c + 2, c + 2), (c + 2, c + 1), (c + 2, c), (c + 2, c - 1)]
    stair_path(b, path1, 1)
    path2 = [(c + 1, c - 2), (c, c - 2), (c - 1, c - 2), (c - 2, c - 2), (c - 2, c - 1), (c - 2, c)]
    stair_path(b, path2, 7)
    b.set(c + 2, 6, c - 2, 'purpur_block')
    # railings round the stairwells
    for x, z in ((c, c + 1), (c + 1, c + 1)):
        b.set(x, 7, z, 'end_stone_brick_wall')
    for x, z in ((c - 1, c - 1), (c - 1, c)):
        b.set(x, 12, z, 'end_stone_brick_wall')

    # ---- ground floor: a niche in the west alcove, a table and seat, storage
    for z in (c - 1, c, c + 1):
        b.set(c - 3, 1, z, 'purple_carpet')
        b.set(c - 3, 4, z, 'purpur_slab', type='top')
    b.set(c - 3, 1, c - 1, 'purple_wool')
    b.spot('sleep', c - 3, 1, c + 1)
    b.candles(c - 3, 3, c - 2, 2)  # a candle on the sill (ledge) at the niche's head
    b.set(c - 3, 2, c - 2, 'purpur_block')
    b.set(c + 1, 1, c - 1, 'purpur_slab', type='top')
    b.candles(c + 1, 2, c - 1, 3, 'magenta')
    b.set(c + 1, 1, c, 'purpur_stairs', facing='south')
    b.spot('sit', c + 1, 1, c)
    b.set(c + 3, 1, c - 1, 'barrel', facing='west', open=False)
    b.set(c + 3, 1, c, 'barrel', facing='up', open=False)
    b.set(c + 3, 2, c, 'barrel', facing='up', open=False)
    hang(b, c, 5, c)
    hang(b, c - 2, 5, c + 2)
    # ---- first floor: a study (every Shulkin keeps records)
    b.set(c - 1, 7, c + 3, 'bookshelf')
    b.set(c + 1, 7, c + 3, 'bookshelf')
    b.set(c - 1, 8, c + 3, 'bookshelf')
    b.set(c + 1, 8, c + 3, 'bookshelf')
    b.set(c, 7, c + 3, 'lectern', facing='north', has_book=False, powered=False)
    b.set(c + 3, 7, c, 'chiseled_bookshelf', facing='west')
    b.fill(c - 1, 7, c, c, 7, c + 1, 'magenta_carpet')
    b.set(c - 3, 7, c - 1, 'purpur_stairs', facing='west')
    b.spot('sit', c - 3, 7, c - 1)
    hang(b, c, 10, c)
    b.end_rod(c - 3, 10, c + 1, 'east')
    # ---- top floor: the lamp room under the glowing gap, the second niche
    for x in (c - 1, c, c + 1):
        b.set(x, 12, c + 3, 'magenta_carpet')
        b.set(x, 15, c + 3, 'purpur_slab', type='top')
    b.set(c + 1, 12, c + 3, 'magenta_wool')
    b.spot('sleep', c - 1, 12, c + 3)
    b.fill(c, 12, c, c + 1, 12, c + 1, 'purple_carpet')
    b.set(c + 2, 12, c - 2, 'purpur_slab', type='top')
    b.candles(c + 2, 13, c - 2, 4, 'white')
    b.end_rod(c, 16, c, 'down')


def _ground(b, spec='end_stone_bricks'):
    """Draw the whole footprint's ground layer (what the islet would give anyway, so previews read)."""
    for x in range(b.w):
        for z in range(b.d):
            if not b.solid(x, b.ground, z):
                b.set(x, b.ground, z, spec)


@building('spire_home_tall', people='shulkin', role='home', size=(11, 30, 11), residents=3, door=5,
          about='A tall tower for three built as two stacked shells: a lower drum whose lid is a railed balcony '
                'carried on four buttresses, then a slimmer upper drum, its glowing gap and a great overhanging lid.')
def spire_home_tall(b):
    c = 5

    def P(dx, dz):
        return c + dx, c + dz

    low = octo(c, c, 4)                       # the lower drum, 9 wide
    up = octo(c, c, 3, k=5)                   # the upper drum, 7 wide with clipped corners
    deck = octo(c, c, 5)                      # the balcony: the lower shell's lid
    F1, F2, F3 = 6, 11, 16                    # floor layers (feet one above)
    # ---- plinth
    put(b, deck, 0, 'end_stone_bricks')
    put(b, shrink(low), 0, 'purpur_block')
    _ground(b, 'end_stone')
    for x, z in (P(-4, -3), P(4, -3), P(-4, 3), P(4, 3)):
        b.set(x, 0, z, 'pearlescent_froglight')
    # ---- the lower shell: drum, glowing gap, and the balcony as its lid, held up by buttresses
    column(b, edge(low), 1, 9, 'purpur_block')
    face_pillars(b, c, 4, 1, 9)
    band(b, edge(low), 10, 10, every=2, posts={P(dx, dz) for dx in (-1, 1) for dz in (-4, 4)} |
         {P(dx, dz) for dx in (-4, 4) for dz in (-1, 1)})
    for sx in (-1, 1):
        for sz in (-1, 1):
            x, z = P(3 * sx, 3 * sz)
            for y in range(1, 11):
                b.set(x, y, z, 'purpur_pillar', axis='y')
    put(b, deck, F2, 'purpur_block')
    lip(b, deck, F2 - 1)
    put(b, shrink(low), F1, 'purpur_block')
    # railing round the balcony, rods on the posts
    for x, z in edge(deck):
        b.set(x, F2 + 1, z, 'end_stone_brick_wall')
        if abs(x - c) + abs(z - c) == 7 or abs(x - c) + abs(z - c) == 5 and (x == c or z == c):
            b.end_rod(x, F2 + 2, z, 'up')
    # ---- the upper shell: drum, glowing gap, the great lid
    column(b, edge(up), F2 + 1, 19, 'purpur_block')
    for x, z in edge(up):
        if abs(x - c) + abs(z - c) == 5:
            for y in range(F2 + 1, 20):
                b.set(x, y, z, 'purpur_pillar', axis='y')
    put(b, shrink(up), F3, 'purpur_block')
    band(b, edge(up), 20, 21, every=2)
    dome(b, c, c, 5, 22, [(0, 3), (0, 5), (0, 6), (0, 7), (0, 8), (0, 10)])
    lip(b, deck, 22)
    b.set(c, 27, c, 'purpur_pillar', axis='y')
    b.set(c, 28, c, 'purpur_pillar', axis='y')
    b.end_rod(c, 29, c, 'up')
    # windows
    for d, (dx, dz) in DIRS4.items():
        for y in (2, 3, 7, 8):
            if not (d == 'north' and y < 5):
                b.set(c + 4 * dx, y, c + 4 * dz, 'magenta_stained_glass_pane')
        for y in (13, 14, 17, 18):
            if not (d == 'east' and y < 16):
                b.set(c + 3 * dx, y, c + 3 * dz, 'magenta_stained_glass_pane')
    # ---- doors: the front door, and one out onto the balcony
    doorway(b, c, 1, c - 4, 'north')
    b.set(c, 0, c - 5, 'end_stone_brick_slab', type='top')
    doorway(b, c + 3, F2 + 1, c, 'east', rods=False)
    # ---- stairs: two flights in the lower drum, one in the upper
    stair_path(b, [P(-1, 2), P(0, 2), P(1, 2), P(2, 2), P(2, 1), P(2, 0), P(2, -1)], 1)
    b.set(*P(2, -2)[:1], F1, P(2, -2)[1], 'purpur_block')
    stair_path(b, [P(1, -2), P(0, -2), P(-1, -2), P(-2, -2), P(-2, -1), P(-2, 0)], F1 + 1)
    stair_path(b, [P(-1, 2), P(0, 2), P(1, 2), P(2, 2), P(2, 1), P(2, 0)], F2 + 1)
    for x, z in (P(0, 1), P(1, 1)):
        b.set(x, F1 + 1, z, 'end_stone_brick_wall')
    for x, z in (P(-1, -1), P(-1, 0)):
        b.set(x, F2 + 1, z, 'end_stone_brick_wall')
    for x, z in (P(0, 1), P(1, 1)):
        b.set(x, F3 + 1, z, 'end_stone_brick_wall')

    # ---- ground floor: a niche in the west alcove, a table, storage
    for dz in (-1, 0, 1):
        x, z = P(-3, dz)
        b.set(x, 1, z, 'purple_carpet')
        b.set(x, 4, z, 'purpur_slab', type='top')
    b.set(*P(-3, -1)[:1], 1, P(-3, -1)[1], 'purple_wool')
    b.spot('sleep', *P(-3, 1)[:1], 1, P(-3, 1)[1])
    x, z = P(1, -1)
    b.set(x, 1, z, 'purpur_slab', type='top')
    b.candles(x, 2, z, 3, 'magenta')
    x, z = P(1, 0)
    b.set(x, 1, z, 'purpur_stairs', facing='south')
    b.spot('sit', x, 1, z)
    for dz in (-1, 0):
        x, z = P(3, dz)
        b.set(x, 1, z, 'barrel', facing='west', open=False)
    hang(b, c, 5, c)
    b.lantern(*P(-2, 2)[:1], 5, P(-2, 2)[1], hanging=True)
    # ---- first floor: the second niche in the south alcove, a study
    for dx in (-1, 0, 1):
        x, z = P(dx, 3)
        b.set(x, F1 + 1, z, 'magenta_carpet')
        b.set(x, F1 + 4, z, 'purpur_slab', type='top')
    b.set(*P(1, 3)[:1], F1 + 1, P(1, 3)[1], 'magenta_wool')
    b.spot('sleep', *P(-1, 3)[:1], F1 + 1, P(-1, 3)[1])
    x, z = P(-3, 0)
    b.set(x, F1 + 1, z, 'lectern', facing='east', has_book=False, powered=False)
    for dz in (-1, 1):
        b.set(*P(-3, dz)[:1], F1 + 1, P(-3, dz)[1], 'bookshelf')
        b.set(*P(-3, dz)[:1], F1 + 2, P(-3, dz)[1], 'bookshelf')
    x, z = P(3, 0)
    b.set(x, F1 + 1, z, 'chiseled_bookshelf', facing='west')
    b.lantern(*P(-1, 0)[:1], F2 - 1, P(-1, 0)[1], hanging=True)
    b.lantern(*P(1, 2)[:1], F2 - 1, P(1, 2)[1], hanging=True) if not b.solid(*P(1, 2)[:1], F2 - 1, P(1, 2)[1]) else None
    # ---- the landing (balcony level)
    b.lantern(*P(1, -1)[:1], F3 - 1, P(1, -1)[1], hanging=True)
    # ---- the top room under the glowing gap: the third niche along the west wall
    for dz in (-1, 0, 1):
        x, z = P(-2, dz)
        b.set(x, F3 + 1, z, 'purple_carpet')
        b.set(x, F3 + 4, z, 'purpur_slab', type='top')
    b.set(*P(-2, -1)[:1], F3 + 1, P(-2, -1)[1], 'purple_wool')
    b.spot('sleep', *P(-2, 1)[:1], F3 + 1, P(-2, 1)[1])
    x, z = P(0, -2)
    b.set(x, F3 + 1, z, 'purpur_slab', type='top')
    b.candles(x, F3 + 2, z, 4, 'white')
    b.end_rod(c, 21, c, 'down')


@building('spire_twin', people='shulkin', role='home', size=(25, 28, 11), residents=4, door=12,
          about='Two lidded towers of unequal height for four, joined at the base by a low entry hall and above it '
                'by an enclosed sky bridge, a glowing tube with its own little lid.')
def spire_twin(b):
    W, E = 5, 19                              # tower centres (x); both at z = 5
    cz = 5
    F1, F2, F3 = 5, 10, 15
    BR = F2                                   # the sky bridge's floor
    _ground(b, 'end_stone_bricks')

    def tower(cx, top_wall, band_y, lid_y, lid_kind):
        plan = octo(cx, cz, 4, k=6)
        put(b, shrink(plan), 0, 'purpur_block')
        column(b, edge(plan), 1, top_wall, 'purpur_block')
        put(b, edge(plan), 1, 'end_stone_bricks')
        for x, z in edge(plan):
            dx, dz = abs(x - cx), abs(z - cz)
            if dx + dz == 6 or (dx == 4 and dz == 1) or (dz == 4 and dx == 1):
                for y in range(1, band_y + (2 if dx + dz == 6 else 0)):
                    b.set(x, y, z, 'purpur_pillar', axis='y')
        band(b, edge(plan), band_y, band_y + 1, every=2,
             posts={c for c in edge(plan) if abs(c[0] - cx) + abs(c[1] - cz) == 6})
        lid = octo(cx, cz, 5, k=7)
        if lid_kind == 'dome':
            dome(b, cx, cz, 5, lid_y, [(0, 3), (0, 5), (0, 6), (0, 7), (0, 7), (0, 9)])
            lip(b, lid, lid_y)
        else:
            lip(b, lid, lid_y)
            put(b, lid - edge(lid), lid_y, 'purpur_block')
            tops = {cell: lid_y + 1 + min(i, 2) for cell, i in rings(lid).items()}
            stair_roof(b, tops, {cell: lid_y + 1 for cell in lid})
        for f in (F1, F2, F3):
            if f < top_wall:
                put(b, shrink(plan), f, 'purpur_block')
        for x, z in ((cx - 4, cz - 1), (cx - 4, cz + 1), (cx + 4, cz - 1), (cx + 4, cz + 1)):
            b.set(x, 0, z, 'end_stone_bricks')
        return plan

    def P(cx, dx, dz):
        return cx + dx, cz + dz

    # ---- the two towers: the west one taller with a domed lid, the east one with a box lid
    tower(W, 18, 19, 21, 'dome')
    tower(E, 14, 15, 17, 'box')
    b.set(W, 25, cz, 'purpur_pillar', axis='y')
    b.set(W, 26, cz, 'purpur_pillar', axis='y')
    b.end_rod(W, 27, cz, 'up')
    b.end_rod(E, 21, cz, 'up')
    for cx in (W, E):
        for d, (dx, dz) in DIRS4.items():
            for y in (2, 3, 7, 8):
                if not ((cx == W and d == 'east' or cx == E and d == 'west') and y < 5):
                    b.set(cx + 4 * dx, y, cz + 4 * dz, 'magenta_stained_glass_pane')
        for d in ('north', 'south'):
            dx, dz = DIRS4[d]
            b.set(cx, 12, cz + 4 * dz, 'magenta_stained_glass_pane')
            b.set(cx, 13, cz + 4 * dz, 'magenta_stained_glass_pane')
    for d in ('north', 'south', 'west'):
        dx, dz = DIRS4[d]
        b.set(W + 4 * dx, 17, cz + 4 * dz, 'magenta_stained_glass_pane')

    # ---- the entry hall between the towers (a low shell), the front door in its north wall
    put(b, rect(10, 3, 14, 7), 0, 'purpur_block')
    for x in range(10, 15):
        for z in (2, 8):
            for y in range(1, 4):
                b.set(x, y, z, 'purpur_block')
    for x in (10, 14):
        for z in (2, 8):
            for y in range(1, 5):
                b.set(x, y, z, 'purpur_pillar', axis='y')
    for x in range(11, 14):
        for z in (2, 8):
            b.set(x, 4, z, 'magenta_stained_glass' if x != 12 else 'pearlescent_froglight')
    hall_lid = rect(9, 1, 15, 9)
    lip(b, hall_lid, 5)
    put(b, shrink(hall_lid), 5, 'purpur_block')
    for x, z in edge(shrink(hall_lid)):
        d = facing_out(shrink(hall_lid), x, z)
        b.set(x, 6, z, 'purpur_stairs', facing=OPP[d], half='bottom')
    put(b, shrink(hall_lid, 2), 6, 'purpur_slab', type='bottom')
    doorway(b, 12, 1, 2, 'north')
    # arches from the hall into each tower's ground floor
    for x in (9, 15):
        for y in (1, 2, 3):
            b.set(x, y, cz, 'air')
    for x, f in ((9, None), (15, None)):
        b.set(x, 3, cz - 1, 'purpur_stairs', facing='south', half='top')
        b.set(x, 3, cz + 1, 'purpur_stairs', facing='north', half='top')
    hang(b, 12, 4, cz)
    b.set(11, 1, 7, 'purpur_stairs', facing='south')
    b.spot('sit', 11, 1, 7)
    b.set(13, 1, 7, 'purpur_stairs', facing='south')
    b.spot('sit', 13, 1, 7)
    b.set(12, 1, 7, 'purpur_slab', type='top')
    b.candles(12, 2, 7, 3, 'magenta')

    # ---- the sky bridge: an enclosed tube, a glowing band down each side, its own little lid
    tube = rect(10, cz - 2, 14, cz + 2)
    put(b, tube, BR, 'purpur_block')
    for x in range(10, 15):
        for z in (cz - 2, cz + 2):
            b.set(x, BR + 1, z, 'purpur_block')
            b.set(x, BR + 2, z, 'pearlescent_froglight' if x in (10, 12, 14) else 'magenta_stained_glass')
            b.set(x, BR + 3, z, 'purpur_block')
    blid = rect(9, cz - 3, 15, cz + 3)
    lip(b, blid, BR + 4)
    put(b, shrink(blid), BR + 4, 'purpur_block')
    for x in range(10, 15):
        b.set(x, BR + 5, cz - 2, 'purpur_stairs', facing='south', half='bottom')
        b.set(x, BR + 5, cz + 2, 'purpur_stairs', facing='north', half='bottom')
        b.set(x, BR + 5, cz - 1, 'purpur_stairs', facing='south', half='bottom')
        b.set(x, BR + 5, cz + 1, 'purpur_stairs', facing='north', half='bottom')
        b.set(x, BR + 5, cz, 'purpur_slab', type='bottom')
    # corbels under the bridge where it meets the towers
    for x, f in ((10, 'west'), (14, 'east')):
        for z in (cz - 1, cz, cz + 1):
            b.set(x, BR - 1, z, 'purpur_stairs', facing=f, half='top')
    for z in (cz - 1, cz, cz + 1):
        b.set(12, BR - 1, z, 'purpur_slab', type='top')
    # openings from the bridge into both towers
    for x in (9, 15):
        for z in (cz - 1, cz, cz + 1):
            for y in (BR + 1, BR + 2, BR + 3):
                b.set(x, y, z, 'air')

    # ---- stairs in both towers (ground -> first -> bridge floor), and up to the west tower's top room
    for cx in (W, E):
        stair_path(b, [P(cx, -1, 2), P(cx, 0, 2), P(cx, 1, 2), P(cx, 2, 2), P(cx, 2, 1), P(cx, 2, 0)], 1)
        stair_path(b, [P(cx, 1, -2), P(cx, 0, -2), P(cx, -1, -2), P(cx, -2, -2), P(cx, -2, -1), P(cx, -2, 0)], F1 + 1)
    stair_path(b, [P(W, -1, 2), P(W, 0, 2), P(W, 1, 2), P(W, 2, 2), P(W, 2, 1), P(W, 2, 0)], F2 + 1)

    # ---- west tower: ground floor (table, storage), first floor (a niche), bridge floor, top room (a niche)
    x, z = P(W, -1, -1)
    b.set(x, 1, z, 'purpur_slab', type='top')
    b.candles(x, 2, z, 3, 'purple')
    b.set(x - 1, 1, z, 'purpur_stairs', facing='west')
    b.spot('sit', x - 1, 1, z)
    for dz in (-1, 0, 1):
        b.set(*P(W, -3, dz)[:1], 1, P(W, -3, dz)[1], 'barrel', facing='east', open=False) if dz != 0 else None
    hang(b, W, 4, cz)
    for dz in (-1, 0, 1):
        x, z = P(W, -3, dz)
        b.set(x, F1 + 1, z, 'purple_carpet')
        b.set(x, F1 + 4, z, 'purpur_slab', type='top')
    b.set(*P(W, -3, -1)[:1], F1 + 1, P(W, -3, -1)[1], 'purple_wool')
    b.spot('sleep', *P(W, -3, 1)[:1], F1 + 1, P(W, -3, 1)[1])
    b.lantern(*P(W, 1, 0)[:1], F2 - 1, P(W, 1, 0)[1], hanging=True)
    b.lantern(*P(W, 0, 0)[:1], F3 - 1, P(W, 0, 0)[1], hanging=True)
    for dz in (-1, 0, 1):
        x, z = P(W, -3, dz)
        b.set(x, F3 + 1, z, 'magenta_carpet')
        b.set(x, F3 + 4, z, 'purpur_slab', type='top')
    b.set(*P(W, -3, 1)[:1], F3 + 1, P(W, -3, 1)[1], 'magenta_wool')
    b.spot('sleep', *P(W, -3, -1)[:1], F3 + 1, P(W, -3, -1)[1])
    x, z = P(W, 0, -3)
    b.set(x, F3 + 1, z, 'lectern', facing='south', has_book=False, powered=False)
    b.end_rod(W, F3 + 5, cz, 'down')
    # ---- east tower: ground floor, first floor (a niche), the top room at bridge level (a niche)
    x, z = P(E, 1, -1)
    b.set(x, 1, z, 'purpur_slab', type='top')
    b.candles(x, 2, z, 3, 'magenta')
    b.set(*P(E, 3, -1)[:1], 1, P(E, 3, -1)[1], 'barrel', facing='west', open=False)
    b.set(*P(E, 3, 1)[:1], 1, P(E, 3, 1)[1], 'chest', facing='west', type='single', waterlogged=False)
    hang(b, E, 4, cz)
    for dz in (-1, 0, 1):
        x, z = P(E, 3, dz)
        b.set(x, F1 + 1, z, 'purple_carpet')
        b.set(x, F1 + 4, z, 'purpur_slab', type='top')
    b.set(*P(E, 3, -1)[:1], F1 + 1, P(E, 3, -1)[1], 'purple_wool')
    b.spot('sleep', *P(E, 3, 1)[:1], F1 + 1, P(E, 3, 1)[1])
    b.lantern(*P(E, -1, 0)[:1], F2 - 1, P(E, -1, 0)[1], hanging=True)
    for dz in (-1, 0, 1):
        x, z = P(E, 3, dz)
        b.set(x, F2 + 1, z, 'magenta_carpet')
        b.set(x, F2 + 4, z, 'purpur_slab', type='top')
    b.set(*P(E, 3, 1)[:1], F2 + 1, P(E, 3, 1)[1], 'magenta_wool')
    b.spot('sleep', *P(E, 3, -1)[:1], F2 + 1, P(E, 3, -1)[1])
    x, z = P(E, 0, 3)
    b.set(x, F2 + 1, z, 'purpur_stairs', facing='south')
    b.spot('sit', x, F2 + 1, z)
    b.end_rod(E, 16, cz, 'down')


