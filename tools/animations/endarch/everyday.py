"""Everyday moments at the Court: how an Endarch stands about when nobody needs ruling.

Endarchs are very tall, with arms that hang to the knee. They are proud, cold and ceremonious: their idles are slow
and small, made of posture (chin high, hands clasped behind, drawn up to full height) and the odd flicker of the
void in them. A Lord's robe is part of its body, so the waist only ever bends a little; the mantle and cape are
counter-rotated whenever it does.
"""
from kit import clip

# hands clasped at the small of the back, outside the robe, mantle and cape
BEHIND = dict(ra=(30, 0, 4), rf=(-8, 0, -42), la=(30, 0, 4), lf=(-8, 0, -42))
# on the way there and back: the arms are already swung back (and a little out, clear of the mantle's edges) but
# the forearms have not folded in yet, so they never sweep through the robe or the cape
SWING = dict(ra=(24, 0, 7), rf=(-4, 0, -6), la=(24, 0, 7), lf=(-4, 0, -6))


@clip("hands_behind", "Hands clasped behind", length=5.5, weight=3, require=["adult"], mirror="never")
def _(c):
    # both arms swing back, then fold in: the hands meet at the small of the back; chin lifts, chest out (the
    # arms go a little further back than BEHIND, as the chest-out lean brings them nearer the hanging cape)
    deep = dict(BEHIND, ra=(33, 0, 4), la=(33, 0, 4))
    c.key(0.6, **SWING, head=(-4, 0, 0), waist=(-2, 0, 0), mantle=(2, 0, 0), cape=(2, 0, 0))
    c.key(1.2, **deep, head=(-8, 0, 0), waist=(-4, 0, 0), mantle=(4, 0, 0), cape=(4, 0, 0))
    c.key(3.0, ra=(34, 0, 4), rf=(-8, 0, -43), la=(33, 0, 4), lf=(-8, 0, -42),
          head=(-8, 6, 0), waist=(-4, 2, 0), mantle=(4, 0, 0), cape=(4, 0, 0))
    c.key(4.3, **deep, head=(-7, -3, 0), waist=(-3, -1, 0), mantle=(3, 0, 0), cape=(3, 0, 0))
    c.key(4.9, **SWING, head=(-3, -1, 0), waist=(-1, 0, 0), mantle=(1, 0, 0), cape=(1, 0, 0))
    c.key(5.5)
    # a Riftguard stands its glaive upright along the spine, blade behind the head, held in the clasped hands
    c.key(0.6, glaive=(-60, 55, 0))
    c.hold(1.2, 4.3, glaive=(-105, 30, 15))
    c.key(4.9, glaive=(-60, 55, 0))


@clip("survey_court", "Survey the Court", length=6.0, weight=3, require=["adult"], mirror="free")
def _(c):
    # a slow imperious sweep of the head from one side to the other, chin raised; the shoulders follow late
    c.key(1.2, head=(-6, -34, 0), waist=(0, -8, 0), mantle=(0, 0, 0))
    c.hold(1.6, 2.2, head=(-7, -36, 1), waist=(0, -9, 0))
    c.key(3.6, head=(-6, 28, -1), waist=(0, 6, 0))
    c.key(4.0, head=(-5, 32, -1), waist=(0, 8, 0))
    c.key(4.6, head=(-5, 30, -1), waist=(0, 7, 0))
    c.key(6.0)


@clip("draw_up_tall", "Draw up to full height", length=3.8, weight=2, require=["adult"], mirror="never",
      boost={"manner:proud": 2})
