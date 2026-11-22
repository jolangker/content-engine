# Di Balik Benda

- Version: v6, updated 2026-10-27 under an explicit user-directed board revision.
- Status: approved direction; v6 applies the user's explicit caption/framing preference to the accepted v5 package. No human approval of a new episode or unseen animation is asserted.
- Requested endpoint: adopt the narration-caption style and lower placement from `stapler-kaki-menutup`, and make objects larger, fitted to the available frame, and centered. Retain the v5 discovery framework, 2.5D identity, interaction/SFX requirements, and 90-second detailed-breakdown format.
- Current phase: board complete, ready for production selection.

## Intent and concept

Short-form Indonesian explainers that open up familiar objects and make their hidden mechanisms visible. The audience should move from curiosity to being able to describe a causal chain in their own words. The object and its behavior carry the story.

The user explicitly developed the idea of zooming into components, breaking assemblies apart, and showing how something works, then requested this board. After the visual board and linked editorial framework were presented together, the user replied "cocok" on 2026-10-23, accepting the presented board v1.

Board name: **Di Balik Benda**. Audience-facing promise: **Yang tersembunyi, jadi terlihat.** Default publishing targets are maintained in [ACCOUNTS.json](ACCOUNTS.json).

Publishing-account setup, 2026-10-25: the user requested board-owned account lists with multiple accounts per board. Instagram `dibalikbenda.id` is mapped to this board in Trypost Local using the matching live display name/username and this board's historical production receipts. The current workspace/account IDs were verified through MCP. This operational update preserves creative v4 and applies to newly resolved production targets; previous Buffer deliveries remain historical records.

## Narration voice configuration

On 2026-10-31, the user requested board-level voice configuration with the root environment as default. [AUDIO.json](AUDIO.json) currently sets `voice_id` to `null`, inheriting the root `.env` `ELEVENLABS_VOICE_ID`. This operational configuration preserves the accepted creative version and existing productions' audio; no new voice ID or regeneration was requested.

## Production contract

On 2026-11-22 the user approved gating productions against a board contract. [CONTRACT.json](CONTRACT.json) restates the v6 rules a finished episode can be checked against: the 90-second duration, the caption region, required narration and interaction SFX, the five-second state-change trigger, and ten judged rules drawn from the story contract, shot direction and medium lock. Each entry cites its source section and adds no creative rule. Creative v6, its approval, exports and existing productions are unchanged.

## Motion evidence

This board was approved before motion previews were required. Its v6 motion and framing direction is evidenced by the productions delivered under v6: `ketel-uap-memutus-arus`, `meteran-pegas-dan-rem` and `gabus-sayap-dan-gigi`. No motion preview is pending; build one when a revision changes the motion direction.

## Approved visual direction

An illustrated inspection bench: pale mineral surfaces, dark blue engineering ink, believable shaded parts, selective transparent sections, and a small functional color vocabulary. Reusable operations: isolate, disassemble, inspect, operate, and reconnect. Use any subset and order that explains the selected mechanism.

Use **2.5D illustration only**: layered parts, illustrated thickness, consistent shading, depth order, and restrained parallax. All whole-object, sectional, exploded, macro, and alternate views retain this language. Flat labels and arrows support the object; standalone flat 2D scenes, true 3D scenes, and mixed-medium sequences are outside the lock. The static examples use editable SVG illustration with shaded volume. A future animation test must establish temporal legibility and mechanical continuity.

See [frame.md](frame.md) for exact tokens and [EDITORIAL.md](EDITORIAL.md) for the approved framework.

## Version 2 production defaults

The user requested increased duration to 90 seconds and more frames because the animation breakdown felt insufficiently detailed, then explicitly clarified "untuk board". This is a direct instruction to update reusable production guidance. It does not request a new visual identity or an unseen animation for approval.

