from kit import clip
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _motion import sampled, env, sn  # noqa: E402

# Trades of the Steads, mimed with big three-fingered hands. Weights keep the trade visible among the everyday
# moments; at their workplace in working hours ("working") they come up far more often.
WORK = {"working": 3}


def job(name):
    return ["adult", "job:" + name]


@clip("grove_prune", "Prunes the chorus", length=5.2, weight=4, require=job("grove_tender"), boost=WORK)
def _(c):
    # one hand steadies a stem, the other pinches off the dead tips; then on to the next stalk
    c.key(0.6, waist=(9, -6, 0), head=(16, -8, 0), la=(-58, -12, 0), lf=(-42, 0, 0), ra=(-48, -24, 0),
          rf=(-62, 0, 0), crown=(4, 0, 0))
    for t in (0.95, 1.45):
        c.key(t, ra=(-54, -28, 0), rf=(-74, 0, 0), crown=(6, 0, -3))
        c.key(t + 0.2, ra=(-44, -20, 0), rf=(-52, 0, 0), crown=(3, 0, 2))
    c.key(1.9, ra=(-30, -6, 8), rf=(-30, 0, 0), head=(12, 10, 0))
    c.key(2.4, waist=(6, 12, 0), head=(4, 14, 0), la=(-82, -6, 0), lf=(-36, 0, 0), ra=(-74, -18, 0),
          rf=(-60, 0, 0), crown=(-2, 0, 4))
    for t in (2.75, 3.25):
        c.key(t, ra=(-80, -22, 0), rf=(-72, 0, 0), crown=(-3, 0, 7))
        c.key(t + 0.2, ra=(-70, -14, 0), rf=(-52, 0, 0), crown=(-1, 0, 1))
    c.key(3.8, ra=(-24, 4, 10), rf=(-24, 0, 0), la=(-40, -6, 0), lf=(-24, 0, 0), head=(6, 6, 0))
    c.key(4.4, waist=(0, 0, 0), head=(0, 0, 0), la=(0, 0, 0), lf=(0, 0, 0), ra=(0, 0, 0), rf=(0, 0, 0),
          crown=(3, 0, 0))
    c.key(5.2)


@clip("grove_coax", "Hums a bud to bloom", length=5.6, weight=3, require=job("grove_tender"), boost=WORK,
      mirror="free")
def _(c):
    cup = dict(ra=(-30, -18, 0), rf=(-42, 0, 0), la=(-30, -18, 0), lf=(-42, 0, 0))
    c.key(0.7, waist=(14, 0, 0), head=(22, 0, 0), root_pos=(0, 0.6, 0), crown=(6, 0, 0), **cup)

    def hum(t):
        e = env(t, 0.7, 3.6, 0.6)
        return dict(crown=(6, 0, 12 * sn(t - 0.7, 1.45) * e), head=(22, 0, 4 * sn(t - 0.7, 1.45, -0.1) * e))
    sampled(c, 0.7, 3.6, hum, step=0.12)
    # the bud opens: the hands rise with it and part, the head comes up pleased
    c.key(3.6, ra=(-48, -14, 0), rf=(-52, 0, 0), la=(-48, -14, 0), lf=(-52, 0, 0), waist=(10, 0, 0),
          root_pos=(0, 0.3, 0))
    c.key(4.2, ra=(-50, 10, 0), rf=(-34, 0, 0), la=(-50, 10, 0), lf=(-34, 0, 0), waist=(4, 0, 0), head=(4, 0, 0),
          crown=(-6, 0, 0), root_pos=(0, 0, 0))
    c.key(4.6, head=(10, 0, 0), crown=(5, 0, 0))
    c.key(5.0, ra=(-6, 0, 2), rf=(-8, 0, 0), la=(-6, 0, 2), lf=(-8, 0, 0), waist=(0, 0, 0), head=(0, 0, 0),
          crown=(-2, 0, 0))
    c.key(5.6)


