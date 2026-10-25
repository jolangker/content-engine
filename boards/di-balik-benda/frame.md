---
name: Di Balik Benda
version: 4
status: approved
visualMedium:
  lock: 2.5D illustration only
  construction: layered vector or raster parts with illustrated volume, depth order, and consistent shading
  camera: pan, push, pull, and restrained layer parallax within the established view
  exclusions: standalone flat 2D scene treatment, true 3D scenes, mixed-medium sequences, arbitrary camera orbits
productionDefaults:
  durationSeconds: 90
  durationTolerance: one output frame
  explanatoryShots:
    targetMin: 14
    targetMax: 18
    startingPoint: 16
    policy: planning range, adaptable to mechanism
  diagnosticPosesPerCriticalAction: 2–4 when needed
  frameRatePolicy: retain the episode frame rate; shot density is independent of fps
  topicPreference: multiple interacting subassemblies and linked causal stages
  causalInteractions: 3–5 as a richness guide, not a part-count quota
  choreographyGuide: SHOT-DIRECTION.md
  repetitionReview: flag repeated framing plus operation across three or more shots
  interactionCoverage: every narrated causal interaction has visible input, contact or transfer, and response
  attentionGuide: cue the active component before the event and carry emphasis to the affected component
  sfxCoverage: every designed interaction event has a synchronized cue or a documented intelligibility exception
colors:
  canvas: "#ECEEE9"
  surface: "#F8F9F5"
  ink: "#172B3B"
  muted: "#536775"
  line: "#CDD4D4"
  input: "#C94422"
  active: "#2459C4"
  output: "#167580"
  metal: "#A6B4BE"
typography:
  display:
    fontFamily: Manrope
    fontWeight: 800
    letterSpacing: "-0.055em"
  body:
    fontFamily: Manrope
    fontWeight: 500
    lineHeight: 1.45
  annotation:
    fontFamily: IBM Plex Mono
    fontWeight: 400
    lineHeight: 1.5
spacing:
  unit: 8px
  boardMargin: 64px
  sampleSafeInset: 32px
components:
  object:
    material: satin polymer, brushed metal, clear sectional housing
    contour: clean silhouettes and consistent mechanical axes
  callout:
    stroke: 1.5px
    termination: dot anchored to the actual component
    label: concise function or part name
  section:
    treatment: exposed internal surface, optional hatch on cut solid material
  ghostHousing:
    opacity: 0.15
    purpose: retain the location and silhouette of the enclosing assembly
motion:
  status: conceptual
  principle: motion explains a mechanical relationship
  engagement: visible action and reaction, progressive attention handoffs, varied event timing, and readable result holds
  operations:
    - isolate
    - explode along real assembly axes
    - section or selectively reveal
    - macro inspection
    - actuate in causal order
    - reassemble into the whole
audio:
  narration: clear Indonesian, foreground priority
  sfx: required, event-synchronized, material-aware interaction cues
  cueTypes: physical mechanism sounds and distinct editorial attention cues
  music: optional, below narration and interaction cues
  review: event cue sheet, frame-aligned onsets, full-speed listening, and phone-speaker intelligibility
---

# Overview

The object is the scene. Its hidden spatial relationships supply the visual interest. The pale bench makes tiny gaps, silhouettes, and colored active parts legible; selective shaded volume makes isolated parts recognizable without a decorative dashboard.

## Palette and semantic color

Orange marks the input, applied force, or initiating action. Blue marks the currently inspected component or contact. Teal marks the resulting motion or outgoing flow. Combine color with labels, direction, and sequence; never rely on color alone. Do not paint every part with a semantic accent. Base materials remain mineral, polymer, and metal.

Colors are board identity tokens. Lighting may shade materials while preserving their semantic identity. A dark interior view is allowed when it materially improves visibility; it is not a mandatory alternating scene treatment.

## Typography

Manrope 800 gives compact, confident titles; Manrope 500 supplies short explanations. IBM Plex Mono 400 identifies parts and inspection states. Use the bundled local font files. The technical register comes from the objects and annotation precision rather than an all-caps HUD.

In the 508 × 903 sample studies, titles are 42px and explanatory copy is 23px. Scale these with the composition; on a 1080px-wide export they correspond to approximately 89px and 49px. Validate on a phone-sized preview. Board metadata is not intended to be burned into episodes.

## Composition

- Keep one dominant object or mechanism per explanatory beat; multiple focal points are optional.
- Favor a coherent assembly axis and preserved component identity across transformations.
- Use space to separate parts and reveal connections. Complexity determines density.
- Put labels close to components with short leaders that terminate on those components.
- Reserve caption and platform-safe areas when the episode destination is known. The samples leave a lower area but are not a universal platform overlay specification.
- Choose framing for each job: context, exploded assembly, cutaway, macro, comparison, causal operation, or whole-system return. Do not force every operation into every episode.

## Motion and camera

