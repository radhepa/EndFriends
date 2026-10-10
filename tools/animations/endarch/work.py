"""The Court at work: the Lord rules from the throne, the Voidmarshal commands, Riftguards drill with the glaive,
the Herald proclaims, the Seer looks into the void and the Steward counts the tribute.

Work clips weigh 3-5 and are boosted while working. Glaive clips are for the Riftguard's body only and never
mirror (the glaive is on the right forearm). At rest the glaive lies level, blade forward, from the hanging hand:
the arm and forearm pitch turn it like a lever (about -80 between them stands it upright).
"""
from kit import clip

WORK = {"working": 2}


@clip("lord_decree", "Lord's decree", length=4.6, weight=4, require=["adult", "job:lord"], boost=WORK)
def _(c):
    # the right hand rises palm-out above the Court, holds, then sweeps down and out: it is decreed
    c.key(0.6, ra=(-10, 0, 5), rf=(-32, 0, 0), head=(4, 0, 0))
    c.key(1.3, ra=(-75, 0, 20), rf=(-55, 0, 0), head=(-10, 0, 0), waist=(-3, 0, 0), mantle=(3, 0, 0))
    c.key(1.5, ra=(-79, 0, 21), rf=(-53, 0, 0), head=(-12, 2, 0), waist=(-4, 0, 0), mantle=(4, 0, 0))
    c.key(2.3, ra=(-77, 0, 20), rf=(-54, 0, 0), head=(-12, 3, 0), waist=(-4, 0, 0), mantle=(4, 0, 0))
    c.key(2.65, ra=(-42, 0, 38), rf=(-8, 0, 0), head=(8, 6, 0), waist=(3, 0, 0), mantle=(-2, 0, 0))
    c.key(2.8, ra=(-38, 0, 41), rf=(-4, 0, 0), head=(9, 6, 0), waist=(3, 0, 0), mantle=(-2, 0, 0))
    c.key(3.4, ra=(-36, 0, 39), rf=(-6, 0, 0), head=(-5, 4, 0), waist=(0, 0, 0), mantle=(0, 0, 0))
    c.key(4.6)


@clip("lord_beckon", "Beckon a thrall", length=4.4, weight=3, require=["adult", "job:lord"], boost=WORK)
def _(c):
    # the hand reaches out palm up and curls twice (come), then points to the floor before the throne
    c.key(0.7, ra=(-55, 0, 8), rf=(-30, 0, 0), head=(-6, 0, 0))
    c.key(1.0, ra=(-55, 0, 8), rf=(-95, 0, 0))
    c.key(1.3, ra=(-56, 0, 8), rf=(-35, 0, 0))
    c.key(1.6, ra=(-55, 0, 8), rf=(-98, 0, 0))
    c.key(1.95, ra=(-55, 0, 8), rf=(-38, 0, 0), head=(-7, 0, 0))
    c.key(2.5, ra=(-38, 0, 6), rf=(-4, 0, 0), head=(12, 0, 0))
    c.key(2.65, ra=(-40, 0, 6), rf=(-2, 0, 0), head=(13, 0, 0))
    c.key(3.4, ra=(-39, 0, 6), rf=(-3, 0, 0), head=(11, 2, 0))
    c.key(4.4)


@clip("lord_regal_repose", "Regal repose", length=6.0, weight=3, require=["adult", "job:lord"], boost=WORK,
      mirror="never")
