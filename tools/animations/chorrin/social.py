from kit import clip
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _motion import sampled, env, sn  # noqa: E402

# Meeting, talking and parting. A Chorrin has no mouth, so the hum carries the words and the crown and long arms
# carry the meaning: the crown dips to greet, sways while they hum, and droops or perks with the mood.


# -- greet ------------------------------------------------------------------------------------------------------

@clip("greet_wave", "Slow long-armed wave", trigger="greet", length=2.8, weight=3, require=["adult"])
def _(c):
    c.key(0.35, ra=(-60, 10, 60), rf=(-30, 0, 0), head=(6, 0, 0), crown=(4, 0, 0))
    c.key(0.65, ra=(-14, 0, 146), rf=(-14, 0, 0), head=(-6, 0, 6), crown=(-4, 0, 5), waist=(-2, 0, -2))

    def wave(t):
        e = env(t, 0.65, 2.0, 0.25)
        return dict(ra=(-14, 0, 146 + 18 * sn(t - 0.65, 0.68) * e), crown=(-4, 0, 5 - 8 * sn(t - 0.65, 0.68, -0.1) * e))
    sampled(c, 0.65, 2.0, wave, step=0.085)
    c.key(2.3, ra=(-10, 0, 14), rf=(-8, 0, 0), head=(4, 0, 0), crown=(3, 0, 0), waist=(0, 0, 0))
    c.key(2.8)


@clip("greet_crown_dip", "Dips the crown in greeting", trigger="greet", length=2.6, weight=3)
def _(c):
    # the Chorrin greeting: a hand to the heart and the crown dipped toward you, so you can see it bloom
    c.key(0.4, ra=(-44, -34, 8), rf=(-79, 0, 0), head=(-4, 0, 0), crown=(-4, 0, 0))
    c.key(0.85, head=(30, 0, 0), waist=(9, 0, 0), crown=(12, 0, 0), root_pos=(0, 0.3, 0))
    c.key(1.35, head=(32, 0, 0), waist=(10, 0, 0), crown=(16, 0, 0))
    c.key(1.75, head=(-6, 0, 0), waist=(-2, 0, 0), crown=(-8, 0, 0), root_pos=(0, 0, 0), ra=(-20, -10, 0),
          rf=(-24, 0, 0))
    c.key(2.1, head=(2, 0, 0), crown=(3, 0, 0), waist=(0, 0, 0), ra=(0, 0, 0), rf=(0, 0, 0))
    c.key(2.6)


@clip("greet_palm", "Raises an open palm and hums", trigger="greet", length=3.0, weight=2, require=["adult"])
def _(c):
    c.key(0.45, ra=(-38, 20, 12), rf=(-104, 0, 0), head=(4, 0, -4), crown=(2, 0, -4))
    c.key(0.7, ra=(-40, 22, 14), rf=(-110, 0, 0), head=(-2, 0, -8))

    def hum(t):
        e = env(t, 0.7, 2.3, 0.3)
        return dict(crown=(2, 0, -4 + 10 * sn(t - 0.7, 0.8) * e), head=(-2, 0, -8 + 4 * sn(t - 0.7, 0.8, -0.1) * e))
    sampled(c, 0.7, 2.3, hum, step=0.1)
    c.key(2.6, ra=(-6, 0, 3), rf=(-10, 0, 0), head=(0, 0, 0), crown=(0, 0, 0))
    c.key(3.0)


@clip("greet_sprout_bounce", "Bouncy sprout wave", trigger="greet", length=2.4, weight=3, require=["child"],
      mirror="free")
