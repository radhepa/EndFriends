"""Shulkin workplaces: the Archive, the Lamp Tower, the Weavers' Loft, the Shellwright's Workshop and
the Driftray Roost."""
import random

from kit import building

from spire._parts import (DIRS4, OPP, air, band, column, corners, doorway, edge, facing_out, hang, lip, octo, put, rect,
                          rings, shrink, stair_path, stair_roof)


def tier_lid(b, plan, y, step_to=None):
    """A stepped lid over ``plan``: at y a lip of upside-down stairs round the outline and a solid
    ceiling inside; at y + 1 a ring of stairs sloping up toward ``step_to`` (the next tier's plan)."""
    lip(b, plan, y)
    put(b, plan - edge(plan), y, 'purpur_block')
    inner = shrink(plan)
    for x, z in edge(plan):
        d = facing_out(plan, x, z)
        b.set(x, y + 1, z, 'purpur_stairs', facing=OPP[d], half='bottom')
    put(b, inner, y + 1, 'purpur_block')
    if step_to is not None:
        ring = inner - step_to
        for x, z in edge(inner):
            if (x, z) in ring:
                d = facing_out(inner, x, z)
                b.set(x, y + 2, z, 'purpur_stairs', facing=OPP[d], half='bottom')


# =========================================================================================== Archive
@building('archive', people='shulkin', role='work', size=(13, 26, 13), door=6, job='archivist',
          about='A tower of three stacked shells, each with its own glowing gap and lid: a tall reading room, '
                'the stacks round a central column of shelves, and a small vault of records at the top.')
