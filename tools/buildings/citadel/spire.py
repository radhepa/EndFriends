"""The Lord's Spire: the Citadel's highest tower, with the Lord's end crystal burning on top.

One spiral stair winds round a solid core all the way up (the shaft's inside stays 5 x 5): the lower
stage has thick walls and corner buttresses, a gallery rings it at y = 20, the slimmer upper stage
(purpur-pillar corners, lancets) ends in the Lord's sanctum, and a crown of obsidian claws holds
the crystal. Obsidian shards float free around the upper stage.
"""
from kit import building

from citadel._parts import (BRICK, CHISELED, CRY, OBS, PILLAR, POLISHED, STAIR, WALL, PANE, arch, banner, eye,
                            put_stone, rod, shards, spiral, stair, stone)

N = 11
C = 5
GAL = 20            # gallery floor (stand at 21)
TOP = 38            # upper stage walls rise to here; sanctum y 34..38
SANCT = 33          # sanctum floor
H = 46


def ring_cells(lo, hi):
    """Cells on the ring of the square lo..hi (inclusive), with the inward facing."""
    for x in range(lo, hi + 1):
        for z in range(lo, hi + 1):
            if x in (lo, hi) or z in (lo, hi):
                f = 'south' if z == lo else 'north' if z == hi else 'east' if x == lo else 'west'
                yield x, z, f, x in (lo, hi) and z in (lo, hi)


@building('lords_spire', people='court', role='civic', size=(N, H, N), door=C,
          about='The Lord\'s Spire: the highest tower, a spiral stair round a glowing core up to the Lord\'s '
                'sanctum, a gallery at mid-height, obsidian shards floating round the slim upper stage, and the '
                'Lord\'s end crystal burning in a crown of obsidian claws on top.')
