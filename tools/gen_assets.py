"""Write the mod's small generated assets: English names, spawn eggs (item model + texture), the
Enderman Eyes item model, and each mob's loot table.

    python tools/gen_assets.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mobkit import MOD_ID, ROOT, spawn_egg  # noqa: E402

ASSETS = os.path.join(ROOT, "src", "main", "resources", "assets", MOD_ID)
DATA = os.path.join(ROOT, "src", "main", "resources", "data", MOD_ID)

# id: (English name, egg base colour, egg spot colour, accent)
MOBS = {
    "shulkin": ("Shulkin", "#a57ba6", "#2c2242", "#cf8cff"),
    "shulkin_child": ("Young Shulkin", "#d8b9d7", "#5a395b", "#cf8cff"),
    "chorrin": ("Chorrin", "#dcdd9f", "#5f3f62", "#cdb2d6"),
    "chorrin_child": ("Chorrin Sprout", "#ecedbd", "#8d6b90", "#cdb2d6"),
    "endarch_lord": ("Endarch Lord", "#1b1430", "#a57ba6", "#d659f5"),
    "endarch_marshal": ("Voidmarshal", "#1b1430", "#3d2a5c", "#d659f5"),
    "endarch_riftguard": ("Riftguard", "#1b1430", "#7f567f", "#cf8cff"),
    "enderman_thrall": ("Enderman Thrall", "#161616", "#a57ba6", "#e079fa"),
    "groveback": ("Groveback", "#d3d594", "#5f3f62", "#cdb2d6"),
    "driftray": ("Driftray", "#5a3f8a", "#e8e0f0", "#cf8cff"),
    "voidhound": ("Voidhound", "#141018", "#2c2242", "#d659f5"),
}

# id: [(item, min, max)] dropped on death (looting adds up to one more of each)
DROPS = {
    "shulkin": [("minecraft:purpur_block", 0, 2), ("minecraft:popped_chorus_fruit", 0, 2)],
    "shulkin_child": [],
    "chorrin": [("minecraft:chorus_fruit", 1, 3), ("minecraft:end_stone", 0, 2)],
    "chorrin_child": [],
    "endarch_lord": [("minecraft:ender_pearl", 3, 6), ("minecraft:crying_obsidian", 2, 4), ("minecraft:end_crystal", 1, 1)],
    "endarch_marshal": [("minecraft:ender_pearl", 2, 4), ("minecraft:obsidian", 1, 3)],
    "endarch_riftguard": [("minecraft:ender_pearl", 1, 3), ("minecraft:amethyst_shard", 0, 2)],
    "enderman_thrall": [("minecraft:ender_pearl", 0, 1)],
    "groveback": [("minecraft:chorus_fruit", 1, 3), ("minecraft:end_stone", 0, 1)],
    "driftray": [("minecraft:phantom_membrane", 0, 1)],
    "voidhound": [("minecraft:ender_pearl", 0, 1)],
}


def write(path, value):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write("\n")


def loot(drops):
    pools = []
    for item, lo, hi in drops:
        pools.append({
            "rolls": 1,
            "entries": [{
                "type": "minecraft:item", "name": item,
                "modifier": [
                    {"type": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": lo, "max": hi}},
                    {"type": "minecraft:enchanted_count_increase", "enchantment": "minecraft:looting",
                     "count": {"type": "minecraft:uniform", "min": 0, "max": 1}},
                ],
            }],
        })
    return {"type": "minecraft:entity", "pools": pools}


def main():
    lang = {
        "item.endexpansion.enderman_eyes": "Enderman Eyes",
        "item.endexpansion.enderman_eyes.desc": "The seal of a Court envoy",
    }
    for i, (mob, (name, base, spots, accent)) in enumerate(MOBS.items()):
        lang[f"entity.{MOD_ID}.{mob}"] = name
        egg = f"{mob}_spawn_egg"
        lang[f"item.{MOD_ID}.{egg}"] = f"{name} Spawn Egg"
        write(os.path.join(ASSETS, "items", egg + ".json"), {"model": {"type": "minecraft:model", "model": f"{MOD_ID}:item/{egg}"}})
        write(os.path.join(ASSETS, "models", "item", egg + ".json"),
              {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD_ID}:item/{egg}"}})
        spawn_egg(mob, base, spots, accent, seed=11 + i)
        write(os.path.join(DATA, "loot_table", "entities", mob + ".json"), loot(DROPS[mob]))
    write(os.path.join(ASSETS, "items", "enderman_eyes.json"), {"model": {"type": "minecraft:model", "model": f"{MOD_ID}:item/enderman_eyes"}})
    write(os.path.join(ASSETS, "models", "item", "enderman_eyes.json"),
          {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD_ID}:item/enderman_eyes"}})
    write(os.path.join(ASSETS, "lang", "en_us.json"), lang)
    print(f"wrote names, eggs and loot tables for {len(MOBS)} mobs")


if __name__ == "__main__":
    main()
