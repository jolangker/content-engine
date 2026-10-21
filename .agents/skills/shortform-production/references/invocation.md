# Invocation options

These are arguments in a skill prompt, not an installed shell command or HyperFrames CLI flags. Parse them before intake, file creation, or media/API calls. Natural-language equivalents carry the same intent.

| Option | Meaning |
| --- | --- |
| `--board=<name>` | Select a board registered in `TRACKER.json`; prefer its exact slug. An exact, unique display name from the registered board's documents also resolves to that slug. |
| `--topic=auto` | Present 10 topics with short briefs and a recommended pick using [topic discovery and selection](topic-selection.md), choose one under delegated authorization, then continue through the requested endpoint. |
| `--automation` | Delegate routine choices and run through the requested endpoint without human review checkpoints, including the pre-render gate. Retain technical and factual verification. |
| `--until=<stage>` | Finish at the selected pipeline stage, including that stage's deliverable and verification. Controls scope independently of automation and review; see Stage endpoint below. |
| `--delivery=package` | Default: verified export plus content package; a narrower explicit endpoint such as script-only still applies. |
| `--delivery=draft` | Continue through Cloudinary hosting and a Buffer draft for each resolved target. |
| `--delivery=queue` | Continue through hosting and actual Buffer scheduling; use configured queue slots unless `--at` supplies a time. |
| `--delivery=publish` | Continue through hosting and immediate publication to each resolved target. |
| `--channel=<service:handle-or-buffer-id>` | Select a target, for example `instagram:eliansatya`, or use an exact Buffer channel ID. Repeat for multiple targets; resolve all IDs against the chosen organization. |
| `--at=<ISO-8601-with-offset>` | With `--delivery=queue`, schedule at this future time instead of using the queue. Example: `2026-11-02T19:00:00+07:00`. |

Organization selection can be supplied in ordinary language or reused from the production's verified account mapping. Quote option values containing spaces. `--automation` is the canonical spelling; do not introduce a second `--auto`/`--autonomous` mode with different behavior.

## Resolve once

1. Validate option names and values. An empty/unknown board, ambiguous name, contradictory duplicate option, a `--topic` value other than `auto`, empty/unknown stage, conflicting stage/delivery endpoints, unknown delivery value, or `--at` outside queue delivery is an input error. Resolve it before side effects; show valid choices. Explicit topic text stays in the ordinary prompt. A nonexistent board never silently falls back to another board.
2. Apply current explicit choices before saved production choices, then project defaults. `--board` on continuation is an explicit board change: preserve prior outputs, identify the dependencies it invalidates, and rebuild only those affected. `--automation` does not waive an invalid selector or authorize a new board's approval.
3. Resolve the topic from supplied material, a uniquely identified existing production, or explicit `--topic=auto`/equivalent selection delegation. Requests to find topics, such as "carikan topik", follow [topic discovery and selection](topic-selection.md) and wait for the user's pick unless selection is explicitly delegated. On a new production, `--topic=auto` resolves the board first and follows that reference. A continuation retains its episode's topic even if the auto option is repeated. A supplied concrete topic/source takes priority over auto discovery. `--board` and `--automation` alone still do not delegate topic selection; without any topic/target/discovery request/delegation, follow context-free intake, or report the missing target as blocked in automation.
4. Persist the resolved board, topic and angle, topic-selection provenance when delegated, execution policy, requested endpoint (including `until` when selected), delivery, target mapping, and schedule in `EPISODE.md`. Reflect the endpoint in `video/BRIEF.md` once that project exists. These are production decisions, not extra root tracker fields. A resume keeps the recorded run policy, endpoint, and selected topic until the user changes them. Current scope, such as "revise the caption only", still limits the current turn; a saved publish endpoint is not a fresh instruction to repost.

