"""The Citadel's curtain wall and corner towers.

THE WALL LINE (for the planner)
  * ``citadel_wall`` is one straight segment, 9 wide (x) x 15 tall x 5 deep (z), outside face north
    (z = 0). It is periodic: copies placed side by side every 9 blocks (x = 0 of the next against
    x = 8 of this one) join seamlessly. Turn it to run along other sides; the outside turns with it.
  * Its walkway (wall-walk) floor is layer y = 10 at local z = 1..3 (you stand at y = 11), with the
    parapet at z = 0 and a rail at z = 4.
  * ``citadel_tower`` (11 x 34 x 11) is the north-west corner tower as drawn: its outside faces are
    north (z = 0) and west (x = 0). The two wall sides attach to its EAST face (x = 10; the north wall
    runs east from x = 11) and its SOUTH face (z = 10; the west wall runs south from z = 11), on the
    middle cells 3..7 of each face. The tower already carries one column of wall profile on those
    cells, and walkway openings at the same y and z, so the wall-walks run straight into it.
  * Placement rule shared by every wall-line piece (tower, wall, gate): the wall's 5-deep profile
    sits on local z = 3..7, i.e. a wall segment's z = 0 is at the tower's (or gate's) z = 3.
  * A closed square with k tiles per side measures 22 + 9k on each side: towers at the corners
    (NW as drawn, NE = turned 1, SE = turned 2, SW = turned 3), k segments between them, and the
    27-wide ``gate_of_eyes`` (gate.py) standing in for 3 of the k segments on one side.
    ``citadel/_view.py --square k`` builds and renders exactly that.
  * The towers' ground doors are on the inner corner: south face x = 8 and east face z = 8 (1 wide,
    4 high), so paths should reach (8, 0, 11) or (11, 0, 8), not the catalogue door on the north face.
"""
from kit import Build, building

from citadel._parts import (BRICK, CHISELED, CRY, OBS, POLISHED, STAIR, WALL, GLASS, PANE, WALK_FLOOR, arch, banner,
                            chain, eye, fill_stone, put_stone, rod, slab, spiral, spire_cap, stair, stone)


# --------------------------------------------------------------------------- the wall segment
def draw_wall(b):
    """One 9 x 15 x 5 wall segment into ``b`` (outside north). Symmetric about x = 4."""
    W, F = 9, WALK_FLOOR
    # footing under everything
    for x in range(W):
        for z in range(5):
            b.set(x, 0, z, OBS if z == 0 else BRICK)
    # body: outer face z = 1, core z = 2..3, inner face z = 4
    fill_stone(b, 0, 1, 1, W - 1, F - 1, 4)
    # obsidian string courses on the outer face
    for x in range(W):
        b.set(x, 5, 1, OBS)
    # battered plinth and the joint buttresses (x = 0 and x = 8 make a 2-wide buttress between segments)
    for x in range(W):
        b.set(x, 1, 0, OBS)
        b.set(x, 2, 0, OBS)
        if x in (0, W - 1):
            for y in range(3, F):
                put_stone(b, x, y, 0)
            b.set(x, 5, 0, OBS)
        else:
            stair(b, x, 3, 0, 'south')
            # machicolation corbels under the parapet
            stair(b, x, F - 1, 0, 'south', half='top')
    # buttress weathering: a stair step where each buttress meets the parapet's corbel table
    # the glowing slit and the eye beneath it, at the bay's centre
    for y in range(4, 8):
        b.set(4, y, 1, GLASS)
        b.set(4, y, 2, CRY)
    b.set(4, 8, 1, CHISELED)
    eye(b, 4, 3, 0, 'north')
    # parapet, merlons (2 wide, crenels at x = 1, 4, 7), peaked caps
    for x in range(W):
        for y in range(F, F + 3):
            put_stone(b, x, y, 0)
    b.set(4, F + 1, 0, CHISELED)
    for x in range(W):
        if x % 3 == 1:
            continue
        put_stone(b, x, F + 3, 0)
        stair(b, x, F + 4, 0, 'east' if x % 3 == 2 or x == W - 1 else 'west')
    # the watching eye in the centre crenel
    eye(b, 4, F + 3, 0, 'north')
    # walkway floor with a crying-obsidian inlay, rail with end-post piers on the inside
    for x in range(W):
        for z in (1, 2, 3):
            b.set(x, F, z, POLISHED)
    b.set(4, F, 2, CRY)
    for x in range(W):
        put_stone(b, x, F, 4)
        if x in (0, W - 1):
            put_stone(b, x, F + 1, 4)
            slab(b, x, F + 2, 4)
        else:
            b.set(x, F + 1, 4, WALL)
    rod(b, 4, F + 2, 4)
    # inner face: a blind pointed arch per bay, banners and a glowing panel in it
    arch(b, 'x', 2, 5, 1, 7, 4, 4, smooth=STAIR)
    for y in range(1, 6):
        b.set(4, y, 3, CRY if y in (1, 2, 4, 5) else OBS)
    banner(b, 3, 6, 4, 'south')
    banner(b, 5, 6, 4, 'south')
    for x in (1, 7):
        b.set(x, F - 1, 4, CHISELED)


