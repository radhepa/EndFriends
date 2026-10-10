"""Voidhound: the Court's hound, built on the vanilla Minecraft wolf (same boxes and pivots as WolfModel,
straightened so nothing is rotated except the tail): a 6x6x4 head with ears and a snout, a shaggy mane, a
lean body, four 2x8x2 legs, a raised tail. What makes it a Voidhound: an Enderman's void-black coat with
purple flecks, two magenta eye slits, and obsidian shards floating over its back.

  voidhound       a Court hound, a little bigger than a wolf (scale 1.3, about 1.1 blocks), with an
                  obsidian collar set with a magenta gem.
  voidhound_pup   the pup the Court gives you for high Favor (scale 0.6), with a purpur collar and a bone
                  tag, one small shard, and a bigger head for its size, like a baby wolf.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "people"))

from common import glow_as, painter, ring_u, shade  # noqa: E402
from mobkit import Model, Pack, faces  # noqa: E402
from endarch import EYE_IN, EYE_OUT, OBS, OBS_EDGE, OBS_GLINT, VOID, VOID_FLECK  # noqa: E402

NAME = "Voidhound"
FUR_LIGHT = "#241c2c"         # the lighter guard hairs that give the coat its texture
PURPUR = ["#a57ba6", "#9f74a0"]
PURPUR_DARK = "#6e4a70"
BONE = "#e8dfcf"


def fur(c, x, y):
    if c.rng.random() < 0.02:
        return c.pick(VOID_FLECK)
    col = c.pick(VOID)
    if c.face in ("front", "back", "left", "right") and (x + 2 * y) % 5 == 0:
        col = FUR_LIGHT
    if c.face == "bottom":
        col = shade(col, 0.8)
    return col


def head(c):
    painter(fur)(c)
    if c.face == "front":
        for x in range(c.w):
            c.set(x, 1, shade(VOID[0], 0.7))          # a heavy brow over the eyes
        # Enderman eye slits on the wolf's eye row, inner corner brightest
        for x0, inner in ((0, 1), (4, 4)):
            for dx in range(2):
                x = x0 + dx
                glow_as(c, x, 2, EYE_IN if x == inner else EYE_OUT, "#c86be0" if x == inner else "#6a1f86")


def snout(c):
    painter(fur)(c)
    if c.face == "front":
        c.set(1, 0, "#050407")                        # nose
        c.set(0, 0, "#0a080c")
        c.set(2, 0, "#0a080c")
    if c.face in ("front", "left", "right"):
        for x in range(c.w):
            c.set(x, c.h - 1, "#08070a")              # the line of the jaw


def collar_px(court, c, x, y):
    if court:
        if c.face in ("left", "right") and y % 3 == 1:
            glow_as(c, x, y, EYE_OUT, "#4a1560")      # magenta studs down the band
            return None
        return OBS_EDGE if (x + y) % 2 == 0 else "#3d2a5c"
    return PURPUR[0] if (x + y) % 3 else PURPUR_DARK


def mane(court):
    """Shaggy fur, with the collar painted round the front of the mane (like vanilla's collar layer):
    obsidian with a magenta gem for the Court's hounds, purpur with a bone tag for your pup."""
    def run(c):
        painter(fur)(c)
        if c.face in ("front", "back", "left", "right"):
            for x in range(c.w):                      # shaggy fringe along the lower edge
                if (x * 3 + ring_u(c, 8, 6)) % 4 == 0:
                    c.set(x, c.h - 1, FUR_LIGHT)
        band = []
        if c.face == "front":
            band = [(x, y) for y in range(c.h) for x in range(c.w)]
        elif c.face in ("left", "right"):
            cols = (c.w - 1, c.w - 2) if c.face == "right" else (0, 1)   # the two columns nearest the head
            band = [(x, y) for y in range(c.h) for x in cols]
        elif c.face == "top":
            band = [(x, y) for y in (c.h - 1, c.h - 2) for x in range(c.w)]
        for x, y in band:
            col = collar_px(court, c, x, y)
            if col is not None:
                c.set(x, y, col)
        if c.face == "front":                         # under the chin: the gem, or the tag
            mid = c.w // 2
            if court:
                glow_as(c, mid - 1, c.h - 1, EYE_OUT, "#6a1f86")
                glow_as(c, mid, c.h - 1, EYE_IN, "#c86be0")
            else:
                c.set(mid - 1, c.h - 1, BONE)
                c.set(mid, c.h - 1, BONE)
    return run


def shard(c, x, y):
    if c.face == "top" or y == 0:
        return OBS_EDGE
    return OBS_GLINT if (x + y) % 4 == 0 else c.pick(OBS)


def build_one(mid, court):
    m = Model(mid, 64, 64, seed=71 if court else 73)
    m.scale = 1.3 if court else 0.6
    P = Pack(m)
    body = m.part("body")
    P.add(body, (-3, 11, 0), (6, 6, 9), faces(painter(fur)))                               # body (wolf: 6x9x6)
    upper = m.part("upper_body")
    P.add(upper, (-4, 10, -6), (8, 7, 6), faces(mane(court)))                              # mane (wolf: 8x6x7)
    hd = m.part("head", (0, 13.5, -7))
    big = 0 if court else 0.8          # a pup's head is bigger for its size, like a baby wolf's
    P.add(hd, (-3, -3, -2), (6, 6, 4), faces(painter(fur), front=head), inflate=big)        # head
    P.add(hd, (-1.5, big * 0.5, -5 - big), (3, 3, 4), faces(snout), inflate=big * 0.4)     # snout
    P.add(hd, (-3, -5 - big, 0), (2, 2, 1), faces(painter(fur)), False, "ear", big * 0.4)  # ears
    P.add(hd, (1, -5 - big, 0), (2, 2, 1), faces(painter(fur)), True, "ear", big * 0.4)
    for side, sx in (("right", -1), ("left", 1)):
        for end, z in (("hind", 7), ("front", -4)):
            lg = m.part(f"{side}_{end}_leg", (1.5 * sx, 16, z))
            P.add(lg, (-1, 0, -1), (2, 8, 2), faces(painter(fur)), side == "left", "leg")
    tail = m.part("tail", (0, 12, 8), (1.75, 0, 0))                                        # raised, like a healthy wolf's
    P.add(tail, (-1, 0, -1), (2, 8, 2), faces(painter(fur)))
    spine = body.part("shards", (0, 8, 0))                                                 # float 3 px over the back
    for z, h in (((1, 3), (4, 4), (7, 2)) if court else ((4, 2),)):
        P.add(spine, (-0.5, -h, z - 0.5), (1, h, 1), faces(painter(shard)))
    P.apply()
    m.save()


def build():
    build_one("voidhound", True)
    build_one("voidhound_pup", False)


if __name__ == "__main__":
    build()
