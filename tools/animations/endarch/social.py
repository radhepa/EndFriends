"""Greeting a guest, dismissing one, holding court in conversation, and murmuring with another Endarch.

An Endarch never hurries and never bows low: a measured nod, a lifted palm, a hand to the breast. A guest must carry
Enderman Eyes, and a looming Endarch leans down to see that they do. Clips that raise the right forearm high avoid
the Riftguard (it would swing the glaive over its head); the Riftguard has its own salute.
"""
from kit import clip

CHEST = dict(ra=(-10, -40, 0), rf=(-135, 0, 0))          # the right hand laid on the breast
BEHIND = dict(ra=(30, 0, 4), rf=(-8, 0, -42), la=(30, 0, 4), lf=(-8, 0, -42))   # hands clasped behind
# on the way to BEHIND and back: arms swung back first, forearms folded in only after (never through the cape)
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


@clip("greet_measured_nod", "Measured nod", trigger="greet", length=2.8, weight=3, require=["adult"])
def _(c):
    # the chin lifts a touch, then one slow nod, and the chin comes back up higher than before
    c.key(0.45, head=(-5, 0, 0))
    c.key(1.15, head=(15, 0, 0), waist=(2, 0, 0), mantle=(-1, 0, 0))
    c.key(1.45, head=(14, 0, 0), waist=(2, 0, 0), mantle=(-1, 0, 0))
    c.key(2.05, head=(-7, 0, 0), waist=(-1, 0, 0), mantle=(1, 0, 0))
    c.key(2.8)


@clip("greet_palm", "Lifted palm", trigger="greet", length=3.2, weight=2, require=["adult"],
      avoid=["rank:riftguard"])
def _(c):
    # the right palm rises to the chin and turns out to the guest: you are seen
    c.key(0.3, ra=(-8, 0, 4), rf=(-20, 0, 0))
    c.key(0.9, ra=(-60, 0, 15), rf=(-70, 0, 0), head=(-6, 0, 0))
    c.key(1.05, ra=(-63, 0, 16), rf=(-67, 0, 0), head=(-7, 0, 0))
    c.key(1.9, ra=(-61, 0, 15), rf=(-69, 8, 0), head=(-6, 3, 0))
    c.key(2.5, ra=(-14, 0, 6), rf=(-20, 0, 0), head=(-2, 0, 0))
    c.key(3.2)


@clip("greet_court_bow", "Courtly half bow", trigger="greet", length=3.6, weight=2, require=["adult"],
      avoid=["rank:riftguard"])
def _(c):
    # the right hand to the breast and a shallow bow (an Endarch's deepest); then up, chin high
    c.key(0.7, **CHEST, la=(6, 0, 4), head=(4, 0, 0))
    c.key(1.3, **CHEST, la=(10, 0, 5), lf=(-6, 0, 0), waist=(6, 0, 0), mantle=(-5, 0, 0), cape=(-5, 0, 0),
          head=(18, 0, 0))
    c.key(1.8, **CHEST, la=(10, 0, 5), lf=(-6, 0, 0), waist=(6, 0, 0), mantle=(-5, 0, 0), cape=(-5, 0, 0),
          head=(17, 0, 0))
    c.key(2.5, ra=(-6, -10, 2), rf=(-30, 0, 0), la=(2, 0, 2), lf=(0, 0, 0), waist=(-2, 0, 0), mantle=(2, 0, 0),
          cape=(2, 0, 0), head=(-8, 0, 0))
    c.key(3.6)


@clip("greet_loom", "Loom over the guest", trigger="greet", length=4.0, weight=2, require=["adult"],
      boost={"manner:proud": 2}, mirror="never")
def _(c):
    # leaning down from its great height to look the guest over (do they carry the Eyes?), then up again
    c.key(0.45, **SWING)
    c.key(0.9, waist=(7, 0, 0), mantle=(-6, 0, 0), cape=(-6, 0, 0), head=(22, 0, 10), **BEHIND)
    c.key(1.6, waist=(7, 3, 0), head=(24, 8, -8))
    c.key(2.2, waist=(7, -2, 0), head=(23, -4, 12))
    c.key(2.5, waist=(7, 0, 0), mantle=(-6, 0, 0), cape=(-6, 0, 0), head=(22, 0, 6), **BEHIND)
    c.key(3.2, waist=(-3, 0, 0), mantle=(3, 0, 0), cape=(3, 0, 0), head=(-8, 0, 0), **SWING)
    c.key(4.0)
    glaive_behind(c, 0, 0.9, 2.5, 4.0)


