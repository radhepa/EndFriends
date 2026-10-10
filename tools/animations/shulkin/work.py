"""Work: every Shulkin trade at its bench, shelf, loom, lamp or roost. Grown-ups only; boosted while working."""
from kit import clip

WORK = {"working": 3}


@clip("archivist_read", "Reads down a page and turns it", length=6.6, weight=4,
      require=["adult", "job:archivist"], boost=WORK)
def _(c):
    tome = dict(ra=(-34, -26, 0), rf=(-62, 0, 0), la=(-34, -26, 0), lf=(-62, 0, 0))
    c.key(0.5, head=(22, -8, 0), lid=(3, 0, 0), **tome)
    # three lines read left to right, the eye snapping back at each line's end
    for i, t in enumerate((0.6, 1.8, 3.0)):
        c.key(t, head=(22 + i * 2, -9, 0))
        c.key(t + 0.95, head=(23 + i * 2, 9, 0))
    c.key(4.2, head=(26, -2, 0), **tome)
    # the page turns: the right hand lifts and sweeps across, the head follows it
    c.key(4.55, ra=(-48, 12, 6), rf=(-70, 0, 0), head=(22, 8, 0))
    c.key(5.0, ra=(-46, -44, 0), rf=(-78, 0, 0), head=(20, -10, 0))
    c.key(5.3, ra=(-34, -28, 0), rf=(-62, 0, 0), head=(23, -6, 0), lid=(3, 0, 0))
    c.key(5.9, head=(20, -4, 0), **tome)
    c.key(6.6)


@clip("archivist_shelve", "Shelves a volume and squares it", length=5.2, weight=3,
      require=["adult", "job:archivist"], boost=WORK)
def _(c):
    c.key(0.5, ra=(-120, 12, 8), rf=(-40, 0, 0), head=(-14, 6, 0), la=(-20, -10, 0), lf=(-30, 0, 0))
    c.key(1.0, ra=(-152, 14, 10), rf=(-18, 0, 0), head=(-24, 8, 0), root_pos=(0, -0.6, 0), lid_pos=(0, -0.8, 0))
    c.key(1.4, ra=(-158, 14, 10), rf=(-10, 0, 0))
    # two taps to push it flush
    c.key(1.6, rf=(-24, 0, 0))
    c.key(1.75, rf=(-8, 0, 0))
    c.key(1.9, rf=(-22, 0, 0))
    c.key(2.05, rf=(-10, 0, 0), root_pos=(0, -0.6, 0))
    c.key(2.5, ra=(-60, -14, 0), rf=(-40, 0, 0), head=(10, -10, 0), root_pos=(0, 0, 0), lid_pos=(0, 0, 0))
    # a fingertip runs along the spines at chest height, checking the order
    c.key(2.9, la=(-58, 34, 4), lf=(-24, 0, 0), head=(12, -26, 0), ra=(-20, -10, 0), rf=(-20, 0, 0))
    c.key(4.1, la=(-58, -14, 0), lf=(-28, 0, 0), head=(12, 6, 0))
    c.key(4.4, la=(-50, -12, 0), head=(4, 4, 0))
    c.key(5.2)


@clip("lamplighter_raise", "Raises the lighting pole to a lamp", length=6.2, weight=4,
      require=["adult", "job:lamplighter"], boost=WORK)
def _(c):
    c.key(0.5, ra=(-80, -14, 0), rf=(-50, 0, 0), la=(-70, -20, 0), lf=(-50, 0, 0), head=(-6, 0, 0))
    c.key(1.3, ra=(-130, -12, 4), rf=(-30, 0, 0), la=(-114, -14, 4), lf=(-32, 0, 0), head=(-20, 0, 0),
          waist=(-3, 0, 0), lid_pos=(0, -1.2, 0), lid=(-6, 0, 0), cape=(2, 0, 0))
    c.key(1.5, ra=(-134, -12, 4), la=(-118, -14, 4), head=(-22, 0, 0))
    # small careful nudges to catch the wick
    c.wobble(1.7, 3.3, 2.5, "ra", 3, base=(-134, -12, 4))
    c.wobble(1.7, 3.3, 2.5, "la", -3, base=(-118, -14, 4))
    c.key(3.6, lid_pos=(0, -2.2, 0), lid=(-10, 0, 0), head=(-24, 0, 0))
    c.key(3.9, lid_pos=(0, -1.6, 0), lid=(-7, 0, 0))
    c.key(4.8, ra=(-70, -14, 0), rf=(-50, 0, 0), la=(-62, -20, 0), lf=(-52, 0, 0), head=(6, 0, 0), waist=(2, 0, 0),
          lid_pos=(0, -0.4, 0), lid=(-2, 0, 0), cape=(0, 0, 0))
    c.key(5.2, head=(10, 0, 0))
    c.key(6.2)