Version 4 locks the visual language to 2.5D and makes interaction, attention handoffs, and event-synchronized SFX required planning decisions. Keep v3's preference for mechanisms with multiple interacting functional parts and linked stages. Use [SHOT-DIRECTION.md](SHOT-DIRECTION.md) for the shot map, coordinated motion, attention and sound cue sheet, and repetition review. Several coupled components may move together; retain one clear explanatory question per beat.

Mix whole-system operation, assembly reveal, interior section, contact macro, progressive causal handoff, coordinated action, and useful state comparison according to the mechanism. Changes in framing and rhythm must reveal a new relationship. Preserve operating state across cuts rather than replaying the same short cycle with new text.

The default film is 90 seconds with 14–18 explanatory shots as a planning range. Use the detailed pacing and state-breakdown guidance in [EDITORIAL.md](EDITORIAL.md). Preserve the original palette, materials, and typography. The existing three static samples remain independent identity studies; they are not the complete 90-second storyboard.

Increase mechanical detail through intermediate states and purposeful macro views. For a critical interaction, plan 2–4 diagnostic poses when useful: before input, approaching contact, contact or transfer, and the result. Add a reset or return state only when the mechanism supports it. Separate annotation reveal, camera reframe, and the important mechanical event in time so the event remains readable.

An exploded view must expose useful part relationships. A macro must reveal actual contact, clearance, constraint, or transfer. A cutaway must preserve the orientation and location of the enclosing part. Avoid treating a simple scale change or rotation of the same undifferentiated object as a complete breakdown.

Camera moves change what can be understood: establish location, approach the relevant component, hold while it operates, then optionally return to context. Use 2.5D pans, pushes, pulls, and restrained layer parallax. Zoom must preserve a recognizable landmark. Reveal an occluded relation through a sectional illustration or an explicitly oriented alternate 2.5D view. When an object is disassembled, keep its physical axis, orientation, and assembly relationships unless a clearly marked explanatory transformation is necessary.

Mechanical input and output follow the verified mechanism. Do not move stationary housings, stretch rigid gears, reverse causal order, or use a looping motion that contradicts the explanation. Indicate time slowing, exaggeration, invisibility, and non-scale spacing when relevant.

Stillness is a valid hold. No decorative ambient motion is required. A camera move, a part moving, and a label reveal should not compete for attention at the same moment. Timing is set from the explanation, not a universal duration or easing quota. The static board establishes poses only.

Each narrated causal interaction must show its input, decisive contact or transfer, and visible response. Lead attention with a brief component emphasis or anchored force/path cue, animate coupled parts according to their actual dependency, then hold the changed state long enough to read. Vary supported actions and event timing across the chain. Increase observable cause and effect throughout the film; annotation entrances alone do not satisfy the interaction requirement. Viewer engagement here means following the mechanism in a linear video, without adding clickable controls or simulated taps.

Plan the full operating path with enough time to observe it. Preserve the 90-second default after measuring audio; do not collapse back to a 30–40-second composition just because the narration is brief. A newly selected episode may explicitly override the default. More storyboard frames do not imply more frames per second.

## Audio concept

Clear Indonesian narration with an active, synchronized interaction sound layer and optional low-level music. Every designed interaction event needs a cue: actuation, meaningful contact, engagement, release, causal handoff, or flow onset/change/stop when present. Sustained motion can share a continuous sound whose changes follow the action; do not add a separate transient to every frame or tooth.

Choose material-aware physical cues for actual operation and distinct, softer editorial cues for a cutaway, assembly separation, or attention handoff. Record editorial cues as stylized guidance, not evidence that a silent internal event is literally audible. Shape a cue to the action: onset at contact, body during travel or flow, and release tail at the stop. Avoid identical clicks on every action or a generic whoosh on every transition.

Plan cues with the storyboard, align each onset to its visible event within one output frame unless an intentional lead or lag is recorded, and review the mixed playback at normal speed. Narration remains intelligible; control overlapping cues and reserve brief quiet for observation. A major interaction left silent requires a recorded reason such as masking or a deliberately quiet contrast. SFX are part of the production deliverable, not an optional final garnish. No audio is generated by this board revision.

## Medium and production

Use 2.5D illustration throughout every episode selecting v4: layered vector or raster parts, clean contours, illustrated side faces or thickness, consistent shading, overlap, and restrained parallax. Cutaways, exploded assemblies, macros, and state comparisons all retain this treatment. Flat labels, arrows, and captions may support the illustrated object. Standalone flat 2D diagram scenes, true 3D scenes, and mixed-medium sequences are outside this visual lock. If a relation needs another angle, author a coherent alternate 2.5D view with shared landmarks. An episode needs an explicit user override to change the medium.

## Do and avoid

Do prioritize legibility, contact, continuity, material differentiation, and explanatory framing. Avoid generic decorative grids, arbitrary HUD numbers, unanchored lines, unsupported technical claims, and cards replacing the actual mechanism. Do not add parts merely to make an illustration look more complex.
