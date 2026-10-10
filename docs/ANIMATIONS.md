# Animations

Every people has an animation pack: at least fifty clips that make them feel alive. Standing folk idle in their
own way and practise their trade, chat with a neighbour, greet you as you walk up, gesture while their line types
out in a conversation and listen while you choose a reply, and react to what happens: a gift they love, one they
don't, a level of friendship or Favor, a sorry accepted, a blow.

Packs only describe motion. The director (`client/anim/Life.java`) decides when each clip plays and the poser
(`client/anim/Poser.java`) adds it on top of the model's live pose. Nothing about animation is saved or synced
except two small things the server already knows: each person's job and manner (synced with the entity) and
reactions to conversation moments (the `endexpansion:cue` packet).

## The packs

| People | Pack | Models it fits |
|---|---|---|
| Shulkin | `shulkin` | grown-up (cape, forearms, the lid) and child (soft shell) |
| Chorrin | `chorrin` | grown-up (forearms, chorus crown) and sprout |
| Endarchs | `endarch` | Lord (mantle, crown), Voidmarshal (cape, circlet), Riftguard (glaive); no children. Thralls don't animate |

Compiled packs live in `src/main/resources/assets/endexpansion/folk_animations/<people>.json`; they are written
in Python under `tools/animations/<people>/*.py` with `tools/animations/kit.py`. Never hand-edit the JSON.

```text
python tools/animations/compile.py                 # compile every people
python tools/animations/compile.py shulkin            # one people
python tools/animations/compile.py --check         # validate, coverage, at least 50 distinct motions, JSON current
python tools/animations/compile.py --list shulkin     # every clip: trigger, length, weight, requirements
python tools/animations/compile.py --parts shulkin    # the parts each model has, and the waist
python tools/animations/sheet.py shulkin --clips stretch,greet_wave --frames 7 [--view 90] [--look shulkin_child] [--mirror]
                                                   # frames of clips on the real model, offline -> tools/animations/out/
```

## How the director chooses

Each person near the player is ticked on the client. When they have stood still for a second and their last clip
has finished, they rest a moment (children less), then pick a clip for the moment:

| Trigger | When |
|---|---|
| `idle` | Standing around: everyday moments and their work compete by weight. |
| `chat_speak`, `chat_listen` | Another of their people stands within about three blocks in front of them; they take turns. |
| `greet` | A player walks up within five and a half blocks in front of them (once a minute at most), or a conversation opens. |
| `talk` | In a conversation with you, while their line types out. |
| `listen` | In a conversation, while you choose a reply. |
| `farewell` | The conversation ends (or they leave it: busy, sleepy, or the audience is over). |
| `happy` | A gift or tribute they love, or a new level of friendship or Favor. |
| `thanks` | A gift or tribute they like or don't mind. |
| `decline` | A gift they dislike, or a sorry they aren't ready to accept. |
| `pleased` | A sorry accepted. |
| `annoyed` | Still upset with you, they turn away. |
| `hurt` | They take damage. |

Reactions play on a second layer and briefly replace the current activity; while walking they keep the upper body
and leave the stride alone; activities fade out when someone starts moving. Nobody repeats their last two clips if
anything else fits. One person in nine is left-handed and mirrors one-handed gestures.

Nobody animates while fighting or asleep, nor a Shulkin shut in its shell. While a clip plays, the model's own
work and talk gestures rest.

Clips are picked by **tags**:

| Tag | Meaning |
|---|---|
| `adult`, `child` | Age. |
| `job:<job>` | Their job: `job:archivist`, `job:grove_tender`, `job:herald`... (children have none). |
| `manner:<manner>` | Their personality's manner: steady, shy, restless, busy, flighty, proud. |
| `working` | At their workplace in working hours: boost work clips with it. |
| `rank:<rank>` | An Endarch's body: `rank:lord`, `rank:marshal`, `rank:riftguard` (a Herald, Seer or Steward has a Lord's or Marshal's body; use `job:` for the role). |
| `social` | A chat partner is near. |
| `talking` | In a conversation with you. |

## File format

```json
{
  "format": 1,
  "species": "shulkin",
  "name": "Shulkin",
  "waist": {"hip": 6, "upper": ["body", "head", "right_arm", "left_arm"]},
  "clips": [
    {"id": "polite_wave", "name": "Polite wave", "trigger": "greet", "length": 2.0, "weight": 3,
     "require": ["adult", "job:archivist|job:keeper"], "avoid": ["manner:shy"], "boost": {"social": 2},
     "blend": [0.25, 0.35], "mirror": "hand", "tracks": {
      "right_arm.rot": [[0, 0, 0, 0], [0.4, -20, 0, 120], [1.2, -20, 0, 130], [2.0, 0, 0, 0]],
      "waist.rot": [[0, 0, 0, 0], [0.6, 10, 0, 0], [2.0, 0, 0, 0]],
      "root.pos": [[0, 0, 0, 0], [0.3, 0, -1, 0], [0.6, 0, 0, 0]]
    }}
  ]
}
```

| Field | Meaning |
|---|---|
| `id` | Lowercase letters, digits and underscores. In game a clip is `<people>:<id>`. |
| `trigger` | One of the triggers above (default `idle`). |
| `length` | Seconds, up to 30. |
| `weight` | Relative chance against the other clips that fit (default 1). |
| `require` | Every entry must match; `a|b` matches either tag. |
| `avoid` | Any matching tag rules the clip out. |
| `boost` | Weight multipliers for matching tags. |
| `blend` | Seconds to fade in and out (default 0.25, 0.35). |
| `mirror` | `hand` mirrors for left-handed folk (default), `free` also at random, `never` keeps it as written. |
| `tracks` | `<part>.rot` (degrees) and `<part>.pos` (model pixels), keys `[seconds, x, y, z]` with increasing times. |

A part is any named part of the people's models (`compile.py --parts`); a part a model doesn't have is skipped
on that model, so one pack serves every look. `waist` bends the pack's upper parts at the hips (rotation only) and
`root` turns or moves the whole body about the feet. Values between keys follow smooth monotone curves that never
overshoot a key; start and end every track at zero so clips blend cleanly (kit.py does this).

## Authoring

`kit.py`'s docstring has the conventions (they make poses read the same on both sides of the body). Weights keep
each person's trade visible among the everyday moments: work 3-5 (boosted by `working`), everyday idles 1-3, manner
variants boosted by their manner. The Endarchs have no children, so their clips need only cover grown-ups. Every trigger needs at least one clip for grown-ups and one for children
(`compile.py --check` says which are missing). Clip names have no commas.

Tips:

- A clip is added to whatever the model is already doing, so small, specific motions read best: a head tilt, a
  hand to the chin, a shrug. Big ones (a bow, a hop, a spin) are for reactions.
- Forearms, shins and lower arms bend at the elbow and knee; use them, a straight arm looks stiff.
- When the waist bends, a cape, veil or mantle swings with the body: counter-rotate it to keep it hanging.
- Keep limbs out of the body: check the sheet from the front (`--view 0`) and the side (`--view 90`).
- The models already sway, breathe and walk, a Shulkin glides and lifts its lid as it talks, a Chorrin's crown
  sways as it hums; clips go on top. A Shulkin's `lid` is a part: lifting it (`lid_pos` y negative, a little
  `lid` pitch) reads as an open, talking or surprised face.
