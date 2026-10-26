# Static board verification — v4

Date: 2026-10-25. Status: agent-verified; v4 applies the user's 2.5D-only, increased interaction/animation, and interaction SFX direction at board scope. The visual palette and typography remain approved. Earlier checks below are historical records, distinguished from this revision's verification.

## Artifacts

- `style-board.html`: editable local-file review board.
- `style-board.png`: updated full board export, 1700 × 3939 pixels.
- `production-defaults.png`: review crop of the new 90-second pacing and breakdown guidance.
- `shot-direction.png`: review crop of v3 topic-complexity and complementary-shot guidance.
- `interaction-direction.png`: v4 review crop of the 2.5D lock, attention/action/response poses, and synchronized SFX planning.
- `SHOT-DIRECTION.md`: production guidance for causal continuity, coordinated motion, varied observation time, and repetition review.
- `study-01.png`, `study-02.png`, `study-03.png`: independent vertical design studies, 508 × 903 pixels each (9:16 rounded to whole pixels).
- `assets/*.svg`: four original schematic illustrations, preserved as editable vector assets.
- `frame.md` and `EDITORIAL.md`: matching approved visual and editorial guidance.
- `assets/SOURCES.md`: font provenance and SHA-256 hashes; original font licenses stored alongside fonts.

## Original inspection

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

## Version 4 revision and inspection

Preserved the previous v3 board package under `revisions/v3/` before editing. The archive contains its documents, editable source, image exports, assets, and a SHA-256 manifest. Recorded existing files for the three current Di Balik Benda productions to verify this board revision leaves them unchanged.

Updated DIRECTION.md, frame.md, EDITORIAL.md, and SHOT-DIRECTION.md consistently. The normative frontmatter now locks the visual medium to 2.5D and specifies interaction, attention, and SFX coverage. Removed the current guidance allowing mixed 2D/3D and sparse sound. Preserved the 90-second default, adaptable 14–18-shot range, and complex-mechanism preference. Added cue-sheet decisions, full-speed motion/audio review, phone-speaker intelligibility, material-aware cues, and explicit distinction between physical and editorial sound. Timing tolerances and the roughly 5-second static-shot review trigger are implementation choices.

Rebuilt the static source and exported the board with the existing local-file exporter. Added a dedicated interaction-direction crop and four illustrative action/sound planning poses. Opened and visually inspected the updated full board and interaction crop. Checked readable hierarchy, unclipped text, consistent palette, and the new 2.5D lock in the visual-system panel. The browser report confirms both bundled fonts loaded, no overflowing HTML text, no horizontal page overflow, and no browser or failed-resource errors. Original independent study images remain unchanged; this revision adds guidance rather than depicting a new verified mechanism.

Checked archive hashes, unchanged production files, tracker JSON and registered paths, source/export consistency, and absence of obsolete mixed-medium/sparse-SFX instructions in current normative guidance. The registry retains its approved board status because this applies explicit user instructions to the existing board; no new human playback approval is recorded.

The preview is static. No animation playback, actual SFX generation, mix listening, or sound synchronization can be verified here. Those are explicit requirements for subsequent productions. No server, listening port, audio request, or episode was created.

## Version 5 refinement and inspection — 2026-10-27

The user explicitly selected all six refinements presented in the preceding board review. Implemented them in the current board as v5, retaining its approved registry entry. Approval refers to the selected direction; the rendered static package is agent-inspected, and no human approval of unseen motion or sound is recorded.

Preserved the complete prior v4 package under `revisions/v4/` before editing: 26 board files, including documents, source, exports, assets and licenses. `SHA256.json` verifies their original bytes. `PRODUCTION-BASELINE.json` records 1,173 tracked production-file hashes and the production registry; all still match after this revision. The board accounts are byte-identical to v4. The tracker still parses, has only `boards` and `productions`, and all registered paths exist. Its Di Balik Benda row remains `approved`; no registry rewrite or production transition was needed.

| Selected refinement | Implementation verified |
| --- | --- |
| One central mystery | EDITORIAL.md's story contract requires the concrete question, opening behavior, scoped answer and supporting evidence. SHOT-DIRECTION.md carries it into the opening shot and review. |
| Components when needed | First-use function/name entries replace the opening component-inventory allocation. The editable first-discovery target is approximately 8–12 seconds, with justified orientation exceptions. |
| Linked discoveries | Each story beat records its question, visual answer, and next causal dependency; the shot map and script review check the connection. |
| One signature interaction | The story contract identifies one physical event; shot planning covers phone-scale framing, contact/transfer, observation, competing cues and marked altered timing. |
| Ending demonstrates the opening answer | The story contract and shot map pair the opening and final demonstration with stable context and the causal detail made visible. |
| Audience appeal in selection | Recognition/proximity, question curiosity, and visual proof are assessed with the existing five mechanism criteria; selection requires written reasons rather than predicted retention scores. |

Updated frame.md's normative version and story contract. Parsed its YAML and compared it to the archive: palette, typography, spacing, components, 2.5D medium and audio requirements are unchanged. The duration remains 90 seconds, and the revised six-interval example totals 90 seconds and 16 shots inside the adaptable 14–18-shot guide. Local links and template substitutions were checked. Existing production checkpoints own the new board-specific checks; this revision adds no separate human approval gate.

Rebuilt `style-board.html` from `build-board.py`. Added three original SVG studies demonstrating a conceptual opening exterior, a contact detail, and the matched revealed answer. These are independent narrative studies, not an episode or engineering reference. Added all six refinements and audience-appeal prompts to the visible board and replaced the pacing strip. The three original 9:16 identity-study compositions are preserved and re-exported; PNG bytes can differ from v4 due to their new subpixel page position.

Exported through the existing local-file exporter, including the new `discovery-direction.png` crop. Inspected the full board, revised pacing, and discovery crop. Corrected the conceptual housing so the revealed gear fits its enclosure, re-exported, and inspected the corrected crop. The opening and final views preserve the input/output axes and framing; the macro isolates their relationship. The final export is 1700 × 5227 pixels (the DOM board height is 5226.4375 pixels). Both local fonts load, with no horizontal page overflow, detected text overflow, browser errors, or failed resource requests. `export-report.json` records browser checks; `verification-v5.json` records preservation and consistency checks. `git diff --check` passes.

No new packages, fonts, image-generation requests, audio, episodes, or publishing operations were needed. The exporter closes its browser in `finally`; it uses file URLs and creates no preview server or listener. Static verification establishes the board package's consistency and layout. Actual motion readability, sound, and retention improvements still require episode playback and available audience analytics.

## User acceptance of v5 — 2026-10-27

After delivery of the implemented package and its preview links, the user replied "approved". Recorded acceptance of both the v5 editorial framework and static visual package in DIRECTION.md and EDITORIAL.md. frame.md and the tracker already carry `approved` and required no status change. This is an approval-record update only; the accepted source and images remain the inspected v5 exports. Future episode motion, audio, render and publishing checkpoints retain their existing scope.
