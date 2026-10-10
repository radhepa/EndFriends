"""Chorrin: short, broad grove-folk of the outer islands, with skin like end stone. A crown of living
chorus grows from the top of the head (no two alike; it flowers as they age). Deep-set violet eyes
glow under a heavy brow, and they have no mouth: they speak in a low hum. Their long arms nearly
reach the ground and end in big three-fingered hands. They wear woven chorus-fiber wraps, a braided
cord belt with a buckle of traded shulker shell, and a hip pouch.

Also builds chorrin_child, a "sprout": round and stubby, with a head as big as an adult's, big bright
eyes under a soft brow, smoother pale stone, and a single chorus sprout where the crown will grow.
About 1 block (1.2 with the sprout)."""
from common import (CHORUS, CHORUS_DEEP, CHORUS_HI, CHORUS_LIGHT, EYE_GLOW, EYE_HOT, FLOWER,
                    FLOWER_DARK, FLOWER_LIGHT, SHELL, SHELL_DARK, SHELL_LIGHT, STONE, STONE_DARK,
                    STONE_DEEP, STONE_LIGHT, mix, painter, ring_u, shade, tone)
from common import glow_as, tinted, young
from mobkit import Model, Pack, faces

NAME = "Chorrin"

CLOTH = ["#8b7a90", "#83728a", "#917f97"]
CLOTH_DARK = "#5f5066"
CLOTH_LIGHT = "#a898ad"
STITCH = "#e2d8e5"
SOCKET = "#3e3242"


