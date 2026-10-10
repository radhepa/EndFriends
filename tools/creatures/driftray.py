"""Driftray: a manta-like flyer that glides on the void currents between islands. Deep violet above,
spotted with points of light like a night sky, pale lavender underneath, a long whip tail with a glowing
tip. Wild ones drift in slow flocks around the Spires; Shulkin Wayfinders tame them with chorus flowers
and ride them across the gaps. Wingspan about 3 blocks."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "people"))

from common import EYE_GLOW, EYE_HOT, ROD, glow_as, mix, painter, ring_u, shade, tone  # noqa: E402
from mobkit import Model, Pack, faces  # noqa: E402

NAME = "Driftray"
TOP = ["#3b2457", "#412860", "#36204f"]
TOP_EDGE = "#7a55a8"
UNDER = ["#e3d6ee", "#dccdea", "#e9def2"]
UNDER_SHADE = "#bfaed2"
STAR = "#e6d4ff"


def skin(c, edge_light=False):
    """Sky-spotted top, pale underside; the rim glows faintly where top meets bottom."""
    for y in range(c.h):
        for x in range(c.w):
            if c.face == "bottom":
                col = c.pick(UNDER)
                if x in (0, c.w - 1) or y in (0, c.h - 1):
                    col = UNDER_SHADE
            elif c.face == "top":
                col = c.pick(TOP)
                if edge_light and (x in (0, c.w - 1) or y in (0, c.h - 1)):
                    col = TOP_EDGE
            else:
                col = TOP_EDGE if y == 0 else mix(TOP[0], UNDER[0], 0.55)
            c.set(x, y, col)
    if c.face == "top":
        for _ in range(max(1, c.w * c.h // 16)):    # its stars
            x, y = c.rng.randrange(c.w), c.rng.randrange(c.h)
            glow_as(c, x, y, STAR, "#5b4a7a")


def body(c):
    skin(c, edge_light=True)
    if c.face == "front":
        for ex in (1, c.w - 2):
            glow_as(c, ex, 1, EYE_HOT, "#6a3a99")


def fin(c):
    skin(c, edge_light=True)


def tail(c, x, y):
    if c.face == "bottom":
        return UNDER_SHADE
    return TOP[0] if (x + y) % 3 else TOP_EDGE


def tail_tip(c):
    for y in range(c.h):
        for x in range(c.w):
            glow_as(c, x, y, EYE_GLOW if (x + y) % 2 else ROD, "#6a3a99")


def build():
    m = Model("driftray", 128, 64, seed=67)
    m.preview = {"right_wing": [0, 0, 0.18], "left_wing": [0, 0, -0.18], "right_tip": [0, 0, 0.22], "left_tip": [0, 0, -0.22]}
    P = Pack(m)
    root = m.part("body", (0, 8, 0))
    P.add(root, (-5, -2, -7), (10, 4, 14), faces(body))
    P.add(root, (-4, 2, -5), (8, 1, 10), faces(fin))                                       # belly ridge
    for sx in (-1, 1):                                                                     # cephalic lobes
        P.add(root, (sx * 3.5 - 1, -1, -10), (2, 2, 3), faces(fin), sx > 0, "lobe")
    for side, sx in (("right", -1), ("left", 1)):
        mir = side == "left"
        wing = root.part(f"{side}_wing", (5 * sx, 0, -1))
        P.add(wing, (-12 if side == "right" else 0, -1, -5), (12, 2, 11), faces(fin), mir, "wing")
        tip = wing.part(f"{side}_tip", (12 * sx, 0, 1))
        P.add(tip, (-8 if side == "right" else 0, -0.5, -3), (8, 1, 6), faces(fin), mir, "tip")
    tl = root.part("tail", (0, 0, 7), (0.08, 0, 0))
    P.add(tl, (-0.5, -0.5, 0), (1, 1, 16), faces(painter(tail)))
    P.add(tl, (-1, -1, 15), (2, 2, 2), faces(tail_tip))
    P.apply()
    m.save()


if __name__ == "__main__":
    build()
