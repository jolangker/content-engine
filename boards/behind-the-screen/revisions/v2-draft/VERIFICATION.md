# Static board verification — illustrated v2

Date: 2026-11-03. Agent review of an unapproved visual/editorial revision. Motion is represented by planned poses, not actual animation frames.

## Scope and preservation

The user requested more illustration, little text and a focus on motion design. The first unapproved draft is preserved in `revisions/v1-draft/`, with SHA-256 hashes in its ARCHIVE.json. No approved board or existing production is revised. Audio and publishing-account configuration remain unchanged.

Current output:

- `style-board.html` / `style-board.png`: current v2 sheet, rebuilt by `python build-board.py` and exported by `node export-board.cjs`.
- Three original editable hero SVGs and 1080 × 1920 PNGs in `studies/`.
- Four original planned-pose SVGs and `motion-poses.png`.
- `phone-review.png`: the hero studies displayed at 384px width.
- `illustration-review.png`: the three illustrations and external explanatory captions.
- `export-report.json`: final geometry, font, zero-word and browser-error checks.

## Visual craft review

**Specificity:** the local face remains in the device while a separate proof travels; the local wipe stays within the browser; repeated media establishes retained source and moving copy. The receivers, tokens, tubes and cabinets are illustrative metaphors, not product captures or literal technical architecture.

**Range:** a diagonal hand/device gesture, a cobalt local/remote scene, and a foreground/background media route share contour, depth and palette while changing composition. The previous headline/diagram template has been replaced rather than merely stripped of labels.

**Text reduction:** all three hero SVGs contain zero SVG text elements and zero visible words. No headline-hiding test is necessary because the hero artwork is already text-free. Exact technical meanings and limits would need the episode narration; the image is not claimed to teach every distinction without words or motion.

**Motion planning:** the four poses preserve the same local face and show hand preparation, contact, proof travel and a post-arrival receiver state. They are separate static compositions. Intermediate motion, sound and timing remain untested.

**Craft:** inspected the direction sheet, all three native-size hero PNGs and the 384px comparison, including the four-pose strip on the sheet. Checked silhouettes, finger/device contact, token/source separation, local wipe bounds, receiver visibility, repeated-media identity, overlaps and phone-scale reading. The illustration includes intentional overlaps and hard offset depth; these are not accidental overflow. Refined the media thumbnails to preserve the original artwork's aspect ratio while cropping to each illustrated screen; re-exported and reinspected the affected comparison.

## Technical checks and limits

The exporter checks board overflow, study dimensions, zero visible words, required board fonts and browser failures. Standalone hero SVGs have no visible text, so their declared font faces may remain unloaded; this is expected and not a missing-font defect. The HTML sheet uses and loads Bricolage Grotesque 700 and Instrument Sans 400/700.

Current silent studies use space down to approximately y=1670. A narrated episode must restage the lower art above its caption band rather than adding captions over these unchanged illustrations. Exact platform overlays, audio and the final caption layout are not verified by this static package.

Local files and a short-lived headless export browser only. No temporary server, playback preview or production project is created. No animation continuity, actual duration, synthesized narration or SFX mix is claimed.

## Final export/state audit

- Direction sheet: 1800 × 2441; three hero PNGs: 1080 × 1920 each.
- Phone comparison: 1234 × 790; illustration review: 1656 × 1052; motion-pose strip: 1656 × 561.
- All seven SVG sources parse and contain zero SVG text elements.
- No checked HTML overflow, horizontal overflow, out-of-frame text or browser errors.
- Required HTML sheet fonts loaded. No visible text requires a font in the standalone illustrations.
- All 27 archived v1 files match their saved SHA-256 hashes; current font/license assets match their manifest.
- AUDIO.json and ACCOUNTS.json match the prior draft exactly.
- Stale v1 diagram-review image removed from the active folder; the archived original remains intact.
- Headless export exits successfully and closes its browser in `finally`. No server was created.

Visual and editorial v2 are ready for feedback. Registry status: `awaiting_review`; no user acceptance is inferred from the revision instruction.