def archive(b):
    c = 6
    p1 = octo(c, c, 5)                       # reading room: an octagon
    p2 = octo(c, c, 4, k=7)                  # the stacks: a square with clipped corners (a quarter turn of shell)
    p3 = octo(c, c, 3)                       # the vault
    # ---- plinth
    put(b, octo(c, c, 6), 0, 'end_stone_bricks')
    put(b, shrink(p1), 0, 'purpur_block')
    for x, z in ((c - 4, c - 4), (c + 4, c - 4), (c - 4, c + 4), (c + 4, c + 4)):
        b.set(x, 0, z, 'pearlescent_froglight')
    # ---- tier 1: walls y1..6, gap y7, lid y8..9
    column(b, edge(p1), 1, 6, 'purpur_block')
    for x, z in corners(p1):
        for y in range(1, 7):
            b.set(x, y, z, 'purpur_pillar', axis='y')
    band(b, edge(p1), 7, 7, every=2, posts=corners(p1))
    tier_lid(b, octo(c, c, 6), 8, step_to=p2)
    # ---- tier 2: walls y10..15, gap y16, lid y17..18
    column(b, edge(p2), 10, 15, 'purpur_block')
    for x, z in corners(p2):
        for y in range(10, 16):
            b.set(x, y, z, 'purpur_pillar', axis='y')
    band(b, edge(p2), 16, 16, every=2, posts=corners(p2))
    tier_lid(b, octo(c, c, 5, k=8), 17, step_to=p3)
    # ---- tier 3: walls y19..21, gap y22, domed lid y23..24 and a crest
    column(b, edge(p3), 19, 21, 'purpur_block')
    band(b, edge(p3), 22, 22, every=2)
    lid3 = octo(c, c, 4)
    lip(b, lid3, 23)
    put(b, lid3 - edge(lid3), 23, 'purpur_block')
    tops = {cell: 24 + min(i, 1) for cell, i in rings(lid3).items()}
    stair_roof(b, tops, {cell: 24 for cell in lid3})
    b.set(c, 25, c, 'end_rod', facing='up')
    # windows: tall slits on the faces of each tier
    for d, (dx, dz) in DIRS4.items():
        for y in range(2, 6):
            if d != 'north' or y >= 5:
                b.set(c + 5 * dx, y, c + 5 * dz, 'magenta_stained_glass_pane')
        for y in range(11, 15):
            b.set(c + 4 * dx, y, c + 4 * dz, 'magenta_stained_glass_pane')
        b.set(c + 3 * dx, 20, c + 3 * dz, 'magenta_stained_glass_pane')
    # ---- the door, with the archive's sign over it
    doorway(b, c, 1, c - 5, 'north')
    b.sign(c, 4, c - 6, ['', 'The Archive', 'all is recorded', ''], facing='north')

    # ---- stairs: one spiral up the inside of the reading room into the stacks
    path = [(c - 1, c + 2), (c, c + 2), (c + 1, c + 2), (c + 2, c + 2), (c + 2, c + 1), (c + 2, c), (c + 2, c - 1),
            (c + 2, c - 2), (c + 1, c - 2), (c, c - 2), (c - 1, c - 2)]
    stair_path(b, path, 1)
    b.set(c - 2, 9, c - 2, 'purpur_block')

    # ---- tier 1: the reading room
    # shelves round the walls (two high), lecterns, a reading table under a lantern
    for x, z in edge(shrink(p1)):
        dx, dz = x - c, z - c
        if max(abs(dx), abs(dz)) < 3:
            continue
        if dz <= -3 and abs(dx) <= 1:
            continue  # the entry
        if abs(dx) == 4 and dz == 0 or abs(dz) == 4 and dx == 0:
            continue  # under the windows
        for y in (1, 2, 3):
            if not b.solid(x, y, z):
                b.set(x, y, z, 'bookshelf' if (x + z + y) % 3 else 'chiseled_bookshelf',
                      **({'facing': OPP[facing_out(shrink(p1), x, z)]} if (x + z + y) % 3 == 0 else {}))
    # under the east flight: low shelves
    for z in (c - 1, c, c + 1):
        for y in (1, 2):
            if not b.solid(c + 2, y, z):
                b.set(c + 2, y, z, 'bookshelf')
    # the archivist's lectern (the job block) by the west window, a second one by the east
    b.set(c - 3, 1, c, 'lectern', facing='east', has_book=False, powered=False)
    b.spot('work', c - 2, 1, c)
    b.set(c - 3, 1, c - 1, 'purpur_slab', type='top')
    b.candles(c - 3, 2, c - 1, 3, 'purple')
    # reading table and seats in the middle
    b.set(c, 1, c, 'purpur_slab', type='top')
    b.set(c - 1, 1, c, 'purpur_slab', type='top')
    b.candles(c, 2, c, 4, 'white')
    b.set(c, 1, c + 1, 'purpur_stairs', facing='south')
    b.spot('sit', c, 1, c + 1)
    b.set(c - 1, 1, c - 1, 'purpur_stairs', facing='north')
    b.spot('sit', c - 1, 1, c - 1)
    b.fill(c - 1, 1, c + 1, c - 1, 1, c + 1, 'purple_carpet')
    hang(b, c, 7, c)
    b.set(c, 7, c, 'iron_chain', axis='y')
    hang(b, c, 6, c)
    for x, z, f in ((c - 4, c - 2, 'east'), (c + 4, c - 2, 'west'), (c - 4, c + 2, 'east'), (c + 4, c + 2, 'west')):
        b.end_rod(x, 5, z, f)

    # ---- tier 2: the stacks, a column of shelves in the middle, a ladder up its south face
    for x, z in rect(c - 1, c - 1, c + 1, c + 1):
        for y in range(10, 17):
            b.set(x, y, z, 'bookshelf' if (x - c) * (z - c) != 0 or y % 3 else 'chiseled_bookshelf',
                  **({'facing': 'north'} if (x - c) * (z - c) == 0 and y % 3 == 0 else {}))
    for y in range(10, 19):
        b.set(c, y, c + 2, 'ladder', facing='south', waterlogged=False)
    b.set(c, 13, c + 1, 'chiseled_bookshelf', facing='south')
    for x, z in edge(shrink(p2)):
        dx, dz = x - c, z - c
        if max(abs(dx), abs(dz)) == 3 and not b.solid(x, 10, z):
            if abs(dx) == 3 and abs(dz) <= 1 or abs(dz) == 3 and abs(dx) <= 1:
                continue
            for y in (10, 11, 12):
                b.set(x, y, z, 'bookshelf')
    for d, (dx, dz) in DIRS4.items():
        x, z = c + 3 * dx, c + 3 * dz
        if d == 'north':
            continue
        b.set(x, 10, z, 'lectern', facing=OPP[d], has_book=False, powered=False)
    hang(b, c - 2, 15, c + 2)
    hang(b, c + 2, 15, c + 2)
    hang(b, c + 2, 15, c - 2) if not b.solid(c + 2, 15, c - 2) else None
    hang(b, c - 2, 15, c - 2) if not b.solid(c - 2, 15, c - 2) else None
    b.spot('stand', c - 2, 10, c)
    # railings beside the stairwell
    b.set(c + 3, 10, c - 1, 'end_stone_brick_wall')
    b.set(c + 3, 10, c - 2, 'end_stone_brick_wall') if not b.solid(c + 3, 10, c - 2) else None

    # ---- tier 3: the vault of records (reached by the ladder)
    air(b, {(c, c + 2)}, 17, 18)
    b.set(c, 19, c, 'lectern', facing='south', has_book=False, powered=False)
    b.chest(c - 1, 19, c - 1, facing='east')
    b.chest(c + 1, 19, c - 1, facing='west')
    b.set(c - 2, 19, c, 'barrel', facing='east', open=False)
    b.set(c + 2, 19, c, 'barrel', facing='west', open=False)
    b.end_rod(c, 22, c, 'down')
    b.set(c - 1, 19, c + 1, 'purple_carpet')
    b.set(c + 1, 19, c + 1, 'purple_carpet')


