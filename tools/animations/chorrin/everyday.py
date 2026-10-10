from kit import clip
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _motion import sampled, env, sn  # noqa: E402

# Everyday moments of the Chorrin: heavy, rooted end-stone folk who hum instead of speaking, tend the chorus that
# grows from their heads, and blink a short hop when something startles them. Most of these suit sprouts too.


@clip("hum_sway", "Humming sway", length=5.0, weight=3, mirror="free")
def _(c):
    # a slow low hum: the body rocks over planted feet, the head and then the crown follow a beat behind
    def pose(t):
        e = env(t, 0, 5.0, 1.1)
        return dict(root=(0, 0, 2.6 * sn(t, 2.5) * e),
                    waist=(1.5 * e, 0, 1.6 * sn(t, 2.5, -0.08) * e),
                    head=(7 * e, 4 * sn(t, 5.0) * e, 4.5 * sn(t, 2.5, -0.15) * e),
                    crown=(2 * sn(t, 1.25) * e, 0, 11 * sn(t, 2.5, -0.3) * e),
                    ra=(0, 0, 2.5 * sn(t, 2.5, -0.25) * e),
                    la=(0, 0, -2.5 * sn(t, 2.5, -0.25) * e))
    sampled(c, 0, 5.0, pose, step=0.125)


@clip("crown_tend", "Tends the crown", length=4.4, weight=2, require=["adult"])
def _(c):
    # the hand comes up in front and the fingers find the crown's side branch (not through the head)
    c.key(0.5, ra=(-100, 0, 4), rf=(-40, 0, 0), head=(4, 0, -4))
    c.key(0.95, ra=(-135, 0, 0), rf=(-42, 0, 0), head=(9, 0, -13), crown=(0, 0, -6), la=(4, 0, 3))
    # picking at a stem: the hand works, the crown gives a little with each tug
    c.key(1.3, ra=(-132, 0, 2), rf=(-50, 0, 0), crown=(0, 0, -11))
    c.key(1.6, ra=(-136, 0, 0), rf=(-40, 0, 0), crown=(0, 0, -4))
    c.key(1.9, ra=(-132, 0, 2), rf=(-50, 0, 0), crown=(2, 0, -12), head=(10, 0, -14))
    c.key(2.25, ra=(-136, 0, 0), rf=(-40, 0, 0), crown=(0, 0, -5))
    c.key(2.6, ra=(-134, 0, 1), rf=(-46, 0, 0), crown=(0, 0, -9), head=(9, 0, -12))
    # let go: the crown springs back past upright
    c.key(3.0, ra=(-96, 0, 4), rf=(-30, 0, 0), crown=(0, 0, 8), head=(2, 0, -3), la=(0, 0, 0))
    c.key(3.35, ra=(-30, 0, 6), rf=(-12, 0, 0), crown=(0, 0, -4), head=(-3, 0, 0))
    c.key(3.8, ra=(4, 0, 0), rf=(0, 0, 0), crown=(0, 0, 2), head=(0, 0, 0))
    c.key(4.4)


@clip("blink_hop", "Little blink-hop", length=2.2, weight=1, mirror="free")
def _(c):
    c.key(0.3, root_pos=(0, 1, 0), waist=(12, 0, 0), ra=(22, 0, 8), la=(22, 0, 8), head=(6, 0, 0), crown=(-4, 0, 0))
    c.key(0.48, root_pos=(0, -4.5, 0), waist=(-5, 0, 0), ra=(-25, 0, 32), la=(-25, 0, 32), rl=(-10, 0, 0),
          ll=(-10, 0, 0), head=(-10, 0, 0), crown=(-14, 0, 0))
    c.key(0.66, root_pos=(0, -5, 0), waist=(-3, 0, 0), ra=(-20, 0, 36), la=(-20, 0, 36), crown=(-8, 0, 0))
    c.key(0.88, root_pos=(0, 1, 0), waist=(10, 0, 0), ra=(8, 0, 14), la=(8, 0, 14), rl=(0, 0, 0), ll=(0, 0, 0),
          head=(8, 0, 0), crown=(16, 0, 0))
    c.key(1.15, root_pos=(0, -0.4, 0), waist=(-2, 0, 0), ra=(-4, 0, 4), la=(-4, 0, 4), head=(-3, 0, 0),
          crown=(-7, 0, 0))
    c.key(1.45, root_pos=(0, 0, 0), waist=(1, 0, 0), ra=(0, 0, 0), la=(0, 0, 0), head=(1, 0, 0), crown=(4, 0, 0))
    c.key(1.8, crown=(-1.5, 0, 0), waist=(0, 0, 0), head=(0, 0, 0))
    c.key(2.2)


