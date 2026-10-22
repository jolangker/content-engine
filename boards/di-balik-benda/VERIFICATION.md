# Static board verification — v1

Date: 2026-10-23. Status: agent-verified; board v1 subsequently approved by the user.

## Artifacts

- `style-board.html`: editable local-file review board.
- `style-board.png`: full board export, 1700 × 2417 pixels.
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
