"""The Thrall Yards: where the Court's Endermen haul and stack blocks.

An open paved yard inside a low wall: a heap of hauled end stone, a neat cube of purpur, a stack of
obsidian, bond posts with iron chains strung between them, an overseer's dais, and low lean-to
shelters along the back wall where the stores are kept.
"""
from kit import building

from citadel._parts import (BRICK, CHISELED, CRY, OBS, PILLAR, POLISHED, WALL, chain, eye, put_stone, rod, slab,
                            stair, _h)

W, H, D = 21, 9, 17
DOOR = 10
SHELTER = (12, 16)        # shelter z range: posts at 12, back wall at 16
ROOF = 5                  # shelter roof layer (Endermen stand 2.9 high: y 1..4 is clear)


@building('thrall_yards', people='court', role='work', size=(W, H, D), door=DOOR,
          about='The thrall yards: a walled yard where Endermen haul and stack the Court\'s blocks -- a heap of end '
                'stone, a cube of purpur, an obsidian stack, bond posts strung with iron chains, an overseer\'s dais '
                'and low lean-to shelters full of stores.')
def thrall_yards(b):
    # ---------------------------------------------------------------- paving
    for x in range(W):
        for z in range(D):
            b.set(x, 0, z, POLISHED if _h(x, 0, z, 3) > 0.1 else 'end_stone_bricks')
    for z in range(0, SHELTER[0]):
        for x in (DOOR - 1, DOOR, DOOR + 1):
            b.set(x, 0, z, BRICK)
    for x, z in ((5, 5), (15, 5), (5, 10), (15, 10), (10, 3), (10, 8)):
        b.set(x, 0, z, CRY)
    # ---------------------------------------------------------------- the low wall with lit piers
    for x in range(W):
        for z in range(SHELTER[0]):
            if x in (0, W - 1) or z == 0:
                if z == 0 and DOOR - 1 <= x <= DOOR + 1:
                    continue
                b.set(x, 1, z, WALL)
    for x, z in ((0, 0), (4, 0), (16, 0), (20, 0), (0, 4), (20, 4), (0, 8), (20, 8)):
        put_stone(b, x, 1, z)
        put_stone(b, x, 2, z)
        rod(b, x, 3, z)
    # gate piers with eyes
    for x in (DOOR - 2, DOOR + 2):
        for y in range(1, 5):
            put_stone(b, x, y, 0)
        b.set(x, 5, 0, CHISELED)
        eye(b, x, 6, 0, 'north')
    # ---------------------------------------------------------------- shelters along the back (z 12..16)
    for x in range(W):
        for y in range(1, ROOF + 2):
            put_stone(b, x, y, SHELTER[1])
        b.set(x, 1, SHELTER[1], OBS)
    for z in range(SHELTER[0], SHELTER[1] + 1):
        for y in range(1, ROOF + 2):
            put_stone(b, 0, y, z)
            put_stone(b, W - 1, y, z)
    for x in range(0, W, 4):
        for y in range(1, ROOF):
            b.set(x, y, SHELTER[0], WALL) if 0 < x < W - 1 else put_stone(b, x, y, SHELTER[0])
    for x in range(W):
        stair(b, x, ROOF, SHELTER[0] - 1, 'south')        # eave lip
        for z in range(SHELTER[0], SHELTER[1]):
            slab(b, x, ROOF, z, top=True)
            if z >= SHELTER[0] + 2:
                stair(b, x, ROOF + 1, z, 'south') if z == SHELTER[0] + 2 else put_stone(b, x, ROOF + 1, z)
        stair(b, x, ROOF + 2, SHELTER[1], 'south')
    # lights under the shelter roof
    for x in (2, 6, 10, 14, 18):
        rod(b, x, ROOF - 1, SHELTER[1] - 1, 'down')
    # stores under the shelters: barrels, stacked bricks, coiled chain
    for x in (1, 2, 3):
        b.barrel(x, 1, 15, 'up')
    b.barrel(1, 2, 15, 'up')
    b.barrel(2, 1, 14, 'north')
    for x in (5, 6, 7):
        b.set(x, 1, 15, 'end_stone_bricks')
        if x != 7:
            b.set(x, 2, 15, 'end_stone_bricks')
    for x in (13, 14, 15):
        b.set(x, 1, 15, 'purpur_block')
    b.set(13, 2, 15, PILLAR, axis='x')
    b.set(14, 2, 15, PILLAR, axis='x')
    for x in (17, 18, 19):
        b.set(x, 1, 15, OBS)
    b.set(18, 2, 15, OBS)
    chain(b, 10, 2, ROOF - 1, 15)
    b.set(10, 1, 15, 'black_carpet')
    for x in (9, 11):
        b.set(x, 1, 14, 'black_carpet')                # where the thralls stand at rest
    # ---------------------------------------------------------------- the heaps
    # hauled end stone, heaped (north-west)
    hx, hz = 4, 4
    for x in range(1, 8):
        for z in range(1, 8):
            d = abs(x - hx) + abs(z - hz)
            height = max(0, 4 - d) + (1 if _h(x, 1, z, 5) > 0.6 and d <= 4 else 0)
            for y in range(1, 1 + height):
                b.set(x, y, z, 'end_stone' if _h(x, y, z, 7) > 0.2 else 'end_stone_bricks')
    # a neat cube of purpur with a corner taken (north-east)
    for x in range(14, 18):
        for z in range(2, 5):
            for y in range(1, 4):
                if (x, y, z) in ((17, 3, 2), (17, 3, 3), (16, 3, 2), (17, 2, 2)):
                    continue
                b.set(x, y, z, 'purpur_block')
    for x in range(14, 17):
        b.set(x, 4, 4, PILLAR, axis='x')
    # stacked obsidian (east), crying blocks set aside
    for x in range(15, 19):
        for z in (7, 8):
            for y in range(1, 3 if x < 18 else 2):
                b.set(x, y, z, OBS)
    b.set(15, 3, 7, OBS)
    b.set(16, 3, 7, CRY)
    # ---------------------------------------------------------------- bond posts with chains strung between
    for x in (7, 13):
        for y in range(1, 4):
            b.set(x, y, 10, WALL)
        b.set(x, 4, 10, CHISELED)
        rod(b, x, 5, 10)
    for x in range(8, 13):
        b.set(x, 3, 10, 'iron_chain', axis='x', waterlogged=False)
    for x in (9, 11):
        b.set(x, 2, 10, 'iron_chain', axis='y', waterlogged=False)
    # ---------------------------------------------------------------- the overseer's dais
    for x in (9, 10, 11):
        stair(b, x, 1, 6, 'south')
        b.set(x, 1, 7, OBS)
    b.set(10, 1, 7, CRY)
    # ---------------------------------------------------------------- spots
    b.spot('stand', 10, 2, 7)          # the overseer on the dais
    b.spot('work', 8, 1, 4)            # at the end-stone heap
    b.spot('work', 13, 1, 3)           # at the purpur cube
    b.spot('work', 14, 1, 8)           # at the obsidian stack
    b.spot('work', 10, 1, 11)          # at the bond posts
    b.spot('work', 4, 1, 13)           # under the shelters
    b.spot('work', 16, 1, 13)
    b.spot('stand', 10, 1, 1)          # at the gate