def _(c):
    # as on the throne: the long forearms fold low before the waist, one over the other; the Lord draws up and looks
    # slowly down the length of the hall, left to right, then lets out a long, bored breath
    fold = dict(ra=(-20, -9, 15), rf=(-99, -72, 0), la=(-19, -1, 11), lf=(-90, -81, 0))
    c.key(0.6, ra=(-12, -4, 8), rf=(-50, -30, 0), la=(-10, 0, 6), lf=(-45, -35, 0), head=(2, 0, 0))
    c.key(1.2, **fold, head=(-6, -18, 0), waist=(-2, 0, 0), mantle=(2, 0, 0))
    c.key(2.8, **fold, head=(-7, 4, 0), waist=(-2, -2, 0), mantle=(2, 0, 0))
    c.key(4.0, **fold, head=(-6, 20, 0), waist=(-2, 3, 0), mantle=(2, 0, 0))
    c.key(4.6, **fold, head=(5, 10, 0), waist=(1, 2, 0), mantle=(-1, 0, 0))
    c.key(5.3, ra=(-6, -2, 4), rf=(-20, -10, 0), la=(-6, 0, 4), lf=(-18, -10, 0), head=(-2, 0, 0), waist=(0, 0, 0),
          mantle=(0, 0, 0))
    c.key(6.0)


@clip("marshal_survey", "Survey the field", length=5.8, weight=4, require=["adult", "job:marshal"], boost=WORK)
def _(c):
    # feet set wide, the left hand at the small of the back; the gaze sweeps the field, then the right arm points the way
    # (the left arm swings back before the forearm folds in, and opens before it comes forward: never through the cape)
    stance = dict(rl=(0, 0, 6), ll=(0, 0, 6), la=(30, 0, 4), lf=(-8, 0, -42))
    c.key(0.4, la=(24, 0, 7), lf=(-4, 0, -6))
    c.key(5.2, la=(24, 0, 7), lf=(-4, 0, -6))
    c.key(0.8, **stance, head=(-4, -24, 0), waist=(2, -6, 0), cape=(-2, 0, 0))
    c.key(2.0, **stance, head=(-4, 26, 0), waist=(2, 6, 0), cape=(-2, 0, 0))
    c.key(2.6, **stance, head=(-6, 4, 0), waist=(2, 0, 0), cape=(-2, 0, 0), ra=(-20, 0, 4), rf=(-30, 0, 0))
    c.key(3.1, **stance, head=(-4, 6, 0), waist=(4, 3, 0), cape=(-3, 0, 0), ra=(-88, 6, 0), rf=(-6, 0, 0))
    c.key(3.25, ra=(-91, 6, 0), rf=(-3, 0, 0))
    c.key(4.4, **stance, head=(-3, 6, 0), waist=(4, 3, 0), cape=(-3, 0, 0), ra=(-89, 6, 0), rf=(-5, 0, 0))
    c.key(5.8)


@clip("marshal_command", "Command the advance", length=3.6, weight=3, require=["adult", "job:marshal"],
      boost=WORK)
def _(c):
    # the right arm rises high and chops forward: advance! the head drives the order home
    c.key(0.8, ra=(-165, 0, 12), rf=(-25, 0, 0), la=(4, 0, 4), lf=(-20, 0, 0), head=(-10, 0, 0),
          waist=(-4, 0, 0), cape=(4, 0, 0))
    c.key(1.0, ra=(-170, 0, 12), rf=(-30, 0, 0), head=(-11, 0, 0))
    c.key(1.2, ra=(-80, 0, 0), rf=(-4, 0, 0), head=(8, 0, 0), waist=(6, 0, 0), cape=(-5, 0, 0))
    c.key(1.32, ra=(-72, 0, 0), rf=(-2, 0, 0), head=(9, 0, 0), waist=(7, 0, 0), cape=(-6, 0, 0))
    c.key(2.2, ra=(-76, 0, 0), rf=(-4, 0, 0), la=(4, 0, 4), lf=(-20, 0, 0), head=(2, 0, 0), waist=(4, 0, 0),
          cape=(-4, 0, 0))
    c.key(3.6)


@clip("marshal_inspect", "Inspect the ranks", length=6.4, weight=3, require=["adult", "job:marshal"], boost=WORK,
      mirror="free")
