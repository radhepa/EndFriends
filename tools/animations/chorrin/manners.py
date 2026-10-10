from kit import clip
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _motion import sampled, env, sn  # noqa: E402

# Personality shows in how a Chorrin stands about: the flighty half-blink at every sound, the shy hide in their
# own hands, the proud stand like a grown kiln, the restless tap, the steady hum like a hillside.


@clip("flighty_jitter", "Jittery little hops", length=3.0, weight=3, require=["manner:flighty"], mirror="free")
def _(c):
    c.key(0.25, head=(-4, 30, 0), root_pos=(0, 0.6, 0), ra=(-10, 0, 0), la=(-10, 0, 0), rf=(-30, 0, 0),
          lf=(-30, 0, 0), crown=(-6, 0, 0))
    c.key(0.4, root_pos=(0, -2.4, 0), head=(-8, 34, 0), crown=(-12, 0, 4), waist=(-3, 0, 0))
    c.key(0.58, root_pos=(0, 0.5, 0), crown=(8, 0, -4), waist=(3, 0, 0))
    c.key(0.8, root_pos=(0, 0, 0), head=(-2, -30, 0), crown=(-3, 0, 6), waist=(0, 0, 0))
    c.wobble(0.8, 1.4, 9, "crown", 7, base=(-3, 0, 0), axis=2)
    c.key(1.5, head=(-6, -36, 0), root_pos=(0, 0.6, 0), crown=(-6, 0, 0))
    c.key(1.66, root_pos=(0, -2.2, 0), head=(-8, 4, 0), crown=(-12, 0, -4), waist=(-3, 0, 0))
    c.key(1.84, root_pos=(0, 0.5, 0), crown=(9, 0, 3), waist=(3, 0, 0))
    c.key(2.1, root_pos=(0, 0, 0), head=(-2, 8, 0), crown=(-3, 0, 0), waist=(0, 0, 0))
    c.key(2.5, ra=(-4, 0, 0), la=(-4, 0, 0), rf=(-8, 0, 0), lf=(-8, 0, 0), head=(0, 0, 0), crown=(2, 0, 0))
    c.key(3.0)


@clip("shy_fiddle", "Shy fiddling", length=4.6, weight=3, require=["manner:shy"])
def _(c):
    hands = dict(ra=(-22, -22, 0), la=(-22, -22, 0), rf=(-55, 0, 0), lf=(-55, 0, 0))
    c.key(0.6, head=(18, -12, 3), crown=(8, 0, 2), waist=(4, -4, 0), **hands)
    c.wobble(0.6, 2.0, 3, "rf", 8, base=(-55, 0, 0))
    # a peek up, caught, and back down
    c.key(2.3, head=(2, 4, 0), crown=(-2, 0, 0), waist=(1, 0, 0))
    c.key(2.55, head=(3, 6, 0))
    c.key(2.85, head=(22, -16, 5), crown=(10, 0, 4), waist=(5, -5, 0))
    c.wobble(2.85, 3.9, 3, "lf", 8, base=(-55, 0, 0))
    c.key(4.0, ra=(-4, 0, 0), la=(-4, 0, 0), rf=(-10, 0, 0), lf=(-10, 0, 0), head=(8, 0, 0), crown=(2, 0, 0),
          waist=(0, 0, 0))
    c.key(4.6)


@clip("proud_stand", "Stands tall and proud", length=4.8, weight=3, require=["manner:proud"], mirror="free")
def _(c):
    c.key(0.7, waist=(-8, 0, 0), head=(-14, 0, 0), crown=(-6, 0, 0), ra=(12, 0, 8), la=(12, 0, 8),
          root_pos=(0, -0.8, 0))
    c.key(1.8, head=(-12, 28, 0), waist=(-8, 6, 0), crown=(-4, 0, -4))
    c.key(3.0, head=(-12, -26, 0), waist=(-8, -6, 0), crown=(-4, 0, 4))
    c.key(3.7, head=(-14, 0, 0), waist=(-8, 0, 0), crown=(-7, 0, 0))
    c.key(4.2, waist=(-2, 0, 0), head=(-3, 0, 0), crown=(3, 0, 0), ra=(2, 0, 2), la=(2, 0, 2), root_pos=(0, 0, 0))
    c.key(4.8)


