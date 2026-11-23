---
name: Bukan, Tapi
version: 1
status: approved
colors:
  ink: "#1F2140"
  white: "#FFFBF2"
  highlight: "#FF7A2F"
  body:
    clay: "#E2674A"
    teal: "#2E9C93"
    plum: "#7C5BB3"
    moss: "#7FA650"
    sand: "#E8B656"
  palettes:
    workshop: { skyTop: "#F9E7C4", skyLow: "#FCF3DF", far: "#E9C99A", near: "#D9A96E", ground: "#C98B52", groundLow: "#B5773F" }
    night: { skyTop: "#232B5C", skyLow: "#3D4A86", far: "#2E3A70", near: "#27315F", ground: "#3A4578", groundLow: "#2B3463" }
    room: { skyTop: "#F3D9C2", skyLow: "#F8E7D6", far: "#E6BFA2", near: "#D9A988", ground: "#A9705A", groundLow: "#8F5A47" }
    dusk: { skyTop: "#C9D8EE", skyLow: "#F6DDD0", far: "#A9B7D8", near: "#8E9CC6", ground: "#7A86B4", groundLow: "#66719E" }
typography:
  caption: { fontFamily: Plus Jakarta Sans, fontWeight: 800, fontSize: 68px, textTransform: lowercase }
  tag: { fontFamily: Plus Jakarta Sans, fontWeight: 800, fontSize: 46px }
  bubble: { fontFamily: Plus Jakarta Sans, fontWeight: 700, fontSize: 50px }
spacing:
  frame: 1080x1920
  horizon: 1010px
  captionCenterY: 1500px
  captionRegion: [60, 1400, 960, 200]
  outline: 8px
---

# Bukan, Tapi — visual specification v1

Source of truth for drawing is the [kit](assets/kit.js); the [sample scenes](assets/scenes.js) show its use.

## Look

Flat 2D shapes with an 8 px ink outline and rounded corners. A stage is five bands: sky gradient, a pale sun disc, two hill bands, a ground gradient split by an ink horizon line near mid-frame. Interiors swap the hills for a wall band and one window. Shading is one darker band on the lower third of a body; no textures, no drop shadows beyond one contact ellipse.

Characters are original "bean" figures: a capsule body with face, two short ink legs, two noodle arms with round hands. Identity comes from body colour plus one head mark (cap, headband, bun). Five expressions (calm, glad, worry, shock, smug), eye direction and sweat drops carry the acting. Two characters in a story never share a body colour.

Each episode picks one stage palette as its base and may switch to a second for a time or place change. `highlight` orange is reserved for the spoken caption word and for the one tag per shot that carries the point; `ink` and `white` are fixed across episodes.

## Framing and captions

1080 x 1920, 30 fps. One or two figures or one object per shot, feet on the ground between y 1300 and 1600 in wide shots, open sky above for tags and bubbles. Cutaways go close on a single prop. The camera may push in up to about 15% during a shot.

Captions are lowercase groups of one to three words on one line, centred at y 1500 (78% of height, as in the references), white with a 12 px ink stroke. The word being spoken sits in an orange rounded box with ink text. Keep the action above the band; ground and prop legs may pass under it.

Paper tags (white, ink outline, tilted 3–4°) follow the object they label and pop in; counters are tags whose number changes. Speech bubbles hold a character's line in sentence case.

## Motion

- First visible change inside the first second (pilot: 0.2 s).
- Cuts follow narration clauses. Target 2.4–3.1 s per shot; a dialogue-led episode may sit near 4.6 s. No shot is static for more than 2 s: something poses, enters, counts or drifts.
- Hard cuts by default. Up to five whip slides per episode, used for "meanwhile" or a jump in time.
- Vocabulary: pose and expression changes, props entering beside the figure, tags popping (back-out ease, about 0.3 s), counters ticking, slow push-ins, sun travel for passing time.

## Audio

Narration leads at about 2.5 words per second, mixed to about −14 LUFS with true peak under −0.5 dBTP. A soft acoustic or piano bed sits about 28 dB under the voice with no ducking. Effects are sparse and tied to visible physical events (a pop on a tag, a whoosh on a whip, impacts on big moments). Voice choice is open; see [AUDIO.json](AUDIO.json).

## Assets

Plus Jakarta Sans variable, SIL OFL 1.1, in `assets/fonts/` with its licence. It stands in for the reference's unidentified bold geometric sans.
