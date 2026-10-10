"""Shared parts for the Citadel of the Endarch Court (no buildings are registered here).

Palette: obsidian and polished blackstone bricks (+ stairs, slabs, walls), crying obsidian,
purpur pillars, magenta glass, iron chains, and end portal frames with eyes as the Court's
watching "eyes". Light: end rods and crying obsidian. Everything is Endarch-scale (3.4-3.8 blocks
tall): arches at least 4 high, rooms at least 5 high.

The wall line (see ``walls.py``): a wall segment is 9 wide (x) and 5 deep (z), outside face north.
Towers and the gate carry the same 5-deep profile at local z = 3..7 (``JOIN``), so every piece in
the wall line shares one z origin. The wall-walk floor is at y = ``WALK_FLOOR`` (stand at y + 1).

Development helpers in this folder (not used by the planner): ``_checks.py`` (block-light, Endarch-
height pathfinding, portal/forbidden-block/spot checks) and ``_view.py`` (previews on a light
background, straight-on views, joint close-ups, a closed square wall).
"""
import math
import random

# ------------------------------------------------------------------ palette
BRICK = 'polished_blackstone_bricks'
CRACKED = 'cracked_polished_blackstone_bricks'
CHISELED = 'chiseled_polished_blackstone'
POLISHED = 'polished_blackstone'
OBS = 'obsidian'
CRY = 'crying_obsidian'
STAIR = 'polished_blackstone_brick_stairs'
SLAB = 'polished_blackstone_brick_slab'
WALL = 'polished_blackstone_brick_wall'
PSTAIR = 'polished_blackstone_stairs'
PSLAB = 'polished_blackstone_slab'
PILLAR = 'purpur_pillar'
GLASS = 'magenta_stained_glass'
PANE = 'magenta_stained_glass_pane'
CHAIN = 'iron_chain'
EYE = 'end_portal_frame'

# the wall line (shared by walls.py, the corner tower and the gate)
SEG_W, SEG_D = 9, 5          # one wall segment: 9 wide, 5 deep
JOIN = (3, 7)                # towers and the gate carry the wall's profile at local z (or x) 3..7
WALK_FLOOR = 10              # wall-walk floor layer; you stand at y = 11
WALL_H = 15                  # wall segment height (y 0..14)

INWARD = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}


def _h(x, y, z, salt=0):
    """Deterministic 0..1 noise per cell (stable between runs, unlike hash())."""
    n = (x * 73856093) ^ (y * 19349663) ^ (z * 83492791) ^ (salt * 2654435761)
    n = (n ^ (n >> 13)) * 1274126177
    return ((n ^ (n >> 16)) & 0xffffff) / 0xffffff


def stone(x, y, z, cracked=0.12):
    """Blackstone brick with a few cracked bricks, so big faces don't read as flat."""
    return CRACKED if _h(x, y, z) < cracked else BRICK


def put_stone(b, x, y, z, cracked=0.12):
    b.set(x, y, z, stone(x, y, z, cracked))


def fill_stone(b, x0, y0, z0, x1, y1, z1, cracked=0.12, only_air=False):
    for y in range(min(y0, y1), max(y0, y1) + 1):
        for z in range(min(z0, z1), max(z0, z1) + 1):
            for x in range(min(x0, x1), max(x0, x1) + 1):
                if only_air and b.solid(x, y, z):
                    continue
                b.set(x, y, z, stone(x, y, z, cracked))


def box_stone(b, x0, y0, z0, x1, y1, z1, cracked=0.12):
    """Hollow box walls (no floor/ceiling) of textured brick."""
    for y in range(y0, y1 + 1):
        for z in range(z0, z1 + 1):
            for x in range(x0, x1 + 1):
                if x in (x0, x1) or z in (z0, z1):
                    b.set(x, y, z, stone(x, y, z, cracked))


def stair(b, x, y, z, facing, half='bottom', kind=STAIR):
    b.set(x, y, z, kind, facing=facing, half=half)


