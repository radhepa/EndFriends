"""The Gate of Eyes: the only way into a Citadel.

Set INTO the wall line: north face outside, south face inside. It is exactly three wall tiles wide
(27 = 3 x 9): the 19-wide gatehouse sits between four columns of real wall profile on each flank
(copied from ``citadel_wall``), so a square wall with the gate in one side still closes with whole
segments. Like the corner tower it carries the wall's 5-deep profile on local z = 3..7, so it shares
the towers' z origin; wall segments butt against its west face (x = 0) and east face (x = 26). The
wall-walk (floor y = 10, z = 4..6) runs straight through the gatehouse and the Herald's chamber.

Front: a deep portal of three receding pointed orders, the outermost ringed with the Court's eyes;
the Herald's balcony juts from the tympanum above the tunnel; a steep gable echoes the arch, between
two slim spired turrets.
"""
from kit import Build, building

from citadel._parts import (BRICK, CHISELED, CRY, OBS, POLISHED, STAIR, WALL, PANE, WALK_FLOOR, arch, arch_ring,
                            banner, chain, eye, fill_stone, put_stone, rod, slab, spire_cap, stair, stone)

ON_MAGENTA = [{'color': 'black', 'pattern': 'minecraft:rhombus'},
              {'color': 'magenta', 'pattern': 'minecraft:circle'},
              {'color': 'black', 'pattern': 'minecraft:border'}]

W, D = 19, 11                     # the gatehouse proper (drawn by _gatehouse)
DOOR = 9
STUB = 4                          # wall columns on each flank
FULL_W = W + 2 * STUB             # 27: three wall tiles
GATE_H = 32
F = WALK_FLOOR                    # wall-walk / chamber floor layer (stand at 11)
TUN_X, TUN_W, TUN_H = 7, 5, 9      # tunnel: x 7..11, y 1..9
EAVE = 17                         # gatehouse walls / roof eaves
# receding orders on the outside face: (z, x0, width, height, rise)
ORDERS = ((0, 4, 11, 19, 7), (1, 5, 9, 17, 6), (2, 6, 7, 15, 5))
REAR = ((10, 5, 9, 15, 6), (9, 6, 7, 13, 5))


def roof_y(x):
    """Ridge roof over x = 3..15: eaves at 17, ridge at 23 over x = 9."""
    return EAVE + (6 - abs(x - DOOR))


def turret(b, x0):
    """A slim turret column x0..x0+2 the full depth; tall 3 x 3 spires front and back."""
    x1 = x0 + 2
    for y in range(1, 16):
        for x in range(x0, x1 + 1):
            for z in range(D):
                put_stone(b, x, y, z)
    for x in range(x0, x1 + 1):
        for z in range(D):
            for y in (1, 2):
                b.set(x, y, z, OBS)
            b.set(x, 6, z, OBS)
            b.set(x, F, z, OBS)
    # crenellated top of the low middle part
    for z in range(3, 8):
        for x in (x0, x1):
            put_stone(b, x, 16, z)
            if z % 2 == 1:
                slab(b, x, 17, z)
        b.set(x0 + 1, 15, z, POLISHED)
    rod(b, x0 + 1, 16, 5)
    # front spire turret (z = 0..2) and a lower rear one (z = 8..10)
    for zs, top in ((0, 24), (8, 20)):
        for y in range(16, top + 1):
            for x in range(x0, x1 + 1):
                for z in range(zs, zs + 3):
                    put_stone(b, x, y, z)
        for x in range(x0, x1 + 1):
            for z in range(zs, zs + 3):
                b.set(x, top - 2, z, OBS)
        # corner pinnacles
        for x in (x0, x1):
            for z in (zs, zs + 2):
                b.set(x, top + 1, z, WALL)
                rod(b, x, top + 2, z)
        spire_cap(b, x0, zs, 3, top + 1, kind=stone, steep=3 if zs == 0 else 2)
        # glowing slit and an eye on the outward face
        zf = zs if zs == 0 else zs + 2
        for y in range(top - 6, top - 2):
            b.set(x0 + 1, y, zf, PANE)
        b.set(x0 + 1, top - 7, zf, CRY)
        if zs == 0:
            eye(b, x0 + 1, 13, zf, 'north')
    # lower slits on the side faces
    xs = x0 if x0 == 0 else x1
    for y in range(7, 10):
        b.set(xs, y, 1, PANE)
        b.set(xs, y, 9, PANE)