def _(c):
    # hands behind, leaning a little, the Voidmarshal turns slowly along a line of thralls; stops on one
    hb = dict(ra=(30, 0, 4), rf=(-8, 0, -42), la=(30, 0, 4), lf=(-8, 0, -42))
    swing = dict(ra=(24, 0, 7), rf=(-4, 0, -6), la=(24, 0, 7), lf=(-4, 0, -6))   # arms back before they fold
    c.key(0.45, **swing)
    c.key(5.8, **swing)
    c.key(0.9, **hb, waist=(6, 0, 0), cape=(-5, 0, 0), head=(8, 0, 0), root=(0, -22, 0))
    c.key(2.2, **hb, waist=(6, 0, 0), cape=(-5, 0, 0), head=(8, 0, 0), root=(0, -4, 0))
    c.key(2.6, **hb, waist=(9, 0, 0), cape=(-7, 0, 0), head=(14, 0, 6), root=(0, -2, 0))
    c.key(3.6, **hb, waist=(9, 0, 0), cape=(-7, 0, 0), head=(14, 0, 8), root=(0, -2, 0))
    c.key(4.0, **hb, waist=(6, 0, 0), cape=(-5, 0, 0), head=(6, 0, 0), root=(0, 2, 0))
    c.key(5.2, **hb, waist=(5, 0, 0), cape=(-4, 0, 0), head=(6, 0, 0), root=(0, 18, 0))
    c.key(6.4)


GUARD = dict(ra=(-35, 0, 5), rf=(-35, 0, 0), glaive=(55, 0, 0))
RIFT = ["adult", "job:riftguard", "rank:riftguard"]


@clip("glaive_thrust", "Glaive thrust drill", length=5.2, weight=4, require=RIFT, boost=WORK, mirror="never")
def _(c):
    # from a low guard, two lunging thrusts: the right foot drives forward, the glaive spears out level
    lunge = dict(rl=(-24, 0, 0), rs=(22, 0, 0), ll=(10, 0, 0), ls=(6, 0, 0), waist=(8, 0, 0),
                 la=(18, 0, 12), lf=(-20, 0, 0), head=(-6, 0, 0))
    back = dict(rl=(-4, 0, 0), rs=(4, 0, 0), ll=(2, 0, 0), ls=(0, 0, 0), waist=(2, 0, 0),
                la=(6, 0, 6), lf=(-14, 0, 0), head=(-2, 0, 0))
    c.key(0.8, **GUARD, **back)
    c.key(1.1, ra=(-28, 0, 5), rf=(-40, 0, 0), glaive=(52, 0, 0))
    c.key(1.35, ra=(-80, 0, 0), rf=(-5, 0, 0), glaive=(82, 0, 0), **lunge)
    c.key(1.5, ra=(-83, 0, 0), rf=(-3, 0, 0), glaive=(84, 0, 0))
    c.key(1.9, ra=(-78, 0, 0), rf=(-6, 0, 0), glaive=(80, 0, 0))
    c.key(2.4, **GUARD, **back)
    c.key(2.7, ra=(-28, 0, 5), rf=(-40, 0, 0), glaive=(52, 0, 0))
    c.key(2.95, ra=(-80, 0, 0), rf=(-5, 0, 0), glaive=(82, 0, 0), **lunge)
    c.key(3.1, ra=(-83, 0, 0), rf=(-3, 0, 0), glaive=(84, 0, 0))
    c.key(3.5, ra=(-78, 0, 0), rf=(-6, 0, 0), glaive=(80, 0, 0))
    c.key(4.1, **GUARD, **back)
    c.key(5.2)


