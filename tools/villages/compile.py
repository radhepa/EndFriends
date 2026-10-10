"""Compile every End village layout into Minecraft data.

For each layout in ``LAYOUTS`` it plans the village (``plan.py``), cuts the canvas into 32x32
column tiles (structure templates under ``data/endexpansion/structure/village/<layout>/``), and
writes one ``endexpansion:village`` structure per kind with its layouts and islet rasters
embedded, the structure sets (Spire 40 / Stead 40 / Crossing 20, Citadels apart and rare), the
biome and structure tags, and a resident catalogue (where each building stands and its spots).

    python tools/villages/compile.py                 everything
    python tools/villages/compile.py spire_a         one layout (worldgen JSON still lists all)
    python tools/villages/compile.py --preview       also write tools/villages/out/<layout>.json for the design page
"""
import argparse
import base64
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / 'src' / 'main' / 'resources' / 'data' / 'endexpansion'
sys.path.insert(0, str(HERE.parent / 'buildings'))
sys.path.insert(0, str(HERE))
import kit  # noqa: E402
import look  # noqa: E402
from plan import Program, plan, Y0  # noqa: E402
import citadel_plan  # noqa: E402
from roster import roster  # noqa: E402

TILE = 32

S, C = 'shulkin', 'chorrin'
SPIRE_CORE = [('lid_hall', S), ('archive', S), ('lamp_tower', S)]
STEAD_CORE = [('popping_kiln', C), ('cooks_hearth', C), ('grove_terraces', C)]

LAYOUTS = {
    # Shulkin Spires: towers on separate islets at varied heights, bridged
    'spire_a': (Program('spire', 'lamp_court', S, SPIRE_CORE + [
        ('shell_nursery', S), ('driftray_roost', S), ('spire_twin', S), ('spire_home_tall', S), ('spire_home', S),
        ('spire_home', S)], gap=(7, 11), tiers=(0, 2, 3, 5, 6)), 11),
    'spire_b': (Program('spire', 'lamp_court', S, SPIRE_CORE + [
        ('weavers_loft', S), ('shellwright', S), ('spire_home_tall', S), ('spire_home', S), ('spire_home', S),
        ('spire_home', S)], gap=(6, 10), tiers=(0, 1, 3, 4, 7)), 23),
    'spire_c': (Program('spire', 'lamp_court', S, [('lid_hall', S), ('lamp_tower', S), ('shell_nursery', S),
        ('weavers_loft', S), ('driftray_roost', S), ('spire_twin', S), ('spire_twin', S), ('spire_home', S)],
        gap=(8, 12), tiers=(0, 2, 4, 6, 8)), 37),
    # Chorrin Steads: low domes crowded onto one island grown along the paths
    'stead_a': (Program('stead', 'hum_circle', C, STEAD_CORE + [
        ('brewhouse', C), ('groveback_pen', C), ('blinkers_post', C), ('dome_home_large', C), ('dome_pair', C),
        ('dome_home', C), ('dome_home', C)], gap=(2, 4), tiers=(0, 0, 1), merge=True, margin=2), 5),
    'stead_b': (Program('stead', 'hum_circle', C, STEAD_CORE + [
        ('stonecutters_yard', C), ('grove_terraces', C), ('dome_home_large', C), ('dome_home', C),
        ('dome_home', C), ('dome_home', C)], gap=(2, 5), tiers=(0, 1, 1, -1), merge=True, margin=2), 17),
    'stead_c': (Program('stead', 'hum_circle', C, [('popping_kiln', C), ('cooks_hearth', C), ('brewhouse', C),
        ('groveback_pen', C), ('stonecutters_yard', C), ('blinkers_post', C), ('dome_pair', C), ('dome_pair', C),
        ('dome_home', C)], gap=(2, 4), tiers=(0, 1), merge=True, margin=2), 29),
    # Crossings: a spire quarter and a stead quarter round the market
    'crossing_a': (Program('crossing', 'market', 'shared', [('crossing_hall', 'shared'), ('trade_stall', 'shared'),
        ('trade_stall_awning', 'shared'), ('archive', S), ('lamp_tower', S), ('spire_home_tall', S), ('spire_home', S),
        ('spire_home', S), ('popping_kiln', C), ('cooks_hearth', C), ('dome_home_large', C), ('dome_home', C),
        ('dome_pair', C)], gap=(3, 6), tiers=(0, 2, 4)), 41),
    'crossing_b': (Program('crossing', 'market', 'shared', [('crossing_hall', 'shared'), ('trade_stall_awning', 'shared'),
        ('weavers_loft', S), ('shellwright', S), ('spire_twin', S), ('spire_home', S), ('grove_terraces', C),
        ('brewhouse', C), ('blinkers_post', C), ('dome_home_large', C), ('dome_home', C), ('dome_home', C)],
        gap=(3, 6), tiers=(0, 3, 5)), 53),
}
CITADELS = {'citadel_a': 7, 'citadel_b': 19}

