# The People of the End

Working title of the mod: **End Expansion** (mod id `endexpansion`, set in one place: `tools/mobkit.py`).
This is a separate mod and repo from Village Friends. From Village Friends we take only the look and
layout of the conversation screen (`FriendshipScreen`: friendship card, dialogue box with portrait and
name ribbon, numbered reply bubbles, the dock), recoloured purpur. All dialogue is new. Animations are
simple poses for now (walking, talking, working, sleeping, fighting).

Everything here is in the game: every people and creature is a mob, villages spawn their residents,
and conversations, friendship and the Court's guest-law work as described in `DIALOGUE.md`.

Concept models: `tools/people/shulkin.py`, `tools/people/chorrin.py`, `tools/people/endarch.py`
(three ranks + an Enderman thrall), and the item `tools/items/enderman_eyes.py` (same box-model kit
as Not-So-Vanilla Mobs). Build and preview:

    python tools/people/shulkin.py
    python tools/preview/preview.py shulkin --views 4

## Where they live

The outer End islands, past the gateways. Nobody reaches them before the Dragon is dead, so every
resident meets the player as "the one who silenced the Dragon". That is the first thing they talk about.

## Shulkin (SHUL-kin) — the shell-folk of the spires

- **Body:** about 2.6 blocks tall, slender, very long arms with three thin fingers. They glide a pixel
  above the ground on pointed feet.
- **Head:** a living shell like a shulker's: a lid over a collar. Their pale face looks out through the
  gap with two glowing violet eyes. The lid lifts when they talk and slams shut when they are hurt or
  frightened (a closed Shulkin takes much less damage, then peeks out again).
- **Dress:** long void-cloth robes, purpur shell pauldrons and breastplate, an embroidered back mantle
  with the Eye of the Spires.
- **Temperament:** formal, precise, ceremonial, long memories, very dry humour. They record everything.
- **Names:** soft and long (Ilvane, Oseth, Maerith, Sovel, Quillane), plus the lamp that was lit when
  their lid first opened: "Ilvane of the Third Lamp".
- **Belief:** a Shulkin who closes and never opens again leaves a living shell behind. They believe the
  shulkers in the old cities are their ancestors, so the player's shulker boxes are an awkward topic.
- **Work (draft):** Archivist, Shellwright, Lamplighter, Weaver, Wayfinder, Keeper of shells.
- **Variety:** shell colour (purpur, deep magenta, pale lilac, rare ivory "old shell"), robe trim by
  job, lid crest.
- **Children** (`shulkin_child`, scale 0.7, about 1.3 blocks): a full-size shell on a small body, the
  shell soft and pale (it darkens and hardens over the years), no crest or armour, a plain smock.
  Named the night their lid first opens. Young lids pop open at everything.

## Chorrin (KOR-in) — the grove-folk of the outer islands

- **Body:** about 1.6 blocks tall (2.1 with the crown), broad and heavy, skin like end stone. Long arms
  that nearly reach the ground and big three-fingered hands. Short legs, wide feet.
- **Head:** a heavy brow over deep-set glowing violet eyes. No mouth: they speak in a low hum.
- **Crown:** living chorus grows from the head. No two are alike, and it flowers with age, seasons and
  mood. Some grow a sprout on a shoulder too.
- **Gift:** when startled they blink a few blocks away, like eating chorus fruit.
- **Dress:** woven chorus-fiber sash and wraps, a braided chorus cord belt with a buckle of traded
  shulker shell, a hip pouch.
- **Temperament:** warm, blunt, funny, communal, endlessly curious about the Overworld (rain, grass,
  the sun). Superstitious about the void.
- **Names:** short and hummable (Mott, Orra, Brannoc, Tumm, Pell, Gorrim), plus their grove:
  "Mott of Low Grove".
- **Work (draft):** Grove-tender, Kiln-keeper, Stonecutter, Cook, Blinker (courier), Brewer.
- **Variety:** skin from pale end stone to darker obsidian-flecked stone, five crown shapes, bloom
  colour, cloth colour.
- **Children: "sprouts"** (`chorrin_child`, scale 0.75, about 1 block, 1.2 with the sprout): round and
  stubby, a head as big as an adult's, big bright eyes, smoother pale stone, a chorus-fiber tunic and a
  single chorus sprout that branches into a crown as they grow. Startled sprouts blink too.

## Endarchs (EN-darks) — the Court, rulers of the Endermen

- **Body:** an Enderman's void-black skin, but taller and broader: about 3.4 blocks, the Lord 3.8.
  Very long arms with three claws.
- **Eyes:** the Enderman's two slits, plus a crown of smaller eyes along the brow. More eyes means
  higher birth: Lord 8, Voidmarshal 6, Riftguard 4, an Enderman 2.