`--automation` delegates board selection when no board was named: use the existing production's board on continuation; for a new production choose a suitable approved board and record the fit. With sufficient direct creative guidance, use `board: null`. If neither a board nor supplied direction supports the subject, record the blocker instead of fabricating a board. Routine creative details are inferred with reasons; missing credentials, ambiguous account identity, unsupported required platform fields, and failed quality checks remain blockers.

## Stage endpoint

Accept these exact `--until` values in pipeline order: `brief`, `research`, `script`, `storyboard`, `audio`, `production`, `verification`, `preview`, `export`, `content_package`, `publishing`. Natural-language endpoints such as "stop after the script" resolve to the corresponding stage. Resolve contradictory explicit endpoints before work; an explicit stage that does not apply to the format, such as audio for a silent video, needs a scope correction rather than silently advancing to another stage.

- Without `--until` or a narrower natural-language endpoint, finish at `content_package`, or at `publishing` for explicitly selected external delivery. Review checkpoints still apply unless `--automation` or a recorded equivalent delegates them.
- With `--until`, complete only the dependencies through that stage. The cap takes precedence over implicit or explicit `--delivery=package`; `--delivery=draft|queue|publish` conflicts with any cap before `publishing`. `--until=publishing` requires an explicit external-delivery action; it does not choose or authorize one. Resolve these conflicts before file creation, synthesis, uploads, or other side effects.
- `--until` alone delegates neither routine choices nor human review. Intermediate checkpoints remain in force. At the final stage, a required review uses `awaiting_review`; acceptance completes that endpoint and stops. With `--automation`, verify the endpoint, record `stage: <stage>`, `status: complete`, deliver it, and stop without asking for review. Earlier-stage endpoints still receive the checks relevant to their artifacts.
- `--until=storyboard` requests the complete [visual storyboard](storyboard.md), including `video/boards/storyboard.png`, with verification. The same artifacts are required when a new production passes through storyboard toward a later endpoint. Estimate timings and update them only if later audio work is requested.
- Enforce the cap at every handoff: storyboard stops before audio synthesis and animation; audio stops before animated assembly; preview stops before the final delivery export. Create only artifacts and run only operations needed for the endpoint, including its own verification. Publishing preflight is needed only when external delivery is in scope.
- Resume interrupted work with its saved cap. Completed bounded work stays complete until the user requests a later endpoint or explicitly asks to continue beyond it; resolve that new endpoint before downstream work. Reuse valid later artifacts in an existing production without deleting them, regressing its recorded progress, or re-executing downstream delivery merely to satisfy an earlier cap.

## Automation and review

For a fresh automated HyperFrames run, pass `flow: automation`, `storyboard: no`, and derived `mode: autonomous` through its normal brief contract. In this pipeline, `storyboard: no` disables the human checkpoint while the [visual storyboard](storyboard.md) artifacts remain required, including the PNG, whenever the endpoint reaches that stage. Explicitly carry this override into the HyperFrames brief and handoff: perform the static sketch/board pass, verify it as the agent, and continue without a human pause. This replaces the owning workflow's instruction to skip sketches in autonomous mode. For continuation, preserve settled flow/layout choices and set the current execution mode to autonomous; update `STORYBOARD.md` mode when present. Initialize HyperFrames only when the selected endpoint needs it.

Also record this project-specific policy in `EPISODE.md` and `video/BRIEF.md` once that project exists:

```text
execution_policy: automation
human_review: none
pre_render_authorization: delegated by the user's --automation instruction
```

When storyboard is in scope, also record that its artifacts are required under [visual storyboard](storyboard.md) and that agent verification replaces the human layout checkpoint. Keep this as production-specific guidance alongside the normal HyperFrames fields; `storyboard: yes` would derive collaborative mode and is not the automation fix.

This policy deliberately overrides HyperFrames' retained human final-look question for this production within the resolved endpoint. Run the checks relevant to that endpoint. When it includes preview, inspect and open or expose the final look; continue to the delivery render without asking only when export is in scope. Record the version as agent-verified under delegated authorization; keep human approval fields false/unset unless a human actually approved it. Reinterpret legacy instructions such as "use approved narration" as the final agent-verified narration for this run, not a reason to pause for approval.

