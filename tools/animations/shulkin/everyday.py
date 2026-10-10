"""Everyday moments of the Shulkin: precise, bookish shell-folk who count, note, tidy and peek out of their lids."""
from kit import clip


@clip("ledger_count", "Counts off on the fingers", length=4.4, weight=2)
def _(c):
    # right hand held up as the ledger, the left taps each finger, the head nodding to every count
    c.key(0.5, ra=(-28, -12, 0), rf=(-85, 0, 0), la=(-34, -28, 0), lf=(-72, 0, 0), head=(16, -2, -3))
    c.key(0.7, ra=(-30, -12, 0), rf=(-88, 0, 0))
    c.key(0.95, la=(-40, -30, 0), lf=(-80, 0, 0), head=(20, -4, -3))
    c.key(1.25, la=(-34, -27, 0), lf=(-72, 0, 0), head=(16, -3, -3))
    c.key(1.55, la=(-41, -29, 0), lf=(-81, 0, 0), head=(20, 0, -3), rf=(-90, 0, 0))
    c.key(1.85, la=(-34, -26, 0), lf=(-72, 0, 0), head=(16, 0, -3), rf=(-86, 0, 0))
    c.key(2.15, la=(-42, -28, 0), lf=(-82, 0, 0), head=(21, 3, -3))
    c.key(2.45, la=(-34, -26, 0), lf=(-72, 0, 0), head=(16, 3, -3), ra=(-30, -12, 0))
    c.rest(2.6, "lid", "lid_pos")
    # the sum comes out right: chin up, lid lifts
    c.key(2.9, head=(-5, 0, 4), lid_pos=(0, -1.6, 0), lid=(-8, 0, 0), ra=(-40, -10, 0), rf=(-80, 0, 0))
    c.key(3.2, head=(-1, 0, 2), lid_pos=(0, -1.2, 0), lid=(-6, 0, 0))
    c.key(3.6, lid_pos=(0, -0.2, 0), lid=(-1, 0, 0), la=(-20, -18, 0), lf=(-40, 0, 0))
    c.key(4.4)


@clip("stretch_reading", "Stretches after long reading", length=4.8, weight=1.5)
def _(c):
    # fingers laced and pushed out, then both arms up in a wide V with the lid yawning open; a roll of the shoulders
    c.key(0.6, ra=(-80, -20, 0), rf=(-20, 0, 0), la=(-80, -20, 0), lf=(-20, 0, 0), head=(4, 0, 0))
    c.key(0.8, ra=(-84, -22, 0), la=(-84, -22, 0))
    c.key(1.5, ra=(-20, 0, 150), rf=(-10, 0, 0), la=(-20, 0, 150), lf=(-10, 0, 0), head=(-16, 0, 0),
          lid_pos=(0, -2.4, 0), lid=(-10, 0, 0), root=(-3, 0, 0))
    c.key(2.2, ra=(-16, 0, 154), la=(-16, 0, 154), head=(-18, 0, 0), lid_pos=(0, -2.8, 0), lid=(-12, 0, 0),
          root=(-3, 0, 0))
    # the arms sweep down wide and the lid settles with a satisfied click
    c.key(2.9, ra=(-20, 0, 40), rf=(-10, 0, 0), la=(-20, 0, 40), lf=(-10, 0, 0), head=(6, 0, 0), lid_pos=(0, 0.6, 0),
          lid=(1, 0, 0), root=(0, 0, 0))
    c.key(3.3, ra=(0, 0, 6), la=(0, 0, 6), ra_pos=(0, -0.8, 0), la_pos=(0, -0.8, 0), lid_pos=(0, 0, 0), lid=(0, 0, 0))
    c.key(3.7, ra_pos=(0, 0.3, 0), la_pos=(0, 0.3, 0), head=(2, 0, 0))
    c.key(4.0, ra_pos=(0, 0, 0), la_pos=(0, 0, 0))
    c.key(4.8)


