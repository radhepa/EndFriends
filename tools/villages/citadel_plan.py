"""Plans Citadels: a square fortress of corner towers and wall bays, the Gate of Eyes in the north wall,
the Court's buildings round an inner court, all on one great squarish islet.

Wall rules (see tools/buildings/citadel/walls.py): a side is 22 + 9k blocks (two 11-block corner towers
and k wall bays of 9). The wall's 5-deep profile sits 3..7 blocks in from the outside, in the towers,
the bays and the gate alike. The gate replaces three bays. The NW tower is drawn as is; the others
are it turned one, two and three quarter turns.
"""
import random

import kit
from plan import Islet, Layout, Plot, Program, STYLES

K = 'court'

# Interior arrangements, in square-centred coordinates for k = 7 (interior runs -34..34 each way):
# name, min x, min z, quarter turns (the front faces the court).
ARRANGEMENTS = {
    'a': [('throne_hall', -13, 0, 0), ('lords_spire', 19, 20, 3), ('seers_spire', -29, 20, 1),
          ('riftguard_barracks', 21, -26, 3), ('thrall_yards', 17, -6, 3), ('war_hall', -33, -27, 1),
          ('voidhound_kennels', -31, -4, 1)],
    'b': [('throne_hall', -13, 0, 0), ('lords_spire', -29, 20, 1), ('seers_spire', 19, 20, 3),
          ('war_hall', 19, -27, 3), ('voidhound_kennels', 21, -4, 3), ('riftguard_barracks', -33, -26, 1),
          ('thrall_yards', -33, -6, 1)],
}


def court_square(size=21):
    """The inner court: dark paving round the Court's eye in crying obsidian, obelisks at the corners."""
    b = kit.Build('citadel_court', (size, 8, size))
    c = size // 2
    b.fill(0, 0, 0, size - 1, 0, size - 1, 'polished_blackstone_bricks')
    for i in range(size):
        for x, z in ((i, 0), (i, size - 1), (0, i), (size - 1, i)):
            b.set(x, 0, z, 'obsidian')
    # the eye: an almond of crying obsidian with an end-stone iris and an obsidian pupil
    for z in range(size):
        for x in range(size):
            dx, dz = abs(x - c), abs(z - c)
            if dx <= 7 and dz <= 3 - dx // 3 and dz >= 2 - dx // 3:
                b.set(x, 0, z, 'crying_obsidian')
            if dx * dx + dz * dz <= 4:
                b.set(x, 0, z, 'end_stone_bricks')
    b.set(c, 0, c, 'obsidian')
    for x, z in ((2, 2), (size - 3, 2), (2, size - 3), (size - 3, size - 3)):
        b.fill(x, 1, z, x, 4, z, 'obsidian')
        b.set(x, 5, z, 'crying_obsidian')
        b.end_rod(x, 6, z, 'up')
        for dx, dz, f in ((1, 0, 'east'), (-1, 0, 'west'), (0, 1, 'south'), (0, -1, 'north')):
            b.set(x + dx, 1, z + dz, 'polished_blackstone_brick_stairs', facing={'east': 'west', 'west': 'east', 'south': 'north', 'north': 'south'}[f])
    return b.finish()


def plan(name, seed, k=7, arrangement='a'):
    program = Program('citadel', 'citadel_court', K, [], gap=(0, 0), tiers=(0,), merge=False, margin=0)
    lay = Layout(name, program, seed)
    side = 22 + 9 * k
    x0 = z0 = -(side // 2)
    shift = (k - 7) * 9 // 2       # arrangements are drawn for k = 7

    # the inner court is the plaza (plots[0]): paths end there
    court = court_square()
    spec = dict(name='citadel_court', people=K, role='plaza', size=(court.w, court.h, court.d), ground=0, residents=0, door=court.w // 2)
    lay.plots.append(Plot('citadel_court', K, court, -(court.w // 2), -27 - shift, 0, 0, spec))

    def add(name_, x, z, turns):
        b = kit.make(name_).turned(turns)
        lay.plots.append(Plot(name_, K, b, x, z, 0, turns, kit.CATALOG[name_]))
        return lay.plots[-1]

    add('citadel_tower', x0, z0, 0)
    add('citadel_tower', x0 + side - 11, z0, 1)
    add('citadel_tower', x0 + side - 11, z0 + side - 11, 2)
    add('citadel_tower', x0, z0 + side - 11, 3)
    g = (k - 3) // 2
    for i in range(k):
        if not g <= i < g + 3:
            add('citadel_wall', x0 + 11 + 9 * i, z0 + 3, 0)
        add('citadel_wall', x0 + 11 + 9 * i, z0 + side - 8, 2)
        add('citadel_wall', x0 + 3, z0 + 11 + 9 * i, 3)
        add('citadel_wall', x0 + side - 8, z0 + 11 + 9 * i, 1)
    gate = add('gate_of_eyes', x0 + 11 + 9 * g, z0, 0)
    for name_, x, z, turns in ARRANGEMENTS[arrangement]:
        if name_ in kit.CATALOG:
            add(name_, x - (shift if x < 0 else -shift), z - (shift if z < 0 else -shift), turns)

    # one great islet, nearly square, with a deep underside
    half = side / 2 + 4
    lay.islets.append(Islet(0, 0, half, half, 0, 46, power=5))
    lay.raster()

    # paths: from each building to the court, and from inside the gate to the court
    lay.lay_paths()
    inner = (gate.x + 13, gate.z + gate.d)
    blocked = lay.blocked(1)
    for c in list(lay.path_y):
        blocked.discard(c)
    path = lay.route(inner, lay.plots[0].rect(-1), blocked)
    if path:
        lay.paths.append((gate, path))
        lay.set_heights(gate, path)
    # the causeway: out of the gate and over the islet's edge
    outer = (gate.x + 13, gate.z - 1)
    causeway = [(outer[0], outer[1] - i) for i in range(0, 14)]
    for c in causeway:
        lay.path_y[c] = 0
        lay.path_people[c] = K
    lay.paths.append((gate, causeway))

    lay.draw()
    # the ground inside the walls is paved; outside it stays end stone
    ox, oz = -lay.minx, -lay.minz
    rng = random.Random(seed)
    for (x, z), (top, depth) in lay.ground.items():
        if x0 + 8 <= x <= x0 + side - 9 and z0 + 8 <= z <= z0 + side - 9:
            cell = lay.canvas.get(x + ox, top + 24, z + oz)
            if cell[0] == 'minecraft:end_stone':
                lay.canvas.set(x + ox, top + 24, z + oz, 'polished_blackstone' if rng.random() < 0.85 else 'blackstone')
    return lay.finish()
