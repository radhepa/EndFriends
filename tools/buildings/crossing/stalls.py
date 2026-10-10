"""Small trade stalls that stand round a Crossing's market (role 'work', front and counter facing the path).

``trade_stall_awning``: a Shulkin stall of purpur under a striped magenta-and-purple cloth awning.
``trade_stall``: a Chorrin stall of end stone, chorus flanking the counter and flowering on its roof.
The trader stands behind the counter; customers stand at the front, under the eave (three blocks clear).
"""
from kit import building
from shared._parts import grow, hanging_sign, banner, EYE_OF_THE_SPIRES


@building('trade_stall_awning', people='shared', role='work', size=(7, 7, 5), door=3, residents=0, job='trader',
          stall_people='shulkin',
          about='A Shulkin trade stall: a purpur counter under a striped cloth awning, bolts of void cloth and '
                'end rods for sale, the Eye of the Spires hanging behind the trader.')
def trade_stall_awning(b):
    # floor: purpur inside, an end-stone-brick apron where customers stand
    for x in range(7):
        b.set(x, 0, 0, 'end_stone_bricks')
        for z in range(1, 5):
            b.set(x, 0, z, 'purpur_block' if (x + z) % 2 else 'purpur_pillar', **({} if (x + z) % 2 else {'axis': 'y'}))
    # posts at the front, a back wall, a closed west side, the east side open for the trader
    for y in range(1, 4):
        b.set(0, y, 1, 'purpur_pillar', axis='y')
        b.set(6, y, 1, 'purpur_pillar', axis='y')
        for x in range(7):
            b.set(x, y, 4, 'purpur_block')
        b.set(0, y, 2, 'purpur_block')
        b.set(0, y, 3, 'purpur_block')
    b.set(0, 4, 4, 'purpur_block')
    b.set(6, 4, 4, 'purpur_block')
    for x in range(1, 6):
        b.set(x, 4, 4, 'purpur_block')
    b.set(0, 2, 2, 'magenta_stained_glass_pane')
    b.set(0, 2, 3, 'magenta_stained_glass_pane')
    b.set(0, 4, 2, 'purpur_slab', type='bottom')
    b.set(0, 4, 3, 'purpur_slab', type='bottom')
    b.set(6, 1, 3, 'purpur_block')
    b.set(6, 2, 3, 'magenta_stained_glass_pane')
    b.set(6, 3, 3, 'purpur_block')
    # the counter: upside-down stairs, lip toward the customers
    for x in range(1, 6):
        b.set(x, 1, 1, 'purpur_stairs', facing='south', half='top')
    # the awning: striped cloth sloping to an eave over the customers
    for x in range(7):
        c = 'magenta' if x % 2 == 0 else 'purple'
        b.set(x, 4, 0, f'{c}_wool_stairs', facing='south', half='bottom')
        b.set(x, 4, 1, f'{c}_wool')
        b.set(x, 5, 2, f'{c}_wool_stairs', facing='south', half='bottom')
        b.set(x, 5, 3, f'{c}_wool')
        b.set(x, 5, 4, f'{c}_wool_slab', type='bottom')
    b.end_rod(0, 6, 4, 'up')
    b.end_rod(6, 6, 4, 'up')
    for x in (1, 5):
        b.end_rod(x, 4, 2, 'down')
    # goods: bolts of cloth, end rods by the bundle, glass, a loom, the Eye of the Spires on the wall
    b.set(1, 1, 3, 'purple_wool')
    b.set(1, 2, 3, 'magenta_wool')
    b.set(2, 1, 3, 'magenta_wool')
    b.set(5, 1, 3, 'loom', facing='west')
    banner(b, 3, 3, 3, base='purple', patterns=EYE_OF_THE_SPIRES, facing='north', wall=True)
    b.end_rod(1, 2, 1, 'east')
    b.end_rod(2, 2, 1, 'east')
    b.set(3, 2, 1, 'magenta_stained_glass_pane')
    b.candles(4, 2, 1, 3, color='magenta')
    b.set(5, 2, 1, 'purple_carpet')
    hanging_sign(b, 3, 3, 0, ['Spire Goods', 'cloth, rods', 'and glass'], facing='north', wood='crimson', color='magenta')
    b.spot('work', 3, 1, 2)
    b.spot('stand', 3, 1, 0)


