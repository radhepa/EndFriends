"""Shared pieces for the Chorrin Stead: half-sunk end-stone domes, round arches, fibre nests, roof groves.

Chorrin build low and round. A dome is a short sunk drum (vertical walls below the islet surface and one
plinth course above it) under a cap that curves in to a flat crown. Every step of the curve carries an
end-stone-brick stair leaning on the step above it, so the cap reads smooth; the crown is bare end stone
so chorus can grow on it, and a pearlescent froglight set beside the crown lights the room and the roof.
"""
import math
import random
import zlib

from kit import DIRS

ES, ESB = 'end_stone', 'end_stone_bricks'
STAIRS, SLAB, WALL = 'end_stone_brick_stairs', 'end_stone_brick_slab', 'end_stone_brick_wall'
LEFT = {'north': 'west', 'south': 'east', 'east': 'north', 'west': 'south'}   # to your left when facing
RIGHT = {v: k for k, v in LEFT.items()}
BACK = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}


def rng_for(*parts):
    """A random source seeded from ``parts`` the same way on every run (``hash()`` of a string is not)."""
    return random.Random(zlib.crc32(repr(parts).encode('utf-8')))


def toward(dx, dz):
    """The compass direction of the larger component of (dx, dz)."""
    if abs(dx) >= abs(dz):
        return 'east' if dx > 0 else 'west'
    return 'south' if dz > 0 else 'north'


def step(x, z, direction, n=1):
    dx, dz = DIRS[direction]
    return x + dx * n, z + dz * n