def _(c):
    c.key(0.3, ra=(-10, 0, 140), la=(-10, 0, 60), root_pos=(0, 0.6, 0), head=(-6, 0, 0), crown=(-6, 0, 0))
    for i, t in enumerate((0.55, 1.05, 1.55)):
        c.key(t, ra=(-10, 0, 160), la=(-10, 0, 80), root_pos=(0, -2.2, 0), head=(-10, 0, 8 if i % 2 else -8),
              crown=(-12, 0, 0))
        c.key(t + 0.25, ra=(-10, 0, 128), la=(-10, 0, 54), root_pos=(0, 0.5, 0), head=(-4, 0, 0), crown=(10, 0, 0))
    c.key(2.05, ra=(0, 0, 10), la=(0, 0, 8), root_pos=(0, 0, 0), head=(0, 0, 0), crown=(-3, 0, 0))
    c.key(2.4)


@clip("greet_shy", "Shy little wave", trigger="greet", length=2.8, weight=1, boost={"manner:shy": 5})
def _(c):
    # hand barely above the waist, fingers waggling, a peek up, the head ducks again
    c.key(0.5, ra=(-18, 6, 8), rf=(-70, 0, 0), head=(18, -10, 6), crown=(8, 0, 4), waist=(3, 0, 0))
    c.wobble(0.6, 1.6, 3, "rf", 12, base=(-70, 0, 0))
    c.wobble(0.6, 1.6, 3, "ra", 6, base=(-18, 6, 8), axis=2)
    c.key(1.2, head=(4, -4, 4), crown=(0, 0, 2))
    c.key(1.6, head=(20, -14, 8), crown=(10, 0, 6))
    c.key(2.2, ra=(-6, 0, 2), rf=(-8, 0, 0), head=(6, 0, 0), crown=(2, 0, 0), waist=(0, 0, 0))
    c.key(2.8)


# -- farewell ---------------------------------------------------------------------------------------------------

@clip("farewell_waggle", "Waggles goodbye", trigger="farewell", length=2.6, weight=3)
def _(c):
    c.key(0.4, ra=(-96, 26, 14), rf=(-40, 0, 0), head=(6, 0, -6), crown=(4, 0, -4))
    c.wobble(0.45, 1.75, 2.4, "rf", 26, base=(-40, 0, 0))
    c.wobble(0.45, 1.75, 2.4, "ra", 8, base=(-96, 26, 14), axis=2)
    c.key(1.75, head=(10, 0, 0), crown=(8, 0, 0))
    c.key(2.15, ra=(-4, 0, 2), rf=(-6, 0, 0), head=(0, 0, 0), crown=(-2, 0, 0))
    c.key(2.6)


@clip("farewell_crown_bless", "Touches the crown and sends you off", trigger="farewell", length=3.2, weight=2,
      require=["adult"])
def _(c):
    # a bit of the grove for the road: fingers to the crown, then the open hand held out toward you
    c.key(0.5, ra=(-135, 0, 0), rf=(-42, 0, 0), head=(9, 0, -12), crown=(0, 0, -8))
    c.key(0.8, ra=(-132, 0, 2), rf=(-48, 0, 0), crown=(0, 0, 4))
    c.key(1.3, ra=(-78, 14, 0), rf=(-14, 0, 0), head=(6, 0, 0), crown=(-4, 0, 0))
    c.key(1.8, ra=(-80, 16, 0), rf=(-12, 0, 0), head=(14, 0, 0), crown=(8, 0, 0))
    c.key(2.3, ra=(-8, 0, 2), rf=(-8, 0, 0), head=(2, 0, 0), crown=(0, 0, 0), root=(0, 10, 0))
    c.key(2.8, root=(0, 4, 0))
    c.key(3.2)


@clip("farewell_sprout_hop", "Hops and waves goodbye", trigger="farewell", length=2.2, weight=3, require=["child"],
      mirror="free")
