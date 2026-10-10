"""The Crossing Hall: a wayhouse where Shulkin and Chorrin meet.

The two halves of the house face the market side by side: on the west a lidded Shulkin tower (purpur
drum, glowing magenta gap, overhanging lid), on the east a half-sunk Chorrin dome with chorus on its
crown. Between them, at the back of a little forecourt, a double door: a crimson leaf for the Shulkin
and a pale oak leaf for the Chorrin, each people's banner hanging over its own leaf. Inside is a short
crossing passage: west into the tower (the Shulkin keeper's ledger desk and lidded sleeping niche),
east down a step into the dome (the Chorrin keeper's larder and fibre nest), and straight on into the
common room across the back of the house: two long tables where purpur and end-stone seats take turns,
the keepers' counter, a records desk, and the shared hearth, its chimney half purpur, half end stone.

Two residents, one of each people (``resident_people``); sleep spots are marked Shulkin first.
"""
import math

from kit import building
from shared._parts import grow, banner, toward, EYE_OF_THE_SPIRES, GROVE_KNOT

W, H, D = 21, 18, 19
G = 1                     # ground layer (the dome floor sinks one step below it)
F = G + 1                 # the layer residents stand in
TX, TZ = 5, 5             # tower centre (drum radius 4, lid radius 5)
DX, DZ, DR = 15.5, 5.5, 4.6   # dome centre and radius
DOOR = 10                 # crimson leaf; the pale oak leaf is DOOR + 1
DOOR_Z = 4
ROOM = (0, 9, 20, 17)     # common room x0, z0, x1, z1 (walls on the edges)
WALL_TOP = 5
SEAM = DOOR + 1           # first x of the end-stone half


# ------------------------------------------------------------------ shapes
def octagon_cells(cx, cz, r):
    k = math.floor(r * 1.45)
    return {(x, z) for z in range(cz - r, cz + r + 1) for x in range(cx - r, cx + r + 1)
            if abs(x - cx) + abs(z - cz) <= k}


def octagon_edge(cx, cz, r):
    k = math.floor(r * 1.45)
    return {(x, z) for (x, z) in octagon_cells(cx, cz, r)
            if abs(x - cx) == r or abs(z - cz) == r or abs(x - cx) + abs(z - cz) == k}


def octagon_corners(cx, cz, r):
    a = math.floor(r * 1.45) - r
    return {(cx + sx * r, cz + sz * a) for sx in (-1, 1) for sz in (-1, 1)} | \
           {(cx + sx * a, cz + sz * r) for sx in (-1, 1) for sz in (-1, 1)}


def disc_cells(cx, cz, r, clip=True):
    return {(x, z) for z in range(math.floor(cz - r) - 1, math.ceil(cz + r) + 2)
            for x in range(math.floor(cx - r) - 1, math.ceil(cx + r) + 2)
            if (x - cx) ** 2 + (z - cz) ** 2 <= r * r + 0.3 and (not clip or z < ROOM[1])}


TOWER = octagon_cells(TX, TZ, 4)
DOME = disc_cells(DX, DZ, DR)          # clipped at the common room's front wall


def dome_layers(y0=G, ry=5.0):
    """Radius of the dome's shell at each layer from the islet surface up (a hemisphere cap)."""
    out, y = {}, y0
    while True:
        f = 1 - ((y - y0) / ry) ** 2
        if f <= 0 or DR * math.sqrt(f) < 0.9:
            return out
        out[y] = DR * math.sqrt(f)
        y += 1