@clip("restless_tap", "Restless foot tap", length=4.2, weight=3, require=["manner:restless|manner:busy"])
def _(c):
    def pose(t):
        e = env(t, 0.1, 3.4, 0.4)
        tap = max(0.0, sn(t, 0.5))
        return dict(rl=(-9 * tap * e, 0, 2 * e), root=(0, 0, -1.2 * e),
                    rf=(-8 * max(0.0, sn(t, 0.25)) * e - 10 * e, 0, 0))
    sampled(c, 0, 3.4, pose, step=0.0625)
    c.key(0.9, head=(-2, 32, 0), crown=(0, 0, -5))
    c.key(1.9, head=(-2, -30, 0), crown=(0, 0, 5))
    c.key(2.8, head=(-6, 4, 0), crown=(-5, 0, 0))
    # a long hum of a sigh
    c.key(3.4, head=(10, 0, 0), crown=(8, 0, 0), root_pos=(0, 0.6, 0), ra=(0, 0, 4), la=(0, 0, 4))
    c.key(3.8, head=(2, 0, 0), crown=(-2, 0, 0), root_pos=(0, 0, 0), ra=(0, 0, 0), la=(0, 0, 0))
    c.key(4.2)


@clip("steady_hum", "Deep slow hum", length=6.0, weight=3, require=["manner:steady"], mirror="free")
def _(c):
    def pose(t):
        e = env(t, 0, 6.0, 1.4)
        b = sn(t, 3.0, -0.25)
        return dict(root_pos=(0, -0.5 * b * e, 0),
                    head=(12 * e, 0, 3 * sn(t, 6.0) * e),
                    crown=(3 * b * e, 0, 9 * sn(t, 3.0, -0.1) * e),
                    waist=(2 * e - 1.5 * b * e, 0, 0),
                    ra=(0, 0, 1.5 * b * e), la=(0, 0, 1.5 * b * e))
    sampled(c, 0, 6.0, pose, step=0.15)


@clip("pouch_check", "Checks the hip pouch", length=4.0, weight=1, require=["adult"], boost={"manner:busy": 3},
      mirror="never")
def _(c):
    # the pouch hangs on the left hip: a pat, a rummage, a count of what's there on the other hand
    c.key(0.5, head=(20, -24, 0), la=(-14, 0, 6), lf=(-35, 0, 0), waist=(4, -6, 0))
    c.key(0.75, la=(-18, 0, 4), lf=(-48, 0, 0))
    c.key(0.95, la=(-12, 0, 6), lf=(-32, 0, 0))
    c.key(1.2, la=(-18, 0, 4), lf=(-48, 0, 0))
    c.key(1.7, head=(14, 0, 0), waist=(2, 0, 0), la=(-40, -20, 0), lf=(-70, 0, 0), ra=(-40, -10, 0),
          rf=(-75, 0, 0))
    for i, t in enumerate((2.0, 2.3, 2.6)):
        c.key(t, ra=(-44, -16, 0), rf=(-80, 0, 0), head=(16, 0, 2))
        c.key(t + 0.15, ra=(-40, -10, 0), rf=(-72, 0, 0), head=(14, 0, -1))
    c.key(3.2, head=(0, 0, 0), crown=(-4, 0, 0), la=(0, 0, 0), lf=(0, 0, 0), ra=(0, 0, 0), rf=(0, 0, 0),
          waist=(0, 0, 0))
    c.key(3.5, crown=(3, 0, 0))
    c.key(4.0)
