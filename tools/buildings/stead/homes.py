"""Chorrin dome homes: half-sunk end-stone domes with a chorus crown, entered down a short flight of
steps to a round door. Nobody sleeps in a bed in the End; Chorrin curl up in nests of woven chorus
fibre (wool stairs round a carpeted hollow).

All three homes have ground = 2 and their floor on layer 0: the room is sunk two blocks, so the step
into the entrance at (door, ground - 1, 0) is a stair one block below the path."""
from kit import building
from stead._parts import (Dome, chorus_tree, sprout, round_door, nest, rug, seat, pot, shelf, hanging_lantern, sunk_entry,
                          arch_opening, ES, ESB, SLAB, STAIRS, WALL)


# ---------------------------------------------------------------------------------------- dome_home
@building('dome_home', people='chorrin', role='home', size=(11, 12, 12), ground=2, residents=2, door=5,
          about='A half-sunk dome for two: steps down to a round door, a chorus crown on the roof, '
                'two fibre nests round a woven rug.')
def dome_home(b):
    d = Dome(b, 5, 6, 4.5, 4.5, floor=0, crown=7.6).build()
    d.berm(skip={(x, z) for x in range(2, 9) for z in range(0, 2)})
    sunk_entry(b, 5, 0, 2)
    round_door(b, 5, 1, 2, ring='purpur_stairs')
    for side in ('east', 'west', 'south'):
        d.window(side, 4)
    d.roof_grove(big=4, small=(1, 2, 3), spread=1)
    # inside: a rug in the middle, nests at the back, a table and stores at the sides
    rug(b, 4, 5, 6, 7, 1, colors=('white', 'purple'), border='brown')
    nest(b, 3, 1, 9, opening='north', rim='brown', bed='white', lining='purple')
    nest(b, 7, 1, 9, opening='north', rim='purple', bed='white', lining='brown')
    b.set(2, 1, 6, SLAB, type='top')
    b.candles(2, 2, 6, 3, color='white')
    seat(b, 2, 1, 5, 'north')
    seat(b, 2, 1, 7, 'south')
    b.barrel(8, 1, 5, facing='up')
    b.barrel(8, 1, 6, facing='west')
    pot(b, 8, 1, 7, 'west')
    b.lantern(8, 2, 5)
    hanging_lantern(b, 5, 4, 6, chain=1)


# ---------------------------------------------------------------------------------- dome_home_large
@building('dome_home_large', people='chorrin', role='home', size=(16, 14, 14), ground=2, residents=4, door=6,
          about='A big half-sunk dome for four with a little sprout dome budding off its side: a hearth room '
                'behind the round door and, through an inner arch, the nest room of the sprouts.')
def dome_home_large(b):
    main = Dome(b, 6, 7, 5.5, 5.5, floor=0, crown=8.6)
    d = Dome(b, 6, 7, 5.5, 5.5, floor=0, crown=8.6, lobes=[(12, 9, 3.5, 3.5, 7.0)]).build()
    d.berm(skip={(x, z) for x in range(3, 10) for z in range(0, 2)})
    sunk_entry(b, 6, 0, 2)
    round_door(b, 6, 1, 2, ring='purpur_stairs')
    # the big dome's own wall stands between the two rooms, with a round arch through it
    for (x, y, z) in main.shell:
        if d.is_room(x, y, z):
            b.set(x, y, z, ESB)
    arch_opening(b, 8, 1, 11, axis='z')
    d.window('west', 4, offset=-2)
    d.window('west', 4, offset=2)
    d.window('south', 4, offset=-2)
    d.window('north', 4, offset=-3)
    d.roof_grove(big=5, small=(2, 3, 1), spread=1, arms=4)
    sx, sz = 12, 9                       # the sprout dome's crown: its own little chorus and skylight
    d.plant(sx + 1, sz, 3, tree=True, arms=2)
    b.set(sx, d.hgt[(sx, sz)] - 1, sz, 'pearlescent_froglight')
    if (sx, sz) in d.piece:
        b.set(sx, d.hgt[(sx, sz)], sz, 'air')
    for x, z in ((1, 12), (14, 13)):     # lamps round the back
        b.set(x, 3, z, WALL)
        b.lantern(x, 4, z)
    # hearth room: a rug, a low table with cushions, stores, high shelves, two nests at the back
    rug(b, 5, 5, 7, 7, 1, colors=('purple', 'white'), border='white')
    b.set(3, 1, 5, SLAB, type='top')
    b.candles(3, 2, 5, 3, color='white')
    seat(b, 2, 1, 5, 'west')
    seat(b, 3, 1, 4, 'north', cushion='brown')
    seat(b, 3, 1, 6, 'south', cushion='white')
    b.barrel(9, 1, 4, facing='up')
    b.barrel(9, 2, 4, facing='west')
    b.barrel(10, 1, 5, facing='west')
    b.lantern(10, 2, 5)
    shelf(b, 4, 3, 11, 'north')
    shelf(b, 8, 3, 11, 'north')
    nest(b, 3, 1, 9, opening='east', rim='brown', bed='white', lining='purple')
    nest(b, 6, 1, 10, opening='north', rim='purple', bed='white', lining='brown')
    hanging_lantern(b, 6, 4, 8, chain=None)
    b.candles(4, 1, 11, 2, color='white')
    # the sprouts' room: two small nests and a candle
    nest(b, 13, 1, 8, opening='south', rim='white', bed='purple', lining='brown')
    nest(b, 13, 1, 11, opening='north', rim='brown', bed='white', lining='purple')
    b.candles(14, 1, 10, 3, color='purple')
    if not b.solid(11, 1, 11):
        pot(b, 11, 1, 11, 'west')
    hanging_lantern(b, 12, 3, 10, chain=None)