@clip("lamplighter_trim", "Trims a wick and shields the flame", length=5.0, weight=3,
      require=["adult", "job:lamplighter"], boost=WORK)
def _(c):
    c.key(0.5, la=(-48, -22, 0), lf=(-72, 0, 0), ra=(-44, -18, 0), rf=(-82, 0, 0), head=(20, 0, 0), lid=(3, 0, 0))
    c.wobble(0.7, 1.8, 3, "rf", 6, base=(-82, 0, 0))
    # leans in close and blows the snuff away: the lid lifts
    c.key(2.1, waist=(8, 0, 0), head=(16, 0, 0), lid_pos=(0, -1.4, 0), lid=(-6, 0, 0), cape=(-4, 0, 0))
    c.key(2.35, head=(10, 0, 0), lid_pos=(0, -1.8, 0))
    c.key(2.7, waist=(4, 0, 0), head=(18, 0, 0), lid_pos=(0, -0.4, 0), lid=(0, 0, 0), cape=(-2, 0, 0))
    # both hands cup round the flame
    c.key(3.1, ra=(-50, -40, 0), rf=(-88, 0, 0), la=(-50, -40, 0), lf=(-88, 0, 0))
    c.key(3.9, ra=(-50, -42, 0), la=(-50, -42, 0), head=(16, 0, 4), waist=(2, 0, 0))
    c.key(4.3, ra=(-20, -16, 0), rf=(-30, 0, 0), la=(-20, -16, 0), lf=(-30, 0, 0), head=(4, 0, 0), waist=(0, 0, 0),
          cape=(0, 0, 0), lid_pos=(0, 0, 0))
    c.key(5.0)


@clip("weaver_loom", "Throws the shuttle and beats the weft", length=6.4, weight=4,
      require=["adult", "job:weaver"], boost=WORK)
def _(c):
    base = dict(ra=(-36, -6, 0), rf=(-52, 0, 0), la=(-36, -6, 0), lf=(-52, 0, 0))
    c.key(0.5, head=(18, 0, 0), **base)
    for i in range(2):
        t = 0.7 + i * 2.6
        thrower, catcher = ("ra", "la") if i == 0 else ("la", "ra")
        tf, cf = ("rf", "lf") if i == 0 else ("lf", "rf")
        # throw across, the head following the shuttle
        c.key(t + 0.35, **{thrower: (-40, -38, 0), tf: (-44, 0, 0), catcher: (-38, 12, 4)},
              head=(18, 12 if i else -12, 0))
        c.key(t + 0.75, **{thrower: (-36, -6, 0), tf: (-52, 0, 0), catcher: (-36, -6, 0)}, head=(18, 0, 0))
        # beat the weft home with both hands
        c.key(t + 1.15, ra=(-22, -4, 0), rf=(-78, 0, 0), la=(-22, -4, 0), lf=(-78, 0, 0), waist=(-3, 0, 0),
              cape=(2, 0, 0))
        c.key(t + 1.4, ra=(-34, -6, 0), rf=(-56, 0, 0), la=(-34, -6, 0), lf=(-56, 0, 0), waist=(2, 0, 0),
              cape=(-1, 0, 0))
        c.key(t + 1.8, waist=(0, 0, 0), cape=(0, 0, 0), **base)
    c.key(5.8, head=(14, 0, 0), **base)
    c.key(6.4)


@clip("weaver_draw", "Draws a thread out to length", length=5.2, weight=3,
      require=["adult", "job:weaver"], boost=WORK)
