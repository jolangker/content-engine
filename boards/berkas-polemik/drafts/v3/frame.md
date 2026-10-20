---
version: "3-draft"
name: Berkas Polemik
description: Visual-first archival identity, revised after feedback about excessive text.
unit: "1080 × 1920 vertical frame"
principle: "One thought, one dominant visual, minimal frame copy."
colors:
  bg: "#121110"
  paper: "#EAE0D0"
  ink: "#1A1816"
  red: "#C32822"
  steel: "#7C756B"
  tape: "#D4A359"
  surface: "#1D1B19"
color-modes:
  normal:
    background: "#121110"
    text: "#EAE0D0"
    scenes: 14
  dramatic-reversed:
    background: "#EAE0D0"
    text: "#121110"
    secondary-text: "#1A1816"
    large-display-accent: "#C32822"
    scenes: 2
    placement: "Two script-driven dramatic beats; no fixed scene numbers."
typography:
  display:
    fontFamily: Space Grotesk
    weight: 700
    fontSize: "108px"
    lineHeight: 1.04
    letterSpacing: "-0.035em"
  source-detail:
    fontFamily: Newsreader
    weight: 400
    fontStyle: italic
    fontSize: "118px in the 900-unit illustration viewBox"
  metadata:
    fontFamily: Space Mono
    weight: 700
    fontSize: "32px"
  simulation-label:
    fontFamily: Space Mono
    weight: 700
    fontSize: "34px"
    lineHeight: 1.35
spacing:
  essential-left: "84px"
  essential-right: "150px"
  essential-top: "160px"
  essential-bottom: "380px"
  headline-top: "324px"
  visual-top: "578px"
  visual-width: "846px"
  visual-height: "900px"
  locator-reserve-top: "1490px"
  caption-reserve-top: "1600px"
  caption-reserve-bottom: "1780px"
content:
  target-duration-seconds: 90
  primary-storyboard-scenes: 16
  format-status: "User confirmed; approximately 90 seconds, exactly 16 scenes."
  study-headline-words: "3–4"
  default-headline-max-words: 6
  explanatory-paragraphs-per-frame: 0
  dominant-visuals-per-frame: 1
  narrative-labels: "Only where needed to identify the depicted relationship."
components:
  document-pair:
    description: "Offset paper objects with the same mark position identified on each; show the difference directly."
  loupe:
    description: "One enlarged source detail with contextual line-work receding; no paragraph around the lens."
  evidence-gap:
    description: "A visible empty region within an illustrated document field, explicitly a metaphor."
---

# Visual-first frame specification

## Confirmed duration and scene count

Target approximately 90 seconds across exactly 16 primary storyboard scenes, as specified by the user on 20 October 2026. Average duration is 5.625 seconds; the editorial pacing template varies scene holds from 4–7 seconds. Each numbered scene has one dominant visual and minimal copy. Internal changes of focus can develop that visual without adding a primary scene. The current three studies illustrate the identity and are not a sixteen-scene storyboard.

## Feedback and hierarchy

The user found v2 too text-heavy and insufficiently visual. Treat this feedback as a change to the frame construction, not a request to merely shorten paragraphs. Start each frame from the relationship to show: a difference, a detail, an interval, a location, or a missing link. Pick an object-based illustration, source crop, map, chronology, or relationship diagram as appropriate to that episode's evidence. Do not use a stack of explanation cards as the default.

In these studies, a two-line headline occupies the upper portion and a single SVG illustration takes 900px of the 1380px essential content height. The illustration must make the idea graspable before its caption is read. Use a single headline of up to six words by default; the three current headlines each use three. Source labels, necessary qualifications, and accessibility needs can override a numeric text cap.

No explanatory paragraph appears inside the study frames. Put longer explanation into narration and production notes. Spoken captions, when produced, need their own reserved space and timing; do not simultaneously place a full spoken sentence, a headline repeating it, and a body paragraph on screen.

## Object and visual language

Use paper geometry, restrained depth, readable crops, physical overlap, and purposeful annotation. A geometric line simulates document context, not readable evidence. Avoid replacing paragraphs with decorative icons that convey no actual relationship. Each visual must perform an explanatory job.