- **Crowns:** the highborn have obsidian shards floating over their heads. The Lord's crown holds an
  end crystal.
- **Ranks:** Lord of the Citadel; Voidmarshals (generals, heavy obsidian plate, war capes);
  Riftguards (high warriors, visored helms, floating rift armour, crystal glaives, teleport behind
  you); court roles Herald, Seer, Steward.
- **Endermen are the Court's thralls and peasants,** "the Court's hands". This explains vanilla:
  Endermen carry blocks because they haul stone for the Court, and they hate being looked in the eye
  because only their masters may do that. In a Citadel they wear a purpur bond-collar.
- **Manner:** imperious, archaic, proud, bound by old law. They never forget a slight.
- **Names:** harsh and sibilant with a title: Lord Vaskhar, Voidmarshal Ithrael, Riftguard Morvex,
  Herald Zhaal.
- **No children (decided):** Endarchs and Endermen are never born as babies, and a Citadel has no
  children in it. Where new ones come from is the Court's oldest secret (a story thread).

## Enderman Eyes and the Citadel

- **Enderman Eyes** (item): a pair of preserved royal eyes in an obsidian reliquary, the seal of an
  Endarch envoy. Rare loot on End ships: 1 ship in 5 (decided).
- **Citadels** are royal villages: rare, far out, Endarchs and their thralls only. Black obsidian and
  purpur fortress, spires with floating fragments, the Lord's end crystal on the highest one.
  Buildings: Gate of Eyes, Throne Hall, War Hall, Riftguard barracks, Seers' spire, thrall yards.
- **Without the Eyes:** the moment you cross the Citadel boundary the Herald cries out, the
  Riftguards rift-step to you and the whole Citadel attacks, Endermen included. No talking.
- **With the Eyes:** the Herald reads the seal at the Gate of Eyes and you are received as a guest.
  You can talk to the Court and earn Favor through service (Favor is kept between visits).
- **You must carry the Eyes on every visit (decided).** Nothing is remembered: every time you enter a
  Citadel the Eyes must be in your inventory. If they leave it while you are inside (dropped, stored,
  lost on death), guest-law ends and the Citadel attacks.
- Attack anyone and guest-law breaks: the Citadel turns on you.

## Creatures

One beast for each people. Models in `tools/creatures/`.