def _(c):
    # a small settle first, then the chest lifts, shoulders roll back and the chin rises: looming at rest
    c.key(0.5, waist=(3, 0, 0), head=(4, 0, 0), mantle=(-2, 0, 0), cape=(-2, 0, 0))
    c.key(1.4, waist=(-6, 0, 0), head=(-13, 0, 0), ra=(7, 0, 7), la=(7, 0, 7), rf=(-4, 0, 0), lf=(-4, 0, 0),
          mantle=(6, 0, 0), cape=(6, 0, 0))
    c.key(1.7, waist=(-5, 0, 0), head=(-11, 0, 0), ra=(6, 0, 6), la=(6, 0, 6), mantle=(5, 0, 0), cape=(5, 0, 0))
    c.key(2.7, waist=(-5, 0, 0), head=(-11, 3, 1), ra=(5, 0, 6), la=(5, 0, 6), mantle=(5, 0, 0), cape=(5, 0, 0))
    c.key(3.8)


@clip("regard_fingers", "Regard the fingers", length=4.6, weight=2, require=["adult"], mirror="never")
def _(c):
    # the left hand rises close before the face (a hand's breadth off the eyes) and the long fingers are turned a
    # little this way and that, coolly inspected; the head follows them
    c.key(0.8, la=(-58, -4, 5), lf=(-122, -9, 0), head=(6, -12, -4))
    c.key(1.1, la=(-57, -4, 5), lf=(-125, -9, 0), head=(6, -12, -5))
    c.key(1.8, la=(-57, -2, 7), lf=(-125, 5, 0), head=(5, -10, -8))
    c.key(2.6, la=(-58, -6, 3), lf=(-124, -21, 0), head=(7, -14, 0))
    c.key(3.2, la=(-57, -4, 5), lf=(-125, -9, 0), head=(6, -12, -3))
    c.key(3.8, la=(-14, 0, -3), lf=(-22, 0, 0), head=(-2, -3, 0))
    c.key(4.6)


@clip("flick_dust", "Flick a mote of dust", length=3.2, weight=2, require=["adult"], mirror="never")
def _(c):
    # the left hand crosses to the right shoulder, brushes twice, then flicks the dust away; chin up after. The
    # elbow comes forward and the forearm does the crossing, so the upper arm stays out of the chest
    c.key(0.7, la=(-51, -23, 19), lf=(-127, -48, 0), head=(9, 22, 0))
    c.key(0.95, la=(-49, -21, 19), lf=(-117, -48, 0), head=(9, 21, 0))
    c.key(1.2, la=(-52, -24, 19), lf=(-128, -48, 0), head=(9, 22, 0))
    c.key(1.45, la=(-46, -8, 12), lf=(-68, -10, 0), head=(-4, -6, 0))
    c.key(1.6, la=(-47, -2, 12), lf=(-60, 0, 0), head=(-6, -8, 0))
    c.key(2.2, la=(-10, 0, 0), lf=(-14, 0, 0), head=(-5, -4, 0))
    c.key(3.2)


@clip("void_flicker", "Flicker of the void", length=2.6, weight=1, require=["adult"], blend=(0.08, 0.4),
      mirror="free")
def _(c):
    # the Enderman in them: the head glitches sideways in little jerks, the arms twitch, then a slow tilt
    jit = [(0.12, (-3, 9, -5)), (0.18, (2, -7, 5)), (0.24, (-2, 11, -3)), (0.31, (1, -5, 7)),
           (0.38, (-3, 8, 0)), (0.46, (1, 2, -3))]
    c.key(0.06, head=(0, 0, 0), ra=(0, 0, 0), la=(0, 0, 0), root=(0, 0, 0))
    for i, (t, h) in enumerate(jit):
        s = 1 if i % 2 else -1
        c.key(t, head=h, ra=(-3, 0, 4 + 2 * s), la=(-3, 0, 4 - 2 * s), root=(0, 1.5 * s, 0))
    c.key(0.6, ra=(-1, 0, 2), la=(-1, 0, 2), root=(0, 0, 0))
    c.key(1.4, head=(3, 4, 11))
    c.key(1.9, head=(3, 3, 10))
    c.key(2.6)


@clip("steeple_fingers", "Steepled fingers", length=5.4, weight=2, require=["adult"], avoid=["rank:riftguard"],
      mirror="never")