def _(c):
    c.key(0.25, root_pos=(0, 0.6, 0), ra=(-10, 0, 40), head=(4, 0, 0))
    c.key(0.5, root_pos=(0, -2.6, 0), ra=(-10, 0, 150), la=(-10, 0, 30), head=(-8, 0, 0), crown=(-12, 0, 0))
    c.key(0.75, root_pos=(0, 0.4, 0), ra=(-10, 0, 120), la=(0, 0, 10), crown=(10, 0, 0))
    c.key(1.0, root_pos=(0, 0, 0), ra=(-10, 0, 160), head=(-4, 0, 8), crown=(-4, 0, 6))
    c.key(1.3, ra=(-10, 0, 124), head=(-4, 0, -8), crown=(2, 0, -6))
    c.key(1.6, ra=(-10, 0, 150), head=(-2, 0, 4))
    c.key(1.95, ra=(0, 0, 8), la=(0, 0, 0), head=(0, 0, 0), crown=(0, 0, 0))
    c.key(2.2)


# -- talk: gestures while their line types out ------------------------------------------------------------------

@clip("talk_open_palms", "Open palms", trigger="talk", length=3.4, weight=3, mirror="free")
def _(c):
    c.key(0.4, ra=(-48, 18, 6), rf=(-40, 0, 0), la=(-36, 14, 4), lf=(-30, 0, 0), head=(4, 0, 0), crown=(2, 0, 0))
    # each phrase lands on one hand, then the other; the head nods along and the crown sways with the hum
    c.key(0.8, ra=(-58, 24, 10), rf=(-48, 0, 0), head=(9, 4, 0), crown=(8, 0, -3))
    c.key(1.15, ra=(-44, 16, 6), rf=(-36, 0, 0), head=(2, 0, 0), crown=(0, 0, 2))
    c.key(1.6, la=(-56, 24, 10), lf=(-46, 0, 0), head=(8, -5, 0), crown=(7, 0, 4))
    c.key(1.95, la=(-36, 14, 4), lf=(-30, 0, 0), head=(2, 0, 0), crown=(0, 0, -2))
    c.key(2.45, ra=(-60, 26, 12), rf=(-46, 0, 0), la=(-58, 26, 12), lf=(-44, 0, 0), head=(10, 0, 0),
          crown=(9, 0, 0))
    c.key(2.9, ra=(-6, 0, 2), rf=(-8, 0, 0), la=(-6, 0, 2), lf=(-8, 0, 0), head=(0, 0, 0), crown=(-2, 0, 0))
    c.key(3.4)


@clip("talk_point_down", "Here in the grove", trigger="talk", length=3.2, weight=2, require=["adult"])
def _(c):
    # a long finger to the stone underfoot, tap, tap; then the open hand turned up to you
    c.key(0.4, ra=(-34, -6, 0), rf=(-10, 0, 0), waist=(6, 0, 0), head=(14, 0, 0))
    c.key(0.6, ra=(-26, -6, 0), rf=(-4, 0, 0), head=(18, 0, 0), crown=(6, 0, 0))
    c.key(0.8, ra=(-34, -6, 0), rf=(-12, 0, 0), crown=(0, 0, 0))
    c.key(1.0, ra=(-26, -6, 0), rf=(-4, 0, 0), head=(18, 0, 0), crown=(6, 0, 0))
    c.key(1.5, ra=(-60, 20, 8), rf=(-42, 0, 0), waist=(0, 0, 0), head=(2, 0, -6), crown=(-2, 0, -4))
    c.key(2.2, ra=(-62, 22, 10), rf=(-46, 0, 0), head=(6, 0, -8), crown=(2, 0, -6))
    c.key(2.7, ra=(-6, 0, 2), rf=(-8, 0, 0), head=(0, 0, 0), crown=(0, 0, 0))
    c.key(3.2)


