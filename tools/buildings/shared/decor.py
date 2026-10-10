"""Street decor: small pieces the planner sprinkles beside paths (role='decor').

Front faces north, toward the path along z = -1. The planner pastes path lamps UNTURNED and centred on a
cell two blocks off the path's centre line, so every lamp keeps its walking-height layers (ground + 1 and
+ 2) to the single centre column; anything wider (a lamp's arms) starts three blocks above the ground,
over the heads of passers-by.
"""
from kit import building
from shared._parts import grow, banner, EYE_OF_THE_SPIRES, BACK


# ------------------------------------------------------------------ lamps
@building('decor_spire_lamp', people='shulkin', role='decor', size=(3, 7, 3), light=True,
          about='A slender purpur lamp post: a little shulker lid on top, end rods hanging from its lip and '
                'one standing on its crown.')
def decor_spire_lamp(b):
    # the lid's rods hang four blocks up, clear of a 2.6-block Shulkin walking the path's edge
    c = 1
    b.set(c, 0, c, 'end_stone_bricks')
    b.set(c, 1, c, 'purpur_block')
    for y in (2, 3, 4):
        b.set(c, y, c, 'purpur_pillar', axis='y')
    # the lid: a purpur cap with a stair lip all round, rods hanging under the lip
    b.set(c, 5, c, 'purpur_block')
    for d, (dx, dz) in {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}.items():
        b.set(c + dx, 5, c + dz, 'purpur_stairs', facing=BACK[d], half='top')
        b.end_rod(c + dx, 4, c + dz, 'down')
    b.end_rod(c, 6, c, 'up')


@building('decor_stead_lamp', people='chorrin', role='decor', size=(1, 5, 1), light=True,
          about='A stout end-stone-brick post holding a pearlescent froglight, three candles burning on top.')
def decor_stead_lamp(b):
    b.set(0, 0, 0, 'end_stone_bricks')
    b.set(0, 1, 0, 'end_stone_bricks')
    b.set(0, 2, 0, 'end_stone_brick_wall')
    b.set(0, 3, 0, 'pearlescent_froglight', axis='y')
    b.candles(0, 4, 0, 3, color='white')


@building('decor_court_lamp', people='court', role='decor', size=(1, 5, 1), light=True,
          about='An obsidian brazier post: blackstone shaft, a bowl of crying obsidian, an end-rod flame.')
def decor_court_lamp(b):
    b.set(0, 0, 0, 'obsidian')
    b.set(0, 1, 0, 'polished_blackstone_bricks')
    b.set(0, 2, 0, 'polished_blackstone_brick_wall')
    b.set(0, 3, 0, 'crying_obsidian')
    b.end_rod(0, 4, 0, 'up')


# ------------------------------------------------------------------ benches
@building('decor_spire_bench', people='shulkin', role='decor', size=(3, 2, 2),
          about='A back-to-back purpur settee: two seats under one raised back, floating slab arms at the ends.')
def decor_spire_bench(b):
    for x in range(3):
        b.set(x, 0, 0, 'purpur_block')
        b.set(x, 0, 1, 'purpur_block')
    for z in (0, 1):
        b.set(0, 1, z, 'purpur_slab', type='top')
        b.set(2, 1, z, 'purpur_slab', type='top')
    b.set(1, 1, 0, 'purpur_stairs', facing='south', half='bottom')
    b.set(1, 1, 1, 'purpur_stairs', facing='north', half='bottom')
    b.spot('sit', 1, 1, 0)
    b.spot('sit', 1, 1, 1)


@building('decor_stead_bench', people='chorrin', role='decor', size=(3, 2, 2),
          about='A long end-stone bench for broad Chorrin backs, chorus flowers growing in the ground behind it.')
def decor_stead_bench(b):
    for x in range(3):
        b.set(x, 1, 0, 'end_stone_brick_stairs', facing='south', half='bottom')
        b.spot('sit', x, 1, 0)
    for x in (0, 2):
        b.set(x, 0, 1, 'end_stone')
        b.set(x, 1, 1, 'chorus_flower', age=5)
    b.set(1, 0, 1, 'end_stone_bricks')
    b.set(1, 1, 1, 'end_stone_brick_slab', type='bottom')


# ------------------------------------------------------------------ planters, goods, banners
@building('decor_chorus_planter', people='chorrin', role='decor', size=(3, 6, 3),
          about='A square end-stone planter with a branching chorus, candles burning on two corners.')
def decor_chorus_planter(b):
    for x in range(3):
        for z in range(3):
            corner = x != 1 and z != 1
            if (x, z) == (1, 1):
                b.set(x, 1, z, 'end_stone')
            elif corner:
                b.set(x, 1, z, 'end_stone_bricks')
            else:
                b.set(x, 1, z, 'end_stone_brick_slab', type='bottom')
    b.candles(0, 2, 0, 2, color='white')
    b.candles(2, 2, 2, 3, color='purple')
    grow(b, 1, 2, 1, 2, [('west', 1, ()), ('east', 2, ())])


@building('decor_crates', people='shared', role='decor', size=(3, 3, 2),
          about='Trade goods waiting by the path: barrels, a crate of popped purpur, bolts of cloth, a pot, a lantern.')
def decor_crates(b):
    b.barrel(0, 1, 0, facing='north')
    b.set(1, 1, 0, 'purpur_block')
    b.set(2, 1, 0, 'decorated_pot', facing='north')
    b.barrel(0, 1, 1, facing='up')
    b.barrel(1, 1, 1, facing='up')
    b.set(2, 1, 1, 'white_wool')
    b.set(0, 2, 1, 'barrel', facing='west', open=False)
    b.set(1, 2, 1, 'purple_wool')
    b.set(1, 2, 0, 'purpur_slab', type='bottom')
    b.lantern(2, 2, 1)


@building('decor_spire_banner_post', people='shulkin', role='decor', size=(1, 5, 1),
          about='A purpur post flying a purple banner with the magenta Eye of the Spires.')
def decor_spire_banner_post(b):
    b.set(0, 0, 0, 'end_stone_bricks')
    b.set(0, 1, 0, 'purpur_block')
    b.set(0, 2, 0, 'purpur_pillar', axis='y')
    banner(b, 0, 3, 0, base='purple', patterns=EYE_OF_THE_SPIRES, facing='north')