def _(c):
    # both hands rise and meet before the chest, fingertips touching; a slow scheming tap, the head lowered
    st_r = dict(ra=(-15, 0, 8), rf=(-120, -34, 0))
    st_l = dict(la=(-15, 0, 8), lf=(-120, -34, 0))
    c.key(1.0, ra=(-16, 0, 9), rf=(-124, -32, 0), la=(-16, 0, 9), lf=(-124, -32, 0), head=(9, 0, 0))
    c.key(1.3, **st_r, **st_l, head=(10, 0, 0))
    for i, t in enumerate((1.9, 2.15, 2.4, 2.65, 2.9)):
        o = 4 if i % 2 == 0 else 0
        c.key(t, rf=(-120 - o, -34 + o, 0), lf=(-120 - (4 - o), -34 + (4 - o), 0))
    c.key(3.8, **st_r, **st_l, head=(10, 5, 3))
    c.key(4.5, ra=(-5, 0, 3), rf=(-30, -8, 0), la=(-5, 0, 3), lf=(-30, -8, 0), head=(2, 2, 0))
    c.key(5.4)


@clip("proud_profile", "Proud profile", length=4.2, weight=1, require=["adult"], mirror="free",
      boost={"manner:proud": 3})
def _(c):
    # the head turns sharply aside, chin up, and holds the profile as if for a portrait
    c.key(0.5, head=(3, -5, 0))
    c.key(1.05, head=(-11, 41, -3), waist=(0, 6, 0))
    c.key(1.2, head=(-12, 44, -3), waist=(0, 7, 0))
    c.key(1.5, head=(-11, 40, -3), waist=(0, 6, 0))
    c.key(3.0, head=(-10, 39, -2), waist=(0, 5, 0))
    c.key(4.2)


@clip("adjust_crown", "Set the crown straight", length=3.6, weight=2, require=["adult", "rank:lord|rank:marshal"])
def _(c):
    # the right hand rises high and out, touches the crown (or circlet) and nudges it true; head tilts to it
    up = dict(ra=(-30, 0, 105), rf=(-10, 0, 128))
    c.key(0.5, ra=(-12, 0, 30), rf=(-20, 0, 30), head=(2, 0, 0))
    c.key(1.0, **up, head=(-3, 6, -6))
    c.key(1.35, ra=(-30, 0, 103), rf=(-10, 0, 133), head=(-2, 4, -8))
    c.key(1.6, ra=(-31, 0, 106), rf=(-10, 0, 124), head=(-3, 7, -5))
    c.key(1.85, **up, head=(-3, 5, -6))
    c.key(2.3, ra=(-20, 0, 60), rf=(-10, 0, 70), head=(-6, 0, 0))
    c.key(2.9, ra=(-2, 0, 6), rf=(-6, 0, 4), head=(-7, 0, 0))
    c.key(3.6)


@clip("smooth_robe", "Smooth the robes", length=3.4, weight=2, require=["adult", "rank:lord|rank:marshal"])
def _(c):
    # the hand lays flat on the chest and strokes down the front of the robe; a glance down, then chin up
    c.key(0.7, ra=(-10, -40, 0), rf=(-135, 0, 0), head=(14, 6, 0))
    c.key(1.2, ra=(5, -40, 0), rf=(-120, 0, 0), head=(17, 5, 0))
    c.key(1.6, ra=(15, -35, 0), rf=(-110, 0, 0), head=(18, 4, 0))
    c.key(2.0, ra=(25, -30, 0), rf=(-100, 0, 0), head=(14, 3, 0))
    c.key(2.4, ra=(14, -12, 2), rf=(-40, 0, 0), head=(-6, 0, 0))
    c.key(3.4)


@clip("glaive_check", "Look along the glaive", length=4.4, weight=3, require=["adult", "rank:riftguard"],
      mirror="never")