def _(c):
    c.key(0.5, la=(-42, -30, 0), lf=(-88, 0, 0), ra=(-44, -32, 0), rf=(-86, 0, 0), head=(18, 0, 0))
    # pinches the thread and draws it out wide, the eye running along it
    c.key(1.6, ra=(-64, 44, 18), rf=(-10, 0, 0), head=(8, 30, 0))
    c.key(1.85, ra=(-62, 46, 20), rf=(-8, 0, 0), head=(8, 33, 0))
    c.key(2.3, head=(12, 4, 0))
    # a measured twist between the fingers, then wound back onto the spindle
    c.wobble(2.3, 3.1, 4, "rf", 7, base=(-10, 0, 0))
    c.key(3.6, ra=(-46, -10, 0), rf=(-70, 0, 0), head=(18, -6, 0))
    c.key(3.9, ra=(-42, -26, 0), rf=(-84, 0, 0))
    c.key(4.2, ra=(-46, -14, 0), rf=(-74, 0, 0))
    c.key(4.6, ra=(-20, -10, 0), rf=(-30, 0, 0), la=(-20, -12, 0), lf=(-30, 0, 0), head=(4, 0, 0))
    c.key(5.2)


@clip("shellwright_tap", "Taps a shell plate true", length=6.0, weight=4,
      require=["adult", "job:shellwright"], boost=WORK)
def _(c):
    c.key(0.5, la=(-46, -18, 0), lf=(-56, 0, 0), ra=(-50, -14, 0), rf=(-70, 0, 0), head=(22, -4, 0), lid=(3, 0, 0))
    # four measured taps of the little hammer, the last one lighter
    for i, t in enumerate((0.8, 1.45, 2.1, 2.75)):
        lift = 30 if i < 3 else 20
        c.key(t, ra=(-50 - lift, -12, 0), rf=(-96, 0, 0), head=(20, -4, 0))
        c.key(t + 0.25, ra=(-44, -14, 0), rf=(-62, 0, 0), head=(23, -4, 0), la=(-46, -18, 0))
        c.key(t + 0.33, la=(-44, -18, 0))
    # holds it up to the light and squints along the edge
    c.key(3.6, la=(-92, -14, 0), lf=(-62, 0, 0), ra=(-30, -10, 0), rf=(-40, 0, 0), head=(-6, -10, -6),
          lid_pos=(0, 0.8, 0), lid=(3, 0, 0))
    c.key(4.4, la=(-94, -10, 0), head=(-8, -14, -8))
    c.key(4.8, head=(4, -6, 0), lid_pos=(0, -0.8, 0), lid=(-4, 0, 0))
    c.key(5.1, head=(-2, -4, 0))
    c.key(5.3, la=(-40, -16, 0), lf=(-50, 0, 0), lid_pos=(0, 0, 0), lid=(0, 0, 0))
    c.key(6.0)


@clip("shellwright_measure", "Spans a plate between the fingers", length=5.0, weight=3,
      require=["adult", "job:shellwright"], boost=WORK)
def _(c):
    c.key(0.5, ra=(-48, 10, 6), rf=(-60, 0, 0), la=(-48, 10, 6), lf=(-60, 0, 0), head=(18, 0, 0))
    c.key(1.0, ra=(-48, 2, 2), la=(-48, 2, 2))
    c.key(1.3, ra=(-48, 6, 4), la=(-48, 6, 4))
    c.key(1.5, ra=(-48, 4, 3), la=(-48, 4, 3), head=(20, 0, 4))
    # the span is held up to the eye and compared
    c.key(2.2, ra=(-70, 4, 3), rf=(-70, 0, 0), la=(-70, 4, 3), lf=(-70, 0, 0), head=(6, 0, 8))
    c.key(2.9, head=(6, 0, -6))
    # a fingertip runs round the edge; a click of the lid: it will do
    c.key(3.3, ra=(-50, -20, 0), rf=(-70, 0, 0), la=(-48, -10, 0), lf=(-62, 0, 0), head=(18, 0, 0))
    c.key(3.9, ra=(-48, 10, 4), rf=(-58, 0, 0), head=(18, 8, 0))
    c.key(4.1, lid_pos=(0, -1.2, 0), lid=(-4, 0, 0), head=(10, 0, 0))
    c.key(4.3, lid_pos=(0, 0.3, 0), lid=(0, 0, 0))
    c.key(5.0)


@clip("wayfinder_bearing", "Takes a bearing over the void", length=5.8, weight=4,
      require=["adult", "job:wayfinder"], boost=WORK)
