"""How an Endarch answers what you do: tribute and Favor, an apology, an insult, a blow.

Their joy is a lifted chin and a gift of the hand; their refusal is a backhand and a turned head. Even hurt, an
Endarch glitches like the Endermen they rule before it recovers its dignity. Reactions play over whatever the body
is doing, so they keep to the arms, head and waist; the ones that lift the right hand high leave the Riftguard out.
"""
from kit import clip

CHEST = dict(ra=(-10, -40, 0), rf=(-135, 0, 0))
# hands clasped at the small of the back (outside the robe, mantle and cape), and the way there: arms swung back
# first, forearms folded in only after, so they never sweep through the robe or the cape
BEHIND = dict(ra=(30, 0, 4), rf=(-8, 0, -42), la=(30, 0, 4), lf=(-8, 0, -42))
SWING = dict(ra=(24, 0, 7), rf=(-4, 0, -6), la=(24, 0, 7), lf=(-4, 0, -6))


def glaive_behind(c, start, held, release, end):
    """With the hands clasped behind, a Riftguard's glaive swings up past the shoulder to stand along its spine
    (and back down after), so it never runs through the body. Other bodies have no glaive and skip it. A clip
    that uses this never mirrors: the glaive stays on the right forearm."""
    if start > 0:
        c.key(start, glaive=(0, 0, 0))
    c.key((start + held) / 2, glaive=(-60, 55, 0))
    c.hold(held, release, glaive=(-105, 30, 15))
    c.key((release + end) / 2, glaive=(-60, 55, 0))
    c.key(end, glaive=(0, 0, 0))


@clip("happy_approval", "Rare approval", trigger="happy", length=3.2, weight=3, require=["adult"], mirror="never")
def _(c):
    # the chin lifts, the hands open a little at the sides, one slow satisfied nod: this pleases the Court
    c.key(0.5, head=(-12, 0, 0), waist=(-3, 0, 0), mantle=(3, 0, 0), cape=(3, 0, 0),
          ra=(-6, 0, 12), rf=(-16, 0, 0), la=(-6, 0, 12), lf=(-16, 0, 0))
    c.key(0.7, head=(-13, 0, 0), ra=(-7, 0, 14), la=(-7, 0, 14))
    c.key(1.4, head=(12, 0, 0), waist=(1, 0, 0), mantle=(-1, 0, 0), cape=(-1, 0, 0))
    c.key(1.8, head=(10, 0, 0))
    c.key(2.4, head=(-8, 0, 0), waist=(-2, 0, 0), mantle=(2, 0, 0), cape=(2, 0, 0),
          ra=(-4, 0, 8), rf=(-10, 0, 0), la=(-4, 0, 8), lf=(-10, 0, 0))
    c.key(3.2)


@clip("happy_bestow_favor", "Bestow Favor", trigger="happy", length=3.8, weight=2, require=["adult"],
      avoid=["rank:riftguard"])
def _(c):
    # the right hand rises high over the guest, palm down, holds there, and comes down wide in an arc
    c.key(0.4, ra=(-20, 0, 6), rf=(-30, 0, 0), head=(2, 0, 0))
    c.key(1.0, ra=(-130, 0, 10), rf=(-20, 0, 0), head=(-12, 0, 0), waist=(-3, 0, 0), mantle=(3, 0, 0),
          cape=(3, 0, 0))
    c.key(1.15, ra=(-134, 0, 10), rf=(-17, 0, 0), head=(-13, 0, 0))
    c.key(2.0, ra=(-130, 0, 10), rf=(-20, 0, 0), head=(-10, 0, 0))
    c.key(2.7, ra=(-60, 20, 50), rf=(-10, 0, 0), head=(4, 0, 0), waist=(1, 0, 0), mantle=(-1, 0, 0),
          cape=(-1, 0, 0))
    c.key(3.8)


@clip("thanks_accept_tribute", "Accept the tribute", trigger="thanks", length=3.2, weight=3, require=["adult"],
      avoid=["rank:riftguard"])
