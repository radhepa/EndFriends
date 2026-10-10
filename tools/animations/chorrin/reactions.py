from kit import clip
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _motion import sampled, env, sn  # noqa: E402

# Reactions to gifts, friendship, apologies and blows. They play on their own layer for a moment, so they are the
# bigger moves: a joyful blink-hop, a crown dipped in thanks, a startled half-blink when struck.


# -- happy ------------------------------------------------------------------------------------------------------

@clip("happy_blink_hop", "Joyful blink-hop", trigger="happy", length=2.6, weight=3, mirror="free", blend=(0.15, 0.3))
def _(c):
    c.key(0.3, root_pos=(0, 1.2, 0), waist=(12, 0, 0), ra=(28, 0, 10), la=(28, 0, 10), head=(8, 0, 0),
          crown=(-6, 0, 0))
    c.key(0.5, root_pos=(0, -6, 0), waist=(-8, 0, 0), ra=(-12, 0, 150), la=(-12, 0, 150), rf=(-10, 0, 0),
          lf=(-10, 0, 0), rl=(-14, 0, 0), ll=(-14, 0, 0), head=(-16, 0, 0), crown=(-20, 0, 0))
    c.key(0.72, root_pos=(0, -6.5, 0), ra=(-12, 0, 160), la=(-12, 0, 160), crown=(-10, 0, 0))
    c.key(0.95, root_pos=(0, 1, 0), waist=(8, 0, 0), ra=(-10, 0, 120), la=(-10, 0, 120), rl=(0, 0, 0),
          ll=(0, 0, 0), head=(4, 0, 0), crown=(18, 0, 0))
    # a smaller second hop, crown still bouncing
    c.key(1.15, root_pos=(0, -2.4, 0), waist=(-4, 0, 0), ra=(-12, 0, 150), la=(-12, 0, 150), head=(-10, 0, 6),
          crown=(-12, 0, -6))
    c.key(1.4, root_pos=(0, 0.5, 0), waist=(4, 0, 0), head=(-2, 0, -4), crown=(10, 0, 6))
    c.key(1.8, root_pos=(0, 0, 0), waist=(0, 0, 0), ra=(-6, 0, 14), la=(-6, 0, 14), rf=(0, 0, 0), lf=(0, 0, 0),
          head=(-4, 0, 0), crown=(-5, 0, 0))
    c.key(2.2, ra=(0, 0, 0), la=(0, 0, 0), head=(0, 0, 0), crown=(2, 0, 0))
    c.key(2.6)


@clip("happy_crown_shimmy", "Crown shimmy", trigger="happy", length=2.8, weight=2, mirror="free")
def _(c):
    c.key(0.3, ra=(-30, 20, 30), rf=(-30, 0, 0), la=(-30, 20, 30), lf=(-30, 0, 0), head=(-6, 0, 0),
          root_pos=(0, 0.4, 0))

    def shimmy(t):
        e = env(t, 0.3, 2.3, 0.3)
        return dict(root=(0, 8 * sn(t, 0.5) * e, 3 * sn(t, 0.5, 0.25) * e),
                    head=(-6, -6 * sn(t, 0.5) * e, 8 * sn(t, 0.5, 0.1) * e),
                    crown=(-4, 0, 18 * sn(t, 0.5, -0.05) * e),
                    root_pos=(0, 0.4 - 0.5 * abs(sn(t, 0.5)) * e, 0))
    sampled(c, 0.3, 2.3, shimmy, step=0.0625)
    c.key(2.4, ra=(0, 0, 6), rf=(-6, 0, 0), la=(0, 0, 6), lf=(-6, 0, 0))
    c.key(2.8)


# -- thanks -----------------------------------------------------------------------------------------------------

@clip("thanks_brow", "Raises the gift to its brow", trigger="thanks", length=3.2, weight=3, require=["adult"],
      mirror="free")
def _(c):
    # taken in both open hands, lifted to the brow as the head bows to meet it (the crown is where a Chorrin keeps
    # what it honours), held a breath while the crown trembles, then lowered with a small nod
    recv = dict(ra=(-60, -25, 10), rf=(-14, 0, 0), la=(-60, -25, 10), lf=(-14, 0, 0))
    lift = dict(ra=(-106, -15, 10), rf=(-16, 0, 0), la=(-106, -15, 10), lf=(-16, 0, 0))
    c.key(0.35, head=(10, 0, 0), crown=(2, 0, 0), **recv)
    c.key(0.6, head=(12, 0, 0), root_pos=(0, 0.3, 0))
    c.key(1.05, head=(18, 0, 0), waist=(8, 0, 0), crown=(8, 0, 0), root_pos=(0, 0, 0), **lift)
    c.wobble(1.1, 1.75, 7, "crown", 6, base=(8, 0, 0), axis=2)
    c.key(1.75, head=(20, 0, 0), waist=(9, 0, 0), **lift)
    c.key(2.2, ra=(-32, -14, 0), rf=(-46, 0, 0), la=(-32, -14, 0), lf=(-46, 0, 0), head=(2, 0, 0), waist=(0, 0, 0),
          crown=(-4, 0, 0))
    c.key(2.5, head=(10, 0, 0), crown=(6, 0, 0))
    c.key(2.85, ra=(-6, 0, 2), rf=(-8, 0, 0), la=(-6, 0, 2), lf=(-8, 0, 0), head=(0, 0, 0), crown=(0, 0, 0))
    c.key(3.2)