def _(c):
    # a hand shades the gap of the lid, a slow sweep of the horizon, then a firm point: that way
    c.key(0.6, ra=(-70, 50, 70), rf=(-90, 0, 0), head=(-6, -10, 0), root=(0, -16, 0), lid_pos=(0, -0.8, 0))
    c.key(1.0, ra=(-74, 50, 70), rf=(-92, 0, 0), head=(-6, -12, 0), root=(0, -18, 0))
    c.key(2.6, head=(-8, 10, 0), root=(0, 16, 0))
    c.key(3.0, ra=(-74, 50, 70), rf=(-92, 0, 0), head=(-8, 10, 0), root=(0, 16, 0), lid_pos=(0, -1.6, 0),
          lid=(-6, 0, 0))
    c.key(3.4, ra=(-88, 34, 6), rf=(-6, 0, 0), la=(-16, -12, 0), lf=(-40, 0, 0), head=(-6, 16, 0), root=(0, 16, 0))
    c.key(3.6, ra=(-92, 36, 6), head=(-6, 18, 0))
    c.key(4.4, ra=(-90, 34, 6), head=(-4, 16, 0), root=(0, 16, 0))
    c.key(4.7, head=(6, 10, 0), lid_pos=(0, -0.4, 0), lid=(-2, 0, 0))
    c.key(5.0, ra=(-30, 10, 2), rf=(-20, 0, 0), la=(-10, -6, 0), lf=(-14, 0, 0), head=(2, 6, 0), root=(0, 4, 0))
    c.key(5.8)


@clip("keeper_cradle", "Cradles an empty shell", length=6.2, weight=4,
      require=["adult", "job:keeper"], boost=WORK)
def _(c):
    cradle = dict(ra=(-30, -32, 0), rf=(-72, 0, 0), la=(-28, -34, 0), lf=(-76, 0, 0))
    c.key(0.6, head=(24, 0, 0), lid_pos=(0, 1.0, 0), **cradle)
    c.wave(0.7, 3.3, 1.3, "root", 2.5, axis=2)
    c.wave(0.7, 3.3, 1.3, "head", -3, base=(24, 0, 0), axis=2, phase=0.15)
    c.key(3.3, **cradle)
    # one hand polishes the old shell in small circles
    c.key(3.6, ra=(-40, -26, 0), rf=(-74, 0, 0))
    c.wave(3.6, 5.2, 0.5, "ra", 6, base=(-40, -26, 0), axis=1)
    c.wave(3.6, 5.2, 0.5, "rf", 6, base=(-74, 0, 0), axis=0, phase=0.25)
    c.key(5.4, head=(18, 0, 0), lid_pos=(0, 0, 0), ra=(-30, -32, 0), rf=(-72, 0, 0))
    c.key(6.2)


@clip("keeper_bless", "Bows over the old shells", length=5.4, weight=3,
      require=["adult", "job:keeper"], boost=WORK)
def _(c):
    joined = dict(ra=(-42, -42, 0), rf=(-96, 0, 0), la=(-42, -42, 0), lf=(-96, 0, 0))
    c.key(0.6, head=(6, 0, 0), **joined)
    # a deep, slow bow with the lid lowered: the ancestors are owed that much
    c.key(1.4, waist=(11, 0, 0), root=(5, 0, 0), cape=(-8, 0, 0), head=(14, 0, 0), lid_pos=(0, 2.4, 0))
    c.key(1.6, waist=(12, 0, 0), root=(5, 0, 0), cape=(-9, 0, 0), lid_pos=(0, 2.6, 0))
    c.key(2.9, waist=(11, 0, 0), root=(5, 0, 0), cape=(-8, 0, 0), lid_pos=(0, 2.5, 0), **joined)
    c.key(3.5, waist=(-2, 0, 0), root=(0, 0, 0), cape=(1, 0, 0), head=(0, 0, 0), lid_pos=(0, -1.0, 0),
          lid=(-4, 0, 0))
    # an open hand toward the shells, palm down
    c.key(3.9, ra=(-62, 28, 10), rf=(-28, 0, 0), la=(-30, -20, 0), lf=(-60, 0, 0), head=(10, 10, 0),
          waist=(0, 0, 0), cape=(0, 0, 0))
    c.key(4.4, ra=(-58, 30, 10), head=(10, 12, 0), lid_pos=(0, -0.3, 0), lid=(-1, 0, 0))
    c.key(5.4)


@clip("hallkeeper_wipe", "Wipes down the long table", length=6.0, weight=4,
      require=["adult", "job:hallkeeper"], boost=WORK)
