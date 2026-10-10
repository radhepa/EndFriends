"""The War Hall: where the Voidmarshals plan the Court's wars over a great table map of the End."""
from kit import building

from citadel._parts import (BRICK, CHISELED, CRY, OBS, POLISHED, STAIR, WALL, PANE, MARSHAL_PATTERN, arch, arch_ring,
                            banner, chain, eye, pillar, put_stone, rod, stair, stone)

W, H, D = 19, 17, 15
DOOR = 9
WALL_TOP = 7                       # walls y 1..7, interior 7 high (ceiling at 8)
BUTTS = (1, 5, 13, 17)             # buttress x positions on the long faces


def roof_y(z):
    """Ridge roof running east-west: eaves at 8 over z = 1 and 13, ridge 14 over z = 7."""
    return WALL_TOP + 1 + min(z - 1, 13 - z)


@building('war_hall', people='court', role='work', size=(W, H, D), door=DOOR, job='voidmarshal',
          about='The Voidmarshals\' hall: a buttressed black hall with a gabled war-porch, racks of crystal '
                'glaives, Marshal banners, and a great war table mapping the End in blocks, the slain Dragon at its centre.')
def war_hall(b):
    # floor
    for x in range(W):
        for z in range(D):
            b.set(x, 0, z, POLISHED)
    for x in range(2, 17):
        for z in range(2, 13):
            b.set(x, 0, z, BRICK if (x + z) % 2 else POLISHED)
    # walls x 1..17, z 1..13
    for y in range(1, WALL_TOP + 1):
        for x in range(1, 18):
            for z in range(1, 14):
                if x in (1, 17) or z in (1, 13):
                    b.set(x, y, z, OBS if y in (1, WALL_TOP) else stone(x, y, z))
    # roof: solid under the slopes (no hollow attic for Endermen to spawn in), stairs on top,
    # an obsidian ridge, eaves overhanging the long walls by one
    for z in range(0, D):
        zz = min(max(z, 1), 13)
        top = roof_y(zz)
        for x in range(1, 18):
            for y in range(WALL_TOP + 1, top):
                if 1 <= z <= 13:
                    put_stone(b, x, y, z)
            if z == 7:
                b.set(x, top, z, OBS)
            elif 1 <= z <= 13:
                stair(b, x, top, z, 'south' if z < 7 else 'north')
            else:
                stair(b, x, top, z, 'south' if z == 0 else 'north')
    for x in range(2, 17):
        for z in range(2, 13):
            b.set(x, WALL_TOP + 1, z, OBS if x % 4 == 1 else BRICK)
    # ridge crest, gable lancets and an eye at each gable apex
    for x in range(1, 18):
        if x % 2 == 1:
            b.set(x, roof_y(7) + 1, 7, WALL)
        if x in (1, 9, 17):
            rod(b, x, roof_y(7) + 2, 7)
    for x, f in ((1, 'west'), (17, 'east')):
        for y in range(WALL_TOP + 2, WALL_TOP + 6):
            b.set(x, y, 7, 'magenta_stained_glass')
        b.set(x, WALL_TOP + 6, 7, CRY)
    # corner pinnacles with rods
    for x in (1, 17):
        for z in (1, 13):
            for y in range(WALL_TOP + 1, WALL_TOP + 4):
                put_stone(b, x, y, z)
            b.set(x, WALL_TOP + 4, z, WALL)
            rod(b, x, WALL_TOP + 5, z)
    # buttresses on the long faces, with eyes on their heads
    for x in BUTTS:
        for z, f in ((0, 'north'), (14, 'south')):
            for y in range(1, 7):
                put_stone(b, x, y, z)
            b.set(x, 1, z, OBS)
            stair(b, x, 7, z, 'south' if z == 0 else 'north')
    for x in (BUTTS[0], BUTTS[-1]):
        for z in (0, 14):
            b.set(x, 7, z, CHISELED)
            eye(b, x, 8, z, 'north' if z == 0 else 'south')
    # magenta lancets between the buttresses
    for x in (3, 15):
        for z in (1, 13):
            for y in range(3, 7):
                b.set(x, y, z, PANE)
    for z in (4, 7, 10):
        for x in (1, 17):
            for y in range(3, 7):
                b.set(x, y, z, PANE)
    # the war-porch: a gabled bay projecting north over the door (x 6..12, z 0)
    for x in range(6, 13):
        for y in range(1, WALL_TOP + 1):
            put_stone(b, x, y, 0)
        b.set(x, 1, 0, OBS)
    for k, x in enumerate(range(6, 13)):
        h = min(k, 6 - k)
        for y in range(WALL_TOP + 1, WALL_TOP + 1 + h):
            put_stone(b, x, y, 0)
            put_stone(b, x, y, 1)
        if x == DOOR:
            b.set(x, WALL_TOP + 1 + h, 0, OBS)
            eye(b, x, WALL_TOP + 2 + h, 0, 'north')
        else:
            stair(b, x, WALL_TOP + 1 + h, 0, 'east' if x < DOOR else 'west')
            stair(b, x, WALL_TOP + 1 + h, 1, 'east' if x < DOOR else 'west')
    arch(b, 'x', DOOR - 1, 3, 1, 6, 0, 1, rise=2, smooth=STAIR)
    for c, dy in arch_ring(3, 6, 2):
        if b.solid(DOOR - 1 + c, 1 + dy, 0) and not b.get(DOOR - 1 + c, 1 + dy, 0)[0].endswith('_stairs'):
            b.set(DOOR - 1 + c, 1 + dy, 0, OBS)
    b.set(DOOR, 7, 0, CRY)
    for x in (6, 12):
        b.set(x, WALL_TOP, 0, CHISELED)
        rod(b, x, WALL_TOP + 1, 0)
    # ---------------------------------------------------------------- the great war table (x 5..13, z 4..10)
    for x in range(5, 14):
        for z in range(4, 11):
            b.set(x, 1, z, POLISHED)
            edge = x in (5, 13) or z in (4, 10)
            b.set(x, 2, z, CHISELED if edge else 'black_concrete')
    for x in (5, 13):
        for z in (4, 10):
            b.set(x, 1, z, OBS)
    # the map: the central island with the Dragon, the outer islands, the peoples' towns
    for x, z in ((8, 7), (9, 6), (9, 7), (9, 8), (10, 7)):
        b.set(x, 2, z, 'end_stone')
    b.set(9, 3, 7, 'dragon_head', rotation=8)
    for x, z in ((8, 6), (10, 8), (10, 6), (8, 8)):
        rod(b, x, 3, z)                                   # the obsidian pillars, in miniature
    b.set(6, 2, 5, 'end_stone')
    b.set(7, 2, 5, 'end_stone')
    b.set(6, 2, 6, 'end_stone')
    pillar(b, 6, 3, 3, 5)                                 # a Shulkin spire
    b.set(12, 2, 9, 'end_stone')
    b.set(11, 2, 9, 'end_stone')
    b.set(12, 2, 8, 'end_stone')
    b.set(12, 3, 9, 'chorus_flower', age=5)               # a Chorrin stead
    b.set(12, 2, 5, OBS)
    b.set(11, 2, 5, OBS)
    b.candles(12, 3, 5, 4, 'magenta')                     # this Citadel
    b.set(6, 2, 9, OBS)
    b.candles(6, 3, 9, 2, 'purple')                       # another Citadel
    b.candles(11, 3, 7, 3, 'purple')                      # a Court host on the march
    b.candles(7, 3, 8, 1, 'black')
    # ---------------------------------------------------------------- racks, banners, the marshals' gear
    for x in (3, 15):
        side = 'east' if x == 3 else 'west'
        xr = 2 if x == 3 else 16
        for z in (4, 5, 6, 8, 9, 10):
            b.set(xr, 1, z, WALL)
            rod(b, xr, 2, z)                              # crystal glaives standing in the rack
        b.set(xr, 1, 7, 'anvil' if x == 3 else 'grindstone', facing='east' if x == 3 else 'north',
              **({} if x == 3 else {'face': 'floor'}))
        banner(b, xr, 6, 7, side, color='black', patterns=MARSHAL_PATTERN)
    for x in (4, 14):
        banner(b, x, 6, 12, 'north', color='purple', patterns=MARSHAL_PATTERN)
    b.barrel(3, 1, 12, 'up')
    b.barrel(15, 1, 12, 'up')
    b.chest(4, 1, 12, 'north')
    b.chest(14, 1, 12, 'north')
    # ---------------------------------------------------------------- light
    chain(b, 9, WALL_TOP - 1, WALL_TOP, 7)
    b.set(9, WALL_TOP - 2, 7, CRY)
    for dx, dz, f in ((1, 0, 'east'), (-1, 0, 'west'), (0, 1, 'south'), (0, -1, 'north')):
        rod(b, 9 + dx, WALL_TOP - 2, 7 + dz, f)
    for x, z, f in ((2, 2, 'up'), (16, 2, 'up'), (2, 12, 'up'), (16, 12, 'up')):
        rod(b, x, 1, z, f)
    for x in (9, 3, 15):
        b.set(x, 1, 13, CRY)                              # glowing base stones light the back
    for x in (7, 11):
        rod(b, x, 5, 2, 'south')
        rod(b, x, 5, 12, 'north')
    # ---------------------------------------------------------------- spots round the table
    for x, z in ((9, 3), (9, 11), (4, 7), (14, 7)):
        b.spot('work', x, 1, z)
    b.spot('stand', DOOR, 1, 2)