# ------------------------------------------------------------------ the tower (west)
def tower(b):
    cx, cz = TX, TZ
    edge = octagon_edge(cx, cz, 4)
    inner = octagon_cells(cx, cz, 3)
    corners = octagon_corners(cx, cz, 4)
    for (x, z) in octagon_cells(cx, cz, 5) - TOWER:
        if z < ROOM[1] and x < DOOR - 1 and b.inside(x, G, z):
            b.set(x, G, z, 'end_stone_bricks')
    # close the sliver between the tower's flank and the passage wall
    for y in range(F, WALL_TOP + 1):
        b.set(cx + 3, y, cz + 3, 'purpur_block')
    # a lamp on the plinth at the tower's outer corner
    b.set(cx - 3, F, cz - 3, 'purpur_pillar', axis='y')
    b.end_rod(cx - 3, F + 1, cz - 3, 'up')
    for (x, z) in TOWER:
        if (x + z) % 2:
            b.set(x, G, z, 'purpur_block')
        else:
            b.set(x, G, z, 'purpur_pillar', axis='y')
    # the drum: purpur walls with pillars at the octagon's corners
    for y in range(F, 12):
        for (x, z) in edge:
            if (x, z) in corners:
                b.set(x, y, z, 'purpur_pillar', axis='y')
            else:
                b.set(x, y, z, 'purpur_block')
        for (x, z) in inner:
            b.set(x, y, z, 'air')
    for (x, z) in inner:
        b.set(x, 7, z, 'purpur_slab', type='top')
    # windows: tall magenta lancets on the outer faces
    for (x, z) in ((cx - 4, cz), (cx, cz - 4)):
        for y in (F + 1, F + 2, 8, 9):
            b.set(x, y, z, 'magenta_stained_glass_pane')
        b.set(x, F, z, 'purpur_stairs', facing=toward(cx - x, cz - z), half='top')
    for y in (8, 9):
        b.set(cx, y, cz + 4, 'magenta_stained_glass_pane')
    # the gap: a recessed ring of magenta glass, end rods and a froglight glowing behind it
    for (x, z) in inner:
        b.set(x, 11, z, 'purpur_block')
    for y in (12, 13):
        for (x, z) in edge:
            b.set(x, y, z, 'air')
        for (x, z) in octagon_edge(cx, cz, 3):
            b.set(x, y, z, 'magenta_stained_glass')
    for dx, dz in ((-2, 0), (2, 0), (0, -2), (0, 2)):
        b.end_rod(cx + dx, 12, cz + dz, 'up')
    b.set(cx, 12, cz, 'pearlescent_froglight', axis='y')
    # the lid: overhangs the drum, steps in to a crest with an end rod
    for (x, z) in octagon_cells(cx, cz, 5):
        if b.inside(x, 14, z):
            b.set(x, 14, z, 'purpur_slab', type='top')
    for (x, z) in octagon_cells(cx, cz, 4):
        b.set(x, 14, z, 'purpur_block')
        b.set(x, 15, z, 'purpur_block')
    for (x, z) in octagon_edge(cx, cz, 5):
        if b.inside(x, 15, z):
            b.set(x, 15, z, 'purpur_stairs', facing=toward(cx - x, cz - z), half='bottom')
    for (x, z) in octagon_cells(cx, cz, 3):
        b.set(x, 16, z, 'purpur_slab', type='bottom')
    for (x, z) in octagon_cells(cx, cz, 2):
        b.set(x, 16, z, 'purpur_block')
    b.end_rod(cx, 17, cz, 'up')
    for x, z, f in ((cx, cz + 5, 'north'), (cx - 5, cz, 'east'), (cx + 5, cz, 'west'), (cx, cz - 5, 'south')):
        if b.inside(x, 13, z):
            b.set(x, 13, z, 'purpur_stairs', facing=f, half='top')
    tower_rooms(b, cx, cz)


def tower_rooms(b, cx, cz):
    # the arch from the passage, three high
    for y in range(F, F + 3):
        b.set(cx + 4, y, cz, 'air')
    b.set(cx + 4, G, cz, 'purpur_block')
    # the ledger desk facing the arch: the keeper behind it, a lectern and candles on it
    for z in (cz - 2, cz - 1):
        b.set(cx + 1, F, z, 'purpur_stairs', facing='west', half='top')
    b.set(cx + 1, F + 1, cz - 2, 'lectern', facing='east', has_book=False, powered=False)
    b.candles(cx + 1, F + 1, cz - 1, 3, color='magenta')
    b.spot('work', cx, F, cz - 1)
    b.set(cx - 1, F, cz - 3, 'chiseled_bookshelf', facing='south')
    b.set(cx - 1, F + 1, cz - 3, 'bookshelf')
    b.set(cx + 1, F, cz - 3, 'crimson_shelf', facing='south')
    # the lidded sleeping niche on the west wall: carpet under a purpur lid, a glowing gap behind
    for z in range(cz - 1, cz + 2):
        b.set(cx - 3, F, z, 'purple_carpet')
        b.set(cx - 3, F + 3, z, 'purpur_slab', type='top')
        b.set(cx - 2, F + 3, z, 'purpur_stairs', facing='west', half='top')
    b.set(cx - 2, F, cz - 2, 'purpur_stairs', facing='south', half='bottom')
    b.set(cx - 2, F, cz + 2, 'purpur_stairs', facing='north', half='bottom')
    b.set(cx - 4, F + 1, cz, 'magenta_stained_glass')
    b.set(cx - 4, F + 2, cz, 'purpur_block')
    b.spot('sleep', cx - 3, F, cz)
    # records on the south side, storage, the ladder to the lamp room (visitors only: residents
    # keep to the ground floor, mobs do not climb ladders)
    b.set(cx - 1, F, cz + 3, 'bookshelf')
    b.set(cx - 1, F + 1, cz + 3, 'bookshelf')
    b.set(cx, F, cz + 3, 'barrel', facing='north', open=False)
    b.set(cx + 2, F, cz + 2, 'barrel', facing='west', open=False)
    for y in range(F, 8):
        b.set(cx + 1, y, cz + 3, 'ladder', facing='north', waterlogged=False)
    b.end_rod(cx, 6, cz, 'down')
    # the lamp room upstairs: the hall's guest book
    b.set(cx - 2, 8, cz - 2, 'lectern', facing='south', has_book=False, powered=False)
    b.set(cx + 2, 8, cz - 2, 'bookshelf')
    b.set(cx + 2, 9, cz - 2, 'bookshelf')
    b.set(cx - 3, 8, cz, 'magenta_carpet')
    b.set(cx - 3, 8, cz + 1, 'purpur_stairs', facing='west', half='bottom')
    b.lantern(cx, 10, cz, hanging=True)


