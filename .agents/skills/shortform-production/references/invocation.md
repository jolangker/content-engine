# Invocation options

These are arguments in a skill prompt, not an installed shell command or HyperFrames CLI flags. Parse them before intake, file creation, or media/API calls. Natural-language equivalents carry the same intent.

| Option | Meaning |
| --- | --- |
| `--board=<name>` | Select a board registered in `TRACKER.json`; prefer its exact slug. An exact, unique display name from the registered board's documents also resolves to that slug. |
| `--topic=auto` | Choose one new topic and angle from the resolved board using [automatic topic selection](topic-selection.md), then continue through the requested endpoint. |
| `--automation` | Delegate routine choices and run through the requested endpoint without human review checkpoints, including the pre-render gate. Retain technical and factual verification. |
| `--delivery=package` | Default: verified export plus content package; a narrower explicit endpoint such as script-only still applies. |
| `--delivery=draft` | Continue through Cloudinary hosting and a Buffer draft for each resolved target. |
| `--delivery=queue` | Continue through hosting and actual Buffer scheduling; use configured queue slots unless `--at` supplies a time. |
| `--delivery=publish` | Continue through hosting and immediate publication to each resolved target. |
| `--channel=<service:handle-or-buffer-id>` | Select a target, for example `instagram:eliansatya`, or use an exact Buffer channel ID. Repeat for multiple targets; resolve all IDs against the chosen organization. |
| `--at=<ISO-8601-with-offset>` | With `--delivery=queue`, schedule at this future time instead of using the queue. Example: `2026-11-02T19:00:00+07:00`. |

Organization selection can be supplied in ordinary language or reused from the production's verified account mapping. Quote option values containing spaces. `--automation` is the canonical spelling; do not introduce a second `--auto`/`--autonomous` mode with different behavior.

## Resolve once

1. Validate option names and values. An empty/unknown board, ambiguous name, contradictory duplicate option, a `--topic` value other than `auto`, unknown delivery value, or `--at` outside queue delivery is an input error. Resolve it before side effects; show valid choices. Explicit topic text stays in the ordinary prompt. A nonexistent board never silently falls back to another board.
2. Apply current explicit choices before saved production choices, then project defaults. `--board` on continuation is an explicit board change: preserve prior outputs, identify the dependencies it invalidates, and rebuild only those affected. `--automation` does not waive an invalid selector or authorize a new board's approval.
3. Resolve the topic from supplied material, a uniquely identified existing production, or explicit `--topic=auto` delegation. On a new production, `--topic=auto` resolves the board first and follows [automatic topic selection](topic-selection.md). A continuation retains its episode's topic even if the auto option is repeated. A supplied concrete topic/source takes priority over auto discovery. `--board` and `--automation` alone still do not delegate topic selection; without any topic/target/delegation, follow context-free intake, or report the missing target as blocked in automation.
4. Persist the resolved board, topic and angle, topic-selection provenance when delegated, execution policy, requested endpoint, delivery, target mapping, and schedule in `EPISODE.md`. These are production decisions, not extra root tracker fields. A resume keeps the recorded run policy and selected topic until the user changes them. Current scope, such as "revise the caption only", still limits the current turn; a saved publish endpoint is not a fresh instruction to repost.

`--automation` delegates board selection when no board was named: use the existing production's board on continuation; for a new production choose a suitable approved board and record the fit. With sufficient direct creative guidance, use `board: null`. If neither a board nor supplied direction supports the subject, record the blocker instead of fabricating a board. Routine creative details are inferred with reasons; missing credentials, ambiguous account identity, unsupported required platform fields, and failed quality checks remain blockers.

## Automation and review

For a fresh automated HyperFrames run, pass `flow: automation`, `storyboard: no`, and derived `mode: autonomous` through its normal brief contract. Keep an internal scene plan and verification evidence. For continuation, preserve settled flow/layout choices and set the current execution mode to autonomous; update `STORYBOARD.md` mode when present.

Also record this project-specific policy in `EPISODE.md` and `video/BRIEF.md` once that project exists:

```text
execution_policy: automation
human_review: none
pre_render_authorization: delegated by the user's --automation instruction
```

This policy deliberately overrides HyperFrames' retained human final-look question for this production. Run its quality checks, inspect the final look, open or expose the preview as appropriate, and continue to render without asking. Record the version as agent-verified under delegated authorization; keep human approval fields false/unset unless a human actually approved it. Reinterpret legacy instructions such as "use approved narration" as the final agent-verified narration for this run, not a reason to pause for approval.

Post concise progress and decision summaries as work continues. In automation, fix failed checks within scope and proceed when they pass. An unresolved dependency produces a concrete blocked result, not `awaiting_review`; preserve completed work. A final pending asynchronous publication is `in_progress`, not a fabricated blocker or success.

Without `--automation` or a recorded equivalent, project review defaults apply. A later explicit request to review together restores human checkpoints. If a single request simultaneously requires automation and a human gate, resolve that contradiction before dependent actions.

## Delivery scope

`--automation` changes interaction, not the endpoint. `--delivery=draft|queue|publish` explicitly authorizes hosting the final asset publicly on Cloudinary and the selected Buffer action. Fulfill that selected action without another permission question once inputs and required production checks are resolved. A delivery option alone retains earlier production review defaults; adding `--automation` removes those checkpoints too. Creating a draft adds no separate standing review gate unless requested.

For external delivery, resolve exact target channels from `--channel`, an explicit user statement, or a verified production/board mapping. A sole connected channel is not a default identity for every board. Preserve known declarations; infer only routine editorial settings. Follow [publishing](publishing.md) for preflight, receipts, and completion.

An explicit narrower endpoint wins over the default package endpoint. A script-only endpoint combined with an external delivery option is contradictory and must be resolved before work. Skill-authoring requests and examples in this guide do not execute any of these deliveries.

## Examples

```text
$shortform-production --board=ruang-di-antara --topic=auto --automation --delivery=publish --channel=instagram:eliansatya
```

Select one non-duplicate topic from the board, research and produce it, then host and publish to the verified channel without review pauses. If a verified board/account mapping already supplies the target, `--channel` can be omitted. This example does not establish a permanent mapping.

```text
$shortform-production topik: limerence --board=ruang-di-antara --automation
```

New production through the content package, with no review pauses. Inspect existing topics for overlap before creating a new production.

```text
$shortform-production lanjut limerence --automation --delivery=draft --channel=instagram:eliansatya
```

Reuse valid existing artifacts, host the verified MP4, and create or reconcile the requested Instagram draft.

```text
$shortform-production topik: confirmation bias --board=berkas-polemik --automation --delivery=queue --channel=instagram:ACCOUNT --at=2026-11-02T19:00:00+07:00
```

Run through scheduling without a review gate once the real target replaces `ACCOUNT` and its identity is verified. Dates and account names here illustrate syntax, not standing production choices.