def _(c):
    c.key(0.6, waist=(10, 0, 0), root=(4, 0, 0), cape=(-6, 0, 0), head=(16, 0, 0), la=(-52, -6, 0),
          lf=(-22, 0, 0), ra=(-56, -10, 0), rf=(-24, 0, 0))
    c.wave(0.7, 3.5, 0.9, "ra", 9, base=(-56, -10, 0), axis=1)
    c.wave(0.7, 3.5, 0.9, "rf", 8, base=(-24, 0, 0), axis=0, phase=0.25)
    c.wave(0.7, 3.5, 0.9, "head", 4, base=(16, 0, 0), axis=1, phase=0.1)
    c.key(3.5, waist=(10, 0, 0), root=(4, 0, 0), cape=(-6, 0, 0), la=(-52, -6, 0), lf=(-22, 0, 0))
    # straightens, squints for streaks, then folds the cloth over the left forearm like a steward and pats it down
    c.key(4.0, waist=(2, 0, 0), root=(0, 0, 0), cape=(-1, 0, 0), head=(12, 0, 10), la=(-20, -6, 0),
          lf=(-20, 0, 0))
    c.key(4.4, head=(12, 0, -6))
    c.key(4.75, la=(-24, -24, 0), lf=(-84, 0, 0), ra=(-46, -20, 0), rf=(-60, 0, 0), head=(14, -6, 0),
          waist=(0, 0, 0), cape=(0, 0, 0))
    c.key(4.95, ra=(-40, -26, 0), rf=(-74, 0, 0))
    c.key(5.1, ra=(-44, -22, 0), rf=(-64, 0, 0))
    c.key(5.3, ra=(-20, -8, 0), rf=(-30, 0, 0), head=(2, 0, 0), la=(-24, -24, 0), lf=(-84, 0, 0))
    c.key(6.0)


@clip("trader_weigh", "Weighs goods in two hands", length=5.4, weight=4,
      require=["adult", "job:trader"], boost=WORK)
def _(c):
    c.key(0.5, ra=(-40, 14, 6), rf=(-46, 0, 0), la=(-40, 14, 6), lf=(-46, 0, 0), head=(14, 0, 0))
    # the hands see-saw like a balance, less each time, the head tipping toward the heavier
    for i, (t, d) in enumerate(((0.9, 7), (1.5, -6), (2.1, 4), (2.7, -2.5))):
        c.key(t, ra=(-40 + d, 14, 6), la=(-40 - d, 14, 6), head=(14, 0, -d))
    c.key(3.2, ra=(-40, 14, 6), la=(-40, 14, 6), head=(14, 0, 0))
    c.key(3.6, head=(4, 0, 0), lid_pos=(0, -1.4, 0), lid=(-6, 0, 0))
    c.key(3.85, head=(10, 0, 0))
    c.key(4.2, ra=(-20, 6, 2), rf=(-26, 0, 0), la=(-20, 6, 2), lf=(-26, 0, 0), head=(2, 0, 0), lid_pos=(0, -0.3, 0),
          lid=(-1, 0, 0))
    c.key(5.4)


@clip("trader_offer", "Lays out the wares with a flourish", length=4.8, weight=3,
      require=["adult", "job:trader"], boost=WORK)
def _(c):
    c.key(0.45, ra=(-52, -30, 0), rf=(-64, 0, 0), head=(12, -8, 0), la=(-20, -14, 0), lf=(-40, 0, 0))
    c.key(1.4, ra=(-54, 40, 14), rf=(-22, 0, 0), head=(8, 26, 0), lid_pos=(0, -1.0, 0), lid=(-4, 0, 0))
    c.key(1.6, ra=(-52, 42, 14), head=(8, 28, 0))
    # two taps on the counter: this one, and this one
    c.key(2.0, ra=(-50, 16, 6), rf=(-40, 0, 0), head=(18, 10, 0), lid_pos=(0, 0, 0), lid=(0, 0, 0))
    c.key(2.15, rf=(-30, 0, 0))
    c.key(2.35, ra=(-50, 0, 4), rf=(-42, 0, 0), head=(18, 0, 0))
    c.key(2.5, rf=(-30, 0, 0))
    c.key(3.0, ra=(-30, -30, 0), rf=(-80, 0, 0), la=(-30, -30, 0), lf=(-80, 0, 0), head=(4, 0, 0),
          waist=(8, 0, 0), cape=(-3, 0, 0))
    c.key(3.6, waist=(0, 0, 0), cape=(0, 0, 0))
    c.key(4.8)