# ------------------------------------------------------------------ the dome (east)
def dome(b):
    """A half-sunk Chorrin dome: its floor one step below the islet, a hemisphere of brick with stair
    ledges, a bare end-stone crown where chorus grows, pearlescent froglights set into the shell."""
    layers = dome_layers()
    ys = sorted(layers)
    cells = {y: disc_cells(DX, DZ, layers[y]) for y in ys}
    floor_y = G - 1
    for (x, z) in DOME:
        b.set(x, floor_y, z, 'end_stone_bricks' if (x + z) % 3 else 'end_stone')
    for y in ys:
        for (x, z) in cells[y]:
            crown = y == ys[-1]
            b.set(x, y, z, 'end_stone' if crown else 'end_stone_bricks')
    for y in ys[:-1]:
        for (x, z) in cells[y] - cells[y + 1]:
            b.set(x, y + 1, z, 'end_stone_brick_stairs', facing=toward(DX - x, DZ - z), half='bottom')
    # carve the room one ring in from the shell (the crown stays as the ceiling)
    for y in ys[:-1]:
        for (x, z) in disc_cells(DX, DZ, layers[y] - 1.1):
            b.set(x, y, z, 'air')
    # a low curb round the dome's foot
    for (x, z) in disc_cells(DX, DZ, DR + 0.9) - disc_cells(DX, DZ, DR + 0.2, clip=False):
        if b.inside(x, F, z) and z < ROOM[1] and x > DOOR + 2:
            b.set(x, F, z, 'end_stone_brick_slab', type='bottom')
    # pearlescent eyes in the shell, shining in and out
    for ang in (-150, -90, -30, 20):
        a = math.radians(ang)
        for k in range(16):
            r = DR - k * 0.25
            x, z = math.floor(DX + math.cos(a) * r + 0.5), math.floor(DZ + math.sin(a) * r + 0.5)
            if b.get(x, F + 1, z)[0] == 'minecraft:end_stone_bricks' and b.get(x, F, z)[0] != 'minecraft:air':
                b.set(x, F + 1, z, 'pearlescent_froglight', axis='y')
                break
    # chorus on the crown and one on the shoulder
    cy = ys[-1] + 1
    grow(b, 15, cy, 5, 3, [('east', 2, ()), ('north', 1, ())])
    grow(b, 16, cy, 6, 1)
    sx, sz = 18, 3
    sy = max(y for y in ys if (sx, sz) in cells[y])
    b.set(sx, sy, sz, 'end_stone')
    b.set(sx, sy + 1, sz, 'air')
    grow(b, sx, sy + 1, sz, 2)
    # the arch from the passage: two wide, a step down
    for z in (6, 7):
        for y in range(G, F + 3):
            b.set(DOOR + 2, y, z, 'air')
            b.set(DOOR + 3, y, z, 'air')
        b.set(DOOR + 2, G, z, 'end_stone_bricks')
        b.set(DOOR + 2, G - 1, z, 'end_stone_bricks')
        b.set(DOOR + 3, G, z, 'end_stone_brick_stairs', facing='west', half='bottom')
    dome_rooms(b, floor_y + 1)