- Document pair: A and B share a material language and comparable mark positions. One visible mark and one empty counterpart carry the difference; no checklist or text comparison is needed.
- Loupe: the single simulated word “ditunda” is enlarged, while surrounding line-work recedes. In a researched episode retain the original crop and context, with an accurate transcription or translation if needed.
- Gap: two fragments and an empty middle make incompleteness visible. The torn-looking edges are an illustrative metaphor. Do not apply this treatment to a real record in a way that implies it was physically torn, censored, or deliberately destroyed without evidence.

## Type and color

Keep Space Grotesk for the brief present-day headline, Space Mono for identification, and Newsreader italic for source words. Preserve the exact approved palette. Use paper on carbon, ink on paper, and tape on carbon for essential text. Red identifies a specific location or difference as line-work, not an institutional verdict.

All source-like content in these studies is labelled **“SIMULASI · BUKAN ARSIP”** at the top of every frame. Marks and signatures are invented illustrations, with no institutional seal or historical attribution. No historical claims are being verified by these design samples.

## Two dramatic reversed-color scenes

User request: exactly two of the sixteen primary scenes swap the background and text colors at dramatic narrative beats. Use fourteen normal carbon-background scenes and two manila-background scenes. Select the two positions from the actual script; do not add extra scenes or treat the swap as a flashing effect. A reversal is a scene-level color mode, not a slide transition.

For the reversed mode, use manila `#EAE0D0` as the background and carbon `#121110` for headlines, series chrome, source locators, and captions. Ink `#1A1816` is also available for text. Carbon/manila contrast is approximately 14.43:1 in either direction; ink/manila is approximately 13.55:1.

Red `#C32822` on manila is approximately 4.41:1: reserve it for large display emphasis or meaningful graphic marks, not small source or caption text. Yellow `#D4A359` on manila is approximately 1.75:1 and steel `#7C756B` on manila is approximately 3.48:1; exclude both from essential small text. Keep yellow emphasis on a carbon field when needed. These limits follow the [WCAG text-contrast thresholds](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html): 4.5:1 for normal text and 3:1 for large text. Assess size at the intended display scale, not just native 1080px.

Remap editorial graphics deliberately for the light field. Preserve the actual colors and legibility of historical scans/photos; do not apply a blanket CSS color-inversion filter. A direct cut on the dramatic beat is a suitable mode change. Avoid simultaneous foreground/background color interpolation through a low-contrast mid-tone. Keep the dramatic result stable long enough to read and review both modes at phone scale.

See [reversed-studies.html](reversed-studies.html), [reversed-studies.png](reversed-studies.png), and [reversed-contrast-QA.json](reversed-contrast-QA.json) for static proof and computed ratios. These demonstrate color handling, not final scene placement or rendered motion.

## Space, sources, and delivery

Essential content stays at x=84–930 and y=160–1540. A single-line source locator can occupy y=1490–1540 in an episode; keep the illustration clear of that line. The static simulated studies have no real source to cite and therefore use only the persistent simulation label. Full references belong in the production package and public source list, not in a frame paragraph.

Check the actual platform preview before producing, since interface overlays vary. Review both native 1080 × 1920 and 360 × 640 exports. Font assets and SIL OFL licenses are reused from `../../assets/`; no network fonts are required.

## Motion and sound remain conceptual

The user requested richer motion. Use the [richer motion proposal](MOTION.md): layer the archival workspace spatially, develop each scene with meaningful object actions, and carry selected shapes or objects into the following scene. Align comparable marks, move from a source to its enlarged detail, and make evidence relationships visible. Use approximately two meaningful internal actions plus a stable reading/result pose in each primary scene; the overall count remains sixteen.

Vary physical direction, speed, depth, and intensity. Avoid entrances for every individual line of text or an identical slow zoom on all scenes. Let the visual settle while narration explains it. No animation or audio was generated for this revision; the detailed choreography, timings, and mix remain proposals for future implementation.

After the `penutup-proklamasi` dry run, the user rejected monotonous slide transitions. Full-scene slide/push transitions are excluded from this refinement. Internal object movement remains available. Choose direct cuts, anchored match cuts, continuous source-to-detail camera moves, local object masks, or selective dissolves according to the actual relationship between adjacent scenes. The updated [motion guidance](MOTION.md#replacement-transition-vocabulary) supersedes the earlier directional-handoff quota. Existing static study exports do not demonstrate these proposed transitions.