def slab(b, x, y, z, top=False, kind=SLAB):
    b.set(x, y, z, kind, type='top' if top else 'bottom')


def eye(b, x, y, z, facing='north'):
    """One of the Court's watching eyes: an end portal frame holding an eye of ender.

    Never set twelve of these in a flat 5x5 ring facing inward (that is a working portal)."""
    b.set(x, y, z, EYE, facing=facing, eye=True)


def chain(b, x, y0, y1, z, axis='y'):
    for y in range(min(y0, y1), max(y0, y1) + 1):
        b.set(x, y, z, CHAIN, axis=axis, waterlogged=False)


def rod(b, x, y, z, facing='up'):
    b.set(x, y, z, 'end_rod', facing=facing)


def pillar(b, x, y0, y1, z, kind=PILLAR):
    for y in range(y0, y1 + 1):
        b.set(x, y, z, kind, axis='y')


# ------------------------------------------------------------------ banners
EYE_PATTERN = [{'color': 'magenta', 'pattern': 'minecraft:rhombus'},
               {'color': 'black', 'pattern': 'minecraft:circle'},
               {'color': 'purple', 'pattern': 'minecraft:border'}]
MARSHAL_PATTERN = [{'color': 'purple', 'pattern': 'minecraft:stripe_center'},
                   {'color': 'magenta', 'pattern': 'minecraft:rhombus'},
                   {'color': 'black', 'pattern': 'minecraft:circle'},
                   {'color': 'magenta', 'pattern': 'minecraft:triangle_bottom'}]
PLAIN_PATTERN = [{'color': 'black', 'pattern': 'minecraft:border'}]


def banner(b, x, y, z, facing, color='black', patterns=None):
    """A wall banner hanging on the block behind it; ``facing`` is the side the cloth faces.

    The default is the Court's eye: a magenta lozenge with a black pupil on black, purple border."""
    pats = EYE_PATTERN if patterns is None else patterns
    nbt = {'id': 'minecraft:banner', 'patterns': [dict(p) for p in pats]}
    b.set(x, y, z, f'{color}_wall_banner', nbt=nbt, facing=facing)