@clip("glaive_sweep", "Glaive sweep drill", length=4.8, weight=3, require=RIFT, boost=WORK, mirror="never")
def _(c):
    # wound up high to the right, the glaive sweeps level across the front; the body turns through it
    c.key(0.9, ra=(-70, 45, 20), rf=(-20, 0, 0), glaive=(70, 0, 0), waist=(0, 22, 0), head=(0, 10, 0),
          la=(-20, 0, 18), lf=(-30, 0, 0), rl=(-6, 0, 0), rs=(8, 0, 0))
    c.key(1.15, ra=(-72, 50, 22), rf=(-22, 0, 0), waist=(0, 25, 0))
    # (the waist does most of the turning: an arm swung further across runs into the chest)
    c.key(1.5, ra=(-70, -38, 6), rf=(-10, 0, 0), glaive=(70, 0, 0), waist=(0, -26, 0), head=(0, -14, 0),
          la=(10, 0, 20), lf=(-20, 0, 0), ll=(-6, 0, 0), ls=(8, 0, 0), rl=(0, 0, 0), rs=(0, 0, 0))
    c.key(1.65, ra=(-70, -42, 6), rf=(-8, 0, 0), glaive=(84, 0, 0), waist=(0, -30, 0))
    c.key(2.3, ra=(-68, -38, 6), rf=(-12, 0, 0), glaive=(82, 0, 0), waist=(0, -25, 0))
    c.key(3.2, **GUARD, waist=(0, 0, 0), head=(-4, 0, 0), la=(6, 0, 6), lf=(-14, 0, 0), ll=(0, 0, 0),
          ls=(0, 0, 0))
    c.key(4.8)


@clip("guard_attention", "Stand to attention", length=6.0, weight=4, require=RIFT, boost=WORK, mirror="never")
def _(c):
    # the glaive snaps upright, the left foot stamps, chin up: a sentry at its post, unmoving
    up = dict(ra=(-8, 0, 0), rf=(-72, 0, 0))
    c.key(0.5, ra=(-4, 0, 0), rf=(-50, 0, 0), ll=(-30, 0, 0), ls=(40, 0, 0), head=(-4, 0, 0))
    c.key(0.75, **up, ll=(-34, 0, 0), ls=(44, 0, 0))
    c.key(0.95, ll=(0, 0, 0), ls=(0, 0, 0), root_pos=(0, 0.6, 0), head=(-10, 0, 0), la=(0, 0, -3))
    c.key(1.1, root_pos=(0, 0, 0), head=(-9, 0, 0))
    c.key(5.0, **up, head=(-9, 0, 0), la=(0, 0, -3))
    c.key(6.0)


@clip("riftguard_watch", "Watchful guard", length=5.6, weight=3, require=RIFT, boost=WORK, mirror="never")
def _(c):
    # knees eased, glaive levelled, the head turns slow and stops hard on something, then eases
    crouch = dict(rl=(-10, 0, 0), rs=(18, 0, 0), ll=(-10, 0, 0), ls=(18, 0, 0), root_pos=(0, 0.4, 0),
                  waist=(6, 0, 0), la=(-10, 0, 10), lf=(-25, 0, 0))
    c.key(0.8, **GUARD, **crouch, head=(-2, -24, 0))
    c.key(2.0, **GUARD, **crouch, head=(-2, 18, 0))
    c.key(2.3, **GUARD, **crouch, head=(-3, 32, 0))
    c.key(2.4, head=(-4, 34, -2), waist=(7, 4, 0))
    c.key(3.6, head=(-4, 33, -2), waist=(7, 4, 0))
    c.key(4.5, **GUARD, head=(-2, 0, 0), waist=(2, 0, 0))
    c.key(5.6)