@clip("thanks_double_nod", "Grateful double nod", trigger="thanks", length=2.4, weight=2, mirror="free")
def _(c):
    # both hands clasped together in front (the hand-on-heart is the greeting's), then two quick nods
    c.key(0.35, ra=(-50, -30, 6), rf=(-50, 0, 0), la=(-50, -30, 6), lf=(-50, 0, 0), head=(-4, 0, 0))
    c.key(0.6, head=(20, 0, 0), crown=(6, 0, 0), waist=(4, 0, 0), root_pos=(0, 0.3, 0))
    c.key(0.85, head=(2, 0, 0), crown=(14, 0, 0), waist=(1, 0, 0), root_pos=(0, 0, 0))
    c.key(1.1, head=(18, 0, 0), crown=(0, 0, 0), waist=(4, 0, 0), root_pos=(0, 0.3, 0))
    c.key(1.35, head=(0, 0, 0), crown=(12, 0, 0), waist=(0, 0, 0), root_pos=(0, 0, 0))
    c.key(1.7, ra=(-8, 0, 2), rf=(-10, 0, 0), la=(-8, 0, 2), lf=(-10, 0, 0), head=(-2, 0, 0), crown=(-4, 0, 0))
    c.key(2.0, crown=(2, 0, 0))
    c.key(2.4)


# -- decline ----------------------------------------------------------------------------------------------------

@clip("decline_shake", "Slow head shake", trigger="decline", length=2.8, weight=3)
def _(c):
    c.key(0.35, ra=(-56, 10, 0), rf=(-84, 0, 0), root_pos=(0, 0, 0.6), head=(4, 0, 0))
    c.cycle(0.45, 1.85, 0.7, dict(head=(6, 22, 0), crown=(0, 0, 10)), dict(head=(6, -22, 0), crown=(0, 0, -10)))
    c.key(2.2, head=(8, 0, 0), crown=(4, 0, 0), ra=(-8, 0, 2), rf=(-10, 0, 0), root_pos=(0, 0, 0))
    c.key(2.8)


@clip("decline_push_back", "Pushes it gently back", trigger="decline", length=2.8, weight=2, require=["adult"])
def _(c):
    c.key(0.4, ra=(-58, -14, 0), rf=(-48, 0, 0), la=(-58, -14, 0), lf=(-48, 0, 0), head=(6, 0, 0))
    c.key(0.8, ra=(-80, -8, 0), rf=(-20, 0, 0), la=(-80, -8, 0), lf=(-20, 0, 0), waist=(2, 0, 0),
          root_pos=(0, 0, 0.4))
    c.key(1.4, ra=(-10, 0, 4), rf=(-14, 0, 0), la=(-10, 0, 4), lf=(-14, 0, 0), waist=(0, 20, 0), head=(-6, 26, -6),
          crown=(-6, 0, 10), root_pos=(0, 0, 0))
    c.key(2.1, waist=(0, 18, 0), head=(-4, 24, -6), crown=(-2, 0, 8))
    c.key(2.5, ra=(0, 0, 0), rf=(0, 0, 0), la=(0, 0, 0), lf=(0, 0, 0), waist=(0, 4, 0), head=(0, 4, 0), crown=(0, 0, 0))
    c.key(2.8)


# -- pleased: a sorry accepted ----------------------------------------------------------------------------------

@clip("pleased_warm_hum", "Warm hum and a nod", trigger="pleased", length=3.4, weight=3)
def _(c):
    # the shoulders let go, a hand to the heart, the crown lifts and sways: all is mended
    c.key(0.4, root_pos=(0, 0.5, 0), ra=(4, 0, 4), la=(4, 0, 4), head=(8, 0, 0), crown=(6, 0, 0))
    c.key(0.9, root_pos=(0, -0.5, 0), ra=(-55, -36, 4), rf=(-54, 0, 0), la=(0, 0, 2), head=(-6, 0, 0),
          crown=(-10, 0, 0), waist=(-2, 0, 0))

    def hum(t):
        e = env(t, 0.9, 2.6, 0.35)
        return dict(crown=(-10 + 4 * e, 0, 12 * sn(t - 0.9, 1.1) * e), head=(-6 + 10 * e, 0, 5 * sn(t - 0.9, 1.1, -0.1) * e))
    sampled(c, 0.9, 2.6, hum, step=0.1)
    c.key(3.0, root_pos=(0, 0, 0), ra=(-6, 0, 2), rf=(-8, 0, 0), la=(0, 0, 0), head=(0, 0, 0), crown=(0, 0, 0),
          waist=(0, 0, 0))
    c.key(3.4)


