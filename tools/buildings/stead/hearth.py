"""The Cook's Hearth: where the whole Stead eats together. A broad, shallow dome held up on eight slender
posts and open on every side, over a stone oven of smokers and cooking fires whose chimney rises through
the crown; round it, long low tables with woven floor cushions, Chorrin-fashion."""
import math

from kit import building
from stead._parts import Dome, hanging_lantern, pot, toward, ES, ESB, SLAB, STAIRS, WALL

C = 6


@building('cooks_hearth', people='chorrin', role='civic', size=(13, 14, 13), ground=0, door=6, job='cook',
          about='A shallow dome on eight slender posts, open on every side, over a stone oven of smokers and '
                'cooking fires with a chimney through the crown; long low tables with woven floor cushions.')
def cooks_hearth(b):
    d = Dome(b, C, C, 6.2, 6.2, floor=0, crown=8.6, wall_top=5, power=0.5).build()
    # open the sides: eight slender posts carry the ring beam; round the tops of the openings
    ring = sorted({(x, z) for (x, y, z) in d.shell if y == 1})
    posts = set()
    for i in range(8):
        a = math.radians(22.5 + 45 * i)
        px, pz = C + 6 * math.sin(a), C - 6 * math.cos(a)
        posts.add(min(ring, key=lambda c: (c[0] - px) ** 2 + (c[1] - pz) ** 2))
    for (x, z) in ring:
        for y in range(1, 5):
            b.set(x, y, z, WALL if (x, z) in posts else 'air')
    for (x, z) in ring:
        if (x, z) in posts:
            continue
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + dx, z + dz) in posts:
                b.set(x, 4, z, STAIRS, facing=toward(dx, dz), half='top')
                break
    # the floor: brick, with a ring of rough stone round the oven
    for (x, z) in d.hgt:
        b.set(x, 0, z, ES if 1.5 < math.hypot(x - C, z - C) <= 2.6 else ESB)
    # the oven: a 3x3 stone block with smokers front and back and cooking fires either side, a fire
    # under the flue, stone shoulders, and its chimney straight up through the crown
    top = d.hgt[(C, C)]
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            b.fill(C + dx, 1, C + dz, C + dx, top, C + dz, ESB)
            if dx or dz:
                b.set(C + dx, top + 1, C + dz, WALL)
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            if dx and dz:
                b.lantern(C + dx, top + 2, C + dz)
    for x in range(C - 1, C + 2):
        b.set(x, 4, C - 2, STAIRS, facing='south', half='bottom')
        b.set(x, 4, C + 2, STAIRS, facing='north', half='bottom')
    for z in range(C - 1, C + 2):
        b.set(C - 2, 4, z, STAIRS, facing='east', half='bottom')
        b.set(C + 2, 4, z, STAIRS, facing='west', half='bottom')
    b.set(C, 1, C - 1, 'smoker', facing='north', lit=True)
    b.set(C, 1, C + 1, 'smoker', facing='south', lit=True)
    for dx, f in ((-1, 'west'), (1, 'east')):
        b.set(C + dx, 1, C, 'campfire', facing=f, lit=True, signal_fire=False, waterlogged=False)
    for y in range(1, top + 2):
        b.set(C, y, C, 'air')
    b.set(C, 1, C, 'campfire', facing='north', lit=True, signal_fire=False, waterlogged=False)
    b.spot('work', C, 1, C - 2)
    # long low tables of brick slabs, woven cushions either side
    tables = [((2, 4), (2, 8), 'z'), ((10, 4), (10, 8), 'z'), ((4, 10), (8, 10), 'x')]
    for (x0, z0), (x1, z1), axis in tables:
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                b.set(x, 1, z, SLAB, type='bottom')
                if (x + z) % 3 == 0:
                    b.candles(x, 2, z, 2 + (x + z) % 2, color='white' if x % 2 else 'purple')
        sides = ((-1, 0), (1, 0)) if axis == 'z' else ((0, -1), (0, 1))
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for dx, dz in sides:
                    sx, sz = x + dx, z + dz
                    if d.is_room(sx, 1, sz) and not b.solid(sx, 1, sz):
                        color = ('purple', 'white', 'brown')[(sx + sz) % 3]
                        b.set(sx, 1, sz, f'{color}_carpet')
                        if (sx + sz) % 2 == 0:
                            b.spot('sit', sx, 1, sz)
    # stores by the oven and lanterns hung from the dome
    b.barrel(4, 1, 2, facing='up')
    b.barrel(8, 1, 2, facing='up')
    pot(b, 3, 1, 3, 'north')
    pot(b, 9, 1, 3, 'north')
    for x, z in ((3, 6), (9, 6), (6, 3), (6, 9)):
        hanging_lantern(b, x, 5, z, chain=None)
    # chorus on the dome's shoulders
    for x, z, h in ((3, 3, 2), (9, 9, 3), (9, 3, 1), (3, 9, 2), (6, 1, 1), (11, 6, 1), (1, 6, 2), (6, 11, 1)):
        if (x, z) in d.hgt:
            d.plant(x, z, h, branches=h >= 3)