def dome_rooms(b, y):
    # the Chorrin keeper's nest: a rim of woven fibre (wool stairs) round a carpet bed
    for x, z, c in ((17, 6, 'brown'), (18, 6, 'white'), (17, 7, 'brown'), (18, 7, 'brown')):
        b.set(x, y, z, f'{c}_carpet')
    for x, z, f in ((16, 7, 'west'), (16, 8, 'west'), (17, 8, 'south'), (18, 8, 'south'), (19, 7, 'east'),
                    (19, 6, 'east'), (18, 5, 'north'), (17, 5, 'north')):
        if b.get(x, y, z)[0] == 'minecraft:air':
            b.set(x, y, z, 'brown_wool_stairs', facing=f, half='bottom')
    b.spot('sleep', 18, y, 7)
    # the larder: barrels, pots, a cauldron, popped chorus put by for the Shulkin
    b.set(14, y, 3, 'barrel', facing='up', open=False)
    b.set(14, y + 1, 3, 'decorated_pot', facing='south')
    b.set(15, y, 3, 'barrel', facing='south', open=False)
    b.set(16, y, 3, 'purpur_block')
    b.set(17, y, 3, 'decorated_pot', facing='south')
    b.set(13, y, 4, 'cauldron')
    b.spot('work', 15, y, 4)
    b.set(14, y, 8, 'end_stone_brick_slab', type='bottom')
    b.spot('sit', 14, y, 8)
    b.lantern(15, 4, 5, hanging=True)


# ------------------------------------------------------------------ forecourt, door and passage
def entrance(b):
    for z in range(0, DOOR_Z):
        for x in range(DOOR - 2, DOOR + 4):
            if (x, z) not in TOWER and (x, z) not in DOME:
                b.set(x, G, z, 'purpur_block' if x < SEAM else 'end_stone_bricks')
    # the doorway: a purpur jamb against the tower, the dome's flank on the other side
    for y in range(F, F + 4):
        b.set(DOOR - 1, y, DOOR_Z, 'purpur_pillar', axis='y')
    b.door(DOOR, F, DOOR_Z, facing='north', kind='crimson', hinge='left')
    b.door(DOOR + 1, F, DOOR_Z, facing='north', kind='pale_oak', hinge='right')
    b.set(DOOR, F + 2, DOOR_Z, 'air')
    b.set(DOOR + 1, F + 2, DOOR_Z, 'air')
    b.set(DOOR, F + 3, DOOR_Z, 'purpur_stairs', facing='south', half='top')
    b.set(DOOR + 1, F + 3, DOOR_Z, 'end_stone_brick_stairs', facing='south', half='top')
    b.set(DOOR + 2, F + 2, DOOR_Z, 'end_stone_bricks')
    b.set(DOOR + 2, F + 3, DOOR_Z, 'end_stone_bricks')
    for x in range(DOOR - 1, DOOR + 3):
        b.set(x, F + 4, DOOR_Z, 'purpur_block' if x < SEAM else 'end_stone_bricks')
    b.set(DOOR, F + 5, DOOR_Z, 'purpur_slab', type='bottom')
    b.set(DOOR + 1, F + 5, DOOR_Z, 'end_stone_brick_slab', type='bottom')
    # each people's banner over its own leaf
    banner(b, DOOR, F + 3, DOOR_Z - 1, base='purple', patterns=EYE_OF_THE_SPIRES, facing='north', wall=True)
    banner(b, DOOR + 1, F + 3, DOOR_Z - 1, base='white', patterns=GROVE_KNOT, facing='north', wall=True)
    # door lamps: an end-rod post on the shell side, a froglight on the grove side
    b.set(DOOR - 1, G, DOOR_Z - 1, 'end_stone_bricks')
    b.set(DOOR - 1, F, DOOR_Z - 1, 'purpur_block')
    b.set(DOOR - 1, F + 1, DOOR_Z - 1, 'purpur_pillar', axis='y')
    b.end_rod(DOOR - 1, F + 2, DOOR_Z - 1, 'up')
    b.set(DOOR + 2, F, DOOR_Z - 1, 'end_stone_bricks')
    b.set(DOOR + 2, F + 1, DOOR_Z - 1, 'pearlescent_froglight', axis='y')
    b.candles(DOOR + 2, F + 2, DOOR_Z - 1, 2, color='white')
    # the passage to the common room: purpur floor west, brick east, a little gabled roof
    for z in range(DOOR_Z + 1, ROOM[1] + 1):
        b.set(DOOR, G, z, 'purpur_pillar', axis='z')
        b.set(DOOR + 1, G, z, 'end_stone_bricks')
        for y in range(F, F + 4):
            b.set(DOOR, y, z, 'air')
            b.set(DOOR + 1, y, z, 'air')
        for x, mat, face in ((DOOR - 1, 'purpur', 'east'), (DOOR + 2, 'end_stone_brick', 'west')):
            if (x, z) in TOWER or (x, z) in DOME:
                continue
            for y in range(F, F + 4):
                b.set(x, y, z, 'purpur_block' if mat == 'purpur' else 'end_stone_bricks')
            b.set(x, F + 4, z, f'{mat}_stairs', facing=face, half='bottom')
        b.set(DOOR, F + 4, z, 'purpur_slab', type='top')
        b.set(DOOR + 1, F + 4, z, 'end_stone_brick_slab', type='top')
        b.set(DOOR, F + 5, z, 'purpur_slab', type='bottom')
        b.set(DOOR + 1, F + 5, z, 'end_stone_brick_slab', type='bottom')
    b.end_rod(DOOR, F + 3, DOOR_Z + 2, 'down')
    b.end_rod(DOOR + 1, F + 3, DOOR_Z + 4, 'down')


