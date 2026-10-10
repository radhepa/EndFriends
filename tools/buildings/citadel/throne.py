"""The Throne Hall: the Lord's basilica.

A tall nave between purpur-pillar arcades, low aisles held up by flying buttresses, a deep eyed
portal under a rose window of magenta glass, and at the south end the Lord's throne on a three-step
dais, its back crowned with the Lord's eight eyes, under Court banners.
"""
import math

from kit import building

from citadel._parts import (BRICK, CHISELED, CRY, OBS, POLISHED, STAIR, WALL, GLASS, PANE, PSTAIR, arch, arch_ring,
                            banner, chain, eye, pillar, put_stone, rod, slab, spire_cap, stair, stone)

W, D = 27, 31
C = 13                              # centre line
NAVE = (9, 17)                      # nave interior x
ARC = (8, 18)                       # arcade lines
AISLE = ((3, 7), (19, 23))          # aisle interiors
OUT = (2, 24)                       # outer aisle walls
Z0, Z1 = 4, 27                      # interior z
PIERS = (7, 11, 15, 19, 23)         # pier z positions
BAYS = (5, 9, 13, 17, 21, 25)       # bay centres
AISLE_TOP = 10                      # aisle wall top / aisle ceiling
NAVE_TOP = 19                       # nave wall top / ceiling layer
H = 31

ON_MAGENTA = [{'color': 'black', 'pattern': 'minecraft:rhombus'},
              {'color': 'magenta', 'pattern': 'minecraft:circle'},
              {'color': 'black', 'pattern': 'minecraft:border'}]
ON_PURPLE = [{'color': 'magenta', 'pattern': 'minecraft:rhombus'},
             {'color': 'black', 'pattern': 'minecraft:circle'},
             {'color': 'black', 'pattern': 'minecraft:border'}]


def roof_y(x):
    """Steep nave roof: eaves 20 at the arcade lines, ridge 25 over the centre."""
    return NAVE_TOP + 1 + (5 - abs(x - C))


def aisle_roof_y(x):
    d = x - OUT[0] if x < C else OUT[1] - x      # 0 at the outer wall .. 5 at the arcade
    return AISLE_TOP + 1 + d // 2


@building('throne_hall', people='court', role='civic', size=(W, H, D), door=C,
          about='The Lord\'s hall: a tall nave between purpur-pillar arcades, aisles braced by flying buttresses, '
                'magenta lancets and a rose window, chandeliers of end rods, and the throne on a three-step dais '
                'crowned with eight eyes under Court banners.')
