from kit import clip
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _motion import sampled, env, sn  # noqa: E402

# Sprouts: round, stubby, a head as big as a grown-up's and a single chorus sprout on top. Short arms (no
# forearms), so their play is in the bounce, the arms and that big head. They are still learning to blink.
KID = ["child"]


@clip("sprout_glide", "Pretends to glide", length=3.8, weight=2, require=KID, mirror="free")
def _(c):
    c.key(0.35, ra=(-6, 0, 78), la=(-6, 0, 78), head=(-6, 0, 0), crown=(-6, 0, 0))

    def glide(t):
        e = env(t, 0.35, 3.3, 0.45)
        return dict(root=(0, 26 * sn(t - 0.35, 2.0) * e, -9 * sn(t - 0.35, 2.0, 0.1) * e),
                    root_pos=(0, -0.8 * abs(sn(t - 0.35, 0.5)) * e, 0),
                    ra=(-6, 0, 78 + 10 * sn(t - 0.35, 2.0, 0.15) * e),
                    la=(-6, 0, 78 - 10 * sn(t - 0.35, 2.0, 0.15) * e),
                    head=(-6, 10 * sn(t - 0.35, 2.0, 0.2) * e, 0),
                    crown=(-6, 0, 14 * sn(t - 0.35, 2.0, -0.05) * e))
    sampled(c, 0.35, 3.3, glide, step=0.1)
    c.key(3.8)


@clip("sprout_try_blink", "Tries to blink like the grown-ups", length=3.8, weight=3, require=KID, mirror="free")
def _(c):
    # scrunch up tight, quiver with effort, pop! ...still here. A look around. A droop.
    c.key(0.4, root_pos=(0, 1.2, 0), head=(16, 0, 0), ra=(-34, -30, 0), la=(-34, -30, 0), crown=(10, 0, 0))
    c.wobble(0.4, 1.3, 11, "root", 2, axis=2)
    c.wobble(0.4, 1.3, 11, "crown", 6, base=(10, 0, 0), axis=2)
    c.key(1.3, root_pos=(0, 1.3, 0), head=(18, 0, 0))
    c.key(1.5, root_pos=(0, -3.4, 0), ra=(-8, 0, 70), la=(-8, 0, 70), head=(-12, 0, 0), crown=(-16, 0, 0))
    c.key(1.75, root_pos=(0, 0.4, 0), ra=(0, 0, 30), la=(0, 0, 30), head=(4, 0, 0), crown=(12, 0, 0))
    c.key(1.95, root_pos=(0, 0, 0), crown=(-4, 0, 0))
    c.key(2.3, head=(-2, 34, 0), crown=(0, 0, -6), ra=(0, 0, 10), la=(0, 0, 10))
    c.key(2.75, head=(-2, -34, 0), crown=(0, 0, 6))
    c.key(3.2, head=(20, 0, 4), crown=(16, 0, 4), ra=(4, 0, 0), la=(4, 0, 0), root_pos=(0, 0.4, 0))
    c.key(3.8)


@clip("sprout_frog_hops", "Frog hops", length=3.2, weight=2, require=KID, mirror="free")
def _(c):
    for i, t in enumerate((0.2, 1.1, 2.0)):
        c.key(t + 0.15, root_pos=(0, 1.2, 0), ra=(40, 0, 6), la=(40, 0, 6), head=(10, 0, 0), crown=(-6, 0, 0))
        c.key(t + 0.4, root_pos=(0, -3.6 + 0.6 * i, 0), ra=(-70, 0, 10), la=(-70, 0, 10), head=(-10, 0, 0),
              crown=(-14, 0, 0), rl=(-12, 0, 0), ll=(-12, 0, 0))
        c.key(t + 0.65, root_pos=(0, 0.6, 0), ra=(-10, 0, 8), la=(-10, 0, 8), head=(6, 0, 0), crown=(14, 0, 0),
              rl=(0, 0, 0), ll=(0, 0, 0))
    c.key(2.95, root_pos=(0, 0, 0), ra=(0, 0, 0), la=(0, 0, 0), head=(0, 0, 0), crown=(-3, 0, 0))
    c.key(3.2)