# ------------------------------------------------------------------ the common room (back)
def roof_h2(z):
    """Roof surface height in half blocks: a low gable, ridge over the room's middle."""
    return 2 * (WALL_TOP + 1) + min(z - (ROOM[1] - 1), (ROOM[3] + 1) - z)


def roof_cell(z):
    """(layer, slab type) of the roof skin over row z."""
    h2 = roof_h2(z)
    return (h2 // 2, 'bottom') if h2 % 2 else (h2 // 2 - 1, 'top')


def common_room(b):
    x0, z0, x1, z1 = ROOM
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if (x, z) in TOWER:
                continue
            west = x < SEAM
            if x in (DOOR, DOOR + 1):
                spec = ('purpur_pillar', {'axis': 'z'}) if west else ('end_stone_bricks', {})
            elif west:
                spec = ('purpur_block', {}) if (x + z) % 2 else ('purpur_pillar', {'axis': 'y'})
            else:
                spec = ('end_stone_bricks', {}) if (x * 3 + z) % 4 else ('end_stone', {})
            b.set(x, G, z, spec[0], **spec[1])
            edge = x in (x0, x1) or z in (z0, z1)
            for y in range(F, WALL_TOP + 1):
                if edge:
                    corner = x in (x0, x1) and z in (z0, z1)
                    if west:
                        b.set(x, y, z, 'purpur_pillar' if corner else 'purpur_block', **({'axis': 'y'} if corner else {}))
                    else:
                        b.set(x, y, z, 'end_stone_bricks')
                else:
                    b.set(x, y, z, 'air')
    # the roof: a low gable of slabs, purpur over the west half, end-stone brick over the east
    for x in range(x0 - 1, x1 + 2):
        west = x < SEAM
        slab = 'purpur_slab' if west else 'end_stone_brick_slab'
        block = 'purpur_block' if west else 'end_stone_bricks'
        for z in range(z0 - 1, z1 + 2):
            if not b.inside(x, 0, z) or (x, z) in TOWER or (x, z) in DOME:
                continue
            y, kind = roof_cell(z)
            b.set(x, y, z, slab, type=kind)
            if x in (x0, x1) or z in (z0, z1):
                for yy in range(WALL_TOP + 1, y + (1 if kind == 'top' else 0)):
                    b.set(x, yy, z, block)
    # the ridge carries lights (mobs could otherwise spawn on the dark top-slab rows of the roof):
    # end rods on the purpur half, froglight knobs on the brick half
    ry, _ = roof_cell((z0 + z1) // 2)
    for x in (2, 6):
        b.end_rod(x, ry + 1, (z0 + z1) // 2, 'up')
    for x in (15, 19):
        b.set(x, ry + 1, (z0 + z1) // 2, 'pearlescent_froglight', axis='y')
    # windows: magenta lancets in the purpur half, white glass in the brick half
    for x in (3, 7):
        for y in (F + 1, F + 2):
            b.set(x, y, z1, 'magenta_stained_glass_pane')
    for x in (14, 18):
        for y in (F + 1, F + 2):
            b.set(x, y, z1, 'white_stained_glass_pane')
    for z in (12, 14):
        for y in (F + 1, F + 2):
            b.set(x0, y, z, 'magenta_stained_glass_pane')
            b.set(x1, y, z, 'white_stained_glass_pane')
    room_things(b)


def room_things(b):
    # two long tables: purpur and end-stone tops and seats taking turns all the way down
    for xs in (range(2, 8), range(13, 19)):
        for x in xs:
            b.set(x, F, 12, 'purpur_slab' if x % 2 else 'end_stone_brick_slab', type='top')
            for z, face in ((11, 'north'), (13, 'south')):
                b.set(x, F, z, 'purpur_stairs' if (x + z) % 2 else 'end_stone_brick_stairs', facing=face, half='bottom')
                b.spot('sit', x, F, z)
        b.candles(xs[1], F + 1, 12, 3, color='purple')
        b.set(xs[3], F + 1, 12, 'decorated_pot', facing='north')
        b.candles(xs[5], F + 1, 12, 2, color='white')
    # lights over the tables: end rods west, lanterns on chains east
    for x in (3, 6):
        b.end_rod(x, 6, 12, 'down')
    for x in (14, 17):
        b.set(x, 6, 12, 'iron_chain', axis='y')
        b.lantern(x, 5, 12, hanging=True)
    # the shared hearth on the back wall, half purpur and half brick
    hx = DOOR
    for y in range(F, F + 3):
        b.set(hx - 1, y, 16, 'purpur_block')
        b.set(hx + 2, y, 16, 'end_stone_bricks')
    for x in (hx, hx + 1):
        b.set(x, F, 16, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
        b.set(x, G, 16, 'purpur_block' if x < SEAM else 'end_stone_bricks')
    for x in range(hx - 1, hx + 3):
        b.set(x, F + 3, 16, 'purpur_stairs' if x < SEAM else 'end_stone_brick_stairs', facing='south', half='top')
    top = 10
    for z in (17, 18):
        for x in (hx, hx + 1):
            mat = 'purpur_block' if x < SEAM else 'end_stone_bricks'
            for y in range(G if z == 18 else F + 3, top):
                b.set(x, y, z, 'purpur_pillar' if x < SEAM and y % 3 == 0 else mat,
                      **({'axis': 'y'} if x < SEAM and y % 3 == 0 else {}))
            b.set(x, top, z, 'purpur_slab' if x < SEAM else 'end_stone_brick_slab', type='bottom')
    # a corbelled lip near the top of the chimney
    for x, z, f in ((hx - 1, 17, 'east'), (hx - 1, 18, 'east'), (hx + 2, 17, 'west'), (hx + 2, 18, 'west')):
        b.set(x, top - 1, z, 'purpur_stairs' if x < SEAM else 'end_stone_brick_stairs', facing=f, half='top')
    b.spot('work', hx, F, 15)
    # the keepers' counter in the east corner: brews and bread
    for x in range(15, 19):
        b.set(x, F, 15, 'end_stone_brick_stairs', facing='south', half='top')
    b.set(19, F, 15, 'end_stone_bricks')
    b.set(16, F + 1, 15, 'brewing_stand', has_bottle_0=True, has_bottle_1=True, has_bottle_2=False)
    b.candles(18, F + 1, 15, 3, color='white')
    b.set(19, F + 1, 15, 'pearlescent_froglight', axis='y')
    b.set(19, F, 16, 'barrel', facing='west', open=False)
    b.set(19, F + 1, 16, 'barrel', facing='up', open=False)
    b.set(15, F, 16, 'smoker', facing='east', lit=False)
    b.spot('work', 17, F, 16)
    # the records desk in the west corner
    b.set(2, F, 16, 'lectern', facing='north', has_book=False, powered=False)
    b.set(1, F, 16, 'chiseled_bookshelf', facing='east')
    b.set(1, F, 15, 'bookshelf')
    b.set(1, F + 1, 16, 'bookshelf')
    b.end_rod(1, F + 1, 15, 'up')
    b.set(4, F, 16, 'purpur_stairs', facing='south', half='bottom')
    b.spot('sit', 4, F, 16)
    b.spot('stand', 2, F, 15)


@building('crossing_hall', people='shared', role='civic', size=(W, H, D), ground=G, residents=2, door=DOOR,
          job='keeper', resident_people=('shulkin', 'chorrin'),
          about='The wayhouse where both peoples meet: a lidded Shulkin tower and a half-sunk Chorrin dome side by '
                'side, a double door between them, and a common room with long tables, a counter and a shared hearth.')
def crossing_hall(b):
    common_room(b)
    tower(b)
    dome(b)
    entrance(b)