def throne_hall(b):
    # ---------------------------------------------------------------- floor
    for x in range(W):
        for z in range(D):
            b.set(x, 0, z, POLISHED)
    for z in range(Z0, Z1 + 1):
        for x in range(OUT[0], OUT[1] + 1):
            b.set(x, 0, z, POLISHED if (x + z) % 2 else BRICK)
        for x in (NAVE[0], NAVE[1]):
            b.set(x, 0, z, OBS)
    for z in PIERS:
        for x in range(OUT[0], OUT[1] + 1):
            b.set(x, 0, z, OBS)
    for z in BAYS[1:-1]:
        for x in (5, 21):
            b.set(x, 0, z, CRY)
        for x in (10, 16):
            b.set(x, 0, z, CRY)
    # ---------------------------------------------------------------- outer aisle walls + rear wall
    for z in range(2, Z1 + 3):
        for y in range(1, AISLE_TOP + 1):
            for x in OUT:
                put_stone(b, x, y, z)
    for x in range(OUT[0], OUT[1] + 1):
        for y in range(1, NAVE_TOP + 1):
            for z in (Z1 + 1, Z1 + 2):
                if y <= AISLE_TOP or ARC[0] <= x <= ARC[1]:
                    put_stone(b, x, y, z)
    for x in range(OUT[0], OUT[1] + 1):
        for z in range(2, Z1 + 3):
            if x in OUT or z in (2, 3, Z1 + 1, Z1 + 2):
                b.set(x, 1, z, OBS)
    # obsidian string course at the aisle-window sills
    for z in range(2, Z1 + 3):
        for x in OUT:
            b.set(x, 2, z, OBS)
            b.set(x, AISLE_TOP, z, OBS)
    # ---------------------------------------------------------------- arcades: purpur piers, pointed arches, clerestory
    for z in range(Z0, Z1 + 1):
        for x in ARC:
            for y in range(1, NAVE_TOP + 1):
                put_stone(b, x, y, z)
    for i in range(len(PIERS) + 1):
        z_lo = (Z0 if i == 0 else PIERS[i - 1] + 1)
        z_hi = (PIERS[i] - 1 if i < len(PIERS) else Z1)
        width = z_hi - z_lo + 1
        for x in ARC:
            arch(b, 'z', z_lo, width, 1, 8, x, x, rise=2, smooth=STAIR)
    for z in PIERS:
        for x in ARC:
            pillar(b, x, 1, 8, z)
            b.set(x, 9, z, CHISELED)
            # capital lights facing into the nave and the aisle
            rod(b, x + (1 if x == ARC[0] else -1), 9, z, 'east' if x == ARC[0] else 'west')
            rod(b, x + (-1 if x == ARC[0] else 1), 9, z, 'west' if x == ARC[0] else 'east')
    # the arcade's first and last bays meet the end walls as half-piers
    for x in ARC:
        for z in (Z0, Z1):
            pillar(b, x, 1, 7, z)
    # obsidian band over the arcade, chiseled cornice under the ceiling
    for z in range(Z0, Z1 + 1):
        for x in ARC:
            b.set(x, AISLE_TOP + 1, z, OBS)
            b.set(x, NAVE_TOP - 1, z, CHISELED)
    # clerestory lancets (magenta) over every bay
    for z in BAYS:
        for x in ARC:
            for y in range(AISLE_TOP + 3, NAVE_TOP - 2):
                b.set(x, y, z, GLASS)
    # ---------------------------------------------------------------- aisle windows and buttresses
    for z in BAYS:
        for x in OUT:
            for y in range(3, 9):
                b.set(x, y, z, GLASS)
            b.set(x, 9, z, CHISELED)
    for z in PIERS + (Z1 + 1,):
        for side, xo, xb in ((0, 0, 1), (1, W - 1, W - 2)):
            # stepped buttress against the aisle wall
            for y in range(1, AISLE_TOP + 1):
                put_stone(b, xb, y, z)
                if y <= 6:
                    put_stone(b, xo, y, z)
            stair(b, xo, 7, z, 'east' if side == 0 else 'west')
            for y in (1, 2):
                b.set(xo, y, z, OBS)
                b.set(xb, y, z, OBS)
            # pinnacle on the buttress head with a watching eye
            put_stone(b, xb, AISLE_TOP + 1, z)
            put_stone(b, xb, AISLE_TOP + 2, z)
            b.set(xb, AISLE_TOP + 3, z, WALL)
            rod(b, xb, AISLE_TOP + 4, z)
            # flying buttress: an arm climbing over the aisle roof to the clerestory
            for k, x in enumerate(range(OUT[0], ARC[0]) if side == 0 else range(OUT[1], ARC[1], -1)):
                y = AISLE_TOP + 3 + k
                put_stone(b, x, y, z)
                stair(b, x, y - 1, z, 'west' if side == 0 else 'east', half='top')
    # ---------------------------------------------------------------- aisle roofs (lean-to) and ceilings
    for x in list(range(OUT[0], ARC[0])) + list(range(ARC[1] + 1, OUT[1] + 1)):
        ry = aisle_roof_y(x)
        for z in range(2, Z1 + 3):
            if b.solid(x, ry, z):
                continue
            for y in range(AISLE_TOP + 1, ry):
                put_stone(b, x, y, z)
            d = x - OUT[0] if x < C else OUT[1] - x
            if d % 2 == 0:
                stair(b, x, ry, z, 'east' if x < C else 'west')
            else:
                slab(b, x, ry, z)
    for x in list(range(AISLE[0][0], AISLE[0][1] + 1)) + list(range(AISLE[1][0], AISLE[1][1] + 1)):
        for z in range(Z0, Z1 + 1):
            b.set(x, AISLE_TOP, z, BRICK)
    # ---------------------------------------------------------------- nave ceiling and roof
    for x in range(NAVE[0], NAVE[1] + 1):
        for z in range(Z0, Z1 + 1):
            b.set(x, NAVE_TOP, z, BRICK)
    for z in range(Z0, Z1 + 1, 4):
        for x in range(NAVE[0], NAVE[1] + 1):
            b.set(x, NAVE_TOP, z, OBS)
    for x in range(ARC[0] - 1, ARC[1] + 2):
        top = roof_y(x)
        for z in range(1, Z1 + 3):
            for y in range(NAVE_TOP + 1, top):
                if not b.solid(x, y, z):
                    put_stone(b, x, y, z)
            if x == C:
                b.set(x, top, z, OBS)
            else:
                stair(b, x, top, z, 'east' if x < C else 'west')
    # ridge cresting: a spine of walls with rods
    for z in range(1, Z1 + 3):
        if z % 3 == 0:
            b.set(C, roof_y(C) + 1, z, WALL)
            if z % 6 == 3:
                rod(b, C, roof_y(C) + 2, z)
    for z in (1, Z1 + 2):
        rod(b, C, roof_y(C) + 2, z)
    # ---------------------------------------------------------------- the facade (z = 0..3)
    # nave front: a thick gable wall
    for x in range(ARC[0], ARC[1] + 1):
        top = roof_y(x)
        for z in range(0, 4):
            for y in range(1, top + (1 if z < 2 else 0)):
                put_stone(b, x, y, z)
    for x in range(ARC[0], ARC[1] + 1):
        for z in (0, 1):
            b.set(x, 1, z, OBS)
            b.set(x, 2, z, OBS)
            stair(b, x, roof_y(x) + 0, z, 'east' if x < C else 'west') if x != C else b.set(x, roof_y(x), z, OBS)
    # aisle fronts (z = 2..3) to the aisle roof
    for x in list(range(OUT[0], ARC[0])) + list(range(ARC[1] + 1, OUT[1] + 1)):
        for z in (2, 3):
            for y in range(1, aisle_roof_y(x)):
                put_stone(b, x, y, z)
    # facade turrets at the nave corners (3 x 3) with spires
    for tx in (ARC[0] - 2, ARC[1]):
        for y in range(1, roof_y(ARC[0]) + 4):
            for x in range(tx, tx + 3):
                for z in range(0, 3):
                    put_stone(b, x, y, z)
        for x in range(tx, tx + 3):
            for z in range(0, 3):
                for y in (1, 2, AISLE_TOP + 1, NAVE_TOP + 1):
                    b.set(x, y, z, OBS)
        top = roof_y(ARC[0]) + 4
        for x, z in ((tx, 0), (tx + 2, 0), (tx, 2), (tx + 2, 2)):
            b.set(x, top, z, WALL)
            rod(b, x, top + 1, z)
        spire_cap(b, tx, 0, 3, top, kind=stone, steep=2)
        for y in range(AISLE_TOP + 3, NAVE_TOP - 1):
            b.set(tx + 1, y, 0, PANE)
        eye(b, tx + 1, AISLE_TOP + 2, 0, 'north')
    # the portal: three receding orders cut into the nave front, passage through to the nave
    arch(b, 'x', C - 2, 5, 1, 10, 0, 3, rise=3, smooth=STAIR)          # passage 5 wide, 10 high
    arch(b, 'x', C - 3, 7, 1, 12, 0, 0, rise=4, smooth=STAIR)          # outer order
    ring = [c for c in arch_ring(7, 12, 4)]
    for c, dy in ring:
        b.set(C - 3 + c, 1 + dy, 0, OBS)
    eyes = [(c, dy) for c, dy in ring if dy >= 2]
    mid = len(eyes) // 2
    for k in range(mid % 3, len(eyes), 3):
        c, dy = eyes[k]
        eye(b, C - 3 + c, 1 + dy, 0, 'north')
    for c, dy in arch_ring(5, 10, 3):
        if b.solid(C - 2 + c, 1 + dy, 1) and not b.get(C - 2 + c, 1 + dy, 1)[0].endswith('_stairs'):
            b.set(C - 2 + c, 1 + dy, 1, CHISELED)
    b.set(C, 11, 1, CRY)
    # steps up to the portal
    for x in range(C - 3, C + 4):
        b.set(x, 0, 0, OBS)
    # rose window in the gable: magenta glass disc with obsidian tracery
    rc, ry, rr = C, 16, 2.6
    for x in range(C - 3, C + 4):
        for y in range(ry - 3, ry + 4):
            d = math.hypot(x - rc, y - ry)
            if d <= rr:
                spoke = (x == rc or y == ry or abs(x - rc) == abs(y - ry)) and d > 0.5
                b.set(x, y, 0, OBS if spoke or d > rr - 0.6 and False else GLASS)
                for z in (1, 2, 3):
                    b.set(x, y, z, GLASS) if z == 3 else b.erase(x, y, z, x, y, z)
            elif d <= rr + 1.0:
                b.set(x, y, 0, OBS)
    b.set(rc, ry, 0, CRY)
    # crowning eye on the gable apex
    eye(b, C, roof_y(C) + 1, 0, 'north')
    # ---------------------------------------------------------------- the rear wall: tall lancets over the throne
    for x in (C - 2, C, C + 2):
        top = 17 if x == C else 16
        for y in range(13, top + 1):
            b.set(x, y, Z1 + 1, GLASS)
            b.set(x, y, Z1 + 2, GLASS)
    for x in range(ARC[0], ARC[1] + 1):
        top = roof_y(x)
        for y in range(NAVE_TOP + 1, top):
            put_stone(b, x, y, Z1 + 2)
    eye(b, C, roof_y(C) + 1, Z1 + 2, 'south')
    # rear buttresses (z = 30) at the arcade lines
    for x in ARC:
        for y in range(1, NAVE_TOP - 2):
            put_stone(b, x, y, D - 1)
        stair(b, x, NAVE_TOP - 2, D - 1, 'north')
    # ---------------------------------------------------------------- the dais and throne
    for x in range(NAVE[0] + 1, NAVE[1]):
        stair(b, x, 1, 21, 'north')
        b.set(x, 1, 22, OBS)
        stair(b, x, 2, 22, 'north')
        for z in range(23, Z1 + 1):
            b.set(x, 1, z, OBS)
            b.set(x, 2, z, OBS)
            stair(b, x, 3, z, 'north') if z == 23 else b.set(x, 3, z, POLISHED)
    for z in range(24, Z1 + 1):
        for x in range(NAVE[0] + 1, NAVE[1]):
            if C - 1 <= x <= C + 1 and z < 26:
                b.set(x, 4, z, 'purple_carpet')
    # the throne: seat, arms, a tall back of obsidian with a crying-obsidian heart
    stair(b, C, 4, 26, 'north', kind=PSTAIR)
    for x in (C - 1, C + 1):
        b.set(x, 4, 26, OBS)
        b.set(x, 5, 26, 'polished_blackstone_slab', type='bottom')
    for y in range(4, 13):
        for x in (C - 1, C, C + 1):
            b.set(x, y, 27, OBS)
    for y in (6, 7, 8, 9):
        b.set(C, y, 27, CRY)
    b.set(C, 13, 27, OBS)
    b.set(C, 14, 27, OBS)
    for x in (C - 2, C + 2):
        pillar(b, x, 4, 10, 27)
        b.set(x, 11, 27, CHISELED)
    rod(b, C, 15, 27)
    # the Lord's eight eyes crowning the throne back: an upright arc on brackets against the rear
    # wall (vertical, so it can never be a portal ring)
    for x, y in ((C - 4, 8), (C + 4, 8), (C - 3, 10), (C + 3, 10)):
        b.set(x, y, 27, CHISELED)
    for x, y in ((C - 4, 9), (C - 3, 11), (C - 2, 12), (C - 1, 13), (C + 1, 13), (C + 2, 12), (C + 3, 11), (C + 4, 9)):
        eye(b, x, y, 27, 'north')
    # banners behind the throne, along the arcade piers, and in the aisles
    for x, color, pats in ((C - 4, 'magenta', ON_MAGENTA), (C + 4, 'magenta', ON_MAGENTA),
                           (C - 3, 'black', None), (C + 3, 'black', None)):
        banner(b, x, 12 if color == 'magenta' else 9, Z1, 'north', color=color, patterns=pats)
    for z in PIERS:
        for x in ARC:
            facing = 'east' if x == ARC[0] else 'west'
            xx = x + (1 if x == ARC[0] else -1)
            banner(b, xx, 15, z, facing, color='purple', patterns=ON_PURPLE)
    # ---------------------------------------------------------------- the nave carpet and chandeliers
    for z in range(Z0, 21):
        for x in (C - 1, C, C + 1):
            b.set(x, 1, z, 'purple_carpet' if x == C else 'black_carpet')
    for z in (8, 13, 18):
        chain(b, C, NAVE_TOP - 4, NAVE_TOP - 1, z)
        b.set(C, NAVE_TOP - 5, z, CRY)
        for dx, dz, f in ((1, 0, 'east'), (-1, 0, 'west'), (0, 1, 'south'), (0, -1, 'north')):
            rod(b, C + dx, NAVE_TOP - 5, z + dz, f)
        rod(b, C, NAVE_TOP - 6, z, 'down')
    # lights over the dais and in the aisles
    for z in (24, 26):
        for x in (NAVE[0], NAVE[1]):
            rod(b, x, 4, z)
    for z in BAYS:
        for x, f in ((AISLE[0][0], 'east'), (AISLE[1][1], 'west')):
            rod(b, x, 7, z, f)
    # ---------------------------------------------------------------- outside lights: glowing base stones
    for z in PIERS + (Z1 + 1,):
        b.set(0, 1, z, CRY)
        b.set(W - 1, 1, z, CRY)
    for x in (4, W - 5):
        b.set(x, 1, 2, CRY)
        b.set(x, 1, Z1 + 2, CRY)
    b.set(C, 1, Z1 + 2, CRY)
    for z in (1, 3):
        b.set(C, 0, z, CRY)
    # ---------------------------------------------------------------- the Court in attendance
    b.spot('work', C, 5, 26)                    # the Lord on the throne
    for x in (C - 2, C + 2):
        b.spot('stand', x, 4, 24)               # Voidmarshals at the Lord's side
    for x in (NAVE[0] + 1, NAVE[1] - 1):
        b.spot('stand', x, 1, 20)               # Riftguards at the foot of the dais
        b.spot('stand', x, 1, Z0 + 1)           # guards at the door
    for z in (9, 13, 17):
        b.spot('stand', NAVE[0] + 1, 1, z)      # courtiers along the nave
        b.spot('stand', NAVE[1] - 1, 1, z)