# ======================================================================================== Lamp Tower
@building('lamp_tower', people='shulkin', role='work', size=(7, 34, 7), door=3, job='lamplighter',
          about="The village's tallest, slenderest tower: a spiral stair winds up a shaft ringed with little "
                'lids and glowing gaps to a lantern room of magenta glass, under a lid crowned with end rods.')
def lamp_tower(b):
    c = 3
    foot = octo(c, c, 3, k=5)               # 7x7, corners clipped
    shaft = octo(c, c, 2, k=3)              # 5x5, corners clipped: walls round a 3x3 core
    ring8 = [(c, c - 1), (c + 1, c - 1), (c + 1, c), (c + 1, c + 1), (c, c + 1), (c - 1, c + 1), (c - 1, c),
             (c - 1, c - 1)]                # the spiral's ring round the central column (clockwise from north)
    TOP = 24                                # the lantern room floor
    # ---- plinth and foot (the first, broadest shell)
    for x in range(7):
        for z in range(7):
            b.set(x, 0, z, 'end_stone_bricks')
    for x, z in ((0, 0), (6, 0), (0, 6), (6, 6)):
        b.set(x, 0, z, 'pearlescent_froglight')
    column(b, edge(foot), 1, 3, 'purpur_block')
    put(b, edge(foot), 1, 'end_stone_bricks')
    for x, z in edge(foot):
        if abs(x - c) + abs(z - c) == 5:
            for y in (1, 2, 3):
                b.set(x, y, z, 'purpur_pillar', axis='y')
    lip(b, foot, 4)
    # ---- the shaft, with stacked little lids: a glowing gap course under a lip every eight blocks
    column(b, edge(shaft), 4, TOP - 1, 'purpur_block')
    for y in (10, 17):
        band(b, edge(shaft), y, y, every=2)
        lip(b, octo(c, c, 3, k=4), y + 1)
    # slit windows on the faces
    for y in (6, 7, 13, 14, 20, 21):
        for d, (dx, dz) in DIRS4.items():
            b.set(c + 2 * dx, y, c + 2 * dz, 'magenta_stained_glass_pane')
    # ---- the central column: purpur pillar with a froglight every few blocks to light the stair
    for y in range(1, TOP):
        b.set(c, y, c, 'pearlescent_froglight' if y % 4 == 2 else 'purpur_pillar', axis='y')
    # ---- the spiral: every cell a step (eight a turn), so a 2.6-block Shulkin always clears the turn above
    for x, z in ring8:
        b.set(x, 0, z, 'purpur_block')
    put(b, shaft, TOP, 'purpur_block')     # the lantern room floor (the stair cuts its way up through it)
    start = ring8.index((c, c - 1))
    path = [ring8[(start + k) % 8] for k in range(TOP)]
    stair_path(b, path, 1, landings=False, clear=4)
    # the door: a deep doorway through the foot and the shaft wall into the bottom of the spiral
    b.door(c, 1, 0, facing='north')
    air(b, {(c, 0)}, 3, 3)
    air(b, {(c, 1)}, 1, 3)
    b.set(c - 1, 3, 0, 'end_stone_brick_stairs', facing='east', half='top')
    b.set(c + 1, 3, 0, 'end_stone_brick_stairs', facing='west', half='top')
    # ---- the lantern room: walls of magenta glass, a great froglight lamp in the middle
    for y in range(TOP + 1, TOP + 5):
        put(b, edge(shaft), y, 'magenta_stained_glass')
        for x, z in edge(shaft):
            if abs(x - c) + abs(z - c) == 3:      # the clipped corners glow: froglight mullions
                b.set(x, y, z, 'pearlescent_froglight')
    for y in range(TOP + 1, TOP + 4):
        b.set(c, y, c, 'pearlescent_froglight')
    b.end_rod(c, TOP + 4, c, 'up')
    b.spot('work', c, TOP + 1, c - 1)
    # the gallery ledge outside the glass (a lid lip)
    lip(b, octo(c, c, 3, k=4), TOP)
    # ---- the lid over the lantern, and the crown of end rods
    lid = octo(c, c, 3, k=4)
    lip(b, lid, TOP + 5)
    put(b, lid - edge(lid), TOP + 5, 'purpur_block')
    tops = {cell: TOP + 6 + min(i, 1) for cell, i in rings(lid).items()}
    stair_roof(b, tops, {cell: TOP + 6 for cell in lid})
    # the crown: a ring of rods round a two-block spire, one more rod on top, rods pointing out
    for x, z in rect(c - 1, c - 1, c + 1, c + 1):
        b.end_rod(x, TOP + 7, z, 'up')
    b.set(c, TOP + 7, c, 'purpur_pillar', axis='y')
    b.set(c, TOP + 8, c, 'purpur_pillar', axis='y')
    b.end_rod(c, TOP + 9, c, 'up')
    for d, (dx, dz) in DIRS4.items():
        b.end_rod(c + 2 * dx, TOP + 7, c + 2 * dz, d)