@clip("sky_wonder", "Wonders at the sky", length=5.2, weight=2, mirror="free")
def _(c):
    c.key(0.8, head=(-30, -14, 0), waist=(-4, 0, 0), crown=(8, 0, 0), ra=(6, 0, 3), la=(6, 0, 3))
    c.key(2.2, head=(-36, 12, 3), waist=(-6, 4, 0), crown=(12, 0, -4))
    c.key(3.4, head=(-33, 24, 5), waist=(-5, 7, 0), crown=(10, 0, -6), ra=(6, 0, 3), la=(6, 0, 3))
    # a little shake of the head: so far away
    c.key(3.8, head=(-14, 10, 0), waist=(-2, 3, 0), crown=(-6, 0, 3))
    c.key(4.1, head=(-6, -8, 0), crown=(5, 0, -5))
    c.key(4.4, head=(-2, 5, 0), crown=(-3, 0, 3), waist=(0, 0, 0), ra=(0, 0, 0), la=(0, 0, 0))
    c.key(5.2)


@clip("long_stretch", "Long-armed stretch", length=3.8, weight=2, require=["adult"], mirror="free")
def _(c):
    c.key(0.4, ra=(-60, 0, 30), la=(-60, 0, 30), rf=(-50, 0, 0), lf=(-50, 0, 0), waist=(4, 0, 0))
    c.key(1.0, ra=(-12, 0, 158), la=(-12, 0, 158), rf=(-8, 0, 0), lf=(-8, 0, 0), waist=(-10, 0, 0),
          head=(-22, 0, 0), crown=(10, 0, 0), root_pos=(0, -1, 0))
    c.wobble(1.0, 1.9, 6, "root", 1.2, axis=2)
    c.key(1.9, ra=(-14, 0, 162), la=(-14, 0, 162), waist=(-12, 0, 0), head=(-24, 0, 0), crown=(12, 0, 0),
          root_pos=(0, -1.2, 0))
    # arms swing down heavily, the shoulders roll and settle
    c.key(2.4, ra=(14, 0, 22), la=(14, 0, 22), rf=(-20, 0, 0), lf=(-20, 0, 0), waist=(6, 0, 0), head=(6, 0, 0),
          crown=(-8, 0, 0), root_pos=(0, 0.4, 0))
    c.key(2.8, ra=(-6, 0, 4), la=(-6, 0, 4), rf=(-4, 0, 0), lf=(-4, 0, 0), waist=(-1, 0, 0), head=(-2, 0, 0),
          crown=(4, 0, 0), root_pos=(0, 0, 0))
    c.key(3.2, ra=(2, 0, 0), la=(2, 0, 0), crown=(-1, 0, 0))
    c.key(3.8)


