"""Plans End villages: buildings ringed round a centre, each on its own islet, joined by paths and bridges.

A plan is made from a ``Program`` (which buildings, how spread out, how high the islets may sit)
and a seed, so every layout is fixed and reproducible. The result is a ``Layout``: one big
``kit.Build`` canvas in layout space (y = 0 is the village floor, the plaza's surface) plus the
ground raster (top and underside depth of every islet column) that the game's ground piece builds.

    python tools/villages/plan.py spire_a          plan one layout and preview it
"""
import heapq
import math
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'buildings'))
import kit  # noqa: E402

# Facing after turning a building: its front is north at 0 quarter turns, then east, south, west.
FRONT = ['north', 'east', 'south', 'west']
STEP = {'north': (0, -1), 'east': (1, 0), 'south': (0, 1), 'west': (-1, 0)}
Y0 = 24          # layout y = 0 sits at canvas layer Y0
HEIGHT = 112     # canvas height


@dataclass
class Style:
    """Materials of a people's paths, bridges, lamps and islet surface."""
    path: str
    edge: str
    stairs: str
    rail: str
    lamp_post: str
    lamp_top: str
    lamp_height: int
    surface: str = 'end_stone'
    apron: str = None
    chorus: float = 0.0          # chance per free islet cell of a planted chorus
    lamp: str = None             # decor building used as the path lamp, if catalogued
    bench: str = None


STYLES = {
    'shulkin': Style(path='purpur_block', edge='end_stone_bricks', stairs='purpur_stairs', rail='end_stone_brick_wall',
                     lamp_post='end_stone_brick_wall', lamp_top='end_rod', lamp_height=3, apron='end_stone_bricks',
                     chorus=0.006, lamp='decor_spire_lamp', bench='decor_spire_bench'),
    'chorrin': Style(path='end_stone_bricks', edge='end_stone_bricks', stairs='end_stone_brick_stairs',
                     rail='end_stone_brick_wall', lamp_post='end_stone_brick_wall', lamp_top='pearlescent_froglight',
                     lamp_height=2, chorus=0.02, lamp='decor_stead_lamp', bench='decor_stead_bench'),
    'court': Style(path='polished_blackstone_bricks', edge='obsidian', stairs='polished_blackstone_brick_stairs',
                   rail='polished_blackstone_brick_wall', lamp_post='polished_blackstone_brick_wall', lamp_top='end_rod',
                   lamp_height=3, apron='obsidian', lamp='decor_court_lamp'),
}


@dataclass
class Program:
    """What a village is made of and how it spreads.

    ``plaza``: the centre building. ``buildings``: (name, people) in placement order (big and
    civic first). ``gap``: (min, max) blocks of void/land between neighbouring islets.
    ``tiers``: islet tops a building may sit at (relative to the plaza). ``merge``: join islets
    into one island along the paths (Steads) instead of bridging them (Spires)."""
    kind: str
    plaza: str
    people: str
    buildings: list
    gap: tuple = (4, 8)
    tiers: tuple = (0,)
    merge: bool = False
    margin: int = 2
    sides: dict = field(default_factory=dict)   # building name -> preferred angle range (radians)


@dataclass
class Plot:
    name: str
    people: str
    build: object          # the finished, turned kit.Build
    x: int                 # min corner in layout space
    z: int
    top: int               # islet top (layout y of the building's ground layer)
    turns: int
    spec: dict

    @property
    def w(self):
        return self.build.w

    @property
    def d(self):
        return self.build.d

    def rect(self, pad=0):
        return (self.x - pad, self.z - pad, self.x + self.w - 1 + pad, self.z + self.d - 1 + pad)

    def center(self):
        return (self.x + (self.w - 1) / 2, self.z + (self.d - 1) / 2)

    def door_cell(self):
        """The layout cell just outside the entrance (where the path starts)."""
        door = self.spec['door']
        lx, lz = door, -1                     # in the unturned building
        w0, d0 = self.spec['size'][0], self.spec['size'][2]
        for _ in range(self.turns):           # turn the local cell with the building
            lx, lz, w0, d0 = d0 - 1 - lz, lx, d0, w0
        return self.x + lx, self.z + lz


