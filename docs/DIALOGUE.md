# Talking to the End peoples

Right-click a Shulkin, a Chorrin, one of their children or (as a guest) a member of the Court to
open the conversation screen. This document covers the dialogue bank, how closeness grows, and the
Court's own rules. The peoples themselves are in `PEOPLE.md`, their villages in `VILLAGES.md`.

## The conversation screen

The Village Friends layout in purpur (`client/screen/ConversationScreen.java`):

- **The dialogue box**: a portrait of the speaker, their name on a ribbon with their job and village,
  and the line typing out in their voice: glassy chimes for the Shulkin (higher for children), a low
  hum for the Chorrin (no mouths), a warped bass for the Court. Space or a click finishes the line.
- **Replies**: numbered bubbles on the right (press 1-8 or click).
- **The dock**: Talk (say hello again), Gift (the Court: Tribute, for what you hold in your main
  hand; two a day) and Farewell (Esc).
- **The card**: how close you are, as ten chorus blossoms (friendship) or ten eyes (Court Favor),
  the level's name, and how far to the next one. A banner drops in when you reach a new level.

## Replies

| Who | Replies |
|---|---|
| Shulkin | Chat · Ask about the Dragon · Ask about their work · Ask about home · Ask about the Chorrin · Ask about the Court · Ask about the old shells · Tell of the Overworld |
| Chorrin | Chat · Ask about the Dragon · Ask about their work · Ask about home · Ask about the Shulkin · Ask about the Court · Ask about the void · Tell of the Overworld |
| Children | Chat · Play together · Ask about the Dragon · Ask about home · Ask about the other people · Ask about the Court · the old shells / the void · Tell of the Overworld |
| The Court | Address them · Ask about the law · Speak of the Dragon · Ask about the thralls · Ask of the other peoples · Ask where Endarchs come from · Offer your service (then: Deliver ...) · the Lord only: Ask for a hound |

What they say on opening depends on the moment: the first meeting (everyone knows you as the one who
silenced the Dragon), after you hit them, when you wake them at night, when you carry a shulker box
(the Shulkin believe shulkers are their ancestors) or Enderman Eyes, or an ordinary greeting.

## Closeness

| | Friendship (Shulkin, Chorrin, children) | Favor (the Court, per Citadel) |
|---|---|---|
| First conversation of the day | +4 | +2 |
| Each topic, once a day | +3 (chat +4) | +1 |
| Gift / tribute they love, like, don't mind, dislike | +25 / +12 / +4 / -8 | +8 / +4 / +1 / -3 |
| Hitting them | -15, and they're wary for a while | breaks guest-law, -20 |
| Service task delivered | | +5 to +14 |

Levels run 0 to 10. Friendship levels need 20, 45, 75, 110, 150, 195, 245, 300, 360 and 425 points;
Favor levels 8, 18, 30, 45, 62, 82, 105, 130, 158 and 190. Every level has its own name in each
people's manner (the Shulkin count how far into their records you are, the Chorrin grow from Seed to
Full Bloom, the Court from Tolerated to Friend of the Crown). What they say grows warmer as you climb.

Friendship is kept by each resident. Favor is kept by a whole Citadel's Court, for good.

## The Court and the Eyes

- **Without Enderman Eyes** a Citadel is closed: cross its boundary and the Herald cries out, and the
  whole Court (Endarchs, thralls and hounds) attacks. Leave and they let you be.
- **With the Eyes** in your inventory you are a guest and may talk to any Endarch. The Eyes must be
  carried on every visit; if they leave your inventory inside (dropped, stored, lost), or you strike
  any member of the Court, guest-law ends and the Citadel attacks.
- **Service**: any Endarch will set a task (sixteen obsidian, eight ender pearls, an end crystal...).
  Bring it and choose Deliver.
- **The hound**: at eight eyes of Favor the Lord gives you a Voidhound pup, once per Citadel. It grows
  up and behaves like a tamed wolf: sit, follow, fight for you, meat heals it.
- **Thralls** never speak: clicking one tells you what you see instead.
- Court mobs from spawn eggs belong to no Citadel: they attack players without the Eyes who come
  within 16 blocks, and anyone who strikes them.
- **Where the Eyes are**: one End ship in five was a Court envoy's, and its left-hand chest (beside the
  elytra) holds a pair (`mixin/EndShipEyesMixin`, loot table `chests/envoy_ship`).

## The dialogue bank

`src/main/resources/data/endexpansion/dialogue/`: `shulkin.json`, `chorrin.json`,
`shulkin_child.json`, `chorrin_child.json` and `court.json`, about 2,000 lines in all. Check it with

    python tools/dialogue/check.py

which enforces the schema and the rules: every topic keyed by minimum level (`"0"` to `"10"`; for
level L the lines under the largest key at or below L are used), placeholders limited to `{player}`,
`{name}`, `{village}`, `{neighbour}`, `{job}`, `{task}`, `{lord}` and `{title}`, lines of at most 200
characters, no duplicates, and no gendered words: every End person is "they". Adult banks also hold
the level names, the people's name pool and their village names; folk banks hold job lines (used for
"Ask about their work"), the Court bank holds per-rank overrides (lord, marshal, riftguard, herald,
seer, steward). Gift tastes are lists of item ids.

The game reads the banks with `talk/DialogueBank.java`; `talk/Conversation.java` picks the topic and
fills the placeholders.