def _gatehouse(b):
    """The 19-wide gatehouse in its own coordinates (x 0..18)."""
    # ground: black road through, polished floors
    for x in range(W):
        for z in range(D):
            b.set(x, 0, z, POLISHED)
    for z in range(D):
        for x in range(TUN_X, TUN_X + TUN_W):
            b.set(x, 0, z, OBS)
        b.set(DOOR, 0, z, CRY if z % 4 == 1 else OBS)
    turret(b, 0)
    turret(b, W - 3)
    # gatehouse body x = 3..15, full depth, up to the eaves; roof above
    fill_stone(b, 3, 1, 0, 15, EAVE - 1, D - 1)
    for x in range(3, 16):
        for z in range(D):
            b.set(x, 1, z, OBS)
    for x in range(3, 16):
        top = roof_y(x)
        for z in range(D):
            for y in range(EAVE, top):
                put_stone(b, x, y, z)
            if x == DOOR:
                b.set(x, top, z, OBS)
            else:
                stair(b, x, top, z, 'east' if x < DOOR else 'west')
    # gable faces: stepped edge on the front and back
    for z in (0, D - 1):
        b.set(DOOR, roof_y(DOOR) + 1, z, WALL)
    # the Herald's chamber (x 4..14, z 4..8, y 11..16) with the wall-walk through it
    b.erase(4, F + 1, 4, 14, EAVE - 1, 8)
    for x in range(4, 15):
        for z in range(4, 9):
            b.set(x, F, z, POLISHED)
            b.set(x, EAVE, z, BRICK)
    for y in range(F + 1, F + 5):
        b.erase(0, y, 4, W - 1, y, 6)
    for x in range(W):
        for z in (4, 5, 6):
            b.set(x, F, z, POLISHED)
    for x in (0, 2, 3, 15, 16, 18):
        for z in (4, 6):
            stair(b, x, F + 4, z, 'north' if z == 4 else 'south', half='top')
    for x in range(4, 15):
        b.set(x, F, 5, OBS)
    b.set(DOOR, F, 5, CRY)
    # tunnel through the whole depth
    tops = arch(b, 'x', TUN_X, TUN_W, 1, TUN_H, 0, D - 1, rise=3, smooth=STAIR)
    # receding orders on both faces
    for z, x0, w, h, r in ORDERS + REAR:
        arch(b, 'x', x0, w, 1, h, z, z, rise=r, smooth=STAIR)
    # ring of the outermost order: obsidian voussoirs, with the Court's eyes set in every third
    ring = [c for c in arch_ring(11, 19, 7) if 3 <= 4 + c[0] <= 15]
    for c, dy in ring:
        b.set(4 + c, 1 + dy, 0, OBS)
    eyes = [(c, dy) for c, dy in ring if dy >= 2]
    mid = len(eyes) // 2
    for k in range(mid % 3, len(eyes), 3):
        c, dy = eyes[k]
        eye(b, 4 + c, 1 + dy, 0, 'north')
    # middle and inner order rings: chiseled and crying obsidian keystones
    for (z, x0, w, h, r) in ORDERS[1:] + REAR:
        for c, dy in arch_ring(w, h, r):
            x, y = x0 + c, 1 + dy
            if 3 <= x <= 15 and b.solid(x, y, z) and not b.get(x, y, z)[0].endswith('_stairs'):
                b.set(x, y, z, OBS if z in (2, 9) else CHISELED)
    b.set(DOOR, 1 + 19, 0, CRY)
    b.set(DOOR, 1 + 17, 1, CRY)
    b.set(DOOR, 1 + 13, 9, CRY)
    # tunnel mouth keystones
    b.set(DOOR, TUN_H + 1, 3, CRY)
    # the Herald's balcony: floor y = 10 jutting from the tympanum (z = 3) out to z = 0, rail on z = 0
    for x in range(6, 13):
        for z in (0, 1, 2):
            b.set(x, F, z, POLISHED)
        b.set(x, F, 0, OBS)
        stair(b, x, F - 1, 0, 'south', half='top')
        b.set(x, F + 1, 0, WALL)
    for x in (5, 13):
        b.set(x, F, 1, POLISHED)
    for x in (6, 12):
        b.set(x, F + 1, 0, OBS)
        rod(b, x, F + 2, 0)
    b.set(DOOR, F + 1, 0, OBS)
    eye(b, DOOR, F + 2, 0, 'north')
    for x in (7, 11):
        chain(b, x, F - 3, F - 2, 0)
        rod(b, x, F - 4, 0, 'down')
    # balcony door into the chamber (3 wide, 4 high)
    arch(b, 'x', 8, 3, F + 1, 5, 3, 3, rise=2)
    # crowning eye at the gable apex, and on the rear gable
    eye(b, DOOR, roof_y(DOOR) + 1, 0, 'north')
    b.set(DOOR, roof_y(DOOR), 0, CRY)
    eye(b, DOOR, roof_y(DOOR) + 1, D - 1, 'south')
    b.set(DOOR, roof_y(DOOR), D - 1, CRY)
    # glowing magenta lancets in the front gable above the arch
    for x in (6, 12):
        for y in (EAVE + 1, EAVE + 2):
            if b.solid(x, y, 0):
                b.set(x, y, 0, PANE)
    # portcullis, raised: iron bars in the tunnel head; chains up through the chamber floor
    for i, t in enumerate(tops):
        x = TUN_X + i
        for y in range(7, 1 + t):
            b.set(x, y, 5, 'iron_bars')
    # tunnel lights: glowing panels in the side walls, rods under the vault
    for z in (2, 5, 8):
        b.set(TUN_X - 1, 4, z, CRY)
        b.set(TUN_X + TUN_W, 4, z, CRY)
    for z in (3, 7):
        rod(b, DOOR, TUN_H, z, 'down')
    # chamber: the Herald's lectern of proclamations, banners, a hanging light
    b.set(DOOR, F + 1, 8, 'lectern', facing='north', has_book=False, powered=False)
    banner(b, 6, F + 4, 8, 'north')
    banner(b, 12, F + 4, 8, 'north')
    for x in (5, 13):
        banner(b, x, F + 4, 3, 'south', color='magenta', patterns=ON_MAGENTA)
    chain(b, DOOR, EAVE - 2, EAVE - 1, 6)
    rod(b, DOOR, EAVE - 3, 6, 'down')
    rod(b, 4, F + 1, 8)
    rod(b, 14, F + 1, 8)
    # spots: the Herald on the balcony, guards in the outer arch (both faces), a warden in the chamber
    b.spot('stand', DOOR, F + 1, 1)
    b.spot('stand', 5, 1, 0)
    b.spot('stand', 13, 1, 0)
    b.spot('stand', 6, 1, D - 1)
    b.spot('stand', 12, 1, D - 1)
    b.spot('work', DOOR, F + 1, 7)