KINDS = {
    'spire_village': ['spire_a', 'spire_b', 'spire_c'],
    'stead_village': ['stead_a', 'stead_b', 'stead_c'],
    'crossing': ['crossing_a', 'crossing_b'],
    'citadel': list(CITADELS),
}


def build_layout(name):
    if name in CITADELS:
        return citadel_plan.plan(name, CITADELS[name])
    program, seed = LAYOUTS[name]
    return plan(name, program, seed)


def bounds(canvas):
    ys = [y for (x, y, z) in canvas.grid]
    return min(ys), max(ys)


def write_layout(lay):
    """Cut the canvas into tiles and return the layout record for the structure JSON."""
    c = lay.canvas
    folder = DATA / 'structure' / 'village' / lay.name
    if folder.exists():
        shutil.rmtree(folder)
    lo, hi = bounds(c)
    tiles = []
    for tz in range(0, c.d, TILE):
        for tx in range(0, c.w, TILE):
            path = folder / f'{tx // TILE}_{tz // TILE}.nbt'
            n = c.save_nbt(path, tx, tz, min(tx + TILE, c.w), min(tz + TILE, c.d), lo, hi + 1)
            if n == 0:
                path.unlink()
                continue
            tiles.append({'template': f'endexpansion:village/{lay.name}/{tx // TILE}_{tz // TILE}',
                          'offset': [tx, lo - Y0, tz]})
    ox, oz = -lay.minx, -lay.minz
    tops = bytearray([128] * (c.w * c.d))     # -128 as an unsigned byte: no islet
    depths = bytearray(c.w * c.d)
    for (x, z), (top, depth) in lay.ground.items():
        i = (z + oz) * c.w + (x + ox)
        assert -127 <= top <= 127, top
        tops[i] = top & 0xFF
        depths[i] = max(0, min(255, depth))
    return {
        'name': lay.name, 'width': c.w, 'depth': c.d, 'min_y': lo - Y0, 'max_y': hi - Y0,
        'center_x': ox, 'center_z': oz, 'tiles': tiles,
        'tops': base64.b64encode(bytes(tops)).decode(), 'depths': base64.b64encode(bytes(depths)).decode(),
    }


def catalogue(lay):
    """Where every building stands in layout space, with its spots, for placing residents later."""
    out = []
    for p in lay.plots:
        spots = []
        for s in p.build.meta.get('spots', []):
            x, y, z = s['pos']
            spots.append({'kind': s['kind'], 'pos': [p.x + x, p.top - p.build.ground + y, p.z + z]})
        out.append({'building': p.name, 'people': p.people, 'role': p.spec.get('role'), 'job': p.spec.get('job'),
                    'residents': p.spec.get('residents', 0), 'turns': p.turns, 'x': p.x, 'z': p.z, 'top': p.top,
                    'size': [p.w, p.build.h, p.d], 'spots': spots})
    return {'layout': lay.name, 'residents': lay.residents(), 'buildings': out}


def write_json(path, value, indent=2):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=indent) + '\n', encoding='utf-8')