- **Groveback** (Chorrin): a slow, broad, six-legged grazer with an end-stone hide and a small chorus
  grove growing on its back (the same chorus as a Chorrin's crown). Pick chorus fruit off its back
  (it regrows); breed with popped chorus. Herded around Steads and Crossings, wild herds on the outer
  islands. About 1.4 blocks tall, 2 long.
- **Driftray** (Shulkin): a manta that glides on the void currents, violet and star-spotted above,
  pale below, with a glowing tail tip. Wild flocks drift around the Spires; tame with chorus flowers
  and ride it across the gaps between islands (slow, gliding flying mount). 3-block wingspan.
- **Voidhound** (the Court): built on the vanilla Minecraft wolf model (same boxes and pivots, user's
  request), scaled 1.3 (about 1.25 blocks). Void-black coat, magenta eye slits, an obsidian collar
  studded in magenta, three obsidian shards floating over its back. Runs with the Riftguards,
  teleports in short hops, reaches intruders without the Eyes first. Citadels only.
- **Voidhound pup** (decided): earn high Favor with a Citadel's Lord and the Court gives you a pup.
  Purpur collar with a bone tag (like a tamed wolf's collar), bigger head for its size like a baby
  wolf, one small shard. Grows into a full hound and behaves like a tamed wolf.

Decided: three creatures is enough.

## How the peoples get along

- **The Old Accord:** the Shulkin built the purpur cities; the Chorrin grew the chorus that fed them.
  Purpur is made from popped chorus fruit, so the Shulkin literally built with Chorrin harvests.
  The Court ruled the central island with its Endermen.
- **The Dragon is loosed:** the Court set the Dragon on the cities. The cities emptied and were sealed.
  Court envoy ships moored at the cities (the dragon head on an End ship's prow is the Court's), each
  carrying Enderman Eyes as its seal.
- **The Long Watch:** the Shulkin and Chorrin scattered to the outer islands and waited the Dragon out
  while the Court ruled the centre.
- **Now:** the player has killed the Dragon. The Court has pulled back to its Citadels and attacks any
  stranger who doesn't bear the Eyes. Shulkin and Chorrin are equals and trading partners, a little
  wary of each other, and both fear the Court. Shulkin call Endermen "the Unlidded" and the Endarchs
  "the Crowned"; Chorrin call Endermen "the Tall Quiet".

## Villages

| Kind | Who | Share (draft) | Look |
|---|---|---|---|
| **Spire** | Shulkin only, 6-14 | 40% | Tall purpur towers on high islands, sky bridges, end-rod lamps, magenta glass. Lid Hall, Archive, Lamp Tower, Shell Nursery. |
| **Stead** | Chorrin only, 8-16 | 40% | Low end-stone domes half sunk into the island, round doors, terraced chorus groves, popping kilns, a stone hum-circle. |
| **Crossing** | Both, 14-24 | 20% | Bigger market towns at gateway rims and bridge islands: a spire quarter and a stead quarter around one shared market. Cross-species friendships and rivalries. |
| **Citadel** | Endarchs + Enderman thralls | rare, outside the split | The royal village. Hostile unless you carry Enderman Eyes. |

## In the game

| Mob | Size (blocks) | Health | Where |
|---|---|---|---|
| Shulkin / child | 2.6 / 1.25 | 30 / 14 | Spires and Crossings |
| Chorrin / sprout | 1.9 / 1.1 | 26 (armour 4) / 12 | Steads and Crossings |
| Endarch Lord | 3.8 | 160 | the Throne Hall |
| Voidmarshal (also the Herald, Seer and Steward) | 3.5 | 100 | War Hall, gate, Seers' Spire, Throne Hall |
| Riftguard | 3.4 | 70 | barracks, gate, throne, the Lord's Spire |
| Enderman thrall | 2.9 | 40 | thrall yards |
| Groveback | 1.4 | 30 | Groveback pens; wild herds on the outer islands |
| Driftray | 1.1 (3 wide) | 24 | Driftray roosts; wild in the End highlands |
| Voidhound / pup | 1.1 / 0.55 | 30 | kennels; a pup from the Lord |

- **Residents live by the overworld clock** (the End's sky never changes): at work from morning (the
  children play round the plaza), at the plaza in the evening, asleep in their niche or nest at night.
  They open doors. A resident who can't find the way while no player is near simply arrives.
- **Every resident has a name, a job, a bed and a workplace** from the village roster
  (`tools/villages/roster.py`). Shulkin are named for their lamp ("Ilvane of the Third Lamp"), Chorrin
  for their grove ("Mott of Low Grove"), Endarchs by title ("Voidmarshal Ithrael").
- **Shulkin** shut their lid when hurt (a quarter of the damage gets through) and sleep shut.
  **Chorrin** blink up to 8 blocks away when hurt.
- **Endarchs** keep their posts and fall on outlaws. Riftguards rift-step behind whoever they fight
  and slip aside from arrows; hounds hop through short rifts. Thralls haul blocks of obsidian.
- **Grovebacks** give 2-4 chorus fruit (sometimes a chorus flower) to an empty hand; the grove on their
  back shrinks and grows back over four minutes. **Driftrays** drift two blocks over the ground and
  never out over the void; tamed, saddled and ridden they fly where you look (jump to rise) and glide
  down when you let go. Neither the ray nor its rider takes fall damage.

## Conversation screen

Same layout as Village Friends, purpur palette:

- Paper `#f6eef7`, paper shade `#e6d6e8`, edge `#4a2c52`, light edge `#b48fb6`, ink `#3b2544`,
  muted `#8a7393`, status text in ender-pearl teal `#2f8f84`.
- Friendship shown as ten chorus blossoms (instead of hearts) that fill as you get closer.
- Dock: Talk, Gift (Tribute for the Court), Farewell. (Village Friends' Story, Time, Travel, Journal,
  Trade and Settlement tabs are not part of this mod yet.)
- Typing voice: Shulkin blips are high and glassy; Chorrin are a low hum; Endarchs a low, warped buzz.
- With Endarchs the meter is Favor, shown as ten eyes instead of blossoms.

## Decisions (2026-10-09)

1. Names: **Shulkin**, **Chorrin** and **Endarch** are final.
2. The Shulkin belief that shulkers are their ancestors stays (shulker boxes are a touchy subject).
3. **No genders** for any of the three peoples. Every resident is "they" in all text, there are no
   gendered names (one name pool per people), and no gendered wardrobe or models.
4. Village mix: Spire 40%, Stead 40%, Crossing 20%. Citadels are separate and rare.
5. Enderman Eyes must be carried on every Citadel visit; they drop on 1 End ship in 5.
6. Three creatures (Groveback, Driftray, Voidhound). The Voidhound looks like a Minecraft wolf; a pup
   is a high-Favor reward from the Court.
7. Shulkin and Chorrin have children; Endarchs and Endermen do not.