# ------------------------------------------------------------------ pointed arches
def arch_tops(width, height, rise=None):
    """Open height of each column of a pointed (gothic) arch ``width`` wide and ``height`` tall.

    The sides run straight up to the springing, then two arcs meet in a point. ``rise`` is how
    much of the height belongs to the pointed head (default: about half the width)."""
    rise = max(1, (width + 1) // 2) if rise is None else rise
    spring = height - rise
    out = []
    s = float(width)
    peak = math.sqrt(s * s - (s / 2) ** 2)
    for i in range(width):
        u = i + 0.5
        u = min(u, s - u)
        f = math.sqrt(max(0.0, s * s - (s - u) ** 2)) / peak
        out.append(spring + max(1, int(round(rise * f ** 1.6))))
    out[width // 2] = height
    if width % 2 == 0:
        out[width // 2 - 1] = height
    return out


def arch(b, plane, a0, width, y0, height, d0, d1, rise=None, smooth=None, trim=None, trim_d=None):
    """Cut a pointed arch opening.

    ``plane`` 'x': the opening spans x = a0..a0+width-1 and goes through z = d0..d1 (a door in a
    north/south face). ``plane`` 'z': spans z, goes through x = d0..d1. Cells are erased (so the
    world's air shows), from layer y0 up. ``smooth``: a stair block id; upside-down stairs are set
    where the arch steps, so the curve reads smoothly. ``trim``: block for the arch ring (the
    voussoirs) on depth layer ``trim_d`` (default d0)."""
    tops = arch_tops(width, height, rise)
    lo, hi = min(d0, d1), max(d0, d1)
    for i, t in enumerate(tops):
        a = a0 + i
        for d in range(lo, hi + 1):
            for y in range(y0, y0 + t):
                x, z = (a, d) if plane == 'x' else (d, a)
                b.erase(x, y, z, x, y, z)
    if trim:
        td = lo if trim_d is None else trim_d
        for i, t in arch_ring(width, height, rise):
            a, y = a0 + i, y0 + t
            x, z = (a, td) if plane == 'x' else (td, a)
            if b.inside(x, y, z):
                b.set(x, y, z, trim(x, y, z) if callable(trim) else trim)
    if smooth:
        mid = (width - 1) / 2.0
        for i, t in enumerate(tops):
            toward = i + 1 if i < mid else i - 1
            if 0 <= toward < width and tops[toward] > t:
                if plane == 'x':
                    facing = 'west' if i < mid else 'east'
                else:
                    facing = 'north' if i < mid else 'south'
                for d in range(lo, hi + 1):
                    x, z = (a0 + i, d) if plane == 'x' else (d, a0 + i)
                    if b.inside(x, y0 + t, z):
                        b.set(x, y0 + t, z, smooth, facing=facing, half='top')
    return tops


def arch_ring(width, height, rise=None):
    """(column offset, y offset) cells just outside a pointed arch opening, bottom-left round to bottom-right."""
    tops = arch_tops(width, height, rise)
    opening = {(i, y) for i, t in enumerate(tops) for y in range(t)}
    ring = set()
    for i, y in opening:
        for di, dy in ((-1, 0), (1, 0), (0, 1)):
            c = (i + di, y + dy)
            if c not in opening and c[1] >= 0:
                ring.add(c)
    cx = (width - 1) / 2.0
    cy = (height - (rise if rise is not None else max(1, (width + 1) // 2))) / 2.0

    def key(c):
        # order from the bottom-left, up and over the top, down to the bottom-right
        theta = math.atan2(c[1] - cy, c[0] - cx)
        phi = theta if theta > -math.pi / 2 else theta + math.tau
        return -phi
    return sorted(ring, key=key)


# ------------------------------------------------------------------ roofs and caps
def spire_cap(b, x0, z0, size, y, kind=BRICK, edge=STAIR, steep=2, tip='end_rod', core=OBS):
    """A square pointed cap: rings step inward one cell every ``steep`` layers, stairs on the
    edges, ending in a single pillar and an end rod (or ``tip``). Returns the tip's y."""
    s = size
    while s >= 1:
        for k in range(steep):
            for z in range(z0, z0 + s):
                for x in range(x0, x0 + s):
                    edge_x = x in (x0, x0 + s - 1)
                    edge_z = z in (z0, z0 + s - 1)
                    if s >= 3 and (edge_x or edge_z):
                        if k == steep - 1 and edge:
                            if edge_z and not edge_x:
                                facing = 'south' if z == z0 else 'north'
                            elif edge_x and not edge_z:
                                facing = 'east' if x == x0 else 'west'
                            else:
                                facing = 'south' if z == z0 else 'north'
                            b.set(x, y, z, edge, facing=facing, half='bottom')
                        else:
                            b.set(x, y, z, kind if not callable(kind) else kind(x, y, z))
                    else:
                        b.set(x, y, z, core if s < 3 else (kind if not callable(kind) else kind(x, y, z)))
            y += 1
        if s <= 2:
            break
        x0 += 1
        z0 += 1
        s -= 2
    if tip:
        b.set(x0 + (s - 1) // 2, y, z0 + (s - 1) // 2, tip, **({'facing': 'up'} if tip == 'end_rod' else {}))
    return y


def merlons(b, cells, y, cap=True):
    """Merlons on the listed (x, z) cells at layer y, each with a slab cap above."""
    for x, z in cells:
        put_stone(b, x, y, z)
        if cap:
            slab(b, x, y + 1, z)


# ------------------------------------------------------------------ the void's floating shards
def shards(b, cx, cz, r0, r1, y0, y1, count, seed, kinds=(OBS, OBS, OBS, CRY), keep_clear=None):
    """Single obsidian fragments hovering around a tower: placed only where no neighbour is solid,
    so each one floats free (it's the End). ``keep_clear(x, y, z)`` can veto a cell."""
    rng = random.Random(seed)
    placed = []
    tries = 0
    while len(placed) < count and tries < count * 80:
        tries += 1
        ang = rng.random() * math.tau
        r = r0 + (r1 - r0) * rng.random()
        x = int(round(cx + math.cos(ang) * r))
        z = int(round(cz + math.sin(ang) * r))
        y = rng.randint(y0, y1)
        if not b.inside(x, y, z) or b.solid(x, y, z):
            continue
        if keep_clear and keep_clear(x, y, z):
            continue
        near = False
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    if (dx or dy or dz) and b.solid(x + dx, y + dy, z + dz):
                        near = True
        if near:
            continue
        b.set(x, y, z, rng.choice(kinds))
        placed.append((x, y, z))
    return placed


# ------------------------------------------------------------------ square spiral stairs
def spiral(b, x0, z0, n, w, y0, y1, start='north', kind=STAIR, landing=BRICK, soffit=True, clear=4):
    """A square spiral stair in the ring of width ``w`` around the inside of an ``n`` x ``n`` shaft
    whose interior's north-west cell is (x0, z0). It climbs clockwise (seen from above) from layer
    y0 (first step block) until a step reaches layer y1 - 1, so you step off onto a floor at y1.

    Sides are flights of stairs, corners are flat landings. ``clear`` cells above every tread are
    erased (Endarch headroom). Returns the list of (cells, y) treads in climbing order."""
    side = n - 2 * w
    assert side >= 1, 'shaft too small for the ring'
    corners = {
        'north': (x0, z0), 'east': (x0 + n - w, z0), 'south': (x0 + n - w, z0 + n - w), 'west': (x0, z0 + n - w)}
    order = ['north', 'east', 'south', 'west']
    i = order.index(start)
    treads = []
    y = y0
    while y <= y1 - 1:
        d = order[i % 4]
        # flight along side d (travel direction clockwise)
        for k in range(side):
            if y > y1 - 1:
                break
            if d == 'north':
                cells = [(x0 + w + k, z0 + j) for j in range(w)]
                facing = 'east'
            elif d == 'east':
                cells = [(x0 + n - w + j, z0 + w + k) for j in range(w)]
                facing = 'south'
            elif d == 'south':
                cells = [(x0 + n - w - 1 - k, z0 + n - w + j) for j in range(w)]
                facing = 'west'
            else:
                cells = [(x0 + j, z0 + n - w - 1 - k) for j in range(w)]
                facing = 'north'
            treads.append((cells, y, facing))
            y += 1
        if y > y1 - 1:
            break
        # corner landing at the end of side d
        nxt = order[(i + 1) % 4]
        cx, cz = corners[nxt]
        cells = [(cx + a, cz + c) for a in range(w) for c in range(w)]
        treads.append((cells, y, None))
        y += 1
        i += 1
    tread_cells = {(x, yy, z) for cells, yy, _ in treads for x, z in cells}
    for cells, yy, facing in treads:
        for x, z in cells:
            if facing:
                b.set(x, yy, z, kind, facing=facing, half='bottom')
            else:
                b.set(x, yy, z, landing)
            for dy in range(1, clear + 1):
                if (x, yy + dy, z) not in tread_cells:
                    b.erase(x, yy + dy, z, x, yy + dy, z)
    if soffit:
        for cells, yy, facing in treads:
            for x, z in cells:
                below = (x, yy - 1, z)
                if yy - 1 > y0 - 1 and below not in tread_cells and not b.solid(*below):
                    # keep headroom of lower turns clear
                    if any((x, yy - 1 - k, z) in tread_cells for k in range(1, clear + 1)):
                        continue
                    if facing:
                        b.set(x, yy - 1, z, kind, facing=INWARD[facing], half='top')
                    else:
                        b.set(x, yy - 1, z, SLAB, type='top')
    return treads