@clip("kiln_stoke", "Stokes the kiln", length=4.8, weight=4, require=job("kiln_keeper"), boost=WORK)
def _(c):
    # two shoves of a long rake into the kiln mouth, then the back of a hand across a hot brow
    grip = dict(ra=(-62, -16, 0), rf=(-34, 0, 0), la=(-48, -26, 0), lf=(-56, 0, 0))
    c.key(0.5, waist=(4, 0, 0), head=(8, 0, 0), root_pos=(0, 0, 1), **grip)
    for t in (0.9, 1.9):
        c.key(t, ra=(-82, -10, 0), rf=(-12, 0, 0), la=(-70, -20, 0), lf=(-30, 0, 0), waist=(12, 0, 0),
              root_pos=(0, 0.4, -1.4), head=(12, 0, 0), crown=(8, 0, 0))
        c.key(t + 0.5, waist=(4, 0, 0), root_pos=(0, 0, 1), head=(6, 0, 0), crown=(-4, 0, 0), **grip)
    c.key(3.0, la=(0, 0, 0), lf=(0, 0, 0), ra=(-121, -20, 4), rf=(-96, 0, 0), head=(12, 0, -4), waist=(0, 0, 0),
          root_pos=(0, 0, 0), crown=(4, 0, 0))
    c.key(3.45, ra=(-112, -12, 0), rf=(-92, 0, 0), head=(10, 0, 4))
    c.key(4.0, ra=(-6, 0, 2), rf=(-6, 0, 0), head=(-2, 0, 0), crown=(-2, 0, 0))
    c.key(4.8)


@clip("kiln_peer", "Peers into the kiln", length=4.2, weight=3, require=job("kiln_keeper"), boost=WORK)
def _(c):
    c.key(0.7, waist=(12, 0, 0), head=(14, 0, 0), ra=(-111, -18, 8), rf=(-84, 0, 0), la=(-14, 0, 6),
          crown=(8, 0, 0))
    c.key(1.6, waist=(14, 0, 0), head=(16, 6, 0))
    # too hot: back from the glow, a waft of the hand, a nod - it's coming along
    c.key(1.9, waist=(-5, 0, 0), head=(-10, 0, 0), ra=(-94, -10, 0), rf=(-70, 0, 0), root_pos=(0, 0, 0.8),
          crown=(-10, 0, 0))
    c.key(2.2, ra=(-78, 8, 0), rf=(-50, 0, 0), crown=(4, 0, 0))
    c.key(2.45, ra=(-86, -6, 0), rf=(-64, 0, 0))
    c.key(2.7, ra=(-78, 8, 0), rf=(-50, 0, 0))
    c.key(3.1, ra=(-10, 0, 2), rf=(-10, 0, 0), la=(0, 0, 0), waist=(0, 0, 0), head=(10, 0, 0),
          root_pos=(0, 0, 0), crown=(2, 0, 0))
    c.key(3.45, head=(-2, 0, 0))
    c.key(4.2)


@clip("stone_chisel", "Chisels stone", length=5.0, weight=4, require=job("stonecutter"), boost=WORK)
def _(c):
    hold = dict(la=(-50, -22, 0), lf=(-32, 0, 0))
    c.key(0.5, waist=(10, 0, 0), head=(18, 0, 0), ra=(-60, -20, 0), rf=(-40, 0, 0), **hold)
    t = 0.8
    for i in range(4):
        c.key(t, ra=(-118, -14, 0), rf=(-66, 0, 0), waist=(7, 0, 0), crown=(-4, 0, 0))
        c.key(t + 0.32, ra=(-56, -22, 0), rf=(-28, 0, 0), waist=(12, 0, 0), crown=(6, 0, 2 if i % 2 else -2),
              root_pos=(0, 0.3, 0))
        c.key(t + 0.45, ra=(-62, -20, 0), rf=(-34, 0, 0), waist=(11, 0, 0), root_pos=(0, 0, 0))
        t += 0.68
    # check the edge with a thumb
    c.key(3.6, ra=(-50, -30, 0), rf=(-50, 0, 0), head=(22, 0, 6), crown=(4, 0, 0))
    c.key(4.0, ra=(-48, -26, 0), rf=(-44, 0, 0), head=(20, 0, -3))
    c.key(4.5, ra=(-4, 0, 2), rf=(-6, 0, 0), la=(-4, 0, 2), lf=(-6, 0, 0), waist=(0, 0, 0), head=(0, 0, 0),
          crown=(-2, 0, 0))
    c.key(5.0)


