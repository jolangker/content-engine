# Behind the Screen — illustrated motion direction v2

Status: `awaiting_review`. Visual v2 and editorial v2 are proposals, not an approved package.

## User direction

On 2026-11-03 the user selected the Behind the Screen concept, then gave this feedback on the first static draft: “gua mau visual yang lebih ilustratif dan sedikit teks. gua mau main di motion design”. This revision makes illustration, object behavior and motion planning central. It replaces the first draft's large per-frame headlines and labeled diagrams.

The user's direction authorizes this board revision. The specific style, text budget, staging and timing below implement that direction; they are not quotations from the user or approval of unseen animation. The previous unapproved package is preserved under [revisions/v1-draft/](revisions/v1-draft/), with its files and hashes in ARCHIVE.json.

## Concept and audience

**Promise:** Understand what happens behind your everyday clicks.

English-language vertical explainers for non-specialists. The proposed initial markets remain the US, UK, Canada and Australia. They are positioning choices, not measured audience demographics. The four pillars remain identity/access, copies/memory, connections/delivery, and visibility/control.

The explanation begins with a familiar action, makes a hidden relationship tangible, and returns to its visible consequence. Narration explains the technical meaning while the illustration demonstrates action, transfer, separation or persistence. See [EDITORIAL.md](EDITORIAL.md).

## Visual v2: tangible digital worlds

Original 2D vector illustrations with broad curved silhouettes, deliberate dark contours, hard offset depth, tactile devices and stylized human gestures. A hand gives a click weight; information becomes a distinct movable object; a service has a receiver; a local record can disappear while a remote object persists.

Keep the pale-lilac/white/ink/cobalt/teal/amber family, Bricolage Grotesque Bold and Instrument Sans. The color system now supports both pale stages and a cobalt full-frame stage. The identity comes from illustrated objects and their behavior rather than a fixed title/diagram/caption layout. Exact rules are in [frame.md](frame.md); rationale is in [DESIGN-PHILOSOPHY.md](DESIGN-PHILOSOPHY.md).

**Text:** zero visible words in all three current hero studies. A proposed production guide is usually 0–3 emphasis words at once, used only when an action needs an anchor. Narration carries detail; speech captions are a separate concise lower layer when narration is produced, with no competing explanatory paragraph. There is no permanent large headline band.

**Motion:** anticipate → contact → transfer → settle is demonstrated through four planned poses of the same identity scene. This is a planning vocabulary, not a fixed sequence for every episode. Preserve object identity, source/destination, local/remote boundaries and cause before response. See [MOTION.md](MOTION.md).

## Review package

- [style-board.png](style-board.png) and [style-board.html](style-board.html): the current sheet and editable source.
- `studies/passkeys.svg` / `.png`: a local face and separate proof object; hand/device interaction.
- `studies/privacy.svg` / `.png`: an illustrated local wipe and a retained remote visit object.
- `studies/delivery.svg` / `.png`: a source image remains while a distinct copy travels from a nearby cache.
- `studies/pose-1.svg` through `pose-4.svg`, plus [motion-poses.png](motion-poses.png): four planned states, not frames sampled from an animation.
- [phone-review.png](phone-review.png): the illustrations at 384px width.
- [VERIFICATION.md](VERIFICATION.md): inspected outputs, corrections and limits.
- [assets/SOURCES.md](assets/SOURCES.md): font provenance, factual anchors and metaphor boundaries.
- [ACCOUNTS.json](ACCOUNTS.json) remains empty. [AUDIO.json](AUDIO.json) still inherits the root voice default; an English voice must be resolved at production time.

## Interpretation limits

The hands, physical-looking receivers, ribbons, tokens, wipes and media cabinets are explanatory metaphors. They are not product screenshots, storage architecture, actual network paths or complete authentication choreography. The local face does not become the token sent to a website. A synced credential is not represented as necessarily device-bound. The privacy example concerns a Chrome Incognito session's local record, not complete invisibility or removal of downloads/bookmarks. The delivery example assumes an available cache hit.

No new technical claim or market estimate is inferred from the artwork. Existing factual source scopes carry forward; each episode still needs claim-level research and narration/visual consistency review.

## Review and next action

- Concept selected; v1 package not accepted.
- Visual v2 and editorial v2 implement the latest user feedback and await review as a concrete package.
- Current phase: static v2 package exported and inspected at sheet, native-frame and 384px phone sizes. The sheet is 1800 × 2441; hero studies are 1080 × 1920; four planned motion poses are included.
- Agent verification: zero visible text in all seven study/pose SVGs, no checked board overflow or browser failures, required sheet fonts loaded, original source preserved in its archive. A final refinement preserves the media artwork's aspect ratio across illustrated screens. See VERIFICATION.md.
- Next action: present v2 for feedback, including the text-free hero studies and planned motion poses.
- No episode, animation playback, audio or publishing action is represented as completed. Motion examples are planned poses only.
- Preview lifecycle: local files and a short-lived export browser; no server or review-hold process needed.
