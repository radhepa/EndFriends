"""Shared painting helpers and End palettes for the people models."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from mobkit import shade, mix, hexc  # noqa: E402,F401

SIDES = ("front", "back", "left", "right")

# Purpur / shulker shell
SHELL = ["#a57ba6", "#9f74a0", "#ab82ac"]
SHELL_LIGHT = "#c39dc3"
SHELL_RIM = "#d8b9d7"
SHELL_DARK = "#7f567f"
SHELL_DEEP = "#5a395b"
HOLLOW = "#22152a"          # inside a shell, in its own shadow
# Void cloth
VOID = ["#2c2242", "#281e3d", "#30264a"]
VOID_DARK = "#1b1430"
VOID_LIGHT = "#3d3259"
TRIM = ["#b48fb6", "#ab85ad"]
ROD = "#f4effa"             # end rod white
ROD_DIM = "#cfc4e0"
# End stone
STONE = ["#dcdd9f", "#d6d898", "#e0e2a6", "#d3d594"]
STONE_LIGHT = "#ecedbd"
STONE_DARK = ["#c4c588", "#bdbe81"]
STONE_DEEP = "#a6a76d"
# Chorus
CHORUS = ["#5f3f62", "#664668", "#58395b"]
CHORUS_LIGHT = "#8d6b90"
CHORUS_HI = "#a98aac"
CHORUS_DEEP = "#3f2742"
FLOWER = ["#cdb2d6", "#c5a8cf", "#d3bbdb"]
FLOWER_LIGHT = "#ede0f1"
FLOWER_DARK = "#9c7aa8"
# Ender glow
EYE_GLOW = "#cf8cff"
EYE_HOT = "#f0d2ff"
EYE_DEEP = "#7a3fb0"


def tone(c, y, col, k=0.14):
    """Banded darkening toward the bottom of side faces; undersides darker still."""
    if c.face in SIDES and c.h > 2:
        f = 1 - k * y / (c.h - 1)
    elif c.face == "bottom":
        f = 1 - k * 1.4
    else:
        f = 1.0
    return shade(col, round(f * 16) / 16)


def ring_u(c, w, d):
    """Column offset of a side face when walking round a box, so patterns continue round corners."""
    return {"front": 0, "left": w, "back": w + d, "right": w + d + w}.get(c.face, 0)


def glow_as(c, x, y, base, light):
    """A lit pixel whose emissive layer is a darker shade, so the additive glow keeps its hue."""
    if not c.inside(x, y):
        return
    c.set(x, y, base)
    c.model.glow_image().putpixel((c.x0 + x, c.y0 + y), hexc(light))


class _Tint:
    """A canvas stand-in that passes every colour written through fn (the glow layer is untouched)."""

    def __init__(self, c, fn):
        self._c, self._fn = c, fn

    def __getattr__(self, k):
        return getattr(self._c, k)

    def set(self, x, y, col):
        if col is not None:
            self._c.set(x, y, self._fn(hexc(col)))

    def glow(self, x, y, col):
        self._c.glow(x, y, self._fn(hexc(col)))

    def fill(self, col):
        for y in range(self.h):
            for x in range(self.w):
                self.set(x, y, col)

    def rect(self, x, y, w, h, col):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, col)

    def noise(self, pal, x=0, y=0, w=None, h=None):
        for yy in range(y, y + (self.h if h is None else h)):
            for xx in range(x, x + (self.w if w is None else w)):
                self.set(xx, yy, self.pick(pal))


def tinted(face_painters, fn):
    """Recolour a faces() dict: every colour its painters write goes through fn(rgba) -> colour."""
    return {f: (lambda p: (lambda c: p(_Tint(c, fn))))(p) if p else None for f, p in face_painters.items()}


def young(amount=0.35, toward="#efe3f2", floor=200):
    """Paler and softer, for a child's shell or skin; very dark colours (hollows, eyes) stay as they are."""
    def fn(col):
        return col if sum(col[:3]) < floor else mix(col, toward, amount)
    return fn


def painter(fn):
    """fn(c, x, y) -> colour or None, applied to every pixel of a face."""
    def run(c):
        for y in range(c.h):
            for x in range(c.w):
                col = fn(c, x, y)
                if col is not None:
                    c.set(x, y, col)
    return run
