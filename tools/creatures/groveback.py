"""Groveback: the Chorrin's herd beast. A slow, broad, six-legged grazer with an end-stone hide and a
small chorus grove growing on its back, the same living chorus as a Chorrin's crown. Chorrin herd
them between the islands and pick chorus fruit off their backs; wild herds wander the outer End.
About 1.4 blocks tall to the top of the grove, 2 blocks long."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "people"))

from common import (CHORUS, CHORUS_DEEP, CHORUS_HI, CHORUS_LIGHT, EYE_GLOW, FLOWER, FLOWER_DARK,  # noqa: E402
                    FLOWER_LIGHT, STONE, STONE_DARK, STONE_DEEP, STONE_LIGHT, glow_as, mix, painter, shade, tone)
from mobkit import Model, Pack, faces  # noqa: E402

NAME = "Groveback"
MOSS = ["#7b6a86", "#71607c", "#85748f"]       # the lilac chorus-moss that carpets its back


def hide(c, k=0.14):
    for y in range(c.h):
        for x in range(c.w):
            c.set(x, y, tone(c, y, c.pick(STONE), k))
    for _ in range(max(1, c.w * c.h // 20)):
        x, y = c.rng.randrange(c.w), c.rng.randrange(c.h)
        c.set(x, y, tone(c, y, STONE_DEEP, k))
        c.set(x, y + 1, tone(c, y + 1, STONE_LIGHT, k))
    if c.face == "bottom":
        c.fill(shade(STONE_DARK[0], 0.85))


def back(c):
    """The body: hide on the sides, a carpet of chorus-moss on top, hanging in fringes down the flanks."""
    hide(c)
    if c.face == "top":
        for y in range(c.h):
            for x in range(c.w):
                c.set(x, y, c.pick(MOSS) if c.rng.random() > 0.08 else CHORUS_LIGHT)
    elif c.face in ("left", "right", "front", "back"):
        for x in range(c.w):
            drop = 1 + (x * 7 + 3) % 3
            for y in range(drop):
                c.set(x, y, c.pick(MOSS) if y < drop - 1 else shade(MOSS[0], 0.8))


def head(c):
    hide(c, 0.1)
    if c.face == "front":
        for ex in (1, c.w - 2):                     # small, kind eyes set wide
            glow_as(c, ex, 2, EYE_GLOW, "#5a2d80")
            c.set(ex, 1, shade(STONE_DARK[0], 0.8))
    if c.face == "top":
        for x in range(c.w):
            c.set(x, 0, c.pick(MOSS))


def muzzle(c):
    hide(c, 0.06)
    if c.face == "front":
        for x in (1, c.w - 2):
            c.set(x, 1, STONE_DEEP)                 # nostrils
        for x in range(1, c.w - 1):
            c.set(x, c.h - 1, shade(STONE_DARK[1], 0.8))


def leg(c):
    hide(c, 0.2)
    if c.face in ("front", "back", "left", "right"):
        for x in range(c.w):
            c.set(x, c.h - 1, STONE_DEEP)           # a hard, dark hoof-rim


def stem(c, x, y):
    if c.face == "top":
        return CHORUS_HI
    if c.face == "bottom":
        return CHORUS_DEEP
    col = c.pick(CHORUS)
    if x == 0:
        col = CHORUS_LIGHT
    return col


def bud(c, x, y):
    if c.face == "top":
        edge = min(x, y, c.w - 1 - x, c.h - 1 - y)
        return FLOWER_LIGHT if edge == 0 else FLOWER_DARK
    if c.face == "bottom":
        return FLOWER_DARK
    col = c.pick(FLOWER)
    if y == 0:
        col = FLOWER_LIGHT
    if x == c.w // 2 and y > 0:
        col = FLOWER_DARK
    return col


def fruit(c, x, y):
    """A ripe chorus fruit, ready to pick."""
    if c.face == "top":
        return "#c9a0d6"
    return "#8e5aa0" if (x + y) % 2 else "#a673b8"


def build():
    m = Model("groveback", 128, 64, seed=61)
    m.preview = {"head": [0.15, 0, 0]}
    P = Pack(m)
    body = m.part("body")
    P.add(body, (-6, 7, -9), (12, 9, 18), faces(back))                                    # barrel
    P.add(body, (-5, 16, -7), (10, 2, 14), faces(lambda c: hide(c, 0.05)))                # belly
    P.add(body, (-5, 5, -8), (10, 2, 7), faces(back))                                     # shoulder hump
    hd = m.part("head", (0, 11, -9))
    P.add(hd, (-4, -3, -7), (8, 6, 7), faces(head))
    P.add(hd, (-3, 0, -10), (6, 4, 3), faces(muzzle))
    for sx in (-1, 1):                                                                     # stubby horn-nubs
        P.add(hd, (sx * 3 - 1, -5, -5), (2, 2, 2), faces(painter(stem)), sx > 0, "nub")
    tail = body.part("tail", (0, 10, 9), (0.6, 0, 0))
    P.add(tail, (-1, 0, 0), (2, 2, 5), faces(lambda c: hide(c, 0.1)))
    P.add(tail, (-1.5, -0.5, 4), (3, 3, 2), faces(painter(bud)))                          # a bloom on the tail
    for i, z in enumerate((-6, 0, 6)):                                                     # six legs
        for side, sx in (("right", -1), ("left", 1)):
            lg = m.part(f"{side}_leg_{i}", (4.5 * sx, 16, z))
            P.add(lg, (-1.5, 0, -1.5), (3, 8, 3), faces(leg), side == "left", "leg")
    grove = body.part("grove", (0, 7, 0))
    for (x, z, h, b) in ((-3, -5, 6, 3), (2, -2, 9, 3), (-1, 4, 5, 2), (3, 5, 4, 2), (-4, 2, 3, 0)):
        P.add(grove, (x - 1, -h, z - 1), (2, h, 2), faces(painter(stem)))
        if b:
            P.add(grove, (x - b / 2, -h - b, z - b / 2), (b, b, b), faces(painter(bud)))
    P.add(grove, (3, -6, -3), (3, 2, 2), faces(painter(stem)))                            # a side branch
    P.add(grove, (5, -8, -3), (2, 2, 2), faces(painter(fruit)))                           # ripe fruit
    P.add(grove, (-5, -4, -6), (2, 2, 2), faces(painter(fruit)))
    P.apply()
    m.save()


if __name__ == "__main__":
    build()
