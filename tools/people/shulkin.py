"""Shulkin: tall, robed shell-folk of the purpur spires. Their head is a living shulker-style shell, a
lid over a collar, and their soft pale face looks out through the gap with two glowing violet eyes.
The lid lifts when they speak and snaps shut when they are frightened or hurt. They stand about two
and a half blocks tall, glide a pixel off the ground on pointed feet, wear long void-cloth robes
under purpur shell pauldrons and a breastplate, and have long arms with three slender fingers.

Also builds shulkin_child: a full-size shell on a small body (children's heads are big for their size),
the shell still soft and pale (it darkens and hardens over the years), no crest, no armour, a plain
smock with one band of trim. About 1.3 blocks."""
import math

from common import (CHORUS, EYE_GLOW, EYE_HOT, FLOWER, FLOWER_DARK, HOLLOW, ROD, ROD_DIM, SHELL,
                    SHELL_DARK, SHELL_DEEP, SHELL_LIGHT, SHELL_RIM, TRIM, VOID, VOID_DARK, VOID_LIGHT,
                    mix, painter, ring_u, shade, tone)
from common import tinted, young
from mobkit import Model, Pack, faces

NAME = "Shulkin"

FLESH = ["#e9dfeb", "#e4d8e7", "#ede5ef"]
FLESH_SHADE = "#c7b6cd"
FLESH_TIP = "#a77fb8"
EYE = "#1d1028"


# -- shell -----------------------------------------------------------------------------------------
def lid_side(c, x, y):
    if y == 0:
        return SHELL_LIGHT
    if y == c.h - 1:
        return SHELL_DARK
    u = x + ring_u(c, 10, 10)
    col = c.pick(SHELL)
    if u % 5 == 4:
        col = shade(col, 0.86)                       # seams between the shell's plates
    return tone(c, y, col, 0.12)


def lid_top(c, x, y):
    edge = min(x, y, c.w - 1 - x, c.h - 1 - y)
    if edge == 0:
        return SHELL_RIM
    if edge == 1:
        return shade(c.pick(SHELL), 1.05)
    if edge == 2:
        return SHELL_DARK if (x + y) % 2 else shade(SHELL_DARK, 1.08)
    return c.pick(SHELL)                             # the purpur tile in the middle


def under(c, x, y):
    """Inside of the lid (seen through the gap): hollow, with a lip of shell round the edge."""
    edge = min(x, y, c.w - 1 - x, c.h - 1 - y)
    return SHELL_DEEP if edge == 0 else HOLLOW


def base_side(c, x, y):
    if y == 0:
        return SHELL_RIM
    if y == c.h - 1:
        return SHELL_DEEP
    u = x + ring_u(c, 10, 10)
    col = c.pick(SHELL)
    if u % 5 == 2:
        col = shade(col, 0.86)
    return tone(c, y, col, 0.16)


def ridge(c, x, y):
    if c.face == "top":
        return SHELL_RIM if x == 0 or (y % 3 == 0) else SHELL_LIGHT
    return SHELL_LIGHT if y == 0 else c.pick(SHELL)


