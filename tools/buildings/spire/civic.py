"""Shulkin civic buildings: the Lamp Court (plaza), the Lid Hall and the Shell Nursery."""
import math
import random

from kit import building

from spire._parts import (DIRS4, OPP, column, doorway, edge, eye, facing_out, hang, heightfield, octo, oval, put, rect,
                          rings, shrink, stair_roof)


# ======================================================================================== Lamp Court
@building('lamp_court', people='shulkin', role='plaza', size=(17, 17, 17), door=8,
          about='The village centre: purpur tiles inlaid with the Eye of the Spires, the great end-rod lamp rising '
                'from its pupil under a little floating lid, benches and chorus planters.')
def lamp_court(b):
    c = 8
    floor = octo(c, c, 8)
    # tiles: an end-stone-brick border, purpur inside with a pillar-top checker
    for x, z in floor:
        b.set(x, 0, z, 'purpur_block' if (x + z) % 2 else 'purpur_pillar', axis='y')
    put(b, edge(floor), 0, 'end_stone_bricks')
    for x in range(17):
        for z in range(17):
            if (x, z) not in floor:
                b.set(x, 0, z, 'end_stone_bricks')
    # the Eye of the Spires, its pupil under the lamp: ivory "old shell" white, purple rim, magenta iris
    eye(b, c, 0, c, half_len=7, half_h=4, iris_r=3, white='quartz_bricks')
    # glowing studs round the court (they keep the whole court lit)
    for x, z in ((c - 7, c), (c + 7, c), (c, c - 7), (c, c + 7), (c - 5, c - 5), (c + 5, c - 5), (c - 5, c + 5),
                 (c + 5, c + 5)):
        b.set(x, 0, z, 'pearlescent_froglight')

    # ---- the lamp: stepped plinth, a pillar shaft with rods, a glowing shell-lamp under a floating lid
    b.set(c, 1, c, 'end_stone_bricks')
    for x, z, f in ((c, c - 1, 'north'), (c, c + 1, 'south'), (c - 1, c, 'west'), (c + 1, c, 'east')):
        b.set(x, 1, z, 'end_stone_brick_stairs', facing=OPP[f])
    for dx, dz in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        b.set(c + dx, 1, c + dz, 'end_stone_brick_slab', type='bottom')
    b.set(c, 2, c, 'purpur_block')
    for y in range(3, 12):
        b.set(c, y, c, 'purpur_pillar', axis='y')
    for y in (5, 8):
        for d, (dx, dz) in DIRS4.items():
            b.end_rod(c + dx, y, c + dz, d)
    # the lamp head: a cage of magenta glass round a froglight heart (a tiny shulker, gap open)
    b.set(c, 12, c, 'purpur_block')
    for x, z in edge(rect(c - 1, c - 1, c + 1, c + 1)):
        b.set(x, 12, z, 'purpur_slab', type='top')
    for y in (13, 14):
        for x, z in rect(c - 1, c - 1, c + 1, c + 1):
            b.set(x, y, z, 'magenta_stained_glass')
    b.set(c, 13, c, 'pearlescent_froglight')
    b.set(c, 14, c, 'pearlescent_froglight')
    for dx, dz in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        b.set(c + dx, 13, c + dz, 'purpur_pillar', axis='y')
        b.set(c + dx, 14, c + dz, 'end_rod', facing='up')
    # the floating lid: held up on four end rods over an open gap
    lid = octo(c, c, 2)
    lid |= rect(c - 2, c - 1, c + 2, c + 1) | rect(c - 1, c - 2, c + 1, c + 2)
    put(b, lid, 15, 'purpur_slab', type='top')
    put(b, rect(c - 1, c - 1, c + 1, c + 1), 16, 'purpur_slab', type='bottom')
    b.set(c, 16, c, 'purpur_block')
    for x, z in edge(lid):
        dx, dz = x - c, z - c
        if abs(dx) == 2 and abs(dz) <= 1 or abs(dz) == 2 and abs(dx) <= 1:
            f = 'east' if dx == 2 else 'west' if dx == -2 else 'south' if dz == 2 else 'north'
            b.set(x, 15, z, 'purpur_stairs', facing=OPP[f], half='top')
    b.set(c, 16, c, 'purpur_pillar', axis='y')

    # ---- benches: corner seats on the four diagonals, facing the lamp
    for sx in (-1, 1):
        for sz in (-1, 1):
            fx = 'east' if sx > 0 else 'west'
            fz = 'south' if sz > 0 else 'north'
            # an L of seats: two along x, one along z, backs to the outside
            for x, z, f in ((c + 4 * sx, c + 5 * sz, fz), (c + 3 * sx, c + 5 * sz, fz), (c + 5 * sx, c + 4 * sz, fx),
                            (c + 5 * sx, c + 3 * sz, fx)):
                b.set(x, 1, z, 'purpur_stairs', facing=f)
                b.spot('sit', x, 1, z)
            # the corner between them: a slab table with candles
            b.set(c + 5 * sx, 1, c + 5 * sz, 'purpur_slab', type='top')
            b.candles(c + 5 * sx, 2, c + 5 * sz, 3, 'magenta')

    # ---- chorus planters at the four corners (end stone soil, end-stone-brick rim, rods at the rim corners)
    for sx in (-1, 1):
        for sz in (-1, 1):
            px, pz = c + 6 * sx, c + 6 * sz
            box = rect(px - 1, pz - 1, px + 1, pz + 1)
            for x, z in box:
                if (x, z) in floor or True:
                    b.set(x, 1, z, 'end_stone_bricks')
            b.set(px, 1, pz, 'end_stone')
            b.set(px - sx, 1, pz - sz, 'end_stone')
            b.chorus(px, 2, pz, height=4, rng=random.Random(px * 31 + pz))
            for x, z in ((px + sx, pz - sz), (px - sx, pz + sz)):
                b.end_rod(x, 2, z, 'up')
    # a stand-and-talk spot by the lamp, facing the door
    b.spot('stand', c, 1, c - 3)


