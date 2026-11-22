---
name: What If It Doubled
version: 1
status: approved
colors:
  paper: "#FFFDF4"
  cobaltBackdrop: "#2F50E8"
  cobaltMid: "#2440C4"
  cobaltDark: "#1A2F99"
  cobaltDeep: "#111F6B"
  cobaltLight: "#9DAEFF"
  plumBackdrop: "#6A35C9"
  plumMid: "#5527A8"
  plumDark: "#401C82"
  plumDeep: "#2A1159"
  plumLight: "#C3A6F7"
  pineBackdrop: "#0E7C6B"
  pineMid: "#0B6557"
  pineDark: "#084D43"
  pineDeep: "#05332D"
  pineLight: "#86D8C6"
  heroRice: "#FFFDF4"
  heroTennis: "#D9F23C"
  heroDice: "#F4493B"
typography:
  display:
    fontFamily: Archivo
    fontWeight: 800
    fontStretch: "100%"
    letterSpacing: "-0.03em"
    lineHeight: 1
  counter:
    fontFamily: Archivo
    fontWeight: 800
    fontStretch: "62%"
    lineHeight: 0.88
  label:
    fontFamily: Archivo
    fontWeight: 700
    fontStretch: "100%"
    letterSpacing: "0.08em"
    textTransform: uppercase
spacing:
  unit: 8px
  typeLeft: 120px
  typeTop: 300px
  typeWidth: 768px
components:
  question:
    referenceCanvas: 1080x1920
    fontSize: 112px
    color: "#FFFDF4"
    maxLines: 4
  dayChip:
    referenceCanvas: 1080x1920
    fontSize: 104px
    background: "#FFFDF4"
    color: backdrop of the episode world
  count:
    referenceCanvas: 1080x1920
    fontSizeMax: 236px
    fontSizeMin: 96px
    fitWidth: 768px
  unit:
    referenceCanvas: 1080x1920
    fontSize: 46px
  payoff:
    referenceCanvas: 1080x1920
    fontSize: 112px
    maxLines: 3
  comparatorTag:
    referenceCanvas: 1080x1920
    nameSize: 40px
    valueSize: 92px
    leaderWidth: 6px
---

# Visual treatment

A toy diorama on a seamless coloured sweep. One everyday object in its own colour; everything else in the frame is one hue in five values. The object is the only thing that changes, and it keeps changing until it is the whole picture. Big white type states the day and the exact count, so the frame reads with the sound off.

Visual revision 1, approved on 2026-11-22. The values below are the ones used by the [style board](style-board.html), the [studies](studies/studies.html) and the [motion preview](motion-preview/index.html).

## Colour

- An episode picks one world: `cobalt`, `plum`, `pine`, or a new ramp built the same way (backdrop, mid, dark, deep, light of a single hue). Props, architecture, landmarks and the ground use only that ramp.
- The object has one flat hero colour that contrasts the world. Rice is paper white, the tennis ball is `#D9F23C`, dice are `#F4493B`. A new object gets a new hero colour.
- Type is always paper `#FFFDF4`. When the hero colour floods the frame, type and the day chip flip to the world's `deep` value.
- No second hue in the world, no gradients, no glow, no outlines, no textures.

## Type

Archivo variable (`assets/fonts/Archivo-Variable.ttf`, SIL OFL 1.1) is the only family, in two widths.

- Question and payoff: weight 800, width 100, 112 px, line height 1, tracking -0.03em, balanced wrap, at most four lines.
- Day chip: weight 800, width 62, 104 px, paper box with the backdrop colour as text.
- Count: weight 800, width 62, tabular figures, fitted to 768 px wide between 96 and 236 px. Past 15 digits it wraps into two lines. Always the exact integer with thousands separators.
- Unit line: weight 700, 46 px, uppercase, tracking 0.08em. From one million up it names the size in words ("2.1 billion grains of rice").
- Comparator tag: name at weight 700, 40 px, uppercase, tracking 0.06em, above the measure in the counter style at 92 px, with a 6 px leader down to the thing it names.

## Framing

- 1080 x 1920. The type block starts at x 120, y 300 and is 768 px wide. This clears the top and side UI of Shorts, Reels and TikTok.
- The object's anchor sits at 70 to 72 percent of frame height. Nothing in hero colour enters the type block except during a hero iris or when the mass itself fills the frame.
- Comparator tags stay inside x 120 to 888, and inside x 120 to 780 when they sit below y 840.
- Keep y above 1500 free of type. A caption track, if a production adds one, goes below the object and never over the count.
- The hook question and the single object are both in frame at 0.0 s. Nothing fades in from empty.

