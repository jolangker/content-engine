---
name: video-to-board
description: Use when a new creative board should follow the visual, storytelling, motion, or audio style of supplied reference videos, including a local folder of clips from the same creator or style.
---

# Video to Board

Translate a reference video's creative grammar into a reusable board. Follow the reference style and apply the user's stated changes. This skill owns board synthesis and the single approval gate before creation. [shortform-board](../shortform-board/SKILL.md) owns the board package and technical verification.

## Establish the reference

Read project instructions, `TRACKER.json`, and shortform-board. Discussion stays in conversation. Identify the supplied reference folders, video files, or URLs and any user direction already given. Request a missing or inaccessible reference before claiming an analysis. A bare invocation does not select an existing board or start production.

Load [rea-video](../rea-video/SKILL.md) to decompose and review each supplied clip. Follow [video analysis](references/video-analysis.md) for clip discovery, native audio review routing, and timestamped evidence. For a local reference folder, persist the analysis in its `_analysis/` subfolder before presenting the proposal. Keep the proposal and its revisions in conversation and defer board files and tracker changes until the build step.

Aim for a faithful reading of the supplied style rather than a menu of new creative directions. Distinguish observed evidence, interpretation, and proposed implementation choices. Preserve the reference's recognizable composition, narrative delivery, pacing, motion, and audio relationships where the user has not requested changes. Treat episode subject matter as evidence of that episode, not proof of the account's entire niche.

## Align the vision at one approval gate

After analysis, present a concrete proposal in natural Indonesian with:

- A concise reading of the reference, supported by representative timestamps and any important access limits.
- The saved analysis path for local references.
- What the board will retain, what will change under the user's direction, and uncertain details requiring a proposed substitute.
- The intended audience experience, proposed content scope, and reusable storytelling, visual, motion, and audio rules.
- The [measures](references/video-analysis.md#measure-each-clip) per clip and the story shape the beat maps share, with the numbers proposed for the board's production contract and the measure each comes from.
- A transfer test: a beat outline for a different, illustrative topic set row by row beside one reference's beat map, with planned times, so a difference in structure or pace is visible before anything is built.
- Audio stated as decisions: the narration voice's character, music use or none, and effect density, each marked heard, measured only, or proposed.

State material assumptions as proposals. Resolve ambiguity that changes the outcome here, including conflicts between the user's direction and the reference. Missing content scope can be proposed here; it need not trigger a separate intake gate.

Whenever the user supplies direction or corrections, synthesize the reference and **all current user direction** into an updated vision. Explain retained traits, intentional changes, and the resulting experience through a concrete example. Check this synthesis with the user before creating the board. Acknowledge-only replies such as "understood" do not establish alignment.

The gate may contain several discussion turns, but it remains one gate. Corrections, a new preference, a broad request to make a board, or silence are not approval of an unseen or revised vision. Proceed only when the user explicitly authorizes creation against the latest presented synthesis. A brief "gas" or "lanjut" can authorize that synthesis when its referent is clear. If a reply combines approval with a material new direction, present the updated synthesis and wait for confirmation; do not silently treat the addition as an approved design.

End the gate response with one concise question that asks whether the summarized vision matches and the board can be created. Explain that this checkpoint comes from the user's requested workflow in this [skill](SKILL.md). Do not create a second gate solely to ask the same permission again. On continuation, use the conversation's latest proposal and response; if their scope cannot be recovered, re-establish it before board creation.

**Gate exit:** the latest synthesis is visible, material conflicts are resolved, and the user has explicitly confirmed that vision and authorized creation. Later material changes before creation return to this same gate. After creation starts, follow requested revision scope and ask only for unresolved information that is necessary to proceed.

## Build the approved direction

After the gate exits, carry the approved synthesis forward as the brief. Follow shortform-board's [board files and state](../shortform-board/references/board-files.md), look/spec guidance, and [visual package workflow](../shortform-board/SKILL.md#build-and-review-the-visual-package). For this route, complete and verify the requested draft package in one pass, then present it for feedback. The user may give feedback during the build or explicitly request a pause.

Create the board at its collision-checked registered path, using the existing board package format rather than inventing another schema. Record the approved direction, approval scope, reference provenance, and deliberate adaptations in `DIRECTION.md`. Save the timestamped evidence and coverage limits in board-local `references/ANALYSIS.md`, with selected supporting frames when useful. Link the board evidence from `DIRECTION.md` and keep the full analysis for local references in the source `_analysis/` directories.

Translate observations into actionable reusable rules in `frame.md` and `EDITORIAL.md`, and restate the checkable ones in the board's [production contract](../shortform-board/references/board-files.md#production-contract). Identify estimates and selected substitutes. Show independent sample compositions using different illustrative material in the static style board. Set the contract's measured limits from the reference measures and cite them in `sources`. Build the motion preview as the pilot scene of the approved synthesis and compare its fingerprint with the references'. Record any remaining conceptual motion and audio behavior.

The approved direction authorizes building the package; it does not approve unseen board artifacts. Deliver the completed, inspected package as `draft`, with its completed scope and optional feedback recorded in `DIRECTION.md`. Do not block delivery on a second mandatory approval. Set `approved` only if the user subsequently accepts the actual visual and editorial package, following shortform-board's state rules.

## Verify and deliver

Check fidelity against the approved synthesis, the timestamped evidence and the reference measures, including user-requested departures: the motion preview's first motion, held share and speaking pace sit with the references', or the difference is a recorded decision. Verify that the visual source and preview agree, fonts load, text is readable, and sample compositions apply the style to different material. Check links, tracker parsing, and the registered board path. Report any remaining unknowns rather than filling them with unrelated board defaults.

Deliver the board path, inspected static and motion previews in scope, a concise account of the adopted style and adaptations, and the board's actual approval state. Episode work, generated audio, publishing configuration, external publication, and Git commits require their own requests.
