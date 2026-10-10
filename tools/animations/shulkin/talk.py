"""Conversation: gestures while a Shulkin's line types out, and how they listen while you choose a reply."""
from kit import clip


@clip("talk_enumerate", "Enumerates the points", trigger="talk", length=4.0, weight=3)
def _(c):
    # the left palm is the list, the right forefinger touches each item in turn
    c.key(0.4, la=(-38, -20, 0), lf=(-62, 0, 0), ra=(-36, -26, 0), rf=(-84, 0, 0), head=(6, 0, 0))
    for i, t in enumerate((0.75, 1.5, 2.25)):
        c.key(t, ra=(-40 - i * 2, -30 + i * 4, 0), rf=(-92, 0, 0), head=(10, -4 + i * 4, 0))
        c.key(t + 0.3, ra=(-34 - i * 2, -24 + i * 4, 0), rf=(-80, 0, 0), head=(4, -2 + i * 4, 0))
    c.key(3.1, ra=(-30, -10, 0), rf=(-60, 0, 0), la=(-30, -12, 0), lf=(-50, 0, 0), head=(0, 0, 0))
    c.key(4.0)


@clip("talk_footnote", "Raises a finger for a footnote", trigger="talk", length=3.2, weight=3)
def _(c):
    c.key(0.3, ra=(-50, -10, 0), rf=(-70, 0, 0), head=(4, 0, 0))
    c.key(0.65, ra=(-96, -10, 0), rf=(-58, 0, 0), head=(-6, 0, 6), lid_pos=(0, -1.2, 0), lid=(-4, 0, 0))
    c.key(0.8, ra=(-92, -10, 0), rf=(-62, 0, 0))
    # the finger wags its small point home
    c.wobble(0.9, 2.1, 3, "rf", 8, base=(-62, 0, 0), decay=0.4)
    c.wobble(0.9, 2.1, 1.5, "head", 4, base=(-6, 0, 6), axis=2)
    c.key(2.5, ra=(-40, -8, 0), rf=(-40, 0, 0), head=(0, 0, 2), lid_pos=(0, -0.3, 0), lid=(0, 0, 0))
    c.key(3.2)


@clip("talk_open_palms", "Opens both palms", trigger="talk", length=3.2, weight=3)
def _(c):
    c.key(0.25, ra=(-20, -10, 0), rf=(-50, 0, 0), la=(-20, -10, 0), lf=(-50, 0, 0))
    c.key(0.7, ra=(-42, 32, 14), rf=(-38, 0, 0), la=(-40, 30, 14), lf=(-40, 0, 0), head=(-2, 0, 8),
          ra_pos=(0, -0.5, 0), la_pos=(0, -0.5, 0), lid_pos=(0, -0.8, 0))
    c.key(0.9, ra=(-44, 34, 16), la=(-42, 32, 16))
    c.key(1.8, ra=(-40, 30, 13), la=(-38, 28, 13), head=(0, 0, 6))
    c.key(2.3, ra=(-18, 6, 4), rf=(-24, 0, 0), la=(-18, 6, 4), lf=(-24, 0, 0), head=(2, 0, 0),
          ra_pos=(0, 0, 0), la_pos=(0, 0, 0), lid_pos=(0, 0, 0))
    c.key(3.2)


@clip("talk_shape_tome", "Shapes a book in the air", trigger="talk", length=3.8, weight=2, require=["adult"])
def _(c):
    # both hands frame something the size of a ledger, weigh it, then close it like a cover
    c.key(0.45, ra=(-54, 22, 8), rf=(-62, 0, 0), la=(-54, 22, 8), lf=(-62, 0, 0), head=(10, 0, 0))
    c.key(0.65, ra=(-56, 24, 9), la=(-56, 24, 9))
    c.key(1.4, ra=(-62, 18, 8), la=(-50, 26, 8), head=(8, 0, -4))
    c.key(2.0, ra=(-50, 26, 8), la=(-62, 18, 8), head=(8, 0, 4))
    c.key(2.5, ra=(-48, -22, 0), rf=(-80, 0, 0), la=(-48, -22, 0), lf=(-80, 0, 0), head=(12, 0, 0))
    c.key(2.65, ra=(-46, -26, 0), la=(-46, -26, 0), lid_pos=(0, 0.6, 0))
    c.key(2.9, lid_pos=(0, 0, 0), head=(4, 0, 0))
    c.key(3.8)


