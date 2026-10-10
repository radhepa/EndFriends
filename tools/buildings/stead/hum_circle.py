"""The Hum Circle: the heart of a Chorrin Stead. A ring of end-stone-brick standing stones round a stone
circle sunk one step into the islet, where the Stead sits on the stepped rim and hums together under a
great planted chorus. The rim stays open and walkable: paths can arrive from every side."""
import math

from kit import building
from stead._parts import ESB, ES, STAIRS, WALL, chorus_tree, rng_for, sprout, toward

C = 8           # centre of the 17 x 17 footprint


def r_of(x, z):
    return math.hypot(x - C, z - C)


@building('hum_circle', people='chorrin', role='plaza', size=(17, 17, 17), ground=1, door=8,
          about='The Stead centre: eight end-stone-brick standing stones round a stone circle sunk one '
                'step, its stepped rim for sitting, a great planted chorus in the middle.')
def hum_circle(b):
    g = b.ground
    for z in range(b.d):
        for x in range(b.w):
            r = r_of(x, z)
            if r <= 5.0:
                # the sunken floor: rough stone round the mound, a brick ring, a traded-purpur ring
                if r <= 2.5:
                    floor = ES
                elif r <= 3.4:
                    floor = ESB
                elif r <= 4.3:
                    floor = 'purpur_block'
                else:
                    floor = ESB
                b.set(x, 0, z, floor)
                b.set(x, g, z, 'air')
            elif r <= 6.0:
                # the stepped rim: stairs whose backs face out, so they are both seats and steps
                b.set(x, g, z, STAIRS, facing=toward(x - C, z - C), half='bottom')
            elif r <= 7.6:
                b.set(x, g, z, ESB)
    # froglights set in the purpur ring at the four quarters
    for x, z in ((C, C - 4), (C + 4, C), (C, C + 4), (C - 4, C)):
        b.set(x, 0, z, 'pearlescent_froglight')
    # the mound: a 3x3 bed of end stone with a sloping brick skirt
    for z in range(C - 2, C + 3):
        for x in range(C - 2, C + 3):
            r = r_of(x, z)
            if max(abs(x - C), abs(z - C)) <= 1:
                b.set(x, g, z, ES)
            elif r <= 2.9:
                b.set(x, g, z, STAIRS, facing=toward(C - x, C - z), half='bottom')
    chorus_tree(b, C, g + 1, C, height=9, arms=10, depth=3, flower_age=(4, 5, 5), reach=True,
                rng=rng_for('great', 4))
    for x, z, h in ((C - 1, C + 1, 2), (C + 1, C - 1, 1), (C + 1, C + 1, 1), (C - 1, C - 1, 2)):
        if not b.solid(x, g + 1, z) and not b.solid(x, g + 2, z):
            sprout(b, x, g + 1, z, h)
    # candles on the skirt corners
    for x, z in ((C - 2, C - 2), (C + 2, C - 2), (C - 2, C + 2), (C + 2, C + 2)):
        if not b.solid(x, g + 1, z) and b.solid(x, g, z):
            b.candles(x, g + 1, z, 3, color='white')
    # seats on the rim steps, at the diagonals and either side of each way down
    for deg in range(0, 360, 30):
        if deg % 90 == 0:
            continue
        a = math.radians(deg)
        x, z = round(C + 5.5 * math.sin(a)), round(C - 5.5 * math.cos(a))
        if 5.0 < r_of(x, z) <= 6.0:
            b.spot('sit', x, g, z)
    # the standing stones: eight, between the four ways in; lanterns on four, chorus crowns on four
    for i in range(8):
        a = math.radians(22.5 + 45 * i)
        x, z = round(C + 7.1 * math.sin(a)), round(C - 7.1 * math.cos(a))
        tall = 4 if i % 2 == 0 else 3
        b.fill(x, g + 1, z, x, g + tall, z, ESB)
        # a shoulder stone leaning on the inner side, so each stone reads chunky, not as a post
        sx, sz = round(C + 6.1 * math.sin(a)), round(C - 6.1 * math.cos(a))
        if (sx, sz) != (x, z) and r_of(sx, sz) > 6.0:
            b.set(sx, g + 1, sz, STAIRS, facing=toward(x - sx, z - sz), half='bottom')
        # a sidestone along the ring
        tx, tz = round(C + 7.1 * math.sin(a + 0.16)), round(C - 7.1 * math.cos(a + 0.16))
        if (tx, tz) != (x, z):
            b.fill(tx, g + 1, tz, tx, g + tall - 1, tz, ESB)
            b.set(tx, g + tall, tz, STAIRS, facing=toward(x - tx, z - tz), half='bottom')
        if i % 2 == 0:
            b.set(x, g + tall + 1, z, WALL)
            b.lantern(x, g + tall + 2, z)
        else:
            b.set(x, g + tall, z, ES)
            b.set(x, g + tall + 1, z, 'chorus_flower', age=5)
