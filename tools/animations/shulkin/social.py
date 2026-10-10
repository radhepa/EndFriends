"""Meeting and parting: Shulkin greet with the lid (their hat and their face at once) and measured bows."""
from kit import clip


@clip("greet_lid_tip", "Tips the lid in greeting", trigger="greet", length=2.8, weight=3)
def _(c):
    c.key(0.25, head=(5, 0, 0), ra=(-20, -10, 0), rf=(-30, 0, 0))
    # a hand to the brim, the lid lifts and tips forward like a hat, a small bow under it
    # (fingers on the front edge of the lid, not through it)
    c.key(0.7, ra=(-104, -18, 0), rf=(-70, 0, 0), head=(12, 0, 0), lid_pos=(0, -2.4, 0), lid=(10, 0, 0))
    c.key(0.9, ra=(-106, -18, 0), head=(14, 0, 0), lid_pos=(0, -2.6, 0), lid=(12, 0, 0))
    c.key(1.4, head=(12, 0, 0), lid_pos=(0, -2.4, 0), lid=(11, 0, 0))
    c.key(1.75, ra=(-50, -12, 0), rf=(-40, 0, 0), head=(-4, 0, 0), lid_pos=(0, -0.6, 0), lid=(-3, 0, 0))
    c.key(2.0, head=(0, 0, 0), lid_pos=(0, -0.2, 0), lid=(0, 0, 0))
    c.key(2.8)


@clip("greet_hand_heart", "Hand to the breast and a measured bow", trigger="greet", length=3.0, weight=3,
      require=["adult"])
def _(c):
    c.key(0.4, ra=(-24, -40, 0), rf=(-88, 0, 0), head=(2, 0, 0))
    c.key(0.95, waist=(12, 0, 0), cape=(-6, 0, 0), head=(10, 0, 0), lid_pos=(0, 1.0, 0), la=(6, 0, 4))
    c.key(1.25, waist=(13, 0, 0), cape=(-7, 0, 0), head=(11, 0, 0))
    c.key(1.8, waist=(-2, 0, 0), cape=(1, 0, 0), head=(-4, 0, 0), lid_pos=(0, -1.3, 0), lid=(-5, 0, 0), la=(0, 0, 0))
    c.key(2.1, waist=(0, 0, 0), cape=(0, 0, 0), head=(0, 0, 0), lid_pos=(0, -0.6, 0), lid=(-2, 0, 0))
    c.key(2.3, ra=(-20, -30, 0), rf=(-60, 0, 0))
    c.key(3.0)


@clip("greet_small_wave", "A small precise wave", trigger="greet", length=2.6, weight=2)
def _(c):
    c.key(0.4, ra=(-56, 38, 30), rf=(-96, 0, 0), head=(0, 0, 8), lid_pos=(0, -1.0, 0), lid=(-4, 0, 0))
    c.wobble(0.5, 1.7, 3, "ra", 8, base=(-56, 38, 30), axis=2, decay=0.3)
    c.key(1.9, ra=(-40, 24, 16), rf=(-76, 0, 0), head=(0, 0, 4), lid_pos=(0, -0.6, 0))
    c.key(2.6)


@clip("greet_shy_peek", "Peeks out and gives a tiny wave", trigger="greet", length=3.2, weight=0.5,
      boost={"manner:shy": 6})
def _(c):
    c.key(0.3, lid_pos=(0, 2.8, 0), head=(12, -10, 0), ra_pos=(0, -0.6, 0), la_pos=(0, -0.6, 0))
    c.key(0.9, lid_pos=(0, 2.9, 0), head=(12, -12, 0))
    # the lid opens a crack; a little flutter of the fingers at chest height
    c.key(1.3, lid_pos=(0, 1.2, 0), head=(8, -4, 4), ra=(-34, -18, 0), rf=(-96, 0, 0))
    c.wobble(1.4, 2.3, 4, "rf", 8, base=(-96, 0, 0))
    c.key(2.5, lid_pos=(0, 1.6, 0), head=(10, -6, 2), ra=(-20, -10, 0), rf=(-50, 0, 0))
    c.key(2.7, ra_pos=(0, 0, 0), la_pos=(0, 0, 0))
    c.key(3.2)