class Dome:
    """A dome on (cx, cz) with outer radii (rx, rz); centres may be half-integers.

    ``floor``: layer of the floor blocks. ``crown``: y of the outer top surface at the centre.
    ``wall_top``: y where the vertical drum ends and the cap starts (default ground + 2: the drum
    shows one plinth course above the islet). ``power`` shapes the cap: 0.5 is a sphere, higher is
    more pointed, lower is flatter. ``build()`` draws the shell and carves the room (explicit air).
    """

    def __init__(self, b, cx, cz, rx, rz, floor, crown, wall_top=None, power=0.6, band=None,
                 floor_block=ESB, seed=0, trim=STAIRS, cap_slab=None, skin=None, slab_at=0.45, max_rise=1,
                 lobes=()):
        self.b = b
        self.cx, self.cz, self.rx, self.rz = cx, cz, rx, rz
        self.floor, self.crown = floor, crown
        self.wall_top = b.ground + 2 if wall_top is None else wall_top
        self.power = power
        self.band = band
        self.floor_block = floor_block
        self.trim, self.cap_slab = trim, cap_slab
        self.custom_skin = skin
        self.slab_at = slab_at
        self.rng = rng_for(b.name, cx, cz, seed)
        self.t = {}        # (x, z) -> true height of the outer surface
        self.hgt = {}      # (x, z) -> full blocks fill the column up to (not including) this layer
        self.piece = {}    # (x, z) -> 'stair' | 'slab': the trim piece sitting on layer hgt
        self.max_rise = max_rise
        for lobe in [(cx, cz, rx, rz, crown)] + list(lobes):
            for c, (t, h) in self._lobe(*lobe).items():
                if c not in self.hgt or (h, t) > (self.hgt[c], self.t[c]):
                    self.t[c], self.hgt[c] = t, h
        self.full = set()
        for (x, z), h in self.hgt.items():
            for y in range(floor, h):
                self.full.add((x, y, z))
        self.inner = set()
        for (x, y, z) in self.full:
            if y < floor + 1:
                continue
            if all(n in self.full for n in ((x + 1, y, z), (x - 1, y, z), (x, y, z + 1), (x, y, z - 1), (x, y + 1, z))):
                self.inner.add((x, y, z))
        self.shell = self.full - self.inner

    def _lobe(self, cx, cz, rx, rz, crown):
        """{(x, z): (t, h)} for one dome outline: concentric rings one block wide, each at one height,
        so every step of the cap runs round cleanly; each ring rises at most ``max_rise`` over the
        one outside it, so every step can carry a stair."""
        b, ring = self.b, {}
        mean_r = (rx + rz) / 2
        for z in range(math.floor(cz - rz), math.ceil(cz + rz) + 1):
            for x in range(math.floor(cx - rx), math.ceil(cx + rx) + 1):
                q = ((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2
                if q <= 1.0 and b.inside(x, 0, z):
                    ring[(x, z)] = math.floor(mean_r * (1 - math.sqrt(q)))
        while True:     # drop lone tips where the outline only grazes a row
            tips = [c for c in ring if sum((c[0] + dx, c[1] + dz) in ring for dx, dz in DIRS.values()) <= 1]
            if not tips:
                break
            for c in tips:
                del ring[c]
        heights, prev = {}, None
        for k in sorted(set(ring.values())):
            rho = max(0.0, 1 - (k + 0.5) / mean_r)
            t = self.wall_top + (crown - self.wall_top) * (1 - rho * rho) ** self.power
            h = max(math.floor(t + 0.35), self.floor + 2)
            if prev is not None and self.max_rise:
                h = min(h, prev + self.max_rise)
            heights[k] = (t, h)
            prev = h
        return {c: heights[k] for c, k in ring.items()}

    # ------------------------------------------------------------- queries
    def has(self, x, z):
        return (x, z) in self.hgt

    def top(self, x, z):
        """Layer of the topmost shell cell of a column (a trim piece counts)."""
        h = self.hgt[(x, z)]
        return h if (x, z) in self.piece else h - 1

    def apex(self):
        """The highest column nearest the centre."""
        return max(self.hgt, key=lambda c: (self.hgt[c], self.t[c], -abs(c[0] - self.cx) - abs(c[1] - self.cz)))

    def room(self, y):
        """Interior air cells on layer y."""
        return sorted((x, z) for (x, yy, z) in self.inner if yy == y)

    def is_room(self, x, y, z):
        return (x, y, z) in self.inner

    def wall_cell(self, direction, y, offset=0):
        """The outermost shell cell on layer y reached walking from the centre toward ``direction``.

        ``offset`` slides the walk sideways (to the right of the direction). Returns (x, z) or None."""
        dx, dz = DIRS[direction]
        rx, rz = DIRS[RIGHT[direction]]
        x, z = math.floor(self.cx + 0.5) + rx * offset, math.floor(self.cz + 0.5) + rz * offset
        last = None
        for _ in range(48):
            if (x, y, z) in self.shell:
                last = (x, z)
                if (x + dx, y, z + dz) not in self.full:
                    return last
            x, z = x + dx, z + dz
        return last

    # ------------------------------------------------------------- drawing
    def skin(self, x, y, z):
        if self.custom_skin:
            found = self.custom_skin(self, x, y, z)
            if found:
                return found
        g = self.b.ground
        if y == self.floor:
            return self.floor_block
        if y <= g + 1:
            return ESB
        if self.band is not None and y == self.band:
            return ESB
        return ES

    def build(self):
        b = self.b
        for (x, y, z) in self.shell:
            b.set(x, y, z, self.skin(x, y, z))
        for (x, z), h in self.hgt.items():
            best, best_key = None, None
            for direction, (dx, dz) in DIRS.items():
                nh = self.hgt.get((x + dx, z + dz), 0)
                if nh <= h:
                    continue
                # prefer the taller neighbour, then the one pointing at the centre
                key = (nh, dx * (self.cx - x) + dz * (self.cz - z))
                if best_key is None or key > best_key:
                    best, best_key = direction, key
            if not b.inside(x, h, z):
                continue
            if not best:
                # an outside corner of a ring: the higher cell is diagonal; finish() turns it outer
                for ddx, ddz in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                    if self.hgt.get((x + ddx, z + ddz), 0) > h:
                        best = toward(ddx, 0) if abs(self.cx - x) <= abs(self.cz - z) else toward(0, ddz)
                        break
            if best:
                b.set(x, h, z, self.trim, facing=best, half='bottom')
                self.piece[(x, z)] = 'stair'
            elif self.cap_slab and self.t[(x, z)] - h >= self.slab_at:
                b.set(x, h, z, self.cap_slab, type='bottom')
                self.piece[(x, z)] = 'slab'
        for (x, y, z) in self.inner:      # explicit air: carves the islet where the room is sunk
            b.set(x, y, z, 'air')
        return self

    def berm(self, skip=()):
        """A ring of stairs leaning on the drum at the plinth course, as if earth were banked against it."""
        b, y = self.b, self.b.ground + 1
        for (x, z) in list(self.hgt):
            for direction, (dx, dz) in DIRS.items():
                ox, oz = x + dx, z + dz
                if (ox, oz) in self.hgt or (ox, oz) in skip or not b.inside(ox, y, oz) or b.solid(ox, y, oz):
                    continue
                if (ox, y, oz) in b.grid:      # explicit air (a trench) stays open
                    continue
                b.set(ox, y, oz, STAIRS, facing=BACK[direction], half='bottom')

    def window(self, direction, y, offset=0, glass='purple_stained_glass_pane', brow=True, brow_block=STAIRS):
        """A small window through the shell. Its brow is the shell block over it turned into an
        upside-down stair, so the window sits in a shadowed notch like a Chorrin's deep-set eye."""
        cell = self.wall_cell(direction, y, offset)
        if not cell:
            return None
        x, z = cell
        dx, dz = DIRS[direction]
        if (x - dx, y, z - dz) not in self.inner or self.b.solid(x + dx, y, z + dz):
            return None
        sx, sz = DIRS[LEFT[direction]]
        if (x + sx, y, z + sz) not in self.shell or (x - sx, y, z - sz) not in self.shell:
            return None     # only in a straight run of wall, where a pane sits flat
        self.b.set(x, y, z, glass)
        if brow and ((x, y + 1, z) in self.shell or self.piece.get((x, z)) and self.hgt[(x, z)] == y + 1):
            self.b.set(x, y + 1, z, brow_block, facing=BACK[direction], half='top')
        return (x, y, z)

    def crown_cells(self):
        """Cap cells where chorus can root: bare end stone with open air above, highest first."""
        out = []
        for (x, z), h in self.hgt.items():
            if (x, z) in self.piece:
                continue
            if self.b.get(x, h - 1, z)[0] == 'minecraft:end_stone' and not self.b.solid(x, h, z):
                out.append((h, self.t[(x, z)], -abs(x - self.cx) - abs(z - self.cz), x, h, z))
        out.sort(reverse=True)
        return [(x, y, z) for *_, x, y, z in out]

    def plant(self, x, z, height, branches=True, tree=False, arms=3):
        """Plant chorus on the cap column (x, z), making its top bare end stone first."""
        b = self.b
        h = self.hgt[(x, z)]
        if (x, z) in self.piece:
            b.set(x, h, z, ES)
            self.hgt[(x, z)] = h = h + 1
            del self.piece[(x, z)]
        b.set(x, h - 1, z, ES)
        height = min(height, b.h - h - 1)
        if (tree or branches) and height >= 3:
            chorus_tree(b, x, h, z, height=height, arms=arms if tree else 2, rng=self.rng, depth=1 if tree else 0)
        elif height >= 1:
            sprout(b, x, h, z, height)
        return (x, h, z)

    def roof_grove(self, big=5, small=(2, 3), skylight=True, spread=2, avoid=(), arms=3):
        """Chorus on the roof: a tall plant on the crown (the house's own chorus crown) and smaller ones
        round it, plus a pearlescent froglight set beside the crown to light the room and the roof."""
        b = self.b
        ax, az = self.apex()
        light = None
        if skylight:
            for direction in ('north', 'east', 'west', 'south'):
                lx, lz = step(ax, az, direction)
                if (lx, lz) not in self.hgt:
                    continue
                ly = self.hgt[(lx, lz)] - 1
                if (lx, ly - 1, lz) in self.inner:
                    if (lx, lz) in self.piece:
                        b.set(lx, ly + 1, lz, 'air')
                        del self.piece[(lx, lz)]
                    b.set(lx, ly, lz, 'pearlescent_froglight')
                    light = (lx, ly, lz)
                    break
        if big > 0:
            self.plant(ax, az, big, tree=True, arms=arms)
        planted = [(ax, az)] + list(avoid)
        for hh in small:
            for (x, y, z) in self.crown_cells():
                if any(abs(x - px) + abs(z - pz) < spread + 1 for px, pz in planted):
                    continue
                if light and abs(x - light[0]) + abs(z - light[2]) < 2:
                    continue
                if all(not b.solid(x, y + k, z) for k in range(hh + 1)):
                    self.plant(x, z, hh, branches=hh >= 3)
                    planted.append((x, z))
                    break
        return light


def _free(b, x, y, z):
    return b.inside(x, y, z) and not b.solid(x, y, z)


def chorus_tree(b, x, y, z, height=6, arms=4, rng=None, depth=2, flower_age=(5,), dirs=None, low=1, reach=False):
    """A big planted chorus, branching like the wild ones: a stem from end stone at (x, y - 1, z) whose
    top cell sends out arms that step one block sideways, climb, and branch again from their own tops,
    every tip ending in a flower. Vanilla breaks a stalk cell that has chorus beside it and blocks both
    above and below, so arms only ever leave from the top of a stalk, never from its middle, and never
    touch another plant. ``dirs`` limits the directions arms may take; ``low`` is kept for callers (arms
    now always start at the stem's top). Flowers are full grown (age 5) by default, so a planted
    chorus keeps its shape. ``reach`` makes arms tend to keep going outward, for a broad crown."""
    rng = rng or rng_for(b.name, x, y, z, 'tree')
    assert b.get(x, y - 1, z)[0] == 'minecraft:end_stone', f'{b.name}: chorus tree at {(x, y, z)} needs end stone below'
    height = min(height, b.h - y - 1)
    for k in range(height):
        if not _free(b, x, y + k, z) or not _lonely(b, x, y + k, z, ()):
            height = k
            break
    if height < 1:
        return
    for k in range(height):
        b.set(x, y + k, z, 'chorus_plant')
    top = y + height - 1
    placed = 0
    if height >= 3 and arms > 0:
        allowed = list(dirs or DIRS)
        for direction in rng.sample(allowed, len(allowed))[:arms]:
            if _arm(b, x, top, z, direction, rng, depth, flower_age, allowed, reach):
                placed += 1
    if not placed and _free(b, x, top + 1, z):
        b.set(x, top + 1, z, 'chorus_flower', age=rng.choice(flower_age))


def sprout(b, x, y, z, height=2, age=5):
    """A straight planted chorus (no branches) of up to ``height`` stalks and a flower, rooted in the end
    stone at (x, y - 1, z). It only grows into free cells, so it never cuts another plant."""
    assert b.get(x, y - 1, z)[0] == 'minecraft:end_stone', f'{b.name}: chorus at {(x, y, z)} needs end stone below'
    top = y
    for k in range(height):
        if not _free(b, x, y + k, z) or not _free(b, x, y + k + 1, z):
            break
        b.set(x, y + k, z, 'chorus_plant')
        top = y + k + 1
    if _free(b, x, top, z):
        b.set(x, top, z, 'chorus_flower', age=age)


def _lonely(b, x, y, z, parents):
    """No chorus beside (x, y, z) except its parent cells: plants that touch break each other."""
    for direction in DIRS:
        nx, nz = step(x, z, direction)
        if (nx, y, nz) in parents:
            continue
        if b.get(nx, y, nz)[0] in ('minecraft:chorus_plant', 'minecraft:chorus_flower'):
            return False
    return True


def _arm(b, x, y, z, direction, rng, depth, flower_age, allowed=None, reach=False):
    """An arm from the top cell (x, y, z) of a stalk; True if it grew."""
    ax, az = step(x, z, direction)
    if not _free(b, ax, y, az) or not _free(b, ax, y - 1, az) or not _free(b, ax, y + 1, az):
        return False
    if not _lonely(b, ax, y, az, {(x, y, z)}) or not _lonely(b, ax, y + 1, az, ()):
        return False
    b.set(ax, y, az, 'chorus_plant')
    up = rng.randint(1, 3)
    top = y
    for k in range(1, up + 1):
        if not _free(b, ax, y + k, az) or not _free(b, ax, y + k + 1, az) or not _lonely(b, ax, y + k, az, ()):
            break
        b.set(ax, y + k, az, 'chorus_plant')
        top = y + k
    grew = False
    if depth > 0 and top > y and rng.random() < 0.7:
        turns = [d for d in (allowed or DIRS) if d != BACK[direction]]
        if reach and direction in turns:
            turns += [direction] * 2
        if turns:
            grew = _arm(b, ax, top, az, rng.choice(turns), rng, depth - 1, flower_age, allowed, reach)
    if not grew and _free(b, ax, top + 1, az):
        b.set(ax, top + 1, az, 'chorus_flower', age=rng.choice(flower_age))
    return True


def arch(b, cx, y, z, facing='north', posts=True, ring=STAIRS, crown=None, **ring_kw):
    """A round arch over a 3-wide opening centred on cx (on x for north/south arches, on z for east/west).

    The opening stands on layer y and is 2.5 blocks high: upside-down end-stone-brick stairs round its
    top corners (row y + 2), a ring of stairs rounds the outside (rows y + 3 and y + 4) and posts at
    +-2 carry it. ``z`` is the plane of the arch (an x for east/west arches)."""
    side = 'x' if facing in ('north', 'south') else 'z'
    lo, hi = (('west', 'east') if side == 'x' else ('north', 'south'))

    def put(u, yy, spec, **kw):
        if side == 'x':
            b.set(cx + u, yy, z, spec, **kw)
        else:
            b.set(z, yy, cx + u, spec, **kw)

    if posts:
        for yy in range(y, y + 3):
            put(-2, yy, ESB)
            put(2, yy, ESB)
    put(-1, y + 2, STAIRS, facing=lo, half='top')
    put(0, y + 2, SLAB, type='top')
    put(1, y + 2, STAIRS, facing=hi, half='top')
    put(-2, y + 3, ring, facing=hi, half='bottom')
    put(-1, y + 3, ESB)
    put(0, y + 3, ESB)
    put(1, y + 3, ESB)
    put(2, y + 3, ring, facing=lo, half='bottom')
    put(-1, y + 4, ring, facing=hi, half='bottom')
    if crown:
        put(0, y + 4, crown, **ring_kw)
    else:
        put(0, y + 4, ring.replace('_stairs', '_slab'), type='bottom')
    put(1, y + 4, ring, facing=lo, half='bottom')


def round_door(b, x, y, z, facing='north', hinge='left', ring=STAIRS, glass='purple_stained_glass_pane',
               keystone=None, posts=ESB):
    """The Chorrin round door: a pale oak door in a round 3x3 opening, with violet glass side lights
    beside it and a transom over it. Upside-down end-stone-brick stairs round the opening's top corners,
    a ring of ``ring`` stairs rounds the frame outside, and posts at +-2 carry it. 5 wide, 5 high.
    ``facing`` is the side the door opens out toward; (x, y, z) is the door's lower half."""
    side = 'x' if facing in ('north', 'south') else 'z'
    lo, hi = (('west', 'east') if side == 'x' else ('north', 'south'))

    def put(u, yy, spec, **kw):
        if side == 'x':
            b.set(x + u, yy, z, spec, **kw)
        else:
            b.set(x, yy, z + u, spec, **kw)

    for yy in range(y, y + 3):
        put(-2, yy, posts)
        put(2, yy, posts)
    b.door(x, y, z, facing=facing, kind='pale_oak', hinge=hinge)
    for yy in (y, y + 1):
        put(-1, yy, glass)
        put(1, yy, glass)
    put(-1, y + 2, STAIRS, facing=lo, half='top')
    put(0, y + 2, glass)
    put(1, y + 2, STAIRS, facing=hi, half='top')
    put(-2, y + 3, ring, facing=hi, half='bottom')
    put(-1, y + 3, ESB)
    put(0, y + 3, ESB)
    put(1, y + 3, ESB)
    put(2, y + 3, ring, facing=lo, half='bottom')
    put(-1, y + 4, ring, facing=hi, half='bottom')
    if keystone:
        put(0, y + 4, keystone)
    else:
        put(0, y + 4, ring.replace('_stairs', '_slab'), type='bottom')
    put(1, y + 4, ring, facing=lo, half='bottom')


def nest(b, x, y, z, opening='north', rim='brown', bed='white', lining='purple', spot=True):
    """A Chorrin sleeping nest of woven fibre: a carpeted hollow at (x, y, z) inside a U of wool stairs,
    open toward ``opening``. The U takes the cells behind and beside the hollow; corners get wool."""
    back = BACK[opening]

    def open_cell(cx, cz):
        # only cells of the room itself: carved air below the islet surface, any free cell above it
        if not b.inside(cx, y, cz) or b.solid(cx, y, cz):
            return False
        return y > b.ground or (cx, y, cz) in b.grid

    b.set(x, y, z, f'{bed}_carpet')
    for direction in (back, LEFT[opening], RIGHT[opening]):
        cx, cz = step(x, z, direction)
        if open_cell(cx, cz):
            b.set(cx, y, cz, f'{rim}_wool_stairs', facing=direction, half='bottom')
    for side in (LEFT[opening], RIGHT[opening]):
        cx, cz = step(*step(x, z, back), side)
        if open_cell(cx, cz):
            b.set(cx, y, cz, f'{lining}_wool')
    if spot:
        b.spot('sleep', x, y, z)


def lantern_post(b, x, y, z, height=1):
    """An end-stone-brick wall post with a lantern on top."""
    for k in range(height):
        b.set(x, y + k, z, WALL)
    b.lantern(x, y + height, z)


def hanging_lantern(b, x, y, z, chain=1):
    """A lantern hanging on iron chain under the block above (x, y + chain + 1, z).
    ``chain=None`` runs the chain up to whatever ceiling is above."""
    if chain is None:
        chain = 0
        while b.inside(x, y + 1 + chain, z) and not b.solid(x, y + 1 + chain, z):
            chain += 1
    for k in range(chain):
        b.set(x, y + 1 + k, z, 'iron_chain', axis='y', waterlogged=False)
    b.lantern(x, y, z, hanging=True)


def rug(b, x0, z0, x1, z1, y, colors=('purple', 'white'), border='brown', skip_solid=True):
    """A woven rug: a border of one colour round a checked middle."""
    for z in range(min(z0, z1), max(z0, z1) + 1):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            if skip_solid and b.solid(x, y, z):
                continue
            edge = x in (x0, x1) or z in (z0, z1)
            color = border if edge else colors[(x + z) % len(colors)]
            b.set(x, y, z, f'{color}_carpet')


def seat(b, x, y, z, facing, cushion='purple'):
    """A cushioned seat (a wool stair; ``facing`` is the side its back is on) and its sit spot."""
    b.set(x, y, z, f'{cushion}_wool_stairs', facing=facing, half='bottom')
    b.spot('sit', x, y, z)


def stone_seat(b, x, y, z, facing):
    b.set(x, y, z, STAIRS, facing=facing, half='bottom')
    b.spot('sit', x, y, z)


def pot(b, x, y, z, facing='north'):
    b.set(x, y, z, 'decorated_pot', facing=facing, cracked=False, waterlogged=False)


def shelf(b, x, y, z, facing):
    """A pale oak shelf (a rare import) on a wall; ``facing`` is the side it opens toward."""
    b.set(x, y, z, 'pale_oak_shelf', facing=facing, powered=False, side_chain='unconnected', waterlogged=False)


def sunk_entry(b, door, floor, z_door, width=3, mat='purple'):
    """The way in for a sunk home: from the islet surface at z = 0 down a flight of stairs to a landing
    in front of the door at z_door. (door, ground, 0) and (door, ground + 1, 0) stay open so the village
    path runs straight in; lanterns on posts mark the top of the steps."""
    g = b.ground
    half = width // 2
    x0, x1 = door - half, door + half
    b.clear(x0, floor + 1, 0, x1, g + 1, z_door - 1)
    z = 0
    for y in range(g - 1, floor, -1):
        for x in range(x0, x1 + 1):
            b.set(x, y, z, STAIRS, facing='north', half='bottom')
            b.fill(x, 0, z, x, y - 1, z, ESB)
        z += 1
    for zz in range(z, z_door):
        b.fill(x0, floor, zz, x1, floor, zz, ESB)
    if mat:
        b.set(door, floor + 1, z_door - 1, f'{mat}_carpet')      # a woven mat at the door
    for x in (x0 - 1, x1 + 1):
        b.fill(x, 0, 0, x, g, z_door - 1, ESB)
        b.set(x, g + 1, 0, WALL)
        b.lantern(x, g + 2, 0)
        for zz in range(1, z_door):
            b.set(x, g + 1, zz, SLAB, type='bottom')


def arch_opening(b, c, y, plane, axis='x', top=True):
    """Cut a round-topped opening 3 wide and 2.5 high through a wall: centred on c along ``axis``
    ('x': the wall runs east-west at z = plane; 'z': it runs north-south at x = plane)."""
    def put(u, yy, spec, **kw):
        if axis == 'x':
            b.set(c + u, yy, plane, spec, **kw)
        else:
            b.set(plane, yy, c + u, spec, **kw)
    lo, hi = ('west', 'east') if axis == 'x' else ('north', 'south')
    for u in (-1, 0, 1):
        for yy in (y, y + 1):
            put(u, yy, 'air')
    if top:
        put(-1, y + 2, STAIRS, facing=lo, half='top')
        put(0, y + 2, SLAB, type='top')
        put(1, y + 2, STAIRS, facing=hi, half='top')
