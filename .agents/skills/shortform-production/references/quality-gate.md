# Quality gate

Read at brief to snapshot the contract, at storyboard, verification and export to gate the work, and before presenting a final preview. A script holds every production to its contract; review supplies the judgement a script cannot.

## Snapshot the contract at brief

Copy the selected board's `CONTRACT.json` to `productions/<slug>/CONTRACT.json` and record its board revision and SHA-256 in `EPISODE.md`. Add the brief's own measurable targets to the snapshot: a duration range the user asked for, the caption region this episode uses. For `board: null`, write the snapshot from the brief with `schema_version: 1`. [Board files](../../shortform-board/references/board-files.md#production-contract) define the fields. Validate it and print the effective rules, standing judged rules included:

```bash
python .agents/skills/shortform-production/scripts/episode_qa.py --contract productions/<slug>
```

A continuation keeps its snapshot. A production that predates contracts takes one when it next enters storyboard, verification or export, limited to the rules of the board revision it recorded.

### Production defaults

An unset field inherits these starting values, tuned on this project's existing episodes:

| Field | Default | What it holds |
| --- | --- | --- |
| `hook.first_sentence_max_seconds` | 5.0 | The first spoken sentence has ended. |
| `hook.first_motion_max_seconds` | 1.0 | The picture has changed outside the caption region. |
| `motion.max_static_seconds` | 5.0 | Longest stretch a scene holds still outside the caption region, and the longest planned gap between storyboard reads; the film's last 3 seconds are exempt. |
| `motion.min_active_area` | 0.01 | Share of the unmasked frame that changes during each scene, and between a frame's first and last storyboard pose. |
| `motion.max_empty_frame_run` | 3 | Consecutive blank/flat frames (`std < 1.5`, `range < 8` outside captions; Gate G2). |
| `motion.max_end_hold_seconds` | 3.5 | Maximum trailing static end-card hold after motion ends (Gate G3). |
| `storyboard.max_same_shot_run` | 2 | Consecutive storyboard frames that share one `shot` label. |
| `audio.loudness_lufs` | −15 to −13 | Integrated loudness of the export. |
| `audio.true_peak_max_dbtp` | −0.5 | True peak of the export. |
| `craft.dom_lint` | false | Require headless Playwright DOM anti-slop (Gate G5) and on-screen text read-time (`readcheck`) receipt `verification/dom-lint.json`. |
| `craft.rubric_min_score` | null | Minimum 1–10 score across all 7 independent jury dimensions (`7.0` floor when a rubric block is present). |
| `craft.require_wow_fix` | false | Require a concrete `wow_upgrade` entry in `REVIEW.md`. |

Duration, scene count, word limits, audio roles and the hook turn are enforced where the contract sets them. Change a default in `episode_qa.py` together with its tests, then run `python -m unittest discover -s .agents/skills/shortform-production/scripts -p "test_*.py"`; it encodes small synthetic films locally and makes no API calls.

## Review the film

1. **Author pass & DOM lint.** Run HyperFrames' checks, its [review](../../hyperframes/references/review.md), and `python .agents/skills/shortform-production/scripts/dom_lint.py --production productions/<slug>` on the assembled composition. Fix any Gate G5 anti-slop hits (corner/edge micro-labels, tracked-caps kickers, `01 / 05` counters, BPM/FPS metadata, slide-deck left-headline + right-card layouts, letter-typed headlines, vibe-coded UI cards, or non-board chrome pinned across 3+ scenes) and any `readcheck` failures (non-caption text cut before `0.5s + 0.28s × words`, or `0.4s` for 1–2 word labels).
2. **Independent pass (7-dimension jury rubric).** A reviewer other than the author reviews the same version before the delivery render. Give a fresh-context reviewer only the effective judged rules, `SCRIPT.md`, `STORYBOARD.md` and the review sheets. Ask for:
   - A `pass` or `fail` with observable frame/time evidence for every judged rule.
   - Harsh 1–10 scores (`5` = student, `7` = solid pro, `8` = agency, `9+` = award shortlist; target `>= 7` on all seven) with concrete evidence across all 7 jury dimensions: `style_fidelity`, `concept_wow`, `motion_craft`, `design_typography`, `finish_texture`, `sound_sync`, and `technical`.
   - Ranked P0 and P1 notes in HyperFrames' note format, the `weakest_shot`, and at least one concrete `wow_upgrade` fix when any dimension scores `< 8`.
   The reviewer reads and reports; the author makes the fixes. Take the first route available and record it:

   | `independent_review` | Route |
   | --- | --- |
   | `subagent` | The host's own sub-agent. |
   | `worker` | An Orca worker through the `orchestration` skill. |
   | `human` | The user reviewed this version at the final-preview checkpoint; the approval is recorded in `EPISODE.md`. |
   | `unavailable` | No agent route exists and no human has reviewed this version yet. |

3. **Listen.** Review the narration take and the mix under [audio generation](audio.md#listen-to-the-take-and-the-mix) and record who heard it.
4. **Record.** Write `video/REVIEW.md` as HyperFrames' delivery note and include this block:

   ```markdown
   ## Gate record

   composition_sha256: <printed by episode_qa.py --production productions/<slug> --digest>
   independent_review: subagent
   listening: worker
   weakest_shot: s07, the collected larvae are small at yard scale
   wow_upgrade: s05, replace static cut with carried water-level push into the siphon chamber (0.35s expo.out)

   - rubric.style_fidelity: 8/10 — layered yard palette, DM Sans 800 outline captions, consistent cutaway seam
   - rubric.concept_wow: 8/10 — immediate scoop comparison in frame 0 and clear self-harvest ramp payoff
   - rubric.motion_craft: 7.5/10 — expo.out arrivals and 0ms stagnant cuts; s07 inset synchronized with backing
   - rubric.design_typography: 8/10 — 68px caption clearance, legible labels at 360px phone width
   - rubric.finish_texture: 7.5/10 — soil strata flecks and clean vector silhouettes without banding
   - rubric.sound_sync: 8/10 — all 3 contact cues within 0.4ms, quiet scene seams below -65 dBFS
   - rubric.technical: 8.5/10 — 1080x1920@30fps, zero lint/DOM-slop/readcheck errors

   - [pass] hook-frame: frame 0 shows the hand on the empty pot under the line "Kalau kamu…"
   - [fail] motion-variety: s02 to s09 share one wide framing
   - P1 · t=41.7s · s04 inset · roots unreadable at 360 px → enlarge inset to 40% width · fixed
   ```

   Give one verdict line for every effective judged rule, each with evidence that names a frame, time or line. When recording jury rubric lines, score all seven dimensions with specific evidence (`episode_qa.py` enforces completeness and the score floor). Use the independent reviewer's verdicts where one ran. Mark every finding `fixed` or `open`. An edit after review changes the composition hash: review what changed and update the record.

## Run the gate

From the project root, once per stage (add `--dom-lint` at `verification` to run and bind `verification/dom-lint.json` in one pass):

```bash
python .agents/skills/shortform-production/scripts/episode_qa.py --production productions/<slug> --stage storyboard
python .agents/skills/shortform-production/scripts/episode_qa.py --production productions/<slug> --stage verification --dom-lint
python .agents/skills/shortform-production/scripts/episode_qa.py --production productions/<slug> --stage export --film productions/<slug>/exports/<file>.mp4
```

- **`storyboard`** reads the plan under [visual storyboard](storyboard.md#plan-change-over-time): planned duration and frame count against the contract, shot variety, the cadence of timed reads, the hook and long-frame poses, and the board artifacts.
- **`verification`** measures a draft proof. Render it from the video project with `npx hyperframes render --quality draft --output verification/proof.mp4`; a proof is verification evidence, and the delivery render keeps its own authorization. The gate checks that every mounted scene animates or plays footage, the contract's duration, scene count, word and audio-role limits, the first sentence and turn timing, the review record against the current composition, a passing verdict for every judged rule, and that no P0 is open. On the film it measures format, motion in each scene with the caption region masked, and the first picture change.
- **`export`** repeats the verification checks on the delivered file and adds its loudness.

Each run writes `video/verification/quality-gate-<stage>.json`; record the status and path in `EPISODE.md`.

| Exit | Status | Next |
| --- | --- | --- |
| 0 | `passed` | The stage's gate criterion is met. |
| 1 | `failed` | Fix the cause, review what changed, run it again. |
| 2 | `needs_human_review` | Only at `verification` with `independent_review: unavailable`. Present the final preview to the user, under active automation too, with `awaiting_review`. After acceptance record `independent_review: human` and continue. |

A failing check stands until its cause is fixed or the user accepts it. Record an accepted exception in the snapshot's `overrides` with the `check` id, a `reason` quoting the decision, and `authority: user` (or `board` where the board's documents grant it). The verdict lists it under `disclose`, together with `listening: unavailable`.

The motion measurement is a floor: it catches frozen scenes, and the judged rules decide whether the motion explains anything.

## Disclose at checkpoints

When presenting a final preview or delivering an endpoint at preview or later, lead with the gate status, the weakest shot, every `disclose` entry and every judged rule marked fail, then the links. An approval covers what was disclosed.
