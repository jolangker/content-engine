---
name: Di Balik Benda
version: 2
status: approved
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
  operations:
    - isolate
    - explode along real assembly axes
    - section or selectively reveal
    - macro inspection
    - actuate in causal order
    - reassemble into the whole
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

The default film is 90 seconds with 14–18 explanatory shots as a planning range. Use the detailed pacing and state-breakdown guidance in [EDITORIAL.md](EDITORIAL.md). Preserve the original palette, materials, and typography. The existing three static samples remain independent identity studies; they are not the complete 90-second storyboard.

Increase mechanical detail through intermediate states and purposeful macro views. For a critical interaction, plan 2–4 diagnostic poses when useful: before input, approaching contact, contact or transfer, and the result. Add a reset or return state only when the mechanism supports it. Separate annotation reveal, camera reframe, and the important mechanical event in time so the event remains readable.

An exploded view must expose useful part relationships. A macro must reveal actual contact, clearance, constraint, or transfer. A cutaway must preserve the orientation and location of the enclosing part. Avoid treating a simple scale change or rotation of the same undifferentiated object as a complete breakdown.

Camera moves change what can be understood: establish location, approach the relevant component, hold while it operates, then optionally return to context. Zoom must preserve a recognizable landmark. When an object is disassembled, keep its physical axis, orientation, and assembly relationships unless a clearly marked explanatory transformation is necessary.

Mechanical input and output follow the verified mechanism. Do not move stationary housings, stretch rigid gears, reverse causal order, or use a looping motion that contradicts the explanation. Indicate time slowing, exaggeration, invisibility, and non-scale spacing when relevant.

Stillness is a valid hold. No decorative ambient motion is required. A camera move, a part moving, and a label reveal should not compete for attention at the same moment. Timing is set from the explanation, not a universal duration or easing quota. The static board establishes poses only.

Plan the full operating path with enough time to observe it. Preserve the 90-second default after measuring audio; do not collapse back to a 30–40-second composition just because the narration is brief. A newly selected episode may explicitly override the default. More storyboard frames do not imply more frames per second.

## Audio concept

Clear Indonesian narration, sparse synchronized mechanical sounds, and optional low-level music. A click may confirm contact; a soft air or liquid cue may reinforce flow. Avoid invented sound that falsely implies a mechanism. No narration or sound has been synthesized for this board.

## Medium and production

These SVG studies demonstrate a 2.5D illustration vocabulary, not a limit on medium. True 3D is appropriate when camera rotation, occlusion, or complex assembly relationships matter. Technical 2D is appropriate when a section explains more clearly. Establish an approved style and motion test before promising a full animation pipeline for a new technique.

## Do and avoid

Do prioritize legibility, contact, continuity, material differentiation, and explanatory framing. Avoid generic decorative grids, arbitrary HUD numbers, unanchored lines, unsupported technical claims, and cards replacing the actual mechanism. Do not add parts merely to make an illustration look more complex.
