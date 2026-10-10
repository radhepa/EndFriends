"""Build the villages design page: every building, one planned village per kind, game screenshots.

  python tools/villages/compile.py --preview          (plans the villages, writes tools/villages/out/*.json)
  python tools/design/build_villages_page.py <out.html>

Screenshots come from the last game test run (build/run/clientGameTest/screenshots/end-*.png).
"""
import base64
import io
import json
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / 'tools' / 'buildings'))
import kit  # noqa: E402
import look  # noqa: E402

VILLAGES = {'spire': 'spire_a', 'stead': 'stead_a', 'crossing': 'crossing_a', 'citadel': 'citadel_a'}
KIND_OF = {'spire': 'spire', 'stead': 'stead', 'crossing': 'crossing', 'citadel': 'citadel'}
TITLES = {
    'lamp_court': 'Lamp Court', 'lid_hall': 'Lid Hall', 'archive': 'Archive', 'lamp_tower': 'Lamp Tower',
    'shell_nursery': 'Shell Nursery', 'weavers_loft': "Weaver's Loft", 'shellwright': "Shellwright's Workshop",
    'driftray_roost': 'Driftray Roost', 'spire_home': 'Spire home', 'spire_home_tall': 'Tall spire home',
    'spire_twin': 'Twin spires', 'hum_circle': 'Hum Circle', 'popping_kiln': 'Popping Kiln',
    'grove_terraces': 'Grove Terraces', 'groveback_pen': 'Groveback Pen', 'brewhouse': 'Brewhouse',
    'stonecutters_yard': "Stonecutter's Yard", 'cooks_hearth': "Cook's Hearth", 'blinkers_post': "Blinker's Post",
    'dome_home': 'Dome home', 'dome_home_large': 'Large dome home', 'dome_pair': 'Paired domes',
    'market': 'The Market', 'crossing_hall': 'Crossing Hall', 'trade_stall': 'Trade stall',
    'trade_stall_awning': 'Awning stall', 'gate_of_eyes': 'Gate of Eyes', 'citadel_wall': 'Citadel wall',
    'citadel_tower': 'Citadel tower', 'throne_hall': 'Throne Hall', 'lords_spire': "The Lord's Spire",
    'war_hall': 'War Hall', 'riftguard_barracks': 'Riftguard Barracks', 'seers_spire': "Seers' Spire",
    'thrall_yards': 'Thrall Yards', 'voidhound_kennels': 'Voidhound Kennels',
}
ORDER = ['plaza', 'gate', 'civic', 'work', 'home', 'wall', 'decor']


def title(name):
    return TITLES.get(name) or name.replace('decor_', '').replace('_', ' ').capitalize()


def pack(blocks):
    return base64.b64encode(struct.pack(f'<{len(blocks)}h', *blocks)).decode()


def buildings():
    out = []
    catalog = kit.load_all()
    for name, spec in catalog.items():
        b = kit.make(name)
        data = look.export(b, cull=False)
        out.append({
            'name': name, 'title': title(name), 'people': 'decor' if spec['role'] == 'decor' else spec['people'],
            'role': spec['role'], 'job': spec.get('job'), 'size': list(spec['size']), 'ground': spec.get('ground', 0),
            'residents': spec.get('residents', 0), 'about': spec.get('about', ''),
            'blocks': sum(1 for s in b.grid.values() if not kit.is_air(s)),
            'vox': {'size': data['size'], 'palette': data['palette'], 'blocks': pack(data['blocks'])},
        })
    out.sort(key=lambda b: (ORDER.index(b['role']) if b['role'] in ORDER else 9, b['name']))
    return out


def villages():
    out = {}
    for kind, name in VILLAGES.items():
        path = ROOT / 'tools' / 'villages' / 'out' / f'{name}.json'
        if not path.exists():
            continue
        v = json.loads(path.read_text())
        out[kind] = {'name': name, 'center': v['center'], 'residents': v['residents'], 'buildings': len(v['buildings']),
                     'vox': {'size': v['size'], 'palette': v['palette'], 'blocks': pack(v['blocks'])}}
    return out


def layouts():
    rows = []
    records = json.loads((ROOT / 'tools' / 'villages' / 'out' / 'records.json').read_text())
    for name, r in records.items():
        cat = json.loads((ROOT / 'src' / 'main' / 'resources' / 'data' / 'endexpansion' / 'villages' / f'{name}.json').read_text())
        kind = name.split('_')[0]
        rows.append({'name': name, 'kind': kind, 'size': f'{r["width"]} × {r["max_y"] - r["min_y"] + 1} × {r["depth"]}',
                     'buildings': len(cat['buildings']), 'residents': cat['residents']})
    return rows


# Shots from the test run (seed 20261009) whose camera landed inside terrain or behind a column.
SKIP = {'spire_village-below', 'stead_village-below', 'crossing-street', 'crossing-below'}
CAPTIONS = {'overview': 'from above', 'side': 'from the far side', 'street': 'standing in the centre', 'below': 'from below: the islets over the void'}
KINDS = {'spire_village': 'Shulkin Spire', 'stead_village': 'Chorrin Stead', 'crossing': 'Crossing', 'citadel': 'Citadel'}


def shots():
    try:
        from PIL import Image
    except ImportError:
        return []
    folder = ROOT / 'build' / 'run' / 'clientGameTest' / 'screenshots'
    out = []
    for path in sorted(folder.glob('*end-*.png')):
        parts = path.stem.split('_', 1)[-1].split('-')
        kind, view = '-'.join(parts[2:-1]), parts[-1]
        if f'{kind}-{view}' in SKIP:
            continue
        img = Image.open(path).convert('RGB')
        img.thumbnail((1280, 720))
        buf = io.BytesIO()
        img.save(buf, 'JPEG', quality=80, optimize=True)
        out.append({'src': 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode(),
                    'caption': f'{KINDS.get(kind, kind)}, {CAPTIONS.get(view, view)}'})
    return out


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'out' / 'villages.html'
    data = {'buildings': buildings(), 'villages': villages(), 'layouts': layouts(), 'shots': shots()}
    page = (HERE / 'villages_page.html').read_text(encoding='utf-8')
    page = page.replace('/*__VIEWER__*/', (ROOT / 'tools' / 'buildings' / 'viewer.js').read_text(encoding='utf-8'))
    page = page.replace('/*__DATA__*/null', json.dumps(data, separators=(',', ':')))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding='utf-8')
    print(out, out.stat().st_size // 1024, 'KB')


if __name__ == '__main__':
    main()
