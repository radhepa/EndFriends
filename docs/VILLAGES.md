# End villages: buildings and layouts

The peoples are in `PEOPLE.md`. This document covers where they live: the 44 buildings, how a
village is laid out, and how it is built into the world. Everything here is implemented: the
villages generate in the outer End (structure type `endexpansion:village`), with their residents.

## How an End village sits in the world

- **Outer islands only.** A village needs land at its centre (at least 60% of the ground within
  12 blocks) and keeps more than 1,000 blocks from the Dragon's island. It sits at the median height
  of the ground round its centre (between y 40 and 120).
- **It brings its own ground.** Every building stands on its own floating **islet**: an end-stone
  top with a rough, tapering underside and a few hanging spikes. Where an islet overlaps the real
  island it merges into it; past the rim it floats over the void. Old terrain above an islet is
  cleared, so hills never bury a house.
- **Paths and bridges.** Paths run from every door to the village centre, three blocks wide, preferring
  land and straight runs and joining each other. Where a path leaves the land it becomes a bridge with
  rails on a ledge either side and lamps on the rails. Islets sit at different heights (Spires up to
  8 blocks above the centre); paths climb with stairs.
- **Nothing wild grows in a village.** Wild chorus and the small floating islands of the outer End
  skip village ground, so doorways and paths stay clear. Planted chorus is part of the buildings.
- **No beds.** Beds explode in the End. Shulkin sleep curled in lidded niches; Chorrin in nests of
  woven chorus fibre; Endarchs and Endermen do not sleep.
- **Always lit.** Endermen spawn in the dark, so every walkable space, roof and path is lit: end rods
  for the Shulkin, pearlescent froglights, lanterns and candles for the Chorrin, end rods and crying
  obsidian for the Court.
