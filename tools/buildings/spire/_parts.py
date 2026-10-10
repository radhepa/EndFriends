"""Shared parts for the Shulkin Spire buildings.

Every Shulkin building echoes a shulker's shell: a BODY (purpur walls on an end-stone-brick course),
the glowing GAP where the shell opens (a band of magenta glass set with pearlescent froglights), and
an overhanging LID (domed, tilted, boxed, stacked, tented or lifted onto pillars). The helpers work
on "plans": sets of (x, z) cells, so the same code draws octagonal towers, long halls and oval shells.

Shulkin stand about 2.6 blocks tall, so every route they walk keeps room for them: doorways are
three blocks high (a door plus an open transom), rooms have at least three clear blocks, stairs
clear four blocks above each tread (the head must pass under the floor above while climbing), and
floors are joined by stairs, never only by ladders (mobs do not path up ladders). Roof tops are
slabs or stairs, or lit, so nothing spawns on them.
"""
import math

DIRS4 = {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}
OPP = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
LEFT = {'north': 'west', 'west': 'south', 'south': 'east', 'east': 'north'}


# ----------------------------------------------------------------------------- plans (sets of cells)
def octo(cx, cz, rx, rz=None, k=None):
    """A chamfered rectangle centred on (cx, cz): |dx| <= rx, |dz| <= rz, |dx| + |dz| <= k.

    With rx == rz and the default k it is the octagon of the original spire home."""
    rz = rx if rz is None else rz
    if k is None:
        k = max(rx, rz) + math.floor(min(rx, rz) * 0.45)
    out = set()
    for z in range(math.floor(cz - rz), math.ceil(cz + rz) + 1):
        for x in range(math.floor(cx - rx), math.ceil(cx + rx) + 1):
            dx, dz = abs(x - cx), abs(z - cz)
            if dx <= rx and dz <= rz and dx + dz <= k:
                out.add((x, z))
    return out


def oval(cx, cz, rx, rz):
    """An ellipse of radii rx, rz (half-integer centres work)."""
    out = set()
    for z in range(math.floor(cz - rz) - 1, math.ceil(cz + rz) + 2):
        for x in range(math.floor(cx - rx) - 1, math.ceil(cx + rx) + 2):
            if ((x - cx) / (rx + 0.5)) ** 2 + ((z - cz) / (rz + 0.5)) ** 2 <= 1.0:
                out.add((x, z))
    return out


def rect(x0, z0, x1, z1):
    return {(x, z) for x in range(min(x0, x1), max(x0, x1) + 1) for z in range(min(z0, z1), max(z0, z1) + 1)}


def edge(cells):
    """Cells of the plan with a side neighbour outside it (a 1-thick, light-tight outline)."""
    return {(x, z) for (x, z) in cells if any((x + dx, z + dz) not in cells for dx, dz in DIRS4.values())}


def shrink(cells, n=1):
    for _ in range(n):
        cells = cells - edge(cells)
    return cells


def rings(cells):
    """Depth of each cell inside the plan: 0 on the outline, 1 just inside it, and so on."""
    out = {}
    i = 0
    cur = set(cells)
    while cur:
        e = edge(cur)
        for c in e:
            out[c] = i
        cur -= e
        i += 1
    return out


def facing_out(cells, x, z):
    """The single best 'out' direction of an outline cell (ties broken by distance from the centre)."""
    outs = [d for d, (dx, dz) in DIRS4.items() if (x + dx, z + dz) not in cells]
    if len(outs) == 1:
        return outs[0]
    cx = sum(c[0] for c in cells) / len(cells)
    cz = sum(c[1] for c in cells) / len(cells)
    if not outs:
        outs = list(DIRS4)
    return max(outs, key=lambda d: (x - cx) * DIRS4[d][0] + (z - cz) * DIRS4[d][1])


def corners(cells):
    """Outline cells where the outline turns (good spots for pillars)."""
    out = set()
    ring = edge(cells)
    for x, z in ring:
        n = [(x + dx, z + dz) in ring for dx, dz in ((0, -1), (0, 1), (1, 0), (-1, 0))]
        straight = (n[0] and n[1] and not n[2] and not n[3]) or (n[2] and n[3] and not n[0] and not n[1])
        if not straight:
            out.add((x, z))
    return out


# ------------------------------------------------------------------------------------- drawing
def put(b, cells, y, spec, only_air=False, **kw):
    for x, z in cells:
        if b.inside(x, y, z) and not (only_air and b.solid(x, y, z)):
            b.set(x, y, z, spec, **kw)