@clip("sprout_head_check", "Checks its sprout is still there", length=3.0, weight=2, require=KID)
def _(c):
    # short arms only reach the sides of that big head: both hands pressed to it (raised a little outward, so
    # they stay outside it), a wiggle to feel for the sprout, which waggles on top
    up = dict(ra=(-174, 0, -6), la=(-174, 0, -6))
    c.key(0.45, head=(-6, 0, 0), crown=(-4, 0, 0), **up)
    c.key(0.8, head=(-4, 10, 4), crown=(0, 0, 18))
    c.key(1.15, head=(-4, -10, -4), crown=(0, 0, -18))
    c.key(1.5, head=(-6, 6, 3), crown=(0, 0, 12))
    # still there: arms down, a happy little bounce
    c.key(1.9, ra=(0, 0, 20), la=(0, 0, 20), head=(0, 0, 0), crown=(0, 0, -4), root_pos=(0, 0.6, 0))
    c.key(2.15, root_pos=(0, -1.6, 0), crown=(-10, 0, 0), head=(-6, 0, 0))
    c.key(2.4, root_pos=(0, 0.3, 0), crown=(8, 0, 0), ra=(0, 0, 6), la=(0, 0, 6), head=(2, 0, 0))
    c.key(3.0)


@clip("sprout_sneak", "Sneaky tiptoe", length=4.0, weight=2, require=KID, mirror="free")
def _(c):
    # mischief: crouched low, tiptoeing side to side, peeking about; then a giggle that gives it all away
    c.key(0.4, root_pos=(0, 1.2, 0), head=(8, 0, 0), ra=(30, 0, 8), la=(30, 0, 8), crown=(6, 0, 0))
    c.key(0.8, root_pos=(-1, 1.2, 0), rl=(-16, 0, 0), head=(6, 30, 0))
    c.key(1.1, root_pos=(-1.4, 1.2, 0), rl=(0, 0, 0))
    c.key(1.5, root_pos=(0, 1.2, 0), ll=(-16, 0, 0), head=(6, -30, 0))
    c.key(1.8, root_pos=(1.4, 1.2, 0), ll=(0, 0, 0))
    c.key(2.2, root_pos=(0.6, 1.2, 0), head=(4, 0, 0), crown=(6, 0, 0))
    c.key(2.4, root_pos=(0.4, 0.6, 0), head=(-8, 0, 0), ra=(-40, -30, 0), la=(-40, -30, 0), crown=(-6, 0, 0))
    c.wobble(2.4, 3.3, 8, "root", 3, axis=2)
    c.wobble(2.4, 3.3, 8, "crown", 10, base=(-6, 0, 0), axis=2)
    c.key(3.3, root_pos=(0, 0, 0), head=(-6, 0, 0))
    c.key(3.6, ra=(0, 0, 0), la=(0, 0, 0), head=(0, 0, 0), crown=(0, 0, 0))
    c.key(4.0)


@clip("sprout_arm_swing", "Swings its arms", length=3.4, weight=2, require=KID, mirror="free")
def _(c):
    def swing(t):
        e = env(t, 0, 3.4, 0.5)
        s = sn(t, 0.85)
        return dict(ra=(-38 * s * e, 0, 4 * e), la=(38 * s * e, 0, 4 * e),
                    root=(0, 9 * s * e, 0),
                    root_pos=(0, -0.5 * abs(s) * e, 0),
                    head=(-3 * e, -5 * s * e, 6 * sn(t, 1.7) * e),
                    crown=(0, 0, 10 * sn(t, 0.85, -0.15) * e))
    sampled(c, 0, 3.4, swing, step=0.07)