# ---------------------------------------------------------------------------------------- dome_pair
@building('dome_pair', people='chorrin', role='home', size=(21, 12, 13), ground=2, residents=5, door=10,
          about='Two half-sunk domes for five, joined by a short vaulted hall; the round door opens off a '
                'sunken court between them, with chorus growing in it.')
def dome_pair(b):
    west = Dome(b, 4, 7, 4.2, 4.2, floor=0, crown=7.4).build()
    east = Dome(b, 16, 7, 4.2, 4.2, floor=0, crown=7.4).build()
    court = {(x, z) for x in range(8, 13) for z in range(0, 10)}
    west.berm(skip=court)
    east.berm(skip=court)
    # the hall: x 9..11, z 6..8, under a little barrel vault
    b.fill(8, 0, 5, 12, 0, 9, ESB)
    b.clear(9, 1, 6, 11, 3, 8)
    b.fill(8, 1, 9, 12, 3, 9, ESB)
    for x in range(8, 13):
        b.set(x, 4, 9, STAIRS, facing='north', half='bottom')
        for z in (6, 7, 8):
            b.set(x, 4, z, ES)
        b.set(x, 5, 6, STAIRS, facing='south', half='bottom')
        b.set(x, 5, 8, STAIRS, facing='north', half='bottom')
        b.set(x, 5, 7, ES)
    arch_opening(b, 7, 1, 8, axis='z')
    arch_opening(b, 7, 1, 12, axis='z')
    chorus_tree(b, 10, 6, 7, height=3, arms=2, depth=0)
    # the sunken court and the door
    sunk_entry(b, 10, 0, 5)
    round_door(b, 10, 1, 5, ring='purpur_stairs')
    b.set(9, 0, 3, ES)
    sprout(b, 9, 1, 3, 2)
    b.set(11, 0, 2, ES)
    sprout(b, 11, 1, 2, 1)
    pot(b, 11, 1, 4, 'west')
    b.lantern(9, 1, 1)
    hanging_lantern(b, 10, 2, 7, chain=1)
    # the yard behind the hall
    b.set(10, 3, 11, WALL)
    b.lantern(10, 4, 11)
    b.barrel(9, 3, 10, facing='up')
    pot(b, 11, 3, 10, 'south')
    for dome, side in ((west, 'west'), (east, 'east')):
        dome.window(side, 4)
        dome.window(side, 4, offset=2)
        dome.window(side, 4, offset=-2)
        dome.roof_grove(big=4, small=(2, 1), spread=1)
    # west dome: three nests round a rug
    rug(b, 3, 6, 5, 8, 1, colors=('purple', 'white'), border='brown')
    nest(b, 4, 1, 4 + 1, opening='south', rim='brown', bed='white', lining='purple')
    nest(b, 2, 1, 7, opening='east', rim='purple', bed='white', lining='brown')
    nest(b, 4, 1, 9, opening='north', rim='brown', bed='white', lining='purple')
    b.lantern(6, 1, 5)
    b.candles(6, 1, 9, 3, color='white')
    # east dome: two nests, the table, the stores
    nest(b, 16, 1, 9, opening='north', rim='brown', bed='white', lining='purple')
    nest(b, 18, 1, 7, opening='west', rim='purple', bed='white', lining='brown')
    b.set(15, 1, 6, SLAB, type='top')
    b.set(16, 1, 6, SLAB, type='top')
    b.candles(15, 2, 6, 3, color='white')
    b.candles(16, 2, 6, 2, color='purple')
    seat(b, 15, 1, 5, 'north')
    seat(b, 16, 1, 5, 'north', cushion='white')
    seat(b, 17, 1, 6, 'east', cushion='brown')
    b.barrel(14, 1, 9, facing='up')
    b.barrel(14, 2, 9, facing='north')
    pot(b, 13, 1, 9, 'north')
    hanging_lantern(b, 16, 4, 7, chain=1)
