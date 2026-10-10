"""Inline the people models (geometry + textures) into the design page.

  python tools/design/build_page.py <out.html>

Rebuild the models and items first (tools/people/*.py, tools/items/*.py); the page reads the generated files.
"""
import base64
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from mobkit import GEOMETRY_DIR, ITEM_TEXTURE_DIR, TEXTURE_DIR  # noqa: E402

PEOPLE = ["shulkin", "shulkin_child", "chorrin", "chorrin_child", "endarch_lord", "endarch_marshal", "endarch_riftguard", "enderman_thrall",
          "groveback", "driftray", "voidhound", "voidhound_pup"]
ITEMS = ["enderman_eyes"]


def uri(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "people.html")
    data = {}
    for pid in PEOPLE:
        with open(os.path.join(GEOMETRY_DIR, pid + ".json"), encoding="utf-8") as f:
            geo = json.load(f)
        glow = os.path.join(TEXTURE_DIR, pid + "_glow.png")
        data[pid] = {"geo": geo, "tex": uri(os.path.join(TEXTURE_DIR, pid + ".png")),
                     "glow": uri(glow) if os.path.exists(glow) else None}
    data["items"] = {i: uri(os.path.join(ITEM_TEXTURE_DIR, i + ".png")) for i in ITEMS}
    with open(os.path.join(HERE, "people_page.html"), encoding="utf-8") as f:
        page = f.read()
    page = page.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(out, os.path.getsize(out) // 1024, "KB")


if __name__ == "__main__":
    main()