@clip("talk_sweep", "Out past the islands", trigger="talk", length=3.6, weight=2, require=["adult"])
def _(c):
    # the whole horizon in one slow sweep of a long arm; the eyes follow it out there
    c.key(0.5, ra=(-84, -26, 0), rf=(-24, 0, 0), head=(-2, -16, 0), waist=(0, -8, 0), crown=(0, 0, 4))
    c.key(1.7, ra=(-92, 52, 0), rf=(-8, 0, 0), head=(-8, 28, 0), waist=(-2, 12, 0), crown=(4, 0, -6))
    c.key(2.2, ra=(-94, 58, 0), head=(-10, 32, 0), crown=(6, 0, -3))
    c.key(2.7, ra=(-30, 10, 4), rf=(-20, 0, 0), head=(4, 6, 0), waist=(0, 2, 0), crown=(-3, 0, 2))
    c.key(3.1, ra=(0, 0, 0), rf=(0, 0, 0), head=(0, 0, 0), waist=(0, 0, 0), crown=(0, 0, 0))
    c.key(3.6)


@clip("talk_fist_palm", "Fist into palm", trigger="talk", length=3.0, weight=2, require=["adult"])
def _(c):
    palm = dict(la=(-46, -24, 0), lf=(-66, 0, 0))
    c.key(0.4, ra=(-70, -18, 0), rf=(-84, 0, 0), head=(-2, 0, 0), **palm)
    for t in (0.65, 1.35):
        c.key(t, ra=(-82, -16, 0), rf=(-96, 0, 0), head=(-4, 0, 0), crown=(-4, 0, 0))
        c.key(t + 0.17, ra=(-46, -26, 0), rf=(-70, 0, 0), head=(10, 0, 0), crown=(10, 0, 0), waist=(4, 0, 0),
              root_pos=(0, 0.3, 0))
        c.key(t + 0.4, ra=(-52, -24, 0), rf=(-74, 0, 0), head=(4, 0, 0), crown=(0, 0, 0), waist=(2, 0, 0),
              root_pos=(0, 0, 0))
    c.key(2.5, ra=(-6, 0, 2), rf=(-8, 0, 0), la=(-4, 0, 2), lf=(-6, 0, 0), head=(0, 0, 0), waist=(0, 0, 0),
          crown=(0, 0, 0))
    c.key(3.0)


@clip("talk_shrug", "Big shrug", trigger="talk", length=2.6, weight=2, mirror="free")
def _(c):
    c.key(0.45, ra=(-30, 30, 22), rf=(-50, 0, 0), la=(-30, 30, 22), lf=(-50, 0, 0), head=(-2, 0, 12),
          crown=(-4, 0, 14), root_pos=(0, -0.6, 0), waist=(-2, 0, 0))
    c.key(1.2, ra=(-32, 32, 24), la=(-32, 32, 24), head=(0, 0, 14), crown=(-2, 0, 16), root_pos=(0, -0.7, 0))
    c.key(1.6, ra=(4, 0, 4), rf=(-6, 0, 0), la=(4, 0, 4), lf=(-6, 0, 0), head=(6, 0, 0), crown=(6, 0, -4),
          root_pos=(0, 0.3, 0), waist=(2, 0, 0))
    c.key(2.0, ra=(0, 0, 0), la=(0, 0, 0), head=(0, 0, 0), crown=(-2, 0, 0), root_pos=(0, 0, 0), waist=(0, 0, 0))
    c.key(2.6)


@clip("talk_sprout_flap", "Excited sprout flapping", trigger="talk", length=2.6, weight=3, require=["child"],
      mirror="free")
def _(c):
    # sprouts tell everything at once: arms flapping, little bounces, the sprout bobbing
    c.key(0.25, ra=(-20, 0, 40), la=(-20, 0, 40), head=(-6, 0, 0))
    c.cycle(0.25, 1.85, 0.4, dict(ra=(-20, 0, 60), la=(-20, 0, 30), root_pos=(0, -1.2, 0), crown=(-10, 0, 0)),
            dict(ra=(-20, 0, 30), la=(-20, 0, 60), root_pos=(0, 0.3, 0), crown=(8, 0, 0)))
    c.key(1.9, head=(-8, 0, 8))
    c.key(2.25, ra=(0, 0, 6), la=(0, 0, 6), root_pos=(0, 0, 0), head=(0, 0, 0), crown=(0, 0, 0))
    c.key(2.6)