Post concise progress and decision summaries as work continues. In automation, fix failed checks within scope and proceed when they pass. An unresolved dependency produces a concrete blocked result, not `awaiting_review`; preserve completed work. A final pending asynchronous publication is `in_progress`, not a fabricated blocker or success.

Without `--automation` or a recorded equivalent, project review defaults apply. A later explicit request to review together restores human checkpoints. If a single request simultaneously requires automation and a human gate, resolve that contradiction before dependent actions.

The pre-script hook checkpoint follows [research and script](research.md): present 3 hooks after research and wait for selection by default. Automation delegates that choice while retaining the visible options and recorded rationale. `--topic=auto` alone delegates only the topic choice and retains the hook checkpoint.

## Delivery scope

`--automation` changes interaction, not the endpoint. `--delivery=draft|queue|publish` explicitly authorizes hosting the final asset publicly on Cloudinary and the selected Buffer action. Fulfill that selected action without another permission question once inputs and required production checks are resolved. A delivery option alone retains earlier production review defaults; adding `--automation` removes those checkpoints too. Creating a draft adds no separate standing review gate unless requested.

For external delivery, resolve exact target channels from `--channel`, an explicit user statement, or a verified production/board mapping. A sole connected channel is not a default identity for every board. Preserve known declarations; infer only routine editorial settings. Follow [publishing](publishing.md) for preflight, receipts, and completion.

The Stage endpoint contract resolves narrower endpoints and delivery conflicts. Skill-authoring requests and examples in this guide do not execute any of these deliveries.

## Examples

```text
$shortform-production topik: confirmation bias --board=berkas-polemik --automation --until=script
```

Research, present 3 hooks and select one under automation, then write and verify the script. Deliver `SCRIPT.md` and finish at `script: complete` without review pauses or downstream video work.

```text
$shortform-production --board=ruang-di-antara --topic=auto --automation --until=storyboard
```

Present 10 topics with short briefs and a recommendation, select one under delegation, research it, and present/select one of 3 hooks under automation. Produce its script and complete visual storyboard, including `video/boards/storyboard.png`, without human checkpoints. Verify and deliver the storyboard, then stop before audio synthesis or animation.

```text
$shortform-production topik: confirmation bias --board=berkas-polemik --until=storyboard
```

After research, present 3 hooks and wait for the user's selection before drafting. Keep the normal script and visual-storyboard review checkpoints. Once the storyboard is accepted, finish there rather than proceeding to audio.

```text
$shortform-production lanjut jeda-yang-kembali --automation --until=preview
```

Reuse valid artifacts and verify the composition preview without review pauses. Stop before a new delivery export; preserve existing exports.

```text
$shortform-production --board=ruang-di-antara --topic=auto --automation --delivery=publish --channel=instagram:eliansatya
```

Select one non-duplicate topic from the board, research and produce it, then host and publish to the verified channel without review pauses. If a verified board/account mapping already supplies the target, `--channel` can be omitted. This example does not establish a permanent mapping.

```text
$shortform-production topik: limerence --board=ruang-di-antara --automation
```

New production through the content package, with no review pauses. Create and agent-verify the complete visual storyboard, including `storyboard.png`, before audio and animation. Inspect existing topics for overlap before creating a new production.

```text
$shortform-production lanjut limerence --automation --delivery=draft --channel=instagram:eliansatya
```

Reuse valid existing artifacts, host the verified MP4, and create or reconcile the requested Instagram draft.

```text
$shortform-production topik: confirmation bias --board=berkas-polemik --automation --delivery=queue --channel=instagram:ACCOUNT --at=2026-11-02T19:00:00+07:00
```

Run through scheduling without a review gate once the real target replaces `ACCOUNT` and its identity is verified. Dates and account names here illustrate syntax, not standing production choices.