# ========================================================================================== Lid Hall
def _band_rhythm(b, ring, y0, top_of, pillar_cells, every=3):
    """Fill a gap band round ``ring``: pillars where given, otherwise glass with a froglight every few."""
    import math as _m
    cx = sum(c[0] for c in ring) / len(ring)
    cz = sum(c[1] for c in ring) / len(ring)
    order = sorted(ring, key=lambda c: _m.atan2(c[1] - cz, c[0] - cx))
    k = 0
    for x, z in order:
        top = top_of(x, z)
        if (x, z) in pillar_cells:
            for y in range(y0, top + 1):
                b.set(x, y, z, 'purpur_pillar', axis='y')
            k = 0
            continue
        k += 1
        for y in range(y0, top + 1):
            b.set(x, y, z, 'pearlescent_froglight' if k % every == 0 else 'magenta_stained_glass')


@building('lid_hall', people='shulkin', role='civic', size=(21, 18, 17), door=10,
          about='The meeting hall under one enormous lid, tilted open toward the plaza over a tall glowing gap; '
                'records are read aloud from the lectern on its dais.')
def lid_hall(b):
    cx = 10
    body_plan = octo(cx, 8, 8, 6, k=11)      # x 2..18, z 2..14
    inner = shrink(body_plan)
    lid_plan = octo(cx, 8, 10, 8, k=15)      # the whole footprint, corners chamfered

    def under(z):
        """The lid's underside: high at the front (open toward the plaza), low at the back hinge."""
        return 7 + round((16 - z) / 4)

    # ---- floor: an end-stone-brick terrace under the overhang, purpur tiles inside
    for x, z in lid_plan:
        b.set(x, 0, z, 'end_stone_bricks')
    for x, z in inner:
        b.set(x, 0, z, 'purpur_block' if (x + z) % 2 else 'purpur_pillar', axis='y')
    for x in range(21):
        for z in range(17):
            if (x, z) not in lid_plan:
                b.set(x, 0, z, 'end_stone_bricks')
    # ---- the body: purpur walls with pillars at the turns and every few blocks along the sides
    ring = edge(body_plan)
    column(b, ring, 1, 5, 'purpur_block')
    # posts carry the lid: the chamfered corners, the portal, the middle of each side
    posts = {(x, z) for (x, z) in ring if abs(x - cx) + abs(z - 8) == 11}
    posts |= {(cx - 2, 2), (cx + 2, 2), (cx - 2, 14), (cx + 2, 14), (2, 8), (18, 8)}
    for x, z in posts:
        for y in range(1, 6):
            b.set(x, y, z, 'purpur_pillar', axis='y')
    # ---- the gap: a glowing band from the wall top up to the tilted lid, pillars carrying the lid
    _band_rhythm(b, ring, 6, lambda x, z: under(z) - 1, posts, every=3)
    # ---- the lid: tilted, domed, a moulded lip all round
    # a box lid like a shulker's: straight sides, a gentle dome, every top a slab (nothing spawns up there)
    depth = rings(lid_plan)
    thick = (5, 7, 7, 9, 9, 11)  # half blocks, by ring from the rim inward
    cols = {}
    for (x, z), i in depth.items():
        lo = 2 * under(z)
        cols[(x, z)] = (lo, lo + thick[min(i, len(thick) - 1)])
    heightfield(b, cols)
    for x, z in edge(lid_plan):
        d = facing_out(lid_plan, x, z)
        b.set(x, under(z), z, 'purpur_stairs', facing=OPP[d], half='top')
    # a crest along the ridge, like the crest on a Shulkin's lid, with end rods to light the roof
    for z in range(4, 14):
        lo, hi = cols[(cx, z)]
        top = (hi - 1) // 2
        b.set(cx, top, z, 'purpur_pillar', axis='z')
        b.set(cx, top + 1, z, 'purpur_slab', type='bottom')
        if z in (4, 9, 13):
            b.end_rod(cx, top + 2, z, 'up')
    for x, z in ((4, 8), (16, 8)):
        lo, hi = cols[(x, z)]
        b.end_rod(x, (hi + 1) // 2, z, 'up')
    # ---- the front: porch under the raised lid, a tall door between windows and benches
    doorway(b, cx, 1, 2, 'north')
    for x in (cx - 2, cx + 2):
        for y in range(1, 6):
            b.set(x, y, 2, 'purpur_pillar', axis='y')
    for x in (cx - 4, cx + 4):
        b.set(x, 4, 1, 'purple_wall_banner', facing='north')
    for x in (cx - 3, cx + 3):
        b.end_rod(x, 4, 1, 'north')
    for x in (cx - 6, cx - 5, cx + 5, cx + 6):
        b.set(x, 1, 1, 'purpur_stairs', facing='south')
        b.spot('sit', x, 1, 1)
    for x, z in ((1, 1), (19, 1), (1, 15), (19, 15)):
        b.set(x, 0, z, 'pearlescent_froglight')
    # lanterns hung from the lid over the porch and the side walks
    for x, z in ((cx - 4, 0), (cx + 4, 0), (cx, 0), (0, 8), (20, 8)):
        top = under(z) - 1
        b.set(x, top, z, 'iron_chain', axis='y')
        hang(b, x, top - 1, z)
    # side and back windows
    for z in (6, 7, 9, 10):
        for y in (2, 3, 4):
            b.set(2, y, z, 'magenta_stained_glass_pane')
            b.set(18, y, z, 'magenta_stained_glass_pane')

    # ---- inside: the dais at the back with the reading lectern, two elders' seats, the archive wall
    for x, z in inner:
        if z >= 11:
            b.set(x, 1, z, 'purpur_block')
    for x in range(6, 15):
        b.set(x, 1, 10, 'purpur_stairs', facing='south')
    b.set(5, 1, 10, 'purpur_slab', type='bottom')
    b.set(15, 1, 10, 'purpur_slab', type='bottom')
    b.set(cx, 2, 12, 'lectern', facing='south', has_book=False, powered=False)
    b.spot('stand', cx, 2, 13)
    for x in (cx - 2, cx + 2):
        b.set(x, 2, 13, 'purpur_stairs', facing='south')
        b.spot('sit', x, 2, 13)
    for x in (5, 6, 14, 15):
        b.set(x, 2, 13, 'bookshelf')
        b.set(x, 3, 13, 'chiseled_bookshelf', facing='north')
    for x in (7, 13):
        b.set(x, 2, 13, 'purpur_slab', type='top')
        b.candles(x, 3, 13, 4, 'magenta')
    # the Eye window above the dais
    for x, y in ((cx - 1, 3), (cx, 3), (cx + 1, 3), (cx - 2, 4), (cx + 2, 4), (cx - 1, 5), (cx, 5), (cx + 1, 5)):
        b.set(x, y, 14, 'purple_stained_glass_pane')
    for x, y in ((cx - 1, 4), (cx + 1, 4)):
        b.set(x, y, 14, 'magenta_stained_glass_pane')
    b.set(cx, 4, 14, 'pearlescent_froglight')
    for x in (6, 14):
        b.set(x, 5, 13, 'purple_wall_banner', facing='north')
    # ---- rows of seats facing the dais, an aisle down the middle from the door
    for z in (6, 8):
        for x in list(range(4, 9)) + list(range(12, 17)):
            b.set(x, 1, z, 'purpur_stairs', facing='north')
            b.spot('sit', x, 1, z)
    # the Eye of the Spires inlaid in the foyer
    eye(b, cx, 0, 4, half_len=6, half_h=2, iris_r=1, white='quartz_bricks')
    # banners and rods on the side walls
    for z in (5, 8, 11):
        b.set(3, 4, z, 'magenta_wall_banner', facing='east') if z != 8 else b.end_rod(3, 5, z, 'east')
        b.set(17, 4, z, 'magenta_wall_banner', facing='west') if z != 8 else b.end_rod(17, 5, z, 'west')
    # lanterns on chains from the lid over the seats and the dais
    for x, z in ((6, 5), (14, 5), (6, 9), (14, 9), (cx, 7), (cx - 3, 12), (cx + 3, 12)):
        top = under(z) - 1
        b.set(x, top, z, 'iron_chain', axis='y')
        b.set(x, top - 1, z, 'iron_chain', axis='y')
        hang(b, x, top - 2, z)


# ===================================================================================== Shell Nursery
def _ray(origin, angle_deg, plan, start=1.5):
    """Cells along a straight ray from ``origin`` (z grows to the south; angle 0 points north)."""
    out = []
    a = math.radians(angle_deg)
    t = start
    while t < 40:
        cell = (round(origin[0] + t * math.sin(a)), round(origin[1] - t * math.cos(a)))
        if cell in plan and cell not in out:
            out.append(cell)
        t += 0.25
    return out


@building('shell_nursery', people='shulkin', role='civic', size=(17, 12, 15), door=8,
          about='A low, wide shell where the soft-shelled children are raised: a scallop-ribbed lid fanning from '
                'a hinge at the back, a glowing gap, empty shells (purple shulker boxes) round the walls, '
                'soft carpets and a glowing nest.')
def shell_nursery(b):
    cx, cz = 8, 7
    body_plan = oval(cx, cz, 6, 5)          # x 2..14, z 2..12
    inner = shrink(body_plan)
    lid_plan = oval(cx, cz, 7, 6)           # one block of overhang
    hinge = (cx, 14.2)                      # the ribs fan out from the back, like a scallop

    def under(z):
        """The lid opens like a clam: shut at the hinge (back), gaping at the front."""
        return 4 + round((13 - z) * 3 / 12)

    # ---- floor: an end-stone-brick veranda under the overhang, purpur inside
    for x in range(17):
        for z in range(15):
            b.set(x, 0, z, 'end_stone_bricks')
    for x, z in inner:
        b.set(x, 0, z, 'purpur_block')
    # ---- body: low purpur walls on an end-stone-brick course, the glowing gap all round
    ring = edge(body_plan)
    column(b, ring, 1, 3, 'purpur_block')
    put(b, ring, 1, 'end_stone_bricks')
    posts = {(x, z) for (x, z) in ring if abs(x - cx) == 6 and z == cz} | {(cx - 3, 2), (cx + 3, 2)}
    _band_rhythm(b, ring, 4, lambda x, z: under(z) - 1, posts, every=2)
    # ---- the lid: a low scallop (slab-topped), ribs one block proud fanning from the hinge
    depth = rings(lid_plan)
    ribs = set()
    for ang in (-60, -30, 0, 30, 60):
        ribs |= {c for c in _ray(hinge, ang, lid_plan) if depth[c] >= 1}
    tops, bottoms = {}, {}
    for (x, z), i in depth.items():
        # a gently domed top tilted with the lid, stair-smoothed
        plane = 4 + (13 - z) * 3 / 12
        bulge = 2.4 * math.sqrt(max(0.0, 1 - ((x - cx) / 7.6) ** 2 - ((z - cz) / 6.6) ** 2))
        bottoms[(x, z)] = under(z)
        tops[(x, z)] = max(round(plane + 1.6 + bulge), under(z) + 2)
    stair_roof(b, tops, bottoms)
    cols = {c: (2 * bottoms[c], 2 * tops[c]) for c in tops}
    # the ribs: pillar ridges, a slab proud of the shell, fanning from the hinge
    for x, z in ribs:
        t = tops[(x, z)]
        b.set(x, t - 1, z, 'purpur_pillar', axis='y')
        b.set(x, t, z, 'purpur_slab', type='bottom')
    for x, z in edge(lid_plan):
        d = facing_out(lid_plan, x, z)
        b.set(x, under(z), z, 'purpur_stairs', facing=OPP[d], half='top')
    # the hinge boss where the ribs meet, a rod on top; one more rod at the crown
    hz = 12
    top = (cols[(cx, hz)][1] + 1) // 2
    b.set(cx, top, hz, 'purpur_block')
    b.end_rod(cx, top + 1, hz, 'up')
    for x in (cx - 1, cx + 1):
        b.set(x, top, hz, 'purpur_stairs', facing='east' if x < cx else 'west')
    b.end_rod(cx, (cols[(cx, cz - 1)][1] + 1) // 2, cz - 1, 'up')

    # ---- entrance under the overhang, lamp posts either side
    doorway(b, cx, 1, 2, 'north')
    for x in (cx - 3, cx + 3):
        b.set(x, 1, 1, 'end_stone_brick_wall')
        b.end_rod(x, 2, 1, 'up')
    # little windows
    for x, z in ((2, cz - 1), (2, cz + 1), (14, cz - 1), (14, cz + 1), (cx - 3, 12), (cx + 3, 12)):
        b.set(x, 2, z, 'magenta_stained_glass_pane')
    for x, z in ((1, 3), (15, 3), (1, 11), (15, 11)):
        b.set(x, 0, z, 'pearlescent_froglight')

    # ---- inside: a soft floor in rings of carpet, a glowing nest in the middle
    for (x, z), i in rings(inner).items():
        b.set(x, 1, z, ('purple_carpet', 'magenta_carpet', 'pink_carpet', 'white_carpet', 'pink_carpet')[min(i, 4)])
    # the nest: a ring of white wool cushions round a glowing floor, where the young ones curl up
    for x, z in edge(rect(cx - 1, cz - 1, cx + 1, cz + 1)):
        if (x, z) != (cx, cz - 1):
            b.set(x, 1, z, 'white_wool_slab', type='bottom')
    b.set(cx, 0, cz, 'pearlescent_froglight')
    b.set(cx, 1, cz, 'white_carpet')
    # empty shells along the walls: the Shulkin believe shulkers are their ancestors
    for x, z in edge(inner):
        dx = x - cx
        if z <= 3 and abs(dx) <= 3:
            continue  # keep the doorway clear
        if (x + z) % 2 == 0 and (x, z) not in ((cx, 11),):
            b.set(x, 1, z, 'purple_shulker_box', facing='up')
    # a reading corner (the young learn their records early), caretakers' seats by the door
    b.set(cx, 1, 11, 'lectern', facing='north', has_book=False, powered=False)
    b.spot('stand', cx, 1, 10)
    for x in (cx - 2, cx + 2):
        b.set(x, 1, 3, 'purpur_stairs', facing='north')
        b.spot('sit', x, 1, 3)
    for x in (cx - 1, cx + 1):
        b.set(x, 1, 11, 'purpur_slab', type='top')
        b.candles(x, 2, 11, 3, 'pink')
    b.spot('stand', cx - 3, 1, cz)
    b.spot('stand', cx + 3, 1, cz)
    # light: lanterns hung from the lid
    for x, z in ((cx - 3, cz - 2), (cx + 3, cz - 2), (cx - 3, cz + 2), (cx + 3, cz + 2)):
        hang(b, x, 4, z)
