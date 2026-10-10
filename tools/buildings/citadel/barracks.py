"""The Riftguard Barracks: a walled training yard (targets, rift posts) in front of the armoury."""
from kit import building

from citadel._parts import (BRICK, CHISELED, CRY, OBS, POLISHED, STAIR, WALL, PANE, MARSHAL_PATTERN, arch, banner,
                            chain, eye, put_stone, rod, stair, stone)

W, H, D = 17, 14, 13
DOOR = 8
YARD = (0, 6)            # yard z range (north part)
ARM_Z = 6                # armoury north wall
ARM_TOP = 6              # armoury walls y 1..6, ceiling at 7


def roof_y(z):
    """Armoury roof ridge along x: eaves 7 at z = 6 and 12, ridge 10 at z = 9."""
    return ARM_TOP + 1 + min(z - ARM_Z, 12 - z)


@building('riftguard_barracks', people='court', role='work', size=(W, H, D), door=DOOR, job='riftguard',
          about='The Riftguards\' barracks: a walled training yard with target blocks and obsidian rift posts '
                'behind an eyed gate, and a gabled armoury of crystal-glaive racks, anvils and grindstones.')
def riftguard_barracks(b):
    # ground
    for x in range(W):
        for z in range(D):
            b.set(x, 0, z, POLISHED)
    for x in range(1, W - 1):
        for z in range(1, ARM_Z):
            b.set(x, 0, z, BRICK if (x + z) % 2 else POLISHED)
    # the sparring ring in the yard
    for x in range(5, 12):
        for z in (2, 4):
            b.set(x, 0, z, OBS)
    b.set(8, 0, 3, CRY)
    # ---------------------------------------------------------------- yard enclosure: piers and low walls
    piers = [(0, 0), (4, 0), (12, 0), (16, 0), (0, 3), (16, 3)]
    for x in range(W):
        for z in range(0, ARM_Z):
            if x in (0, W - 1) or z == 0:
                if 7 <= x <= 9 and z == 0:
                    continue
                b.set(x, 1, z, OBS)
                b.set(x, 2, z, WALL)
    for x, z in piers:
        for y in range(1, 5):
            put_stone(b, x, y, z)
        b.set(x, 5, z, WALL)
        rod(b, x, 6, z)
    # the gate: tall piers and a pointed lintel with an eye
    for x in (6, 10):
        for y in range(1, 7):
            put_stone(b, x, y, 0)
        b.set(x, 1, 0, OBS)
        b.set(x, 7, 0, WALL)
        rod(b, x, 8, 0)
    for x, y, f in ((7, 5, 'west'), (9, 5, 'east')):
        stair(b, x, y, 0, f, half='top')
    for x in (7, 9):
        put_stone(b, x, 6, 0)
    b.set(8, 6, 0, CHISELED)
    b.set(8, 7, 0, OBS)
    eye(b, 8, 8, 0, 'north')
    for x in (5, 11):
        b.set(x, 1, 0, OBS)
        b.set(x, 2, 0, WALL)
    # targets on posts along the yard's side walls, facing in
    for z in (2, 4):
        for x, f in ((1, 'east'), (15, 'west')):
            b.set(x, 1, z, OBS)
            put_stone(b, x, 2, z)
            b.set(x, 3, z, 'target')
    for x in (2, 14):
        b.set(x, 1, 1, 'target')
    # rift posts: obsidian columns with glowing tops, where Riftguards practise the rift-step
    for x, z in ((4, 3), (12, 3)):
        for y in range(1, 4):
            b.set(x, y, z, OBS)
        b.set(x, 4, z, CRY)
        rod(b, x, 5, z)
    # ---------------------------------------------------------------- the armoury (x 1..15, z 6..12)
    for y in range(1, ARM_TOP + 1):
        for x in range(1, 16):
            for z in range(ARM_Z, 13):
                if x in (1, 15) or z in (ARM_Z, 12):
                    b.set(x, y, z, OBS if y in (1, ARM_TOP) else stone(x, y, z))
    for x in range(2, 15):
        for z in range(ARM_Z + 1, 12):
            b.set(x, 0, z, POLISHED if (x + z) % 2 else BRICK)
            b.set(x, ARM_TOP + 1, z, OBS if x % 4 == 0 else BRICK)
    # roof: solid under the slopes, stairs on top, obsidian ridge, rods and an eye on the gables
    for z in range(ARM_Z - 1, 13):
        zz = max(z, ARM_Z)
        top = roof_y(zz)
        for x in range(0, W):
            if 1 <= x <= 15 and z >= ARM_Z:
                for y in range(ARM_TOP + 1, top):
                    if not b.solid(x, y, z):
                        put_stone(b, x, y, z)
            if z == 9:
                b.set(x, top, z, OBS)
            elif z >= ARM_Z:
                stair(b, x, top, z, 'south' if z < 9 else 'north')
            else:
                stair(b, x, ARM_TOP + 1, z, 'south')
    for x in (0, 16):
        rod(b, x, roof_y(9) + 1, 9)
    for x in range(1, 16, 2):
        b.set(x, roof_y(9) + 1, 9, WALL)
    rod(b, 8, roof_y(9) + 2, 9)
    for x, f in ((1, 'west'), (15, 'east')):
        b.set(x, ARM_TOP + 2, 9, CRY)
    # door from the yard: pointed arch 3 wide, 5 high
    arch(b, 'x', DOOR - 1, 3, 1, 5, ARM_Z, ARM_Z, rise=2, smooth=STAIR)
    b.set(DOOR, 6, ARM_Z, CRY)
    banner(b, 5, 5, ARM_Z - 1, 'north', color='purple', patterns=MARSHAL_PATTERN)
    banner(b, 11, 5, ARM_Z - 1, 'north', color='purple', patterns=MARSHAL_PATTERN)
    # windows
    for x in (4, 12):
        for y in range(2, 5):
            b.set(x, y, 12, PANE)
    for x in (1, 15):
        for y in range(2, 5):
            b.set(x, y, 9, PANE)
    # ---------------------------------------------------------------- armoury fittings
    for x in range(3, 14):
        if x in (7, 8, 9):
            continue
        b.set(x, 1, 11, WALL)
        rod(b, x, 2, 11)                              # a rack of crystal glaives
    banner(b, 8, 5, 11, 'north')
    b.set(8, 1, 11, 'smithing_table')
    b.set(7, 1, 11, 'anvil', facing='east')
    b.set(9, 1, 11, 'grindstone', facing='north', face='floor')
    b.barrel(2, 1, 7, 'up')
    b.barrel(2, 1, 8, 'east')
    b.barrel(14, 1, 7, 'up')
    b.chest(14, 1, 8, 'west')
    for x in (2, 14):
        b.set(x, 1, 10, 'iron_bars')
        b.set(x, 2, 10, 'iron_bars')
        rod(b, x, 3, 10)
    # light
    for x in (5, 11):
        chain(b, x, ARM_TOP, ARM_TOP, 9)
        rod(b, x, ARM_TOP - 1, 9, 'down')
    for z in (8, 10):
        b.set(8, 0, z, CRY)
    for x in (4, 12):
        b.set(x, 0, 1, CRY)
    b.set(8, 1, 12, CRY)
    # ---------------------------------------------------------------- spots
    for x, z in ((3, 2), (13, 2), (3, 4), (13, 4)):
        b.spot('work', x, 1, z)                   # at the targets
    b.spot('work', 8, 1, 3)                       # in the sparring ring
    b.spot('work', 8, 1, 10)                      # at the anvil
    b.spot('stand', 8, 1, 1)                      # at the gate