@clip("sprout_hum", "Hums to the shoulder sprout", length=4.2, weight=1, require=["adult"], mirror="never")
def _(c):
    # the little sprout on the left shoulder gets a private song: shoulder lifted to meet the face, a cupped hand
    c.key(0.5, head=(8, -20, 4), la=(-4, 0, 7), crown=(0, 0, 3))
    c.key(1.0, head=(16, -36, 9), la=(-8, 0, 13), lf=(-12, 0, 0), ra=(-55, -40, 12), rf=(-39, 0, 0),
          waist=(3, -6, 2), crown=(4, 0, 8))
    c.key(1.6, head=(18, -38, 12), crown=(6, 0, 14), la=(-8, 0, 15))
    c.key(2.2, head=(15, -35, 7), crown=(3, 0, 2), la=(-7, 0, 12))
    c.key(2.8, head=(18, -38, 12), crown=(6, 0, 14), la=(-8, 0, 15), ra=(-57, -41, 12), rf=(-42, 0, 0))
    c.key(3.3, head=(4, -10, 2), la=(0, 0, 2), lf=(0, 0, 0), ra=(-6, -6, 0), rf=(-8, 0, 0), waist=(0, 0, 0),
          crown=(0, 0, -5))
    c.key(3.7, head=(0, 2, 0), crown=(0, 0, 2), ra=(2, 0, 0), rf=(0, 0, 0))
    c.key(4.2)


@clip("ground_pat", "Pats the earth", length=4.4, weight=1, require=["adult"])
def _(c):
    # a deep bow and a long arm down to the end stone underfoot (the hand reaches the ground in front of the
    # feet, the other hand braced on the thigh): pat, pat, pat, and a satisfied nod
    c.key(0.7, waist=(24, 0, 0), head=(18, 0, 0), ra=(-34, 0, 6), rf=(-20, 0, 0), la=(-24, 0, 8), lf=(-26, 0, 0),
          root_pos=(0, 1.2, 0), crown=(-6, 0, 0))
    for i, t in enumerate((1.0, 1.35, 1.7)):
        c.key(t, ra=(-42, 0, 6), rf=(-34, 0, 0))
        c.key(t + 0.17, ra=(-28, 0, 6), rf=(-3, 0, 0), crown=(-6 + 3 * (i % 2), 0, 0))
    c.key(2.2, head=(22, 0, -6))
    c.key(2.7, waist=(-2, 0, 0), head=(-6, 0, 0), ra=(0, 0, 0), rf=(0, 0, 0), la=(0, 0, 0), lf=(0, 0, 0),
          root_pos=(0, 0, 0), crown=(8, 0, 0))
    c.key(3.1, head=(6, 0, 0), crown=(-4, 0, 0), waist=(0, 0, 0))
    c.key(3.5, head=(-2, 0, 0), crown=(2, 0, 0))
    c.key(4.4)


@clip("hum_beat", "Hums a beat", length=4.2, weight=2)
def _(c):
    def pose(t):
        e = env(t, 0, 4.2, 0.6)
        beat = max(0.0, sn(t, 0.7)) ** 2
        lag = max(0.0, sn(t, 0.7, -0.12)) ** 2
        return dict(head=(9 * beat * e, 0, -3 * e),
                    crown=(10 * lag * e, 0, 4 * sn(t, 1.4) * e),
                    ra=(-10 * beat * e, 0, 6 * e),
                    rf=(-14 * beat * e, 0, 0),
                    root_pos=(0, 0.35 * beat * e, 0),
                    waist=(2 * beat * e, 0, 1.5 * e))
    sampled(c, 0, 4.2, pose, step=0.0875)


