"""Reactions: gifts, favour, apologies and blows. Shulkin show delight with the lid and hold displeasure in it."""
from kit import clip


@clip("happy_lid_pop", "The lid pops up with delight", trigger="happy", length=2.6, weight=3, blend=(.15, .35))
def _(c):
    # a little crouch with the lid down, then the lid flies up, a hop, the arms up and out
    c.key(0.25, root_pos=(0, 0.6, 0), lid_pos=(0, 1.0, 0), head=(8, 0, 0), ra=(-6, 0, -2), la=(-6, 0, -2))
    c.key(0.5, root_pos=(0, -2.2, 0), lid_pos=(0, -3.6, 0), lid=(-14, 0, 0), head=(-12, 0, 0),
          ra=(-30, 30, 44), rf=(-30, 0, 0), la=(-30, 30, 44), lf=(-30, 0, 0), cape=(10, 0, 0))
    c.key(0.75, root_pos=(0, 0.5, 0), lid_pos=(0, -2.8, 0), lid=(-10, 0, 0), head=(-6, 0, 0),
          ra=(-24, 26, 36), la=(-24, 26, 36), cape=(-3, 0, 0))
    c.key(0.95, root_pos=(0, 0, 0), cape=(1, 0, 0))
    # the lid chatters down as the delight settles
    c.wobble(1.0, 1.9, 5, "lid_pos", 0.7, base=(0, -1.8, 0), axis=1, decay=0.6)
    c.key(2.0, ra=(-10, 8, 8), rf=(-14, 0, 0), la=(-10, 8, 8), lf=(-14, 0, 0), head=(0, 0, 4), lid=(-4, 0, 0),
          cape=(0, 0, 0))
    c.key(2.6)


@clip("happy_hug_ledger", "Hugs it close like a treasured book", trigger="happy", length=3.4, weight=2)
def _(c):
    hug = dict(ra=(-34, -46, 0), rf=(-96, 0, 0), la=(-34, -46, 0), lf=(-96, 0, 0))
    c.key(0.4, head=(10, 0, 0), lid_pos=(0, -1.2, 0), lid=(-4, 0, 0), **hug)
    c.key(0.6, ra=(-30, -48, 0), la=(-30, -48, 0), ra_pos=(0, -0.4, 0), la_pos=(0, -0.4, 0))
    # sways happily side to side with it, the head leaning into the sway
    c.wave(0.7, 2.7, 1.0, "root", 4, axis=2)
    c.wave(0.7, 2.7, 1.0, "head", 6, base=(10, 0, 0), axis=2, phase=0.1)
    c.key(2.7, lid_pos=(0, -1.4, 0), ra=(-30, -48, 0), la=(-30, -48, 0))
    c.key(3.0, ra=(-16, -20, 0), rf=(-40, 0, 0), la=(-16, -20, 0), lf=(-40, 0, 0), lid_pos=(0, -0.4, 0),
          ra_pos=(0, 0, 0), la_pos=(0, 0, 0))
    c.key(3.4)


@clip("thanks_receive", "Receives it with both hands", trigger="thanks", length=3.0, weight=3)
def _(c):
    c.key(0.45, ra=(-48, -16, 0), rf=(-48, 0, 0), la=(-48, -16, 0), lf=(-48, 0, 0), head=(14, 0, 0), waist=(4, 0, 0))
    c.key(0.65, ra=(-46, -18, 0), la=(-46, -18, 0))
    # draws it in to the breast and dips the head, the lid lifting a touch in thanks
    c.key(1.2, ra=(-30, -40, 0), rf=(-92, 0, 0), la=(-30, -40, 0), lf=(-92, 0, 0), head=(16, 0, 0), waist=(6, 0, 0),
          lid_pos=(0, -1.2, 0), lid=(4, 0, 0), cape=(-3, 0, 0))
    c.key(1.7, head=(4, 0, 0), waist=(0, 0, 0), cape=(0, 0, 0), lid_pos=(0, -0.8, 0), lid=(-3, 0, 0))
    c.key(2.3, ra=(-16, -16, 0), rf=(-40, 0, 0), la=(-16, -16, 0), lf=(-40, 0, 0), lid_pos=(0, -0.2, 0),
          lid=(0, 0, 0))
    c.key(3.0)