# ===================================================================================== Weavers' Loft
@building('weavers_loft', people='shulkin', role='work', size=(11, 17, 11), door=5, job='weaver',
          about='A square workshop of looms under a tall octagonal tent of a lid; its gap is an open drying loft '
                'where void cloth and dyed wool hang, banners flying from the posts.')
def weavers_loft(b):
    c = 5
    body_plan = rect(1, 1, 9, 9)
    inner = shrink(body_plan)
    lid_plan = octo(c, c, 5, k=7)
    LOFT = 5                                 # loft floor
    UNDER = 10                               # lid underside
    # ---- ground, plinth, body
    for x in range(11):
        for z in range(11):
            b.set(x, 0, z, 'end_stone_bricks')
    put(b, inner, 0, 'purpur_block')
    for x, z in ((0, 0), (10, 0), (0, 10), (10, 10)):
        b.set(x, 0, z, 'pearlescent_froglight')
    column(b, edge(body_plan), 1, LOFT - 1, 'purpur_block')
    put(b, edge(body_plan), 1, 'end_stone_bricks')
    posts = {(1, 1), (9, 1), (1, 9), (9, 9), (c, 1), (c, 9), (1, c), (9, c)}
    for x, z in posts:
        for y in range(1, UNDER):
            b.set(x, y, z, 'purpur_pillar', axis='y')
    # a stair cornice where the body meets the loft
    for x, z in edge(body_plan):
        if (x, z) not in posts:
            d = facing_out(body_plan, x, z)
            dx, dz = DIRS4[d]
            if b.inside(x + dx, LOFT, z + dz):
                b.set(x + dx, LOFT, z + dz, 'purpur_stairs', facing=OPP[d], half='top')
    put(b, body_plan, LOFT, 'purpur_block')
    # windows
    for x, z in ((1, 3), (1, 7), (9, 3), (9, 7), (3, 9), (7, 9)):
        for y in (2, 3):
            b.set(x, y, z, 'magenta_stained_glass_pane')
    # ---- the loft: the shell's gap left open, a railing round it, banners flying from the posts
    for x, z in edge(body_plan):
        if (x, z) not in posts:
            b.set(x, LOFT + 1, z, 'magenta_stained_glass_pane')
    for x, z in posts:
        if (x, z) in ((1, 1), (9, 1), (1, 9), (9, 9)):
            b.end_rod(x, UNDER, z, 'up')     # the square's corners poke out past the turned lid: lamps on them
            continue
        d = facing_out(body_plan, x, z)
        dx, dz = DIRS4[d]
        b.set(x + dx, UNDER - 1, z + dz, ('purple_wall_banner' if (x + z) % 2 else 'magenta_wall_banner'), facing=d)
    # ---- the lid: an octagonal tent turned against the square body, lit from beneath
    lip(b, lid_plan, UNDER)
    put(b, lid_plan - edge(lid_plan), UNDER, 'purpur_block')
    tops = {cell: UNDER + 1 + min(i, 4) for cell, i in rings(lid_plan).items()}
    stair_roof(b, tops, {cell: UNDER + 1 for cell in lid_plan})
    peak = max(tops.values())
    b.set(c, peak, c, 'purpur_pillar', axis='y')
    b.set(c, peak + 1, c, 'end_rod', facing='up')
    for x, z in ((c - 2, c - 2), (c + 2, c - 2), (c - 2, c + 2), (c + 2, c + 2), (c, c)):
        b.set(x, UNDER, z, 'pearlescent_froglight')
    # ---- the door
    doorway(b, c, 1, 1, 'north')
    # ---- stairs up the east wall to the loft
    path = [(8, 7), (8, 6), (8, 5), (8, 4), (8, 3)]
    stair_path(b, path, 1)
    for z in (3, 4, 5, 6):
        b.set(7, LOFT + 1, z, 'magenta_stained_glass_pane')
    # ---- the workshop: looms (the weaver's at the west wall), bolts of cloth, a dye vat
    b.set(2, 1, 4, 'loom', facing='east')
    b.spot('work', 3, 1, 4)
    b.set(2, 1, 6, 'loom', facing='east')
    b.set(4, 1, 8, 'loom', facing='north')
    for x, z, w in ((2, 8, 'purple_wool'), (2, 7, 'magenta_wool'), (3, 8, 'black_wool'), (6, 8, 'white_wool')):
        b.set(x, 1, z, w)
    b.set(2, 2, 8, 'purple_wool')
    b.set(2, 1, 2, 'cauldron')
    b.set(3, 1, 2, 'barrel', facing='up', open=False)
    b.set(7, 1, 2, 'chest', facing='south', type='single', waterlogged=False)
    b.fill(4, 1, 4, 6, 1, 6, 'purple_carpet')
    b.set(5, 1, 5, 'magenta_carpet')
    b.set(6, 1, 6, 'purpur_stairs', facing='east')
    b.spot('sit', 6, 1, 6)
    hang(b, 4, 4, 3)
    hang(b, 4, 4, 7)
    b.end_rod(2, 4, c, 'east')
    # ---- the loft: drying cloth, bales of wool, a seat to sort it
    for x, z in ((2, 2), (2, 3), (3, 2)):
        b.set(x, LOFT + 1, z, 'magenta_wool')
    b.set(2, LOFT + 2, 2, 'purple_wool')
    for x, z in ((2, 8), (3, 8), (2, 7)):
        b.set(x, LOFT + 1, z, 'black_wool')
    b.fill(4, LOFT + 1, 4, 6, LOFT + 1, 7, 'white_carpet')
    b.set(5, LOFT + 1, 8, 'loom', facing='north')
    b.set(4, LOFT + 1, 8, 'purpur_stairs', facing='south')
    b.spot('sit', 4, LOFT + 1, 8)