@clip("dust_off", "Brushes off stone dust", length=3.8, weight=1, require=["adult"])
def _(c):
    c.key(0.4, head=(14, 0, 0), waist=(4, 0, 0))
    for i, t in enumerate((0.55, 1.05)):
        c.key(t, ra=(-42, -18, 0), rf=(-70, 0, 0))
        c.key(t + 0.3, ra=(-38, -30, 0), rf=(-56, 0, 0), waist=(4, -4, 0))
    # the other side, then a heavy shake of both arms
    c.key(1.7, ra=(-4, 0, 0), rf=(-10, 0, 0), la=(-42, -18, 0), lf=(-70, 0, 0), head=(14, 6, 0), waist=(4, 4, 0))
    c.key(2.0, la=(-38, -30, 0), lf=(-56, 0, 0))
    c.key(2.35, la=(0, 0, 4), lf=(0, 0, 0), ra=(0, 0, 4), rf=(0, 0, 0), head=(2, 0, 0), waist=(0, 0, 0))
    c.wobble(2.35, 3.1, 7, "root", 1.8, axis=2, decay=0.6)
    c.wobble(2.35, 3.1, 7, "crown", 9, axis=2, decay=0.5)
    c.key(3.3, la=(0, 0, 0), ra=(0, 0, 0), head=(0, 0, 0))
    c.key(3.8)


@clip("crown_shake", "Shakes out the crown", length=2.6, weight=1, mirror="free")
def _(c):
    c.key(0.3, head=(6, 0, 0), ra=(0, 0, 4), la=(0, 0, 4), root_pos=(0, 0.4, 0))
    c.wobble(0.35, 1.45, 6, "head", 14, base=(6, 0, 0), axis=2, decay=0.35)
    c.wobble(0.45, 1.8, 6, "crown", 22, axis=2, decay=0.55)
    c.wobble(0.4, 1.5, 6, "root", 2.2, axis=2, decay=0.5)
    c.key(1.45, ra=(0, 0, 10), la=(0, 0, 10), root_pos=(0, 0, 0))
    c.key(1.9, head=(-4, 0, 0), ra=(0, 0, 0), la=(0, 0, 0))
    c.key(2.6)


@clip("drowsy_droop", "Drowsy droop", length=5.2, weight=1)
def _(c):
    c.key(1.2, head=(16, 0, 3), crown=(6, 0, 0), waist=(4, 0, 0), ra=(-4, 0, 0), la=(-4, 0, 0))
    c.key(2.6, head=(30, 0, 6), crown=(14, 0, 4), waist=(8, 0, 0), ra=(-8, 0, -2), la=(-8, 0, -2),
          root_pos=(0, 0.5, 0))
    c.key(3.0, head=(33, 0, 7), crown=(18, 0, 5))
    # a jolt awake, the crown flicks back, a puzzled look around
    c.key(3.18, head=(-10, 0, 0), crown=(-16, 0, 0), waist=(-4, 0, 0), ra=(-14, 0, 10), la=(-14, 0, 10),
          root_pos=(0, -1.2, 0))
    c.key(3.5, head=(-2, 22, 0), crown=(8, 0, -6), waist=(0, 0, 0), ra=(0, 0, 3), la=(0, 0, 3), root_pos=(0, 0, 0))
    c.key(4.0, head=(-2, -18, 0), crown=(-4, 0, 6))
    c.key(4.5, head=(2, 0, 0), crown=(2, 0, 0), ra=(0, 0, 0), la=(0, 0, 0))
    c.key(5.2)


@clip("root_settle", "Settles into the stone", length=4.0, weight=2, mirror="free")
def _(c):
    # weight rocks onto one wide foot, then the other, and sinks: rooted
    c.key(0.6, root=(0, 0, -3.5), root_pos=(-0.8, 0, 0), rl=(0, 0, 2), ll=(0, 0, 4), head=(0, 0, 3),
          crown=(0, 0, 6))
    c.key(1.3, root=(0, 0, 3.5), root_pos=(0.8, 0, 0), rl=(0, 0, 4), ll=(0, 0, 2), head=(0, 0, -3),
          crown=(0, 0, -7))
    c.key(1.9, root=(0, 0, -1.5), root_pos=(-0.3, 0, 0), rl=(0, 0, 0), ll=(0, 0, 0), head=(0, 0, 1),
          crown=(0, 0, 4))
    c.key(2.4, root=(0, 0, 0), root_pos=(0, 0.6, 0), waist=(3, 0, 0), head=(6, 0, 0), crown=(-5, 0, 0),
          ra=(0, 0, 3), la=(0, 0, 3))
    c.key(3.2, root_pos=(0, 0.5, 0), waist=(2, 0, 0), head=(5, 0, 0), crown=(2, 0, 0))
    c.key(4.0)