@clip("thanks_heart_nods", "Hand to the breast and two nods", trigger="thanks", length=2.6, weight=2)
def _(c):
    c.key(0.35, ra=(-24, -40, 0), rf=(-88, 0, 0), head=(2, 0, 4))
    for t in (0.6, 1.15):
        c.key(t, head=(13, 0, 4), lid_pos=(0, 0.6, 0))
        c.key(t + 0.3, head=(0, 0, 4), lid_pos=(0, -1.2, 0), lid=(-4, 0, 0))
    c.key(1.9, ra=(-20, -30, 0), rf=(-60, 0, 0), head=(0, 0, 2), lid_pos=(0, -0.4, 0), lid=(-1, 0, 0))
    c.key(2.6)


@clip("decline_palm", "A raised palm: no thank you", trigger="decline", length=2.8, weight=3)
def _(c):
    c.key(0.35, ra=(-78, 8, 6), rf=(-46, 0, 0), head=(4, -16, 0), lid_pos=(0, 1.4, 0), root=(0, -6, 0))
    c.key(0.55, ra=(-82, 8, 6), rf=(-40, 0, 0))
    c.key(0.8, head=(6, -24, 0))
    c.key(1.05, head=(6, -10, 0))
    c.key(1.3, head=(6, -22, 0))
    c.key(1.9, ra=(-50, 6, 4), rf=(-40, 0, 0), head=(2, -8, 0), lid_pos=(0, 0.8, 0), root=(0, -3, 0))
    c.key(2.8)


@clip("decline_hand_back", "Hands it back with a small bow", trigger="decline", length=3.4, weight=2)
def _(c):
    # takes it in both hands, looks it over with the lid sinking, one small shake of the head, and holds it back out
    # to you with a correct little bow (from the feet, so children can do it too)
    held = dict(ra=(-46, -14, 0), rf=(-50, 0, 0), la=(-46, -14, 0), lf=(-50, 0, 0))
    c.key(0.4, head=(16, 0, 0), lid_pos=(0, 0.6, 0), **held)
    c.key(0.9, head=(14, 0, -10), lid_pos=(0, 1.4, 0), **held)
    c.key(1.3, head=(12, -10, -4))
    c.key(1.55, head=(12, 10, -4))
    c.key(1.8, head=(12, -4, -2), lid_pos=(0, 1.4, 0), **held)
    c.key(2.2, ra=(-70, -10, 0), rf=(-20, 0, 0), la=(-70, -10, 0), lf=(-20, 0, 0), head=(10, 0, 0), root=(4, 0, 0),
          lid_pos=(0, 1.0, 0))
    c.key(2.5, ra=(-72, -10, 0), la=(-72, -10, 0), root=(4, 0, 0))
    c.key(2.85, ra=(-16, -6, 0), rf=(-20, 0, 0), la=(-16, -6, 0), lf=(-20, 0, 0), head=(2, 0, 0), root=(0, 0, 0),
          lid_pos=(0, 0.4, 0))
    c.key(3.4)


@clip("pleased_mollified", "Lets out a breath and softens", trigger="pleased", length=3.4, weight=3)
def _(c):
    c.key(0.4, ra_pos=(0, -0.6, 0), la_pos=(0, -0.6, 0), head=(-6, 0, 0), lid_pos=(0, -0.6, 0))
    # the shoulders drop, the lid lifts gently, the head tilts and gives a small nod
    c.key(1.1, ra_pos=(0, 0.5, 0), la_pos=(0, 0.5, 0), head=(6, 0, 8), lid_pos=(0, -1.4, 0), lid=(-5, 0, 0),
          ra=(-18, -22, 0), rf=(-66, 0, 0), la=(-18, -22, 0), lf=(-66, 0, 0))
    c.key(1.6, head=(12, 0, 8))
    c.key(2.0, head=(2, 0, 6), lid_pos=(0, -1.2, 0))
    c.key(2.6, ra_pos=(0, 0, 0), la_pos=(0, 0, 0), lid_pos=(0, -0.4, 0), lid=(-1, 0, 0))
    c.key(3.4)


@clip("pleased_strike_record", "Strikes the grievance from the record", trigger="pleased", length=3.4, weight=2,
      require=["adult"])