@clip("greet_proud_nod", "One slow nod from on high", trigger="greet", length=2.8, weight=0.5,
      require=["adult"], boost={"manner:proud": 6})
def _(c):
    c.key(0.4, waist=(-4, 0, 0), head=(-12, 0, 0), lid_pos=(0, -1.6, 0), lid=(-6, 0, 0), ra=(-14, -24, 0),
          rf=(-60, 0, 0), la=(-14, -24, 0), lf=(-60, 0, 0))
    c.key(0.8, head=(-12, 0, 0))
    c.key(1.3, head=(10, 0, 0), lid_pos=(0, -0.6, 0), lid=(2, 0, 0))
    c.key(1.8, head=(-10, 0, 0), lid_pos=(0, -1.4, 0), lid=(-5, 0, 0))
    c.key(2.2, waist=(-2, 0, 0), head=(-4, 0, 0))
    c.key(2.8)


@clip("farewell_bow_close", "Bows and lowers the lid", trigger="farewell", length=3.0, weight=3,
      require=["adult"])
def _(c):
    joined = dict(ra=(-40, -42, 0), rf=(-94, 0, 0), la=(-40, -42, 0), lf=(-94, 0, 0))
    c.key(0.45, head=(4, 0, 0), **joined)
    c.key(1.0, waist=(10, 0, 0), cape=(-5, 0, 0), head=(12, 0, 0), lid_pos=(0, 2.2, 0))
    c.key(1.6, waist=(11, 0, 0), cape=(-6, 0, 0), head=(13, 0, 0), lid_pos=(0, 2.4, 0), **joined)
    c.key(2.2, waist=(0, 0, 0), cape=(0, 0, 0), head=(2, 0, 0), lid_pos=(0, 0.6, 0))
    c.key(3.0)


@clip("farewell_wave_turn", "Raises a hand and turns to go", trigger="farewell", length=3.0, weight=2)
def _(c):
    c.key(0.4, ra=(-116, 34, 24), rf=(-40, 0, 0), head=(0, 0, 4), lid_pos=(0, -1.0, 0))
    c.key(0.7, ra=(-120, 38, 30))
    c.key(1.0, ra=(-116, 30, 20))
    # turns away while the head stays a beat longer on you
    c.key(1.5, root=(0, 24, 0), head=(0, -18, 0), ra=(-60, 6, 4), rf=(-30, 0, 0), lid_pos=(0, -0.4, 0),
          cape=(4, 0, -3))
    c.key(2.0, root=(0, 28, 0), head=(0, -6, 0), ra=(-10, 0, 0), rf=(-10, 0, 0), cape=(1, 0, -1))
    c.key(3.0)


@clip("farewell_noted", "Taps the shell: you are noted", trigger="farewell", length=2.6, weight=2,
      require=["adult"])
def _(c):
    # a fingertip taps the side of the shell twice (I shall remember this), then a curt nod; the elbow goes out
    # wide so the hand comes to the lid from the side
    c.key(0.45, ra=(-120, 60, 0), rf=(-86, 0, 0), head=(0, 0, 8))
    c.key(0.65, rf=(-98, 0, 0), lid_pos=(0, -0.6, 0))
    c.key(0.8, rf=(-86, 0, 0), lid_pos=(0, 0, 0))
    c.key(0.95, rf=(-98, 0, 0), lid_pos=(0, -0.6, 0))
    c.key(1.1, rf=(-86, 0, 0), lid_pos=(0, 0, 0))
    c.key(1.5, ra=(-40, -8, 0), rf=(-30, 0, 0), head=(12, 0, 0))
    c.key(1.8, head=(-2, 0, 0))
    c.key(2.6)