@clip("herald_proclaim", "Herald's proclamation", length=5.2, weight=4, require=["adult", "job:herald"], boost=WORK)
def _(c):
    # arms flung wide and high, chest out, head back: hear the Court! a second push, then a slow lowering
    wide = dict(ra=(-25, 0, 115), rf=(-20, 0, 0), la=(-25, 0, 115), lf=(-20, 0, 0))
    c.key(0.6, ra=(-10, 0, 20), rf=(-30, 0, 0), la=(-10, 0, 20), lf=(-30, 0, 0), head=(5, 0, 0),
          waist=(2, 0, 0), mantle=(-2, 0, 0), cape=(-2, 0, 0))
    c.key(1.3, **wide, head=(-15, 0, 0), waist=(-5, 0, 0), mantle=(5, 0, 0), cape=(5, 0, 0))
    c.key(1.5, ra=(-27, 0, 119), la=(-27, 0, 119), head=(-16, 0, 0))
    c.key(2.4, **wide, head=(-13, 4, 0))
    c.key(2.7, ra=(-30, 0, 126), rf=(-12, 0, 0), la=(-30, 0, 126), lf=(-12, 0, 0), head=(-18, 0, 0),
          waist=(-6, 0, 0), mantle=(6, 0, 0), cape=(6, 0, 0))
    c.key(3.5, **wide, head=(-14, -3, 0), waist=(-5, 0, 0), mantle=(5, 0, 0), cape=(5, 0, 0))
    c.key(4.4, ra=(-12, 0, 22), rf=(-14, 0, 0), la=(-12, 0, 22), lf=(-14, 0, 0), head=(-4, 0, 0),
          waist=(-1, 0, 0), mantle=(1, 0, 0), cape=(1, 0, 0))
    c.key(5.2)


@clip("herald_present", "Herald presents", length=4.6, weight=3, require=["adult", "job:herald"], boost=WORK)
def _(c):
    # the hand starts at the breast and unrolls out to the side, palm up: behold; head and body follow it
    c.key(0.7, ra=(-10, -40, 0), rf=(-135, 0, 0), head=(4, -6, 0))
    c.key(1.4, ra=(-45, 40, 45), rf=(-15, 0, 0), head=(6, 24, 0), waist=(4, 8, 0), mantle=(-3, 0, 0),
          cape=(-3, 0, 0), la=(-6, 0, 4), lf=(-20, 0, 0))
    c.key(1.6, ra=(-47, 44, 47), rf=(-12, 0, 0), head=(8, 26, 0), waist=(5, 9, 0))
    c.key(2.8, ra=(-45, 42, 45), rf=(-14, 0, 0), head=(6, 22, 0), waist=(4, 8, 0), mantle=(-3, 0, 0),
          cape=(-3, 0, 0), la=(-6, 0, 4), lf=(-20, 0, 0))
    c.key(3.7, ra=(-8, 6, 8), rf=(-12, 0, 0), head=(-4, 4, 0), waist=(0, 0, 0), mantle=(0, 0, 0), cape=(0, 0, 0))
    c.key(4.6)


@clip("seer_gaze_void", "Seer gazes into the void", length=6.4, weight=4, require=["adult", "job:seer"],
      boost=WORK, mirror="never")
def _(c):
    # the head tips back, both palms rise slowly, a trance tremor runs through the hands, then they sink
    rise = dict(ra=(-40, 0, 25), rf=(-45, 0, 0), la=(-40, 0, 25), lf=(-45, 0, 0))
    c.key(1.8, **rise, head=(-28, 0, 0), waist=(-4, 0, 0), mantle=(4, 0, 0), cape=(4, 0, 0))
    c.wobble(2.0, 3.8, 7, "rf", 4, base=(-46, 0, 0))
    c.wobble(2.0, 3.8, 6, "lf", 4, base=(-44, 0, 0), axis=0)
    c.wobble(2.0, 3.8, 5, "head", 2.5, base=(-30, 0, 0), axis=2)
    c.key(4.2, **rise, head=(-26, 0, 0), waist=(-4, 0, 0), mantle=(4, 0, 0), cape=(4, 0, 0))
    c.key(5.4, ra=(-6, 0, 6), rf=(-12, 0, 0), la=(-6, 0, 6), lf=(-12, 0, 0), head=(6, 0, 0), waist=(1, 0, 0),
          mantle=(-1, 0, 0), cape=(-1, 0, 0))
    c.key(6.4)