@clip("stone_heave", "Heaves a block", length=4.6, weight=3, require=job("stonecutter"), boost=WORK,
      mirror="free")
def _(c):
    grab = dict(ra=(-30, -8, 0), rf=(-20, 0, 0), la=(-30, -8, 0), lf=(-20, 0, 0))
    hug = dict(ra=(-62, -22, 0), rf=(-78, 0, 0), la=(-62, -22, 0), lf=(-78, 0, 0))
    c.key(0.6, root_pos=(0, 1.2, 0), waist=(18, 0, 0), head=(14, 0, 0), crown=(-6, 0, 0), **grab)
    c.key(0.85, root_pos=(0, 1.4, 0), waist=(19, 0, 0))
    c.key(1.5, root_pos=(0, -0.3, 0), waist=(-6, 0, 0), head=(-6, 0, 0), crown=(8, 0, 0), **hug)
    c.wobble(1.5, 2.1, 7, "root", 1.2, axis=2)
    c.key(2.4, waist=(2, 26, 0), head=(4, 18, 0), root_pos=(0, 0, 0), crown=(0, 0, -6))
    c.key(2.9, waist=(16, 30, 0), head=(16, 20, 0), root_pos=(0, 1, 0), crown=(-4, 0, 0), **grab)
    c.key(3.3, waist=(2, 8, 0), head=(-4, 4, 0), root_pos=(0, 0, 0), ra=(0, 0, 6), rf=(-8, 0, 0), la=(0, 0, 6),
          lf=(-8, 0, 0), crown=(6, 0, 3))
    c.key(3.7, waist=(-3, 0, 0), head=(-6, 0, 0), crown=(-3, 0, 0), ra=(0, 0, 0), la=(0, 0, 0))
    c.key(4.6)


@clip("gather_pick", "Picks chorus fruit", length=5.4, weight=4, require=job("gatherer"), boost=WORK,
      mirror="never")
def _(c):
    # up on the toes for a fruit high on the stalk (reaching up in front, clear of the head), a twist and a tug,
    # passed to the other hand and patted into the pouch on the left hip; once more
    for t0, side in ((0.0, 1), (2.5, -1)):
        c.key(t0 + 0.6, ra=(-155, -10, 0), rf=(-8, 0, 0), head=(-26, 6 * side, -4), waist=(-4, 0, 0),
              root_pos=(0, -0.8, 0), crown=(10, 0, 0), la=(-6, 0, 4), lf=(0, 0, 0))
        c.key(t0 + 0.95, ra=(-150, -10, 2), rf=(-26, 0, 0), crown=(14, 0, -4))
        c.key(t0 + 1.15, ra=(-155, -10, 0), rf=(-10, 0, 0), crown=(8, 0, 3))
        c.key(t0 + 1.35, ra=(-138, -10, 4), rf=(-44, 0, 0), root_pos=(0, 0, 0), crown=(12, 0, 0))
        c.key(t0 + 1.8, ra=(-50, -28, 4), rf=(-40, 0, 0), la=(-50, -28, 4), lf=(-40, 0, 0), head=(16, 0, 0),
              waist=(2, 0, 0), crown=(-4, 0, 0))
        c.key(t0 + 2.15, ra=(-8, 0, 4), rf=(-10, 0, 0), la=(-14, 0, 6), lf=(-35, 0, 0), head=(18, -20, 0),
              waist=(4, -6, 0))
        c.key(t0 + 2.3, la=(-18, 0, 4), lf=(-46, 0, 0))
    c.key(5.05, ra=(-4, 0, 2), rf=(-6, 0, 0), head=(0, 0, 0), waist=(0, 0, 0), la=(0, 0, 0), lf=(0, 0, 0),
          crown=(2, 0, 0))
    c.key(5.4)