def overlap(a, b):
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])


@dataclass
class Islet:
    cx: float
    cz: float
    rx: float
    rz: float
    top: int
    depth: float           # underside depth at the centre
    power: float = 2.0     # 2 = an ellipse; higher is squarer (a Citadel's islet)


class Layout:
    def __init__(self, name, program, seed):
        self.name, self.program, self.rng = name, program, random.Random(seed)
        self.plots, self.islets, self.paths = [], [], []
        self.ground = {}   # (x, z) -> [top, depth]
        self.path_y = {}   # (x, z) -> deck layer of a path cell
        self.path_people = {}
        self.decor = []
        self.canvas = None

    # ------------------------------------------------------------- placing
    def make(self, name, turns):
        b = kit.make(name)
        return b.turned(turns)

    def place_plaza(self):
        p = self.program
        if p.plaza in kit.CATALOG:
            b = self.make(p.plaza, 0)
            plot = Plot(p.plaza, p.people, b, -(b.w // 2), -(b.d // 2), 0, 0, kit.CATALOG[p.plaza])
        else:  # a plain paved disc stands in for a plaza that isn't designed yet
            b = kit.Build(p.plaza, (15, 2, 15))
            b.disc(7, 0, 7, 7, STYLES.get(p.people, STYLES['shulkin']).path)
            spec = dict(name=p.plaza, people=p.people, role='plaza', size=(15, 2, 15), ground=0, residents=0, door=7)
            plot = Plot(p.plaza, p.people, b, -7, -7, 0, 0, spec)
        self.plots.append(plot)
        r = max(plot.w, plot.d) / 2 + 2.5
        self.islets.append(Islet(0, 0, r, r, 0, 6 + r * 1.1))
        return plot

    def place(self, name, people, angle, tiers):
        """Put a building on the ray at ``angle`` from the centre, as close as it fits, door toward the centre."""
        spec = kit.CATALOG[name]
        p = self.program
        gap_lo, gap_hi = p.gap
        rng = self.rng
        best = None
        for wiggle in (0, 0.12, -0.12, 0.25, -0.25, 0.4, -0.4, 0.6, -0.6):
            a = angle + wiggle
            # which side of the centre: the door must face back toward it
            dx, dz = math.cos(a), math.sin(a)
            if abs(dx) > abs(dz):
                turns = 3 if dx > 0 else 1        # east of centre: front faces west
            else:
                turns = 0 if dz > 0 else 2        # south of centre: front faces north
            w, d = (spec['size'][0], spec['size'][2]) if turns % 2 == 0 else (spec['size'][2], spec['size'][0])
            gap = rng.randint(gap_lo, gap_hi)
            for r in range(6, 140):
                cx, cz = dx * r, dz * r
                x, z = round(cx - (w - 1) / 2), round(cz - (d - 1) / 2)
                rect = (x, z, x + w - 1, z + d - 1)
                pad = gap + p.margin
                if any(overlap((rect[0] - pad, rect[1] - pad, rect[2] + pad, rect[3] + pad), o.rect()) for o in self.plots):
                    continue
                if best is None or r < best[0]:
                    best = (r, x, z, turns)
                break
        r, x, z, turns = best
        # the Lamp Tower is the village's beacon: always on one of the highest islets
        top = max(tiers) if spec.get('job') == 'lamplighter' else rng.choice(tiers)
        b = self.make(name, turns)
        plot = Plot(name, people, b, x, z, top, turns, spec)
        self.plots.append(plot)
        cx, cz = plot.center()
        rx, rz = plot.w / 2 + p.margin + 0.5, plot.d / 2 + p.margin + 0.5
        self.islets.append(Islet(cx, cz, rx, rz, top, 5 + min(rx, rz) * 1.4))
        return plot

    def place_all(self):
        p = self.program
        plaza = self.place_plaza()
        names = [(n, pp) for n, pp in p.buildings if n in kit.CATALOG]
        missing = [n for n, _ in p.buildings if n not in kit.CATALOG]
        if missing:
            print(f'  {self.name}: not designed yet, skipped: {", ".join(missing)}')
        start = self.rng.uniform(0, 2 * math.pi)
        if p.people == 'shared':
            # a Crossing: the spire quarter on one side of the market, the stead quarter on the other
            groups = [[nm for nm in names if nm[1] == 'shulkin'], [nm for nm in names if nm[1] != 'shulkin']]
            for g, group in enumerate(groups):
                for i, (name, people) in enumerate(group):
                    angle = start + math.pi * g + math.pi * (i + 0.5) / max(len(group), 1) + self.rng.uniform(-0.1, 0.1)
                    self.place(name, people, angle, p.tiers if people == 'shulkin' else (0, 0, 1))
            return plaza
        n = len(names)
        for i, (name, people) in enumerate(names):
            if name in p.sides:
                lo, hi = p.sides[name]
                angle = self.rng.uniform(lo, hi)
            else:
                angle = start + 2 * math.pi * i / max(n, 1) + self.rng.uniform(-0.15, 0.15)
            self.place(name, people, angle, p.tiers)
        return plaza

    def merge_paths(self):
        """Steads: grow land along every path so the islets join into one lumpy island."""
        for plot, path in self.paths:
            for i, cell in enumerate(path):
                if i % 2:
                    continue
                y = self.path_y[cell]
                r = 3.4 + self.rng.random() * 0.8
                self.islets.append(Islet(cell[0], cell[1], r, r, y, 3 + r * 0.6))
        self.ground = {}
        self.raster()

    # ------------------------------------------------------------- ground
    def raster(self):
        """Columns of every islet: each column belongs to the islet it is deepest inside."""
        rng = random.Random(self.rng.random())
        cells = {}
        for k, isl in enumerate(self.islets):
            for z in range(math.floor(isl.cz - isl.rz) - 1, math.ceil(isl.cz + isl.rz) + 2):
                for x in range(math.floor(isl.cx - isl.rx) - 1, math.ceil(isl.cx + isl.rx) + 2):
                    e = (abs(x - isl.cx) / isl.rx) ** isl.power + (abs(z - isl.cz) / isl.rz) ** isl.power
                    # a slightly ragged edge
                    wob = 1 + 0.12 * math.sin(x * 1.7 + z * 0.9 + k) * math.cos(z * 1.3 - x * 0.6)
                    if e <= wob:
                        if (x, z) not in cells or e < cells[(x, z)][0]:
                            cells[(x, z)] = (e, k)
        for (x, z), (e, k) in cells.items():
            isl = self.islets[k]
            # an inverted cone, rough underneath, now and then a hanging spike
            taper = (1 - min(e, 1.0) ** (1 / isl.power)) ** 0.8
            depth = 1 + isl.depth * taper * (0.8 + 0.4 * rng.random())
            if taper > 0.25 and rng.random() < 0.07:
                depth += rng.randint(2, 6)
            self.ground[(x, z)] = [isl.top, max(1, round(depth))]
        # buildings stand on their own islet's top even where another islet's edge reaches in
        for plot in self.plots:
            x0, z0, x1, z1 = plot.rect()
            for x in range(x0, x1 + 1):
                for z in range(z0, z1 + 1):
                    g = self.ground.get((x, z))
                    self.ground[(x, z)] = [plot.top, max(g[1] if g else 0, 4 + plot.top - (g[0] if g else plot.top))]

    def on_land(self, x, z):
        return (x, z) in self.ground

    def blocked(self, pad=1):
        cells = set()
        for plot in self.plots[1:]:
            x0, z0, x1, z1 = plot.rect(pad)
            for x in range(x0, x1 + 1):
                for z in range(z0, z1 + 1):
                    cells.add((x, z))
        return cells

    # ------------------------------------------------------------- paths
    def route(self, start, goal_rect, blocked):
        """A* from start to any cell inside goal_rect or onto an existing path.

        Prefers land (Steads strongly), existing paths and straight runs."""
        gx0, gz0, gx1, gz1 = goal_rect

        def h(c):
            dx = max(gx0 - c[0], 0, c[0] - gx1)
            dz = max(gz0 - c[1], 0, c[1] - gz1)
            return dx + dz

        void_cost = 3.0 if self.program.merge else 1.3
        open_ = [(h(start), 0.0, start, None)]
        came_from, cost, seen = {}, {(start, None): 0.0}, set()
        while open_:
            f, g, cell, d = heapq.heappop(open_)
            if (cell, d) in seen:
                continue
            seen.add((cell, d))
            if (gx0 <= cell[0] <= gx1 and gz0 <= cell[1] <= gz1) or (cell in self.path_y and cell != start):
                path, key = [cell], (cell, d)
                while key in came_from:
                    key = came_from[key]
                    path.append(key[0])
                return path[::-1]
            if g > 400:
                continue
            for nd, (dx, dz) in STEP.items():
                n = (cell[0] + dx, cell[1] + dz)
                if n in blocked:
                    continue
                step = 1.0 if self.on_land(*n) else void_cost
                if d is not None and nd != d:
                    step += 0.6
                ng = g + step
                key = (n, nd)
                if ng < cost.get(key, 1e9):
                    cost[key] = ng
                    came_from[key] = (cell, d)
                    heapq.heappush(open_, (ng + h(n), ng, n, nd))
        return None

    def lay_paths(self):
        p = self.program
        plaza = self.plots[0]
        goal = plaza.rect(-1)
        width = 3
        for plot in self.plots[1:]:
            if plot.spec.get('role') in ('decor', 'wall', 'gate'):
                continue
            blocked = self.blocked(1)
            start = plot.door_cell()
            # free the doorstep and the cells in front of the door
            fx, fz = STEP[FRONT[plot.turns]]
            for k in range(0, 3):
                for s in (-1, 0, 1):
                    c = (start[0] + fx * k + (fz != 0) * s, start[1] + fz * k + (fx != 0) * s)
                    blocked.discard(c)
            for c in list(self.path_y):
                blocked.discard(c)
            path = self.route(start, goal, blocked)
            if path is None:
                print(f'  {self.name}: no path from {plot.name}')
                continue
            self.paths.append((plot, path))
            self.set_heights(plot, path)

    def set_heights(self, plot, path):
        """Deck heights from the door (the plot's islet top) to the end of the path, one step at a time."""
        end = path[-1]
        y_end = self.path_y.get(end, 0)
        y0 = plot.top
        n = len(path)
        # cells already part of another path keep their height; ramp only over the new cells
        new = [c for c in path if c not in self.path_y]
        m = max(len(new) - 1, 1)
        rise = y_end - y0
        steps = min(abs(rise), m)
        i = 0
        for c in path:
            if c in self.path_y:
                continue
            # spread the steps along the run, flat for the first and last two cells
            t = 0 if m <= 4 else max(0.0, min(1.0, (i - 2) / max(m - 4, 1)))
            y = y0 + round(math.copysign(steps, rise) * t) if rise else y0
            self.path_y[c] = y
            self.path_people[c] = plot.people if self.program.people == 'shared' else self.program.people
            i += 1

    # ------------------------------------------------------------- drawing
    def draw(self):
        xs = [x for x, z in self.ground] + [c[0] for c in self.path_y]
        zs = [z for x, z in self.ground] + [c[1] for c in self.path_y]
        for plot in self.plots:
            x0, z0, x1, z1 = plot.rect()
            xs += [x0, x1]
            zs += [z0, z1]
        self.minx, self.minz = min(xs) - 3, min(zs) - 3
        W, D = max(xs) - self.minx + 4, max(zs) - self.minz + 4
        c = self.canvas = kit.Build(self.name, (W, HEIGHT, D))
        ox, oz = -self.minx, -self.minz
        rng = random.Random(self.rng.random())
        people = self.program.people

        def style_at(x, z):
            pp = self.path_people.get((x, z), people)
            return STYLES['shulkin' if pp == 'shared' else pp]

        # islet surface
        for (x, z), (top, depth) in self.ground.items():
            st = style_at(x, z)
            c.set(x + ox, top + Y0, z + oz, st.surface)
        # aprons round buildings
        for plot in self.plots[1:]:
            st = STYLES.get(plot.people if plot.people != 'shared' else 'shulkin')
            if st and st.apron:
                x0, z0, x1, z1 = plot.rect(1)
                for x in range(x0, x1 + 1):
                    for z in range(z0, z1 + 1):
                        if (x, z) in self.ground and self.ground[(x, z)][0] == plot.top and not (
                                plot.x <= x < plot.x + plot.w and plot.z <= z < plot.z + plot.d):
                            c.set(x + ox, plot.top + Y0, z + oz, st.apron)
        # paths, three wide, with stairs where the deck steps and rails where it crosses the void
        deck = {}
        for plot, path in self.paths:
            for i, cell in enumerate(path):
                y = self.path_y[cell]
                nxt = path[min(i + 1, len(path) - 1)]
                prv = path[max(i - 1, 0)]
                dx, dz = nxt[0] - prv[0], nxt[1] - prv[1]
                along = 'x' if abs(dx) >= abs(dz) else 'z'
                sides = [(0, 0), (0, -1), (0, 1)] if along == 'x' else [(0, 0), (-1, 0), (1, 0)]
                for k, (sx, sz) in enumerate(sides):
                    cell2 = (cell[0] + sx, cell[1] + sz)
                    if cell2 in deck and deck[cell2][0] >= y and k:
                        continue
                    deck[cell2] = (y, k == 0, cell, along)
        plaza_rect = self.plots[0].rect()
        for (x, z), (y, centre, owner, along) in deck.items():
            if plaza_rect[0] <= x <= plaza_rect[2] and plaza_rect[1] <= z <= plaza_rect[3]:
                continue
            if any(p.x <= x < p.x + p.w and p.z <= z < p.z + p.d for p in self.plots[1:]):
                continue
            st = style_at(*owner)
            c.set(x + ox, y + Y0, z + oz, st.path if centre else st.edge)
            for k in (1, 2, 3):
                c.set(x + ox, y + Y0 + k, z + oz, 'air')
            land = self.ground.get((x, z))
            g_top = land[0] if land else None
            if land is None or g_top != y:
                # the deck owns this column now: an embankment down to its islet, or a bridge deck over the void
                if land is None:
                    self.ground[(x, z)] = [y, 0]
                else:
                    self.ground[(x, z)] = [y, max(0, y - g_top) + land[1]]
        # steps: where a deck cell is one higher than the cell before it along the path
        for plot, path in self.paths:
            for i in range(1, len(path)):
                a, b = path[i - 1], path[i]
                ya, yb = self.path_y[a], self.path_y[b]
                if ya == yb:
                    continue
                lo, hi = (a, b) if ya < yb else (b, a)
                y_lo = min(ya, yb)
                facing = {(1, 0): 'east', (-1, 0): 'west', (0, 1): 'south', (0, -1): 'north'}[(hi[0] - lo[0], hi[1] - lo[1])]
                st = style_at(*lo)
                along = 'x' if hi[0] != lo[0] else 'z'
                for s in (-1, 0, 1):
                    cx_, cz_ = (lo[0], lo[1] + s) if along == 'x' else (lo[0] + s, lo[1])
                    if (cx_, cz_) in deck and deck[(cx_, cz_)][0] == y_lo:
                        c.set(cx_ + ox, y_lo + 1 + Y0, cz_ + oz, st.stairs, facing=facing, half='bottom')
        # rails just outside deck edges that face the void, on a ledge of the deck's edge block
        self.rails = {}
        for (x, z), (y, centre, owner, along) in deck.items():
            if plaza_rect[0] <= x <= plaza_rect[2] and plaza_rect[1] <= z <= plaza_rect[3]:
                continue
            if any(p.x <= x < p.x + p.w and p.z <= z < p.z + p.d for p in self.plots[1:]):
                continue
            st = style_at(*owner)
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, z + dz)
                if n in deck or n in self.ground or n in self.rails:
                    continue
                if any(p.x - 1 <= n[0] <= p.x + p.w and p.z - 1 <= n[1] <= p.z + p.d for p in self.plots):
                    continue
                c.set(n[0] + ox, y + Y0, n[1] + oz, st.edge)
                c.set(n[0] + ox, y + Y0 + 1, n[1] + oz, st.rail)
                self.rails[n] = y
        self.deck = deck
        # buildings
        for plot in self.plots:
            c.paste(plot.build, plot.x + ox, plot.top + Y0 - plot.build.ground, plot.z + oz)
        # lamps along the paths, and chorus on free ground
        self.lamps(ox, oz)
        self.planting(ox, oz, rng)

    def free(self, x, z):
        if (x, z) in self.deck:
            return False
        for p in self.plots:
            x0, z0, x1, z1 = p.rect(1)
            if x0 <= x <= x1 and z0 <= z <= z1:
                return False
        return (x, z) in self.ground

    def lamps(self, ox, oz):
        c = self.canvas
        placed = []
        for plot, path in self.paths:
            for i in range(3, len(path) - 2, 7):
                cell = path[i]
                y = self.path_y[cell]
                prv, nxt = path[i - 1], path[i + 1]
                along = 'x' if nxt[0] != prv[0] else 'z'
                for s in (2, -2):
                    x, z = (cell[0], cell[1] + s) if along == 'x' else (cell[0] + s, cell[1])
                    if any(abs(x - a) + abs(z - b) < 5 for a, b in placed):
                        continue
                    st = STYLES['shulkin' if self.path_people.get(cell, self.program.people) == 'shared'
                                else self.path_people.get(cell, self.program.people)]
                    if self.free(x, z) and self.ground[(x, z)][0] == y:
                        self.lamp(st, x + ox, y + Y0 + 1, z + oz)
                        placed.append((x, z))
                        break
                    if self.rails.get((x, z)) == y:
                        # on a bridge: a lamp on the rail
                        c.set(x + ox, y + Y0 + 2, z + oz, st.lamp_top, **({'facing': 'up'} if st.lamp_top == 'end_rod' else {}))
                        placed.append((x, z))
                        break

    def lamp(self, st, x, y, z):
        c = self.canvas
        if st.lamp and st.lamp in kit.CATALOG:
            b = kit.make(st.lamp)
            c.paste(b, x - b.w // 2, y - 1 - b.ground, z - b.d // 2)
            return
        for k in range(st.lamp_height):
            c.set(x, y + k, z, st.lamp_post)
        top = st.lamp_top
        c.set(x, y + st.lamp_height, z, top, **({'facing': 'up'} if top == 'end_rod' else {}))

    def planting(self, ox, oz, rng):
        c = self.canvas
        for (x, z), (top, depth) in sorted(self.ground.items()):
            if depth == 0 or not self.free(x, z):
                continue
            st = STYLES['shulkin' if self.program.people == 'shared' else self.program.people]
            if rng.random() >= st.chorus:
                continue
            if any(not self.free(x + dx, z + dz) for dx in (-1, 0, 1) for dz in (-1, 0, 1)):
                continue
            if c.get(x + ox, top + Y0, z + oz)[0] != 'minecraft:end_stone':
                continue
            if any(c.solid(x + ox + dx, top + Y0 + k, z + oz + dz) for dx in (-1, 0, 1) for dz in (-1, 0, 1) for k in (1, 2, 3)):
                continue
            c.chorus(x + ox, top + Y0 + 1, z + oz, height=rng.randint(2, 5), rng=rng)

    # ------------------------------------------------------------- results
    def finish(self):
        self.canvas.finish()
        return self

    def residents(self):
        return sum(p.spec.get('residents', 0) for p in self.plots)


def plan(name, program, seed):
    lay = Layout(name, program, seed)
    lay.place_all()
    lay.raster()
    lay.lay_paths()
    if program.merge:
        lay.merge_paths()
    lay.draw()
    return lay.finish()

