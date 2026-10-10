"""The Market: the shared centre of a Crossing.

Purpur tiles on the west (Shulkin) half, end stone on the east (Chorrin) half, meeting down the middle
in interlocking teeth that swirl into a two-lobed emblem round the centre: the Old Accord, the shell and
the grove, each holding a dot of the other. On the emblem stands the Accord Lamp: a purpur column wrapped
in planted chorus, crowned with a little shulker shell (glass gap glowing with a froglight, purpur lid,
end rod). Its planter's rim is a ring of seats. Four striped tent stalls stand in the corners, Shulkin
on the purpur half, Chorrin on the end-stone half, each with an L-shaped counter facing the crossroads.
The outer ring and the four avenues stay open: paths can arrive at any point of the rim.
"""
import math
import random

import kit
from kit import building
import shared.decor  # noqa: F401  (registers the street decor pasted at the entrances)
from shared._parts import grow, hanging_sign, banner, toward, BACK, EYE_OF_THE_SPIRES

N = 23
C = 11            # centre column
R = 6.5           # emblem radius


def shell_side(dx, dz):
    """The Accord emblem: True where the purpur (shell) half is, False for end stone (grove)."""
    h = R / 2
    if dx * dx + (dz + h) ** 2 <= 1.05:
        return True              # the shell's dot in the grove lobe
    if dx * dx + (dz - h) ** 2 <= 1.05:
        return False             # the grove's dot in the shell lobe
    if dx * dx + (dz + h) ** 2 <= h * h:
        return False
    if dx * dx + (dz - h) ** 2 <= h * h:
        return True
    return dx < 0