# -- listen: while you choose a reply ---------------------------------------------------------------------------

@clip("listen_tilt", "Tilts the head and listens", trigger="listen", length=4.0, weight=3, mirror="free")
def _(c):
    c.key(0.8, head=(4, 6, 13), crown=(0, 0, 18), waist=(1, 0, 2))
    c.key(2.4, head=(6, 8, 15), crown=(0, 0, 21))
    c.key(2.8, head=(10, 6, 12), crown=(6, 0, 16))
    c.key(3.1, head=(4, 6, 12), crown=(0, 0, 14))
    c.key(3.6, head=(0, 0, 0), crown=(0, 0, -3), waist=(0, 0, 0))
    c.key(4.0)


@clip("listen_chin", "Hand to chin", trigger="listen", length=4.4, weight=2, require=["adult"])
def _(c):
    c.key(0.6, ra=(-77, -24, 8), rf=(-106, 0, 0), la=(-28, -26, 0), lf=(-66, 0, 0), head=(10, 0, 0), crown=(4, 0, 0))

    def hum(t):
        e = env(t, 0.6, 3.6, 0.5)
        return dict(crown=(4, 0, 9 * sn(t - 0.6, 1.5) * e), head=(10 + 2 * sn(t - 0.6, 1.5, 0.25) * e, 0, 0))
    sampled(c, 0.6, 3.6, hum, step=0.15)
    c.key(3.9, ra=(-6, 0, 2), rf=(-8, 0, 0), la=(-4, 0, 2), lf=(-6, 0, 0), head=(0, 0, 0), crown=(0, 0, 0))
    c.key(4.4)


@clip("listen_hum_nod", "Hums and nods along", trigger="listen", length=3.6, weight=2, mirror="free")
def _(c):
    def nod(t):
        e = env(t, 0, 3.6, 0.5)
        n = max(0.0, sn(t, 1.1)) ** 1.5
        return dict(head=(3 * e + 10 * n * e, 0, 0), crown=(12 * max(0.0, sn(t, 1.1, -0.12)) * e, 0, 3 * e),
                    root_pos=(0, 0.25 * n * e, 0))
    sampled(c, 0, 3.6, nod, step=0.1)


@clip("listen_lean", "Leans in to listen", trigger="listen", length=4.2, weight=1, require=["adult"],
      boost={"manner:steady": 2})
def _(c):
    clasp = dict(ra=(-34, -24, 0), rf=(-62, 0, 0), la=(-34, -24, 0), lf=(-62, 0, 0))
    c.key(0.8, waist=(9, 0, 0), head=(-4, 0, 6), crown=(-2, 0, 8), root_pos=(0, 0, -0.6), **clasp)
    c.key(2.4, head=(-2, 0, 9), crown=(0, 0, 12))
    c.key(2.9, head=(6, 0, 4), crown=(6, 0, 5))
    c.key(3.6, waist=(0, 0, 0), head=(0, 0, 0), crown=(0, 0, 0), root_pos=(0, 0, 0), ra=(-4, 0, 0), rf=(-6, 0, 0),
          la=(-4, 0, 0), lf=(-6, 0, 0))
    c.key(4.2)


# -- chatting with a neighbour ----------------------------------------------------------------------------------

