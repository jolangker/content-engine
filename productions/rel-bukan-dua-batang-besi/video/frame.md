---
board: bongkar-sistem
version: 2
status: proposed-for-review
format:
  width: 1080
  height: 1920
  aspect_ratio: '9:16'
colors:
  board_paper: '#F8F4E8'
  ink: '#173B42'
  sky: '#C5D5D8'
  cream: '#FFF5DE'
  grass: '#52684A'
  grass_light: '#6A8052'
  earth: '#75604A'
  deep_earth: '#875B43'
  sand: '#D7B286'
  stone: '#696B64'
  steel: '#8E9997'
  teal: '#3C6261'
  flow_cool: '#2B9FCE'
  flow_warm: '#E56E43'
  yellow: '#CCA84F'
  white: '#F7F5EB'
  dark_material: '#25494C'
  skin: '#AB8567'
  roof: '#8F5140'
  timber: '#65513E'
  plaster: '#C6C1AD'
  concrete: '#9D9B91'
  water_material: '#4292AA'
typography:
  primary:
    family: Barlow
    weights:
    - 400
    - 700
    - 900
    files:
    - assets/barlow-regular.ttf
    - assets/barlow-bold.ttf
    - assets/barlow-black.ttf
  technical:
    family: IBM Plex Mono
    weights:
    - 400
    files:
    - assets/ibm-plex-mono.ttf
  caption:
    family: Barlow
    weight: 700
    size_px: 58
    line_height: 1.1
    tracking_em: -0.015
  emphasis:
    family: Barlow
    weight: 900
    size_px: 92
    line_height: 0.98
  label:
    family: Barlow
    weight: 700
    size_px: 34
spacing:
  safe_left_px: 72
  safe_right_px: 150
  safe_top_px: 160
  safe_bottom_px: 290
  caption_padding_x_px: 26
  caption_padding_y_px: 17
components:
  caption:
    foreground: '#173B42'
    background: '#FFF5DE'
    radius_px: 16
    max_lines: 2
  series_mark:
    text: BONGKAR SISTEM
    foreground: '#173B42'
    accent: '#CCA84F'
  character:
    cap: '#CCA84F'
    work_shirt: '#3C6261'
    trousers: '#65513E'
    boots: '#283C3D'
    proportions: adult, approximately 1.76 m in current illustrative source
visual_style:
  setting: continuous full-screen environment
  rendering: semi-realistic technical visualization
  camera: perspective with authored in-shot motion
  geometry: real-scale construction and adult human proportions
pacing:
  default_seconds: 90
  working_range_seconds:
  - 75
  - 95
  minimum_exclusive_seconds: 60
  meaningful_steps_at_90_seconds:
  - 20
  - 26
---

# A place you enter, a change you notice

V2 replaces the isolated toy diorama with semi-realistic architectural/technical imagery inside a continuous populated environment. It responds directly to [FEEDBACK-v2.md](FEEDBACK-v2.md). Palette values are material albedo inputs and exact UI colors; illumination/view transforms change rendered material pixels.

## Environment and framing

Ground, buildings, streets/yards, vegetation, props, and context extend beyond the frame and the camera path. Show foreground, subject, and background with useful depth and material differences. No floating slab, visible base outline, blank color moat, or large empty caption band. The sky may appear as part of a real composition. Context may be cropped at the edges; essential actions remain visible.

A close-up still has an environment: connected pipes, a nearby wall, the receiving surface, and out-of-focus context establish where the detail belongs. A local cutaway exposes the relevant region while the surrounding place continues. Do not make the whole world a cut-out miniature by default.

## Materials and scale

Use restrained natural colors, modest physical edge radii, real wall/roof thicknesses, constructed frames/eaves/fittings, varied roughness, readable metallic/plastic/concrete surfaces, and proportionate wear/texture. Avoid inflated bevels, capsule limbs, giant heads/eyes, clay blobs, and candy saturation as the general identity. The new stills are original procedural 3D architectural studies, not photographs or a claim of photorealism. Improve real-scale geometry and materials before applying a grade.

The recurring builder keeps a yellow cap/hardhat and teal clothing at adult proportions. Clothing details and silhouette establish identity. Humor stays in the premature celebration, situational reversal, and prop timing; it does not require a toy-shaped human or an inaccurate mechanism. Comic scale exaggeration is permitted only as an overt theatrical convention.

## Noticeable state change

Each important intervention needs before, action/contact, and an observable result. Change both framing and staging when the event is too small at phone size. The action target should be dominant for the critical moment; a useful starting point is roughly one quarter or more of the phone-frame width for detailed contact. Move the camera closer rather than falsifying travel or part size.

After the action, preserve the changed state. A short result hold lets the audience register it. Selective labels and schematic flow notation clarify the physical event, never substitute for it. Blue/orange thermal notation retains its meaning within a topic. The new water study uses visible material flow, not thermal coding.

## Camera and composition

Use perspective and authored travel inside shots: dolly approach, flow/subject tracking, useful side reveal, low/eye detail, overhead/section, pull-back to the whole, and motivated zoom-in/out. Mix these by explanatory purpose. Cuts connect views but cannot supply all motion. Do not reset the camera per subtitle or apply one continuous generic zoom to the entire film.

Critical contact may need a brief settled view even in a fast piece. Show depth, occlusion and parallax on spatial moves. Maintain physical state, screen direction and component connections across views. The majority-of-shots camera target and verification rules are in PRODUCTION-STANDARDS.md; static board images do not prove this temporal requirement.

## Typography and safe zones

Retain local Barlow 400/700/900 and IBM Plex Mono 400. Spoken captions use cream backing and ink text, 58 px at 1080 x 1920 as the starting size. Use short meaningful groups, at most two lines. Avoid permanent scene titles, repeated explanatory labels, and production disclaimers occupying the viewing field unless they communicate a necessary episode limitation. Review labels in the board are not mandatory episode overlays.

Essential text and actions must survive the actual destination UI. The initial safe inset values remain working guidelines. Let scenery bleed to the edges; captions stay screen-anchored while the camera moves. Choose a calm region that does not cover the important contact. Do not shrink the world to preserve an oversized text reservation.

## Pacing and audio

Default 90 seconds, typically 75-95, always strictly above 60 unless the user changes that requirement. Roughly 20-26 meaningful visual steps at 90 seconds is a planning target. Add evidence-backed intermediate operations and consequences, not padding. Fit narration to the richer action map. The original six long static views are not the baseline.

Discrete interaction SFX are required where audible events warrant them. Rain is ambience; BGM remains optional. Pair motion/contact/result with appropriate cues, exact triggers and export proof. See MOTION-AND-AUDIO.md and PRODUCTION-STANDARDS.md. No new audio or animation has been generated in this static-board revision.