# -- end-stone skin --------------------------------------------------------------------------------
def skin(c, k=0.12):
    """End stone: pale yellow with clusters of small dark pits, each with a lit lower rim."""
    for y in range(c.h):
        for x in range(c.w):
            c.set(x, y, tone(c, y, c.pick(STONE), k))
    for _ in range(max(1, c.w * c.h // 22)):
        x, y = c.rng.randrange(c.w), c.rng.randrange(c.h)
        c.set(x, y, tone(c, y, STONE_DEEP, k))
        c.set(x + 1, y, tone(c, y, c.pick(STONE_DARK), k))
        c.set(x, y + 1, tone(c, y + 1, STONE_LIGHT, k))
    if c.face == "top":
        for x in range(c.w):
            if c.rng.random() < 0.3:
                c.set(x, c.rng.randrange(c.h), STONE_LIGHT)


def head(c):
    skin(c, 0.1)
    if c.face != "front":
        return
    # rows 2-3 sit behind the brow; eyes in deep sockets on rows 4-5; the jaw plate covers 6-7
    for y in (2, 3):
        for x in range(c.w):
            c.set(x, y, shade(c.pick(STONE_DARK), 0.85))
    for sx in (1, 5):
        for dx in range(3):
            c.set(sx + dx, 4, SOCKET)
            c.set(sx + dx, 5, mix(SOCKET, STONE_DEEP, 0.35))
    for ex in (2, 6):
        c.glow(ex, 4, EYE_HOT)
        c.glow(ex - 1, 4, shade(EYE_GLOW, 0.75))
        c.glow(ex + 1, 4, shade(EYE_GLOW, 0.75))
        c.glow(ex, 5, shade(EYE_GLOW, 0.55))
    c.set(4, 4, shade(STONE[0], 0.9))              # the bridge between the eyes
    c.set(4, 5, STONE_LIGHT)


def brow(c):
    skin(c, 0.05)
    if c.face in ("front", "left", "right"):
        for x in range(c.w):
            c.set(x, 0, STONE_LIGHT)
            c.set(x, c.h - 1, shade(c.pick(STONE_DARK), 0.9))
    if c.face == "bottom":
        c.fill(SOCKET)


def jaw(c):
    """A heavy jaw plate where a mouth would be, ridged where their hum resonates."""
    skin(c, 0.05)
    if c.face == "front":
        for x in range(1, c.w - 1, 2):
            c.set(x, 1, STONE_DEEP)
    if c.face == "bottom":
        c.fill(STONE_DEEP)


def veined(c):
    """Skin with chorus roots showing through it."""
    skin(c)
    if c.face in ("top", "bottom"):
        return
    x = c.rng.randrange(c.w)
    for y in range(c.h):
        c.set(x, y, mix(CHORUS_LIGHT, STONE[0], 0.35))
        if c.rng.random() < 0.4:
            x = max(0, min(c.w - 1, x + c.rng.choice((-1, 1))))


# -- crown of chorus -------------------------------------------------------------------------------
def stem(c, x, y):
    if c.face == "top":
        return CHORUS_HI
    if c.face == "bottom":
        return CHORUS_DEEP
    col = c.pick(CHORUS)
    if x == 0:
        col = CHORUS_LIGHT
    if (x + y) % 3 == 0:
        col = shade(col, 0.85)
    return col


def bud(c, x, y):
    """A chorus flower: pale petals, darker creases, a lit top."""
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


# -- clothing --------------------------------------------------------------------------------------
def torso(c):
    skin(c)
    w, d = 12, 8
    for y in range(c.h):
        for x in range(c.w):
            if c.face in ("top", "bottom"):
                continue
            u = x + ring_u(c, w, d)
            # a sash over the right shoulder down to the left hip, front and back
            if c.face in ("front", "back"):
                t = x if c.face == "front" else c.w - 1 - x
                if 0 <= t - y * 0.9 < 3:
                    col = CLOTH_LIGHT if t - y * 0.9 < 1 else c.pick(CLOTH)
                    if y % 3 == 0:
                        col = STITCH
                    c.set(x, y, tone(c, y, col, 0.1))
            if y >= 8:                               # the wrap below the belt
                col = c.pick(CLOTH) if u % 4 else CLOTH_DARK
                c.set(x, y, tone(c, y, col, 0.1))


def weave(c, x, y):
    if c.face in ("top", "bottom", "left", "right"):
        return CLOTH_DARK
    if y == c.h - 1:
        return None if x % 2 else CLOTH_LIGHT        # fringe
    col = CLOTH[0] if (x + y) % 2 else CLOTH_DARK
    if y % 3 == 1 and x % 2 == 0:
        col = CLOTH_LIGHT
    return col


def cord(c, x, y):
    if c.face in ("top", "bottom"):
        return CHORUS_DEEP
    k = (x + y) % 3
    return CHORUS_LIGHT if k == 0 else (CHORUS[0] if k == 1 else CHORUS_DEEP)


def buckle(c, x, y):
    if c.face == "front":
        edge = min(x, y, c.w - 1 - x, c.h - 1 - y)
        return SHELL_LIGHT if edge == 0 and y == 0 else (SHELL_DARK if edge == 0 else SHELL[0])
    return SHELL_DARK


def pouch(c, x, y):
    if c.face == "top":
        return CLOTH_DARK
    if y <= 1:
        return CLOTH_LIGHT if y == 0 else CLOTH_DARK  # the flap
    return tone(c, y, c.pick(CLOTH), 0.15)


# -- limbs -----------------------------------------------------------------------------------------
def forearm(c):
    skin(c)
    if c.face in ("front", "back", "left", "right"):
        for x in range(c.w):                         # wrist wrap
            c.set(x, 0, CLOTH_LIGHT if x % 2 else CLOTH[0])
            c.set(x, 1, CLOTH_DARK)


def hand(c):
    skin(c, 0.06)
    if c.face in ("front", "bottom"):
        for x in (1, 3):                             # three thick fingers
            for y in range(c.h // 2 if c.face == "front" else 0, c.h):
                c.set(x, y, shade(c.pick(STONE_DARK), 0.85))
    if c.face == "front":
        for x in (0, 2, 4):
            c.set(x, 0, STONE_LIGHT)                 # knuckles


def foot(c):
    skin(c, 0.05)
    if c.face == "front":
        c.set(c.w // 2, 0, STONE_DEEP)
        c.set(c.w // 2, 1, STONE_DEEP)
    if c.face == "bottom":
        c.fill(STONE_DEEP)


def build():
    m = Model("chorrin", 128, 64, seed=23)
    m.preview = {"right_arm": [0.0, 0, 0.18], "left_arm": [0.0, 0, -0.18]}
    P = Pack(m)

    body = m.part("body")
    P.add(body, (-6, 6, -4), (12, 11, 8), faces(torso))                               # barrel torso
    P.add(body, (-5, 3, -1), (10, 4, 6), faces(veined))                                  # shoulder hump
    P.add(body, (-6.5, 12, -4.5), (13, 2, 9), faces(painter(cord)))                    # braided belt
    P.add(body, (-1.5, 11.5, -5), (3, 3, 1), faces(painter(buckle)))                   # shell buckle
    P.add(body, (-3.5, 14, -4.6), (7, 7, 1), faces(painter(weave)))                    # front apron
    P.add(body, (-3.5, 14, 3.6), (7, 6, 1), faces(painter(weave)))                     # back flap
    P.add(body, (6, 13, -2), (3, 4, 3), faces(painter(pouch)))                         # hip pouch

    hd = m.part("head", (0, 6, -2))
    P.add(hd, (-4.5, -8, -4.5), (9, 8, 9), faces(head))
    P.add(hd, (-5, -6, -5.5), (10, 2, 1), faces(brow))                                   # heavy brow
    P.add(hd, (-4, -2, -5), (8, 2, 1), faces(jaw))
    crown = hd.part("crown", (0, -8, 0))
    P.add(crown, (-1, -4, -1), (2, 4, 2), faces(painter(stem)))                        # central stalk
    P.add(crown, (-1.5, -7, -1.5), (3, 3, 3), faces(painter(bud)))
    P.add(crown, (-4, -3, -0.5), (3, 2, 2), faces(painter(stem)))                      # right branch
    P.add(crown, (-4, -5, -0.5), (2, 2, 2), faces(painter(stem)))
    P.add(crown, (-4.5, -7, -1), (3, 2, 3), faces(painter(bud)))
    P.add(crown, (1, -2, 0), (3, 2, 2), faces(painter(stem)))                          # left branch
    P.add(crown, (2, -4, 0), (2, 2, 2), faces(painter(stem)))
    P.add(crown, (-3, -1, 2), (2, 1, 2), faces(painter(stem)))                         # nubs
    P.add(crown, (2, -1, -3), (1, 1, 1), faces(painter(stem)))

    for side, sx in (("right", -1), ("left", 1)):
        mirror = side == "left"
        arm = m.part(f"{side}_arm", (8 * sx, 7, 0))
        P.add(arm, (-2, -1, -2), (4, 7, 4), faces(veined), mirror, "upper")
        P.add(arm, (-2.5, -2, -2.5), (5, 2, 5), faces(skin), mirror, "shoulder")
        if side == "left":                           # a sprout of chorus on one shoulder
            P.add(arm, (0, -4, -0.5), (1, 2, 1), faces(painter(stem)))
            P.add(arm, (-0.5, -5.5, -1), (2, 2, 2), faces(painter(bud)))
        fore = arm.part(f"{side}_forearm", (0, 6, 0))
        P.add(fore, (-2.5, 0, -2.5), (5, 4, 5), faces(forearm), mirror, "fore")
        P.add(fore, (-2.5, 4, -2.5), (5, 3, 5), faces(hand), mirror, "hand")

        leg = m.part(f"{side}_leg", (3 * sx, 17, 0))
        P.add(leg, (-2.5, 0, -2.5), (5, 5, 5), faces(skin), mirror, "leg")
        P.add(leg, (-3, 5, -4), (6, 2, 7), faces(foot), mirror, "foot")

    P.apply()
    m.save()


def child_head(c):
    skin(c, 0.08)
    if c.face != "front":
        return
    # row 3 sits behind the soft brow; big round eyes on rows 4-5, wide-set
    for x0 in (1, 6):
        for dx in (0, 1):
            for dy in (0, 1):
                c.set(x0 + dx, 4 + dy, SOCKET)
        glow_as(c, x0, 4, EYE_HOT, "#a46ad6")
        glow_as(c, x0 + 1, 4, EYE_GLOW, "#6a3a99")
        glow_as(c, x0, 5, EYE_GLOW, "#6a3a99")
        glow_as(c, x0 + 1, 5, shade(EYE_GLOW, 0.7), "#4a2a70")
    for x in (0, 8):
        c.set(x, 6, STONE_LIGHT)                    # round, pale cheeks


def wrap(c, x, y):
    """A little chorus-fiber tunic."""
    if c.face in ("top", "bottom"):
        return CLOTH_DARK
    if y == c.h - 1:
        return CLOTH_DARK
    return CLOTH_LIGHT if (x + ring_u(c, 9, 7)) % 4 == 0 else c.pick(CLOTH)


def build_child():
    m = Model("chorrin_child", 128, 64, seed=29)
    m.scale = 0.75
    m.preview = {"right_arm": [0, 0, 0.3], "left_arm": [0, 0, -0.3]}
    P = Pack(m)
    smooth = young(0.25, toward="#f2f2cf")           # young stone: paler, the pits still shallow

    body = m.part("body")
    P.add(body, (-4, 12, -3), (8, 8, 6), tinted(faces(lambda c: skin(c, 0.08)), smooth))       # round body
    P.add(body, (-4.25, 11.75, -3.25), (8.5, 6.5, 6.5), faces(painter(wrap)))                  # tunic
    hd = m.part("head", (0, 12, -0.5))
    P.add(hd, (-4.5, -8, -4), (9, 8, 8), tinted(faces(lambda c: skin(c, 0.08), front=child_head), smooth))
    P.add(hd, (-4.5, -5, -5), (9, 1, 1), tinted(faces(brow), smooth))                          # soft brow
    sprout = hd.part("crown", (0, -8, 0))
    P.add(sprout, (-0.5, -3, -0.5), (1, 3, 1), faces(painter(stem)))
    P.add(sprout, (-1, -5, -1), (2, 2, 2), faces(painter(bud)))
    P.add(sprout, (0.5, -2, -0.5), (2, 1, 1), faces(painter(stem)))                            # a first side shoot

    for side, sx in (("right", -1), ("left", 1)):
        mirror = side == "left"
        arm = m.part(f"{side}_arm", (5.5 * sx, 13, 0))
        P.add(arm, (-1.5, -1, -1.5), (3, 4, 3), faces(painter(wrap)), mirror, "upper")                       # tunic sleeve
        P.add(arm, (-2, 3, -2), (4, 3, 4), tinted(faces(hand), smooth), mirror, "hand")
        leg = m.part(f"{side}_leg", (2.5 * sx, 20, 0))
        P.add(leg, (-2, 0, -2), (4, 2, 4), tinted(faces(lambda c: skin(c, 0.1)), smooth), mirror, "leg")
        P.add(leg, (-2.5, 2, -3), (5, 2, 5), tinted(faces(foot), smooth), mirror, "foot")

    P.apply()
    m.save()


if __name__ == "__main__":
    build()
    build_child()
