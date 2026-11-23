---
name: Budidaya di Halaman
version: 4
status: approved
colors:
  paper: "#F6F1DD"
  ink: "#202F27"
  sky: "#EEE6BD"
  hill: "#8EB69C"
  grass: "#76AD58"
  soil: "#9D5634"
  deepSoil: "#743E2C"
  sand: "#C9915D"
  water: "#5EB5BC"
  liner: "#2C7080"
  storm: "#515C72"
  roof: "#A64C35"
  yellow: "#FFD44D"
  white: "#FFF9E8"
  captionOutline: "#281D18"
typography:
  display:
    fontFamily: DM Sans
    fontWeight: 900
    letterSpacing: "-0.045em"
  body:
    fontFamily: DM Sans
    fontWeight: 500
    lineHeight: 1.45
  caption:
    fontFamily: DM Sans
    fontWeight: 800
    lineHeight: 1.12
spacing:
  unit: 8px
  frameSideInset: 88px
components:
  cover:
    referenceCanvas: 1080x1920
    fontSize: 76px
    lineHeight: 0.99
    top: 240px
    textAlign: center
    accent: "#FFD44D"
  thumbnail:
    referenceCanvas: 1080x1920
    safeArea: "0 420px 1080px 1080px"
    panelInset: 80px
    panelTop: 449px
    panelColor: "#281D18E6"
    panelRadius: 32px
    fontSize: 104px
    lineHeight: 0.98
    maxLines: 2
    textAlign: center
    accent: "#FFD44D"
  endCard:
    composition1x: 0.625s
    delivered: 0.5s
  priceTag:
    referenceCanvas: 1080x1920
    nail: 600px 594px
    width: 400px
    bodyTop: 636px
    background: "#FFF9E8"
    border: 4px solid #281D18
    radius: 18px
    sumSize: 38px
    totalSize: 54px
    totalBackground: "#FFD44D"
    noteSize: 28px
    drop: 0.2s
    swingSettle: 0.5s
    figurePop: 0.15s
    minHold1x: 3s
  caption:
    referenceCanvas: 1080x1920
    fontSize: 46px
    lineHeight: 1.12
    color: "#FFF9E8"
    activeColor: "#FFD44D"
    outlineColor: "#281D18"
    outlineWidth: 4px
    top: 1392px
    textAlign: center
    maxLines: 2
---

# Visual treatment

Build a flat illustrated world from horizontally layered sky, vegetation, soil, water, and infrastructure. A mild skew on rims and lids suggests depth. The soil section exposes the deciding action. Most of the frame consists of large flat shapes with restrained flecks, ripple marks and environmental detail around the active system. Warm clay and a pale sky establish the site. Clear water and dark liner separate the mechanism. Yellow belongs to the cover promise and the currently emphasized word.

The editable studies draw original 2D shapes on Canvas. The hexadecimal values, DM Sans family, dimensions, and timing ranges are selects for this board. They approximate the reference by function.

## Framing and captions

- Compose in 1080 × 1920 portrait. In a wide study place the ground seam near 38–46% of frame height with a house or vegetation behind it. Let a decisive vessel or interaction fill at least 40% of the frame width. A closer view may bring the seam upward to keep the whole action in view.
- Keep an uninterrupted line from the start of an action to its consequence. Retain the inlet, outlet, containment edge, or another landmark when reframing. Give roots, strata, or rocks a distinct texture so they read as context.
- Let the cover sit on a restrained dark scrim over a view of the result. Center the main phrase above the action and reserve yellow for its promise. In normal playback use short groups in the lower third and keep the action above or beside them. Preserve the 88 px side inset and reposition vertically if a flow path needs the space.
- Reveal letters as whole words in time with speech. Keep prior words visible in warm white and highlight the current word in yellow. Reset with the next phrase. Preserve the 46 px size and break or shorten a phrase if it needs more than two lines. Use the dark outline for reading over both water and soil.
- On the closing question's final ~2 seconds over the wide shot, suspend the per-word white reversion once the first word of the signature phrase **bikin di halaman** is spoken: keep each word of **bikin di halaman** highlighted in yellow (`#FFD44D`) as it is spoken so the full three-word phrase remains yellow through the end of the line, and fade in a subtle, small account handle (from `ACCOUNTS.json`) beneath the caption without obstructing the completed yard view.

## Price tag

- In the income scene, keep the finished system in view as the landmark and make the weighing or counting the decisive interaction, at least 40% of the frame width.
- Show the figures on a small paper tag hung by a string from a nail on the scale's beam, or on the nearest object in the scene. It stays beside the action and leaves the sky and the harvest open. It holds the sum (`10 kg × Rp25.000`), the total on a yellow chip, and a note with `estimasi`, the sale route and the price month.
- The tag drops onto its nail in 0.2 seconds and its swing dies out within half a second. Each figure pops in on the word that says it, in 0.15 seconds, and the tag grows downward as lines arrive. Hold the complete tag for at least 3 seconds at 1x (2.4 seconds delivered). Spoken numbers stay rounded; the tag shows the exact figures.

## Thumbnail and end card

- The thumbnail is a 1080 × 1920 PNG showing the finished system in a wide view, with one dark headline panel above it. Keep the headline and the decisive vessel inside the central 1080 × 1080 square (y 420–1500), so 3:4 and 1:1 grid crops still show both.
- Set the headline in DM Sans 900 at 104 px on two lines, warm white, with the promise in yellow. Use no other text, handle or badge.
- Draw it from the episode's own final wide view, so the thumbnail shows the system the film actually built.
- The last 0.625 seconds of the 1x composition (0.5 seconds delivered) is an exact copy of the thumbnail, entered on a hard cut after the closing line and its handle cue. Captions are cleared on the end card. On Instagram, Trypost points the cover at this frame (`cover_offset_ms` = delivered duration in ms − 250). YouTube and Facebook receive the PNG as a manual upload.

## Motion

- Author and review motion in the 1x composition; the delivered file plays it at 1.25x with pitch kept. Holds and read windows that only just pass at 1x feel short at delivery speed, so give reveals their full hold.
- Open on the first action within the first second. Change the scale or subject state when the viewer needs new information. Use a short push-in or cut for a reveal, lateral tracking for a route, and a slow return to wide for a completed system.
- Show one primary movement at a time. Give the viewer the source before a flow cue travels and hold the destination briefly after it arrives. Repeated fish, bubbles, and ambience stay subordinate to that movement.
- A brief shift in sky and ambient color conveys elapsed time. Hold the geometry steady through the simplest day-to-night transition. Weather and heat cues earn screen time by changing the next beat.
- Reserve dotted streams, ripples, bubbles, or heat marks for the processes they describe. Distinguish a schematic cue from the object itself with lighter value or a distinct edge. The style-board strip demonstrates still positions for a water route.

## Audio

Use warm Indonesian conversational narration to set the pace. Leave a short quiet space when a reveal needs room. Set the background music decision to `none` for the full episode, including the opening and closing. Use short sound effects where contact, dripping, flow, splashing, or a part settling into place benefits from an audible cue. Keep effects subordinate to the narration and let the gaps between cues stay quiet.
