---
name: Budidaya di Halaman
version: 5
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

Build a living, flat-illustrated 2.5D backyard world from depth-separated sky, distant horizon, yard midground, soil cutaway, water, and infrastructure. A mild skew on rims and lids suggests depth, while true depth parallax during camera moves gives the yard physical space. The soil section exposes the deciding action. Most of the frame consists of crisp flat shapes with tactile surface marks, moving water glints, swaying foliage, and reactive weather around the active system. Warm clay and a pale sky establish the site. Clear water and dark liner separate the mechanism. Yellow belongs to the cover promise, the price-tag total, and the currently emphasized word.

The editable studies draw original 2D shapes on Canvas. The hexadecimal values, DM Sans family, dimensions, and timing ranges are selects for this board. They approximate the reference by function while upgrading the world to a living, event-reactive system.

## Living world and parallax

Keep the yard visibly alive in every frame without competing with the active mechanism or the lower caption band:

- **Four depth planes (2.5D parallax):** Drive background layers from the active camera transform `(x, y, zoom)` at distinct parallax multipliers so every push-in, pan, and pull-out reveals spatial depth:
  - **Plane 0 — Sky & Celestial (`0.18×` camera motion):** Time-of-day sky gradient, drifting multi-layer clouds (thickening and darkening before rain), moving sun/moon arc, subtle midday heat-shimmer bands, and faint night stars.
  - **Plane 1 — Distant Horizon (`0.45×`):** Rolling hills, distant tree ridges, and occasional tiny silhouette birds gliding across the upper sky.
  - **Plane 2 — Yard Midground (`0.80×`):** Neighborhood house (warm window glow and soft porch light turning on at dusk/night), wind-swaying banana leaves and backyard shrubs (sway amplitude and frequency increase during storms), yard fence/hedges, adjacent garden beds that grow visibly lusher over elapsed months, and delicate yard micro-life (an occasional small butterfly/dragonfly near daytime leaves, soft fireflies at night).
  - **Plane 3 — Hero Cutaway & Foreground (`1.00×`, optional wide-shot edge blades at `1.14×`):** Soil strata, active pond/vessel/bed, keeper, tools, continuous gentle surface ripples and glints, reactive wet soil darkening under leaks or rain, and optional thin foreground grass silhouettes tucked at the far left/right edges on wide shots (kept clear of the caption band).
- **Reactive lighting and weather:** Elapsed time and weather shift the whole environment together — sky gradient, sun/moon position, ambient wash, directional shadows, foliage sway, house window glow, and wet ground darkening — rather than swapping a single static tint.
- **Figure-ground & caption discipline:** Background motion stays lower-contrast, lower-saturation, and slower than the primary hero interaction. The lower soil strata behind the caption band (`y 1380–1570`) stay calm, deep, and free of high-contrast moving shapes so 46 px captions remain effortlessly legible on phones.

## Framing and captions

- Compose in 1080 × 1920 portrait. In a wide study place the ground seam near 38–46% of frame height with a house and swaying vegetation behind it. Let a decisive vessel or interaction fill at least 40% of the frame width. A closer view may bring the seam upward to keep the whole action in view.
- Keep an uninterrupted line from the start of an action to its consequence. Retain the inlet, outlet, containment edge, or another landmark when reframing. Give roots, strata, or rocks a distinct texture so they read as context.
- Let the cover sit on a restrained dark scrim over a view of the result. Center the main phrase above the action and reserve yellow for its promise. In normal playback use short groups in the lower third and keep the action above or beside them. Preserve the 88 px side inset and reposition vertically if a flow path needs the space.
- Reveal letters as whole words in time with speech. Keep prior words visible in warm white and highlight the current word in yellow. Reset with the next phrase. Preserve the 46 px size and break or shorten a phrase if it needs more than two lines. Use the dark outline for reading over both water and soil.
- On the closing question's final ~2 seconds over the wide shot, suspend the per-word white reversion once the first word of the signature phrase **bikin di halaman** is spoken: keep each word of **bikin di halaman** highlighted in yellow (`#FFD44D`) as it is spoken so the full three-word phrase remains yellow through the end of the line, and fade in a subtle, small account handle (from `ACCOUNTS.json`) beneath the caption without obstructing the completed yard view.

## Price tag

