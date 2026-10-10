"""Endarchs: the ruling caste of the Endermen. Taller and broader than an Enderman, with the same
void-black skin, but a crown of extra eyes along the brow and floating obsidian shards that hover
over the head of the highborn. Three ranks share one body:

  endarch_lord       the Lord of a Citadel: a floating crown of obsidian spires around an end crystal,
                     a royal mantle of dragon's-breath magenta trimmed in dragon bone, a high collar.
  endarch_marshal    a Voidmarshal (general): heavy obsidian plate, spiked pauldrons, a war cape with a
                     torn hem, a floating circlet.
  endarch_riftguard  a Riftguard (high warrior): a visored helm with the eyes burning through a T-slit,
                     floating shard pauldrons, a rift glaive with a crystal blade.

Also builds enderman_thrall, a vanilla-proportioned Enderman wearing the Court's bond-collar, for
comparison (in game this would be a layer on vanilla Endermen inside a Citadel).

  python tools/people/endarch.py            all four
"""
import math

from common import glow_as, mix, painter, ring_u, shade, tone
from mobkit import Model, Pack, faces

NAME = "Endarch"

VOID = ["#120f16", "#16121b", "#0e0c11", "#141017"]
VOID_FLECK = ["#2b1a3a", "#3a2350"]
EYE_OUT = "#d659f5"
EYE_IN = "#fbe3ff"
EYE_DIM = "#8f2fb0"
OBS = ["#170f23", "#1c1229", "#140d1f"]
OBS_HI = "#3d2a5c"
OBS_EDGE = "#4f3675"
OBS_GLINT = "#7b52b5"
ROYAL = ["#5c1a5f", "#64216b", "#551858"]
ROYAL_LIGHT = "#8d3796"
ROYAL_DARK = "#3a0f3d"
BONE = ["#e8dfcf", "#ded4c2", "#efe7d9"]
BONE_DARK = "#b9ad98"
CRYSTAL = "#f4c4f7"
CRYSTAL_HOT = "#fff0ff"
CRYSTAL_DEEP = "#c27ad0"
COLLAR = ["#a57ba6", "#9f74a0"]          # the purpur bond-collar the thralls wear
COLLAR_DARK = "#6e4a70"


# -- skin and eyes ---------------------------------------------------------------------------------
def skin(c, x, y):
    if c.rng.random() < 0.035:
        return c.pick(VOID_FLECK)
    return c.pick(VOID)


def face(eyes="lord"):
    """Void skin; the two Enderman eye-slits on row 4, and (for the highborn) a diadem of small eyes."""
    def run(c):
        painter(skin)(c)
        if c.face != "front":
            return
        for x0 in (0, 5):                            # the two main slits, Enderman-style
            inner = x0 + (2 if x0 == 0 else 0)
            for dx in range(3):
                x = x0 + dx
                glow_as(c, x, 4, EYE_IN if x == inner else EYE_OUT, "#c86be0" if x == inner else "#6a1f86")
        small = {"lord": [(1, 2), (3, 1), (4, 1), (6, 2), (2, 0), (5, 0)],
                 "marshal": [(1, 2), (3, 1), (4, 1), (6, 2)],
                 "guard": [(3, 2), (4, 2)],
                 "thrall": []}[eyes]
        for x, y in small:                           # the crown of eyes along the brow
            glow_as(c, x, y, EYE_OUT if (x + y) % 2 else EYE_DIM, "#5a1872")
        for x in range(2, 6):                        # a seam where the jaw closes
            c.set(x, 6, "#08070a")
    return run


# -- materials -------------------------------------------------------------------------------------
def obsidian(c, x, y):
    if c.face == "top":
        return OBS_HI if (x + y) % 5 == 0 else c.pick(OBS)
    if c.face in ("front", "back", "left", "right") and y == 0:
        return OBS_EDGE
    if c.rng.random() < 0.05:
        return OBS_GLINT
    return tone(c, y, c.pick(OBS), 0.1)


