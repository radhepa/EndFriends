"""The Blinker's Post: the Stead's courier station. A tiny dome hut behind a big round door, with a tall
mast rising out of its crown: brick at the foot, a shaft of traded purpur, courier banners and lanterns on
its arms, and a chorus flower at the very top so blinkers can see it from the next island. Message barrels
stack up round the hut, and a purpur blink-stone is set in the paving out front."""
from kit import building
from stead._parts import Dome, round_door, hanging_lantern, pot, shelf, seat, ES, ESB, STAIRS, WALL


@building('blinkers_post', people='chorrin', role='work', size=(9, 17, 10), ground=0, door=4, job='blinker',
          about='A tiny dome hut behind a big round door, a tall purpur mast with courier banners and a chorus '
                'flower rising from its crown, message barrels stacked round it, a blink-stone out front.')
def blinkers_post(b):
    cx, cz = 4, 6
    d = Dome(b, cx, cz, 3.3, 3.3, floor=0, crown=6.5, wall_top=3, power=0.6).build()
    round_door(b, cx, 1, 3, ring='purpur_stairs')
    d.window('east', 2)
    d.window('west', 2)
    # the blink-stone: a purpur ring set in the paving with a froglight at its heart
    for x in range(2, 7):
        for z in range(0, 3):
            b.set(x, 0, z, ESB)
    for x, z in ((3, 0), (4, 0), (5, 0), (3, 1), (5, 1), (3, 2), (4, 2), (5, 2)):
        b.set(x, 0, z, 'purpur_block')
    b.set(4, 0, 1, 'pearlescent_froglight')
    # the mast out of the crown
    top = d.hgt[(cx, cz)]
    y = top
    b.set(cx, y, cz, ESB)
    for k in range(1, 6):
        b.set(cx, y + k, cz, 'purpur_pillar', axis='y')
    b.set(cx, y + 6, cz, ESB)
    b.set(cx, y + 7, cz, ES)
    b.set(cx, y + 8, cz, 'chorus_plant')
    b.set(cx, y + 9, cz, 'chorus_flower', age=5)
    # arms with lanterns, and courier banners hung on the mast
    for dx in (-1, 1):
        b.set(cx + dx, y + 5, cz, WALL)
        b.set(cx + dx, y + 6, cz, STAIRS, facing='west' if dx > 0 else 'east', half='bottom')
        hanging_lantern(b, cx + dx, y + 4, cz, chain=0)
    b.set(cx, y + 4, cz - 1, 'purple_wall_banner', facing='north')
    b.set(cx, y + 4, cz + 1, 'white_wall_banner', facing='south')
    # chorus round the foot of the mast
    for x, z, h in ((cx - 1, cz + 1, 1), (cx + 1, cz + 1, 2)):
        if (x, z) in d.hgt:
            d.plant(x, z, h, branches=False)
    # inside: the reading desk, message barrels, a cushion, a candle
    b.set(cx, 1, 8, 'lectern', facing='north', has_book=False, powered=False)
    b.spot('work', cx, 1, 7)
    b.barrel(2, 1, 6, facing='east')
    b.barrel(2, 1, 7, facing='up')
    b.barrel(6, 1, 6, facing='west')
    if b.solid(7, 2, 7):
        shelf(b, 6, 2, 7, 'west')
    seat(b, 6, 1, 7, 'east', cushion='brown')
    b.candles(2, 2, 7, 3, color='white')
    hanging_lantern(b, cx, 3, cz, chain=None)
    # message barrels stacked round the hut outside
    for x, yy, z, f in ((8, 1, 4, 'up'), (8, 1, 5, 'west'), (8, 1, 6, 'up'), (8, 2, 5, 'up'), (7, 1, 8, 'north'),
                        (8, 1, 8, 'up'), (8, 2, 8, 'west'), (0, 1, 5, 'east'), (0, 1, 6, 'up'), (0, 2, 6, 'up'),
                        (1, 1, 9, 'up')):
        if not b.solid(x, yy, z):
            b.barrel(x, yy, z, facing=f)
    pot(b, 7, 1, 2, 'north')
    pot(b, 1, 1, 2, 'north')
    b.set(8, 1, 1, WALL)
    b.lantern(8, 2, 1)
    b.set(0, 1, 1, WALL)
    b.lantern(0, 2, 1)
