# End Expansion

A Fabric mod for Minecraft 26.3 that gives the outer End its peoples. Past the gateways, once the
Dragon is dead, you find villages floating on their own islets, people who greet you as the one who
silenced the Dragon, and the Citadels of the Court that set it loose.

## The peoples

- **The Shulkin**: tall shell-folk of the purpur **Spires**. Formal, precise, dryly funny, keepers of
  records. Their lid lifts when they talk and slams shut when they are hurt. They believe the
  shulkers in the old cities are their ancestors, so mind what you do with shulker boxes.
- **The Chorrin**: stone-skinned, chorus-crowned grove-folk of the **Steads**. Warm, blunt and
  endlessly curious about the Overworld. They have no mouths and hum instead, and blink away like
  chorus fruit when startled.
- **Crossings**: market towns where the two live side by side.
- **The Endarch Court**: the ruling caste of the Endermen, with a Lord, Voidmarshals, Riftguards and
  a Herald, Seer and Steward. Endermen in bond-collars are their thralls. A **Citadel** attacks
  anyone who comes in without **Enderman Eyes**, the seal of a Court envoy found on one End ship in
  five. Bring the Eyes and you are a guest: earn Favor with service and tribute, and the Lord may
  give you a Voidhound pup.

Shulkin and Chorrin have children. Nobody in the End has a gender; everyone is "they".

## Creatures

- **Groveback**: a slow six-legged grazer with a chorus grove on its back. Pick the fruit with an
  empty hand (it grows back) and breed them with popped chorus fruit.
- **Driftray**: a manta of the void currents. Tame it with chorus flowers, saddle it and fly between
  the islands.
- **Voidhound**: the Court's hound, built like a Minecraft wolf. Wild ones guard the Citadels; a pup
  from the Lord grows up loyal to you.

## Talking

Right-click any Shulkin, Chorrin or (as a guest) Endarch. The conversation screen has their portrait,
the line typing out in their voice, numbered replies and a gift button. Friendship shows as ten chorus
blossoms and the Court's Favor as ten eyes. About 2,250 lines of dialogue change as you grow closer.

- **Story**: everyone has a story of their own. Help with what they ask, come back on other days,
  and they tell you the rest; answer them one of two ways and they give you something.
- **Journal**: your memories with each person, what you've learned about them, and their story so far.
- **Personalities**: most stand still while you talk; the shy keep their distance, the restless pace,
  the busy go back to work, a proud Lord ends the audience. Strike someone and they'll turn away from
  you until you say sorry.

See [docs/DIALOGUE.md](docs/DIALOGUE.md).

## Finding them

    /locate structure endexpansion:spire_village
    /locate structure endexpansion:stead_village
    /locate structure endexpansion:crossing
    /locate structure endexpansion:citadel

Villages sit at least 1,000 blocks from the main island. Citadels are rare.

## Building

Requires Java 25.

    gradlew build                                              the mod jar, in build/libs
    gradlew runClientGameTest -PendTests=People                in-game test of the peoples, with screenshots
    gradlew runClientGameTest -PendTests=Villages              in-game test of the villages

Design and developer notes are in `docs/`:
- [PEOPLE.md](docs/PEOPLE.md): the peoples and their lore.
- [VILLAGES.md](docs/VILLAGES.md): the buildings and how villages are generated.
- [DIALOGUE.md](docs/DIALOGUE.md): conversations, friendship, Favor and the dialogue bank.

The `tools/` folder holds the Python that makes the models, textures, buildings, village layouts and
dialogue checks.

## License

MIT