@clip("smooth_robe", "Smooths the robe", length=3.6, weight=2, require=["adult"])
def _(c):
    c.key(0.4, ra=(-22, -24, 0), rf=(-48, 0, 0), la=(-22, -24, 0), lf=(-48, 0, 0), head=(18, 0, 0), waist=(5, 0, 0))
    c.key(1.0, ra=(-8, -18, 0), rf=(-20, 0, 0), la=(-8, -18, 0), lf=(-20, 0, 0), head=(22, 0, 0))
    c.key(1.25, ra=(-20, -24, 0), rf=(-46, 0, 0), la=(-24, -24, 0), lf=(-50, 0, 0))
    c.key(1.85, ra=(-6, -16, 0), rf=(-16, 0, 0), la=(-7, -16, 0), lf=(-18, 0, 0), head=(22, 0, 0), waist=(6, 0, 0))
    # straightens up, quietly pleased with the hang of it
    c.key(2.3, ra=(4, 0, 6), rf=(-6, 0, 0), la=(4, 0, 6), lf=(-6, 0, 0), waist=(-4, 0, 0), head=(-6, 0, 0))
    c.key(2.6, ra=(2, 0, 3), la=(2, 0, 3), waist=(-2, 0, 0), head=(-3, 0, 0))
    c.key(3.6)


@clip("ponder_brim", "Ponders with a finger at the brim", length=5.2, weight=2, require=["adult"])
def _(c):
    c.key(0.5, la=(-32, -38, 0), lf=(-78, 0, 0), ra=(-42, -22, 0), rf=(-100, 0, 0), head=(6, 8, 6))
    c.key(0.9, ra=(-48, -26, 0), rf=(-112, 0, 0), head=(4, 10, 8), lid=(4, 0, 0))
    c.wobble(1.3, 2.7, 2.2, "rf", 6, base=(-112, 0, 0))
    c.key(3.0, head=(2, -6, -6), ra=(-48, -26, 0))
    c.key(3.2, lid=(4, 0, 0))
    c.rest(3.3, "lid_pos")
    # the idea arrives: a finger goes up and the lid lifts
    c.key(3.6, ra=(-96, -10, 0), rf=(-48, 0, 0), head=(-8, 0, 0), lid_pos=(0, -1.8, 0), lid=(-10, 0, 0))
    c.key(3.8, ra=(-90, -10, 0), rf=(-52, 0, 0))
    c.key(4.3, lid_pos=(0, -0.5, 0), lid=(-3, 0, 0), la=(-20, -20, 0), lf=(-40, 0, 0))
    c.key(5.2)


@clip("sky_gaze", "Gazes up into the void", length=5.0, weight=1.5)
def _(c):
    c.key(0.8, head=(-28, 0, 0), lid_pos=(0, -1.2, 0), lid=(-8, 0, 0), waist=(-4, 0, 0), ra=(6, 0, 5), la=(6, 0, 5))
    c.key(1.0, head=(-30, 0, 0))
    c.key(2.6, head=(-30, 6, 2), lid_pos=(0, -1.4, 0))
    # a long sigh: the head comes down and the shoulders drop
    c.key(3.2, head=(6, 0, 0), lid_pos=(0, 0.6, 0), lid=(1, 0, 0), waist=(2, 0, 0), ra=(2, 0, 0), la=(2, 0, 0),
          ra_pos=(0, 0.6, 0), la_pos=(0, 0.6, 0))
    c.key(3.6, head=(2, 0, 0), lid_pos=(0, 0.2, 0))
    c.key(5.0)