def obsidian_plate(c, x, y):
    """Plate armour: obsidian with a lit rim on every edge."""
    edge = min(x, y, c.w - 1 - x, c.h - 1 - y)
    if edge == 0 and c.face not in ("bottom",):
        return OBS_EDGE if y == 0 or c.face == "top" else OBS_HI
    if c.rng.random() < 0.05:
        return OBS_GLINT
    return c.pick(OBS)


def royal_px(c, x, y, w, d):
    u = x + ring_u(c, w, d)
    col = c.pick(ROYAL)
    if u % 4 == 0:
        col = ROYAL_LIGHT
    elif u % 4 == 3:
        col = ROYAL_DARK
    return tone(c, y, col, 0.14)


def scales(c, x, y):
    """Dragon-bone trim: overlapping pale scales."""
    if c.face == "bottom":
        return BONE_DARK
    if (x + (y // 2) % 2) % 2 == 0 and y % 2 == 1:
        return BONE_DARK
    return c.pick(BONE)


def crystal(c, x, y):
    if c.face == "top" or y == 0:
        return CRYSTAL_HOT
    return CRYSTAL if (x + y) % 2 else CRYSTAL_DEEP


def glowing(fn, k=0.45):
    """Paint with fn and add a dimmer copy to the emissive layer (keeps the hue under additive glow)."""
    def run(c):
        for y in range(c.h):
            for x in range(c.w):
                col = fn(c, x, y)
                if col is not None:
                    glow_as(c, x, y, col, shade(col, k))
    return run


def robe(w, d, hem=True, slit=False, sash=False):
    def run(c):
        for y in range(c.h):
            for x in range(c.w):
                if c.face == "top":
                    c.set(x, y, ROYAL_DARK)
                    continue
                if c.face == "bottom":
                    c.set(x, y, shade(ROYAL_DARK, 0.7))
                    continue
                col = royal_px(c, x, y, w, d)
                if slit and c.face == "front" and abs(x - (c.w - 1) / 2) < 1:
                    col = "#08070a"                  # the robe opens at the front over the legs
                if hem and y >= c.h - 2:
                    col = c.pick(BONE) if y == c.h - 2 else BONE_DARK
                if sash and c.face in ("front", "back"):
                    t = x if c.face == "front" else c.w - 1 - x
                    if 0 <= t - y < 2:
                        col = c.pick(BONE)
                c.set(x, y, col)
    return run


def mantle(torn=False):
    def run(c):
        for y in range(c.h):
            for x in range(c.w):
                if c.face == "front":
                    col = ROYAL_DARK                 # lining
                elif c.face in ("left", "right", "top", "bottom"):
                    col = ROYAL_DARK
                else:
                    col = royal_px(c, x, y, c.w, 1)
                    if x in (0, c.w - 1):
                        col = c.pick(BONE)
                if y >= c.h - 3:
                    if torn and (x * 7 + 3) % 5 < (y - (c.h - 3)) + 1:
                        c.clear(x, y)                # a ragged war-torn hem
                        continue
                    if not torn and y == c.h - 2:
                        col = c.pick(BONE)
                c.set(x, y, col)
        if c.face == "back" and not torn:
            # the sigil of the Court: one great eye, embroidered in bone and burning at its centre
            cx, cy = c.w / 2 - 0.5, 9
            for y in range(cy - 3, cy + 4):
                half = (3 - abs(y - cy)) * 1.4
                for x in range(c.w):
                    if abs(abs(x - cx) - half) < 0.6:
                        c.set(x, y, BONE[0])
            for x in (int(cx - 0.5), int(cx + 0.5) + 0):
                c.glow(x, cy, EYE_OUT)
            c.glow(int(cx), cy, EYE_IN)
        if c.face == "back" and torn:
            # chevrons of rank on the war cape
            for i in range(3):
                for x in range(c.w):
                    yy = 4 + i * 3 + abs(x - (c.w - 1) / 2) * 0.5
                    if 1 <= x <= c.w - 2:
                        c.set(x, int(yy), ROYAL_LIGHT)
    return run


def collar(c, x, y):
    if c.face in ("top", "bottom"):
        return COLLAR_DARK
    if y == c.h - 1:
        return COLLAR_DARK
    u = x + ring_u(c, 9, 9)
    return "#e6d9c4" if u % 9 == 4 and y == 1 else c.pick(COLLAR)   # a bone ring at the throat


# -- shared body -----------------------------------------------------------------------------------
def body(m, P, arms_pose=True, cloth_legs=False):
    """The Endarch body (54 px, about 3.4 blocks): long legs, broad chest, very long arms."""
    torso = m.part("body")
    P.add(torso, (-1.5, -22, -1.5), (3, 2, 3), faces(painter(skin)))                       # neck
    P.add(torso, (-5, -20, -2.5), (10, 9, 5), faces(painter(skin)))                         # chest
    P.add(torso, (-3.5, -11, -2), (7, 6, 4), faces(painter(skin)))                          # waist
    head = m.part("head", (0, -22, 0))
    arms, fores, legs = {}, {}, {}
    for side, sx in (("right", -1), ("left", 1)):
        mirror = side == "left"
        arm = m.part(f"{side}_arm", (6.5 * sx, -19, 0))
        P.add(arm, (-1, -1, -1), (2, 14, 2), faces(painter(skin)), mirror, "upper")
        fore = arm.part(f"{side}_forearm", (0, 13, 0))
        P.add(fore, (-1, 0, -1), (2, 12, 2), faces(painter(skin)), mirror, "fore")
        for fx, fz in ((-1, -1), (0, -1), (-0.5, 0)):       # three long claws
            P.add(fore, (fx, 12, fz), (1, 4, 1), faces(painter(skin)), mirror, "claw")
        leg = m.part(f"{side}_leg", (2.2 * sx, -5, 0))
        P.add(leg, (-1.5, 0, -1.5), (3, 14, 3), faces(painter(skin)), mirror, "thigh")
        shin = leg.part(f"{side}_shin", (0, 14, 0))
        P.add(shin, (-1, 0, -1), (2, 13, 2), faces(painter(skin)), mirror, "shin")
        P.add(shin, (-1.5, 13, -3.5), (3, 2, 5), faces(painter(skin)), mirror, "foot")
        arms[side], fores[side], legs[side] = arm, fore, leg
    return torso, head, arms, fores, legs


def head_cube(P, head, eyes):
    P.add(head, (-4, -8, -4), (8, 8, 8), faces(painter(skin), front=face(eyes)))


def shard_ring(P, part, n, radius, heights, start=0.0, size=1):
    """Floating obsidian shards standing in a ring (the crown of the highborn)."""
    for i in range(n):
        a = start + i * 2 * math.pi / n
        h = heights[i % len(heights)]
        x, z = math.sin(a) * radius, -math.cos(a) * radius
        P.add(part, (round(x - size / 2, 2), -h, round(z - size / 2, 2)), (size, h, size), faces(painter(obsidian)))


# -- the ranks -------------------------------------------------------------------------------------
def lord():
    m = Model("endarch_lord", 128, 128, seed=41)
    m.scale = 1.12
    m.preview = {"right_arm": [0.08, 0, 0.1], "left_arm": [-0.05, 0, -0.1]}
    P = Pack(m)
    torso, head, arms, fores, legs = body(m, P)
    head_cube(P, head, "lord")
    P.add(torso, (-3, -19.5, -3), (6, 5, 1), faces(painter(obsidian_plate)))               # breastplate
    P.add(torso, (-1, -18.5, -3.6), (2, 2, 1), glowing(crystal))                           # crystal brooch
    P.add(torso, (-4.5, -11, -3), (9, 8, 6), faces(robe(9, 6, hem=False, sash=True)))       # robe
    P.add(torso, (-5.5, -3, -3.5), (11, 20, 7), faces(robe(11, 7, slit=True)))             # long skirt
    P.add(torso, (-5.5, -27, 4), (11, 7, 2), faces(painter(scales)))                       # high collar
    cape = torso.part("mantle", (0, -20, 2.6), (0.07, 0, 0))
    P.add(cape, (-6, 0, 0), (12, 41, 1), faces(mantle()))
    for side in ("right", "left"):
        P.add(arms[side], (-2.5, -2.5, -3), (5, 3, 6), faces(painter(scales)), side == "left", "epaulette")
        P.add(arms[side], (-1.5, 7, -1.5), (3, 7, 3), faces(robe(3, 3, hem=False)), side == "left", "sleeve")
    crown = head.part("crown", (0, -11, 0))                                                  # floats 3 px up
    shard_ring(P, crown, 8, 4.5, [3, 4, 6, 4, 3, 4, 6, 4])
    P.add(crown, (-1, -9, -5.5), (2, 9, 2), faces(painter(obsidian)))                       # the high spire
    P.add(crown, (-1, -13, -5.5), (2, 3, 2), glowing(crystal))                              # its end crystal
    P.apply()
    m.save()


def marshal():
    m = Model("endarch_marshal", 128, 128, seed=43)
    m.scale = 1.04
    m.preview = {"right_arm": [-0.05, 0, 0.16], "left_arm": [0.05, 0, -0.16]}
    P = Pack(m)
    torso, head, arms, fores, legs = body(m, P)
    head_cube(P, head, "marshal")
    P.add(torso, (-5.5, -20.5, -3), (11, 9, 6), faces(painter(obsidian_plate)))            # cuirass
    P.add(torso, (-4, -11.5, -2.5), (8, 5, 5), faces(painter(obsidian)))                    # plated waist
    P.add(torso, (-5, -7, -3.2), (10, 7, 6.4), faces(painter(obsidian_plate)))             # fauld
    def sigil(c, x, y):
        # an open eye, the Court's mark of command
        if c.face != "front":
            return OBS[0]
        edge = x in (0, c.w - 1)
        if y == 1:
            return EYE_DIM if edge else EYE_IN
        return OBS[0] if edge else EYE_DIM
    P.add(torso, (-2.5, -18.5, -3.6), (5, 3, 1), faces(glowing(sigil, 0.4)))               # rank sigil
    cape = torso.part("cape", (0, -20, 3.1), (0.1, 0, 0))
    P.add(cape, (-5.5, 0, 0), (11, 32, 1), faces(mantle(torn=True)))
    for side, sx in (("right", -1), ("left", 1)):
        mir = side == "left"
        P.add(arms[side], (-3.5, -3.5, -3.5), (6, 5, 7), faces(painter(obsidian_plate)), mir, "pauldron")
        P.add(arms[side], (-2.5, -7.5, -2), (1, 4, 1), faces(painter(obsidian)), mir, "spike")
        P.add(arms[side], (-0.5, -6.5, 0), (1, 3, 1), faces(painter(obsidian)), mir, "spike2")
        P.add(fores[side], (-1.5, 4, -1.5), (3, 6, 3), faces(painter(obsidian_plate)), mir, "vambrace")
        P.add(legs[side], (-2, 4, -2), (4, 7, 4), faces(painter(obsidian_plate)), mir, "cuisse")
    circlet = head.part("circlet", (0, -10, 0))
    shard_ring(P, circlet, 6, 4.8, [2, 3, 2])
    P.apply()
    m.save()


def riftguard():
    m = Model("endarch_riftguard", 128, 128, seed=47)
    m.preview = {"right_arm": [-0.25, 0, 0.12], "right_forearm": [-1.15, 0, 0], "left_arm": [0.1, 0, -0.1]}
    P = Pack(m)
    torso, head, arms, fores, legs = body(m, P)

    def helm(c):
        painter(obsidian_plate)(c)
        if c.face == "front":                        # the T-slit, eyes burning through
            for x in range(1, c.w - 1):
                c.set(x, 4, "#060508")
            for y in range(4, 8):
                c.set(c.w // 2, y, "#060508")
            for x in (1, 2, 3, 5, 6, 7):
                c.glow(x, 4, EYE_OUT if x in (2, 6) else EYE_DIM)
            c.glow(4, 5, EYE_IN)
    P.add(head, (-4.5, -8.5, -4.5), (9, 9, 9), faces(helm))
    P.add(head, (-0.5, -11.5, -4), (1, 3, 8), faces(painter(obsidian)))                    # crest
    P.add(torso, (-5.5, -20.5, -3), (11, 8, 6), faces(painter(obsidian_plate)))            # breastplate
    P.add(torso, (-4.5, -7, -3), (9, 5, 6), faces(robe(9, 6, hem=True)))                   # tasset cloth
    for side in ("right", "left"):
        mir = side == "left"
        # pauldrons float a pixel clear of the shoulder: rift armour
        P.add(arms[side], (-3, -5.5, -3), (5, 2, 6), faces(painter(obsidian_plate)), mir, "float_plate")
        P.add(arms[side], (-2.5, -3, -2.5), (4, 1, 5), faces(painter(obsidian)), mir, "float_plate2")
        P.add(fores[side], (-1.5, 2, -1.5), (3, 7, 3), faces(painter(obsidian_plate)), mir, "bracer")
        P.add(legs[side], (-2, 2, -2), (4, 9, 4), faces(painter(obsidian_plate)), mir, "greave")
    glaive = fores["right"].part("glaive", (0, 13, -0.5), (1.4, 0, 0))    # held upright
    P.add(glaive, (-0.5, -26, -0.5), (1, 40, 1), faces(painter(obsidian)))                 # haft
    P.add(glaive, (-1.5, -27, -1.5), (3, 1, 3), faces(painter(obsidian_plate)))            # guard
    def blade(c, x, y):
        if c.face in ("left", "right"):
            # the blade's profile: a long point, widest near the guard (bottom rows)
            half = (y + 1) / c.h * 2.5
            mid = (c.w - 1) / 2
            if abs(x - mid) > half:
                return None
            return CRYSTAL_HOT if abs(abs(x - mid) - half) < 0.8 else (CRYSTAL if (x + y) % 2 else CRYSTAL_DEEP)
        return CRYSTAL_DEEP
    def blade_paint(c):
        for y in range(c.h):
            for x in range(c.w):
                c.clear(x, y)
        glowing(blade, 0.35)(c)
    P.add(glaive, (-0.5, -36, -2.5), (1, 9, 5), faces(blade_paint))                        # crystal blade
    P.apply()
    m.save()


def thrall():
    """A vanilla-proportioned Enderman (3 blocks), wearing the Court's purpur bond-collar."""
    m = Model("enderman_thrall", 64, 64, seed=53)
    m.preview = {"right_arm": [0.1, 0, 0.05], "left_arm": [-0.1, 0, -0.05]}
    P = Pack(m)
    torso = m.part("body")
    P.add(torso, (-4, -16, -2), (8, 12, 4), faces(painter(skin)))
    head = m.part("head", (0, -16, 0))
    P.add(head, (-4, -8, -4), (8, 8, 8), faces(painter(skin), front=face("thrall")))
    P.add(torso, (-4.5, -17, -4.5), (9, 2, 9), faces(painter(collar)))                     # bond-collar
    for side, sx in (("right", -1), ("left", 1)):
        arm = m.part(f"{side}_arm", (5 * sx, -14, 0))
        P.add(arm, (-1, -2, -1), (2, 30, 2), faces(painter(skin)), side == "left", "arm")
        leg = m.part(f"{side}_leg", (2 * sx, -4, 0))
        P.add(leg, (-1, 0, -1), (2, 28, 2), faces(painter(skin)), side == "left", "leg")
    P.apply()
    m.save()


def build():
    lord(); marshal(); riftguard(); thrall()


if __name__ == "__main__":
    build()
