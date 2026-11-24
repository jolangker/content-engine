# Budidaya di Halaman

Revision 6. Editorial v6 and visual v4 approved on 2026-11-23, including the motion preview; see [Visual v4](#visual-v4-price-tag).

## Approved direction

On 2026-11-21, the user narrowed the concept to home-yard cultivation, ponds, and related activities, then replied “cocok” to the updated proposal and creation question. This authorized building the board for that niche. The complete visual and editorial package was approved by the user on 2026-11-22.

The audience is Indonesian-speaking general viewers curious about growing and raising things in a small yard. The viewer starts building on the first spoken beat, puts a simple version into use, and develops that same setup in response to what happens. The episode culminates in the working pond, rearing setup, or other backyard production system that the viewer has seen take shape. Then one scene shows what its first output is worth. Backyard aquaculture anchors the scope. Episodes are delivered at 1.25x. Every connected account gets one shared content package, and the thumbnail doubles as the film's end card.

## Reference and adaptations

The three local `jadiginisodara` reels establish the vertical illustrated cutaway, rapid setup, repeated problem and repair, progressive white-and-yellow captions, and final site-wide reveal. [Timestamped evidence and coverage](references/ANALYSIS.md) records the sources, selected frames, and limits of visual and acoustic analysis.

The studies use original locations, layouts, illustrations and sample wording. DM Sans is a selected typeface substitute, and the colors and dimensions are implementation choices informed by the visible roles in the clips. The overall mix direction uses the measured prominence of the separated vocal stem. Delivery, music and effects are creative specifications for future episodes.

## Package

- [Editorial framework v6](EDITORIAL.md) and [visual specification v4](frame.md).
- [Editable style board](style-board.html), [PNG preview](style-board.png) and [phone view](style-board-phone.png), rendered by [capture.py](capture.py). Three independent studies cover a pond and its outlet, aeration in a hatchery, and a live-feed harvest. A separate strip shows three static positions of a flow reveal. The revision 6 row adds the [income scene](income-study.png), the [thumbnail](thumbnail-study.png) with its crop check, the timeline position of both new beats and the shared-package rules. Revision 6 drawings live in [assets/studies-r6.js](assets/studies-r6.js).
- [Motion preview](motion-preview.mp4) and its [editable project](motion-preview/index.html); `motion-preview/build_draw.py` regenerates its copy of the study helpers.
- [Voice configuration](AUDIO.json) sets ElevenLabs **Pribs – Friendly Casual Narration** (`5g0yKK2JwTRka0IG61Hh`) as the board default, as selected by the user. [Publishing accounts](ACCOUNTS.json) configures Instagram `@bikindihalaman.id` in Trypost (`Admin's Workspace`), selected and confirmed by the user on 2026-11-22. The YouTube channel **Bikin Di Halaman** (`@bikindihalaman_id`, same workspace) was added on 2026-11-22 at the user's request ("koneksian dahulu youtube Bikin Di Halaman"), matched by display name against the live Trypost account list. The Facebook page **Bangun Di Halaman** was added on 2026-11-22 at the user's request; Trypost returns no username for it, so `handle` records the page display name. The Instagram account stays first in the list; the closing-caption handle cue uses that first account.
- [Production contract](CONTRACT.json) restates the editorial v6 / visual v4 rules a finished episode can be checked against: 90–112.5 s at 1x with `delivery.speed` 1.25, first action within the first second, caption region, narration with effects and no music, and ten judged rules. The rules include `income-scene` and an end card in `closing-signature`. A contract was first added on 2026-11-22, when the user approved gating productions against a board contract; each entry cites its source section.
- Motion evidence: the [motion preview](motion-preview.mp4), reviewed with revision 6. Before it, the board's motion direction was evidenced by the `kentang-dalam-pot` and `pot-sumbu-selada` exports.
- Revision 5 (editorial v5, visual v2, its contract and style board) is preserved in [revisions/5](revisions/5/).

## Revision 6

Requested by the user on 2026-11-23: add one income scene once the system works, deliver renders at 1.25x, make a thumbnail and check whether Trypost can upload one, and stop differentiating the content package per platform or account. On the same day the user chose: the duration window applies to the 1x composition at 90–112.5 s, so the 1.25x file runs 72–90 s and fits a Facebook Reel; the income scene shows a sourced rupiah estimate; the thumbnail is delivered as a PNG plus an in-video end card.

Prepared in `drafts/r6/` and promoted to the board root on approval; the v5 package moved to `revisions/5/`.

Trypost check (2026-11-23, `list-content-types-tool` and the post tools): Trypost has no custom thumbnail image upload. A video item's `meta.cover_offset_ms` chooses a cover frame on content types with `supports_video_cover`: `instagram_reel` and `instagram_feed` support it, while `youtube_short`, `facebook_reel` and `facebook_post` do not. This is why the thumbnail is also the film's end card. The workspace-wide tooling now supports this: the contract field `delivery.speed` makes the export gate measure a retimed file against its 1x composition, and the content-package and publishing references follow a board-level shared package and the cover-frame route.

Visual review of the draft (2026-11-23, 1440 px board, 1080 × 1920 studies, 390 px phone view): the first income render hid the keeper and basin behind the card, and its scale was too small to be the decisive interaction. The card was moved into the sky, and the scale, basin and keeper were enlarged so the weighing spans more than 40% of the width. Fish drawn behind the bowl and basin rims were redrawn on top. In the thumbnail, a band between the filled sky and the pond scrim was removed by matching their colour. Remaining limit: the income figures (10 kg, Rp25.000/kg, Nov 2026) are illustrative and have no source.

The user approved the static draft on 2026-11-23 ("approve"). This covers editorial v6, the visual spec v3 and the style board with its studies. Because the revision changes the motion direction, the board's approval still waits for the motion preview.

Motion preview: [motion-preview.mp4](motion-preview.mp4) (SHA-256 `c10e76c6…0781`) and its [editable project](motion-preview/index.html). It is a 24.83 s composition at 1x, rendered as a 24 fps master (`motion-preview/verification/master-24fps.mp4`, 596 frames) and restamped to 30 fps with the audio time-stretched 1.25x, pitch kept. The delivered clip is 19.88 s, 1080 × 1920.
- What it demonstrates:
  - The build hook: bare yard, digging from 0.25 s, liner, filling, fish.
  - A hard cut to the income beat: three fish onto the hanging scale, the needle settling, and the income card entering with the total chip arriving last and held 3.1 s at 1x.
  - A cut to the closing wide pull-out: congratulation and next-build question, "bikin di halaman" staying yellow, the handle fading in.
  - A hard cut to a 0.5 s end card identical to the thumbnail. Instagram's cover would point at about 19,620 ms.
- Sound: narration in the board voice and CC0/Pixabay effects; sources are in `motion-preview/assets/audio/CREDITS.md`.
- Measurements (`episode_qa.py --fingerprint`, caption region masked): first motion 0.2 s, longest static 0.2 s, held share 0.0, −13.64 LUFS, −1.86 dBTP.
- HyperFrames check: no errors. Remaining warnings follow approved board positions (cover at 240 px, captions at 1392 px, handle beneath them, outside some platform safe zones) and the intentionally short end card (0.6 s against a 2 s closing-line floor).
- Twelve decoded frames of the delivered clip were inspected.
- Limits at build time: the agent could not hear the mix (`listening: unavailable`); the figures and price month are illustrative.

The user watched the motion preview and approved it on 2026-11-23 ("approve"). Revision 6 is now the board's approved package: new productions selecting this board use editorial v6, visual v3 and its contract, while existing productions keep their snapshots. Remaining limits: the illustrative income figures, and the user's listening approval is the only listening record of the preview mix.

## Revision 7 (draft, awaiting review)

Requested by the user on 2026-11-24: vary hooks within the pattern "Kalo kamu {aksi}.., {konjungsi temporal} kamu {aksi}.., kamu sudah punya... Tapi, {masalah}..."; give scripts the chain premature first system → problem → improvement → new problem → improvement again → problem–improvement loop → stable system → monetization → closing (closing unchanged); and make clear the board is not limited to dug pits.

Editorial v7 is prepared in [drafts/r7/EDITORIAL.md](drafts/r7/EDITORIAL.md) with its [contract](drafts/r7/CONTRACT.json) (`build-first`, `shortfall-before-fix`, `final-job` and `income-scene` reworded; `hook.first_sentence_max_seconds` raised to 10 s and a `tapi` turn required by 12 s; the contract validates). Visual v4 is unchanged. Until the user approves, editorial v6 at the board root stays the approved package and the tracker entry stays `approved`.

- Open: the motion preview still speaks the v6 hook ("Kalau kamu gali lubang…, jadilah kolam lele sendiri"). Refreshing it needs new narration and a re-render.
- Next action on approval: move the v6 `EDITORIAL.md` and `CONTRACT.json` to `revisions/6/`, promote the drafts to the board root, and update this file.

## Visual v4: price tag

On 2026-11-23 the user rejected the income card and its animation: "cardnya terlalu blocking dan animasinya lambat". They chose a tag hung on the scale. Visual v4 replaces the card with a 400 px paper tag hung by a string from a nail on an overhang of the scale beam (nail at 600, 594 px). It holds only the sum, the yellow total chip and a two-line `estimasi harga pengepul / Nov 2026` note at 28 px, the phone type floor.
- Timing: it drops in 0.2 s on "sepuluh" (10.8 s at 1x) and its swing settles within 0.5 s. Each figure pops in 0.15 s on its word (13.04 s and 14.72 s), and the tag grows downward. The total holds 3.1 s at 1x.
- Supporting changes: the slow drift zoom in the income scene was removed so the tag stays on its nail. The editorial wording and the `income-scene` contract rule now say "price tag", with the contract revision set to editorial v6 / visual v4. No production references visual v3, so v3 survives in Git history rather than under `revisions/`.
- Updated files: [frame.md](frame.md#price-tag), [income study](income-study.png), [style board](style-board.png), and the re-rendered [motion preview](motion-preview.mp4) (SHA-256 `c789edc1…bb11`, 19.88 s delivered).
- Measurements: first motion 0.2 s, longest static 0.2 s, −13.68 LUFS, −2.05 dBTP. HyperFrames craft now warns only about the intentional 0.5 s end card.

The user approved visual v4 on 2026-11-23 ("approve") after watching the re-rendered motion preview. New productions selecting this board use editorial v6 / visual v4 and its contract.

## Review

The first nila script followed a particle through a completed system. Editorial v2 made the keeper's goal, first attempt, visible shortfall, response, and retest part of angle selection. The maggot production then opened with a scoop from an established bin, so its build covered a collection improvement. On 2026-11-22 the user clarified that a board episode starts with the creation of the cultivation setup itself. The user also set a 90-second minimum, asked for more events, and specified a closing congratulation followed by a question about what to build next. Editorial v3 applies those requirements at topic selection and script review, with a 97-second illustrative catfish outline.

The user clarified that the build should be the subject of the episode, as in the reference pond and farm scripts. Editorial v4 compresses the initial build, then makes the system's development and first working result the story. It includes a 100-second illustrative outline. [Script evidence by reference](references/ANALYSIS.md#script-structure-across-the-references).

The user approved the editorial v5 / visual v2 package on 2026-11-22; revision 6 replaced it on 2026-11-23 and it is preserved in [revisions/5](revisions/5/). Earlier editorial revisions remain available as [v1](revisions/1/EDITORIAL.md), [v2](revisions/2/EDITORIAL.md), [v3](revisions/3/EDITORIAL.md), and [v4](revisions/4/EDITORIAL.md); visual v1 is preserved as [v1](revisions/1/frame.md). Visual v1 was exported at 1440 × 1328 and inspected together with all three portraits at a 390 px phone viewport; visual v2 keeps the same approved visual assets and adds only the closing caption signature cue.

The compositions and motion poses are static. The user set the board's audio direction to narration with scene-linked sound effects and no background music. [Current audio direction](frame.md#audio). On 2026-11-22, the user also approved embedding the consecutive signature phrase **bikin di halaman** into the spoken closing question (no opening intro or spoken follow CTA), paired with the yellow closing caption highlight and subtle handle cue in [frame.md](frame.md#framing-and-captions).