@clip("chat_tell", "Tells a neighbour", trigger="chat_speak", length=3.6, weight=3)
def _(c):
    c.key(0.4, ra=(-50, 16, 6), rf=(-46, 0, 0), head=(2, 0, -4), crown=(0, 0, -4))
    c.key(0.8, ra=(-64, 22, 10), rf=(-36, 0, 0), head=(8, 0, -6), crown=(6, 0, -6), waist=(3, 4, 0))
    c.key(1.2, ra=(-48, 10, 4), rf=(-54, 0, 0), head=(2, 0, -2), crown=(-2, 0, 0), waist=(1, 2, 0))
    c.key(1.7, ra=(-58, 34, 14), rf=(-26, 0, 0), head=(4, 8, -4), crown=(4, 0, -8))
    c.key(2.3, ra=(-56, 30, 12), rf=(-30, 0, 0), head=(10, 4, 0), crown=(9, 0, -2))
    c.key(2.7, ra=(-28, 6, 4), rf=(-24, 0, 0), head=(2, 0, 0), crown=(-2, 0, 0), waist=(0, 0, 0))
    c.key(3.1, ra=(0, 0, 0), rf=(0, 0, 0), head=(0, 0, 0), crown=(0, 0, 0))
    c.key(3.6)


@clip("chat_laugh", "Hums a big laugh", trigger="chat_speak", length=3.0, weight=2, mirror="free")
def _(c):
    # the laugh comes out as a rumbling hum: shoulders shake, head back, a hand on the belly
    c.key(0.3, head=(-10, 0, 0), waist=(-4, 0, 0), ra=(-34, -30, 0), rf=(-50, 0, 0), crown=(8, 0, 0))
    c.wobble(0.3, 1.9, 7, "root_pos", 0.7, axis=1)
    c.wobble(0.3, 1.9, 7, "crown", 7, base=(8, 0, 0), axis=0)
    c.wobble(0.3, 1.9, 3.5, "head", 5, base=(-12, 0, 0), axis=2)
    c.key(1.9, waist=(8, 0, 0), la=(0, 0, 8))
    c.key(2.3, head=(8, 0, 0), waist=(6, 0, 0), crown=(-4, 0, 0))
    c.key(2.6, head=(0, 0, 0), waist=(0, 0, 0), ra=(0, 0, 0), rf=(0, 0, 0), la=(0, 0, 0), crown=(0, 0, 0))
    c.key(3.0)


@clip("chat_nod", "Nods along with a neighbour", trigger="chat_listen", length=3.4, weight=3)
def _(c):
    c.key(0.5, head=(4, 0, 6), crown=(0, 0, 9), waist=(2, 0, 0))
    for t in (0.9, 1.6):
        c.key(t, head=(14, 0, 4), crown=(4, 0, 6))
        c.key(t + 0.3, head=(2, 0, 6), crown=(-6, 0, 9))
    c.key(2.6, head=(4, 0, 2), crown=(2, 0, 4), la=(-6, 0, 4))
    c.key(3.0, head=(0, 0, 0), crown=(0, 0, 0), waist=(0, 0, 0), la=(0, 0, 0))
    c.key(3.4)


@clip("chat_hum_along", "Traces the harmony with a hand", trigger="chat_listen", length=4.4, weight=2,
      mirror="free")
def _(c):
    # Chorrin join each other's hum: an open hand floats up and down with the note they are holding, the head
    # lifting with the high notes and settling with the low ones, the crown keeping the beat
    c.key(0.6, ra=(-44, 10, 6), rf=(-58, 0, 0), head=(4, 0, 8), crown=(0, 0, 10), waist=(2, 0, 0))

    def tune(t):
        e = env(t, 0.6, 3.5, 0.5)
        note = sn(t - 0.6, 1.9)
        return dict(ra=(-44 - 14 * note * e, 10 + 12 * sn(t - 0.6, 3.8) * e, 6),
                    rf=(-58 + 8 * note * e, 0, 0),
                    head=(4 - 7 * note * e, 0, 8),
                    crown=(-4 * note * e, 0, 10 + 9 * sn(t - 0.6, 0.95) * e))
    sampled(c, 0.6, 3.5, tune, step=0.1)
    # the note ends: the hand settles, a small satisfied nod
    c.key(3.8, ra=(-12, 0, 2), rf=(-14, 0, 0), head=(9, 0, 2), crown=(6, 0, 2), waist=(0, 0, 0))
    c.key(4.1, head=(0, 0, 0), crown=(-2, 0, 0))