@building('citadel_wall', people='court', role='wall', size=(9, 15, 5), door=4, tile=9, outside='north',
          walk_y=WALK_FLOOR + 1, walk_z=(1, 3),
          about='One bay of the Citadel curtain wall: a battered obsidian plinth, a glowing magenta slit, '
                'machicolated parapet with an eye in the centre crenel, and a lit wall-walk behind it.')
def citadel_wall(b):
    draw_wall(b)


def wall_segment():
    """A fresh drawn (unfinished) wall segment, for pieces that carry the wall's profile."""
    w = Build('wall_profile', (9, 15, 5))
    draw_wall(w)
    return w


def wall_stub(b, east_x, south_z, lo=3):
    """Copy one column of wall profile onto a tower's east face (x = east_x, z = lo..lo+4) and its
    south face (z = south_z, x = lo..lo+4), so the next wall segment joins it seamlessly."""
    w = wall_segment()
    if east_x is not None:
        for (x, y, z), s in w.grid.items():
            if x == 8:
                b.set(east_x, y, lo + z, s, nbt=w.nbt.get((x, y, z)))
    if south_z is not None:
        t = w.turned(3)           # outside west; its z = 8 row is the wall's x = 0 column
        for (x, y, z), s in t.grid.items():
            if z == 8:
                b.set(lo + x, y, south_z, s, nbt=t.nbt.get((x, y, z)))


# --------------------------------------------------------------------------- the corner tower
def _ring(n):
    """Cells on the outer ring of an n x n square, with the inward facing for each."""
    out = []
    for x in range(n):
        for z in range(n):
            if x in (0, n - 1) or z in (0, n - 1):
                corner = x in (0, n - 1) and z in (0, n - 1)
                f = 'south' if z == 0 else 'north' if z == n - 1 else 'east' if x == 0 else 'west'
                out.append((x, z, f, corner))
    return out


TOWER_TOP = 20                    # shaft walls rise to this layer; crown deck on it


@building('citadel_tower', people='court', role='wall', size=(11, 34, 11), door=5, outside=('north', 'west'),
          joins=('east', 'south'), join_cells=(3, 7), walk_y=WALK_FLOOR + 1, inner_doors=((8, 1, 10), (10, 1, 8)),
          about='The corner tower: battered obsidian base, a shaft with glowing slits and corner buttresses '
                'crowned by eyes, a machicolated crown with pinnacles and a steep black spire. Walls join its east '
                'and south faces; a spiral stair inside climbs to the wall-walk.')