def preview(lay):
    ground = {}
    ox, oz = -lay.minx, -lay.minz
    for (x, z), (top, depth) in lay.ground.items():
        if depth > 0:
            ground[(x + ox, z + oz)] = (top + Y0 - 1, max(0, depth - 1))
    data = look.export(lay.canvas, ground=ground)
    data['center'] = [ox, Y0, oz]
    data['name'] = lay.name
    data['residents'] = lay.residents()
    data['buildings'] = [{'name': p.name, 'x': p.x + ox, 'z': p.z + oz, 'w': p.w, 'd': p.d, 'top': p.top + Y0}
                         for p in lay.plots]
    out = HERE / 'out' / f'{lay.name}.json'
    write_json(out, data, indent=None)
    return out


def worldgen(records):
    survey = {'radius': 12, 'step': 4, 'min_land': 0.6, 'min_y': 40, 'max_y': 120, 'min_distance': 1000}
    for kind, names in KINDS.items():
        layouts = [records[n] for n in names if n in records]
        if not layouts:
            continue
        tag = 'citadel' if kind == 'citadel' else 'end_village'
        write_json(DATA / 'worldgen' / 'structure' / f'{kind}.json', {
            'type': 'endexpansion:village', 'biomes': f'#endexpansion:has_structure/{tag}', 'step': 'surface_structures',
            'spawn_overrides': {}, 'terrain_adaptation': 'none', 'survey': survey, 'layouts': layouts}, indent=1)
    write_json(DATA / 'tags' / 'worldgen' / 'biome' / 'has_structure' / 'end_village.json',
               {'values': ['minecraft:end_highlands', 'minecraft:end_midlands']})
    write_json(DATA / 'tags' / 'worldgen' / 'biome' / 'has_structure' / 'citadel.json',
               {'values': ['minecraft:end_highlands']})
    write_json(DATA / 'tags' / 'worldgen' / 'structure' / 'villages.json',
               {'values': ['endexpansion:spire_village', 'endexpansion:stead_village', 'endexpansion:crossing']})
    write_json(DATA / 'worldgen' / 'structure_set' / 'villages.json', {
        'structures': [{'structure': 'endexpansion:spire_village', 'weight': 2},
                       {'structure': 'endexpansion:stead_village', 'weight': 2},
                       {'structure': 'endexpansion:crossing', 'weight': 1}],
        'placement': {'type': 'minecraft:random_spread', 'spacing': 24, 'separation': 9, 'salt': 1946210431,
                      'exclusion_zone': {'other_set': 'minecraft:end_cities', 'chunk_count': 4}}})
    write_json(DATA / 'worldgen' / 'structure_set' / 'citadels.json', {
        'structures': [{'structure': 'endexpansion:citadel', 'weight': 1}],
        'placement': {'type': 'minecraft:random_spread', 'spacing': 64, 'separation': 24, 'salt': 1302880551,
                      'exclusion_zone': {'other_set': 'endexpansion:villages', 'chunk_count': 6}}})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('names', nargs='*')
    ap.add_argument('--preview', action='store_true')
    args = ap.parse_args()
    kit.load_all()
    names = args.names or [n for kind in KINDS.values() for n in kind]
    records_path = HERE / 'out' / 'records.json'
    records = json.loads(records_path.read_text()) if records_path.exists() and args.names else {}
    catalog = {}
    for name in names:
        lay = build_layout(name)
        records[name] = write_layout(lay)
        catalog[name] = catalogue(lay)
        records[name]['residents'] = roster(catalog[name])
        catalog[name]['roster'] = records[name]['residents']
        write_json(DATA / 'villages' / f'{name}.json', catalog[name])
        r = records[name]
        print(f'{name:12s} {r["width"]}x{r["max_y"] - r["min_y"] + 1}x{r["depth"]}  {len(r["tiles"])} tiles  '
              f'{len(lay.plots)} buildings  {len(r["residents"])} on the roster  {len(lay.paths)} paths')
        if args.preview:
            preview(lay)
    write_json(records_path, records, indent=None)
    worldgen(records)


if __name__ == '__main__':
    main()