@clip("gather_sort", "Sorts the gathering", length=4.8, weight=3, require=job("gatherer"), boost=WORK)
def _(c):
    basket = dict(la=(-40, -26, 0), lf=(-74, 0, 0))
    c.key(0.5, head=(18, 0, 0), waist=(5, 0, 0), ra=(-36, -20, 0), rf=(-62, 0, 0), **basket)
    # hold one up to the eyes: a turn, a squint... this one is no good, flicked away
    c.key(1.1, ra=(-92, -22, 0), rf=(-78, 0, 0), head=(-4, 0, 10), crown=(0, 0, 6))
    c.key(1.5, ra=(-96, -18, 0), rf=(-72, 0, 0), head=(-2, 4, -8), crown=(0, 0, -5))
    c.key(1.9, ra=(-70, 40, 10), rf=(-20, 0, 0), head=(4, 26, 0), crown=(0, 0, 4))
    c.key(2.1, ra=(-58, 48, 12), rf=(-10, 0, 0))
    c.key(2.6, ra=(-36, -20, 0), rf=(-62, 0, 0), head=(18, 0, 0), crown=(0, 0, 0))
    # this one is good: a pleased bob, into the basket
    c.key(3.1, ra=(-88, -22, 0), rf=(-80, 0, 0), head=(0, 0, 4))
    c.key(3.35, head=(8, 0, 4), crown=(8, 0, 0), root_pos=(0, 0.3, 0))
    c.key(3.6, ra=(-44, -24, 0), rf=(-72, 0, 0), head=(16, 0, 0), crown=(-3, 0, 0), root_pos=(0, 0, 0))
    c.key(4.2, ra=(-4, 0, 2), rf=(-6, 0, 0), la=(-4, 0, 2), lf=(-6, 0, 0), head=(0, 0, 0), waist=(0, 0, 0),
          crown=(1, 0, 0))
    c.key(4.8)


@clip("cook_stir", "Stirs the pot", length=5.2, weight=4, require=job("cook"), boost=WORK)
def _(c):
    def stir(t):
        e = env(t, 0.2, 4.6, 0.6)
        return dict(ra=((-46 + 9 * sn(t, 1.1)) * e, (-12 + 14 * sn(t, 1.1, 0.25)) * e, 0),
                    rf=(-44 * e, 0, 0),
                    waist=(6 * e, 3 * sn(t, 1.1, 0.25) * e, 0),
                    head=(18 * e, 5 * sn(t, 1.1, 0.15) * e, 0),
                    crown=(3 * e, 0, 6 * sn(t, 1.1, 0.05) * e),
                    la=(-6 * e, 0, 14 * e), lf=(-40 * e, 0, 0))
    sampled(c, 0, 4.6, stir, step=0.1)
    c.key(5.2)


@clip("cook_taste", "Wafts the steam", length=4.4, weight=3, require=job("cook"), boost=WORK)
def _(c):
    # no mouth to taste with: a Chorrin cook wafts the steam up and judges by the smell
    c.key(0.5, waist=(10, 0, 0), head=(16, 0, 0), ra=(-50, -14, 0), rf=(-40, 0, 0))
    for t in (0.8, 1.3):
        c.key(t, ra=(-72, -16, 0), rf=(-80, 0, 0), head=(4, 0, 0), waist=(6, 0, 0))
        c.key(t + 0.3, ra=(-48, -14, 0), rf=(-36, 0, 0), head=(12, 0, 0), waist=(9, 0, 0))
    c.key(2.0, head=(-8, 0, 6), waist=(-2, 0, 0), ra=(-20, 0, 6), rf=(-20, 0, 0), crown=(-6, 0, 4))
    c.key(2.5, head=(-10, 0, -6), crown=(-4, 0, -6))
    # mm: a slow approving nod, the crown bobs along
    c.key(2.9, head=(10, 0, 0), crown=(10, 0, 0))
    c.key(3.2, head=(-2, 0, 0), crown=(-4, 0, 0))
    c.key(3.5, head=(8, 0, 0), crown=(6, 0, 0))
    c.key(3.9, head=(0, 0, 0), crown=(0, 0, 0), ra=(0, 0, 0), rf=(0, 0, 0), waist=(0, 0, 0))
    c.key(4.4)


