# Video analysis

Use reviewed [rea-video](../../rea-video/SKILL.md) findings to propose reusable style rules and show uncertainty at the board approval gate.

## Discover clips and choose output paths

- For a supplied local folder, find the playable video files in it and its subfolders. Skip `_analysis/` trees during discovery. Use `<reference-folder>/_analysis/` as the output root. For individually supplied local files, use `_analysis/` in each file's parent folder and analyze the selected files.
- Give each clip its own output directory under `_analysis/` using its path relative to the reference folder, including the filename extension. For example, write the output for `references/jadiginisodara/clip.mp4` to `references/jadiginisodara/_analysis/clip.mp4/`. Use that directory for `decompose -o`, the optional `survey -o`, and subsequent review commands. Keep `VIDEO.md`, the `video/` handoff, reports, and supporting files together there.
- For URL-only references, follow project research guidance to fetch the playable source and use a temporary per-clip directory when the user supplies no local reference folder or output path.

## Decompose and review the source

1. Follow `rea-video`'s analysis and review workflow with the installed CLI. Check `rea-video --help` for available commands. Use `survey` when the CLI supports it and the skill calls for it, then run `decompose` and `summary`. Use `--no-vlm` for local analysis and the configured VLM workflow when requested. Use `--lang en` for Indonesian requests and synthesize the findings in Indonesian.
2. Follow `rea-video`'s visual and audio review guidance. Inspect the storyboard, representative shots, and motion around important cuts, reveals, and transitions. When visual review is available, merge reviewed findings using `review` and `apply-review`. For clips with audio, follow the [native audio review priorities](#native-audio-review) and compare available audio timestamps with the visual sequence. Treat uncertain classifications and unverified detections as provisional.
3. Start with the reviewed `VIDEO.md` and use its map to find available evidence for timing, story, packaging, and sound. Fill evidence gaps from the source clip and record what remains uncertain. The user-facing response follows `video-to-board`'s proposal and approval step. Treat any automatically generated remake material as scratch output.

### Native audio review

Use the first applicable route:

1. **Main agent.** If the current session can receive native audio input, analyze the source audio directly.
2. **Antigravity.** If the main agent lacks native audio input and Orca Orchestration is available, load the `orchestration` skill and follow its version-matched guide. Start a worker in the shared workspace with `orchestration worker-start --worktree current --agent antigravity`. Give it a self-contained, read-only task with the absolute source paths, review ranges, and evidence requirements below. Ask it to report any native input limitation. Collect the result through the Orca worker lifecycle before synthesizing the proposal.
3. **No native review.** If the main agent lacks native audio input and Orca Orchestration is unavailable, skip native review. Use available `rea-video` measurements and transcripts as evidence for the claims they support. Use the same evidence if the Antigravity worker cannot ingest the audio.

For either native route, use the source clip when the session can ingest its audio, or use the original mix as an audio file such as `rea-video`'s `stems/original.wav`. Keep timestamps relative to the source clip. Record the file, input method, and range directly heard, with timestamped audible evidence and uncertainty for observations on delivery, emphasis, pauses, music character and changes, sound effects, and relative prominence. Document the evidence used and any gaps under [record coverage](#record-coverage).

## Record coverage

Record the source file or URL, analyzed duration or range, aspect ratio, audio availability, and methods actually used. Inspect the full clip's progression where practical. For a long reference, agree on a representative range if full coverage is impractical. Review each clip before identifying shared traits and variations.

If the CLI or its analysis output is unavailable, use direct inspection for visuals and follow the same native audio review priorities. If important visuals or audio remain inaccessible, resolve access or agree on reduced coverage at the same vision gate. Use contact sheets for composition, frame sequences or playback for motion, transcripts for wording and structure, and native audio observations for delivery and sound cues.

## Measure each clip

Numbers keep the board at the reference's pace. Record one row per clip in `_analysis/ANALYSIS.md`:

| Measure | Source |
| --- | --- |
| Duration, shot count, average shot length | `summary` in the clip's `breakdown.json` from `rea-video`. |
| First picture change, longest held stretch, held share, loudness | `python .agents/skills/shortform-production/scripts/episode_qa.py --fingerprint <clip> --caption-region <x,y,width,height>`. Give the burned-in caption region in the clip's pixels so caption changes stay out of the motion numbers. |
| Motion heatmap, cut beat-grid fit, ground/accent palette, percussive onsets & stem ducking | `python .agents/skills/video-to-board/scripts/clone_measure.py --video <clip> --out <clip-analysis-dir>/clone_metrics --caption-region <x,y,width,height> [--stems-dir <clip-analysis-dir>/stems]`. Produces `clone_metrics.json` and `motion_heatmap.jpg`. |
| Spoken words, exact words per second & hook-turn timestamp | `stems/vocals.wav` aligned via `align_narration.py` (or `faster-whisper` word timestamps) when `rea-video` speech lines are `timing: estimated`. |
| Closest open-licensed font match (x-height, stem weight, width & tracking) | `python .agents/skills/video-to-board/scripts/font_match.py --crop <frame.png> --box <x0,y0,x1,y1> --text "<exact visible line>" --json <clip-analysis-dir>/font_match.json`. |
| When the first spoken sentence ends, and when the first turn, problem or reveal lands | Transcript and captions, checked against the frames. |
| How many times the format's unit repeats (problem and fix, question and answer, step) | The beat map below. |
| Music and effects: heard, measured only, or absent | The native audio review, `clone_measure.py` (`stems_ducking` & `cuts_near_onset_share`), and the stems. |

Mark a number the tools could not produce as unmeasured.

## Map the beats

For each clip write a beat map: one row per story beat with its time range, what is said (paraphrased), what the picture does, and the beat's job in the story (hook, first version, turn, fix, payoff, closing line). Rows that recur across clips are the board's story shape; rows that appear once are that episode's choices. Keep the maps in `_analysis/ANALYSIS.md`.

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

Before approval, write `_analysis/ANALYSIS.md` for each local reference folder. List the source clips, link their per-clip `VIDEO.md` files when available, and include the per-clip measures, the beat maps, timestamped findings, recurring traits, and variations. Keep the proposal in conversation.

After approval, write the evidence relevant to the new board in its `references/ANALYSIS.md`. Include source provenance, coverage, timestamped findings, uncertainty, and the reasoning behind selected substitutes or user-directed departures. Copy selected frames with source timestamps where they materially support the decisions.

Treat factual claims inside the reference as source content, not independently verified facts. Mark sample copy as illustrative and follow the project's research rules if making factual claims. Reference analysis does not authorize copying operational account identities or configuring publishing targets.