@clip("yawn_lid", "Stifles a yawn behind a hand", length=3.4, weight=1)
def _(c):
    c.key(0.3, head=(6, 0, 0), lid_pos=(0, 0.5, 0))
    c.key(0.9, head=(-18, 0, -4), lid_pos=(0, -3.2, 0), lid=(-16, 0, 0), ra=(-62, -32, 0), rf=(-105, 0, 0),
          waist=(-4, 0, 0))
    c.key(1.5, head=(-20, 0, -5), lid_pos=(0, -3.4, 0))
    c.key(1.8, lid_pos=(0, 0.8, 0), lid=(2, 0, 0), head=(4, 0, 0), waist=(1, 0, 0))
    c.key(2.0, head=(4, -8, 0), lid_pos=(0, 0.3, 0))
    c.key(2.2, head=(4, 7, 0))
    c.key(2.4, head=(3, -3, 0), lid_pos=(0, 0, 0), lid=(0, 0, 0))
    c.key(2.5, ra=(-10, -5, 0), rf=(-15, 0, 0))
    c.key(3.4)


@clip("folded_sway", "Folds the hands and sways", length=5.6, weight=1.5)
def _(c):
    folded = dict(ra=(-22, -24, 0), rf=(-76, 0, 0), la=(-22, -24, 0), lf=(-76, 0, 0))
    c.key(0.5, head=(4, 0, 0), **folded)
    c.key(5.0, **folded)
    c.wave(0.6, 5.0, 2.2, "root", 3, axis=2)
    c.wave(0.6, 5.0, 2.2, "head", -4, base=(4, 0, 0), axis=2, phase=0.1)
    c.wave(0.6, 5.0, 1.1, "lid_pos", 0.6, axis=1)
    c.key(5.6)


@clip("shell_settle", "Settles the shell with a click", length=2.6, weight=1.5)
def _(c):
    c.key(0.25, ra=(0, 0, -3), la=(0, 0, -3), ra_pos=(0, -0.8, 0), la_pos=(0, -0.8, 0), head=(-4, 0, 0),
          lid_pos=(0, -2.2, 0), lid=(-8, 0, 0))
    c.key(0.55, lid_pos=(0, 1.4, 0), lid=(1, 0, 0), head=(6, 0, 0), ra_pos=(0, 0.4, 0), la_pos=(0, 0.4, 0),
          ra=(1, 0, 1), la=(1, 0, 1))
    c.wobble(0.6, 1.3, 7, "head", 5, base=(5, 0, 0), axis=1, decay=0.8)
    c.key(0.8, lid_pos=(0, 0.4, 0), lid=(0, 0, 0))
    c.key(1.6, ra_pos=(0, 0, 0), la_pos=(0, 0, 0), lid_pos=(0, 0, 0))
    c.key(2.6)


@clip("tug_cape", "Tugs the cape straight", length=3.6, weight=1.5, require=["adult"])
def _(c):
    # a glance over the shoulder, a hand reaches back and pulls the cape true, a snap and a settle
    c.key(0.45, head=(4, 34, 0), ra=(10, 10, 6), rf=(-10, 0, 0), waist=(0, 6, 0))
    c.key(0.9, head=(8, 42, -4), ra=(24, 4, -2), rf=(-12, 0, 0), waist=(2, 10, 0), cape=(4, 0, 2))
    c.key(1.3, ra=(30, 6, -3), rf=(-8, 0, 0), cape=(16, 0, 9))
    c.key(1.6, ra=(29, 6, -3), rf=(-10, 0, 0), cape=(15, 0, 8))
    c.key(1.85, ra=(20, 8, 8), rf=(-18, 0, 0), cape=(-5, 0, -2), head=(6, 30, -2))
    c.key(2.1, cape=(3, 0, 1), ra=(4, 0, 3), rf=(-6, 0, 0), waist=(0, 3, 0), head=(0, 8, 0))
    c.key(2.35, cape=(-1, 0, 0), head=(-4, 0, 2), waist=(-2, 0, 0))
    c.key(3.6)


