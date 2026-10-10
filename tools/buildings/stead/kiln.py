"""The Popping Kiln: a beehive kiln of coursed end stone where the kiln-keeper pops chorus fruit, the stuff
all purpur is made of. Its steps run round it like the coils of a skep. Furnaces ring the firing chamber
round a campfire whose smoke goes up the chimney; out front, a work porch under a striped awning of
woven chorus fibre, stacked with barrels of fruit."""
from kit import building
from stead._parts import Dome, arch, hanging_lantern, pot, seat, toward, ES, ESB, SLAB, WALL

FIRES = ('blast_furnace', 'furnace', 'smoker', 'furnace')


def kiln_skin(dome, x, y, z):
    """Coursed stone: alternate courses of end stone and end stone bricks, like the coils of a skep."""
    if y == dome.floor:
        return ESB
    return ES if y % 2 else ESB


@building('popping_kiln', people='chorrin', role='work', size=(11, 15, 12), ground=0, door=5, job='kiln_keeper',
          about='A coiled beehive kiln with a smoking chimney, furnaces round a campfire inside, and a work '
                'porch of chorus-fruit barrels under a striped fibre awning.')
def popping_kiln(b):
    cx, cz = 5, 7
    d = Dome(b, cx, cz, 4.5, 4.5, floor=0, crown=12, wall_top=5, power=0.45, max_rise=3, skin=kiln_skin).build()
    # the chimney: a collar of walls round the crown, the flue open straight down to the hearth
    top = d.hgt[(cx, cz)]
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            if dx or dz:
                b.set(cx + dx, top - 1, cz + dz, ESB)
                b.set(cx + dx, top, cz + dz, WALL)
                b.set(cx + dx, top + 1, cz + dz, WALL if dx and dz else 'air')
    for dx, dz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        b.lantern(cx + dx, top + 2, cz + dz)
    for y in range(top - 3, top + 1):
        b.set(cx, y, cz, 'air')
    b.set(cx, 1, cz, 'campfire', facing='north', lit=True, signal_fire=False, waterlogged=False)
    # the mouth: a round open arch in the north face
    arch(b, cx, 1, 3, facing='north', ring='purpur_stairs')
    b.clear(cx - 1, 1, 3, cx + 1, 2, 3)
    # the firing ring: furnaces, blast furnaces and smokers against the inside wall, facing the hearth
    edge = [(x, z) for (x, z) in d.room(1)
            if any((x + ddx, 1, z + ddz) in d.shell for ddx, ddz in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            and z > 4]
    edge.sort(key=lambda c: (c[1], c[0]))
    for i, (x, z) in enumerate(edge):
        kind = FIRES[i % len(FIRES)]
        if (x, z) in ((cx - 1, 9), (cx + 1, 9)):
            b.barrel(x, 1, z, facing='up')
            continue
        b.set(x, 1, z, kind, facing=toward(cx - x, cz - z), lit=(i % 3 != 1))
        if i % 2 == 0 and d.is_room(x, 2, z):
            b.set(x, 2, z, ESB if i % 4 else 'barrel', **({} if i % 4 else {'facing': 'up', 'open': False}))
    b.spot('work', cx, 1, cz + 2)
    # the porch: brick paving, four posts, a striped awning of wool slabs, barrels of chorus fruit
    b.fill(1, 0, 0, 9, 0, 2, ESB)
    for x, z in ((1, 0), (9, 0), (1, 2), (9, 2)):
        b.fill(x, 1, z, x, 3, z, WALL)
    for x in range(1, 10):
        cloth = 'purple_wool_slab' if x % 2 else 'white_wool_slab'
        for z in range(0, 3):
            b.set(x, 4, z, cloth, type='top')
    hanging_lantern(b, 3, 2, 1, chain=1)
    hanging_lantern(b, 7, 2, 1, chain=1)
    for x, z, f in ((2, 1, 'up'), (2, 2, 'east'), (8, 1, 'up'), (8, 2, 'west')):
        b.barrel(x, 1, z, facing=f)
    b.barrel(2, 2, 2, facing='up')
    b.barrel(8, 2, 2, facing='up')
    b.set(1, 1, 1, SLAB, type='top')
    b.candles(1, 2, 1, 3, color='white')
    pot(b, 9, 1, 1, 'west')
    seat(b, 2, 1, 0, 'west', cushion='brown')
    # behind the kiln: lamps on posts, and the fuel stack
    for x in (1, 9):
        b.set(x, 1, 10, WALL)
        b.lantern(x, 2, 10)
    b.barrel(2, 1, 11, facing='up')
    b.barrel(8, 1, 11, facing='up')
    # a little of the keeper's own crop growing on the kiln's shoulders
    for x, z in ((2, 5), (8, 9), (8, 5)):
        if (x, z) in d.hgt:
            d.plant(x, z, 2, branches=False)