@clip("blinker_ready", "Readies a blink", length=4.0, weight=4, require=job("blinker"), boost=WORK, mirror="free")
def _(c):
    # a courier's ritual: tug the sash tight, coil low, quiver... and decide it is not time yet
    c.key(0.45, ra=(-55, -38, 12), rf=(-38, 0, 0), head=(10, 0, 0))
    c.key(0.65, ra=(-50, -34, 8), rf=(-30, 0, 0), root_pos=(0, 0.3, 0))
    c.key(1.0, ra=(24, 0, 10), rf=(-10, 0, 0), la=(24, 0, 10), lf=(-10, 0, 0), waist=(14, 0, 0), head=(4, 0, 0),
          root_pos=(0, 1.2, 0), crown=(-8, 0, 0))
    c.wobble(1.0, 1.8, 10, "root", 1.4, axis=2)
    c.wobble(1.0, 1.8, 10, "crown", 6, base=(-8, 0, 0), axis=2)
    c.key(1.8, root_pos=(0, 1.3, 0), waist=(15, 0, 0))
    c.key(2.05, root_pos=(0, -2.2, 0), waist=(-4, 0, 0), ra=(-40, 0, 20), la=(-40, 0, 20), rf=(-20, 0, 0),
          lf=(-20, 0, 0), head=(-8, 0, 0), crown=(-14, 0, 0))
    c.key(2.35, root_pos=(0, 0.4, 0), waist=(5, 0, 0), ra=(4, 0, 6), la=(4, 0, 6), rf=(-6, 0, 0), lf=(-6, 0, 0),
          head=(6, 0, 0), crown=(12, 0, 0))
    c.key(2.7, root_pos=(0, 0, 0), waist=(0, 0, 0), head=(4, 18, 6), crown=(-4, 0, 4), ra=(0, 0, 0), la=(0, 0, 0),
          rf=(0, 0, 0), lf=(0, 0, 0))
    c.key(3.3, head=(2, 4, 2), crown=(2, 0, -2))
    c.key(4.0)


@clip("brewer_swirl", "Swirls a brew", length=4.6, weight=4, require=job("brewer"), boost=WORK)
def _(c):
    c.key(0.6, ra=(-74, -18, 0), rf=(-66, 0, 0), la=(-46, -26, 0), lf=(-70, 0, 0), head=(10, 0, 0))

    def swirl(t):
        e = env(t, 0.6, 2.6, 0.3)
        return dict(ra=(-74 + 5 * sn(t, 0.42) * e, -18 + 6 * sn(t, 0.42, 0.25) * e, 0),
                    crown=(0, 0, 4 * sn(t, 0.84) * e))
    sampled(c, 0.6, 2.6, swirl, step=0.05)
    # up to the eye and a long critical look; a tilt of the head; a satisfied hum
    c.key(3.0, ra=(-110, -26, 0), rf=(-70, 0, 0), head=(-8, 0, 8), crown=(0, 0, 6))
    c.key(3.5, ra=(-112, -24, 0), head=(-6, 0, -6), crown=(0, 0, -6))
    c.key(3.8, head=(6, 0, 0), crown=(8, 0, 0))
    c.key(4.2, ra=(-6, 0, 2), rf=(-8, 0, 0), la=(-4, 0, 2), lf=(-6, 0, 0), head=(0, 0, 0), crown=(0, 0, 0))
    c.key(4.6)