def seam(z):
    """x of the first end-stone cell on row z outside the emblem: teeth two rows tall, three deep."""
    return C + (2 if (z // 2) % 2 else -1)


def floor(b, rng):
    for z in range(N):
        for x in range(N):
            dx, dz = x - C, z - C
            r = math.hypot(dx, dz)
            rim = x in (0, N - 1) or z in (0, N - 1)
            if r <= R:
                west = shell_side(dx, dz)
                spec = ('purpur_pillar', {'axis': 'y'}) if west else ('end_stone', {})
            elif r <= R + 0.8:
                # a ring of the other people's stone frames the emblem
                west = x < C
                spec = ('end_stone_bricks', {}) if west else ('purpur_block', {})
            else:
                west = x < seam(z)
                if rim:
                    spec = ('purpur_pillar', {'axis': 'z' if x in (0, N - 1) else 'x'}) if west else ('end_stone_bricks', {})
                elif west:
                    # purpur basketweave: 2x2 blocks of pillars laid alternately
                    axis = 'x' if ((x // 2) + (z // 2)) % 2 else 'z'
                    spec = ('purpur_block', {}) if (x % 6 == 3 and z % 6 == 3) else ('purpur_pillar', {'axis': axis})
                else:
                    spec = ('end_stone', {}) if rng.random() < 0.28 else ('end_stone_bricks', {})
            b.set(x, 0, z, spec[0], **spec[1])


def accord_lamp(b):
    """The centre: a seat-rimmed planter, chorus wrapped round a purpur column, a shulker-shell lamp."""
    for dz in range(-2, 3):
        for dx in range(-2, 3):
            x, z = C + dx, C + dz
            ring = max(abs(dx), abs(dz))
            if ring <= 1:
                b.set(x, 1, z, 'end_stone')
            elif abs(dx) == 2 and abs(dz) == 2:
                if dx < 0:
                    b.set(x, 1, z, 'purpur_pillar', axis='y')
                    b.end_rod(x, 2, z, 'up')
                else:
                    b.set(x, 1, z, 'end_stone_brick_wall')
                    b.lantern(x, 2, z)
            else:
                stairs = 'purpur_stairs' if shell_side(dx, dz) else 'end_stone_brick_stairs'
                b.set(x, 1, z, stairs, facing=toward(-dx, -dz), half='bottom')
                b.spot('sit', x, 1, z)
    # the column
    for y in range(1, 8):
        b.set(C, y, C, 'purpur_pillar', axis='y')
    # chorus wrapped round it (vanilla-safe: branches only from the top of a stalk)
    grow(b, C, 2, C - 1, 3, [('west', 2, ()), ('east', 1, ())])
    grow(b, C, 2, C + 1, 4, [('west', 2, ()), ('east', 1, ())])
    grow(b, C - 1, 2, C, 2)
    grow(b, C + 1, 2, C, 2)
    # corbels under the lamp
    for d in ('north', 'south', 'east', 'west'):
        dx, dz = {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}[d]
        b.set(C + dx, 7, C + dz, 'purpur_stairs', facing=BACK[d], half='top')
    # the shell: glowing gap round a froglight, then the lid with its lip
    for dz in (-1, 0, 1):
        for dx in (-1, 0, 1):
            b.set(C + dx, 8, C + dz, 'magenta_stained_glass')
            b.set(C + dx, 9, C + dz, 'purpur_block')
            b.set(C + dx, 10, C + dz, 'purpur_slab', type='bottom')
    b.set(C, 8, C, 'pearlescent_froglight', axis='y')
    for d, (dx, dz) in {'north': (0, -2), 'south': (0, 2), 'east': (2, 0), 'west': (-2, 0)}.items():
        for s in (-1, 0, 1):
            x, z = (C + dx + s, C + dz) if dz else (C + dx, C + dz + s)
            b.set(x, 9, z, 'purpur_stairs', facing=BACK[d], half='top')
    b.set(C, 10, C, 'purpur_block')
    b.end_rod(C, 11, C, 'up')
    for dx, dz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        b.end_rod(C + 2 * dx, 9, C + 2 * dz, 'up')


def tent(b, x0, z0, x1, z1, y, ca, cb, skip_corners=False):
    """A striped pyramid of wool stairs over the box (x0..x1, z0..z1), eaves at layer y, rising one
    layer per ring to a flat wool crown. Stripes run down each face (colours ca, cb)."""
    x0, x1, z0, z1 = min(x0, x1), max(x0, x1), min(z0, z1), max(z0, z1)
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    for z in range(z0, z1 + 1):
        for x in range(x0, x1 + 1):
            ring = min(x - x0, x1 - x, z - z0, z1 - z)
            corner = ring == 0 and (x in (x0, x1)) and (z in (z0, z1))
            if corner and skip_corners:
                continue
            inner = ring >= min(x1 - x0, z1 - z0) // 2
            dx, dz = cx - x, cz - z
            if inner:
                b.set(x, y + ring, z, f'{ca}_wool')
                continue
            if abs(dx) > abs(dz):
                facing, along = ('east' if dx > 0 else 'west'), z
            else:
                facing, along = ('south' if dz > 0 else 'north'), x
            colour = ca if along % 2 == 0 else cb
            b.set(x, y + ring, z, f'{colour}_wool_stairs', facing=facing, half='bottom')


TENTS = {
    # kind: post, stripes (a, b), counter stairs, rug
    'shulkin': ('purpur_pillar', ('magenta', 'purple'), 'purpur_stairs', 'purple_carpet'),
    'chorrin': ('end_stone_brick_wall', ('white', 'brown'), 'end_stone_brick_stairs', 'brown_carpet'),
    'chorrin2': ('end_stone_brick_wall', ('white', 'purple'), 'end_stone_brick_stairs', 'white_carpet'),
}


def corner_stall(b, qx, qz, kind, goods, sign):
    """A 6x6 striped tent in the corner (qx, qz) (-1 = west/north), counter facing the crossroads."""
    post, (ca, cb), counter, rug = TENTS[kind]
    shulkin = kind == 'shulkin'

    def X(u):
        return 1 + u if qx < 0 else N - 2 - u

    def Z(v):
        return 1 + v if qz < 0 else N - 2 - v

    in_u = 'east' if qx < 0 else 'west'      # direction of +u (toward the avenue)
    in_v = 'south' if qz < 0 else 'north'    # direction of +v
    # rug, posts, counter
    for u in range(1, 5):
        for v in range(1, 5):
            b.set(X(u), 1, Z(v), rug)
    for u, v in ((0, 0), (5, 0), (0, 5), (5, 5)):
        for y in range(1, 5 if not shulkin else 6):
            b.set(X(u), y, Z(v), post, **({'axis': 'y'} if post == 'purpur_pillar' else {}))
    for k in range(1, 5):
        b.set(X(5), 1, Z(k), counter, facing=BACK[in_u], half='top')
        b.set(X(k), 1, Z(5), counter, facing=BACK[in_v], half='top')
    tent(b, X(0), Z(0), X(5), Z(5), 4, ca, cb, skip_corners=True)
    # lights: posts carry lamps above the eaves, and one hangs under the crown
    for u, v in ((0, 0), (5, 0), (0, 5), (5, 5)):
        if shulkin:
            b.end_rod(X(u), 6, Z(v), 'up')
        else:
            b.lantern(X(u), 5, Z(v))
    if shulkin:
        b.end_rod(X(2), 5, Z(2), 'down')
        b.end_rod(X(3), 5, Z(3), 'down')
    else:
        b.lantern(X(2), 5, Z(2), hanging=True)
        b.lantern(X(3), 5, Z(3), hanging=True)
    # the trader stands in the crook of the counter
    b.spot('work', X(4), 1, Z(4))
    # a hanging sign over the long counter, readable from the avenue
    hanging_sign(b, X(5), 3, Z(2), sign, facing=in_u, wood='crimson' if shulkin else 'pale_oak',
                 color='magenta' if shulkin else 'white')
    goods(b, X, Z, in_u, in_v)


# ------------------------------------------------------------------ what each stall sells
def void_cloth(b, X, Z, in_u, in_v):
    """Shulkin weaver: bolts of void cloth, a loom, banners."""
    b.set(X(1), 1, Z(1), 'purple_wool')
    b.set(X(1), 2, Z(1), 'magenta_wool')
    b.set(X(2), 1, Z(1), 'magenta_wool')
    b.set(X(1), 1, Z(2), 'purple_wool')
    b.set(X(1), 2, Z(2), 'purple_wool')
    b.set(X(1), 1, Z(3), 'loom', facing=in_u)
    banner(b, X(3), 1, Z(1), base='purple', patterns=EYE_OF_THE_SPIRES, facing=in_v)
    b.set(X(5), 2, Z(1), 'magenta_carpet')
    b.set(X(5), 2, Z(2), 'purple_carpet')
    b.candles(X(5), 2, Z(4), 2, color='magenta')
    b.set(X(2), 2, Z(5), 'magenta_carpet')
    b.candles(X(4), 2, Z(5), 3, color='purple')


def lamps(b, X, Z, in_u, in_v):
    """Shulkin lamplighter: end rods by the bundle, magenta glass, a ledger."""
    b.set(X(1), 1, Z(1), 'magenta_stained_glass')
    b.set(X(2), 1, Z(1), 'magenta_stained_glass')
    b.set(X(1), 2, Z(1), 'purpur_slab', type='bottom')
    b.set(X(1), 1, Z(2), 'barrel', facing='up', open=False)
    b.end_rod(X(1), 2, Z(2), 'up')
    b.set(X(1), 1, Z(3), 'lectern', facing=in_u, has_book=False, powered=False)
    for k in (1, 3):
        b.end_rod(X(5), 2, Z(k), in_v)
    b.set(X(5), 2, Z(2), 'magenta_stained_glass_pane')
    b.candles(X(5), 2, Z(4), 1, color='magenta')
    b.end_rod(X(1), 2, Z(5), in_u)
    b.end_rod(X(3), 2, Z(5), in_u)
    b.set(X(2), 2, Z(5), 'magenta_stained_glass_pane')


def chorus_fruit(b, X, Z, in_u, in_v):
    """Chorrin grove-tender: chorus by the stem (planted in the counter), baskets, pots."""
    b.set(X(1), 1, Z(1), 'barrel', facing='up', open=False)
    b.set(X(2), 1, Z(1), 'barrel', facing=in_v, open=False)
    b.set(X(1), 2, Z(1), 'barrel', facing='up', open=False)
    b.set(X(1), 1, Z(2), 'decorated_pot', facing=in_u)
    b.set(X(1), 1, Z(3), 'composter', level=7)
    # the long counter has a planting box: end stone with chorus flowers for sale
    for k in (1, 3):
        b.set(X(5), 1, Z(k), 'end_stone')
        b.set(X(5), 2, Z(k), 'chorus_flower', age=5)
    b.set(X(5), 1, Z(2), 'pearlescent_froglight', axis='y')
    b.set(X(5), 2, Z(2), 'decorated_pot', facing=in_u)
    b.set(X(1), 2, Z(5), 'brown_carpet')
    b.candles(X(3), 2, Z(5), 2, color='white')


def brews(b, X, Z, in_u, in_v):
    """Chorrin brewer: draughts on the counter, a cauldron, popped chorus (purpur) for the Shulkin."""
    b.set(X(1), 1, Z(1), 'cauldron')
    b.set(X(2), 1, Z(1), 'purpur_block')
    b.set(X(2), 2, Z(1), 'purpur_slab', type='bottom')
    b.set(X(1), 1, Z(2), 'purpur_block')
    b.set(X(1), 2, Z(2), 'purpur_block')
    b.set(X(1), 1, Z(3), 'barrel', facing=in_u, open=False)
    b.set(X(5), 2, Z(2), 'brewing_stand', has_bottle_0=True, has_bottle_1=False, has_bottle_2=True)
    b.set(X(5), 2, Z(4), 'decorated_pot', facing=in_u)
    b.set(X(5), 1, Z(3), 'pearlescent_froglight', axis='y')
    b.candles(X(2), 2, Z(5), 3, color='brown')
    b.set(X(4), 2, Z(5), 'flower_pot')


@building('market', people='shared', role='plaza', size=(N, 12, N), door=C, entrances=('north', 'east', 'south', 'west'),
          about='The Crossing market: purpur and end stone meeting in a swirl round a chorus-wrapped shell lamp, '
                'with four striped tent stalls in the corners.')
def market(b):
    rng = random.Random(1123)
    floor(b, rng)
    accord_lamp(b)
    corner_stall(b, -1, -1, 'shulkin', void_cloth, ['Void Cloth', 'bolts and', 'banners'])
    corner_stall(b, -1, 1, 'shulkin', lamps, ['Rods and', 'Lenses', 'lit to order'])
    corner_stall(b, 1, -1, 'chorrin', chorus_fruit, ['Chorus', 'fresh and', 'popped'])
    corner_stall(b, 1, 1, 'chorrin2', brews, ['Brews', 'and pots'])
    # the entrances, each marked by the people whose half it opens on (north and south by both)
    for name, x, z in (('decor_spire_lamp', 8, 2), ('decor_stead_lamp', 14, 2),
                       ('decor_spire_banner_post', 8, 20), ('decor_chorus_planter', 14, 20),
                       ('decor_spire_banner_post', 1, 8), ('decor_spire_banner_post', 1, 14),
                       ('decor_stead_lamp', 21, 8), ('decor_stead_lamp', 21, 14)):
        place(b, name, x, z)


def place(b, name, cx, cz):
    """Paste a catalogued decor piece centred on (cx, cz), its ground layer on the plaza floor."""
    d = kit.make(name)
    b.paste(d, cx - d.w // 2, -d.ground, cz - d.d // 2)
