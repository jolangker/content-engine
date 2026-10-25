# Verification — board v1

Date: 2026-10-25. Outcome: static board ready for visual/editorial review; no human approval is claimed for the new package.

## Delivered artifacts

- `style-board.html`: editable local HTML/CSS with bundled fonts and original rendered imagery.
- `style-board.png`: 1740 × 2947 board image.
- `style-board.pdf`: one page, approximately 1305.12 × 2212.08 points.
- `study-01.png`, `study-02.png`, `study-03.png`: 1080 × 1920 each.
- `phone-study-01.png` through `phone-study-03.png`: 360 × 640 each.
- `character-direction.png`: 1616 × 405 acting/identity strip.
- Original `.blend` geometry, 3D PNG renders, source scripts, font files/licenses, reference manifest/contact sheets, and board guidance.

## Automated layout/export checks

See [export-report.json](export-report.json). All three Barlow weights and IBM Plex Mono loaded locally. No missing image, horizontal page overflow, detected text overflow, failed request, or browser runtime error was reported. The three native frames retain 1080 × 1920 geometry. Caption positions fit the proposed safe area. Ink `#173B42` on cream `#FFF5DE` has an approximately 11.13:1 contrast ratio.

The initial PDF paginated the footer onto a second page. The conflicting fixed CSS page size was removed, and the final PDF was regenerated at the measured board height with a small rounding allowance. [pdf-report.json](pdf-report.json) confirms one page and expected headings/closing review label. System Poppler was unavailable; the installed PyMuPDF renderer produced [pdf-review.png](pdf-review.png) for visual inspection.

## Visual inspection

Inspected the full board, original rendered scenes, all three 360 × 640 frame exports, character strip, and final PDF page rendering. The final images show legible captions, recognizable recurring character, readable earth sections, schematic warm/cool path markers, and a clear oversized visitor/suitcase joke. The poses fit the character strip without clipping. Essential action and speech remain separate. No new clip, font, or overlap defect was observed in the final revision.

During iteration, character transforms initially lost sphere scales; updating the Blender dependency graph before the rotation corrected this. Soil noise now uses world-position coordinates. The character-strip camera was widened and aligned, and the house section's intake, flow markers, and connection into the room were made visible. These affected assets and all board exports were regenerated and inspected afterward.

## Scope and limits

This is a static reusable identity board, not an episode storyboard or a completed film. The three studies are independent fictional compositions. No claim is made that mechanical motion, camera continuity, comedy timing, narration delivery, sound design, thermal performance, railway behavior, or a complete installed system has been validated. Palette values in 3D are material inputs; lit render pixels vary with illumination and view transform.

No speech synthesis, paid generation, audio, music, hosted media, publishing action, HyperFrames initialization, or production entry was created. Only the new board row is changed in the root tracker. Existing board and production documents are preserved.

## Preview lifecycle

File-based previews only. The Puppeteer exporter closes its browser in `finally`. Blender helper processes exited after their still renders; no matching `build-scenes.py` process remained at the end. No temporary HTTP server or HyperFrames preview was started or retained.

## Review state

Concept, comedy approach, and nominal duration were selected in the conversation. Newly proposed visual tokens, character appearance, detailed editorial rules, and the delivered v1 images await review. Acceptance of this exact package can close those layers together without a redundant final gate. A later production retains its own script, storyboard, and final-preview reviews.