@clip("herder_call", "Hums the herd home", length=5.0, weight=4, require=job("herder"), boost=WORK)
def _(c):
    # a long arm high and swinging slow so the herd sees it, a deep hum, then two big beckons
    c.key(0.6, ra=(-14, 0, 150), rf=(-10, 0, 0), head=(-12, -10, 0), waist=(-3, -8, 0), crown=(6, 0, 0))

    def wave(t):
        e = env(t, 0.6, 2.6, 0.4)
        return dict(ra=(-14, 0, 150 + 16 * sn(t - 0.6, 1.0) * e), crown=(6, 0, -8 * sn(t - 0.6, 1.0, -0.1) * e))
    sampled(c, 0.6, 2.6, wave, step=0.1)
    for t in (2.9, 3.6):
        c.key(t, ra=(-100, 8, 0), rf=(-10, 0, 0), head=(0, -10, 0), waist=(4, -8, 0), crown=(-4, 0, 0))
        c.key(t + 0.4, ra=(-70, -10, 0), rf=(-96, 0, 0), head=(4, -8, 0), waist=(-2, -6, 0), crown=(5, 0, 0))
    c.key(4.5, ra=(-4, 0, 2), rf=(-6, 0, 0), head=(0, 0, 0), waist=(0, 0, 0), crown=(0, 0, 0))
    c.key(5.0)


@clip("hall_sweep", "Sweeps the hall", length=5.4, weight=4, require=job("hallkeeper"), boost=WORK)
def _(c):
    # both hands on an imagined broom: long low strokes across the floor
    def sweep(t):
        e = env(t, 0.1, 4.8, 0.5)
        s = sn(t, 1.4)
        return dict(ra=((-38 - 6 * s) * e, (-10 + 14 * s) * e, 0), rf=(-30 * e, 0, 0),
                    la=((-56 + 4 * s) * e, (-18 + 14 * s) * e, 0), lf=(-52 * e, 0, 0),
                    waist=(10 * e, -14 * s * e, 0), head=(16 * e, -8 * s * e, 0),
                    crown=(2 * e, 0, 5 * sn(t, 1.4, -0.12) * e),
                    root_pos=(0, 0, -0.4 * (1 - abs(s)) * e))
    sampled(c, 0, 4.8, sweep, step=0.1)
    c.key(5.4)


@clip("trader_offer", "Shows off the wares", length=4.8, weight=4, require=job("trader"), boost=WORK)
def _(c):
    # palms up over the goods, a grand sweep of the arm along the stall, then hands rubbed together: well?
    c.key(0.5, ra=(-56, 12, 0), rf=(-32, 0, 0), la=(-56, 12, 0), lf=(-32, 0, 0), head=(6, 0, 0), waist=(4, 0, 0),
          crown=(4, 0, 0))
    c.key(0.8, head=(12, 0, 0), crown=(10, 0, 0))
    c.key(1.05, head=(4, 0, 0), crown=(-2, 0, 0))
    c.key(1.6, ra=(-82, 52, 0), rf=(-10, 0, 0), la=(-10, 0, 4), lf=(-12, 0, 0), head=(0, 30, 0), waist=(2, 14, 0),
          crown=(0, 0, -6))
    c.key(2.3, ra=(-80, 64, 0), rf=(-8, 0, 0), head=(-2, 40, 0), waist=(1, 18, 0), crown=(0, 0, -3))
    c.key(2.8, ra=(-44, -22, 0), rf=(-72, 0, 0), la=(-44, -22, 0), lf=(-72, 0, 0), head=(4, 0, 6), waist=(3, 0, 0),
          crown=(0, 0, 6))
    c.wobble(2.8, 3.7, 6, "rf", 7, base=(-72, 0, 0))
    c.wobble(2.8, 3.7, 6, "lf", 7, base=(-72, 0, 0))
    c.key(3.7, head=(2, 0, 8), crown=(0, 0, 8))
    c.key(4.2, ra=(-4, 0, 2), la=(-4, 0, 2), rf=(-8, 0, 0), lf=(-8, 0, 0), head=(0, 0, 0), waist=(0, 0, 0),
          crown=(0, 0, 0))
    c.key(4.8)