@clip("greet_glaive_salute", "Glaive salute", trigger="greet", length=3.4, weight=4,
      require=["adult", "rank:riftguard"], mirror="never")
def _(c):
    # the glaive snaps upright before the face, a sharp nod over it, and it is lowered again
    up = dict(ra=(-25, -28, 0), rf=(-55, 0, 0))
    c.key(0.45, ra=(-12, -10, 0), rf=(-40, 0, 0), head=(-2, 0, 0))
    c.key(0.7, **up, head=(-6, 0, 0))
    c.key(0.82, ra=(-27, -29, 0), rf=(-56, 0, 0))
    c.key(1.3, **up, head=(10, 0, 0))
    c.key(1.6, **up, head=(-6, 0, 0))
    c.key(2.3, **up, head=(-5, 0, 0))
    c.key(2.8, ra=(-6, -4, 0), rf=(-12, 0, 0), head=(-2, 0, 0))
    c.key(3.4)


@clip("farewell_dismiss", "Dismissive flick", trigger="farewell", length=2.6, weight=3, require=["adult"],
      avoid=["rank:riftguard"])
def _(c):
    # the hand lifts and flicks the guest away with the back of the fingers; the head is already turning
    c.key(0.45, ra=(-35, 0, 0), rf=(-60, 0, 0), head=(2, 0, 0))
    c.key(0.62, ra=(-36, -6, 0), rf=(-66, 0, 0))
    c.key(0.82, ra=(-26, 28, 24), rf=(-16, 0, 0), head=(-8, -18, 0))
    c.key(0.95, ra=(-25, 32, 27), rf=(-12, 0, 0), head=(-9, -20, 0))
    c.key(1.6, ra=(-10, 12, 10), rf=(-8, 0, 0), head=(-8, -18, 0), waist=(0, -5, 0))
    c.key(2.6)


@clip("farewell_show_door", "Show the door", trigger="farewell", length=3.4, weight=3, require=["adult"],
      mirror="never")
def _(c):
    # the audience is over: the left arm sweeps out wide and level toward the way out, palm open, the head turning
    # with it; then the chin comes back up and the arm is held there a moment longer than is polite. (The left
    # arm, so a Riftguard's glaive stays where it is.)
    c.key(0.5, la=(-28, -12, 6), lf=(-55, 0, 0), head=(2, 0, 0))
    c.key(1.1, la=(-12, 24, 66), lf=(-8, 0, 0), head=(-4, -26, 0), waist=(0, -5, 0))
    c.key(1.3, la=(-11, 26, 68), lf=(-6, 0, 0), head=(-5, -28, 0))
    c.key(1.9, la=(-12, 24, 66), lf=(-8, 0, 0), head=(-10, -5, 0), waist=(0, -2, 0))
    c.key(2.5, la=(-12, 22, 64), lf=(-10, 0, 0), head=(-9, -3, 0))
    c.key(3.4)


@clip("farewell_brow_touch", "Fingertips to the brow", trigger="farewell", length=3.0, weight=2, require=["adult"],
      avoid=["rank:riftguard"])
def _(c):
    # a courtly leave-taking: the long fingertips touch the brow as the head inclines to meet them, then the hand
    # is carried out and down to the side: you may withdraw
    c.key(0.45, ra=(-40, -6, 10), rf=(-90, -4, 0), head=(2, 0, 0))
    c.key(0.85, ra=(-73, -4, 18), rf=(-134, -5, 0), head=(8, 0, 0))
    c.key(1.25, ra=(-72, -4, 18), rf=(-136, -5, 0), head=(10, 0, 0))
    c.key(1.8, ra=(-45, 18, 42), rf=(-28, 0, 0), head=(-6, 0, 0))
    c.key(2.1, ra=(-42, 20, 44), rf=(-24, 0, 0), head=(-7, 0, 0))
    c.key(3.0)


GLAIVE_UP = dict(ra=(-8, 0, 0), rf=(-72, 0, 0))       # a Riftguard's glaive held upright at its side


@clip("farewell_to_post", "Back to the post", trigger="farewell", length=3.0, weight=3,
      require=["adult", "rank:riftguard"], mirror="never")
