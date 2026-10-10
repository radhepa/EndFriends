"""Shulkin children: soft pale shells that pop open at everything, short arms, no cape. Play, fidgets, mischief.

The pack's waist sits at the top of a child's smock, so these bend with the root (about the feet), never the waist.
"""
from kit import clip

CHILD = ["child"]


@clip("child_hop_count", "Hops and counts the tiles", length=4.2, weight=3, require=CHILD, mirror="free")
def _(c):
    # three hops, an arm thrown up for each count, the lid popping with every landing
    for i, t in enumerate((0.3, 1.2, 2.1)):
        arm, other = ("ra", "la") if i % 2 == 0 else ("la", "ra")
        c.key(t, root_pos=(0, 0.6, 0), lid_pos=(0, 0.6, 0), **{arm: (-20, 0, 10), other: (-6, 0, 6)})
        c.key(t + 0.3, root_pos=(0, -2.4, 0), lid_pos=(0, -2.2, 0), lid=(-8, 0, 0),
              **{arm: (-20, 0, 140), other: (8, 0, 20)}, head=(-10, 0, 0))
        c.key(t + 0.6, root_pos=(0, 0.4, 0), lid_pos=(0, 0.2, 0), lid=(0, 0, 0),
              **{arm: (-20, 0, 30), other: (0, 0, 8)}, head=(4, 0, 0))
    c.key(3.2, root_pos=(0, 0, 0), head=(0, 0, 0), ra=(0, 0, 4), la=(0, 0, 4))
    c.key(4.2)


@clip("child_peekaboo", "Plays peekaboo with the lid", length=4.4, weight=3, require=CHILD)
def _(c):
    c.key(0.3, lid_pos=(0, 0.4, 0), head=(6, 0, 0), ra=(-10, 0, -4), la=(-10, 0, -4))
    c.key(0.5, lid_pos=(0, 4.0, 0), head=(12, 0, 0), ra=(-30, -20, 0), la=(-30, -20, 0))
    c.key(1.3, lid_pos=(0, 4.0, 0), head=(12, 0, 0), root=(0, 0, 3))
    # boo!
    c.key(1.5, lid_pos=(0, -3.4, 0), lid=(-14, 0, 0), head=(-10, 0, 0), ra=(-20, 0, 100), la=(-20, 0, 100),
          root_pos=(0, -1.0, 0), root=(0, 0, 0))
    c.key(1.75, lid_pos=(0, -2.8, 0), root_pos=(0, 0, 0))
    # a giggle that rattles the lid
    c.wobble(1.8, 2.7, 6, "lid_pos", 0.9, base=(0, -2.4, 0), axis=1)
    c.wobble(1.8, 2.7, 6, "head", 4, base=(-6, 0, 0), axis=2)
    c.key(2.9, lid_pos=(0, 0.5, 0), lid=(0, 0, 0), ra=(-8, 0, 20), la=(-8, 0, 20), head=(4, 0, 0))
    c.key(3.1, lid_pos=(0, 4.0, 0), head=(12, 8, 0), ra=(-30, -20, 0), la=(-30, -20, 0))
    c.key(3.7, lid_pos=(0, 3.6, 0), head=(10, 10, 0))
    c.key(4.4)


@clip("child_sleeve_twirl", "Twists side to side with flying arms", length=3.8, weight=2, require=CHILD,
      mirror="free")
def _(c):
    c.key(0.3, ra=(0, 0, 70), la=(0, 0, 70), root=(0, 30, 0), head=(0, -10, 0))
    c.key(0.8, ra=(0, 0, 80), la=(0, 0, 60), root=(0, -40, 0), head=(-4, 14, 0), lid_pos=(0, -1.2, 0))
    c.key(1.4, ra=(0, 0, 60), la=(0, 0, 80), root=(0, 40, 0), head=(-4, -14, 0), lid_pos=(0, -0.2, 0))
    c.key(2.0, ra=(0, 0, 80), la=(0, 0, 60), root=(0, -36, 0), head=(-4, 12, 0), lid_pos=(0, -1.2, 0))
    c.key(2.6, ra=(0, 0, 50), la=(0, 0, 60), root=(0, 18, 0), head=(2, -6, 0), lid_pos=(0, -0.4, 0))
    # dizzy: a wobble and a lopsided lid
    c.key(3.0, ra=(0, 0, 10), la=(0, 0, 14), root=(0, 0, 4), head=(4, 0, -8), lid=(0, 0, 6))
    c.key(3.3, root=(0, 0, -2), head=(2, 0, 4))
    c.key(3.8)


@clip("child_poke_mischief", "Sneaks up for a poke", length=4.6, weight=2, require=CHILD)
def _(c):
    # eyes low under the lid, a look each way, a creep forward, a poke; then shut up tight, all innocence
    c.key(0.4, lid_pos=(0, 2.0, 0), head=(8, -24, 0), ra=(-10, 0, -4), la=(-10, 0, -4))
    c.key(0.9, head=(8, 24, 0))
    c.key(1.4, head=(8, 0, 0), root=(6, 0, 0), ra=(-40, -10, 0), la=(-14, 0, -2))
    c.key(1.8, root=(8, 0, 0), root_pos=(0, 0, -0.6), ra=(-44, -10, 0))
    c.key(2.0, ra=(-92, -4, 0), root=(10, 0, 0), root_pos=(0, 0, -1.2), lid_pos=(0, -1.6, 0), lid=(-6, 0, 0))
    c.key(2.15, ra=(-70, -4, 0))
    c.key(2.3, ra=(-92, -4, 0))
    c.key(2.55, ra=(-10, 0, -4), root=(0, 0, 0), root_pos=(0, 0, 0), lid_pos=(0, 3.8, 0), lid=(0, 0, 0),
          head=(14, 0, 0))
    c.key(3.6, lid_pos=(0, 3.6, 0), head=(12, 0, 0))
    c.key(4.0, lid_pos=(0, 1.6, 0), head=(6, 10, 0))
    c.key(4.6)