- Default duration: 90 seconds; verify the final timeline and export to within one output frame unless an episode explicitly overrides it.
- Shot planning: 14–18 explanatory shots, approximately 16 as a starting point, adaptable to mechanism complexity. This is a planning recommendation selected to implement the request, not a user-specified numeric quota.
- Detail: identify parts, expose relationships, show critical contact or transfer through intermediate poses, and follow the result or reset. Include useful macro and cutaway views according to the mechanism.
- Storyboard: record each shot's new information and 2–4 diagnostic poses for a complex action when needed. More frames means richer visual explanation, not higher fps.
- Pacing: an editable 90-second allocation is provided in EDITORIAL.md. Preserve time for observation and the operating cycle; expand supported explanation instead of stretching a short existing animation.
- Scope: these defaults apply to newly created productions that select v2. The existing pulpen, resleting, and jepitan-baju productions retain their recorded v1 direction and exports.
- Previous approved package: [revisions/v1/DIRECTION.md](revisions/v1/DIRECTION.md); source, exports, assets, and checks preserved with a hash manifest.

## Version 3 complexity and animation direction

The user reports continued monotonous animation and wants more complex mechanisms to break down. This follows the explicit board-scoped revision, so it updates reusable topic selection and choreography rather than an existing episode. The latest cable-tie production records 90 seconds and 16 shots around one local passing/locking interaction; that recorded scope motivates raising topic depth. Its full motion has not been reviewed in this board-edit turn, and no new playback-quality claim is made.

- Topic preference: several interacting subassemblies and linked state-dependent stages. Use approximately 3–5 meaningful causal interactions as a richness guide; do not equate visible part count with complexity.
- Selection: compare causal depth, visual discovery, motion diversity, evidence, and production scope. Ease of implementation must not default selection back to a single-contact object.
- Scope: explain one coherent subsystem or cycle of a richer mechanism within 90 seconds. Candidate seeds in EDITORIAL.md are research starting points, not verified technical claims or a selected episode.
- Choreography: coordinate coupled parts, preserve operating state across views, and alternate explanatory tasks and observation durations. Camera, annotation, or transition changes alone do not establish varied mechanism animation.
- Review: a shot map and motion review must identify repeated loops and framing with no new mechanical relationship. See [SHOT-DIRECTION.md](SHOT-DIRECTION.md).
- Version preservation: the previous v2 package is archived under [revisions/v2/DIRECTION.md](revisions/v2/DIRECTION.md), with source, exports, assets, and hashes. Existing productions retain their recorded board versions.
- The 90-second default and adaptable 14–18-shot planning range remain in effect. No new episode, audio, animation demonstration, or publishing action is implied.

## Version 4 visual lock, interaction, and sound

The user's 2026-10-25 revision explicitly requests 2.5D only, more interactions and animation so viewers stay aware and engaged, and SFX at interactions. Apply these as board requirements for future productions selecting v4:

- **Visual lock:** layered 2.5D illustrated geometry throughout, including cutaways and alternate views. Keep the existing palette, typography, material vocabulary, 90-second default, and adaptable 14–18-shot planning range.
- **Visible interactions:** every narrated causal interaction shows input, contact or transfer, and response. Increase observable action across the chain instead of relying on new labels, camera moves, or repeated unchanged loops.
- **Attention:** briefly cue the active part, animate the event, hand attention to the affected component, and hold the changed state. Use varied supported actions and timing without competing highlights or invented mechanism stages.
- **Interaction SFX:** every designed interaction event needs an event-synchronized sound or a recorded reason for intentional silence. Sustained and coupled actions may share a cue. Distinguish physical mechanism sounds from softer stylized editorial cues; keep narration intelligible and vary cues by action and material.
- **Production handoff:** each storyboard includes attention handoffs and a sound cue sheet. Review actual motion and the mix at full speed; check event onsets within one output frame unless an intentional lead or lag is recorded. A roughly 5-second no-state-change review trigger and cue-sheet details are agent implementation choices, not user-specified quotas.
- **Version preservation:** the previous approved package, source, exports, assets, and checks are preserved under [revisions/v3/DIRECTION.md](revisions/v3/DIRECTION.md), with SHA-256 hashes and existing-production file hashes. Existing productions retain their recorded direction.
- **Artifact scope:** the static board makes the lock and action/sound planning visible. Motion and audio remain conceptual until a production is requested; this revision generates no audio or animated demonstration.