def _(c):
    # the glaive snaps upright, one curt nod, and the Riftguard turns its eyes back to its watch
    c.key(0.4, ra=(-4, 0, 0), rf=(-50, 0, 0))
    c.key(0.6, **GLAIVE_UP, head=(-6, 0, 0))
    c.key(1.0, **GLAIVE_UP, head=(12, 0, 0))
    c.key(1.35, **GLAIVE_UP, head=(-6, 0, 0))
    c.key(1.9, **GLAIVE_UP, head=(-6, 30, 0), root=(0, 12, 0))
    c.key(2.4, **GLAIVE_UP, head=(-5, 28, 0), root=(0, 12, 0))
    c.key(3.0)


@clip("talk_open_palm", "Open palm", trigger="talk", length=3.2, weight=3, require=["adult"],
      avoid=["rank:riftguard"])
def _(c):
    # explaining, unhurried: the right hand opens out palm up toward the listener and settles back
    c.key(0.5, ra=(-20, 0, 5), rf=(-40, 0, 0), head=(2, 0, 0))
    c.key(1.1, ra=(-45, 15, 25), rf=(-35, 0, 0), head=(-4, 6, -4))
    c.key(1.3, ra=(-47, 17, 27), rf=(-32, 0, 0))
    c.key(2.1, ra=(-42, 12, 22), rf=(-38, 0, 0), head=(-3, 4, -3))
    c.key(2.6, ra=(-14, 0, 4), rf=(-22, 0, 0), head=(0, 0, 0))
    c.key(3.2)


@clip("talk_finger_raise", "Raised finger", trigger="talk", length=3.0, weight=2, require=["adult"],
      avoid=["rank:riftguard"])
def _(c):
    # one long finger raised beside the face, then three measured taps on the air to mark each point
    up = dict(ra=(-35, 0, 15), rf=(-100, 0, 0))
    c.key(0.5, **up, head=(-6, 0, 0))
    c.key(0.75, ra=(-36, 0, 15), rf=(-104, 0, 0))
    for t in (1.1, 1.6, 2.1):
        c.key(t, ra=(-38, 0, 15), rf=(-80, 0, 0), head=(6, 0, 0))
        c.key(t + 0.22, **up, head=(-2, 0, 0))
    c.key(3.0)


@clip("talk_both_hands", "Measured hands", trigger="talk", length=3.6, weight=3, require=["adult"],
      avoid=["rank:riftguard"], mirror="never")
def _(c):
    # both hands come up before the body, palms out, and part slowly as the point is laid out
    c.key(0.7, ra=(-30, 0, 10), rf=(-55, 0, 0), la=(-30, 0, 10), lf=(-55, 0, 0), head=(-3, 0, 0))
    c.key(1.4, ra=(-32, 10, 20), rf=(-50, 0, 0), la=(-34, 14, 24), lf=(-46, 0, 0), head=(-5, -4, 0))
    c.key(2.2, ra=(-30, 14, 24), rf=(-48, 0, 0), la=(-30, 18, 28), lf=(-44, 0, 0), head=(2, 3, 0))
    c.key(2.9, ra=(-12, 0, 6), rf=(-24, 0, 0), la=(-12, 0, 6), lf=(-24, 0, 0), head=(0, 0, 0))
    c.key(3.6)


@clip("talk_hand_on_chest", "We of the Court", trigger="talk", length=3.8, weight=2, require=["adult"],
      avoid=["rank:riftguard"])
def _(c):
    # the hand to the breast (we, the Court) and then out, palm up, to the listener (and you)
    c.key(0.6, **CHEST, head=(-6, 0, 0), waist=(-2, 0, 0), mantle=(2, 0, 0), cape=(2, 0, 0))
    c.key(1.4, **CHEST, head=(-8, 0, 0), waist=(-2, 0, 0), mantle=(2, 0, 0), cape=(2, 0, 0))
    c.key(2.0, ra=(-50, 10, 20), rf=(-30, 0, 0), head=(4, 4, 0), waist=(2, 0, 0), mantle=(-2, 0, 0),
          cape=(-2, 0, 0))
    c.key(2.2, ra=(-52, 12, 22), rf=(-27, 0, 0))
    c.key(2.9, ra=(-46, 8, 18), rf=(-32, 0, 0), head=(2, 3, 0))
    c.key(3.8)


@clip("talk_chin_high", "Chin high flourish", trigger="talk", length=3.4, weight=2, require=["adult"],
      mirror="never", boost={"manner:proud": 2})
def _(c):
    # speaking down the nose, the head turned a little away; the left hand turns a lazy flourish
    c.key(0.6, head=(-10, -10, 3), la=(-40, 0, 20), lf=(-50, 0, 0))
    c.key(1.2, la=(-42, 0, 22), lf=(-52, 32, 0), head=(-11, -12, 4))
    c.key(1.8, la=(-44, 0, 24), lf=(-48, -22, 0), head=(-10, -9, 2))
    c.key(2.3, la=(-40, 0, 20), lf=(-50, 10, 0), head=(-9, -10, 3))
    c.key(3.4)


