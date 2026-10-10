"""The Voidhound Kennels: a low fortified block of barred stalls for the Court's hounds."""
from kit import building

from citadel._parts import (BRICK, CHISELED, CRY, OBS, POLISHED, STAIR, PANE, arch, banner, chain, eye, put_stone,
                            rod, slab, stair, stone)

W, H, D = 13, 9, 11
DOOR = 6
TOP = 5                    # walls y 1..5, flat roof at 6 (Endarch handlers need the height)
AISLE = (5, 7)
STALLS = ((1, 4), (8, 11))  # stall x ranges, west and east
STALL_Z = ((1, 4), (6, 9))  # two stalls per side, divided at z = 5


@building('voidhound_kennels', people='court', role='work', size=(W, H, D), door=DOOR,
          about='The Voidhound kennels: a low crenellated block with an eyed arch, four barred stalls along a lit '
                'aisle, carpet beds, bone gnaw-blocks, chained leashes and the handler\'s stores.')
def voidhound_kennels(b):
    # floor
    for x in range(W):
        for z in range(D):
            b.set(x, 0, z, POLISHED)
    for z in range(1, D - 1):
        for x in range(AISLE[0], AISLE[1] + 1):
            b.set(x, 0, z, OBS if x == DOOR else BRICK)
        b.set(DOOR, 0, z, CRY if z in (2, 7) else OBS)
    # walls
    for y in range(1, TOP + 1):
        for x in range(W):
            for z in range(D):
                if x in (0, W - 1) or z in (0, D - 1):
                    b.set(x, y, z, OBS if y == 1 else stone(x, y, z))
    # flat roof, crenellated parapet, corner pinnacles with rods
    for x in range(W):
        for z in range(D):
            b.set(x, TOP + 1, z, BRICK if 0 < x < W - 1 and 0 < z < D - 1 else OBS)
    for x in range(W):
        for z in range(D):
            if x in (0, W - 1) or z in (0, D - 1):
                corner = x in (0, W - 1) and z in (0, D - 1)
                along = x if z in (0, D - 1) else z
                if corner:
                    put_stone(b, x, TOP + 2, z)
                    rod(b, x, TOP + 3, z)
                elif along % 2 == 0:
                    slab(b, x, TOP + 2, z)
    # the door: an open pointed arch, 3 wide and 5 high, an eye over it
    arch(b, 'x', DOOR - 1, 3, 1, 5, 0, 0, rise=2, smooth=STAIR)
    for x in (DOOR - 2, DOOR + 2):
        for y in range(1, TOP + 1):
            b.set(x, y, 0, OBS)
    # a peaked gablet over the arch, carrying the eye
    b.set(DOOR, TOP + 1, 0, OBS)
    b.set(DOOR, TOP + 2, 0, CHISELED)
    stair(b, DOOR - 1, TOP + 2, 0, 'east')
    stair(b, DOOR + 1, TOP + 2, 0, 'west')
    eye(b, DOOR, TOP + 3, 0, 'north')
    # obsidian pilasters break up the long faces
    for y in range(1, TOP + 1):
        for x in (2, W - 3):
            b.set(x, y, 0, OBS)
            b.set(x, y, D - 1, OBS)
        for z in (5,):
            b.set(0, y, z, OBS)
            b.set(W - 1, y, z, OBS)
    # slit windows on the sides
    for z in (3, 7):
        for x in (0, W - 1):
            for y in (2, 3, 4):
                b.set(x, y, z, PANE)
    # ---------------------------------------------------------------- stalls
    for (x0, x1) in STALLS:
        front = x1 if x0 == 1 else x0
        for z in range(1, D - 1):
            for y in (1, 2):
                if z == 5:
                    put_stone(b, front, y, z)
                elif z not in (3, 7):
                    b.set(front, y, z, 'iron_bars')
            if z == 5:
                for y in range(3, TOP + 1):
                    put_stone(b, front, y, z)
        # the divider between the two stalls
        for x in range(x0, x1 + 1):
            for y in range(1, TOP + 1):
                put_stone(b, x, y, 5)
        for (z0, z1) in STALL_Z:
            back = x0 if x0 == 1 else x1
            # a bed of carpet, a bone to gnaw, a bowl, a leash chain on the back wall
            for x in range(min(x0, x1), max(x0, x1) + 1):
                for z in range(z0, z1 + 1):
                    if x != front:
                        b.set(x, 1, z, 'black_carpet' if (x + z) % 3 else 'purple_carpet')
            b.set(back, 1, z0, 'bone_block', axis='y')
            b.set(back, 1, z1, 'cauldron')
            chain(b, back, 2, TOP, (z0 + z1) // 2)
            rod(b, back, TOP, z0 + 1 if z0 + 1 != (z0 + z1) // 2 else z0, 'down')
    # Court banners on the ends of the stall dividers, facing the aisle
    banner(b, AISLE[0], 4, 5, 'east')
    banner(b, AISLE[1], 4, 5, 'west')
    # ---------------------------------------------------------------- the handler's end of the aisle
    b.barrel(DOOR - 1, 1, D - 2, 'up')
    b.barrel(DOOR + 1, 1, D - 2, 'up')
    b.set(DOOR, 1, D - 2, 'lectern', facing='north', has_book=False, powered=False)
    banner(b, DOOR, 4, D - 2, 'north')
    chain(b, DOOR, TOP, TOP, 4)
    rod(b, DOOR, TOP - 1, 4, 'down')
    # outside lights by the door
    for x in (DOOR - 2, DOOR + 2):
        b.set(x, 1, 0, CRY)
    for z in (2, 8):
        b.set(0, 1, z, CRY)
        b.set(W - 1, 1, z, CRY)
    b.set(DOOR, 1, D - 1, CRY)
    # ---------------------------------------------------------------- spots
    b.spot('work', DOOR, 1, 6)      # the handler in the aisle
    b.spot('stand', DOOR, 1, 1)     # at the door