def _(c):
    # the glaive comes upright before the face, its blade tipped back to be looked over, turned, lowered
    c.key(0.8, ra=(-33, -14, 5), rf=(-58, 0, 0), glaive=(-6, 0, 0), head=(-12, 0, 0))
    c.key(1.2, ra=(-35, -15, 5), rf=(-55, 0, 0), glaive=(-15, 0, 0), head=(-26, 2, 0))
    c.key(1.9, ra=(-35, -15, 5), rf=(-55, 0, 0), glaive=(-15, 12, 0), head=(-27, 6, -4))
    c.key(2.6, ra=(-35, -15, 5), rf=(-55, 0, 0), glaive=(-14, -10, 0), head=(-26, -3, 4))
    c.key(3.1, ra=(-34, -15, 5), rf=(-56, 0, 0), glaive=(-12, 0, 0), head=(-20, 0, 0))
    c.key(3.6, ra=(-8, -2, 2), rf=(-14, 0, 0), glaive=(0, 0, 0), head=(-4, 0, 0))
    c.key(4.4)


@clip("weight_shift", "Shift the weight", length=4.0, weight=2, require=["adult"], mirror="free")
def _(c):
    # weight settles onto one leg: the other knee eases, the hips tip and the shoulders answer
    c.key(1.2, rl=(-7, 0, 0), rs=(13, 0, 0), root=(0, 0, 2), waist=(0, 0, -3), head=(0, 0, 2), ra=(0, 0, 2))
    c.key(1.4, rl=(-8, 0, 0), rs=(15, 0, 0), root=(0, 0, 2.2), waist=(0, 0, -3.4), head=(0, 0, 2.4), ra=(0, 0, 2))
    c.key(2.9, rl=(-7, 0, 0), rs=(13, 0, 0), root=(0, 0, 2), waist=(0, 0, -3), head=(0, 3, 2), ra=(0, 0, 2))
    c.key(4.0)


@clip("impatient_drum", "Drum the fingers", length=3.8, weight=1, require=["adult"], mirror="never",
      boost={"manner:restless": 3, "manner:busy": 2})
def _(c):
    # the long fingers of the left hand drum on the thigh while one foot taps; a sideways look of impatience
    c.key(0.5, la=(-4, 0, 6), lf=(-6, 0, 0), head=(0, -10, 3))
    c.wobble(0.6, 2.6, 6, "lf", 7, base=(-8, 0, 0))
    c.cycle(0.7, 2.7, 0.5, dict(ll=(-4, 0, 0), ls=(6, 0, 0)), dict(ll=(0, 0, 0), ls=(0, 0, 0)), end_on="b")
    c.key(1.6, head=(2, -14, 4))
    c.key(2.6, la=(-4, 0, 6), head=(-6, 4, 0))
    c.key(3.8)


@clip("gaze_at_the_void", "Gaze up at the void", length=5.0, weight=2, require=["adult"], mirror="free")
def _(c):
    # the head tips slowly back to the black sky; the body leans with it, then sinks back level
    c.key(1.6, head=(-30, 6, 2), waist=(-4, 0, 0), mantle=(4, 0, 0), cape=(4, 0, 0), ra=(2, 0, 3), la=(2, 0, 3))
    c.key(3.0, head=(-33, -4, -2), waist=(-5, 0, 0), mantle=(5, 0, 0), cape=(5, 0, 0), ra=(2, 0, 4), la=(2, 0, 4))
    c.key(3.6, head=(-30, -5, -2), waist=(-4, 0, 0), mantle=(4, 0, 0), cape=(4, 0, 0))
    c.key(5.0)


@clip("enderman_tilt", "Enderman head tilt", length=3.2, weight=2, require=["adult"], mirror="free",
      blend=(0.25, 0.15))
def _(c):
    # the slow, uncanny tilt of the head all the way over, held a breath too long, then snapped upright
    c.key(1.4, head=(4, 6, 24))
    c.key(2.2, head=(5, 7, 27))
    c.key(2.4, head=(3, 4, 18))
    c.key(2.55, head=(-2, 0, -3))
    c.key(2.75, head=(0, 0, 1))
    c.key(3.2)
