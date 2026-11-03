---
name: Behind the Screen
version: 1
status: proposed
visualMedium:
  construction: original vector interface illustrations with opaque surfaces and shallow illustrated depth
  organizingPrinciple: separate a familiar screen into the local operation, exchange and destination relevant to the explanation
  exclusions: decorative neon, glass effects, particle fields, fake code, unsupported product screenshots
colors:
  canvas: "#F0EFF8"
  surface: "#FFFFFF"
  ink: "#22213B"
  transit: "#4054E8"
  resolved: "#087C78"
  input: "#F0B64A"
typography:
  display:
    fontFamily: Bricolage Grotesque
    fontWeight: 700
    fontSize: 96px
    letterSpacing: "-0.045em"
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
    fontSize: 46px
    lineHeight: 1.24
spacing:
  unit: 8px
  boardMargin: 72px
  frameSafeInset: 80px
components:
  frame:
    width: 1080px
    height: 1920px
    topicBaseline: 180px
    titleRegion: "x=80..1000, y=260..530"
    explanatoryStage: "x=80..1000, y=580..1500"
    bottomQuietRegion: "y=1740..1920"
    heroOccupancy: at least 55% of stage width or height with legible relevant relationships
  caption:
    region: "x=80..1000, y=1570..1740"
    maxLines: 2
    textAlign: center
    background: canvas
    minimumArtClearance: 60px
  surface:
    fill: surface
    cornerRadius: 24px
    outline: "4px ink at 20% opacity when not an active boundary"
    depthOffset: "12–24px toward lower right, ink at 12% opacity"
  route:
    activeStroke: 12px
    inactiveStroke: 6px
    inactiveOpacity: 0.25
    arrowHeadLength: 22px
    cornerRadius: 28px
    endPolicy: land on the source/destination edge, never terminate inside unrelated text
  boundary:
    stroke: 4px
    labelRequired: true
    nonColorCue: enclosing outline, line pattern and explicit local/remote wording
productionDefaults:
  durationSeconds: "60–90, adjusted to the explanatory need"
  shotPlanning: "9–14 as a starting range, not a fixed count"
  motionStatus: conceptual only; verify temporal legibility in production
  accountTargets: ACCOUNTS.json
---

# Open interfaces

## Material and hierarchy

The screen is a recognizable surface; a second plane or compartment identifies a different responsibility or location. Use shallow illustrated thickness for devices, service panels and data-bearing surfaces. Flatten deliberately for a boundary comparison or a route map. Realistic 3D, screenshots and stock footage are not defaults; a documented product capture may be used later if needed to establish a particular behavior.

Use the six exact colors above. Derive quiet lines and surfaces using opacity over the specified ground. Cobalt means an active transfer or attention route. Teal means a resolved or verified state. Amber means the current input or question; it is not a universal danger color. A role must also be communicated through wording, shape, direction or containment.

Bricolage Grotesque Bold is for the central question or concise explanatory statement. Instrument Sans is for UI, labels and spoken captions. Only bundled 400/700 weights are supported; do not synthesize 500/600/800. Keep labels at least 34px at native 1080 width; title size may adapt to content between 88 and 112px. Remove competing copy before reducing type.

## Composition

Preserve the relationships needed to answer the question. A local process stays inside its boundary, an external request crosses that boundary, and a retained copy remains visible while another location is inspected. Every critical path has a source, destination and direction. Routes may pass behind a foreground surface only when the entry/exit remains obvious. Do not cross a label with a route.

The title region and caption region are starting anchors rather than mandatory space reservations for every explanatory shot. Later shots may relinquish the large title to increase the diagram's scale. Keep speech captions in the declared lower region, short and synchronized, with at most two lines. Test actual platform overlays per production; the proposed safe region is not a universal platform guarantee.

The style-board's three studies are independent design demonstrations. Study 1 uses a local verification/service exchange, study 2 a device/website boundary, and study 3 a schematic cache-hit route. Their labels identify concepts, not every step of a complete technical protocol. Their source scopes are recorded in assets/SOURCES.md.

## Motion vocabulary — proposed, not playback-verified

- **Open:** preserve the screen's position and separate only the relevant layer by 96–160px over about 0.6 seconds, then hold for inspection. Opaque surfaces avoid unreadable layered text.
- **Follow:** carry a packet or proof marker along a fully visible directed route. Keep the active endpoints in view and distinguish request and response with labels and separate paths.
- **Resolve:** change the destination state after arrival. Shape or text changes accompany color; do not imply causal order solely through narration.
- **Return:** reassemble or zoom back to the same familiar screen and demonstrate the opening result. Preserve an anchor so the viewer can connect cause with consequence.

For a future 30fps production, 18–24 frames is a starting duration for a layer opening, 24–45 for a route traversal, and 12–18 for a compact state change. Timing must follow speech, reading and causal observation, not an untested quota. Use a cubic-bezier(0.22, 1, 0.36, 1) easing for plane movements; use linear travel where constant speed has explanatory value. Stillness is purposeful during reading or close inspection. Do not pulse or drift unrelated elements.

## Audio — proposed

Warm, articulate conversational English with space between causal steps. Resolve an appropriate English narration voice during production rather than assuming the root voice matches this market. AUDIO.json currently inherits the configured default and does not generate audio.

Use restrained, dry interface sounds tied to a visible tap, transfer, boundary crossing or resolved state, allowing silence when it teaches better. A quiet electronic bed is optional and must yield to speech. Avoid constant typing, alarm cues and a generic cybersecurity mood. Record actual cue timing, mix and exceptions during production.

## Review checks

At phone size, identify the initiating action, active relationship and result without relying on a paragraph of copy. Temporarily hide the display headline to test the diagram's communication. Check native-size and phone-size labels, actual font loading, path endpoints, local/remote containment, source scopes and platform overlay clearance. Reverify motion, captions and sound through actual playback when a production is requested.