def lords_spire(b):
    # ---------------------------------------------------------------- base
    for x in range(N):
        for z in range(N):
            b.set(x, 0, z, OBS if x in (0, N - 1) or z in (0, N - 1) else POLISHED)
    for x, z, f, corner in ring_cells(0, N - 1):
        b.set(x, 1, z, OBS)
        b.set(x, 2, z, OBS)
        if corner:
            put_stone(b, x, 3, z)
        else:
            stair(b, x, 3, z, f)
    # lower stage: walls two thick (x, z = 1..2 and 8..9), up to the gallery floor
    for y in range(1, GAL):
        for x in range(1, 10):
            for z in range(1, 10):
                if x in (1, 2, 8, 9) or z in (1, 2, 8, 9):
                    b.set(x, y, z, OBS if y in (4, 12) and (x in (1, 9) or z in (1, 9)) else stone(x, y, z))
    # corner buttresses on the plinth, each crowned with an eye
    for cx, cz in ((0, 0), (10, 0), (0, 10), (10, 10)):
        sx = 1 if cx == 0 else -1
        sz = 1 if cz == 0 else -1
        for y in range(4, 15):
            put_stone(b, cx, y, cz)
            if y < 10:
                put_stone(b, cx + sx, y, cz)
                put_stone(b, cx, y, cz + sz)
        stair(b, cx + sx, 10, cz, 'south' if cz == 0 else 'north')
        stair(b, cx, 10, cz + sz, 'east' if cx == 0 else 'west')
        b.set(cx, 9, cz, OBS)
        b.set(cx, 15, cz, CHISELED)
        eye(b, cx, 16, cz, 'north' if cz == 0 else 'south')
    # ---------------------------------------------------------------- the core and the spiral stair
    for y in range(1, SANCT):
        for x in range(4, 7):
            for z in range(4, 7):
                glow = (x == C) != (z == C) and y % 4 == 2
                b.set(x, y, z, CRY if glow else OBS)
    treads = spiral(b, 3, 3, 5, 1, 1, SANCT, start='south', soffit=False)
    # ---------------------------------------------------------------- entrance: tall open arch on the north
    arch(b, 'x', C - 1, 3, 1, 5, 0, 2, rise=2, smooth=STAIR)
    b.set(C, 6, 0, CRY)
    eye(b, C, 7, 0, 'north')
    # ---------------------------------------------------------------- gallery at y = 20
    for x, z, f, corner in ring_cells(0, N - 1):
        if corner:
            for y in range(GAL - 2, GAL + 4):
                put_stone(b, x, y, z)
            b.set(x, GAL + 4, z, WALL)
            rod(b, x, GAL + 5, z)
            continue
        stair(b, x, GAL - 1, z, f, half='top')
        b.set(x, GAL, z, OBS)
        b.set(x, GAL + 1, z, WALL)
    for x, z, f, corner in ring_cells(1, N - 2):
        b.set(x, GAL, z, POLISHED)
    for x, z, f in ((C, 0, 'north'), (0, C, 'west'), (C, 10, 'south'), (10, C, 'east')):
        b.set(x, GAL + 1, z, OBS)
        eye(b, x, GAL + 2, z, f)
    # ---------------------------------------------------------------- upper stage: 7 x 7, purpur corners
    for y in range(GAL, TOP + 1):
        for x, z, f, corner in ring_cells(2, 8):
            if corner:
                b.set(x, y, z, PILLAR, axis='y')
            else:
                b.set(x, y, z, OBS if y % 5 == 0 else stone(x, y, z))
    # sanctum floor over the core, and the arrival from the stair
    for x in range(3, 8):
        for z in range(3, 8):
            if not b.solid(x, SANCT, z):
                b.set(x, SANCT, z, POLISHED)
    tread_cells = {(x, y, z) for cells, y, _ in treads for x, z in cells}
    for cells, y, facing in treads:
        for x, z in cells:
            for dy in range(1, 5):
                if y + dy >= SANCT and (x, y + dy, z) not in tread_cells:
                    b.erase(x, y + dy, z, x, y + dy, z)   # headroom up through the sanctum floor
    # lancets: lower stage through both wall layers, upper stage, sanctum
    for y in range(6, 11):
        for d in (1, 2):
            b.set(C, y, d, PANE) if d == 1 else b.set(C, y, d, 'magenta_stained_glass')
            b.set(d, y, C, PANE) if d == 1 else b.set(d, y, C, 'magenta_stained_glass')
            b.set(C, y, 10 - d, PANE) if d == 1 else b.set(C, y, 10 - d, 'magenta_stained_glass')
            b.set(10 - d, y, C, PANE) if d == 1 else b.set(10 - d, y, C, 'magenta_stained_glass')
    for y0, y1 in ((24, 31), (37, 39)):
        for y in range(y0, y1 + 1):
            for x, z in ((C, 2), (2, C), (C, 8), (8, C)):
                b.set(x, y, z, PANE)
    # gallery door: from the stair landing at the gallery floor out through the upper-stage wall
    land = [(cells, y) for cells, y, facing in treads if y == GAL]
    assert land, 'no stair tread at the gallery floor'
    (lx, lz), = land[0][0][:1]
    out = (lx - 1, lz) if lx == 3 else (lx + 1, lz) if lx == 7 else (lx, lz - 1) if lz == 3 else (lx, lz + 1)
    for y in range(GAL + 1, GAL + 5):
        b.erase(out[0], y, out[1], out[0], y, out[1])
    b.set(out[0], GAL, out[1], POLISHED)
    b.meta['gallery_door'] = list(out)
    # ---------------------------------------------------------------- the crown: stepped roof, claws, crystal
    for x in range(2, 9):
        for z in range(2, 9):
            edge = x in (2, 8) or z in (2, 8)
            if edge and not (x in (2, 8) and z in (2, 8)):
                f = 'south' if z == 2 else 'north' if z == 8 else 'east' if x == 2 else 'west'
                stair(b, x, TOP + 1, z, f)
            elif edge:
                b.set(x, TOP + 1, z, PILLAR, axis='y')
            else:
                b.set(x, TOP + 1, z, BRICK)
    for x in range(3, 8):
        for z in range(3, 8):
            edge = x in (3, 7) or z in (3, 7)
            if edge and not (x in (3, 7) and z in (3, 7)):
                f = 'south' if z == 3 else 'north' if z == 7 else 'east' if x == 3 else 'west'
                stair(b, x, TOP + 2, z, f)
            else:
                b.set(x, TOP + 2, z, OBS)
    for x in range(4, 7):
        for z in range(4, 7):
            b.set(x, TOP + 3, z, CRY if (x, z) == (C, C) else POLISHED)
    # four obsidian claws rise from the corners and curl in over the crystal
    for x, z in ((3, 3), (7, 3), (3, 7), (7, 7)):
        for y in range(TOP + 2, TOP + 6):
            b.set(x, y, z, OBS)
        ix, iz = x + (1 if x < C else -1), z + (1 if z < C else -1)
        b.set(ix, TOP + 6, iz, OBS)
        b.set(ix, TOP + 7, iz, CRY)
    for x, z in ((C, 3), (C, 7), (3, C), (7, C)):
        rod(b, x, TOP + 3, z)
    b.end_crystal(C, TOP + 4, C)          # the Lord's crystal, floating over the glowing stone
    # ---------------------------------------------------------------- shards of the void, floating free
    shards(b, C, C, 4.6, 5.6, GAL + 6, TOP + 4, 22, seed=40, kinds=(OBS, OBS, OBS, CRY))
    shards(b, C, C, 3.6, 5.2, TOP + 3, H - 1, 4, seed=41, kinds=(OBS, CRY))
    # ---------------------------------------------------------------- sanctum furnishings
    # the Lord's altar on the core top (off the stair ring): two eyes either side of a glowing stone
    b.set(C, SANCT, C + 1, CRY)
    eye(b, C - 1, SANCT + 1, C + 1, 'north')
    eye(b, C + 1, SANCT + 1, C + 1, 'north')
    banner(b, C, SANCT + 4, 3, 'south')
    rod(b, C, TOP, C, 'down')
    # ---------------------------------------------------------------- spots
    b.spot('stand', C, 1, 3)
    b.spot('stand', C, SANCT + 1, C)
    b.spot('stand', out[0], GAL + 1, out[1])