@clip("sleeve_tuck_rock", "Tucks the hands in the sleeves and rocks", length=5.4, weight=1.5, require=["adult"])
def _(c):
    tucked = dict(ra=(-38, -42, 0), rf=(-88, 0, 0), la=(-36, -44, 0), lf=(-92, 0, 0))
    c.key(0.6, head=(2, 0, 0), **tucked)
    c.key(4.7, **tucked)
    # heel to toe about the feet, the head nodding a beat behind, the cape trailing
    c.wave(0.7, 4.7, 2.0, "root", 3, axis=0)
    c.wave(0.7, 4.7, 2.0, "head", -3, base=(2, 0, 0), axis=0, phase=0.12)
    c.wave(0.7, 4.7, 2.0, "cape", -3, axis=0, phase=0.2)
    c.key(5.4)


@clip("air_note", "Writes a note in the air", length=4.4, weight=2)
def _(c):
    # the left forearm is the slate, the right finger writes a line, underlines it and dots it
    c.key(0.5, la=(-40, -18, 0), lf=(-70, 0, 0), ra=(-42, -26, 0), rf=(-78, 0, 0), head=(18, -6, 0))
    c.key(0.8, ra=(-46, -30, 0), rf=(-82, 0, 0))
    c.wave(0.8, 2.6, 0.45, "ra", 6, base=(-46, -30, 0), axis=1)
    c.wave(0.8, 2.6, 0.3, "rf", 5, base=(-82, 0, 0), axis=0)
    c.wave(0.8, 2.6, 1.8, "head", 6, base=(18, -6, 0), axis=1)
    c.key(2.95, ra=(-44, -12, 0), head=(18, 2, 0))
    c.key(3.15, rf=(-90, 0, 0))
    c.key(3.3, rf=(-80, 0, 0), head=(14, 0, -2))
    c.key(3.6, ra=(-30, -14, 0), rf=(-50, 0, 0), la=(-24, -14, 0), lf=(-40, 0, 0), head=(4, 0, 0))
    c.key(4.4)


@clip("dust_sleeve", "Brushes dust from a sleeve", length=3.2, weight=1.5, require=["adult"])
def _(c):
    c.key(0.45, la=(-48, -6, 0), lf=(-52, 0, 0), ra=(-40, -34, 0), rf=(-80, 0, 0), head=(14, -12, 0))
    c.cycle(0.6, 2.0, 0.46, dict(ra=(-42, -40, 0), rf=(-86, 0, 0)), dict(ra=(-36, -28, 0), rf=(-70, 0, 0)))
    # a flick off the fingers and a satisfied look
    c.key(2.25, ra=(-26, 18, 10), rf=(-30, 0, 0), head=(10, 10, 0))
    c.key(2.5, ra=(-14, 8, 4), rf=(-14, 0, 0), la=(-20, -2, 0), lf=(-20, 0, 0), head=(0, 0, 0))
    c.key(3.2)


@clip("polish_lid", "Polishes the lid with a sleeve", length=4.0, weight=1, require=["adult"])
def _(c):
    # the hand works round the edge of the lid, clear of the face
    c.key(0.55, ra=(-150, -6, 0), rf=(-66, 0, 0), head=(4, 0, 9), lid=(0, 0, 3))
    c.key(0.75, ra=(-156, -8, 0), rf=(-62, 0, 0))
    c.wobble(0.8, 2.6, 3.2, "ra", 6, base=(-156, -8, 0), axis=1)
    c.wave(0.8, 2.6, 0.62, "lid", 2.5, base=(0, 0, 3), axis=2)
    # the elbow straightens to lift the hand off before the arm comes down past the face
    c.key(2.75, ra=(-150, -6, 0), rf=(-24, 0, 0))
    c.key(2.95, ra=(-124, 6, 16), rf=(-40, 0, 0), head=(-6, 0, 2), lid_pos=(0, -1.0, 0), lid=(-4, 0, 0))
    c.key(3.25, ra=(-40, -6, 0), rf=(-20, 0, 0), lid_pos=(0, -0.3, 0), head=(-2, 0, 0))
    c.key(4.0)