@clip("talk_lean_in", "Lean in and warn", trigger="talk", length=3.6, weight=2, require=["adult"],
      mirror="never")
def _(c):
    # a cold warning: the tall body leans down over the listener, a long finger wagging slowly
    c.key(0.8, waist=(6, 0, 0), mantle=(-5, 0, 0), cape=(-5, 0, 0), head=(14, 0, -6), la=(-30, 0, 10),
          lf=(-95, 0, 0))
    c.wobble(1.0, 2.6, 1.6, "lf", 14, base=(-95, 0, 0), axis=1)
    c.key(2.8, waist=(6, 0, 0), mantle=(-5, 0, 0), cape=(-5, 0, 0), head=(12, 0, -4), la=(-28, 0, 10))
    c.key(3.6)


@clip("talk_glaive_upright", "Speaks over the glaive", trigger="talk", length=3.4, weight=4,
      require=["adult", "rank:riftguard"], mirror="never")
def _(c):
    # the glaive stood upright at the side, the free hand opens and closes as the Riftguard reports
    c.key(0.6, **GLAIVE_UP, la=(-35, 0, 20), lf=(-40, 0, 0), head=(-4, 0, 0))
    c.key(1.3, **GLAIVE_UP, la=(-38, 6, 26), lf=(-30, 0, 0), head=(4, -4, 0))
    c.key(2.0, **GLAIVE_UP, la=(-30, 0, 16), lf=(-50, 0, 0), head=(-2, 2, 0))
    c.key(2.7, **GLAIVE_UP, la=(-8, 0, 4), lf=(-14, 0, 0), head=(0, 0, 0))
    c.key(3.4)


FOLD_L = dict(la=(-12, 0, 8), lf=(-95, -72, 0))       # the left forearm folded across the waist


@clip("listen_head_tilt", "Cool head tilt", trigger="listen", length=4.2, weight=3, require=["adult"],
      mirror="never")
def _(c):
    # hands behind, the head tilts a few degrees, weighing every word; one small nod to go on
    c.key(0.5, **SWING)
    c.key(1.0, **BEHIND, head=(4, 0, 9), waist=(2, 0, 0), mantle=(-1, 0, 0), cape=(-1, 0, 0))
    c.key(2.6, **BEHIND, head=(5, 3, 11), waist=(2, 0, 0), mantle=(-1, 0, 0), cape=(-1, 0, 0))
    c.key(3.0, head=(11, 2, 8))
    c.key(3.3, head=(4, 2, 8))
    c.key(3.7, **SWING)
    c.key(4.2)
    glaive_behind(c, 0, 1.0, 2.6, 4.2)


@clip("listen_chin_hand", "Hand to the chin", trigger="listen", length=4.6, weight=2, require=["adult"],
      avoid=["rank:riftguard"])
def _(c):
    # the left arm folds across the waist to prop the right elbow; the chin rests on the knuckles; a slow nod
    chin = dict(ra=(-30, 0, 15), rf=(-150, -25, 0))
    c.key(0.9, **chin, **FOLD_L, head=(6, 0, -3))
    c.key(2.6, **chin, **FOLD_L, head=(7, 3, -5))
    c.key(3.1, head=(14, 3, -4))
    c.key(3.5, **chin, **FOLD_L, head=(5, 2, -4))
    c.key(4.6)


@clip("listen_skeptical", "Skeptical regard", trigger="listen", length=4.0, weight=2, require=["adult"],
      mirror="never", boost={"manner:proud": 2})
def _(c):
    # looking down the nose from the side, one arm folded: unconvinced, and letting it show
    c.key(0.8, **FOLD_L, head=(-8, 14, -6), waist=(-2, 4, 0), mantle=(2, 0, 0), cape=(2, 0, 0))
    c.key(2.0, **FOLD_L, head=(-9, 16, -8), waist=(-2, 4, 0))
    c.key(2.6, head=(-6, 10, 2))
    c.key(3.1, **FOLD_L, head=(-8, 13, -5), waist=(-2, 4, 0), mantle=(2, 0, 0), cape=(2, 0, 0))
    c.key(4.0)


@clip("chat_speak_aside", "A remark aside", trigger="chat_speak", length=3.4, weight=3, require=["adult"],
      mirror="never")
