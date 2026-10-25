# Verification - Bongkar Sistem v2

Date: 2026-10-25. Outcome: revised static visual/editorial package ready for review. No human approval, moving-camera verification, or audible-mix verification is claimed.

## Delivered package

- style-board.html and style-board.png: editable source and 1740 x 2903 review image.
- style-board.pdf: one inspected page; approximately 1305.12 x 2178.96 points.
- Three study PNGs at 1080 x 1920, plus 360 x 640 phone checks.
- interaction-direction.png: before/action/result strip with planned sound roles.
- Six original v2 Blender stills and editable scenes under assets/renders-v2/.
- Updated DIRECTION, EDITORIAL, frame spec, MOTION-AND-AUDIO, FEEDBACK-v2, PRODUCTION-STANDARDS, and SFX-PLAN documents.

## Static checks

export-report.json records all four local font faces loaded, zero missing images, zero browser/runtime/request errors, no horizontal overflow, and no detected text overflow. All three captions compute to 58 px in their native 1080 x 1920 frames; their backing and position fit the working safe area. A CSS specificity mismatch that initially shrank captions on the board was repaired before final export.

pdf-report.json confirms one page and expected headings, step range, and review label. System Poppler is unavailable; installed PyMuPDF rendered pdf-review.png. The complete final PDF page was visually inspected. Early shell encoding substitutions in arrows/ranges were corrected in source and all affected exports regenerated. Final output uses readable arrows and hyphen ranges.

## Visual inspection and changes

Inspected full-environment, detail, overhead, and action-pose renders; the full board; all three phone frames; the interaction strip; and the final PDF render. The new setting extends beyond the frame and includes continuous ground, architecture, adjacent houses, vegetation, utilities, material texture, adult proportions, and distinct perspective views. No isolated slab or blank color moat remains. Camera angle/scale differs substantially between the independent studies. The close view makes handle and flow changes readable; the three static action poses show absent flow, initial drops, and a sustained result.

V2 is a procedural semi-realistic technical/architectural study, not photography or a claim that all assets meet a photoreal target. Fine foliage/human modeling and a polished final episode still require production-specific work. An initial physical-sky trial produced poor exposure/horizon and was replaced with controlled world fill/sun/area lighting. Final stills were re-rendered after that correction. No image-generation or third-party stock assets were used.

## Temporal and audio limits

The user requested stronger interactions, a fuller setting, faster progression over 60 seconds, less cartoonish design, more discrete SFX, and in-shot camera motion. V2 records all six as concrete production standards rather than certifying them from static images. The action strip is a pose proposal; it has no hand performance, elapsed-time evidence, or validated valve mapping. The angle samples do not prove a smooth camera move. SFX matrix entries are cue plans, not generated/placed/audible audio.

For a future v2 film, use PRODUCTION-STANDARDS.md to verify the meaningful-step map, measured duration, before/contact/result noticeability, moving-camera proof, and event-to-cue coverage/export listening. Static frames, runtime validation, ASR, and loudness measurements cannot substitute for those criteria.

## Test evidence and preservation

The test production's EPISODE, scene-plan, final storyboard, REVIEW, and sound_design files were read. Its recorded export is 84.7 seconds, six long scenes, one rain ambience cue, with placement/trickle accents explicitly omitted. Its final storyboard and three sampled 2.4-second intervals were inspected; no full playback or perceptual listening claim is made. The user's subjective audio feedback is recorded as such.

The complete prior board is preserved at revisions/v1-before-production-feedback/ with its ARCHIVE.json hashes. V1 was not approved as a complete board. The existing production's source, narration, audio, export, and tracker row were not revised. No production, synthesis, hosting, publishing, or shared-skill changes were created.

## Lifecycle and review status

File-based HTML/image/PDF previews only. No HTTP or HyperFrames preview server was started. Blender helpers completed; the one owned render interrupted for scene reuse was identified by executable and exact board-script command line. Puppeteer closes its browser in finally. No unrelated Blender/MCP process was stopped. Rendering backup files created for this revision are cleaned only inside the verified renders-v2 directory.

The v2 package is awaiting visual/editorial feedback. The user-directed revision is authorization to make changes, not approval of unseen results. An acceptance can cover the delivered package together; it does not establish an episode's animation or mix quality.