def _(c):
    c.key(0.4, la=(-40, -18, 0), lf=(-66, 0, 0), ra=(-44, -28, 0), rf=(-84, 0, 0), head=(18, -4, 0))
    # one firm line through it, a dot, and the matter is closed
    c.key(0.8, ra=(-46, -40, 0), rf=(-86, 0, 0))
    c.key(1.15, ra=(-42, -4, 0), rf=(-82, 0, 0), head=(18, 4, 0))
    c.key(1.35, rf=(-92, 0, 0))
    c.key(1.5, rf=(-82, 0, 0))
    c.key(2.0, ra=(-20, -10, 0), rf=(-40, 0, 0), la=(-20, -10, 0), lf=(-30, 0, 0), head=(-4, 0, 0),
          lid_pos=(0, -1.4, 0), lid=(-5, 0, 0))
    c.key(2.4, head=(6, 0, 0), lid_pos=(0, -0.8, 0))
    c.key(3.4)


@clip("annoyed_turn_away", "Folds the arms and turns away", trigger="annoyed", length=3.6, weight=3)
def _(c):
    folded = dict(ra=(-40, -44, 0), rf=(-92, 0, 0), la=(-38, -46, 0), lf=(-90, 0, 0))
    c.key(0.45, root=(0, -28, 0), head=(-8, -8, 0), lid_pos=(0, 1.6, 0), cape=(2, 0, 2), **folded)
    c.key(0.65, root=(0, -32, 0), cape=(0, 0, 0))
    # a huff: the shoulders lift and drop
    c.key(1.0, ra_pos=(0, -0.7, 0), la_pos=(0, -0.7, 0), head=(-12, -10, 0))
    c.key(1.3, ra_pos=(0, 0.3, 0), la_pos=(0, 0.3, 0), head=(-8, -8, 0))
    c.key(2.7, root=(0, -30, 0), head=(-8, -6, 0), lid_pos=(0, 1.7, 0), ra_pos=(0, 0, 0), la_pos=(0, 0, 0),
          **folded)
    c.key(3.6)


@clip("annoyed_tapping", "Drums the fingers on a folded arm", trigger="annoyed", length=3.8, weight=2,
      require=["adult"])
def _(c):
    c.key(0.4, la=(-38, -46, 0), lf=(-90, 0, 0), ra=(-34, -40, 0), rf=(-84, 0, 0), head=(-4, 6, 0),
          lid_pos=(0, 2.0, 0))
    c.wobble(0.5, 2.6, 5, "rf", 8, base=(-84, 0, 0))
    c.key(1.4, head=(-4, -6, 0))
    c.key(2.0, head=(-4, 6, 0))
    c.key(2.6, head=(-4, -2, 0), lid_pos=(0, 2.2, 0))
    c.key(3.0, ra=(-30, -36, 0), rf=(-80, 0, 0), lid_pos=(0, 1.6, 0))
    c.key(3.8)


@clip("hurt_flinch", "Flinches and ducks into the shell", trigger="hurt", length=1.8, weight=3, blend=(.05, .4),
      mirror="free")
def _(c):
    # (the shell itself snaps shut on the model; this is the body's flinch under it)
    c.key(0.08, lid_pos=(0, 1.0, 0), head=(18, 0, 0), ra=(-46, -40, 0), rf=(-100, 0, 0), la=(-42, -40, 0),
          lf=(-96, 0, 0), root=(-5, 0, 0), root_pos=(0, 0, 1.2), ra_pos=(0, -0.8, 0), la_pos=(0, -0.8, 0))
    c.key(0.2, head=(16, 6, 0), root=(-4, 0, 0))
    c.key(0.9, head=(14, 4, 0), root=(-2, 0, 0), root_pos=(0, 0, 0.6), lid_pos=(0, 0.8, 0))
    c.key(1.8)


@clip("hurt_stagger", "Staggers to one side", trigger="hurt", length=1.8, weight=2, blend=(.05, .4), mirror="free")
def _(c):
    c.key(0.1, root=(0, 10, 7), root_pos=(-0.8, 0, 0.8), head=(10, -22, -10), lid_pos=(0, 1.2, 0),
          ra=(-30, 10, 30), rf=(-30, 0, 0), la=(-10, -30, -2), lf=(-80, 0, 0), cape=(12, 0, -8))
    c.key(0.35, root=(0, 6, -2), root_pos=(-0.4, 0, 0.4), head=(8, -10, 4), cape=(-4, 0, 4))
    c.key(0.6, root=(0, 4, 1), head=(10, -6, -2), cape=(2, 0, -1))
    c.key(1.1, ra=(-12, 4, 10), rf=(-14, 0, 0), la=(-12, -24, 0), lf=(-70, 0, 0), head=(6, 0, 0), lid_pos=(0, 0.6, 0))
    c.key(1.8)