- **Sized for the people.** Shulkin are 2.6 blocks tall: their doors have an open block above, rooms
  have at least 3 clear blocks and floors are joined by stairs (mobs don't climb ladders). Endarchs are
  3.4-3.8 tall: Court doorways are at least 4 high and ceilings at least 5.

## Mix and size

| Kind | Who | Share | Residents | Footprint |
|---|---|---|---|---|
| **Spire** | Shulkin | 40% | 9-11 | about 85-110 blocks across |
| **Stead** | Chorrin | 40% | 10-13 | about 75-95 |
| **Crossing** | both | 20% | 16-20 | about 105 |
| **Citadel** | the Court | rare, placed apart | 22 (a Lord, 4 Voidmarshals in their roles, 9 Riftguards, 5 thralls, 3 hounds) | 101 x 110 |

Villages share one placement grid (`endexpansion:villages`: every 24 chunks, at least 9 apart, kept
4 chunks from End cities). Citadels have their own sparse grid (every 64 chunks, at least 24 apart,
kept 6 chunks from villages). Find them with `/locate structure endexpansion:spire_village`,
`stead_village`, `crossing` or `citadel`.

## Palettes

| People | Main | Accents | Light | Doors |
|---|---|---|---|---|
| Shulkin (Spires) | purpur block, pillar, stairs, slabs | end stone brick plinths, magenta glass, purple and magenta cloth | end rods | crimson (it reads as magenta) |
| Chorrin (Steads) | end stone, end stone bricks (stairs, slabs, walls) | planted chorus, woven cloth in purple, white and brown wool, traded purpur | pearlescent froglights, lanterns, candles | pale oak, framed as round arches |
| Court (Citadels) | obsidian, polished blackstone bricks | crying obsidian, purpur pillars, magenta glass, iron chains, end portal frames with eyes as the Court's "eyes" | end rods, crying obsidian | open pointed arches |

The End has no trees, so wood is a rare import: doors, a few shelves and signs, nothing structural.

## Shulkin Spire

Purpur towers on separate islets at different heights, joined by railed bridges. Every Shulkin
building echoes a shulker's shell: a body, the glowing magenta **gap** where the shell opens, and an
overhanging **lid**.

| Building | Size | Role | Lives / works | |
|---|---|---|---|---|
| Lamp Court | 17x17x17 | plaza | | Purpur tiles inlaid with the Eye of the Spires; the end-rod lamp rises from its pupil under a floating lid; benches and chorus planters. |
| Lid Hall | 21x18x17 | civic | | One enormous lid tilted open toward the plaza over a tall glowing gap; a lectern on a dais, rows of seats. |
| Shell Nursery | 17x12x15 | civic | | A scallop shell gaping at the front; soft carpet rings, a glowing nest, purple shulker boxes as empty shells. |
| Archive | 13x26x13 | work | Archivist | Three stacked shells: reading room, stacks round a central column of shelves, records vault. |
| Lamp Tower | 7x34x7 | work | Lamplighter | The tallest: a spiral stair to a magenta lantern room and a crown of end rods. Always on a high islet. |
| Weaver's Loft | 11x17x11 | work | Weaver | Looms under an octagonal tent lid; the gap is an open drying loft flying banners. |
| Shellwright's Workshop | 13x12x11 | work | Shellwright | A small domed shop beside a yard under a lid lifted onto pillars; stonecutters, purpur stock. |
| Driftray Roost | 13x13x13 | work | Wayfinder | A railed deck over a squat pier, open at the back over the void for landing Driftrays. |
| Spire home | 11x24x11 | home | 2 | A drum with buttresses carrying a domed lid, two lidded sleeping niches. |
| Tall spire home | 11x30x11 | home | 3 | Two stacked shells; the lower lid is a railed balcony. |
| Twin spires | 25x28x11 | home | 4 | Two towers joined by an entry hall and an enclosed sky bridge. |

## Chorrin Stead

Low end-stone domes half sunk into one lumpy island grown along the paths, round arched doors, chorus
on every roof.

| Building | Size | Role | Lives / works | |
|---|---|---|---|---|
| Hum Circle | 17x17x17 | plaza | | Eight standing stones round a circle sunk one step, a great chorus in the middle, stepped seats. |
| Popping Kiln | 11x15x12 | work | Kiln-keeper | A beehive kiln with a smoking chimney, furnaces round a campfire, a porch of chorus-fruit barrels. |
| Grove Terraces | 15x11x13 | work | Grove-tender | Three stepped beds of planted chorus with a stair up the middle. |
| Groveback Pen | 15x7x13 | work | | A round walled pasture with a pale oak gate, a feeding trough and a lean-to. |
| Brewhouse | 11x13x12 | work | Brewer | A dome sunk one step with a lantern cupola; brewing stands round a cauldron over a sunken fire. |
| Stonecutter's Yard | 13x9x11 | work | Stonecutter | Stacks of cut bricks, a lifting frame, a half dome sheltering the stonecutters. |
| Cook's Hearth | 13x14x13 | civic | Cook | A dome on eight posts, open all round, over the communal oven; long low tables and cushions. |
| Blinker's Post | 9x17x10 | work | Blinker | A tiny dome hut with a tall purpur mast, courier banners and message barrels. |
| Dome home | 11x12x12 | home | 2 | Half sunk, steps down to a round door, two fibre nests. |
| Large dome home | 16x14x14 | home | 4 | A big dome with a sprout dome budding off its side. |
| Paired domes | 21x12x13 | home | 5 | Two domes joined by a vaulted hall round a sunken court. |

## Crossing

A spire quarter and a stead quarter on either side of one shared market, built from both peoples'
sets plus:

| Building | Size | Role | Lives / works | |
|---|---|---|---|---|
| The Market | 23x12x23 | plaza | | Purpur and end stone meeting in a swirl round a chorus-wrapped shell lamp; four striped tent stalls. |
| Crossing Hall | 21x18x19 | civic | 2 keepers (one Shulkin, one Chorrin) | A lidded tower and a half-sunk dome side by side, a double door, a common room with long tables and a shared hearth. |
| Trade stalls | 7x7x5, 7x6x5 | work | a trader each | One purpur under a striped awning, one end stone with chorus flowering on its roof. |

## Citadel

A square black fortress (side 22 + 9k blocks; the layouts use k = 7, 85 blocks) on one great square
islet, walls of nine-block bays between four corner towers, the Gate of Eyes in the north wall and a
royal causeway out over the void. Inside: a dark-paved court with the Court's eye in crying obsidian.

| Building | Size | Role | |
|---|---|---|---|
| Gate of Eyes | 27x32x11 | gate | A three-order pointed portal ringed with eyes, the Herald's balcony over a 5-wide tunnel. Takes the place of three wall bays. |
| Wall bay, corner tower | 9x15x5, 11x34x11 | wall | Battered obsidian, glowing slits, machicolations, eyes in the crenels; a lit wall-walk all the way round (floor at layer 10). |
| Throne Hall | 27x31x31 | civic | A nave between purpur arcades, flying buttresses, a rose window, the throne on a dais under an arc of eight eyes. |
| The Lord's Spire | 11x46x11 | civic | The highest tower, shards floating round it, the Lord's end crystal on top (it can't be broken by players). |
| War Hall | 19x17x15 | work (Voidmarshals) | Glaive racks and a war table mapping the End. |
| Riftguard Barracks | 17x14x13 | work (Riftguards) | A training yard with target blocks and rift posts, an armoury. |
| Seers' Spire | 11x39x11 | work (Seers) | Amethyst banded with crying obsidian, an observatory of magenta glass. |
| Thrall Yards | 21x9x17 | work | Where Endermen stack the Court's blocks; bond posts with chains. |
| Voidhound Kennels | 13x9x11 | work | Four barred stalls off a lit aisle. |

## Street decor

Lamp posts for each people (purpur with a tiny lid, end-stone with a froglight, an obsidian brazier),
benches, a chorus planter, crates, a banner post. The planner puts a lamp beside every path about
every 7 blocks, and on bridge rails.

## Layouts

Ten fixed layouts: `spire_a`/`b`/`c`, `stead_a`/`b`/`c`, `crossing_a`/`b`, `citadel_a`/`b` (mirrored
arrangements). The game picks one at random and turns it to one of four sides.

## How it is built (for developers)

- **Buildings** are Python functions in `tools/buildings/<people>/` drawing into a `kit.Build`
  (contract in `tools/buildings/kit.py`). Fronts face north; the entrance is on the north face.
  The kit refuses beds and unknown block ids, checks doors have room on both sides and that every
  chorus block would survive vanilla's `canSurvive` (plants only branch from a stalk's top).
  Each building marks `sleep`/`work`/`sit`/`stand` spots for its future residents.
  Preview: `python tools/buildings/preview.py <name>` (PNG in `tools/buildings/out/`), or
  `--people shulkin` for a contact sheet, `--all --check` to build everything.
- **Villages** are planned by `tools/villages/plan.py` (rings round the plaza) and
  `tools/villages/citadel_plan.py` (the fortress). `python tools/villages/compile.py --preview`
  writes everything: the tiles (32x32-column structure templates under
  `data/endexpansion/structure/village/<layout>/`), the four structures with their layouts and islet
  rasters embedded (`data/endexpansion/worldgen/structure/`), the structure sets, the biome and
  structure tags, and a resident catalogue per layout (`data/endexpansion/villages/<layout>.json`:
  every building's place, turn and spots). `python tools/villages/preview.py <layout>` renders one.
- **In the game**, `EndVillageStructure` surveys the site, picks a layout and a rotation, then adds a
  `GroundPiece` (clears old terrain, lays the islets) and the `TilePiece`s on top. Templates are placed
  with known shapes, so the stored fence, pane, wall, stair and chorus states are kept as drawn. A
  `ResidentPiece` spawns each resident and animal on the roster when the chunk holding their home
  generates.
  `VillageGrounds` keeps wild chorus and end islands out.
- **Template format:** Minecraft 26.3 reads block-state palettes as `id` / `properties` (lower case);
  `Name` / `Properties` load as air.
- **Test:** `gradlew runClientGameTest -PendTests=Villages -PtestHeap=1536m` creates a world with
  structures on (seed 20261009), locates each kind in the outer End, checks the ground piece and
  blocks were placed, and photographs each from above, the side, the plaza and below
  (`build/run/clientGameTest/screenshots/end-*.png`). `-PendKinds=spire_village,citadel` limits it.

## Residents

`tools/villages/roster.py` turns each layout's catalogue into a roster, embedded in the structure JSON
(`residents`) and listed in `data/endexpansion/villages/<layout>.json` (`roster`):

- A resident per sleep spot in every home; in homes of three or more the last one or two are
  children (and a quarter of two-bed homes have a child).
- Every job building takes an adult of its people: Archivist, Lamplighter, Weaver, Shellwright,
  Wayfinder and Keeper of Shells for the Shulkin; Kiln-keeper, Grove-tender, Brewer, Stonecutter, Cook,
  Blinker and Herder for the Chorrin. Adults left over keep shells (Shulkin) or gather (Chorrin).
- The Crossing Hall's two keepers are one Shulkin (first sleep spot) and one Chorrin (second); the
  trade stalls take a trader from each people in turn.
- Groveback Pens get three Grovebacks, Driftray Roosts two Driftrays.
- A Citadel gets its Court by building (see `PEOPLE.md`).

## Notes for later

- The Groveback Pen's gate is a fence gate the herders don't open yet; the herd stays inside.
- Banners (Shulkin and Court) use the 1.20.5+ pattern format and should be checked in game.
