# Historical draft reference — superseded for new productions

The user applied the developed draft as the approved canonical [Berkas Polemik v3 board](../../DIRECTION.md) on 20 October 2026. The notes below retain their historical review statuses. This registered draft path is preserved for productions that already selected `berkas-polemik-v3-draft`; it is not the active choice for new episodes. Existing production references remain unchanged.

---

# Berkas Polemik — visual refinement v3

Status: awaiting visual review. Prepared 20 October 2026. This draft responds to the user's feedback on v2: **“masih terlalu banyak teks di frame dan kurang visualisasi”** (too much frame text and insufficient visualization).

## Revision scope

The v2 visual treatment was not accepted. Its enlarged type still treated frames as reading sheets. V3 changes the presentation model: a short headline and one dominant visual perform the explanation. Retain the approved forensic-dossier identity, palette, and local font families. Keep v1 active at the board root and preserve v2 as revision history.

The wider editorial proposal remains pending. The user has explicitly confirmed the duration and scene count below; that confirmation does not approve the rest of the visual or editorial package. See [the editorial proposal and pacing template](EDITORIAL.md).

## Confirmed production format

On 20 October 2026, the user specified **approximately 90 seconds with exactly 16 primary frames/scenes**: “gua mau di ~90s dengan 16 frame”. This replaces the earlier 60–90-second default and the assistant's unaccepted 65-second / 10-scene suggestion for this refinement.

