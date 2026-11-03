# Static board verification — title/subtitle v3

Date: 2026-11-03. Agent verification of visual/editorial v3, subsequently accepted by the user's “cocok” response. The user requires titles and subtitles, while illustration and motion remain central. The displayed karaoke treatment is accepted; no identified external-reference match is claimed.

## Preservation and output

- `revisions/v1-draft/`: all 27 archived files match their saved hashes.
- `revisions/v2-draft/`: all 33 archived files match their saved hashes.
- Audio and publishing-account configuration exactly match v2.
- Current sheet: `style-board.html` / `style-board.png`, 1800 × 2665.
- Three hero PNGs: 1080 × 1920 each, with two-line titles and one short subtitle phrase.
- `subtitle-style.png`: 1656 × 191; four static states of one phrase with a different active word.
- `phone-review.png`: 1234 × 790, displaying each hero at 384px width.
- Four isolated illustration motion poses remain available in SVG and the motion-pose strip. They are planning drawings, not frames captured from an animation.

## Visual review

Inspected the phone comparison and subtitle-state strip after export. The title remains distinct from the illustration and the subtitle has its own lower band. Titles are dark on pale stages and white on the cobalt stage. Inactive subtitle words are white on ink; the active word is ink on an amber rounded highlight. Word spacing was increased after the initial review so the highlight does not visually crowd adjacent words.

The original v2 art is reframed with a uniform scale of 0.86 and translation (70,80), preserving proportions while leaving room for title and subtitle. Critical source/destination relationships remain visible. The caption panel was moved down 12px after the first clearance check; the final minimum art-to-subtitle clearance is 68.08px, above the 60px requirement.

Current static caption examples are illustrative English sample writing, constrained by the existing source scopes. They are not approved narration or word alignment. The exact technical meaning still depends on episode narration and claim-level evidence.

## Final exporter checks

`python build-board.py` uses local FontTools metrics for stable word placement. `node export-board.cjs` uses the established local-file browser workflow. No dependency was installed and no preview server was started.

- No checked HTML overflow, horizontal overflow, SVG text outside its frame, failed browser request or page error.
- Each hero contains exactly two title lines and 4, 4 or 5 subtitle words respectively.
- Exactly one active word per displayed subtitle; the word fits its highlight and each panel fits the caption region.
- Art/subtitle clearances: 108.40px, 119.58px and 68.08px.
- Required Bricolage Grotesque 700 and Instrument Sans 700 faces load in standalone hero SVGs. Instrument Sans 400 is unused there and may remain unloaded. All sheet fonts load.
- All current SVG sources parse successfully. PNG signatures/dimensions are verified from their headers.
- Both archived drafts remain intact; AUDIO.json and ACCOUNTS.json are unchanged.
- The export browser closes in `finally` and the final command exits successfully. No server, production project or review-hold process is created.

## Remaining limits

No narration, measured word onset, highlight animation, SFX, final mix or actual motion continuity is generated or playback-verified. A future production must align the subtitle to its approved voiceover, inspect the full motion sweep against caption clearance, and check actual destination-platform overlays. The accepted static treatment does not assert those runtime checks have passed.

Visual/editorial v3 has status `approved`, recorded from the user's “cocok” response on 2026-11-03 after the final preview was shown. The source/export status labels were updated to accepted wording without changing the artwork or typography; the exporter was rerun to keep them consistent. No new production was created.
