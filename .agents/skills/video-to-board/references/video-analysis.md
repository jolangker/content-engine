# Video analysis

Use reviewed [rea-video](../../rea-video/SKILL.md) findings to propose reusable style rules and show uncertainty at the board approval gate.

## Decompose and review the source

1. Prefer the supplied original file. For URLs, follow project research guidance to access the playable video, then stage the media in temporary storage for `rea-video`. Use a separate temporary output directory for each clip.
2. Follow `rea-video`'s analysis and review workflow with the installed CLI. Check `rea-video --help` for available commands. Use `survey` when the CLI supports it and the skill calls for it, then run `decompose` and `summary`. Use `--no-vlm` for local analysis and the configured VLM workflow when requested. Use `--lang en` for Indonesian requests and synthesize the findings in Indonesian.
3. Follow `rea-video`'s visual and audio review guidance. Inspect the storyboard, representative shots, and motion around important cuts, reveals, and transitions. Listen to the available audio and compare narration, music, and sound cues with the visual sequence. When visual review is available, merge reviewed findings using `review` and `apply-review`. Treat uncertain classifications and unverified detections as provisional.
4. Start with the reviewed `VIDEO.md` and use its map to find available evidence for timing, story, packaging, and sound. Fill evidence gaps from the source clip and record what remains uncertain. The user-facing response follows `video-to-board`'s proposal and approval step. Treat any automatically generated remake material as scratch output.

## Record coverage

Record the source file or URL, analyzed duration or range, aspect ratio, audio availability, and methods actually used. Inspect the full clip's progression where practical. For a long reference, agree on a representative range if full coverage is impractical. Review each clip before identifying shared traits and variations.

If the CLI or its analysis output is unavailable, use direct inspection as the fallback for this workflow and record which evidence it supplied. If important visuals or audio remain inaccessible, resolve access or agree on reduced coverage at the same vision gate. Use contact sheets for composition, frame sequences or playback for motion, transcripts for wording and structure, and audible tracks for delivery and sound cues.

## Read the creative grammar

Capture evidence where it changes a reusable board decision:

| Layer | Look for |
| --- | --- |
| Storytelling | Hook mechanism, viewpoint, information order, explanation depth, reveals, ending, relationship between words and images. |
| Composition | Subject scale, hierarchy, negative space, framing, recurring arrangements, caption placement, screen format. |
| Visual language | Media type, illustration dimensionality, lighting, texture, shape vocabulary, palette roles, typography roles and relative scale. |
| Motion and editing | Shot/hold lengths, cuts, transitions, camera versus object motion, text timing, acceleration, recurring motion used to explain meaning. |
| Audio | Language, delivery, pauses, music character and changes, SFX purpose, relative prominence, synchronization with visual events. |

Use timestamps or ranges relative to the analyzed clip. A compact evidence table can contain `time/range`, `observation`, `reusable rule`, and `certainty/limit`. Distinguish source measurements from interpretations and adaptation choices. Exact font names, color tokens, easing curves, source software, music identity, and creator intent remain uncertain without sufficient evidence. Derive implementable tokens with a stated rationale rather than claiming guessed values were recovered exactly.

Capture a small set of identity-defining traits, flexible patterns, and episode-specific choices. A faithful board should explain how to reproduce the experience on new subjects: for example, what triggers a cutaway, when a label appears, and what the viewer must understand before a reveal. Avoid reducing the reference to a palette and font list. Keep reference content and branding distinct from reusable style; use new illustrative copy and subject matter in board studies unless the user explicitly requests reuse.

## Carry evidence into the board

Before approval, keep analysis in conversation and scratch files in temporary storage. After approval, preserve the useful evidence in the new board's `references/ANALYSIS.md`: source provenance, actual coverage, timestamped findings, stable traits, variations, uncertainty, and the reasoning behind selected substitutes or user-directed departures. Include selected frames with source timestamps where they materially support the decisions; do not require a full copied video to understand the board.

Treat factual claims inside the reference as source content, not independently verified facts. Mark sample copy as illustrative and follow the project's research rules if making factual claims. Reference analysis does not authorize copying operational account identities or configuring publishing targets.
