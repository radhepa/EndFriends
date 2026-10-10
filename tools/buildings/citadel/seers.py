"""The Seers' Spire: a slim tower of amethyst and crying obsidian with a glass observatory on top,
where the Court's Seers watch the void through a great scrying eye."""
from kit import building

from citadel._parts import (BRICK, CHISELED, CRY, OBS, PILLAR, POLISHED, STAIR, WALL, PANE, arch, chain, eye, pillar,
                            rod, spiral, spire_cap, stair)

N = 11
C = 5
OBSV = 22               # observatory floor (stand at 23)
OTOP = 27               # observatory walls rise to here
H = 39
AMETHYST = 'amethyst_block'


@building('seers_spire', people='court', role='work', size=(N, H, N), door=C, job='seer',
          about='The Seers\' Spire: a slim tower of amethyst banded with crying obsidian, a spiral stair round a '
                'purpur pillar, and a corbelled observatory of magenta glass where a great scrying eye watches the void.')
def seers_spire(b):
    # ---------------------------------------------------------------- terrace and corner columns
    for x in range(N):
        for z in range(N):
            b.set(x, 0, z, OBS if x in (0, N - 1) or z in (0, N - 1) else POLISHED)
    for x in range(1, 10):
        for z in range(1, 10):
            if x in (1, 9) or z in (1, 9):
                b.set(x, 0, z, CRY if (x + z) % 4 == 0 else OBS)
    for cx, cz in ((1, 1), (9, 1), (1, 9), (9, 9)):
        for y in range(1, 9):
            b.set(cx, y, cz, OBS if y % 4 else CRY)
        b.set(cx, 9, cz, WALL)
        b.set(cx, 10, cz, 'amethyst_cluster', facing='up', waterlogged=False)
    # ---------------------------------------------------------------- the shaft: 7 x 7 of amethyst, obsidian corners
    for y in range(1, OBSV):
        for x in range(2, 9):
            for z in range(2, 9):
                if not (x in (2, 8) or z in (2, 8)):
                    continue
                corner = x in (2, 8) and z in (2, 8)
                if corner:
                    b.set(x, y, z, OBS)
                elif y % 5 == 0:
                    b.set(x, y, z, CRY)
                else:
                    b.set(x, y, z, AMETHYST)
    for y in (1, 2):
        for x in range(2, 9):
            for z in range(2, 9):
                if x in (2, 8) or z in (2, 8):
                    b.set(x, y, z, OBS)
    for x, z in ((8, 6), (6, 8), (2, 4), (2, 6)):
        b.set(x, 1, z, CRY)                     # glowing stones light the pocket under the stair
    # crying-obsidian rune slits climbing each face
    for y in range(7, 19, 4):
        for x, z in ((C, 2), (2, C), (C, 8), (8, C)):
            b.set(x, y, z, PANE)
            b.set(x, y + 1, z, PANE)
    # ---------------------------------------------------------------- the stair: 2 wide round a purpur pillar
    pillar(b, C, 1, OBSV - 1, C)
    treads = spiral(b, 3, 3, 5, 2, 1, OBSV, start='north')
    # door: a tall pointed arch on the north (3 wide, 5 high)
    arch(b, 'x', C - 1, 3, 1, 5, 2, 2, rise=2, smooth=STAIR)
    b.set(C, 6, 2, CRY)
    eye(b, C, 7, 1, 'north')
    b.set(C, 6, 1, CHISELED)
    # ---------------------------------------------------------------- the observatory (9 x 9, corbelled out)
    for x in range(1, 10):
        for z in range(1, 10):
            edge = x in (1, 9) or z in (1, 9)
            if edge:
                corner = x in (1, 9) and z in (1, 9)
                if not corner:
                    f = 'south' if z == 1 else 'north' if z == 9 else 'east' if x == 1 else 'west'
                    stair(b, x, OBSV - 1, z, f, half='top')
                b.set(x, OBSV, z, OBS)
            elif not b.solid(x, OBSV, z):
                b.set(x, OBSV, z, POLISHED)
    tread_cells = {(x, y, z) for cells, y, _ in treads for x, z in cells}
    for cells, y, _ in treads:
        for x, z in cells:
            for dy in range(1, 5):
                if y + dy >= OBSV and (x, y + dy, z) not in tread_cells:
                    b.erase(x, y + dy, z, x, y + dy, z)
    for y in range(OBSV + 1, OTOP + 1):
        for x in range(1, 10):
            for z in range(1, 10):
                if not (x in (1, 9) or z in (1, 9)):
                    continue
                corner = x in (1, 9) and z in (1, 9)
                if corner:
                    b.set(x, y, z, AMETHYST)
                elif x in (1, 9) and z in (3, 7) or z in (1, 9) and x in (3, 7):
                    b.set(x, y, z, PILLAR, axis='y')
                elif y == OTOP:
                    b.set(x, y, z, CRY)
                else:
                    b.set(x, y, z, PANE)
    # observatory roof: a stepped amethyst-and-obsidian cone with an end-rod finial
    spire_cap(b, 1, 1, 9, OTOP + 1, kind=lambda x, y, z: AMETHYST if y % 2 else OBS, steep=2, core=OBS)
    for x in range(2, 9):
        for z in range(2, 9):
            b.set(x, OTOP, z, BRICK)
    # ---------------------------------------------------------------- the scrying eye and the Seers' things
    hole = {(x, z) for (x, y, z) in tread_cells if y >= OBSV - 4}
    b.set(C, OBSV, C, CRY)
    if (C, C) not in hole:
        eye(b, C, OBSV + 1, C, 'north')
    for x, z in ((2, 2), (8, 2), (2, 8), (8, 8)):
        if (x, z) in hole:
            continue
        b.set(x, OBSV + 1, z, AMETHYST)
        b.set(x, OBSV + 2, z, 'amethyst_cluster', facing='up', waterlogged=False)
    # the Seer's lectern of observations
    if (3, 3) not in hole:
        b.set(3, OBSV + 1, 3, 'lectern', facing='south', has_book=False, powered=False)
    chain(b, C, OTOP - 1, OTOP - 1, C)
    rod(b, C, OTOP - 2, C, 'down')
    # rail round the stairwell where the floor is open (not where the stair arrives)
    last_cells, last_y, _ = treads[-1]
    arrive = {(x + dx, z + dz) for x, z in last_cells for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))}
    for (x, z) in sorted(hole):
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, nz = x + dx, z + dz
            if (nx, nz) in hole or (nx, nz) in arrive or not (2 <= nx <= 8 and 2 <= nz <= 8):
                continue
            if b.get(nx, OBSV + 1, nz)[0] == 'minecraft:air' and b.solid(nx, OBSV, nz):
                b.set(nx, OBSV + 1, nz, WALL)
    # ---------------------------------------------------------------- spots
    b.spot('work', 3, OBSV + 1, 4)
    b.spot('stand', C, 1, 2)          # in the doorway
