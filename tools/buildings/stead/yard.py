"""The Stonecutter's Yard: an open paved yard where end stone is cut into bricks. Stacks of finished
bricks and a heap of rough stone flank the way in, a stone lifting frame hangs a block on its chain, and at
the back a half dome open to the yard shelters the stonecutters."""
import random

from kit import building
from stead._parts import Dome, hanging_lantern, lantern_post, pot, stone_seat, ES, ESB, SLAB, STAIRS, WALL


@building('stonecutters_yard', people='chorrin', role='work', size=(13, 9, 11), ground=0, door=6, job='stonecutter',
          about='A paved yard with stacks of cut end-stone bricks, a heap of rough stone and a lifting frame, '
                'and a half dome open to the yard sheltering two stonecutters.')
def stonecutters_yard(b):
    rng = random.Random(41)
    # the paving: brick, worn through to rough end stone here and there
    for z in range(b.d):
        for x in range(b.w):
            b.set(x, 0, z, ES if rng.random() < 0.22 else ESB)
    # the shelter: a dome cut in half, its open face to the yard
    d = Dome(b, 6, 7, 4.3, 3.9, floor=0, crown=6.6, power=0.6).build()
    for (x, z) in list(d.hgt):
        if z < 7:
            for y in range(1, b.h):
                if b.solid(x, y, z):
                    b.set(x, y, z, 'air')
    # the cut edge reads as an arch: give it a brick lip
    for x in range(b.w):
        for y in range(1, b.h):
            if b.solid(x, y, 7) and b.get(x, y, 7)[0] == 'minecraft:end_stone':
                b.set(x, y, 7, ESB)
    for x in range(3, 10):
        b.set(x, 0, 8, ESB)
        b.set(x, 0, 9, ESB)
    b.set(4, 1, 9, 'stonecutter', facing='north')
    b.set(8, 1, 9, 'stonecutter', facing='north')
    b.spot('work', 4, 1, 8)
    b.set(6, 1, 9, SLAB, type='top')
    b.candles(6, 2, 9, 2, color='white')
    if not b.solid(3, 1, 8):
        b.barrel(3, 1, 8, facing='up')
    if not b.solid(9, 1, 8):
        b.barrel(9, 1, 8, facing='up')
    hanging_lantern(b, 6, 3, 8, chain=1)
    d.roof_grove(big=3, small=(2, 1), skylight=False, spread=1)
    # stacks of cut bricks on the west side: blocks, slabs on top, stairs leaning
    stacks = [(1, 1, 3), (2, 1, 2), (1, 2, 2), (2, 2, 1), (1, 4, 3), (2, 4, 2), (1, 5, 1)]
    for x, z, h in stacks:
        b.fill(x, 1, z, x, h, z, ESB)
        if h < 3:
            b.set(x, h + 1, z, SLAB, type='bottom')
    b.set(3, 1, 1, STAIRS, facing='west', half='bottom')
    b.set(3, 1, 4, STAIRS, facing='west', half='bottom')
    b.set(2, 1, 3, SLAB, type='bottom')
    b.set(2, 2, 3, SLAB, type='top')
    # a heap of rough end stone on the east side
    heap = [(10, 1, 2), (11, 1, 3), (11, 2, 2), (10, 2, 1), (11, 3, 1), (10, 3, 1), (11, 4, 2), (10, 4, 1),
            (9, 2, 1)]
    for x, z, h in heap:
        b.fill(x, 1, z, x, h, z, ES)
    b.set(9, 1, 3, STAIRS, facing='east', half='bottom')
    if not b.solid(10, 3, 2):
        b.set(10, 3, 2, STAIRS, facing='south', half='bottom')
    # the lifting frame over the heap: two posts, a beam, a block hanging on its chain
    for x in (8, 12):
        b.fill(x, 1, 5, x, 4, 5, WALL)
    b.fill(8, 5, 5, 12, 5, 5, SLAB, type='bottom')
    b.set(10, 5, 5, ESB)
    b.set(10, 4, 5, 'iron_chain', axis='y', waterlogged=False)
    b.set(10, 3, 5, 'iron_chain', axis='y', waterlogged=False)
    b.set(10, 2, 5, ES)
    b.lantern(8, 6, 5)
    b.lantern(12, 6, 5)
    # low walls along the sides, lamps at the front corners, a bench by the gate
    for z in range(0, 7):
        if not b.solid(0, 1, z):
            b.set(0, 1, z, WALL)
        if not b.solid(12, 1, z):
            b.set(12, 1, z, WALL)
    lantern_post(b, 0, 1, 0)
    lantern_post(b, 12, 1, 0)
    stone_seat(b, 4, 1, 0, 'north')
    pot(b, 8, 1, 0, 'north')