@building('trade_stall', people='shared', role='work', size=(7, 6, 5), door=3, residents=0, job='trader',
          stall_people='chorrin',
          about='A Chorrin trade stall: a heavy end-stone counter with a planting box of chorus flowers, chorus '
                'growing up both front corners and flowering along the roof, lanterns within.')
def trade_stall(b):
    for x in range(7):
        b.set(x, 0, 0, 'end_stone')
        for z in range(1, 5):
            b.set(x, 0, z, 'end_stone_bricks' if (x * 2 + z) % 5 else 'end_stone')
    # wall posts at the front, brick back wall and west side, the east side open for the trader
    for y in range(1, 4):
        b.set(0, y, 1, 'end_stone_brick_wall')
        b.set(6, y, 1, 'end_stone_brick_wall')
        for x in range(7):
            b.set(x, y, 4, 'end_stone_bricks')
        b.set(0, y, 2, 'end_stone_bricks')
        b.set(0, y, 3, 'end_stone_bricks')
    b.set(6, 1, 3, 'end_stone_bricks')
    b.set(6, 2, 3, 'end_stone_brick_wall')
    b.set(6, 3, 3, 'end_stone_bricks')
    b.set(3, 2, 4, 'pearlescent_froglight', axis='z')
    # counter: brick stairs with a planting box of chorus flowers in the middle
    for x in range(1, 6):
        b.set(x, 1, 1, 'end_stone_brick_stairs', facing='south', half='top')
    b.set(3, 1, 1, 'end_stone')
    b.set(3, 2, 1, 'chorus_flower', age=5)
    # roof: bottom slabs (nothing can spawn on them), an eave of stairs, a strip of end stone at the
    # back where chorus flowers grow along the roof
    for x in range(7):
        for z in (1, 2, 3):
            b.set(x, 4, z, 'end_stone_brick_slab', type='bottom')
        b.set(x, 4, 4, 'end_stone')
        if x % 2 == 0:
            b.set(x, 5, 4, 'chorus_flower', age=5)
    for x in range(1, 6):
        b.set(x, 4, 0, 'end_stone_brick_stairs', facing='south', half='bottom')
    # round the upper corners of the opening, as Chorrin frame every doorway
    b.set(1, 3, 1, 'end_stone_brick_stairs', facing='west', half='top')
    b.set(5, 3, 1, 'end_stone_brick_stairs', facing='east', half='top')
    # chorus climbing the front corners
    for x in (0, 6):
        grow(b, x, 1, 0, 3, flower=True)
    # lanterns hung from the roof, clear of the trader's head
    b.lantern(1, 3, 3, hanging=True)
    b.lantern(5, 3, 3, hanging=True)
    # goods: chorus fruit in pots and barrels, a brewing stand, popped chorus (purpur) for the Shulkin
    b.set(1, 1, 3, 'barrel', facing='up', open=False)
    b.set(1, 2, 3, 'barrel', facing='east', open=False)
    b.set(2, 1, 3, 'decorated_pot', facing='north')
    b.set(4, 1, 3, 'purpur_block')
    b.set(4, 2, 3, 'purpur_slab', type='bottom')
    b.set(5, 1, 3, 'cauldron')
    b.set(1, 2, 1, 'brewing_stand', has_bottle_0=True, has_bottle_1=False, has_bottle_2=True)
    b.set(5, 2, 1, 'decorated_pot', facing='north')
    b.candles(2, 2, 1, 2, color='white')
    b.candles(4, 2, 1, 3, color='purple')
    hanging_sign(b, 3, 3, 0, ['Grove Stall', 'chorus fresh', 'and popped'], facing='north', wood='pale_oak', color='white')
    b.spot('work', 3, 1, 2)
    b.spot('stand', 3, 1, 0)