# -- annoyed: still upset with you ------------------------------------------------------------------------------

@clip("annoyed_turn", "Turns away with a grumble", trigger="annoyed", length=3.2, weight=3)
def _(c):
    c.key(0.3, root_pos=(0, 0.5, 0), head=(10, 0, 0), crown=(6, 0, 0), ra=(6, 0, 0), la=(6, 0, 0))
    # a low grumbling hum: the crown bristles, the body swings away, the chin goes up
    c.key(0.75, root=(0, -34, 0), head=(-12, -26, 0), waist=(-4, -6, 0), crown=(-8, 0, 0), ra=(14, 0, 4),
          la=(14, 0, 4), root_pos=(0, 0, 0))
    c.wobble(0.75, 1.6, 9, "crown", 5, base=(-8, 0, 0), axis=2)
    c.key(2.3, root=(0, -36, 0), head=(-14, -28, 0), waist=(-4, -6, 0), crown=(-8, 0, 0))
    c.key(2.8, root=(0, -8, 0), head=(-2, -6, 0), waist=(0, 0, 0), crown=(2, 0, 0), ra=(0, 0, 0), la=(0, 0, 0))
    c.key(3.2)


@clip("annoyed_stomp", "Stomps a heavy foot", trigger="annoyed", length=2.4, weight=2, mirror="free")
def _(c):
    c.key(0.4, rl=(-26, 0, 2), root=(0, 0, -3), head=(14, 0, 0), waist=(4, 0, 0), ra=(10, 0, 10), la=(10, 0, 10),
          crown=(-6, 0, 0))
    c.key(0.55, rl=(4, 0, 0), root=(0, 0, 0), root_pos=(0, 0.8, 0), head=(18, 0, 0), crown=(14, 0, 0),
          ra=(6, 0, 14), la=(6, 0, 14))
    c.wobble(0.6, 1.4, 8, "crown", 8, base=(6, 0, 0), axis=2, decay=0.6)
    c.key(0.8, rl=(0, 0, 0), root_pos=(0, 0, 0))
    c.key(1.5, head=(16, 10, 0), crown=(4, 0, 0), waist=(4, 0, 0))
    c.key(2.0, head=(4, 4, 0), crown=(0, 0, 0), waist=(0, 0, 0), ra=(0, 0, 0), la=(0, 0, 0))
    c.key(2.4)


# -- hurt -------------------------------------------------------------------------------------------------------

@clip("hurt_flinch", "Flinches behind its arms", trigger="hurt", length=1.6, weight=3, blend=(0.06, 0.3))
def _(c):
    c.key(0.1, waist=(12, 0, 0), head=(14, 0, 0), ra=(-62, -22, 0), rf=(-86, 0, 0), la=(-62, -22, 0),
          lf=(-86, 0, 0), root_pos=(0, 0.6, 1.4), crown=(-14, 0, 0))
    c.key(0.25, waist=(10, 0, 0), head=(16, 0, 4), crown=(10, 0, 0), root_pos=(0, 0.5, 1.6))
    c.key(0.7, waist=(5, 0, 0), head=(8, 0, 2), ra=(-30, -10, 0), rf=(-40, 0, 0), la=(-30, -10, 0),
          lf=(-40, 0, 0), crown=(-4, 0, 0), root_pos=(0, 0.2, 0.6))
    c.key(1.1, waist=(0, 0, 0), head=(0, 0, 0), ra=(0, 0, 0), rf=(0, 0, 0), la=(0, 0, 0), lf=(0, 0, 0),
          crown=(2, 0, 0), root_pos=(0, 0, 0))
    c.key(1.6)


@clip("hurt_startle_blink", "Startled half-blink", trigger="hurt", length=1.8, weight=2, mirror="free",
      blend=(0.05, 0.3))
def _(c):
    # struck, a Chorrin's body tries to blink away: a jolt up and out, arms flung, a heavy landing
    c.key(0.12, root_pos=(0, -3.5, 0.8), ra=(-10, 0, 56), la=(-10, 0, 56), rf=(-20, 0, 0), lf=(-20, 0, 0),
          head=(-14, 0, 0), crown=(-22, 0, 0), waist=(-6, 0, 0))
    c.key(0.32, root_pos=(0, 1.2, 0.6), ra=(10, 0, 18), la=(10, 0, 18), rf=(-10, 0, 0), lf=(-10, 0, 0),
          head=(14, 0, 0), crown=(18, 0, 0), waist=(10, 0, 0))
    c.wobble(0.32, 1.1, 8, "root", 2.5, axis=2, decay=0.6)
    c.key(0.75, root_pos=(0, 0.3, 0.2), head=(6, 0, 0), crown=(-6, 0, 0), waist=(4, 0, 0))
    c.key(1.2, root_pos=(0, 0, 0), ra=(0, 0, 0), la=(0, 0, 0), rf=(0, 0, 0), lf=(0, 0, 0), head=(0, 0, 0),
          crown=(2, 0, 0), waist=(0, 0, 0))
    c.key(1.8)