- In the income scene, keep the finished system in view as the landmark and make the weighing or counting the decisive interaction, at least 40% of the frame width.
- Show the figures on a small paper tag hung by a string from a nail on the scale's beam, or on the nearest object in the scene. It stays beside the action and leaves the sky and the harvest open. It holds the sum (`10 kg × Rp25.000`), the total on a yellow chip, and a note with `estimasi`, the sale route and the price month.
- Anchor the price tag in world/camera space (matching the beam nail's projected screen transform) so subtle camera settles and fish-drop reactions never detach the tag from its nail.
- The tag drops onto its nail in 0.2 seconds and its swing dies out within half a second. Each figure pops in on the word that says it, in 0.15 seconds, and the tag grows downward as lines arrive. Hold the complete tag for at least 3 seconds at 1x (2.4 seconds delivered). Spoken numbers stay rounded; the tag shows the exact figures.

## Thumbnail and end card

- The thumbnail is a 1080 × 1920 PNG showing the finished system in a wide view, with one dark headline panel above it. Keep the headline and the decisive vessel inside the central 1080 × 1080 square (y 420–1500), so 3:4 and 1:1 grid crops still show both.
- Set the headline in DM Sans 900 at 104 px on two lines, warm white, with the promise in yellow. Use no other text, handle or badge.
- Draw it from the episode's own final wide view, so the thumbnail shows the system the film actually built.
- The last 0.625 seconds of the 1x composition (0.5 seconds delivered) is an exact copy of the thumbnail, entered on a hard cut after the closing line and its handle cue. Captions are cleared on the end card. On Instagram, Trypost points the cover at this frame (`cover_offset_ms` = delivered duration in ms − 250). YouTube and Facebook receive the PNG as a manual upload.

## Motion and event-driven camera

- Author and review motion in the 1x composition; the delivered file plays it at 1.25x with pitch kept. Holds and read windows that only just pass at 1x feel short at delivery speed, so give reveals their full hold.
- Open on the first action within the first second.
- **Event-driven camera choreography (beat-level, not just scene-level):** Treat the camera as an active observer of every interaction inside a scene, not a static tripod that only changes on cuts:
  - **Action push / punch-in (`+10% to +25%` zoom + target pan):** Whenever a problem surfaces or a key component installs (driving stakes, exposing a leak, seating a valve, stretching a net, landing harvest), move cleanly toward the interaction with a snappy ease-out (`outExpo` / `outCubic`, `0.25–0.45 s`), then breathe back slightly (`power2.inOut`) to show the effect on the whole system.
  - **Follow-the-action tracking:** Track laterally or diagonally along moving routes — hose filling, tarp/paranet pulling, runoff pipes, scoop transfers, and fish drops from basin to scale — within the same beat.
  - **Tactile micro-impact settle:** Synchronize physical impacts (digging strokes, stake hammering, bricks/pipes landing, fish landing on the scale pan, heavy rain/thunder onset) with a damped `2–5 px` vertical/directional micro-impulse (`0.12–0.18 s`, damped cosine) paired with the matching SFX transient so 2D actions feel grounded and weighty.
  - **No dead-freeze holds:** No beat longer than `3.0 s` holds a completely motionless camera (`motion.max_static_seconds: 3.0`). Even wide establishing and closing views carry a gentle living drift (`1.5–4%` zoom/pan settle) that activates depth parallax while keeping typography readable.
- Show one primary movement at a time. Give the viewer the source before a flow cue travels and hold the destination briefly after it arrives. Repeated fish, bubbles, and living-world ambience stay subordinate to that primary action.
- Reserve dotted streams, ripples, bubbles, or heat marks for the processes they describe. Distinguish a schematic cue from the object itself with lighter value or a distinct edge.

## Audio

Use warm Indonesian conversational narration to set the pace. Leave a short quiet space when a reveal needs room. Set the background music decision to `none` for the full episode, including the opening and closing.

- **Board organic SFX library (hybrid sourcing):** Every production inherits the board's curated organic SFX kit in `assets/sfx/` (`manifest.json` and `CREDITS.md`), covering construction/material contact (digging, wood stakes, tarp rustle, net pull, PVC fitting snap), water and weather (pouring, splashing, draining, aerator bubbles, rain shower), yard interactions (pellet scatter, scale chain, gentle yard air), camera movement (`cam-whoosh`), and payoff cues (`tag-click`, `tag-pop`). Source new episode-specific effects **hybrid**: royalty-free **CC0 / CC BY** (Openverse/Freesound and bundled Pixabay) first, trimmed and loudness-balanced with FFmpeg; use **ElevenLabs Sound Effects** only when an essential organic cue has no clean royalty-free match and generation is authorized.
- **Event-locked foley density:** Pair every visible build interaction, failure reveal, water/weather onset, camera punch-in/pan, and price-tag pop with 1–2 frame-accurate organic micro-SFX cues (target roughly `25–45` timed cues across a `90–112.5 s` 1x episode, ~1.5–2.5 cues per event) rather than sparse UI clicks.
- **Short diegetic condition beds:** While `bgm` remains `none`, active environmental states (rain shower, continuous pouring/draining, running aerator, or ultra-gentle backyard morning/evening breeze on wide establishing/closing views) may layer a cleanly faded diegetic ambience bed kept strictly under speech (`~ −22 to −28 dB` below narration, passing the `>= 3.0 dB` vocal-band SNR check).
- **Audible yet subordinate mix:** Keep foley clearly audible at phone playback volume (not buried below perception) while keeping narration firmly dominant and avoiding any transient that masks spoken syllables.