## 3D treatment

Scene source: [assets/scene/diorama.js](assets/scene/diorama.js), [counter.js](assets/scene/counter.js), [type.css](assets/scene/type.css), [landmask.js](assets/scene/landmask.js). Three.js r187 is vendored under `assets/vendor/` (MIT).

| Decision | Direction |
| --- | --- |
| Form | Low-poly, faceted, built from boxes, lathes and cones. Real proportions at a stated metric scale: a 6.6 mm rice grain, a 4 x 4 x 2.5 m room, a 93 m statue, a globe. Detail stops at the silhouette. No faces: a statue is a silhouette in a world value. Containers are open or cut away so the mass inside reads. |
| Materials | `MeshLambertMaterial` with `flatShading`, one flat colour per part, no maps, no specular, no transparency. Hero colour is used on the object and its mass only. |
| Light and depth | One white directional key from upper left (intensity 1.75), one ambient fill tinted 35 percent toward the world's `light` value (intensity 2.05), no tone mapping. A shadow catcher in the world's `deep` value at 50 percent gives one hard contact shadow. The backdrop is the flat scene colour, so depth comes from value steps between faces. |
| Camera and movement | Perspective, 26 degree field of view, pitch 20 to 38 degrees, yaw 28 to 40 degrees. One continuous eased dolly back through every scale that shares a scene (plate, table and room are one scene), with no cut and no wipe. The object stays where it is; the camera leaves. A cut happens only under a hero iris, at a jump to city scale or beyond. Small-scale items are drawn and counted individually; from thousands up the mass is a faceted heap whose volume follows the count. |
| Finishing and annotations | No post-processing, depth of field, bloom or grain. Tags are DOM type projected from a world point, so they stay sharp. Antialiased canvas at pixel ratio 1. |

Per episode: the object and its hero colour, the world ramp, which four or five scales are shown, the comparators, the camera path, and the timings. Identity: the ramp logic, the type system, the lighting, flat shading, the counter stack, the tag, the unbroken pull-back, and the hero iris for big jumps.

## Scale ladder

Table, room, building, landmark, city, country, planet. An episode shows four or five rungs chosen by its own arithmetic, and may skip rungs. Each jump has exactly one comparator, shown as a physical thing beside or around the mass and tagged with a real measure in the same unit. The style board lists example comparators per rung.

## Motion

- Hold: the question holds 1.5 to 2 s on a locked camera.
- Tick: each day the count snaps to the new value with a 7 percent overshoot settling in 0.16 s, and the new items hop out of the old ones. Day intervals shorten by about 10 percent each day.
- Pull back: the default way to change scale. One unbroken dolly while the count runs, on a single eased path in log distance, through every scale one scene can hold. The smaller scene stays inside the larger one (the plate on the table in the room), and the mass spills from one container into the next. No cut, no wipe.
- Hero iris: only for a big jump that no single scene can contain, to a city, a country or the planet. The hero colour blooms from the mass to cover the frame, the days race on and the cut happens under it, then it closes onto the next scale. About 0.7 s. Type flips to `deep` once the bloom reaches the type block. Never two irises back to back: a pull-back or a hold sits between them.
- Tag: the comparator tag grows up from the thing it names in 0.3 s, then everything holds long enough to read.
- Payoff: the count and unit leave; the day chip and one sentence stay. Hold at least 1.5 s.
- Rewind: the film runs backwards in about 0.7 s and lands on frame one, so the loop point is invisible.

All motion is a pure function of time. The scene renders from `hf-seek`; nothing accumulates between frames.

## Audio

Direction only, not yet produced; the motion preview is silent.

- No narration. Sound effects are dense and lead the mix.
- One dry tick per day, pitching up as days shorten.
- The object's material sound under the ticks, scaling with the count: single items, then a pour, then a roar.
- One hit on each scale jump, a different take each time.
- A short stamp when a comparator tag lands.
- Near silence for a beat, then one small dry sound on the payoff.
- The rewind gets a short reversed sweep that ends on the first tick.
- Thin music bed at or under -24 LUFS, below the effects, silent under the payoff.