# ===================================================================================== Shellwright
@building('shellwright', people='shulkin', role='work', size=(13, 12, 11), door=4, job='shellwright',
          about="The Shellwright's workshop: a small domed shell of a shop beside a yard where purpur is cut, "
                'under a lid lifted clear onto pillars; stonecutters, a smithing table and stacks of stock.')
def shellwright(b):
    shop = octo(4, 5, 3, 4, k=6)             # x 1..7, z 1..9
    sc = (4, 5)
    canopy = rect(9, 0, 12, 10)
    # ---- ground: purpur inside the shop, end stone bricks in the yard
    for x in range(13):
        for z in range(11):
            b.set(x, 0, z, 'end_stone_bricks')
    put(b, shrink(shop), 0, 'purpur_block')
    for x, z in ((0, 0), (0, 10), (12, 10)):
        b.set(x, 0, z, 'pearlescent_froglight')
    # ---- the shop: a little shell (walls, gap, domed lid)
    column(b, edge(shop), 1, 4, 'purpur_block')
    put(b, edge(shop), 1, 'end_stone_bricks')
    for x, z in edge(shop):
        if abs(x - sc[0]) + abs(z - sc[1]) == 6:
            for y in range(1, 6):
                b.set(x, y, z, 'purpur_pillar', axis='y')
    band(b, edge(shop), 5, 5, every=2, posts={c for c in edge(shop) if abs(c[0] - 4) + abs(c[1] - 5) == 6})
    lid = octo(4, 5, 4, 5, k=8)
    lid = {c for c in lid if c[0] <= 7}
    lip(b, lid, 6)
    put(b, lid - edge(lid), 6, 'purpur_block')
    tops = {cell: 7 + min(i, 4) for cell, i in rings(lid).items()}
    stair_roof(b, tops, {cell: 7 for cell in lid})
    peak = max(tops, key=lambda cell: (tops[cell], -abs(cell[0] - sc[0]) - abs(cell[1] - sc[1])))
    b.end_rod(peak[0], tops[peak] + (1 if b.get(peak[0], tops[peak], peak[1])[0].endswith('slab') else 0), peak[1], 'up')
    # windows
    for x, z in ((1, 4), (1, 6), (4, 9)):
        for y in (2, 3):
            b.set(x, y, z, 'magenta_stained_glass_pane')
    # ---- the door
    doorway(b, 4, 1, 1, 'north')
    # ---- the yard: a lid lifted onto five pillars, a low wall round the back
    for x, z in ((9, 0), (12, 0), (9, 10), (12, 10), (12, 5)):
        for y in range(1, 5):
            b.set(x, y, z, 'purpur_pillar', axis='y')
        b.set(x, 0, z, 'end_stone_bricks')
    lip(b, canopy, 5)
    put(b, canopy - edge(canopy), 5, 'purpur_block')
    for x, z in edge(canopy):
        d = facing_out(canopy, x, z)
        b.set(x, 6, z, 'purpur_stairs', facing=OPP[d], half='bottom')
    put(b, shrink(canopy), 6, 'purpur_slab', type='bottom')
    for x, z in ((10, 3), (10, 7), (10, 5)):
        b.set(x, 5, z, 'pearlescent_froglight')
    for z in range(1, 10):
        if z not in (5,):
            b.set(12, 1, z, 'end_stone_brick_wall')
    for x in range(8, 12):
        b.set(x, 1, 10, 'end_stone_brick_wall')
    # a gap in the shop wall into the yard
    for z in (4, 5):
        for y in (1, 2, 3):
            b.set(7, y, z, 'air')
    b.set(7, 3, 4, 'purpur_stairs', facing='south', half='top')
    b.set(7, 3, 5, 'purpur_stairs', facing='north', half='top')
    # ---- in the yard: stonecutters (the shellwright's by the shop), a smithing table, stacks of purpur stock
    b.set(9, 1, 2, 'stonecutter', facing='north')
    b.spot('work', 9, 1, 3)
    b.set(11, 1, 2, 'stonecutter', facing='north')
    b.set(10, 1, 8, 'smithing_table')
    b.set(11, 1, 8, 'grindstone', face='floor', facing='north')
    # stock: blocks, pillars laid on their sides, slabs
    for x, z, h in ((11, 6, 2), (11, 7, 1), (10, 7, 1)):
        for y in range(1, 1 + h):
            b.set(x, y, z, 'purpur_block')
    b.set(11, 3, 6, 'purpur_slab', type='bottom')
    for z in (3, 4):
        b.set(11, 1, z, 'purpur_pillar', axis='z')
    b.set(11, 2, 3, 'purpur_pillar', axis='z')
    b.set(8, 1, 9, 'end_stone_bricks')
    b.set(9, 1, 9, 'end_stone')
    b.set(9, 2, 9, 'chorus_flower', age=5)
    b.set(8, 2, 9, 'purpur_stairs', facing='west')
    b.chest(10, 1, 9, facing='north')
    b.set(9, 1, 5, 'purpur_stairs', facing='west')
    b.spot('sit', 9, 1, 5)
    hang(b, 9, 4, 6)
    # ---- in the shop: a counter, shelves of finished pieces, storage
    for x in (2, 3):
        b.set(x, 1, 5, 'purpur_slab', type='top')
    b.candles(2, 2, 5, 3, 'magenta')
    b.set(2, 1, 8, 'barrel', facing='up', open=False)
    b.set(3, 1, 8, 'barrel', facing='up', open=False)
    b.set(2, 2, 8, 'barrel', facing='up', open=False)
    b.set(5, 1, 8, 'stonecutter', facing='west')
    b.set(6, 1, 8, 'purpur_stairs', facing='west', half='top')
    b.set(6, 2, 8, 'purpur_slab', type='bottom')
    b.set(3, 1, 6, 'purpur_stairs', facing='west')
    b.spot('sit', 3, 1, 6)
    hang(b, 4, 4, 4)
    hang(b, 4, 4, 7)


