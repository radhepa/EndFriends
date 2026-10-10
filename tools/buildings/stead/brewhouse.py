"""The Brewhouse: a dome sunk one step into the islet, with a little lantern cupola on its crown to let the
fumes out. Inside, a cauldron simmers over a sunken campfire between the brewing stands, and the walls
are lined with barrels, cauldrons and shelves of bottles."""
from kit import building
from stead._parts import Dome, round_door, sunk_entry, pot, shelf, seat, toward, ES, SLAB, STAIRS, WALL


@building('brewhouse', people='chorrin', role='work', size=(11, 13, 12), ground=1, door=5, job='brewer',
          about='A dome sunk one step, crowned with a lantern cupola: brewing stands round a cauldron over a '
                'sunken fire, the walls lined with barrels, cauldrons and shelves.')
def brewhouse(b):
    cx, cz = 5, 7
    d = Dome(b, cx, cz, 4.5, 4.5, floor=0, crown=8.4, power=0.6, band=4).build()
    d.berm(skip={(x, z) for x in range(2, 9) for z in range(0, 3)})
    sunk_entry(b, cx, 0, 3)
    round_door(b, cx, 1, 3, ring='purpur_stairs')
    for side in ('east', 'west', 'south'):
        d.window(side, 3)
    # the cupola: four posts on the crown, a stepped cap with a chorus flower for a finial
    top = d.hgt[(cx, cz)]
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            if dx and dz:           # corner posts, capped with slabs
                b.fill(cx + dx, top, cz + dz, cx + dx, top + 1, cz + dz, WALL)
                b.set(cx + dx, top + 2, cz + dz, SLAB, type='bottom')
            elif dx or dz:          # the cap's sides lean in to the finial
                b.set(cx + dx, top + 2, cz + dz, STAIRS, facing=toward(-dx, -dz), half='bottom')
    b.set(cx, top + 2, cz, ES)
    b.set(cx, top + 3, cz, 'chorus_flower', age=5)
    b.set(cx, top + 1, cz, 'iron_chain', axis='y', waterlogged=False)
    b.lantern(cx, top, cz, hanging=True)
    b.set(cx, top - 1, cz, 'pearlescent_froglight')     # the vent's glowing floor is the room's skylight
    # chorus on the shoulders of the dome, round the cupola
    for x, z, h in ((cx - 2, cz + 1, 3), (cx + 2, cz + 2, 2), (cx + 2, cz - 2, 1), (cx - 2, cz - 2, 2)):
        d.plant(x, z, h, branches=h >= 3)
    # the brewing hearth: a cauldron over a campfire sunk in the floor, brewing stands either side
    b.set(cx, 0, cz, 'campfire', facing='north', lit=True, signal_fire=False, waterlogged=False)
    b.set(cx, 1, cz, 'cauldron')
    for x in (cx - 1, cx + 1):
        b.set(x, 1, cz, 'brewing_stand', has_bottle_0=True, has_bottle_1=x < cx, has_bottle_2=False)
    b.spot('work', cx - 1, 1, cz - 1)
    seat(b, cx + 1, 1, cz - 1, 'south', cushion='white')
    # the walls: cauldrons, barrels, shelves of bottles, a working bench
    for x, z in ((2, 6), (2, 8)):
        b.set(x, 1, z, 'cauldron')
    b.set(2, 1, 7, SLAB, type='top')
    b.set(2, 2, 7, 'brewing_stand', has_bottle_0=True, has_bottle_1=True, has_bottle_2=True)
    for x, z, f in ((8, 6, 'up'), (8, 7, 'west'), (8, 8, 'up'), (7, 9, 'north')):
        b.barrel(x, 1, z, facing=f)
    b.barrel(8, 2, 7, facing='up')
    b.candles(8, 2, 6, 3, color='purple')
    b.candles(8, 2, 8, 2, color='white')
    shelf(b, 4, 2, 10, 'north')
    shelf(b, 6, 2, 10, 'north')
    pot(b, 3, 1, 9, 'north')
    pot(b, 5, 1, 10, 'north')
    if not b.solid(3, 1, 4):
        b.lantern(3, 1, 4)
    if not b.solid(7, 1, 4):
        b.lantern(7, 1, 4)