@clip("seer_scry", "Seer scries", length=6.0, weight=3, require=["adult", "job:seer"], boost=WORK, mirror="never")
def _(c):
    # the hands cup an unseen orb before the chest and turn about it; the head bows close over it
    r_hi, r_lo = dict(ra=(-18, 0, 10), rf=(-118, -14, 0)), dict(ra=(-12, 0, 10), rf=(-98, -14, 0))
    l_hi, l_lo = dict(la=(-18, 0, 10), lf=(-118, -14, 0)), dict(la=(-12, 0, 10), lf=(-98, -14, 0))
    c.key(1.0, **r_lo, **l_lo, head=(16, 0, 0), waist=(3, 0, 0), mantle=(-2, 0, 0), cape=(-2, 0, 0))
    c.cycle(1.4, 4.6, 1.6, {**r_hi, **l_lo}, {**r_lo, **l_hi})
    c.key(2.2, head=(20, 6, 4))
    c.key(3.8, head=(20, -6, -4))
    c.key(4.6, head=(18, 0, 0), waist=(3, 0, 0), mantle=(-2, 0, 0), cape=(-2, 0, 0))
    c.key(5.3, ra=(-4, 0, 4), rf=(-25, -4, 0), la=(-4, 0, 4), lf=(-25, -4, 0), head=(2, 0, 0), waist=(0, 0, 0),
          mantle=(0, 0, 0), cape=(0, 0, 0))
    c.key(6.0)


@clip("steward_count", "Steward counts the tribute", length=5.6, weight=4, require=["adult", "job:steward"],
      boost=WORK, mirror="never")
def _(c):
    # the left forearm held level as a ledger, the right hand ticks down it; a nod with every count
    ledger = dict(la=(-20, 0, 0), lf=(-75, -30, 0))
    c.key(0.8, **ledger, ra=(-22, 0, 0), rf=(-66, -25, 0), head=(18, 0, 0))
    ticks = (1.2, 1.7, 2.2, 2.7, 3.2, 3.7)
    for i, t in enumerate(ticks):
        c.key(t, ra=(-25, 0, 0), rf=(-76, -25, 0), head=(20, 0, 0))
        c.key(t + 0.18, ra=(-25 + i, 0, 0), rf=(-68, -25, 0), head=(16, 0, 0))
    c.key(4.3, **ledger, ra=(-20, 0, 0), rf=(-60, -20, 0), head=(10, 8, -6))
    c.key(4.6, **ledger, head=(9, 8, -7))
    c.key(5.6)


@clip("steward_inspect", "Inspect the tribute", length=5.2, weight=3, require=["adult", "job:steward"], boost=WORK)
def _(c):
    # a stiff, shallow bend over the tribute (the robes allow no more); the hand turns a piece over and weighs
    # it; upright again, a curt nod
    bend = dict(waist=(6, 0, 0), mantle=(-5, 0, 0), cape=(-5, 0, 0), rl=(-4, 0, 0), rs=(7, 0, 0), ll=(-4, 0, 0),
                ls=(7, 0, 0), root_pos=(0, 0.3, 0))
    c.key(1.0, **bend, head=(30, 0, 0), ra=(-40, 0, 0), rf=(-14, 0, 0), la=(14, 0, 4), lf=(-10, 0, 0))
    c.key(1.4, ra=(-45, 0, 0), rf=(-10, 0, 0), head=(33, 0, 0))
    c.key(2.0, ra=(-46, 0, 0), rf=(-12, 40, 0), head=(33, 6, -4))
    c.key(2.6, ra=(-44, 0, 0), rf=(-24, -10, 0), head=(30, 2, 2))
    c.key(3.0, ra=(-44, 0, 0), rf=(-18, 0, 0))
    c.key(3.4, **bend, head=(24, 0, 0))
    c.key(4.1, waist=(-2, 0, 0), mantle=(2, 0, 0), cape=(2, 0, 0), rl=(0, 0, 0), rs=(0, 0, 0), ll=(0, 0, 0),
          ls=(0, 0, 0), root_pos=(0, 0, 0), head=(-6, 0, 0), ra=(-4, 0, 2), rf=(-6, 0, 0), la=(0, 0, 0),
          lf=(0, 0, 0))
    c.key(4.4, head=(6, 0, 0))
    c.key(4.6, head=(-3, 0, 0))
    c.key(5.2)
