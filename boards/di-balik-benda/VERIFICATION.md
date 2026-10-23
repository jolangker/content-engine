# Static board verification — v3

Date: 2026-10-23. Status: agent-verified; v3 implements the user's further complexity and animation-variety direction at board scope. Original visual identity remains approved.

## Artifacts

- `style-board.html`: editable local-file review board.
- `style-board.png`: updated full board export, 1700 × 3287 pixels.
- `production-defaults.png`: review crop of the new 90-second pacing and breakdown guidance.
- `shot-direction.png`: review crop of v3 topic-complexity and complementary-shot guidance.
- `SHOT-DIRECTION.md`: production guidance for causal continuity, coordinated motion, varied observation time, and repetition review.
- `study-01.png`, `study-02.png`, `study-03.png`: independent vertical design studies, 508 × 903 pixels each (9:16 rounded to whole pixels).
- `assets/*.svg`: four original schematic illustrations, preserved as editable vector assets.
- `frame.md` and `EDITORIAL.md`: matching approved visual and editorial guidance.
- `assets/SOURCES.md`: font provenance and SHA-256 hashes; original font licenses stored alongside fonts.

## Inspection

Opened the exported full board and all three sample frames for visual inspection. Corrected a stray input annotation, overlapping hero footnotes, an unanchored leader, the gear-output rotation arrow, and placement of a macro-study label. Inspected the revised exports.

The browser export report confirms both local font families loaded, no horizontal page overflow, no overflowing HTML text, and no browser or failed-resource errors. Automated overflow checks complement the visual inspection; they do not verify mechanical geometry or animation.

Static diagrams are explicitly illustrative, not verified engineering diagrams. Temporal legibility, physical motion, camera continuity, narration, and audio remain untested because no animated demonstration is part of this board request.

## Reproduction and lifecycle

Run `python boards/di-balik-benda/build-board.py` and `node boards/di-balik-benda/export-board.cjs` from the workspace root. The builder reuses preserved font files and fetches only missing fonts or licenses. The exporter uses Puppeteer available in this environment and the installed Chrome executable; it accepts a `CHROME_EXECUTABLE` override.

Current Puppeteer screenshot API documentation was fetched through Context7 before using the exporter. No additional package was installed, no production files were changed, and no server or listening port was created. The exporter closes its browser in `finally`.

The user subsequently accepted the presented board package with "cocok" on 2026-10-23. Approval labels were updated in the source and re-exported without changing the visual direction. Agent verification and the user's acceptance are recorded separately.

## Version 2 revision

The user requested 90 seconds and more detailed breakdown frames, then clarified that this applies to the board. Updated EDITORIAL.md, frame.md, and DIRECTION.md consistently, replaced the old 25–50-second default, and added a visible 90-second planning strip to the board. The 14–18 explanatory-shot range and approximately 16-shot example are implementation recommendations, adjustable to the mechanism, not a fabricated user-specified quota. Complex actions receive 2–4 diagnostic poses when needed. Shot density is explicitly separate from frame rate.

The example intervals total 90 seconds. The exporter reports loaded local fonts, no HTML text overflow, no horizontal page overflow, and no browser or failed-resource errors. Inspected the updated full export and the production-defaults crop. The three original independent style studies retain their composition and role; they are not relabeled as a full episode storyboard.

Preserved the previous approved package in `revisions/v1/`, including editable source, image exports, fonts, licenses, and a SHA-256 manifest. Existing pulpen, resleting, and jepitan-baju productions continue to reference their recorded v1 direction; their files were not changed. No new narration, animation, render, or server was created. This verifies the board update, not the quality of a future 90-second film.

## Version 3 revision

The user's further feedback concerns monotonous animation and insufficient mechanism complexity. Preserved the entire v2 package under `revisions/v2/` before applying changes. The archive includes a SHA-256 manifest and hashes of the four existing Di Balik Benda production receipts.

Updated topic selection to prioritize interacting subassemblies and multiple linked causal interactions. The approximately 3–5-interaction guide is an implementation preference, not a literal user-specified quota or a raw part-count minimum. Added SHOT-DIRECTION.md, linked it from the editorial and visual specs, and clarified that physically coupled parts must move together when required. Added purposeful visual-treatment choices, operating-state continuity, variable observation time, and a review trigger for repeated shot runs. Kept the 90-second default and adaptable 14–18-shot range.

Rebuilt the HTML and PNG with the v3 guidance section, updated the functional-motion glyph, and exported separate shot-direction and pacing crops. Inspected the updated full board and shot-direction crop. The export report confirms local fonts loaded, no overflowing HTML text or horizontal page overflow, and no browser or failed-resource errors. The three independent style-study PNGs remain byte-identical to their archived v2 versions.

Inspected only the latest episode's written scope and review records for context; no full motion playback was performed in this board edit. Existing episode receipts remain unchanged, and no technical claim about the candidate mechanisms was added as verified evidence. Candidate names are explicitly research seeds. No episode, audio, animation demonstration, new package, or preview server was created. These checks establish the board update and its consistency, not the quality of an unseen future animation.
