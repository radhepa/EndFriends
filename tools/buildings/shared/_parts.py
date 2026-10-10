"""Shared pieces for the Crossing buildings and the street decor, plus development checks.

  python tools/buildings/shared/_parts.py [names...]     light + support report (default: all of mine)

Chorus: ``grow()`` draws planted chorus the way vanilla grows it. A chorus plant cell that has chorus
(or anything) both above and below it may NOT have a chorus plant beside it, so a stalk only branches
from its top cell; the branch steps sideways over air and climbs from there. ``kit.Build.chorus()``
branches from the middle of a stalk, which vanilla breaks on the first neighbour update, so these
buildings use ``grow()`` instead.

Support: ``check_support()`` applies the vanilla survival rules of everything that pops off when
unsupported (chorus, lanterns, candles, carpets, doors, banners, signs, ladders), so nothing breaks the
first time a block next to it changes in the world.

Light: no sky light in the End, so any walkable cell at block light 0 lets Endermen spawn.
``light_report()`` floods block light through the build and lists dark walkable cells.
"""
import random
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import kit  # noqa: E402
from kit import DIRS, bid, props, is_air, full_cube  # noqa: E402

ES, ESB = 'end_stone', 'end_stone_bricks'
ESB_STAIRS, ESB_SLAB, ESB_WALL = 'end_stone_brick_stairs', 'end_stone_brick_slab', 'end_stone_brick_wall'
PB, PP, P_STAIRS, P_SLAB = 'purpur_block', 'purpur_pillar', 'purpur_stairs', 'purpur_slab'
BACK = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
CW = {'north': 'east', 'east': 'south', 'south': 'west', 'west': 'north'}
CCW = {v: k for k, v in CW.items()}
ROTATION = {'south': 0, 'west': 4, 'north': 8, 'east': 12}


def toward(dx, dz):
    """Compass direction of the larger component of (dx, dz)."""
    if abs(dx) >= abs(dz):
        return 'east' if dx > 0 else 'west'
    return 'south' if dz > 0 else 'north'


# ------------------------------------------------------------------ chorus
def grow(b, x, y, z, h, branches=(), flower=True, age=5):
    """Planted chorus from (x, y, z): a stalk ``h`` cells tall; at its top it either flowers or branches.

    ``branches``: (direction, height, sub_branches) tuples. A branch's first cell is the sideways step at
    the top cell's level (it counts in ``height``), then it climbs. Flowers default to age 5 (fully grown)
    so the planting keeps its shape instead of creeping over roofs and paths."""
    for k in range(h):
        b.set(x, y + k, z, 'chorus_plant')
    top = y + h - 1
    if branches:
        for direction, h2, sub in branches:
            dx, dz = DIRS[direction]
            grow(b, x + dx, top, z + dz, h2, sub, flower, age)
    elif flower:
        b.set(x, top + 1, z, 'chorus_flower', age=age)


def _is(b, pos, name):
    return b.get(*pos)[0] == 'minecraft:' + name


def _ground(b, x, y, z):
    """The block at a cell; undrawn cells on or below the ground layer count as the islet's end stone."""
    s = b.grid.get((x, y, z))
    if s is None and y <= b.ground:
        return ('minecraft:end_stone', ())
    return s if s is not None else kit.AIR


def chorus_ok(b, x, y, z):
    """Vanilla ChorusPlantBlock / ChorusFlowerBlock.canSurvive."""
    s = b.get(x, y, z)
    below = _ground(b, x, y - 1, z)
    if s[0] == 'minecraft:chorus_plant':
        sandwiched = not is_air(_ground(b, x, y + 1, z)) and not is_air(below)
        for dx, dz in DIRS.values():
            side = (x + dx, y, z + dz)
            if _is(b, side, 'chorus_plant'):
                if sandwiched:
                    return False
                sb = _ground(b, x + dx, y - 1, z + dz)
                if bid(sb) in ('chorus_plant', 'end_stone'):
                    return True
        return bid(below) in ('chorus_plant', 'end_stone')
    if s[0] == 'minecraft:chorus_flower':
        if bid(below) in ('chorus_plant', 'end_stone'):
            return True
        if not is_air(below):
            return False
        found = False
        for dx, dz in DIRS.values():
            n = _ground(b, x + dx, y, z + dz)
            if bid(n) == 'chorus_plant':
                if found:
                    return False
                found = True
            elif not is_air(n):
                return False
        return found
    return True


