---
name: Behind the Screen
version: 2
status: proposed
visualMedium:
  construction: original 2D vector illustrations with bold contours, opaque fills and hard offset depth
  organizingPrinciple: explain digital relationships through gesture, object behavior and transfer
  characters: stylized hands and people when they establish a meaningful human action
  exclusions: permanent title-and-diagram layouts, paragraph overlays, fake product screenshots, decorative code, generic neon
colors:
  canvas: "#F0EFF8"
  surface: "#FFFFFF"
  ink: "#22213B"
  transit: "#4054E8"
  state: "#087C78"
  touch: "#F0B64A"
typography:
  display:
    fontFamily: Bricolage Grotesque
    fontWeight: 700
    fontSize: 88px
    letterSpacing: "-0.04em"
    lineHeight: 1.06
  body:
    fontFamily: Instrument Sans
    fontWeight: 400
    lineHeight: 1.35
  annotation:
    fontFamily: Instrument Sans
    fontWeight: 700
    fontSize: 38px
    lineHeight: 1.2
  caption:
    fontFamily: Instrument Sans
    fontWeight: 700
    fontSize: 44px
    lineHeight: 1.24
spacing:
  unit: 8px
  boardMargin: 72px
  frameSafeInset: 80px
components:
  frame:
    width: 1080px
    height: 1920px
    illustrationStage: "x=60..1020, y=180..1670"
    heroOccupancy: 70–90% of usable stage width or height, adjusted for full motion sweep
    textLayout: no permanent large title band
    lowerCaptionReserve: "y=1570..1740 when spoken captions are present"
    bottomQuietRegion: "y=1740..1920"
  illustration:
    principalContour: 6–8px
    smallDetailStroke: 4px
    shallowDepthOffset: "12–28px, ink at 16–23% opacity"
    groundShadow: flat ellipse, ink at 10–15% opacity
    silhouette: broad curves and meaningful overlaps; no decorative floating parts
  transfer:
    body: a distinct token, copy or signal whose identity persists along the route
    ribbonWidth: 48–78px
    contour: 6–10px beyond the ribbon body
    highlight: 9px surface at 20% opacity
    inverseStage: surface-colored route is allowed on a transit-colored ground
    meaning: illustrative motion path, not literal data plumbing or measured topology
  emphasisText:
    guide: usually 0–3 words visible at once; zero is welcome
    rule: identify a distinction only when the action and narration need an anchor
    maxLines: 1–2
  caption:
    region: "x=108..972, y=1570..1740"
    maxLines: 2
    textAlign: center
    phrasePolicy: short speech-aligned phrases; no second explanatory paragraph
    minimumArtClearance: 60px at the actual visible state
productionDefaults:
  durationSeconds: "60–90, adjusted to explanatory need"
  shotPlanning: "9–14 as a starting range; multiple meaningful action beats per shot"
  motionGuide: MOTION.md
  motionStatus: planned poses only; temporal continuity and audio are not verified
  accountTargets: ACCOUNTS.json
---

# Illustration carries the process

## Material and scale

Draw objects the audience can recognize: a hand holding a phone, a browser surface, a media picture, a receiving station. Deliberate illustrative metaphors can embody a hidden relationship. Keep the metaphor's scope in the production research notes, then let narration establish the exact technical meaning. Do not depict a metaphor as a literal hardware or protocol diagram.

Use the six exact colors above and opacity-derived quiet tones. The touch color may also color skin and media content; the palette is not a universal diagnostic legend. A traveling object and its destination must also be distinguishable by silhouette, pattern and location. The cobalt scene uses white routes and surfaces with ink contours so the relationship stays visible. Avoid glow, blur and glass as substitutes for illustrated form.

Supported weights are 400/700 only. Typography remains available, but no headline appears inside the current hero studies. If a future episode needs emphasis, start with 0–3 words and remove words before shrinking them. This is a proposed implementation guide for the user's “little text” preference, not an exact numeric instruction from the user.

## Staging and composition

Let the illustration take the principal field. Vary close gestures, transfer arcs, bounded local spaces, and foreground/background relationships. Do not repeat the same device-plus-box diagram with new labels. Keep enough context to recognize the source and destination when the camera follows a moving object.

Some inactive illustration may be cropped intentionally during a transition, but the active contact, transfer and resulting state must remain legible. The static studies use available space down to y≈1670 because they have no narration or captions. A narrated episode must reframe its art above the caption region and maintain the specified clearance; do not place a caption over these unchanged study layouts.

Caption speech in short synchronized phrases when narration is present. Keep captions as a separate lower layer, with a contrast surface if the stage changes color. Avoid an additional headline, diagram labels and caption all saying the same thing. These silent design studies require no invented subtitles.

## Visual storytelling checks

- A face/local approval remains visibly local; the proof is a distinct object with a different pattern.
- A copy separates while the source remains; do not accidentally animate a move as duplication.
- An external visit arrives before the local record is cleared. The wipe is bounded to the local surface, not the remote object.
- A nearby media copy can supply the viewer in the illustrated cache-hit case; a long pale route does not claim a measured physical distance or the nearest possible server.
- Responses follow arrival and are perceptible through geometry or pattern as well as color.

See MOTION.md for pose planning, proposed timing, choreography and rig handoff.

## Audio concept

Warm conversational English, with narration carrying definitions and qualifications. A visible gesture may receive a short dry contact cue; a transfer can have a restrained movement cue; the receiving state can land with a small material sound. Use sound to emphasize causality, not every moving detail. No mandatory music bed, alarm atmosphere or constant clicking. Voice, audio and mix remain ungenerated and require production-level resolution.