def citadel_tower(b):
    N, F, T = 11, WALK_FLOOR, TOWER_TOP
    # floor: polished with an obsidian/crying-obsidian centre
    for x in range(N):
        for z in range(N):
            b.set(x, 0, z, OBS if x in (0, N - 1) or z in (0, N - 1) else POLISHED)
    # battered base: an obsidian ring two high, then a sloped course
    for x, z, f, corner in _ring(N):
        b.set(x, 1, z, OBS)
        b.set(x, 2, z, OBS)
        if corner:
            put_stone(b, x, 3, z)
        else:
            stair(b, x, 3, z, f)
    # the shaft: 9 x 9 (x, z = 1..9), interior 7 x 7, obsidian courses
    for y in range(1, T + 1):
        for x in range(1, 10):
            for z in range(1, 10):
                if x in (1, 9) or z in (1, 9):
                    b.set(x, y, z, OBS if y in (4, F, 16) else stone(x, y, z))
    # clasping corner buttresses (L-shaped), stepped, each carrying a watching eye
    for cx, cz in ((0, 0), (10, 0), (0, 10), (10, 10)):
        sx = 1 if cx == 0 else -1
        sz = 1 if cz == 0 else -1
        for y in range(4, 12):
            put_stone(b, cx, y, cz)
            if y < 9:
                put_stone(b, cx + sx, y, cz)
                put_stone(b, cx, y, cz + sz)
        b.set(cx, 8, cz, OBS)
        stair(b, cx + sx, 9, cz, 'south' if cz == 0 else 'north')
        stair(b, cx, 9, cz + sz, 'east' if cx == 0 else 'west')
        b.set(cx, 12, cz, CHISELED)
        eye(b, cx, 13, cz, 'north' if cz == 0 else 'south')
    # walls join the east and south faces: one column of the wall's own profile on cells 3..7
    wall_stub(b, east_x=10, south_z=10)
    # interior floors: the wall-walk room and the crown deck
    for x in range(2, 9):
        for z in range(2, 9):
            b.set(x, F, z, POLISHED)
            b.set(x, T, z, BRICK)
    for x in range(4, 7):
        for z in range(4, 7):
            b.set(x, 0, z, CRY if (x + z) % 2 == 0 else OBS)
            b.set(x, F, z, CRY if (x, z) == (5, 5) else OBS)
    # core column under the wall-walk room, with glowing faces
    for y in range(1, F):
        for x in range(4, 7):
            for z in range(4, 7):
                b.set(x, y, z, CRY if (x == 5 or z == 5) and y % 3 == 2 else OBS)
    # spiral stair from the ground to the wall-walk room (south side, west side, then north side)
    spiral(b, 2, 2, 7, 2, 1, F, start='south')
    # ground doors on the inner corner (south face at x = 8, east face at z = 8): narrow, 4 high
    for y in range(1, 5):
        b.erase(8, y, 9, 8, y, 10)
        b.erase(9, y, 8, 10, y, 8)
    b.set(8, 5, 9, CHISELED)
    b.set(9, 5, 8, CHISELED)
    stair(b, 8, 5, 10, 'north', half='top')
    stair(b, 10, 5, 8, 'west', half='top')
    # wall-walk openings: east face (z = 4..6) and south face (x = 4..6), 4 high, pointed lintel
    for y in range(F + 1, F + 5):
        b.erase(9, y, 4, 9, y, 6)
        b.erase(4, y, 9, 6, y, 9)
    for k in (4, 6):
        stair(b, 9, F + 4, k, 'north' if k == 4 else 'south', half='top')
        stair(b, k, F + 4, 9, 'west' if k == 4 else 'east', half='top')
    b.set(9, F + 5, 5, CRY)
    b.set(5, F + 5, 9, CRY)
    # glowing slits: outside faces on both floors, inner faces above the wall's reach
    for y in range(5, 9):
        b.set(5, y, 1, PANE)
        b.set(1, y, 5, PANE)
    for y in range(12, 16):
        b.set(5, y, 1, PANE)
        b.set(1, y, 5, PANE)
    for y in range(17, 20):
        for x, z in ((5, 1), (1, 5), (5, 9), (9, 5), (3, 1), (7, 1), (1, 3), (1, 7)):
            b.set(x, y, z, PANE)
    # crown: corbel table, parapet, merlons, corner pinnacles
    for x, z, f, corner in _ring(N):
        if corner:
            for y in range(T - 2, T + 4):
                put_stone(b, x, y, z)
            b.set(x, T + 1, z, OBS)
            b.set(x, T + 4, z, WALL)
            rod(b, x, T + 5, z)
            continue
        stair(b, x, T - 1, z, f, half='top')
        b.set(x, T, z, BRICK)
        put_stone(b, x, T + 1, z)
        along = x if z in (0, N - 1) else z
        if along % 2 == 0 and along != 5:
            put_stone(b, x, T + 2, z)
            slab(b, x, T + 3, z)
    for x in range(1, 10):
        for z in range(1, 10):
            if x in (1, 9) or z in (1, 9):
                b.set(x, T, z, POLISHED)
    # an eye in the middle crenel of each crown face, watching outward
    for x, z, f in ((5, 0, 'north'), (0, 5, 'west'), (5, 10, 'south'), (10, 5, 'east')):
        eye(b, x, T + 2, z, f)
    # the steep black spire, banded with obsidian
    tip = spire_cap(b, 2, 2, 7, T + 1, kind=stone, steep=3)
    for y in (T + 3, T + 6, T + 9):
        for x in range(2, 9):
            for z in range(2, 9):
                if b.get(x, y, z)[0] == 'minecraft:' + BRICK or b.get(x, y, z)[0] == 'minecraft:cracked_' + BRICK:
                    b.set(x, y, z, OBS)
    # the wall-walk room (y = 11..19): banners, a rack of crystal glaives, a hanging light
    chain(b, 5, T - 2, T - 1, 5)
    rod(b, 5, T - 3, 5, 'down')
    banner(b, 5, F + 4, 2, 'south')
    banner(b, 2, F + 4, 5, 'east')
    for x, z in ((8, 2), (8, 3), (7, 2)):
        rod(b, x, F + 1, z)
    rod(b, 8, F + 1, 8)
    # a rail round the stairwell (the stair arrives from the west on z = 2..3)
    for x, z in ((4, 4), (4, 5), (2, 6), (3, 6)):
        b.set(x, F + 1, z, WALL)
    # ground floor: glowing floor stones by the doors
    b.set(8, 0, 8, CRY)
    b.set(7, 0, 8, CRY)
    b.spot('stand', 7, F + 1, 7)
    b.spot('stand', 8, 1, 7)