def plates(c, x, y):
    """Overlapping shell scales for pauldrons and the mantle."""
    if c.face == "top":
        return SHELL_RIM if (x + y) % 4 == 0 else c.pick(SHELL)
    if c.face == "bottom":
        return SHELL_DEEP
    if y == 0:
        return SHELL_LIGHT
    if y % 2 == 0:
        return SHELL_DARK if (x + y // 2) % 3 else shade(SHELL_DARK, 0.9)
    return tone(c, y, c.pick(SHELL), 0.1)


def breastplate(c, x, y):
    if c.face != "front":
        return SHELL_DARK if c.face in ("left", "right", "bottom") else SHELL_LIGHT
    edge = min(x, y, c.w - 1 - x, c.h - 1 - y)
    if edge == 0:
        return SHELL_LIGHT if y == 0 else SHELL_DARK
    return c.pick(SHELL)


def breastplate_rune(c):
    painter(breastplate)(c)
    if c.face == "front":                            # the eye-shaped sigil of the spires
        cx = c.w // 2
        for x, y in ((cx - 1, 1), (cx, 1), (cx - 2, 2), (cx + 1, 2), (cx - 1, 3), (cx, 3)):
            c.set(x, y, ROD_DIM)
        c.glow(cx - 1, 2, EYE_GLOW)
        c.glow(cx, 2, EYE_GLOW)


# -- the face inside -------------------------------------------------------------------------------
def face(c):
    for y in range(c.h):
        for x in range(c.w):
            col = c.pick(FLESH)
            if y <= 1:
                col = mix(col, HOLLOW, 0.55 if y == 0 else 0.3)   # in the lid's shadow
            if c.face != "front":
                col = shade(col, 0.88)
            c.set(x, y, col)
    if c.face == "front":
        # big, wide-set eyes in the gap (rows 2-3): dark, with a glowing pupil low and inward
        for ex, inner in ((1, 2), (5, 5)):
            for dy in (2, 3):
                for dx in (0, 1):
                    c.set(ex + dx, dy, EYE)
            c.glow(inner, 3, EYE_GLOW)
            c.glow(inner, 2, shade(EYE_GLOW, 0.55))
        c.set(0, 3, FLESH_SHADE)
        c.set(7, 3, FLESH_SHADE)


def flesh(c, x, y):
    return tone(c, y, c.pick(FLESH), 0.1)


def finger(c, x, y):
    if y >= c.h - 1:
        return FLESH_TIP
    return tone(c, y, c.pick(FLESH), 0.12)


# -- cloth -----------------------------------------------------------------------------------------
def cloth_px(c, x, y, w, d, k=0.12):
    u = x + ring_u(c, w, d)
    col = c.pick(VOID)
    if u % 3 == 0:
        col = VOID_LIGHT if c.face != "back" else c.pick(VOID)     # long folds
    elif u % 3 == 2:
        col = shade(col, 0.82)
    return tone(c, y, col, k)


def robe(w, d, hem=False, tabard=False, sash=None, collar=False):
    def run(c):
        for y in range(c.h):
            for x in range(c.w):
                if c.face == "top":
                    c.set(x, y, VOID_DARK)
                    continue
                if c.face == "bottom":
                    c.set(x, y, shade(VOID_DARK, 0.8))
                    continue
                col = cloth_px(c, x, y, w, d)
                if tabard and c.face == "front" and abs(x - (c.w - 1) / 2) <= 1.6:
                    # the embroidered front panel: rod-white chevrons on purpur
                    col = TRIM[0] if (x + y) % 2 == 0 else TRIM[1]
                    if (y + abs(x - (c.w - 1) / 2) * 2) % 4 < 1:
                        col = ROD_DIM
                if sash and sash[0] <= y <= sash[1]:
                    col = TRIM[0] if y == sash[0] else TRIM[1]
                    if y == sash[1]:
                        col = shade(TRIM[1], 0.8)
                if collar and y == 0:
                    col = TRIM[0]
                if hem and y >= c.h - 2:
                    col = TRIM[0] if y == c.h - 2 else shade(TRIM[1], 0.85)
                    if y == c.h - 2 and (x + ring_u(c, w, d)) % 3 == 1:
                        col = ROD
                c.set(x, y, col)
        if sash and c.face == "front":              # the knot of the sash
            k = c.w // 2 - 1
            for x, y in ((k, sash[1] + 1), (k + 1, sash[1] + 1), (k, sash[1] + 2)):
                c.set(x, y, TRIM[1])
    return run


def cuff(c, x, y):
    if c.face == "bottom":
        return HOLLOW
    if c.face == "top":
        return TRIM[1]
    if y == c.h - 1:
        return ROD if (x + ring_u(c, 4, 4)) % 2 == 0 else TRIM[0]
    return tone(c, y, c.pick(TRIM), 0.1)


def cape(c):
    for y in range(c.h):
        for x in range(c.w):
            if c.face == "front":                   # lining, against the body
                col = shade(c.pick(SHELL), 0.8)
            elif c.face in ("top", "bottom", "left", "right"):
                col = TRIM[1]
            else:
                col = tone(c, y, VOID_DARK if (x % 3) else c.pick(VOID), 0.08)
                if y >= c.h - 2:
                    col = TRIM[0]
            c.set(x, y, col)
    if c.face == "back":
        # edge stripes, and the eye of the spires: a tall diamond in rod-white thread, glowing at its heart
        for y in range(c.h - 2):
            c.set(0, y, TRIM[1])
            c.set(c.w - 1, y, TRIM[1])
        cx, cy, r = c.w / 2 - 0.5, 8, 5
        for y in range(cy - r, cy + r + 1):
            half = (r - abs(y - cy)) * 0.6
            for x in range(c.w):
                dx = abs(x - cx)
                if abs(dx - half) < 0.55 or (half < 0.6 and dx < 0.6):
                    c.set(x, y, ROD_DIM)
        for x, y in ((c.w // 2 - 1, cy), (c.w // 2, cy)):
            c.glow(x, y, EYE_GLOW)
        c.glow(c.w // 2 - 1, cy - 1, shade(EYE_GLOW, 0.6))
        c.glow(c.w // 2, cy + 1, shade(EYE_GLOW, 0.6))
        for y in (cy + r + 2, cy + r + 4):
            for x in range(2, c.w - 2):
                if (x + y) % 2 == 0:
                    c.set(x, y, ROD_DIM)


def wraps(c, x, y):
    """Leg wraps: dark cloth bound in a spiral."""
    if c.face in ("top", "bottom"):
        return VOID_DARK
    return VOID_LIGHT if (x + y) % 4 == 0 else tone(c, y, VOID_DARK, 0.05)


def build():
    m = Model("shulkin", 128, 64, seed=11)
    m.preview = {"right_arm": [0.1, 0, 0.12], "left_arm": [-0.1, 0, -0.12],
                 "right_forearm": [-0.25, 0, 0], "left_forearm": [-0.2, 0, 0]}
    P = Pack(m)

    body = m.part("body")
    P.add(body, (-1, -7, -1), (2, 2, 2), faces(painter(flesh)))                       # neck
    P.add(body, (-5, -5, -3), (10, 2, 6), faces(painter(plates)))                     # mantle
    P.add(body, (-4, -4, -2.5), (8, 6, 5), faces(robe(8, 5, collar=True)))           # chest
    P.add(body, (-3, -3.8, -3.2), (6, 5, 1), faces(breastplate_rune))                 # breastplate
    P.add(body, (-3, 2, -2), (6, 4, 4), faces(robe(6, 4, sash=(1, 2))))               # waist + sash
    P.add(body, (-4, 6, -3), (8, 6, 6), faces(robe(8, 6, tabard=True)))               # skirt
    P.add(body, (-5, 12, -3.5), (10, 7, 7), faces(robe(10, 7, tabard=True, hem=True)))  # long hem
    cape_part = body.part("cape", (0, -4, 2.6), (0.08, 0, 0))
    P.add(cape_part, (-4, 0, 0), (8, 17, 1), faces(cape))

    head = m.part("head", (0, -7, 0))
    P.add(head, (-4, -7, -3), (8, 6, 6), faces(face))                                 # the face inside
    P.add(head, (-5, -3, -5), (10, 3, 10), faces(painter(base_side), top=painter(under),
                                                 bottom=lambda c: c.fill(SHELL_DEEP)))  # collar shell
    lid = head.part("lid", (0, -7, 0))   # raised 4 px: the face shows through the gap
    P.add(lid, (-5, -4, -5), (10, 4, 10), faces(painter(lid_side), top=painter(lid_top),
                                                bottom=painter(under)))
    P.add(lid, (-1, -5, -4), (2, 1, 8), faces(painter(ridge)))                        # crest

    for side, sx in (("right", -1), ("left", 1)):
        mirror = side == "left"
        arm = m.part(f"{side}_arm", (5.5 * sx, -3, 0))
        P.add(arm, (-1.5, -1, -1.5), (3, 9, 3), faces(robe(3, 3)), mirror, "sleeve")
        P.add(arm, (-2.5 if side == "right" else -2.5, -2.5, -3), (5, 3, 6), faces(painter(plates)), mirror, "pauldron")
        fore = arm.part(f"{side}_forearm", (0, 8, 0))
        P.add(fore, (-1.5, 0, -1.5), (3, 5, 3), faces(robe(3, 3)), mirror, "fore")
        P.add(fore, (-2, 4, -2), (4, 3, 4), faces(painter(cuff)), mirror, "cuff")
        P.add(fore, (-1, 6.5, -1), (2, 3, 2), faces(painter(flesh)), mirror, "palm")
        P.add(fore, (-1, 9.5, -1), (1, 3, 1), faces(painter(finger)), mirror, "finger")
        P.add(fore, (0, 9.5, -1), (1, 3, 1), faces(painter(finger)), mirror, "finger")
        P.add(fore, (-0.5 if side == "right" else -0.5, 9.5, 0), (1, 2, 1), faces(painter(finger)), mirror, "thumb")

        leg = m.part(f"{side}_leg", (2 * sx, 6, 0))
        P.add(leg, (-1, 0, -1), (2, 15, 2), faces(painter(wraps)), mirror, "leg")
        P.add(leg, (-0.5, 15, -0.5), (1, 2, 1), faces(painter(finger)), mirror, "point")

    P.apply()
    m.save()


def build_child():
    m = Model("shulkin_child", 128, 64, seed=13)
    m.scale = 0.7
    m.preview = {"right_arm": [0.15, 0, 0.2], "left_arm": [-0.1, 0, -0.2]}
    P = Pack(m)
    soft = young(0.4)                                # a young shell: paler and softer than an adult's

    body = m.part("body")
    P.add(body, (-3, 6, -2), (6, 4, 4), faces(robe(6, 4, collar=True)))               # smock
    P.add(body, (-4, 10, -3), (8, 8, 6), faces(robe(8, 6, sash=(0, 1), hem=True)))    # skirt, to the feet

    head = m.part("head", (0, 6, 0))
    P.add(head, (-4, -7, -3), (8, 6, 6), faces(face))
    P.add(head, (-5, -3, -5), (10, 3, 10), tinted(faces(painter(base_side), top=painter(under),
                                                        bottom=lambda c: c.fill(SHELL_DEEP)), soft))
    lid = head.part("lid", (0, -7, 0))
    P.add(lid, (-5, -4, -5), (10, 4, 10), tinted(faces(painter(lid_side), top=painter(lid_top),
                                                       bottom=painter(under)), soft))

    for side, sx in (("right", -1), ("left", 1)):
        mirror = side == "left"
        arm = m.part(f"{side}_arm", (4 * sx, 7, 0))
        P.add(arm, (-1, -1, -1), (2, 5, 2), faces(robe(2, 2)), mirror, "sleeve")
        P.add(arm, (-1.5, 3, -1.5), (3, 2, 3), faces(painter(cuff)), mirror, "cuff")
        P.add(arm, (-1, 5, -1), (2, 2, 2), faces(painter(flesh)), mirror, "hand")
        P.add(arm, (-1, 7, -1), (1, 2, 1), faces(painter(finger)), mirror, "finger")
        P.add(arm, (0, 7, -1), (1, 2, 1), faces(painter(finger)), mirror, "finger")
        leg = m.part(f"{side}_leg", (1.5 * sx, 14, 0))
        P.add(leg, (-1, 0, -1), (2, 7, 2), faces(painter(wraps)), mirror, "leg")
        P.add(leg, (-0.5, 7, -0.5), (1, 2, 1), faces(painter(finger)), mirror, "point")

    P.apply()
    m.save()


if __name__ == "__main__":
    build()
    build_child()