@clip("child_play_archivist", "Plays at being a grave archivist", length=4.8, weight=2, require=CHILD)
def _(c):
    # very straight, a pretend tome held out, the slowest, most solemn nods
    c.key(0.5, ra=(-60, -30, 0), la=(-60, -30, 0), head=(-6, 0, 0), root_pos=(0, -0.6, 0), lid=(-4, 0, 0))
    c.key(1.2, head=(16, 0, 0))
    c.key(1.9, head=(-6, 0, 0))
    c.key(2.6, head=(16, 0, 0))
    # "Hmm. Quite." Then the act breaks into a wiggle and the lid pops
    c.key(3.1, head=(-4, 0, 0), ra=(-60, -30, 0), la=(-60, -30, 0), root_pos=(0, -0.6, 0))
    c.key(3.3, root=(0, 0, 6), ra=(-10, 0, 40), la=(-10, 0, 40), lid_pos=(0, -2.6, 0), lid=(-10, 0, 0),
          root_pos=(0, -1.2, 0), head=(-8, 0, 0))
    c.key(3.55, root=(0, 0, -6), root_pos=(0, 0, 0))
    c.key(3.8, root=(0, 0, 4), lid_pos=(0, -1.8, 0))
    c.key(4.05, root=(0, 0, -2), lid_pos=(0, -0.8, 0), lid=(-3, 0, 0), ra=(0, 0, 10), la=(0, 0, 10), head=(0, 0, 0))
    c.key(4.8)


@clip("child_march_sentry", "Marches on the spot like a sentry", length=4.4, weight=2, require=CHILD, mirror="free")
def _(c):
    # chin up, knees high, stiff arms swinging; a stamp to a halt, one arm shot up, the lid popping with pride
    for i in range(5):
        t = 0.4 + 0.5 * i
        leg, other = ("rl", "ll") if i % 2 == 0 else ("ll", "rl")
        fwd, back = ("la", "ra") if i % 2 == 0 else ("ra", "la")
        c.key(t, **{leg: (-38, 0, 0), other: (0, 0, 0), fwd: (-30, 0, 4), back: (24, 0, 4)}, root_pos=(0, -0.5, 0),
              head=(-6, 0, 0), lid_pos=(0, -0.6, 0))
        c.key(t + 0.25, rl=(0, 0, 0), ll=(0, 0, 0), ra=(0, 0, 4), la=(0, 0, 4), root_pos=(0, 0, 0),
              lid_pos=(0, 0, 0))
    c.key(2.9, root_pos=(0, 0.3, 0), head=(-4, 0, 0))
    c.key(3.2, ra=(-12, 0, 150), la=(0, 0, 4), root_pos=(0, 0, 0), head=(-8, 0, 0), lid_pos=(0, -2.2, 0),
          lid=(-8, 0, 0))
    c.wobble(3.25, 3.75, 6, "lid_pos", 0.5, base=(0, -2.0, 0), axis=1)
    c.key(3.75, ra=(-12, 0, 146), head=(-6, 0, 4), lid=(-6, 0, 0))
    c.key(4.4)


@clip("child_farewell_bob", "Bobs a little bow and flutters a hand", trigger="farewell", length=3.0, weight=3,
      require=CHILD, mirror="free")
def _(c):
    # a quick bow from the toes with the lid ducking shut, then a bye-bye flutter at chest height and a look back
    # over the shoulder while turning to go
    c.key(0.3, root=(10, 0, 0), head=(8, 0, 0), lid_pos=(0, 2.0, 0), ra=(8, 0, 4), la=(8, 0, 4))
    c.key(0.55, root=(10, 0, 0), lid_pos=(0, 2.2, 0))
    c.key(0.85, root=(0, 0, 0), head=(-4, 0, 6), lid_pos=(0, -1.6, 0), lid=(-6, 0, 0), ra=(-62, -10, 20),
          la=(0, 0, 4))
    c.wobble(0.95, 1.9, 4, "ra", 14, base=(-62, -10, 20), axis=2)
    c.key(2.2, root=(0, 28, 0), head=(0, -18, 0), ra=(0, 0, 8), lid_pos=(0, -0.6, 0), lid=(-2, 0, 0))
    c.key(2.5, root=(0, 30, 0), head=(0, -20, 0))
    c.key(3.0)


@clip("child_greet_bounce", "Bounces and waves both arms", trigger="greet", length=2.8, weight=3, require=CHILD)
def _(c):
    c.key(0.2, root_pos=(0, 0.6, 0), lid_pos=(0, 0.6, 0))
    c.key(0.45, root_pos=(0, -2.0, 0), lid_pos=(0, -3.0, 0), lid=(-12, 0, 0), ra=(-10, 0, 140), la=(-10, 0, 140),
          head=(-8, 0, 0))
    c.key(0.7, root_pos=(0, 0.3, 0), lid_pos=(0, -2.0, 0))
    c.key(0.85, root_pos=(0, 0, 0))
    # both arms wave overhead, the lid still bobbing
    c.wobble(0.9, 2.0, 3, "ra", 14, base=(-10, 0, 135), axis=2)
    c.wobble(0.9, 2.0, 3, "la", -14, base=(-10, 0, 135), axis=2)
    c.wave(0.9, 2.1, 0.6, "lid_pos", 0.8, base=(0, -1.8, 0), axis=1)
    c.key(2.3, ra=(0, 0, 20), la=(0, 0, 20), lid=(-3, 0, 0), head=(0, 0, 4))
    c.key(2.8)
