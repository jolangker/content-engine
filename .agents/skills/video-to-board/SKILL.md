---
name: video-to-board
description: Turn supplied reference videos into a new creative board that closely follows their visual, storytelling, motion, and audio style. Align the user's direction and obtain approval before creating the board. Use for video-derived boards, not episode recreation or board-export handoffs.
---

# Video to Board

Translate a reference video's creative grammar into a reusable board. Follow the reference style and apply the user's stated changes. This skill owns board synthesis and the single approval gate before creation. [shortform-board](../shortform-board/SKILL.md) owns the board package and technical verification.

## Establish the reference

Read project instructions, `TRACKER.json`, and shortform-board. Discussion stays in conversation. Identify the supplied video files or URLs and any user direction already given. Request a missing or inaccessible reference before claiming an analysis. A bare invocation does not select an existing board or start production.

Load [rea-video](../rea-video/SKILL.md) to decompose and review each supplied clip. Follow [video analysis](references/video-analysis.md) to turn the reviewed output into timestamped board evidence and document coverage and uncertainty. Keep downloaded media and analysis outputs in temporary storage outside `boards/`. Before approval, keep the proposal and its revisions in conversation and defer board files and tracker changes until the build step.

Aim for a faithful reading of the supplied style rather than a menu of new creative directions. Distinguish observed evidence, interpretation, and proposed implementation choices. Preserve the reference's recognizable composition, narrative delivery, pacing, motion, and audio relationships where the user has not requested changes. Treat episode subject matter as evidence of that episode, not proof of the account's entire niche.

## Align the vision at one approval gate

After analysis, present a concrete proposal in natural Indonesian with:

- A concise reading of the reference, supported by representative timestamps and any important access limits.
- What the board will retain, what will change under the user's direction, and uncertain details requiring a proposed substitute.
- The intended audience experience, proposed content scope, and reusable storytelling, visual, motion, and audio rules.
- A concrete description of how a different topic would look and unfold under those rules. Label the example as illustrative.

State material assumptions as proposals. Resolve ambiguity that changes the outcome here, including conflicts between the user's direction and the reference. Missing content scope can be proposed here; it need not trigger a separate intake gate.

Whenever the user supplies direction or corrections, synthesize the reference and **all current user direction** into an updated vision. Explain retained traits, intentional changes, and the resulting experience through a concrete example. Check this synthesis with the user before creating anything. Acknowledge-only replies such as "understood" do not establish alignment.

The gate may contain several discussion turns, but it remains one gate. Corrections, a new preference, a broad request to make a board, or silence are not approval of an unseen or revised vision. Proceed only when the user explicitly authorizes creation against the latest presented synthesis. A brief "gas" or "lanjut" can authorize that synthesis when its referent is clear. If a reply combines approval with a material new direction, present the updated synthesis and wait for confirmation; do not silently treat the addition as an approved design.

End the gate response with one concise question that asks whether the summarized vision matches and the board can be created. Explain that this checkpoint comes from the user's requested workflow in this [skill](SKILL.md). Do not create a second gate solely to ask the same permission again. On continuation, use the conversation's latest proposal and response; if their scope cannot be recovered, re-establish it before board creation.

**Gate exit:** the latest synthesis is visible, material conflicts are resolved, and the user has explicitly confirmed that vision and authorized creation. Later material changes before creation return to this same gate. After creation starts, follow requested revision scope and ask only for unresolved information that is necessary to proceed.

## Build the approved direction

After the gate exits, follow shortform-board's [board files and state](../shortform-board/references/board-files.md), look/spec guidance, and visual verification. Carry the approved synthesis forward as the brief. For this route, complete the full requested draft without shortform-board's intermediate visual or editorial approval pauses; retain its technical and creative checks. The user may still give feedback or explicitly request a pause.

Create the board at its collision-checked registered path, using the existing board package format rather than inventing another schema. Record the approved direction, approval scope, reference provenance, and deliberate adaptations in `DIRECTION.md`. Save the timestamped evidence and coverage limits in board-local `references/ANALYSIS.md`, with selected supporting frames when useful. Link the analysis from `DIRECTION.md`; preserve usable assets and relative evidence links when moving temporary material.

Translate observations into actionable reusable rules in `frame.md` and `EDITORIAL.md`. Mark estimates and selected substitutes rather than presenting them as measured source facts. Show independent sample compositions using different illustrative material in the static style board. Describe motion and audio behavior even when the deliverable is static, making clear that they have not been demonstrated in a rendered video.

The approved direction authorizes building the package; it does not approve unseen board artifacts. Deliver the completed, inspected package as `draft`, with its completed scope and optional feedback recorded in `DIRECTION.md`. Do not block delivery on a second mandatory approval. Set `approved` only if the user subsequently accepts the actual visual and editorial package, following shortform-board's state rules.

## Verify and deliver

Check fidelity against the approved synthesis and timestamped evidence, including user-requested departures. Verify that the visual source and preview agree, fonts load, text is readable, and sample compositions apply the style to different material. Check links, tracker parsing, and the registered board path. Report any remaining unknowns rather than filling them with unrelated board defaults.

Deliver the board path, inspected preview, a concise account of the adopted style and adaptations, and its actual approval state. This workflow creates no episode, animated demo, generated audio, publishing configuration, or external publication unless separately requested. Board creation is not a Git commit instruction.
