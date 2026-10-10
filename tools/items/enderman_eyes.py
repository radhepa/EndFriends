"""Enderman Eyes: the seal of an Endarch envoy. A pair of preserved royal eyes set in an obsidian
reliquary with a purpur rim, a bone clasp below and a fine chain above. Rare loot on End ships.

  python tools/items/enderman_eyes.py      -> textures/item/enderman_eyes.png (+ an 8x preview in tools/preview/out)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from mobkit import ITEM_TEXTURE_DIR, hexc  # noqa: E402
from PIL import Image  # noqa: E402

PAL = {
    ".": None,
    "K": "#0b0910",   # outline
    "O": "#1c1229",   # obsidian
    "o": "#140d1f",   # obsidian, shadowed
    "H": "#3d2a5c",   # obsidian highlight
    "P": "#a57ba6",   # purpur rim
    "p": "#7f567f",
    "L": "#d2b0d2",
    "E": "#d659f5",   # eye
    "W": "#fbe3ff",   # eye, brightest
    "M": "#8f2fb0",   # eye, dim edge
    "B": "#e8dfcf",   # bone clasp
    "b": "#b9ad98",
    "C": "#8a7a92",   # chain
    "c": "#5e5066",
}

SPRITE = [
    "................",
    "......c..c......",
    ".......CC.......",
    ".....KLPPLK.....",
    "...KKPPPPPPKK...",
    "..KPHHOOOOOOPK..",
    ".KPHOOOOOOOOOPK.",
    ".KPMEEWOOWEEMPK.",
    ".KPOMEMOOMEMOPK.",
    ".KpOOOOooOOOOpK.",
    "..KpOOOOOOOOpK..",
    "..KKppOooOppKK..",
    "....KKpBBpKK....",
    "......KBbK......",
    ".......KK.......",
    "................",
]


def main():
    assert len(SPRITE) == 16 and all(len(r) == 16 for r in SPRITE), [len(r) for r in SPRITE]
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(SPRITE):
        for x, ch in enumerate(row):
            if PAL[ch]:
                img.putpixel((x, y), hexc(PAL[ch]))
    os.makedirs(ITEM_TEXTURE_DIR, exist_ok=True)
    img.save(os.path.join(ITEM_TEXTURE_DIR, "enderman_eyes.png"))
    out = os.path.join(os.path.dirname(HERE), "preview", "out")
    os.makedirs(out, exist_ok=True)
    big = Image.new("RGBA", (160, 160), (139, 139, 139, 255))
    big.alpha_composite(img.resize((128, 128), Image.NEAREST), (16, 16))
    big.save(os.path.join(out, "enderman_eyes_x8.png"))


if __name__ == "__main__":
    main()