## Version 5 discovery, audience appeal, and proof

After a research discussion and board review, the user explicitly requested "implementasi semua usulannya" on 2026-10-27. This accepts the six presented directions for board implementation. They are now requirements for future productions selecting v5:

1. **Central mystery:** one concrete question about a visible behavior, supported by the selected mechanism's evidence and answerable within the episode.
2. **Components when needed:** show the first meaningful causal discovery early and introduce each part at its functional use. Approximately 8–12 seconds is an editable first-discovery planning target, not a proven retention threshold. Avoid a front-loaded component catalogue; use an exploded view to resolve a real spatial question.
3. **Linked discoveries:** plan the question, visual answer, and next causal dependency for each story beat. Supply useful answers throughout rather than artificially postponing all explanation.
4. **Signature interaction:** select one physical event for the strongest close inspection; give its contact/transfer enough scale and observation time, reduce competing cues, and mark slowed timing where needed.
5. **Demonstrated ending:** pair the final demonstration with the opening behavior and show the hidden cause that answers it. Use recognizable context and a purposeful replay, section, or comparison.
6. **Audience appeal:** compare recognition/proximity, curiosity of the actual question, and visual proof alongside causal depth, visual discovery, motion diversity, evidence, and production scope. Record the reason for selection rather than predicting retention from a score.

EDITORIAL.md owns the topic rubric, episode story contract, voice, progressive disclosures, and revised editable 90-second allocation. SHOT-DIRECTION.md adds discovery/first-use/story-role fields and integrates all six checks into the existing production review checkpoints. frame.md keeps the same visual tokens and declares the story contract. The static board includes an independent conceptual opening/contact/answer study, the six refinements, topic-selection prompts, and revised pacing. These studies do not select or verify an episode.

The previous v4 package is preserved under [revisions/v4/](revisions/v4/), with SHA-256 hashes and a baseline of existing tracked production files and production registry entries. Existing productions retain their recorded board versions and media. The board remains approved because this implements the six explicitly selected directions; no additional approval gate is inferred.