@clip("ancestor_hush", "Listens for the old shells", length=5.6, weight=1)
def _(c):
    # something far off in the void: a hand to the breast, the lid lifting to hear, a small reverent nod
    c.key(0.9, ra=(-24, -38, 0), rf=(-86, 0, 0), head=(-6, 22, 10), lid_pos=(0, -1.0, 0), lid=(-5, 0, 0))
    c.key(1.3, head=(-7, 26, 12), lid_pos=(0, -1.6, 0), lid=(-7, 0, 0))
    c.key(2.9, head=(-8, 27, 13), lid_pos=(0, -1.7, 0))
    c.key(3.5, head=(14, 10, 4), lid_pos=(0, 1.0, 0), lid=(2, 0, 0), ra=(-26, -40, 0), rf=(-88, 0, 0))
    c.key(4.0, head=(10, 6, 2), lid_pos=(0, 0.4, 0))
    c.key(4.6, ra=(-10, -16, 0), rf=(-30, 0, 0), head=(2, 0, 0), lid_pos=(0, 0, 0), lid=(0, 0, 0))
    c.key(5.6)


@clip("proud_posture", "Squares the shoulders", length=4.2, weight=0.6, require=["adult"],
      boost={"manner:proud": 6})
def _(c):
    c.key(0.35, waist=(3, 0, 0), head=(4, 0, 0))
    c.key(0.9, waist=(-6, 0, 0), head=(-12, 0, 0), ra=(-12, -22, 0), rf=(-56, 0, 0), la=(-12, -22, 0),
          lf=(-56, 0, 0), lid_pos=(0, -1.2, 0), lid=(-4, 0, 0), cape=(-2, 0, 0))
    c.key(1.1, waist=(-5, 0, 0), head=(-10, 0, 0))
    # turns a little to show the profile, then back
    c.key(1.9, root=(0, 12, 0), head=(-10, -10, 0))
    c.key(2.9, root=(0, 10, 0), head=(-11, -8, 0))
    c.key(3.4, root=(0, 0, 0), head=(-4, 0, 0), waist=(-2, 0, 0), lid_pos=(0, -0.4, 0), lid=(-1, 0, 0))
    c.key(4.2)


@clip("shy_hunch", "Draws into the shell", length=4.6, weight=0.5, boost={"manner:shy": 6})
def _(c):
    c.key(0.5, ra=(-8, -6, -4), la=(-8, -6, -4), ra_pos=(0, -0.8, 0), la_pos=(0, -0.8, 0), head=(12, -14, 0),
          lid_pos=(0, 2.2, 0))
    c.key(0.7, lid_pos=(0, 2.5, 0))
    c.key(1.9, head=(13, -16, 0))
    # a quick glance back through a crack of the lid, then away again
    c.key(2.3, head=(8, 6, -3), lid_pos=(0, 1.2, 0))
    c.key(2.8, head=(8, 8, -3), lid_pos=(0, 1.0, 0))
    c.key(3.1, head=(13, -12, 0), lid_pos=(0, 2.4, 0))
    c.key(3.9, ra_pos=(0, 0, 0), la_pos=(0, 0, 0), ra=(-2, 0, 0), la=(-2, 0, 0), head=(4, -4, 0),
          lid_pos=(0, 0.6, 0))
    c.key(4.6)