# ------------------------------------------------------------------ support rules
def _face_full_up(s):
    """The top face is a full square (doors, standing banners need a sturdy floor)."""
    if is_air(s):
        return False
    name, p = bid(s), props(s)
    if name.endswith('_slab'):
        return p.get('type') in ('top', 'double')
    if name.endswith('_stairs'):
        return p.get('half') == 'top'
    return full_cube(s)


def _face_full_down(s):
    if is_air(s):
        return False
    name, p = bid(s), props(s)
    if name.endswith('_slab'):
        return p.get('type') in ('bottom', 'double')
    if name.endswith('_stairs'):
        return p.get('half', 'bottom') == 'bottom'
    return full_cube(s)


def _center_up(s):
    """Block.canSupportCenter(.., UP): candles and standing lanterns."""
    name = bid(s) if not is_air(s) else ''
    return _face_full_up(s) or name.endswith(('_wall', '_fence', 'glass_pane')) or name in (
        'iron_bars', 'iron_chain', 'end_rod', 'lightning_rod')


def _center_down(s):
    """Block.canSupportCenter(.., DOWN): hanging lanterns and ceiling hanging signs."""
    name = bid(s) if not is_air(s) else ''
    return _face_full_down(s) or name.endswith(('_wall', '_fence', 'glass_pane')) or name in (
        'iron_bars', 'iron_chain', 'end_rod', 'lightning_rod')


def _solid(s):
    """BlockState.isSolid() (legacy solid), roughly: things with a big collision box."""
    if is_air(s):
        return False
    name = bid(s)
    if name.endswith(('_carpet', '_button', '_pressure_plate', '_sign', '_banner', 'candle', 'lantern', '_rod',
                      '_door', '_trapdoor')):
        return False
    return name not in ('chorus_plant', 'chorus_flower', 'iron_chain', 'ladder', 'flower_pot', 'end_rod') \
        and not name.startswith('potted_')


def check_support(b):
    """Every block that vanilla pops off when unsupported, checked against its neighbours."""
    bad = []
    for (x, y, z), s in b.grid.items():
        name, p = bid(s), props(s)
        below = _ground(b, x, y - 1, z)
        above = b.get(x, y + 1, z)
        ok = True
        if name in ('chorus_plant', 'chorus_flower'):
            ok = chorus_ok(b, x, y, z)
        elif name in ('lantern', 'soul_lantern') or name.endswith('copper_lantern'):
            ok = _center_down(above) if p.get('hanging') == 'true' else _center_up(below)
        elif name.endswith('candle'):
            ok = _center_up(below)
        elif name.endswith('_carpet'):
            ok = not is_air(below)
        elif name.endswith('_door') and p.get('half') == 'lower':
            ok = _face_full_up(below)
        elif name.endswith(('_wall_banner', '_wall_sign')) or name == 'ladder':
            dx, dz = DIRS[p.get('facing', 'north')]
            ok = _solid(b.get(x - dx, y, z - dz))
        elif name.endswith('_banner'):
            ok = _solid(below)
        elif name.endswith('_hanging_sign') and 'wall' not in name:
            ok = _center_down(above)
        if not ok:
            bad.append(f'{name} at {(x, y, z)}')
    return bad


# ------------------------------------------------------------------ light
EMIT = {'end_rod': 14, 'crying_obsidian': 10, 'lantern': 15, 'soul_lantern': 10, 'sea_lantern': 15,
        'glowstone': 15, 'end_gateway': 15, 'end_portal_frame': 1, 'brewing_stand': 1, 'campfire': 15,
        'soul_campfire': 10, 'pearlescent_froglight': 15, 'ochre_froglight': 15, 'verdant_froglight': 15,
        'shroomlight': 15, 'copper_lantern': 15, 'enchanting_table': 7}