@clip("talk_dry_aside", "A dry aside behind the hand", trigger="talk", length=3.4, weight=2, require=["adult"])
def _(c):
    # the hand comes up beside the gap, the lid tips up on one side: a wry remark
    c.key(0.5, ra=(-82, -28, 0), rf=(-96, 0, 0), head=(2, -14, 8), lid_pos=(0, -0.8, 0), lid=(-3, 0, -7),
          root=(0, -6, 0))
    c.key(0.75, ra=(-86, -28, 0), head=(2, -16, 9), lid=(-4, 0, -8))
    c.key(1.9, ra=(-84, -28, 0), head=(4, -14, 8), lid=(-4, 0, -8))
    # back to you with a small knowing nod
    c.key(2.4, ra=(-30, -12, 0), rf=(-40, 0, 0), head=(8, 0, 0), lid_pos=(0, -0.3, 0), lid=(0, 0, -2),
          root=(0, 0, 0))
    c.key(2.7, head=(0, 0, 0), lid=(0, 0, 0))
    c.key(3.4)


@clip("listen_tilt", "Tilts the head and lifts the lid", trigger="listen", length=3.8, weight=3)
def _(c):
    folded = dict(ra=(-20, -22, 0), rf=(-72, 0, 0), la=(-20, -22, 0), lf=(-72, 0, 0))
    c.key(0.6, head=(-2, 6, 12), lid_pos=(0, -1.4, 0), lid=(-5, 0, 0), **folded)
    c.key(0.8, head=(-2, 7, 13))
    c.key(2.4, head=(-3, 8, 12), lid_pos=(0, -1.6, 0), **folded)
    c.key(2.8, head=(8, 4, 6), lid_pos=(0, -0.6, 0), lid=(-2, 0, 0))
    c.key(3.1, head=(2, 2, 3))
    c.key(3.8)


@clip("listen_chin", "Hand under the brim and slow nods", trigger="listen", length=4.2, weight=3,
      require=["adult"])
def _(c):
    c.key(0.5, la=(-32, -38, 0), lf=(-78, 0, 0), ra=(-46, -26, 0), rf=(-112, 0, 0), head=(4, 0, -5))
    c.key(1.2, head=(10, 0, -5), lid_pos=(0, 0.4, 0))
    c.key(1.6, head=(3, 0, -5), lid_pos=(0, 0, 0))
    c.key(2.4, head=(10, 0, -4), lid_pos=(0, 0.4, 0))
    c.key(2.8, head=(3, 0, -4), lid_pos=(0, 0, 0))
    c.key(3.4, la=(-32, -38, 0), lf=(-78, 0, 0), ra=(-46, -26, 0), rf=(-112, 0, 0), head=(2, 0, -2))
    c.key(4.2)


@clip("listen_note_palm", "Notes it down in the palm", trigger="listen", length=4.4, weight=2, require=["adult"])
def _(c):
    c.key(0.4, la=(-40, -18, 0), lf=(-66, 0, 0), ra=(-40, -28, 0), rf=(-82, 0, 0), head=(2, 0, 0))
    # eyes on you, then down to the note, scribble, and back up
    c.key(0.9, head=(20, -6, 0))
    c.wobble(1.0, 1.9, 5, "rf", 6, base=(-84, 0, 0))
    c.key(2.2, head=(0, 0, 0), lid_pos=(0, -0.8, 0))
    c.key(2.7, head=(20, -6, 0), lid_pos=(0, 0, 0))
    c.wobble(2.8, 3.4, 5, "rf", 6, base=(-84, 0, 0))
    c.key(3.6, head=(2, 0, 0), ra=(-30, -14, 0), rf=(-50, 0, 0), la=(-26, -12, 0), lf=(-40, 0, 0))
    c.key(4.4)