@building('gate_of_eyes', people='court', role='gate', size=(FULL_W, GATE_H, D), door=STUB + DOOR, wall_z=(3, 7),
          walk_y=F + 1, tunnel=(STUB + TUN_X, STUB + TUN_X + TUN_W - 1), tiles=3,
          about="The only way in: a deep pointed obsidian portal of three orders ringed with the Court's eyes, "
                "the Herald's balcony above the tunnel, a steep gable and two spired turrets, flanked by wall; "
                "three wall tiles wide, and the wall-walk runs through.")
def gate_of_eyes(b):
    from citadel.walls import wall_segment
    house = Build('gatehouse', (W, GATE_H, D))
    _gatehouse(house)
    # paved forecourt and inner court under the flanks
    for x in range(FULL_W):
        for z in range(D):
            b.set(x, 0, z, POLISHED)
    b.paste(house, STUB, 0, 0)
    for spot in house.meta.get('spots', []):
        x, y, z = spot['pos']
        b.spot(spot['kind'], x + STUB, y, z)
    # four columns of wall on each flank, continuing the wall's own rhythm (x 0..3 west, 5..8 east)
    wall = wall_segment()
    for (x, y, z), state in wall.grid.items():
        if x < STUB:
            b.set(x, y, z + 3, state, nbt=wall.nbt.get((x, y, z)))
        elif x > 8 - STUB:
            b.set(x + FULL_W - 9, y, z + 3, state, nbt=wall.nbt.get((x, y, z)))
    # glowing inlays light the paving in front of and behind the flanks
    for x in (1, FULL_W - 2):
        for z in (1, D - 2):
            b.set(x, 0, z, CRY)
