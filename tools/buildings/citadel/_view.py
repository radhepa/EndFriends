"""Development previews for the Citadel on a light background (obsidian vanishes on the default one).

  python tools/buildings/citadel/_view.py gate_of_eyes [--cut N]   -> out/_court_<name>.png
  python tools/buildings/citadel/_view.py gate_of_eyes --front     straight-on N/S/W/E views + top cutaway
  python tools/buildings/citadel/_view.py --joint tower|gate       joint close-ups (try --cut 11)
  python tools/buildings/citadel/_view.py --square 5               a closed square wall, 5 tiles a side
  python tools/buildings/citadel/_view.py --line 2                 one wall line with the gate

Uses ``preview.py`` unchanged (it only swaps the page's background and, for tall pieces, the
camera aim at run time).
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


def _page():
    import preview
    return preview, preview.PAGE.replace('#1d1828', '#9ea6b8').replace('0x1d1828', '0x9ea6b8')


def render_build(b, out_png, cut=None, label=None, views=None):
    import look
    preview, page = _page()
    if b.h > 1.6 * max(b.w, b.d):
        # tall pieces: aim higher and stand back so the top is in frame
        page = page.replace('const ty = sy * 0.38;', 'const ty = sy * 0.5;').replace(
            'const r = Math.max(sx, sz, sy * 0.9) * 0.9 + 4;', 'const r = Math.max(sx, sz, sy * 1.15) * 0.9 + 4;')
    if views:
        page = page.replace('const VIEWS = [[-35, 28, 0], [35, 28, 0], [145, 28, 0], [215, 28, 0], [-35, 62, 1]];',
                            'const VIEWS = ' + views + ';')
    c = b.ground + 3 if cut is None else cut
    items = [{'name': label or b.name, 'full': look.export(b), 'cut': look.export(b, cut=c), 'info': preview.info(b)}]
    html = (page.replace('__THREE__', preview.THREE)
            .replace('__VIEWER__', (HERE / 'viewer.js').read_text(encoding='utf-8'))
            .replace('__ITEMS__', json.dumps(items)))
    return preview.shoot(html, str(out_png), (1500, 900))


def wall_line(n_side=2):
    """NW tower, 2 walls, the gate, 2 walls, NE tower; then the west side going south."""
    import kit
    kit.load_all()
    tower = kit.make('citadel_tower')
    wall = kit.make('citadel_wall')
    gate = kit.make('gate_of_eyes')
    length = 11 + n_side * 9 + gate.w + n_side * 9 + 11
    depth = 11 + n_side * 9 + 2
    v = kit.Build('wall_line', (length, max(tower.h, gate.h) + 2, depth))
    v.paste(tower, 0, 0, 0)
    x = 11
    for _ in range(n_side):
        v.paste(wall, x, 0, 3)
        x += 9
    v.paste(gate, x, 0, 0)
    x += gate.w
    for _ in range(n_side):
        v.paste(wall, x, 0, 3)
        x += 9
    v.paste(tower, x, 0, 0, turns=1)
    # west side going south from the NW tower, and east side from the NE tower
    z = 11
    for _ in range(n_side):
        v.paste(wall, 3, 0, z, turns=3)
        v.paste(wall, x + 3, 0, z, turns=1)
        z += 9
    v.finish()
    return v


def square(k=5):
    """A closed square Citadel wall, k tiles per side, the gate (3 tiles) centred in the north side.

    Every piece shares one rule: a side's wall profile sits 3 cells in from the tower's outer face."""
    import kit
    kit.load_all()
    tower = kit.make('citadel_tower')
    wall = kit.make('citadel_wall')
    gate = kit.make('gate_of_eyes')
    side = 22 + 9 * k
    v = kit.Build('square', (side, max(tower.h, gate.h), side))
    far = side - 11
    v.paste(tower, 0, 0, 0)                 # NW
    v.paste(tower, far, 0, 0, turns=1)      # NE
    v.paste(tower, far, 0, far, turns=2)    # SE
    v.paste(tower, 0, 0, far, turns=3)      # SW
    left = (k - 3) // 2
    i = 0
    while i < k:
        x = 11 + 9 * i
        if i == left:
            v.paste(gate, x, 0, 0)
            i += 3
            continue
        v.paste(wall, x, 0, 3)                               # north, outside north
        i += 1
    for i in range(k):
        t = 11 + 9 * i
        v.paste(wall, t, 0, far + 3, turns=2)                # south, outside south
        v.paste(wall, 3, 0, t, turns=3)                      # west, outside west
        v.paste(wall, far + 3, 0, t, turns=1)                # east, outside east
    v.finish()
    return v


def joints(which):
    """Close-ups of the joints: 'tower' = the NW tower with one wall each way; 'gate' = the gate between walls."""
    import kit
    kit.load_all()
    tower = kit.make('citadel_tower')
    wall = kit.make('citadel_wall')
    gate = kit.make('gate_of_eyes')
    if which == 'tower':
        v = kit.Build('joint_tower', (20, tower.h, 20))
        v.paste(tower, 0, 0, 0)
        v.paste(wall, 11, 0, 3)
        v.paste(wall, 3, 0, 11, turns=3)
    else:
        v = kit.Build('joint_gate', (9 + gate.w + 9, gate.h, gate.d))
        v.paste(wall, 0, 0, 3)
        v.paste(gate, 9, 0, 0)
        v.paste(wall, 9 + gate.w, 0, 3)
    v.finish()
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--joint', choices=('tower', 'gate'))
    ap.add_argument('--square', type=int, default=0, help='closed square wall with N tiles per side')
    ap.add_argument('names', nargs='*')
    ap.add_argument('--cut', type=int)
    ap.add_argument('--line', type=int, default=0, help='wall line test with N segments per run')
    ap.add_argument('--front', action='store_true', help='straight-on views: north, south, west, east, top')
    ap.add_argument('--views', help='JSON list of [azimuth, elevation, cutaway 0/1] (5 views)')
    args = ap.parse_args()
    import kit
    kit.load_all()
    out_dir = HERE / 'out'
    views = '[[0, 8, 0], [180, 8, 0], [-90, 8, 0], [90, 8, 0], [0, 89, 1]]' if args.front else args.views
    tag = '_front' if args.front else '_views' if args.views else ''
    if args.square:
        print(render_build(square(args.square), out_dir / f'_court_square{tag}.png', cut=args.cut, views=views))
    if args.joint:
        print(render_build(joints(args.joint), out_dir / f'_court_joint_{args.joint}{tag}.png', cut=args.cut, views=views))
    if args.line:
        print(render_build(wall_line(args.line), out_dir / f'_court_wall_line{tag}.png', cut=args.cut, views=views))
    for n in args.names:
        print(render_build(kit.make(n), out_dir / f'_court_{n}{tag}.png', cut=args.cut, views=views))


if __name__ == '__main__':
    main()