Here, a frame means a storyboard composition/scene, not an individual encoded video frame. Detail changes within a composition do not increase the count unless they become a separate storyboard scene. Plan 16 numbered scenes, averaging 5.625 seconds, with duration adapted to the narration and evidence. The [90-second pacing template](EDITORIAL.md#the-dossier-structure) uses varied 4–7-second scenes.

Confirmed constraints apply to future productions using this refinement. They do not authorize an episode, create 16 episode-specific designs, or change existing productions. The three current visual studies remain independent identity samples.

## Proposed visual decisions

- Use a 3–4-word headline in these studies, with no explanatory paragraphs inside the frame.
- Allocate roughly two thirds of the essential content area's height to one visual construction.
- Communicate differences through actual object relationships: marked versus unmarked documents, enlarged detail, and an interrupted document field.
- Move longer explanation into narration and board documentation. Production source locators and essential qualifiers remain visible when needed; do not remove them merely to meet a word budget.
- Treat each graphic as an explanatory illustration, explicitly labelled simulation. A missing mark does not establish forgery; an empty region does not establish destruction.

## Independent studies

| Study | Main copy | Visualization |
| --- | --- | --- |
| A | “Satu tanda hilang.” | Two offset paper objects, with an annotated mark on A and its empty counterpart on B. |
| B | “Periksa kata kuncinya.” | A large physical loupe isolates the simulated word “ditunda”. |
| C | “Jejaknya belum utuh.” | Two document fragments surround a conspicuous empty region. This is a metaphor for a gap, not a reconstruction of a damaged historical record. |

These are independent design studies, not a historical argument or episode sequence. No real archive, seal, quotation, signature, or historical number is represented.

## Files and provenance

- [style-board.png](style-board.png): full review board.
- [frame-studies.png](frame-studies.png): direct view of the three revised frames.
- [style-board.html](style-board.html): editable HTML and inline SVG source.
- `study-01.png` to `study-03.png`: native 1080 × 1920 studies.
- `phone-study-01.png` to `phone-study-03.png`: 360 × 640 review exports.
- [frame.md](frame.md): visual specification and text budget.
- [QA.json](QA.json): export checks and recorded inspection.
- [build-board.py](build-board.py): reproduces this revision from the preserved v2 board with local SVG illustrations.
- [export-board.py](export-board.py): renders the review PNGs.
- Fonts and licenses remain in `../../assets/`.

Registry discovery used `hyperframes catalog --query "archival document comparison magnifying glass missing evidence" --json` on the `words` tier. The returned comparison-split and before-after-wipe items are moving split-panel treatments; none supplies the static archival/loupe/missing-record illustrations needed here. The illustrations were therefore authored as editable SVG, without installing a video project or adding animation.

## Review and next action

Review whether the three frames now communicate visually with sufficiently little reading. Motion and audio remain conceptual. No user approval is recorded. Keep the root tracker `approved` for v1 while this draft is under review. Promote a revision only after the relevant layers have been accepted.

## Motion feedback and proposed refinement

On 20 October 2026, the user asked how motion would work and explicitly requested richer motion to make the content more engaging. The desired richness is confirmed; the specific treatment is proposed in [MOTION.md](MOTION.md): a layered archival workspace, meaningful internal actions, and object/shape continuity between scenes. It preserves approximately 90 seconds and sixteen primary scenes, with sparse text.

Next action for the motion layer: review this proposed choreography. No composition, animated demo, narration, or sound has been created. The static visual package and wider editorial proposal remain pending independently of the confirmed format and motion preference.

## Dry-run feedback — slide transitions

The user tested [penutup-proklamasi](../../../../productions/penutup-proklamasi/EPISODE.md), which explicitly selected the registered `berkas-polemik-v3-draft` board. They reported that slide transitions between frames felt monotonous. The test's source confirms ten leftward push-slide transitions among fifteen boundaries, including five consecutive pushes at the beginning with identical 0.5-second timing.

Confirmed correction: full-scene slide/push transitions are excluded for this refinement. The former nine-directional-handoff target is removed. Internal object movement remains valid; the criticism concerns inter-scene presentation. [MOTION.md](MOTION.md) now specifies relationship-driven cuts, anchor matches, source-to-detail continuity, local masks, and selective dissolves as the replacement proposal. The previous motion proposal is preserved under `revisions/`.

Current state: overall board remains draft, with the revised transition proposal ready for review. The broader visual/editorial package has not been approved. The completed test production and its export are unchanged by this board-guidance revision. Next action: collect any remaining dry-run feedback and assess the revised transition language when implemented; preserve the approximately 90-second / sixteen-scene format.

## Confirmed topic focus and research preference

The user specified: “gua mau topik pembahasan sejarah kelam dan konspirasi di indonesia sih dengan sumber dari buku, jurnal, etc”. The selected niche is therefore dark Indonesian history and conspiracies in Indonesia, with books, journals, and other credible traceable material as the research base. This replaces generic contested-history selection as the draft board's topical priority.

[EDITORIAL.md](EDITORIAL.md) now implements this focus through five relevant pillars, a niche-first topic-selection gate, and passage-level book/journal sourcing. It distinguishes documented coordination, source-backed disputed allegations, and circulating conspiracy narratives without predetermining the conclusion. A dark-history topic need not involve a conspiracy to qualify.

The niche and source preference are user-confirmed. The detailed editorial implementation and revised audience promise are proposals; this preference does not approve every board layer. The previous editorial text is preserved in `revisions/editorial-before-dark-history-focus.md`. Existing productions are unchanged, and no new episode or topic research has been started. Overall board status remains draft.

## Focus reset accepted

After discussing current political news, the user said the direction felt unclear. The assistant recommended returning to one account promise: **“Berkas Polemik membedah sejarah kelam dan dugaan konspirasi di Indonesia lewat penelusuran sumber.”** The user accepted with “oke boleh”. This accepts the core editorial positioning, the dark-history/conspiracy scope, and the books/journals/documents research base.

Daily political news remains an unadopted expansion, not a third pillar or a required posting mix. Current events can supply a reason to revisit history, but standalone regime/news commentary is outside the default topic gate. [EDITORIAL.md](EDITORIAL.md) records this accepted focus and prevents automatic topic selection from drifting into general news or minor historical trivia.

Approval scope: the focused editorial positioning only. It does not approve every detailed sourcing rule, the full visual/motion revision, or a new episode. The registered draft stays `draft` while those layers remain unresolved. Next action: use this clear topic gate in subsequent board discussion or an explicitly requested production.

## Two dramatic reversed-color scenes requested

The user requested two frames with background and text colors swapped at dramatic script moments, and asked whether contrast/readability would remain safe. This is a confirmed format preference: fourteen normal dark scenes and two light reversed scenes within the existing sixteen-scene total. Their positions depend on the episode's actual dramatic beats.

[frame.md](frame.md#two-dramatic-reversed-color-scenes) specifies manila background with carbon/ink text, plus restrictions for red, yellow, and steel accents. The [static color proof](reversed-studies.png) and [computed contrast report](reversed-contrast-QA.json) make the choice reviewable. The variation is authored by remapping editorial surfaces, not blindly inverting historical media. No completed or in-progress production was modified by this board-level change. The board package remains draft pending the unresolved visual/motion review.
