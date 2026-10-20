---
version: "2-draft"
name: Berkas Polemik
description: Evidence-led forensic-dossier identity; refinement of approved v1.
unit: "1080 × 1920 vertical frame"
principle: "Traceable evidence; readable detail; conclusions proportionate to the record."
colors:
  bg: "#121110"
  paper: "#EAE0D0"
  ink: "#1A1816"
  red: "#C32822"
  steel: "#7C756B"
  tape: "#D4A359"
  surface: "#1D1B19"
typography:
  display:
    fontFamily: Space Grotesk
    weight: 700
    fontSize: "108px"
    lineHeight: 1.04
    letterSpacing: "-0.035em"
  reading:
    fontFamily: Space Grotesk
    weight: 500
    fontSize: "52px"
    lineHeight: 1.25
  quote:
    fontFamily: Newsreader
    weight: 400
    fontStyle: italic
    fontSize: "72px"
    lineHeight: 1.15
  metadata:
    fontFamily: Space Mono
    weight: 400
    fontSize: "32px"
    lineHeight: 1.4
  label:
    fontFamily: Space Mono
    weight: 700
    fontSize: "34px"
    lineHeight: 1.35
spacing:
  essential-left: "84px"
  essential-right: "150px"
  essential-top: "160px"
  essential-bottom: "380px"
  source-band-top: "1370px"
  source-band-bottom: "1530px"
  caption-reserve-top: "1600px"
  caption-reserve-bottom: "1780px"
  block-gap: "48px"
components:
  evidence-sheet:
    backgroundColor: "{colors.paper}"
    color: "{colors.ink}"
    borderRadius: "0px"
    padding: "48px"
    description: "An editorial presentation surface with explicit source-type labelling."
  status-label:
    font: "{typography.label}"
    description: "State a bounded observation or evidence limit, not a decorative verdict."
  source-band:
    font: "{typography.metadata}"
    color: "{colors.paper}"
    description: "Concise source locator and material type, separate from optional captions."
---

# Proposed frame rules

## Continuity and hierarchy

Keep the approved palette and three families. Space Grotesk carries the present-day explanation, Space Mono identifies evidence, and Newsreader distinguishes a source's voice. Only use Newsreader as a quotation voice when the text is verified, or conspicuously marked as simulated in a design study.

At 1080 × 1920, use a 108px display, 52px reading text, 72px quotations, and 32–34px metadata. The board previews are scaled to 40%; the standalone studies preserve native resolution. Keep one main thought and at most two short evidence fragments in a frame. Essential meaning must not depend on a miniature facsimile.

## Color use

Paper on carbon and ink on paper carry reading text. Tape on carbon identifies attention or uncertainty. Red rules on paper mark a specific discrepancy; paper on red is reserved for large display text. Keep red and steel off small essential text. Steel can define structural rules and nonessential marks. Do not convey status through color alone.

These refinements retain the existing colors while changing their application. Exact text-pair contrast is checked in the export report.

## Composition and provenance

Essential content uses x=84–930 and y=160–1540. This conservative starting envelope is a production guide; check the actual destination preview, since interface overlays vary. The source band stays above y=1530, separate from optional spoken captions at y=1600–1780. Leave lower interface space clear. The static studies omit captions because they have no narration.

Use one dominant piece of evidence with editorial commentary visibly outside it. A copy comparison may use two vertically stacked paper sections, not two unreadably narrow columns. Vary the communicative need across frames: comparison, close reading, finding/limit. Avoid filling space with tiny archival metadata.

Label study material on every frame: **“SIMULASI · BUKAN ARSIP”**. No invented institutional seals, archival call numbers, historical quantities, or attributed historical quotations appear in the draft board. In production replace all study copy with researched material and real locators, retaining source-type labels.

## Motion intent — conceptual only

Move to help the viewer read: establish the source, isolate a detail, compare related passages, then hold the finding. Proposed detail move: 0.35–0.55s; proposed comparison arrival: 0.4–0.6s, no elastic bounce. Reading holds must be determined from the final copy and narration. Do not use dramatic reveals to imply concealed information without evidence. These are directions, not a rendered or validated animation.

## Sound intent — conceptual only

Keep narration clear and measured. A restrained low bed or occasional paper sound may support the physical-dossier identity, with silence available for difficult material. Avoid constant typing, alarm cues, or suspense that tells viewers an allegation is already proven. Music level and timing require a future production mix; no audio is part of this static draft.

## Local assets

Use the approved font files and SIL OFL licenses in `../../assets/`. Supported cuts used here: Space Grotesk 500/700, Space Mono 400/700, Newsreader italic 400. No new typefaces or network dependencies are introduced.