def _(c):
    # to the other Endarch: the head tips toward someone off to the side and the left hand flicks at them
    c.key(0.6, head=(4, -10, 6), la=(-25, 0, 8), lf=(-50, 0, 0))
    c.key(1.2, head=(2, -32, 4), waist=(0, -6, 0), la=(-30, -10, 20), lf=(-30, 0, 0))
    c.key(1.35, la=(-31, -14, 24), lf=(-24, 0, 0))
    c.key(2.0, head=(6, 2, 6), waist=(2, 0, 0), la=(-20, 0, 8), lf=(-40, 0, 0), mantle=(-1, 0, 0), cape=(-1, 0, 0))
    c.key(2.4, head=(10, 2, 4))
    c.key(3.4)


@clip("chat_speak_point", "Point into the distance", trigger="chat_speak", length=3.6, weight=2,
      require=["adult"], avoid=["rank:riftguard"])
def _(c):
    # the long arm lifts and points far off; the head follows it, then turns back to see it understood
    c.key(0.5, ra=(-20, 0, 4), rf=(-35, 0, 0), head=(-2, 6, 0))
    c.key(1.1, ra=(-85, 25, 10), rf=(-5, 0, 0), head=(-5, 26, 0), waist=(0, 6, 0))
    c.key(1.25, ra=(-88, 26, 10), rf=(-3, 0, 0))
    c.key(2.2, ra=(-84, 24, 10), rf=(-6, 0, 0), head=(-3, 4, 0), waist=(0, 4, 0))
    c.key(2.8, ra=(-12, 4, 4), rf=(-14, 0, 0), head=(0, 0, 0), waist=(0, 0, 0))
    c.key(3.6)


@clip("chat_listen_temple", "Fingers to the temple", trigger="chat_listen", length=4.0, weight=3,
      require=["adult"], mirror="never")
def _(c):
    # two long fingers come up to the temple and the head leans into them, weighing what the other says; one
    # slow, small nod. (The left hand, so a Riftguard's glaive stays where it is.)
    temple = dict(la=(-62, 33, 42), lf=(-154, 27, 0))     # fingertips just off the temple (a Riftguard's head too)
    c.key(0.5, la=(-34, 12, 22), lf=(-80, 10, 0), head=(1, -2, 4))
    c.key(1.0, **temple, head=(2, -4, 10))
    c.key(2.3, la=(-62, 33, 42), lf=(-155, 28, 0), head=(3, -6, 11))
    c.key(2.7, la=(-60, 32, 42), lf=(-154, 26, 0), head=(7, -5, 10))
    c.key(3.1, **temple, head=(2, -4, 10))
    c.key(3.6, la=(-30, 10, 18), lf=(-70, 8, 0), head=(0, -1, 3))
    c.key(4.0)


@clip("chat_listen_glance", "Glance away", trigger="chat_listen", length=3.2, weight=2, require=["adult"],
      mirror="free")
def _(c):
    # the eyes drift off to something more interesting, come back, and a small shake: not impressed
    c.key(0.8, head=(-3, -30, 0))
    c.key(1.4, head=(-3, -28, 2))
    c.key(1.8, head=(0, 0, 0))
    c.key(2.0, head=(0, 7, 0))
    c.key(2.2, head=(0, -6, 0))
    c.key(2.4, head=(0, 4, 0))
    c.key(3.2)


@clip("chat_speak_blade_point", "Point the way with the blade", trigger="chat_speak", length=3.8, weight=3,
      require=["adult", "rank:riftguard"], mirror="never")
def _(c):
    # to a fellow guard: the glaive comes up level and its blade points off across the hall, the head following
    # it; then the blade is lowered and the head turns back to the fellow with one curt nod
    point = dict(ra=(-55, 35, 20), rf=(-20, 0, 0), glaive=(92, 33, 0))
    c.key(0.5, ra=(-25, 10, 8), rf=(-30, 0, 0), glaive=(40, 10, 0), head=(-2, 6, 0))
    c.key(1.1, **point, head=(-4, 30, 0), waist=(0, 6, 0))
    c.key(1.3, ra=(-57, 36, 20), rf=(-18, 0, 0), glaive=(93, 33, 0))
    c.key(2.2, **point, head=(-3, 28, 0), waist=(0, 6, 0))
    c.key(2.7, ra=(-25, 10, 8), rf=(-30, 0, 0), glaive=(40, 10, 0), head=(8, 0, 0), waist=(0, 0, 0))
    c.key(3.0, head=(-2, 0, 0))
    c.key(3.8)