Research used for the preceding discussion: [YouTube's Shorts creator interview](https://blog.youtube/creator-and-artist-stories/youtube-shorts-deep-dive/) supplies practitioner advice on hooks; [Gruber et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4252494/) investigates curiosity and memory; [Brame](https://pmc.ncbi.nlm.nih.gov/articles/PMC5132380/) reviews educational-video design; [YouTube retention guidance](https://support.google.com/youtube/answer/9314415?hl=en) informs later evaluation. Bodies were read through Jina during that discussion. The board refinements are a creative synthesis, not an experimentally established recipe for short-video completion. Evaluate actual outcomes with available episode analytics; record missing metrics and audience/traffic differences.

## Version 6 caption reference and large centered framing

The user explicitly prefers the caption style and placement in `stapler-kaki-menutup`, and the larger, screen-fitted centered object in that production. This updates reusable board direction for new productions selecting v6.

- Inspected the actual caption composition and the production's rendered 19-second review frame. Caption values come from `productions/stapler-kaki-menutup/video/compositions/captions.html`: Manrope 600, 46px/1.3, ink `#172B3B`, pale block `#F8F9F5`, 18px/26px padding, 14px radius; region x=108, y=1500, width=848 on a 1080x1920 canvas. The caption is a centered short phrase in a text-fitted block. The older SPEC.md summary says 43px; use the actual 46px composition.
- Keep that lower caption anchor across shots, with short speech-aligned phrases and at most two lines. Resegment long copy before shrinking it. Check destination overlays at production time.
- Center and enlarge the visible object or active subassembly within the usable mechanism stage. The implementation target is x=80..1000, y=430..1410, center x=540/y=920, with 80–95% occupancy of the width or height according to aspect ratio. These numbers operationalize the user's preference; they are not claimed measurements of all stapler shots.
- Fit actual geometry and the full relevant motion sweep, preserve contact and a recognizable landmark, and keep annotations clear of the caption. Use a purposeful macro crop of inactive context when needed. Avoid counting empty SVG bounds as a large object. Exact values and review checks live in frame.md and SHOT-DIRECTION.md.
- Preserve the previous accepted v5 package under [revisions/v5/](revisions/v5/), including source, exports, assets, and hashes. Existing productions retain their recorded versions and media. No production, audio, or publishing action is requested.
- Refresh the three independent 9:16 studies to show the adopted lower caption and tighter centered object framing, and add an explicit reference/fit guidance panel. Static sample phrases remain illustrative.

## Provenance and limits

- Creative source: the current user conversation; no external account or artist has been analyzed or copied.
- All mechanical illustrations are original schematic design studies, not engineering references or assembly instructions. Generic pump, valve, zipper, and gear geometry must be checked against the chosen real mechanism before episode reuse.
- All sample copy is illustrative. It is not a verified episode script.
- Fonts and their original licenses are stored under `assets/`; asset URLs and hashes are recorded in `assets/SOURCES.md`.
- Creative references consulted: local Shortform Board, HyperFrames Creative, house style, video composition, typography, motion principles, and design-spec guidance. Their decorative defaults are overridden by this concept's need for technical focus and purposeful stillness.

## Scope-specific interpretation

There is no universal decoration count, focal-point count, ambient motion requirement, mandatory font pairing, background sameness, or fixed narrative sequence. A single component on a quiet field is appropriate when it teaches clearly. The 14–18-shot range is a planning baseline, not a forced scene count. Retain readable type, functional color consistency, faithful motion, and reproducible production assets.

The current request authorizes the board revision, matching static source/export updates, and preservation of the previous package. Episode production, audio generation, and publishing remain separate requests.

## Review

- Concept: selected through the conversation.
- Visual v1: approved by the user's "cocok" response on 2026-10-23.
- Editorial v1: accepted with the presented board package in the same response; no separate confirmation requested.
- Editorial and production guidance v2: direct user instruction for 90 seconds and richer breakdown applied at board scope. Shot-range and timing allocations are implementation choices, not fabricated quotations or approvals of a new film.
- Editorial and choreography guidance v3: direct user instruction for more complex mechanisms and less monotonous animation applied at board scope. The causal-interaction guide and repetition-review trigger are implementation choices; no new animation is represented as human-approved.
- Visual, interaction, and sound guidance v4: direct user instruction on 2026-10-25 applied at board scope. The cue-sheet fields, roughly 5-second static-shot review trigger, and synchronization tolerance are implementation decisions. This records the requested board adjustment, not human approval of an unseen animated film or sound mix.
- Discovery and proof v5: the user selected all six presented refinements on 2026-10-27. Their implementation covers the editorial, visual/shot guidance, static source and inspected exports. First-discovery timing and the question-chain starting range are implementation choices. Actual retention, motion, and audio remain episode-level verification.
- Delivered v5 package: explicitly approved by the user's "approved" response on 2026-10-27, covering the presented editorial framework, visual/shot direction and static board. The current tracker entry remains `approved`. The accepted package is ready for future production selection.
- Caption/framing v6: explicit board preference on 2026-10-27; adopted the inspected stapler caption treatment and lower anchor, plus large fitted centered object framing. Numeric framing targets are implementation choices. Applies to new productions selecting v6; existing productions retain their recorded versions. Updated static samples receive agent visual verification; no new human playback approval is claimed.
- Motion and sound: conceptual only; no animated demo or audio generated.
- Verification: see [VERIFICATION.md](VERIFICATION.md) for the current static export checks and their limits.
- Next action: await an explicit episode or board-revision request. Approval of this board does not start a production or approve an unseen animation test.
- Preview lifecycle: file-based HTML and image exports only. No preview server created or retained.