def _(c):
    # the hand comes out palm up, closes on the offering, and draws it to the breast; a nod of receipt
    c.key(0.6, ra=(-45, 0, 8), rf=(-30, 0, 0), head=(8, 0, 0))
    c.key(0.9, ra=(-47, 0, 8), rf=(-26, 0, 0))
    c.key(1.2, ra=(-44, 0, 8), rf=(-60, 0, 0), head=(6, 0, 0))
    c.key(1.8, **CHEST, head=(10, 0, 0))
    c.key(2.2, **CHEST, head=(-4, 0, 0))
    c.key(3.2)


@clip("thanks_gracious_wave", "Gracious wave", trigger="thanks", length=2.8, weight=3, require=["adult"],
      mirror="never")
def _(c):
    # the head inclines a degree or two and the left hand turns over lazily: it is accepted, you may go
    c.key(0.6, head=(10, 0, 4), la=(-25, 0, 15), lf=(-40, 0, 0))
    c.key(1.0, la=(-27, 0, 17), lf=(-40, 22, 0), head=(11, 0, 4))
    c.key(1.4, la=(-27, 0, 17), lf=(-42, -18, 0), head=(4, 0, 2))
    c.key(1.8, la=(-20, 0, 12), lf=(-36, 6, 0), head=(-4, 0, 0))
    c.key(2.8)


@clip("decline_wave_away", "Wave it away", trigger="decline", length=2.8, weight=3, require=["adult"],
      mirror="never")
def _(c):
    # the head turns from the offering and the back of the left hand sweeps it away, twice
    c.key(0.35, la=(-30, -20, 0), lf=(-60, 0, 0), head=(-2, 10, 0))
    c.key(0.6, la=(-25, 30, 30), lf=(-15, 0, 0), head=(-8, 22, 0))
    c.key(0.85, la=(-30, -14, 2), lf=(-55, 0, 0))
    c.key(1.1, la=(-26, 32, 32), lf=(-14, 0, 0), head=(-9, 24, 0))
    c.key(1.8, la=(-10, 10, 10), lf=(-10, 0, 0), head=(-8, 20, 0), waist=(0, 5, 0))
    c.key(2.8)


@clip("decline_disdain", "Disdainful refusal", trigger="decline", length=3.2, weight=2, require=["adult"],
      mirror="never", boost={"manner:proud": 2})
def _(c):
    # a look down at the thing, the head recoils, the body draws back, and a palm comes up: no
    c.key(0.5, head=(16, 0, 0), waist=(2, 0, 0))
    c.key(0.8, head=(14, 0, 0))
    c.key(1.1, head=(-12, 10, -4), waist=(-4, 0, 0), mantle=(4, 0, 0), cape=(4, 0, 0), la=(-50, 0, 15),
          lf=(-60, 0, 0))
    c.key(1.25, head=(-14, 11, -5), la=(-52, 0, 16), lf=(-58, 0, 0))
    c.key(2.2, head=(-11, 9, -4), waist=(-4, 0, 0), mantle=(4, 0, 0), cape=(4, 0, 0), la=(-48, 0, 15),
          lf=(-60, 0, 0))
    c.key(3.2)


@clip("pleased_absolution", "Absolution", trigger="pleased", length=3.6, weight=3, require=["adult"],
      mirror="never")
def _(c):
    # the left hand lifts palm down over the penitent and is laid slowly on the air; a long, slow nod
    c.key(0.8, la=(-62, 0, 10), lf=(-30, 0, 0), head=(-6, 0, 0))
    c.key(1.0, la=(-64, 0, 10), lf=(-28, 0, 0))
    c.key(1.8, la=(-50, 0, 10), lf=(-36, 0, 0), head=(14, 0, 0), waist=(2, 0, 0), mantle=(-1, 0, 0),
          cape=(-1, 0, 0))
    c.key(2.3, la=(-46, 0, 10), lf=(-36, 0, 0), head=(12, 0, 0))
    c.key(2.9, la=(-10, 0, 4), lf=(-12, 0, 0), head=(-4, 0, 0), waist=(0, 0, 0), mantle=(0, 0, 0), cape=(0, 0, 0))
    c.key(3.6)


@clip("pleased_settle", "Composure restored", trigger="pleased", length=3.4, weight=2, require=["adult"],
      mirror="never")