def emission(s):
    name, p = bid(s), props(s)
    if name.endswith('candle'):
        return 3 * int(p.get('candles', 1)) if p.get('lit') == 'true' else 0
    if name.endswith('campfire') and p.get('lit') == 'false':
        return 0
    return EMIT.get(name, 0)


def opaque(s):
    if is_air(s):
        return False
    name = bid(s)
    if 'glass' in name and name != 'tinted_glass':
        return False
    if name.endswith(('_stairs', '_slab')):
        return True  # conservative: light really leaks round them
    return full_cube(s)


def light_map(b, pad=3):
    level, q = {}, deque()
    for pos, s in b.grid.items():
        e = emission(s)
        if e:
            level[pos] = e
            q.append(pos)
    while q:
        x, y, z = q.popleft()
        v = level[(x, y, z)] - 1
        if v <= 0:
            continue
        for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            n = (x + d[0], y + d[1], z + d[2])
            if not (-pad <= n[0] < b.w + pad and -pad <= n[1] < b.h + pad and -pad <= n[2] < b.d + pad):
                continue
            if opaque(_ground(b, *n)) or level.get(n, 0) >= v:
                continue
            level[n] = v
            q.append(n)
    return level


def walkable(b, x, y, z):
    """An air cell a mob could stand in: open here and above, a full top face below."""
    here = b.get(x, y, z)
    if not (is_air(here) or bid(here).endswith(('_pressure_plate', '_button')) or bid(here) == 'end_rod'):
        return False
    if not is_air(b.get(x, y + 1, z)) and full_cube(b.get(x, y + 1, z)):
        return False
    return _face_full_up(_ground(b, x, y - 1, z))


def light_report(b, inset=0):
    """(darkest walkable cell level, list of dark cells) over the footprint shrunk by ``inset``."""
    level = light_map(b)
    dark, worst = [], 99
    for x in range(inset, b.w - inset):
        for z in range(inset, b.d - inset):
            for y in range(b.ground + 1, b.h):
                if walkable(b, x, y, z):
                    v = level.get((x, y, z), 0)
                    worst = min(worst, v)
                    if v == 0:
                        dark.append((x, y, z))
    return worst, dark


# ------------------------------------------------------------------ reach and headroom
def _open(s):
    """Can a body pass through this cell?"""
    if is_air(s):
        return True
    return bid(s).endswith(('_door', '_carpet', '_pressure_plate', '_button', '_sign', '_banner'))


def _low(s):
    """A bottom slab or bottom stair: you stand on it half a block up, inside its cell."""
    name, p = bid(s), props(s)
    return (name.endswith('_slab') and p.get('type') == 'bottom') or (name.endswith('_stairs') and p.get('half') == 'bottom')


def _feet(b, x, y, z):
    """Feet height (in half blocks) of someone standing in column (x, z) at layer y, or None."""
    if y <= 0 or y > b.h + 1:
        return None
    here = _ground(b, x, y, z)
    if _low(here):
        return 2 * y + 1
    if _open(here) and not _open(_ground(b, x, y - 1, z)) and not _low(_ground(b, x, y - 1, z)):
        return 2 * y
    return None


def headroom(b, x, y, z):
    """Clear blocks above the feet of someone standing at (x, y, z)."""
    f = _feet(b, x, y, z)
    if f is None:
        return 0
    start = y + 1 if f % 2 else y      # from a half step, count the whole blocks above the step
    n = 0
    while start + n < b.h + 4 and _open(b.get(x, start + n, z)):
        n += 1
    return n


def reach(b, start, tall=3):
    """Cells reachable on foot from ``start`` (x, y, z) by a body ``tall`` blocks high (steps of half or
    one block, no ladders)."""
    seen, q = {start}, deque([start])
    while q:
        x, y, z = q.popleft()
        f0 = _feet(b, x, y, z)
        for dx, dz in DIRS.values():
            for dy in (0, 1, -1):
                n = (x + dx, y + dy, z + dz)
                if n in seen or not (-1 <= n[0] <= b.w and -1 <= n[2] <= b.d):
                    continue
                f1 = _feet(b, *n)
                if f1 is None or abs(f1 - f0) > 2:
                    continue
                if headroom(b, *n) < tall:
                    continue
                seen.add(n)
                q.append(n)
    return seen