@clip("restless_shift", "Shifts and drums the fingers", length=4.2, weight=0.5, boost={"manner:restless": 6})
def _(c):
    c.key(0.4, la=(-30, -40, 0), lf=(-84, 0, 0), ra=(-26, -30, 0), rf=(-70, 0, 0), root=(0, 0, 3), head=(4, -10, 0))
    c.wobble(0.5, 1.8, 5, "rf", 9, base=(-74, 0, 0))
    c.key(1.2, head=(2, 18, 0), lid_pos=(0, -0.8, 0))
    c.key(1.5, head=(2, 20, 0), lid_pos=(0, 0, 0))
    # weight onto the other foot, a look the other way, more drumming
    c.key(2.1, root=(0, 0, -3), head=(4, -16, 2), lid_pos=(0, -0.8, 0))
    c.wobble(2.1, 3.3, 5, "rf", 9, base=(-74, 0, 0))
    c.key(2.4, lid_pos=(0, 0, 0))
    c.key(3.0, root=(0, 0, -2), head=(0, -4, 0))
    c.key(3.5, la=(-14, -18, 0), lf=(-30, 0, 0), ra=(-10, -10, 0), root=(0, 0, 1), head=(0, 4, 0))
    c.key(4.2)


@clip("busy_tick_off", "Ticks off the room at a glance", length=3.6, weight=0.5, require=["adult"],
      boost={"manner:busy": 6})
def _(c):
    # a forefinger snaps to four things in turn (that, that, that and that), a curt nod for each; then the hands
    # brush each other clean and the lid clicks: done
    for t, arm, head in ((0.3, (-62, -30, 0), (14, -24, 0)), (0.75, (-104, 30, 12), (-12, 26, 0)),
                         (1.2, (-84, 4, 2), (2, 0, 0)), (1.65, (-58, 46, 20), (16, 32, 0))):
        c.key(t, ra=arm, rf=(-12, 0, 0), head=head)
        c.key(t + 0.2, rf=(-22, 0, 0), head=(head[0] + 7, head[1], 0))
    c.key(2.2, ra=(-40, -20, 0), rf=(-50, 0, 0), la=(-40, -20, 0), lf=(-50, 0, 0), head=(6, 0, 0))
    c.key(2.35, ra=(-44, -10, 0), la=(-36, -30, 0), lid_pos=(0, -1.0, 0), lid=(-4, 0, 0))
    c.key(2.5, ra=(-36, -30, 0), la=(-44, -10, 0))
    c.key(2.65, ra=(-42, -14, 0), la=(-38, -24, 0))
    c.key(2.9, ra=(-14, 0, 4), rf=(-10, 0, 0), la=(-14, 0, 4), lf=(-10, 0, 0), head=(0, 0, 0), lid_pos=(0, 0.3, 0),
          lid=(0, 0, 0))
    c.key(3.6)


@clip("flighty_start", "Starts and snaps shut at a sound", length=4.4, weight=0.5, boost={"manner:flighty": 6})
def _(c):
    # a sound somewhere: the lid slams, the arms come in; then a slow peek out, a look round and relief
    c.key(0.15, lid_pos=(0, -0.8, 0), head=(-4, 8, 0))
    c.key(0.3, lid_pos=(0, 4.0, 0), head=(14, 0, 0), ra=(-20, -20, -4), rf=(-50, 0, 0), la=(-20, -20, -4),
          lf=(-50, 0, 0), root_pos=(0, 0, 0.6))
    c.key(0.45, lid_pos=(0, 3.8, 0), head=(16, 0, 0))
    c.key(1.4, lid_pos=(0, 3.8, 0), head=(15, 0, 0))
    c.key(2.0, lid_pos=(0, 2.4, 0), head=(10, -16, 0))
    c.key(2.5, head=(10, 16, 0), lid_pos=(0, 2.0, 0))
    c.key(2.9, head=(4, 0, 0), lid_pos=(0, -0.8, 0), lid=(-4, 0, 0), ra=(-6, 0, 2), rf=(-10, 0, 0), la=(-6, 0, 2),
          lf=(-10, 0, 0), root_pos=(0, 0, 0))
    c.key(3.3, head=(8, 0, 0), lid_pos=(0, 0.3, 0), lid=(0, 0, 0), ra=(2, 0, 1), la=(2, 0, 1))
    c.key(4.4)
