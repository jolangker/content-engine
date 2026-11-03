---
name: Behind the Screen
version: 3
status: approved
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
    fontSize: 84px
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
    fontSize: 54px
    lineHeight: 1.24
spacing:
  unit: 8px
  boardMargin: 72px
  frameSafeInset: 80px
components:
  frame:
    width: 1080px
    height: 1920px
    titleRegion: "x=80..1000, y=120..330"
    illustrationStage: "x=80..1000, y=350..1530"
    heroOccupancy: 70–90% of usable stage width or height, adjusted for full motion sweep
    textLayout: title on the opening and meaningful sections; subtitles in a separate lower band
    lowerCaptionReserve: "y=1616..1728"
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
    guide: usually 0–3 supplementary emphasis words; does not limit the title or spoken subtitles
    rule: identify a distinction only when the action and narration need an anchor
    maxLines: 1–2
  caption:
    interpretation: displayed karaoke treatment accepted by the user's cocok response on 2026-11-03
    region: "x=108..972, y=1616..1728"
    baseline: 1690px
    panelColor: ink
    panelRadius: 24px
    panelPaddingX: 28px
    inactiveWordColor: surface
    activeWordColor: ink
    activeWordBackground: touch
    activeWordRadius: 14px
    activeWordPaddingX: 12px
    activeWordHeight: 80px
    activeWordsAtOnce: 1
    wordGap: actual font space advance plus 16px
    maxLines: 2
    textAlign: center
    phrasePolicy: typically 3–6 words; full phrase stays while the active word changes; segment at natural speech boundaries
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

Supported weights are 400/700 only. The user explicitly requires titles and subtitles. Show a short readable title on the opening and meaningful section changes; do not remove it under the earlier little-text guide. Titles use Bricolage Grotesque 700; subtitles use Instrument Sans 700. Keep extra labels sparse. The 0–3-word guide applies only to supplementary emphasis.

## Staging and composition

Let the illustration take the principal field. Vary close gestures, transfer arcs, bounded local spaces, and foreground/background relationships. Do not repeat the same device-plus-box diagram with new labels. Keep enough context to recognize the source and destination when the camera follows a moving object.

Some inactive illustration may be cropped intentionally during a transition, but the active contact, transfer and resulting state must remain legible. The current studies reframe the v2 artwork with translate(70,80) and uniform scale 0.86, preserving proportions and leaving at least 60px above the subtitle panel. A future animation must fit its full motion sweep to the same clearances rather than assume a static fit proves it.

The accepted karaoke treatment keeps a short phrase in a dark rounded panel. Inactive words are white; exactly one active word has an amber rounded highlight and dark text. The phrase and line breaks stay still during that phrase. Advance the highlight at measured word onsets from the actual narration, including pauses; do not space highlights evenly or bounce the text. Keep the complete spoken content accessible across successive phrases.

The user wrote “katole style” and subsequently accepted the displayed karaoke interpretation with “cocok” on 2026-11-03. This accepts the treatment without claiming an identified external reference. The static samples and four subtitle states use illustrative copy and have no narration or verified word timings. Additional movement is reserved for the illustrations.

## Visual storytelling checks

- A face/local approval remains visibly local; the proof is a distinct object with a different pattern.
- A copy separates while the source remains; do not accidentally animate a move as duplication.
- An external visit arrives before the local record is cleared. The wipe is bounded to the local surface, not the remote object.
- A nearby media copy can supply the viewer in the illustrated cache-hit case; a long pale route does not claim a measured physical distance or the nearest possible server.
- Responses follow arrival and are perceptible through geometry or pattern as well as color.

See MOTION.md for pose planning, proposed timing, choreography and rig handoff.

## Audio concept

Warm conversational English, with narration carrying definitions and qualifications. A visible gesture may receive a short dry contact cue; a transfer can have a restrained movement cue; the receiving state can land with a small material sound. Use sound to emphasize causality, not every moving detail. No mandatory music bed, alarm atmosphere or constant clicking. Voice, audio and mix remain ungenerated and require production-level resolution.