# ==================================================================================== Driftray Roost
@building('driftray_roost', people='shulkin', role='work', size=(13, 13, 13), door=6, job='wayfinder', rim=True,
          about="An open perch for Driftrays at the islet's edge: a broad deck (the lid) over a squat pier (the "
                "body) with a glowing gap between, railed at the sides and open at the back to the void, "
                "end-rod landing posts, chorus to tempt the rays, and the Wayfinder's little shell of a shelter.")
def driftray_roost(b):
    c = 6
    DECK = 4                                  # deck floor layer (walk at DECK + 1)
    pier = octo(c, c + 1, 4)                  # x 2..10, z 3..11
    deck = octo(c, c, 6)                      # the whole footprint, corners clipped
    # ---- ground and the pier (the body), a glowing gap under the deck (the lid)
    for x in range(13):
        for z in range(13):
            b.set(x, 0, z, 'end_stone_bricks')
    column(b, pier, 1, DECK - 1, 'end_stone_bricks')
    for x, z in edge(pier):
        if abs(x - c) + abs(z - c - 1) == 6:
            b.set(x, 1, z, 'purpur_pillar', axis='y')
    band(b, edge(pier), DECK - 1, DECK - 1, every=2)
    put(b, deck, DECK, 'purpur_block')
    for (x, z), i in rings(deck).items():
        if i == 0:
            b.set(x, DECK, z, 'purpur_stairs', facing=OPP[facing_out(deck, x, z)], half='top')
        elif i >= 2 and (x + z) % 2 == 0:
            b.set(x, DECK, z, 'purpur_pillar', axis='y')
    # the outer ring is the walkable lip: slabs make a smooth floor over the stair moulding
    for x, z in edge(deck):
        b.set(x, DECK, z, 'purpur_stairs', facing=OPP[facing_out(deck, x, z)], half='top')
    # ---- the way up: a stair from the front, cut through the deck's edge
    path = [(c, 0), (c, 1), (c, 2), (c, 3)]
    stair_path(b, path, 1)
    b.set(c, 0, 0, 'end_stone_bricks')
    # ---- railings down the sides with lamp posts; the back (over the void) left open for landing
    rail = set()
    for x, z in edge(deck):
        if z >= 10 or (x == c and z <= 4):
            continue
        rail.add((x, z))
        b.set(x, DECK + 1, z, 'end_stone_brick_wall')
    for x, z in rail:
        if abs(x - c) + abs(z - c) in (7, 8) and (x + z) % 3 == 0:
            b.end_rod(x, DECK + 2, z, 'up')
    for x in (c - 1, c + 1):
        b.set(x, DECK + 1, 0, 'end_stone_brick_wall') if (x, 0) in deck else None
        b.end_rod(x, DECK + 2, 0, 'up') if (x, 0) in deck else None
    # landing posts at the open back: tall pillars with rods pointing out over the void
    for x in (2, c, 10):
        z = max(zz for (xx, zz) in deck if xx == x)
        for y in range(DECK + 1, DECK + 5):
            b.set(x, y, z, 'purpur_pillar', axis='y')
        b.end_rod(x, DECK + 5, z, 'up')
        b.end_rod(x, DECK + 4, z + 1, 'south') if b.inside(x, DECK + 4, z + 1) else None
    # ---- on the deck: a lodestone to steer by, a bell to call the rays, chorus to tempt them
    b.set(c, DECK + 1, c + 1, 'lodestone')
    b.set(c, DECK + 2, c + 1, 'end_rod', facing='up')
    b.set(c + 3, DECK + 1, c + 3, 'end_stone')
    b.chorus(c + 3, DECK + 2, c + 3, height=3, rng=random.Random(7))
    b.set(c + 4, DECK + 1, c + 1, 'end_stone')
    b.chorus(c + 4, DECK + 2, c + 1, height=2, rng=random.Random(11))
    b.set(c + 2, DECK + 1, c - 2, 'bell', attachment='floor', facing='north', powered=False)
    b.spot('stand', c, DECK + 1, c + 4)
    b.spot('stand', c + 2, DECK + 1, c + 5)
    # ---- the Wayfinder's shelter: a little shell on the west of the deck, open to the east
    sp = octo(2, c - 1, 2, k=3)               # x 0..4, z 3..7
    column(b, edge(sp), DECK + 1, DECK + 3, 'purpur_block')
    band(b, edge(sp), DECK + 4, DECK + 4, every=2)
    slid = octo(2, c - 1, 3, k=4)
    slid = {cl for cl in slid if b.inside(cl[0], 0, cl[1])}
    lip(b, slid, DECK + 5)
    put(b, slid - edge(slid), DECK + 5, 'purpur_block')
    tops = {cell: DECK + 6 + min(i, 1) for cell, i in rings(slid).items()}
    stair_roof(b, tops, {cell: DECK + 6 for cell in slid})
    b.end_rod(2, DECK + 8, c - 1, 'up')
    for y in range(DECK + 1, DECK + 4):
        b.set(4, y, c - 1, 'air')
    b.set(4, DECK + 3, c - 2, 'purpur_stairs', facing='south', half='top')
    b.set(4, DECK + 3, c, 'purpur_stairs', facing='north', half='top')
    b.set(1, DECK + 1, c - 1, 'cartography_table')
    b.spot('work', 2, DECK + 1, c - 1)
    b.set(2, DECK + 1, c - 2, 'purpur_stairs', facing='north')
    b.spot('sit', 2, DECK + 1, c - 2)
    b.set(2, DECK + 1, c, 'barrel', facing='up', open=False)
    hang(b, 2, DECK + 4, c - 1)
