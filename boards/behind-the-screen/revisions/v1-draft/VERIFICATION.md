# Static board verification — v1

Date: 2026-11-03. This is agent verification of a proposed static package, not human creative approval or video playback review.

## Delivered artifacts

- `style-board.html`: editable local-file direction sheet, rebuilt by `python build-board.py`.
- `style-board.png`: 1800 × 2505, exported by `node export-board.cjs`.
- `studies/passkeys.svg`, `privacy.svg`, `delivery.svg`: original editable vector sources with bundled local fonts.
- Corresponding study PNGs: each 1080 × 1920.
- `phone-review.png`: 1234 × 790 comparison, with each study displayed at 384 × 682.67.
- `diagram-review.png`: 1656 × 1063 comparison with display headlines hidden, preserving diagram labels and captions.
- `export-report.json`: final geometry, font, browser-error and overflow results.
- `assets/asset-manifest.json`: SHA-256 hashes for the five copied font/license assets.

## Visual craft review

**Specificity:** recognizable sign-in and browsing surfaces, explicit device/website boundaries, and repeated media at origin/edge/viewer make the diagrams about everyday digital behavior. The shared shallow opaque surfaces and directed exchanges support the selected concept. No borrowed brand, stock artwork or generated bitmap imagery is embedded.

**Communication:** the headline-hidden export still distinguishes local approval from remote proof, a local history record from an external visit, and an available cached copy from the origin. It retains explanatory labels; this is not a claim that a technical diagram communicates every detail without any words. The full-board and native-size inspections were followed by the phone-width comparison.

**Range:** the first study traces a local/remote exchange, the second exposes a privacy boundary, and the third uses spatial routing and repeated media. They are independent compositions, not consecutive episode scenes or a forced three-card video format.

**Corrections made and rechecked:**

1. Added a distinct local-check compartment to the passkey device so the remote proof cannot be mistaken for transmitted biometric data.
2. Anchored the signed-proof leader to the response path rather than leaving its end visually detached.
3. Interrupted the dashed origin/cache path around the “Nearby copy” label, removing a line/text crossing.
4. Corrected the export helper's HTML reset after standalone SVG capture. The final export exits successfully and closes its own browser in `finally`.

**Craft and fidelity:** headers, annotations and two-line captions are contained at board and study sizes. All requested local 400/700 fonts loaded. The tested text colors have contrast ratios of 13.65:1 for ink on ground, 5.04:1 for cobalt on ground, and 5.04:1 for white on teal. The crossed-out history entry is intentionally muted to indicate a removed record; required explanatory text uses the declared high-contrast colors. The six visual colors and supported font weights agree with frame.md and the source.

## Technical checks

Final export report:

- No HTML horizontal overflow or overflowing checked text containers.
- No SVG text outside a study's frame.
- All fonts loaded in the direction sheet and standalone SVG exports.
- Each standalone study's document bounds are exactly 1080 × 1920.
- No captured browser page errors or failed requests.
- PNG signatures and file dimensions checked directly from PNG headers.
- All recorded font/license hashes match the copied files.
- AUDIO.json, ACCOUNTS.json and export-report.json parse successfully.

Only file: URLs and a short-lived headless browser were used. No preview server, listening port or review-hold process was created. The export command completed and its browser was closed. Existing boards and productions are outside this change.

## Limits and review pending

Source bodies and their claim boundaries are recorded in assets/SOURCES.md. The passkey illustration covers local biometric verification, the privacy illustration is scoped to Chrome Incognito history after session closure, and the delivery illustration assumes a cache hit. These are explanatory abstractions, not complete protocol diagrams or product captures.

Motion poses, proposed durations/easing, narration voice and audio remain conceptual. No speech-aligned captions, actual synthesized voice, animation continuity, final mix, platform UI overlay or audience performance has been verified. Production-level research and playback checks remain necessary for a future episode request.

Both editorial v1 and visual v1 are ready for user review. The concept was selected; the unseen package was not pre-approved. Registry status: `awaiting_review`.