def _(c):
    # the shoulders let go of their stiffness, a breath out, and the hands find each other behind the back
    c.key(0.7, waist=(-4, 0, 0), mantle=(4, 0, 0), cape=(4, 0, 0), head=(-8, 0, 0), ra=(4, 0, 8), la=(4, 0, 8))
    c.key(1.4, waist=(2, 0, 0), mantle=(-2, 0, 0), cape=(-2, 0, 0), head=(9, 0, 0), ra=(2, 0, 0), la=(2, 0, 0),
          rf=(0, 0, 0), lf=(0, 0, 0))
    c.key(1.8, **SWING)
    c.key(2.3, **BEHIND, waist=(-1, 0, 0), mantle=(1, 0, 0), cape=(1, 0, 0), head=(-4, 0, 0))
    c.key(2.7, **BEHIND, head=(-5, 4, 0))
    c.key(3.05, **SWING)
    c.key(3.4)
    glaive_behind(c, 1.4, 2.3, 2.7, 3.4)


@clip("annoyed_turn_away", "Turn the shoulder", trigger="annoyed", length=3.8, weight=3, require=["adult"],
      mirror="never")
def _(c):
    # the body turns its shoulder on you, hands clasped hard behind, the chin high and looking elsewhere
    c.key(0.5, **SWING)
    c.key(0.6, root=(0, -18, 0), head=(-4, -10, 0), waist=(0, -4, 0))
    c.key(1.0, **BEHIND, root=(0, -34, 0), head=(-11, -22, 0), waist=(0, -6, 0), mantle=(3, 0, 0), cape=(3, 0, 0))
    c.key(1.15, root=(0, -36, 0), head=(-12, -24, 0))
    c.key(2.8, **BEHIND, root=(0, -33, 0), head=(-11, -20, 0), waist=(0, -6, 0), mantle=(3, 0, 0), cape=(3, 0, 0))
    c.key(3.3, **SWING)
    c.key(3.8)
    glaive_behind(c, 0, 1.0, 2.8, 3.8)


@clip("annoyed_loom_glare", "Looming glare", trigger="annoyed", length=3.6, weight=2, require=["adult"],
      mirror="free")
def _(c):
    # slowly the tall body leans down over you, head low and still; then it straightens all at once
    c.key(1.2, waist=(7, 0, 0), mantle=(-6, 0, 0), cape=(-6, 0, 0), head=(18, 0, 4), rf=(-10, 0, 0),
          lf=(-12, 0, 0), ra=(-4, 0, 4), la=(-4, 0, 4))
    c.key(2.1, waist=(7, 2, 0), mantle=(-6, 0, 0), cape=(-6, 0, 0), head=(19, 3, 5))
    c.key(2.4, waist=(-3, 0, 0), mantle=(3, 0, 0), cape=(3, 0, 0), head=(-10, 0, 0), rf=(0, 0, 0), lf=(0, 0, 0),
          ra=(0, 0, 0), la=(0, 0, 0))
    c.key(2.6, waist=(-2, 0, 0), head=(-9, 0, 0))
    c.key(3.6)


@clip("hurt_recoil", "Recoil", trigger="hurt", length=1.6, weight=3, require=["adult"], blend=(0.05, 0.35))
def _(c):
    # the head snaps back, the arms fly out and the body rocks back before it steadies (the right foot only
    # gives a little: a bigger kick runs the thigh out through the back of a Lord's robe)
    c.key(0.12, head=(-24, 6, 4), waist=(-6, 0, 0), mantle=(6, 0, 0), cape=(6, 0, 0), ra=(-28, 0, 30),
          rf=(-25, 0, 0), la=(-34, 0, 34), lf=(-30, 0, 0), rl=(4, 0, 0), rs=(3, 0, 0), root_pos=(0, 0, 0.8))
    c.key(0.3, head=(-18, 4, 2), waist=(-5, 0, 0), mantle=(5, 0, 0), cape=(5, 0, 0), ra=(-22, 0, 24),
          la=(-28, 0, 28), root_pos=(0, 0, 0.6))
    c.key(0.8, head=(4, 0, 0), waist=(2, 0, 0), mantle=(-1, 0, 0), cape=(-1, 0, 0), ra=(-4, 0, 6), rf=(-8, 0, 0),
          la=(-4, 0, 6), lf=(-8, 0, 0), rl=(0, 0, 0), rs=(0, 0, 0))
    c.key(1.6)