def column(b, cells, y0, y1, spec, **kw):
    for y in range(y0, y1 + 1):
        put(b, cells, y, spec, **kw)


def air(b, cells, y0, y1):
    for y in range(y0, y1 + 1):
        for x, z in cells:
            if b.inside(x, y, z):
                b.set(x, y, z, 'air')


def heightfield(b, cols, block='purpur_block', slab='purpur_slab'):
    """Fill each column (x, z) -> (bottom, top) given in HALF blocks: [bottom, top).

    Half cells become slabs, so lids and domes step in half blocks."""
    for (x, z), (lo, hi) in cols.items():
        for y in range(lo // 2, (hi + 1) // 2 + 1):
            low_in = lo <= 2 * y < hi
            high_in = lo <= 2 * y + 1 < hi
            if not b.inside(x, y, z):
                continue
            if low_in and high_in:
                b.set(x, y, z, block)
            elif low_in:
                b.set(x, y, z, slab, type='bottom')
            elif high_in:
                b.set(x, y, z, slab, type='top')


def stair_roof(b, tops, bottoms, block='purpur_block', stairs='purpur_stairs', slab='purpur_slab', flat='slab'):
    """A roof from whole-block heights: column (x, z) is solid from ``bottoms[(x, z)]`` up to
    ``tops[(x, z)] - 1``. Where the surface steps down to a neighbour (or to the outline) the top block
    becomes a stair facing uphill, so domes and slopes read smooth. Ridges and peaks get a slab;
    with ``flat='slab'`` flat tops are capped with a bottom slab too (nothing spawns on a slab)."""
    for (x, z), top in tops.items():
        lo = bottoms[(x, z)]
        for y in range(lo, top):
            b.set(x, y, z, block)
        down = [d for d, (dx, dz) in DIRS4.items() if tops.get((x + dx, z + dz), -99) < top]
        if top - 1 < lo:
            continue
        if not down:
            if flat == 'slab':
                b.set(x, top, z, slab, type='bottom')
            continue
        ups = [d for d in DIRS4 if d not in down]
        ups = [d for d in ups if OPP[d] in down] or ups
        if not ups:
            if top - 1 > lo:
                b.set(x, top - 1, z, slab, type='bottom')
            continue
        best = max(ups, key=lambda d: tops.get((x + DIRS4[d][0], z + DIRS4[d][1]), -99))
        b.set(x, top - 1, z, stairs, facing=best, half='bottom')


def lip(b, cells, y, block='purpur_stairs'):
    """Upside-down stairs round the outline at layer y: the moulded underside of a lid's overhang."""
    for x, z in edge(cells):
        d = facing_out(cells, x, z)
        if b.inside(x, y, z):
            b.set(x, y, z, block, facing=OPP[d], half='top')


def gap_band(b, plan, y0, y1, every=3, glass='magenta_stained_glass', glow='pearlescent_froglight', recess=1):
    """The glowing gap, recessed: the outline of ``plan`` is left open (a shadow line) and the band is
    set back by ``recess`` in magenta glass, every ``every``-th cell a froglight."""
    cx = sum(c[0] for c in plan) / len(plan)
    cz = sum(c[1] for c in plan) / len(plan)
    inner = shrink(plan, recess) if recess else plan
    ring = sorted(edge(inner), key=lambda c: math.atan2(c[1] - cz, c[0] - cx))
    if recess:
        air(b, edge(plan), y0, y1)
    for i, (x, z) in enumerate(ring):
        for y in range(y0, y1 + 1):
            b.set(x, y, z, glow if every and i % every == 0 else glass)
    return ring


def band(b, ring_cells, y0, y1, every=3, posts=()):
    """The glowing gap, flush: magenta glass with a froglight every few cells, pillars at ``posts``."""
    cx = sum(c[0] for c in ring_cells) / len(ring_cells)
    cz = sum(c[1] for c in ring_cells) / len(ring_cells)
    order = sorted(ring_cells, key=lambda c: math.atan2(c[1] - cz, c[0] - cx))
    k = 0
    for x, z in order:
        if (x, z) in posts:
            for y in range(y0, y1 + 1):
                b.set(x, y, z, 'purpur_pillar', axis='y')
            k = 0
            continue
        k += 1
        for y in range(y0, y1 + 1):
            b.set(x, y, z, 'pearlescent_froglight' if k % every == 0 else 'magenta_stained_glass')


# ------------------------------------------------------------------------------------- doors
def doorway(b, x, y, z, facing='north', arch='purpur_stairs', lintel='purpur_block', rods=True, hinge='left'):
    """A crimson door with an open transom above it (three blocks high, for 2.6-block Shulkin),
    framed by an upside-down stair arch and a pair of end rods beside it."""
    b.door(x, y, z, facing=facing, hinge=hinge)
    b.set(x, y + 2, z, 'air')
    side = LEFT[facing]
    dx, dz = DIRS4[side]
    for s in (1, -1):
        b.set(x + s * dx, y + 2, z + s * dz, arch, facing=side if s == -1 else OPP[side], half='top')
    if lintel:
        b.set(x, y + 3, z, lintel)
    if rods:
        fx, fz = DIRS4[facing]
        for s in (1, -1):
            px, pz = x + s * dx + fx, z + s * dz + fz
            if b.inside(px, y + 2, pz) and not b.solid(px, y + 2, pz):
                b.end_rod(px, y + 2, pz, facing)


# ------------------------------------------------------------------------------------- stairs
def stair_path(b, path, y, block='purpur_stairs', landing='purpur_block', clear=4, under='purpur_stairs',
               landings=True):
    """Lay a stair along ``path`` (an ordered list of (x, z) side-by-side cells), starting with the
    feet at layer ``y`` (the floor is y - 1). Straight cells get a stair that climbs one block;
    cells where the path turns get a flat landing (or, with ``landings=False``, a stair facing the
    new way, for tight spirals). Headroom above each step is cleared (``clear`` blocks above the
    tread), so the floors above get stairwell holes: draw floors first, then stairs. Returns the
    feet level reached.

    ``under``: upside-down stairs under each tread for a clean zigzag soffit (None to leave it)."""
    level = y
    n = len(path)
    for i, (x, z) in enumerate(path):
        nxt = path[i + 1] if i + 1 < n else None
        prv = path[i - 1] if i > 0 else None
        d_in = (x - prv[0], z - prv[1]) if prv else None
        d_out = (nxt[0] - x, nxt[1] - z) if nxt else d_in
        turning = prv is not None and nxt is not None and d_in != d_out
        if (turning and landings) or d_out is None:
            b.set(x, level - 1, z, landing)
            for h in range(clear):
                b.set(x, level + h, z, 'air')
            continue
        facing = {(0, -1): 'north', (0, 1): 'south', (1, 0): 'east', (-1, 0): 'west'}[d_out]
        b.set(x, level, z, block, facing=facing, half='bottom')
        if under and level - 1 >= 0 and not b.solid(x, level - 1, z):
            b.set(x, level - 1, z, under, facing=OPP[facing], half='top')
        for h in range(1, clear + 1):
            b.set(x, level + h, z, 'air')
        level += 1
    return level


# ------------------------------------------------------------------------------------- furniture
def eye(b, cx, y, cz, half_len=6, half_h=3, outline='purple_concrete', white='purpur_block',
        iris='magenta_concrete', pupil='pearlescent_froglight', iris_r=2, along='x', skip=()):
    """The Eye of the Spires inlaid in a floor: an almond outline, an iris diamond and a glowing pupil."""
    cells = {}
    for dz in range(-half_h, half_h + 1):
        for dx in range(-half_len, half_len + 1):
            t = abs(dx) / (half_len + 0.5)
            if abs(dz) <= half_h * (1 - t * t) + 0.35:
                cells[(dx, dz)] = 'in'
    for (dx, dz) in list(cells):
        if any((dx + ex, dz + ez) not in cells for ex, ez in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            cells[(dx, dz)] = 'line'
    for (dx, dz), kind in cells.items():
        x, z = (cx + dx, cz + dz) if along == 'x' else (cx + dz, cz + dx)
        if (x, z) in skip or not b.inside(x, y, z):
            continue
        r = abs(dx) + abs(dz)
        if kind == 'line':
            b.set(x, y, z, outline)
        elif r == 0:
            b.set(x, y, z, pupil)
        elif r <= iris_r:
            b.set(x, y, z, iris)
        else:
            b.set(x, y, z, white)
    return cells


def hang(b, x, y, z, kind='lantern', reach=8):
    """A hanging lantern at (x, y, z) on an iron chain run up to the first solid block above it."""
    b.lantern(x, y, z, hanging=True, kind=kind)
    for yy in range(y + 1, min(b.h, y + 1 + reach)):
        if b.solid(x, yy, z):
            return
        b.set(x, yy, z, 'iron_chain', axis='y')
    raise AssertionError(f'{b.name}: nothing above the lantern at {(x, y, z)} to hang it from')
