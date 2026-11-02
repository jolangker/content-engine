# Ruang di Antara — editorial v1.4 / visual v1.2

Status: `approved`. On 2026-11-02, after reviewing POV discontinuities in published scripts, the user instructed "implementasi semua yang lu sarankan". This accepts editorial v1.4: stable audience roles, explicit dialogue ownership and a narration-only continuity check, retaining the narrative structure accepted as v1.3 on 2026-10-25 with "apply adjustment ini". Visual v1.2, revision 02, remains the package accepted on 2026-10-21 with "cocok". This is the active reusable board for subsequent productions selecting `ruang-di-antara`.

## Publishing accounts

Default publishing targets are maintained in [ACCOUNTS.json](ACCOUNTS.json). It currently maps this board to Instagram `@eliansatya` in Trypost's `Admin's Workspace`; the workspace and exact account identity were verified during the 2026-11-02 analytics pull. Historical Buffer accounts and deliveries are preserved in their production records. Account configuration changes future target inheritance without changing this board's creative approval or authorizing delivery.

## Purpose and audience

Help Indonesian adults recognize everyday relationship experiences, understand a relevant psychology concept through the interaction and consider one concrete response or observation. Use intimate, observant lo/lu–gua speech, consistent within each episode: a reflection companion explaining a pattern. The five editorial pillars and source standards are defined in [EDITORIAL.md](EDITORIAL.md).

## Accepted direction

- Recognizable question hooks drawn from specific everyday situations, varying the entry point, viewpoint across episodes and framing rather than repeatedly opening with "Pernah nggak sih lo/lu...". Brief dialogue or an observation can lead into the question. The episode answers it.
- Preserve the audience role through each episode and identify dialogue speakers and instruction recipients under [POV continuity](EDITORIAL.md#pov-continuity--required-for-every-script). The narration alone must make each perspective transition understandable.
- Write the hook and bridge together. Vary bridges through a relevant reinterpretation, distinction, follow-up question, action or direct introduction; "mungkin bukan... tapi..." is an option when justified, not a repeated formula.
- Introduce one verified psychology concept early using its English name followed immediately by its Indonesian meaning and an everyday explanation. Use "itu namanya..." only for an actual example of the concept; avoid unsupported labels and diagnoses.
- Follow the opening with substantive discussion of how the concept relates to the scene, then one concrete application and a closing answer. Give explanation and discussion roughly half the narration as a flexible planning guide. Naming a term and moving directly to tips is insufficient. Detailed steps and checks are in EDITORIAL.md.
- Visual action occupies the principal content field: organic faceless participants, context-bearing illustrated objects, speech spaces, distance, connection, boundaries and traces.
- Short selective emphasis copy, full spoken captions and no supporting paragraphs that repeat the narration. The accepted implementation starts with 0–5 emphasis words where useful; current studies use 0–3. Longer necessary definitions or communication examples can be staged.
- Exactly sixteen meaningful frames, approximately ninety seconds (planning range 85–95). Plan multiple semantic animation beats inside each frame; 3–5 is the accepted starting guideline, adapted to reading and narration.
- Exactly two dramatic frames switch to charcoal background and cream text/captions/chrome. Fourteen use cream and charcoal. Select both dramatic moments from the script; example positions 04 and 12 are illustrative.
- Preserve the cream/charcoal/brick/sand palette, local Newsreader/DM Sans fonts and fixed series chrome. No gender, blame or diagnostic color coding. No B-roll.
- Intimate narration, sparse material sounds, purposeful silence and an episode-specific music decision. The richer visual rhythm does not impose an SFX quota.

Exact visual tokens, geometry, motion handoff and palette rules are in [frame.md](frame.md). Audio direction and library reuse are in [AUDIO.md](AUDIO.md).

## Package and limits

[Style board](style-board.png), [editable HTML/SVG](style-board.html), individual study PNGs, font files/licenses and optional PDF are available locally. Six samples are independent fictional studies, not an episode sequence or researched psychology claims. The four-pose strip describes changes within one frame; the sixteen-cell strip demonstrates rhythm.

Approval covers the editorial v1.4 direction and the previously accepted visual v1.2 package and conceptual motion/audio vocabulary. The static board remains the visual v1.2 reference; its independent fictional copy studies do not replace the active script structure in EDITORIAL.md. It is not a claim that animation smoothness, actual synthesized narration, a final audio mix or a new episode has been reviewed. Verification and preservation evidence are in [VERIFICATION.md](VERIFICATION.md).

## Review history and version preservation

V1 visual and editorial direction was accepted on 2026-10-16. V2 was tried and accepted on 2026-10-17, then the user returned to v1 visuals with denser approximately ninety-second explanations on 2026-10-18 as v1.1. Implementation and sound clarifications followed on 2026-10-20.

The actual final v1.1 root package, including these clarifications, original source/exports and assets, is preserved at [revisions/v1.1-final-2026-10-21/](revisions/v1.1-final-2026-10-21/). Earlier archives remain available. The v1.2 review record is in [drafts/v1.2/DIRECTION.md](drafts/v1.2/DIRECTION.md); its earlier text-led visual pass is retained under that draft's review-history/ folder.

On 2026-10-25, the user requested a revised script flow, clarified that hook and bridge phrasing should vary, required English concept names plus Indonesian meanings, reviewed a full active-listening sample narration and requested application. The final root v1.2 package was preserved at [revisions/v1.2-final-2026-10-25/](revisions/v1.2-final-2026-10-25/) before updating the accepted editorial guidance to v1.3. ARCHIVE.json records hashes of the preserved files. Visual and audio contracts and exports retain v1.2; this revision changes the editorial framework.

On 2026-11-02, the user accepted all recommendations from the published-script POV analysis. Before applying editorial v1.4, the active v1.3 root package and required assets/components were preserved at [revisions/v1.3-final-2026-11-02/](revisions/v1.3-final-2026-11-02/); ARCHIVE.json records hashes for all 31 files. The [POV review](reviews/2026-11-02-pov.md) records findings for all twelve published scripts and corrected fictional passages for the eight affected episodes. The production research/script reference now requires the selected board's continuity check and carries its actor mapping through synthesis text, captions and storyboard actors.

Existing production briefs, specifications, media and tracker selections retain their recorded direction. This board revision governs subsequent production intake unless the user requests a revision of a particular existing production. Historical correction examples are editorial guidance, not replacements for published episode artifacts.

## Narration voice configuration

On 2026-10-31, the user requested board-level voice configuration with the root environment as default. [AUDIO.json](AUDIO.json) currently sets `voice_id` to `null`, inheriting the root `.env` `ELEVENLABS_VOICE_ID`. This operational configuration preserves the accepted creative versions and existing productions' audio; no new voice ID or regeneration was requested.

## Current phase and next action

Editorial v1.4 is applied and approved by the user's implementation instruction. No board review remains pending. Use editorial v1.4 with visual/audio v1.2 when a subsequent production selects this board, and complete its POV contract and narration-only continuity check before advancing the script. Existing productions retain their recorded versions; use the POV review's repair examples when an episode revision is requested.

## Analytics review — 2026-11-02

The user's request for insights on "di-antara-kita" was resolved to this registered board and its configured account. The completed [analysis](insights/2026-11-02/ANALYSIS.md) and [source snapshot](insights/2026-11-02/snapshot.json) cover the October 4–November 2 publication cohort: twelve posts, eleven with saved metrics. Positive everyday-connection episodes lead views, while shallow average watch warrants a controlled opening experiment. Per-post metric timestamps differ and the latest post has no metrics, so these are provisional findings. Analytics recommendations remain unapproved experiments, separate from the accepted editorial v1.4 POV revision above; visual v1.2 and the approved tracker status remain active. Next analytics action: obtain comparable 24-hour, 72-hour and 7-day snapshots, especially for the newest posts, before treating the ranking as stable.
