# Behind the Screen — illustration, title and subtitle direction v3

Status: `approved`. The user accepted the presented v3 board with “cocok” on 2026-11-03. This accepts the illustrated direction, short titles and displayed karaoke subtitle treatment, together with the previously presented board concept. Editorial v3 implements that concept. Motion timing, narration and actual subtitle synchronization still require production-level verification.

## User direction

On 2026-11-03 the user selected the Behind the Screen concept, then gave this feedback on the first static draft: “gua mau visual yang lebih ilustratif dan sedikit teks. gua mau main di motion design”. This revision makes illustration, object behavior and motion planning central. It replaces the first draft's large per-frame headlines and labeled diagrams.

The user's direction authorizes this board revision. The specific style, text budget, staging and timing below implement that direction; they are not quotations from the user or approval of unseen animation. The previous unapproved package is preserved under [revisions/v1-draft/](revisions/v1-draft/), with its files and hashes in ARCHIVE.json.

The user subsequently clarified: “tetep butuh teks untuk judul dan subtitle. subtitle gua prefer yg katole style gitu”. This supersedes v2's zero-text interpretation. The complete unapproved v2 package is preserved under [revisions/v2-draft/](revisions/v2-draft/). No matching “katole” reference was identified. Karaoke was presented as an interpretation; the user's subsequent “cocok” accepts the displayed treatment and resolves the open styling choice without claiming an exact external-reference match.

## Concept and audience

**Promise:** Understand what happens behind your everyday clicks.

English-language vertical explainers for non-specialists. The proposed initial markets remain the US, UK, Canada and Australia. They are positioning choices, not measured audience demographics. The four pillars remain identity/access, copies/memory, connections/delivery, and visibility/control.

The explanation begins with a familiar action, makes a hidden relationship tangible, and returns to its visible consequence. Narration explains the technical meaning while the illustration demonstrates action, transfer, separation or persistence. See [EDITORIAL.md](EDITORIAL.md).

## Visual v3: tangible digital worlds, titles and subtitles

Original 2D vector illustrations with broad curved silhouettes, deliberate dark contours, hard offset depth, tactile devices and stylized human gestures. A hand gives a click weight; information becomes a distinct movable object; a service has a receiver; a local record can disappear while a remote object persists.

Keep the pale-lilac/white/ink/cobalt/teal/amber family, Bricolage Grotesque Bold and Instrument Sans. The color system now supports both pale stages and a cobalt full-frame stage. The identity comes from illustrated objects and their behavior rather than a fixed title/diagram/caption layout. Exact rules are in [frame.md](frame.md); rationale is in [DESIGN-PHILOSOPHY.md](DESIGN-PHILOSOPHY.md).

**Text:** short opening/section titles are required; spoken subtitles occupy their own lower band. The illustrations carry the action and remain large. The 0–3-word guide applies only to additional emphasis, not titles/subtitles. Current samples each show a two-line title and one short subtitle phrase.

**Accepted subtitle treatment:** Instrument Sans Bold, a dark rounded phrase panel, white inactive words, one amber highlight behind the active dark word. Phrase layout stays fixed; the highlight follows actual speech onsets in production. The current board shows four static highlight states. The displayed treatment is accepted; no further clarification is needed to use it.

**Motion:** anticipate → contact → transfer → settle is demonstrated through four planned poses of the same identity scene. This is a planning vocabulary, not a fixed sequence for every episode. Preserve object identity, source/destination, local/remote boundaries and cause before response. See [MOTION.md](MOTION.md).

## Review package

- [style-board.png](style-board.png) and [style-board.html](style-board.html): the current sheet and editable source.
- `studies/passkeys.svg` / `.png`: a local face and separate proof object; hand/device interaction.
- `studies/privacy.svg` / `.png`: an illustrated local wipe and a retained remote visit object.
- `studies/delivery.svg` / `.png`: a source image remains while a distinct copy travels from a nearby cache.
- `studies/pose-1.svg` through `pose-4.svg`, plus [motion-poses.png](motion-poses.png): four planned states, not frames sampled from an animation.
- [phone-review.png](phone-review.png): the illustrations at 384px width.
- [subtitle-style.png](subtitle-style.png) and four `studies/subtitle-state-*.svg` sources: the accepted karaoke treatment with four active-word states.
- [VERIFICATION.md](VERIFICATION.md): inspected outputs, corrections and limits.
- [assets/SOURCES.md](assets/SOURCES.md): font provenance, factual anchors and metaphor boundaries.
- [ACCOUNTS.json](ACCOUNTS.json) remains empty. [AUDIO.json](AUDIO.json) still inherits the root voice default; an English voice must be resolved at production time.

## Interpretation limits

The hands, physical-looking receivers, ribbons, tokens, wipes and media cabinets are explanatory metaphors. They are not product screenshots, storage architecture, actual network paths or complete authentication choreography. The local face does not become the token sent to a website. A synced credential is not represented as necessarily device-bound. The privacy example concerns a Chrome Incognito session's local record, not complete invisibility or removal of downloads/bookmarks. The delivery example assumes an available cache hit.

No new technical claim or market estimate is inferred from the artwork. Existing factual source scopes carry forward; each episode still needs claim-level research and narration/visual consistency review.

## Review and next action

- Concept selected; v1 package not accepted.
- User review: “cocok” on 2026-11-03 accepts the presented v3 board and karaoke subtitle treatment. Visual v3 and the editorial framework for the accepted concept are ready for future production selection.
- Current phase: v3 exported and inspected at phone size; typography/clearance and archive/configuration audits pass. Sheet: 1800 × 2665; hero studies: 1080 × 1920. Four isolated motion poses and four subtitle style states are included. Minimum measured illustration/subtitle clearance: 68.08px. See VERIFICATION.md.
- Next action: await an explicit production or board-revision request. No new production is started by board acceptance.
- No episode, animation playback, audio or publishing action is represented as completed. Motion examples are planned poses only.
- Preview lifecycle: local files and a short-lived export browser; no server or review-hold process needed.