@clip("chat_explain", "Explains along the rows", trigger="chat_speak", length=4.4, weight=3)
def _(c):
    # the right hand traces three rows of an invisible ledger, each lower than the last
    c.key(0.4, ra=(-72, -24, 0), rf=(-40, 0, 0), head=(-4, -8, 0), la=(-14, -10, 0), lf=(-30, 0, 0))
    for i, t in enumerate((0.5, 1.3, 2.1)):
        c.key(t, ra=(-72 + i * 9, -24, 0), rf=(-40, 0, 0), head=(-4 + i * 4, -8, 0))
        c.key(t + 0.6, ra=(-72 + i * 9, 30, 10), rf=(-36, 0, 0), head=(-4 + i * 4, 14, 0))
    # then turns the open hand to the listener
    c.key(3.2, ra=(-44, 20, 10), rf=(-40, 0, 0), head=(0, 0, 4), lid_pos=(0, -1.0, 0))
    c.key(3.6, ra=(-40, 18, 8), head=(2, 0, 3), lid_pos=(0, -0.6, 0))
    c.key(4.4)


@clip("chat_recount", "Recounts it with the lid bobbing", trigger="chat_speak", length=4.0, weight=3)
def _(c):
    c.key(0.4, waist=(5, 0, 0), cape=(-2, 0, 0), ra=(-40, -12, 0), rf=(-60, 0, 0), la=(-36, -12, 0),
          lf=(-56, 0, 0), head=(4, 0, 0))
    c.cycle(0.5, 1.9, 0.6, dict(ra=(-46, -12, 0), la=(-32, -12, 0), lid_pos=(0, -0.8, 0)),
            dict(ra=(-34, -12, 0), la=(-44, -12, 0), lid_pos=(0, 0, 0)))
    # "and then!": the lid flies up and the arms open wide
    c.key(2.2, ra=(-56, 40, 24), rf=(-30, 0, 0), la=(-56, 40, 24), lf=(-30, 0, 0), head=(-10, 0, 0),
          lid_pos=(0, -2.6, 0), lid=(-10, 0, 0), waist=(-3, 0, 0), cape=(2, 0, 0))
    c.key(2.45, ra=(-54, 38, 22), la=(-54, 38, 22), lid_pos=(0, -2.3, 0), head=(-8, 0, 0))
    c.key(3.1, ra=(-20, 6, 4), rf=(-20, 0, 0), la=(-20, 6, 4), lf=(-20, 0, 0), head=(2, 0, 0), lid_pos=(0, -0.3, 0),
          lid=(-1, 0, 0), waist=(0, 0, 0), cape=(0, 0, 0))
    c.key(4.0)


@clip("chat_nod_along", "Nods along slowly", trigger="chat_listen", length=3.8, weight=3)
def _(c):
    folded = dict(ra=(-20, -24, 0), rf=(-74, 0, 0), la=(-20, -24, 0), lf=(-74, 0, 0))
    c.key(0.5, head=(2, 0, 4), **folded)
    for t in (0.9, 1.9):
        c.key(t, head=(12, 0, 4), lid_pos=(0, 0.5, 0))
        c.key(t + 0.45, head=(1, 0, 4), lid_pos=(0, -0.4, 0))
    c.key(3.0, head=(2, 0, 2), lid_pos=(0, 0, 0), **folded)
    c.key(3.8)


@clip("chat_dry_chuckle", "A dry little chuckle", trigger="chat_listen", length=3.0, weight=2)
def _(c):
    # the lid chatters a few times, the shoulders shake once or twice; nothing more is permitted
    c.key(0.3, ra=(-58, -30, 0), rf=(-100, 0, 0), head=(6, 0, 6))
    c.wobble(0.35, 1.6, 6, "lid_pos", 0.9, base=(0, -0.9, 0), axis=1, decay=0.5)
    c.wobble(0.35, 1.6, 3, "ra_pos", 0.5, axis=1)
    c.wobble(0.35, 1.6, 3, "la_pos", 0.5, axis=1)
    c.wobble(0.35, 1.6, 3, "head", 3, base=(6, 0, 6), axis=0, decay=0.5)
    c.key(2.1, ra=(-20, -10, 0), rf=(-30, 0, 0), head=(2, 0, 2))
    c.key(3.0)