@clip("cradle_fruit", "Cradles a chorus fruit", length=5.4, weight=2, require=["adult"], mirror="free")
def _(c):
    hold = dict(ra=(-40, -24, 0), rf=(-78, 0, 0), la=(-40, -24, 0), lf=(-78, 0, 0))
    c.key(0.7, head=(18, 0, 0), crown=(6, 0, 0), **hold)
    # rocking it gently, humming, then lifting it to eye level to admire
    c.key(1.4, root=(0, 0, 2.5), head=(22, 0, -5), crown=(4, 0, -6))
    c.key(2.1, root=(0, 0, -2.5), head=(22, 0, 5), crown=(4, 0, 7))
    c.key(2.7, root=(0, 0, 0), head=(4, 0, 0), crown=(-4, 0, 0), ra=(-62, -24, 0), rf=(-82, 0, 0),
          la=(-62, -24, 0), lf=(-82, 0, 0))
    c.key(3.5, head=(2, 0, 6), crown=(-2, 0, 6), ra=(-64, -22, 0), la=(-64, -22, 0))
    c.key(4.1, head=(16, 0, 0), crown=(4, 0, 0), **hold)
    c.key(4.8, ra=(0, 0, 2), rf=(-6, 0, 0), la=(0, 0, 2), lf=(-6, 0, 0), head=(0, 0, 0), crown=(-2, 0, 0))
    c.key(5.4)


@clip("void_ward", "Wards off the void", length=3.8, weight=1, require=["adult"])
def _(c):
    # superstitious: a wary look over the shoulder toward the edge, a thump on the chest, a touch to the crown
    # (the head turns less than the body: the clip adds to wherever they are already looking)
    c.key(0.5, head=(4, 34, 0), waist=(0, 18, 0), crown=(0, 0, -5))
    c.key(1.0, head=(6, 42, 0), waist=(0, 24, 0))
    c.key(1.3, head=(0, 6, 0), waist=(0, 2, 0), ra=(-50, -36, 0), rf=(-46, 0, 0), crown=(0, 0, 4))
    c.key(1.45, ra=(-44, -38, 0), rf=(-40, 0, 0), root_pos=(0, 0.3, 0))
    c.key(1.6, ra=(-50, -36, 0), rf=(-46, 0, 0), root_pos=(0, 0, 0))
    c.key(1.75, ra=(-44, -38, 0), rf=(-40, 0, 0))
    c.key(2.2, ra=(-135, 0, 0), rf=(-42, 0, 0), head=(9, 0, -12), waist=(0, 0, 0), crown=(0, 0, -10))
    c.key(2.55, ra=(-132, 0, 2), rf=(-48, 0, 0), crown=(0, 0, 5))
    c.key(3.1, ra=(-6, 0, 2), rf=(-6, 0, 0), head=(0, 0, 0), crown=(0, 0, -2))
    c.key(3.8)


@clip("look_about", "Curious look about", length=4.6, weight=2, mirror="free")
def _(c):
    c.key(0.7, head=(4, 38, 4), waist=(0, 10, 0), crown=(0, 0, -6))
    c.key(1.4, head=(6, 42, 14), waist=(0, 12, 0), crown=(0, 0, 8))
    c.key(1.7, head=(2, 34, 10))
    c.key(2.5, head=(2, -36, -4), waist=(0, -10, 0), crown=(0, 0, 9))
    c.key(3.2, head=(-4, -40, -10), waist=(0, -12, 0), crown=(0, 0, -6))
    c.key(3.8, head=(1, -4, 0), waist=(0, -2, 0), crown=(0, 0, 3))
    c.key(4.6)