def reach_report(b, starts, tall=3):
    """Spots (sleep/work/stand) that can't be reached from ``starts`` with ``tall`` headroom."""
    seen = set()
    for s in starts:
        seen |= reach(b, s, tall)
    bad = []
    for spot in b.meta.get('spots', []):
        if spot['kind'] == 'sit':
            continue
        p = tuple(spot['pos'])
        if p not in seen:
            bad.append(f"{spot['kind']} {p} (headroom {headroom(b, *p)})")
    return bad


# ------------------------------------------------------------------ signs and banners
def hanging_sign(b, x, y, z, lines, facing='north', wood='crimson', glowing=True, color='white', back=None):
    """A ceiling hanging sign (hangs from the block above). Text on both faces unless ``back`` is given."""
    text = (list(lines) + [''] * 4)[:4]
    back_text = (list(back if back is not None else lines) + [''] * 4)[:4]
    nbt = {'id': 'minecraft:hanging_sign',
           'front_text': {'messages': text, 'color': color, 'has_glowing_text': bool(glowing)},
           'back_text': {'messages': back_text, 'color': color, 'has_glowing_text': bool(glowing)},
           'is_waxed': True}
    b.set(x, y, z, f'{wood}_hanging_sign', nbt=nbt, rotation=ROTATION[facing], attached=False, waterlogged=False)


# The Eye of the Spires (Shulkin) and the Grove Knot (Chorrin) as banner patterns.
EYE_OF_THE_SPIRES = [('rhombus', 'white'), ('circle', 'magenta'), ('border', 'magenta'), ('triangles_bottom', 'magenta')]
GROVE_KNOT = [('flower', 'purple'), ('curly_border', 'brown')]


def banner(b, x, y, z, base='purple', patterns=EYE_OF_THE_SPIRES, facing='north', wall=False):
    """A banner (1.20.5+ block entity format: patterns = [{pattern, color}]).

    Standing: ``facing`` is the side its face shows to. Wall: hangs on the block behind it."""
    nbt = {'id': 'minecraft:banner',
           'patterns': [{'pattern': 'minecraft:' + pat, 'color': col} for pat, col in patterns]}
    if wall:
        b.set(x, y, z, f'{base}_wall_banner', nbt=nbt, facing=facing)
    else:
        b.set(x, y, z, f'{base}_banner', nbt=nbt, rotation=ROTATION[facing])


# ------------------------------------------------------------------ dev report
MINE = ('crossing', 'shared')


def report(names=None):
    catalog = kit.load_all()
    if not names:
        names = [n for n, s in catalog.items() if s['fn'].__module__.split('.')[0] in MINE]
    ok = True
    for n in names:
        b = kit.make(n)
        worst, dark = light_report(b)
        bad = check_support(b)
        spots = b.meta.get('spots', [])
        kinds = {k: sum(1 for s in spots if s['kind'] == k) for k in ('sleep', 'work', 'sit', 'stand')}
        spec = catalog[n]
        start = (spec['door'], b.ground + 1, -1)
        far = reach_report(b, [start]) if spec['role'] in ('civic', 'work', 'home', 'plaza') else []
        print(f'{n:26s} {b.w}x{b.h}x{b.d}  min light {worst if worst != 99 else "-":>2}  dark {len(dark):3d}  '
              f'unsupported {len(bad)}  unreachable {len(far)}  spots {kinds}')
        for cell in dark[:12]:
            print('    dark', cell)
        for msg in bad[:12]:
            print('    unsupported', msg)
        for msg in far:
            print('    unreachable (3 high)', msg)
        ok = ok and not dark and not bad and not far
    return ok


if __name__ == '__main__':
    sys.exit(0 if report(sys.argv[1:]) else 1)