@clip("hurt_glitch", "Void glitch", trigger="hurt", length=1.8, weight=3, require=["adult"], blend=(0.04, 0.4),
      mirror="free")
def _(c):
    # like the Endermen it rules: the whole body jerks in little glitches, the head twitching out of step
    jerks = [(0.06, 7, (-6, 14, -8)), (0.13, -6, (4, -12, 9)), (0.2, 5, (-8, 10, 4)), (0.28, -5, (2, -9, -7)),
             (0.36, 4, (-5, 6, 6)), (0.45, -3, (0, -4, -3))]
    for t, yaw, h in jerks:
        c.key(t, root=(0, yaw, 0), head=h, waist=(-3, 0, yaw * 0.6), ra=(-12, 0, 10 + yaw), la=(-12, 0, 10 - yaw))
    c.key(0.6, root=(0, 0, 0), head=(-6, 0, 0), waist=(-2, 0, 0), ra=(-6, 0, 8), la=(-6, 0, 8))
    c.key(1.1, head=(-8, 0, 0))
    c.key(1.8)


@clip("hurt_clutch", "Clutch the wound", trigger="hurt", length=2.4, weight=2, require=["adult"],
      blend=(0.05, 0.4), mirror="never")
def _(c):
    # folding a little round the blow, the left hand to the chest; then upright with a cold stare
    c.key(0.15, waist=(8, 0, 0), mantle=(-6, 0, 0), cape=(-6, 0, 0), head=(18, 0, -4), la=(-14, 0, 12),
          lf=(-120, -75, 0), ra=(-14, 0, 10), rf=(-20, 0, 0))
    c.key(0.7, waist=(6, 0, 0), mantle=(-5, 0, 0), cape=(-5, 0, 0), head=(14, 0, -3))
    c.key(1.4, waist=(-2, 0, 0), mantle=(2, 0, 0), cape=(2, 0, 0), head=(-8, 0, 0), la=(-4, 0, 3), lf=(-30, -10, 0),
          ra=(-2, 0, 2), rf=(-4, 0, 0))
    c.key(2.4)


@clip("happy_glaive_lift", "Glaive raised high", trigger="happy", length=3.2, weight=4,
      require=["adult", "rank:riftguard"], mirror="never")
def _(c):
    # the Riftguard's joy, kept ceremonious: the glaive raised high overhead, blade to the void, held there in
    # salute while the chin lifts after it, and brought down
    high = dict(ra=(-150, 0, -10), rf=(-10, 0, 0), glaive=(65, 0, 0))
    c.key(0.35, ra=(-40, 0, 0), rf=(-50, 0, 0), glaive=(20, 0, 0), head=(4, 0, 0))
    c.key(0.8, **high, head=(-18, 0, 0), waist=(-4, 0, 0))
    c.key(1.0, ra=(-153, 0, -10), rf=(-8, 0, 0), glaive=(66, 0, 0), head=(-20, 0, 0))
    c.key(2.0, **high, head=(-17, 0, 0), waist=(-4, 0, 0))
    c.key(2.6, ra=(-20, 0, 2), rf=(-40, 0, 0), glaive=(18, 0, 0), head=(-4, 0, 0), waist=(0, 0, 0))
    c.key(3.2)


@clip("thanks_glaive_dip", "Dip the glaive", trigger="thanks", length=3.0, weight=4,
      require=["adult", "rank:riftguard"], mirror="never")
def _(c):
    # the glaive comes upright, then its blade is dipped toward the giver with a bow of the head
    up = dict(ra=(-8, 0, 0), rf=(-72, 0, 0))
    c.key(0.5, **up, glaive=(0, 0, 0), head=(-4, 0, 0))
    c.key(1.1, **up, glaive=(35, 0, 0), head=(14, 0, 0))
    c.key(1.6, **up, glaive=(33, 0, 0), head=(13, 0, 0))
    c.key(2.1, **up, glaive=(0, 0, 0), head=(-5, 0, 0))
    c.key(3.0)
