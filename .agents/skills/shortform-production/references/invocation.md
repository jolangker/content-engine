# Invocation options

These are arguments in a skill prompt, not an installed shell command or HyperFrames CLI flags. Parse them before intake, file creation, or media/API calls. Natural-language equivalents carry the same intent.

| Option | Meaning |
| --- | --- |
| `--board=<name>` | Select a board registered in `TRACKER.json`; prefer its exact slug. An exact, unique display name from the registered board's documents also resolves to that slug. |
| `--topic=auto` | Prepare a lightweight editorial shortlist of 10 topics using [topic discovery and selection](topic-selection.md), record the shortlist and delegated pick, summarize the selected topic, then research that topic and continue through the requested endpoint. |
| `--automation` | Delegate routine choices and run through the requested endpoint without human review checkpoints, including the pre-render gate. Retain technical and factual verification and the [quality gate](quality-gate.md) with its independent review. |
| `--automation=after-topic` | Keep human topic selection, then activate automation after the topic is accepted. |
| `--automation=after-hook` | Keep the normal topic and hook choices, then activate automation after the user selects the hook. |
| `--automation=after-script` | Keep normal checkpoints through human script approval, then activate automation. |
| `--automation=after-storyboard` | Keep normal checkpoints through human visual-storyboard approval, then activate automation. |
| `--until=<stage>` | Finish at the selected pipeline stage, including that stage's deliverable and verification. Controls scope independently of automation and review; see Stage endpoint below. |
| `--delivery=package` | Default: verified export plus content package; a narrower explicit endpoint such as script-only still applies. |
| `--delivery=draft` | Continue through media upload/reuse and a Trypost Local draft for each resolved target. |
| `--delivery=queue` | Continue through media upload/reuse and actual Trypost scheduling; use configured queue slots unless `--at` supplies a time. |
| `--delivery=publish` | Continue through media upload/reuse and immediate Trypost publication to each resolved target. |
| `--channel=<service:handle-or-account-id>` | Override board targets for this production, for example `instagram:dibalikbenda.id`, or use an exact Trypost social-account ID. Repeat for multiple targets; the combined explicit set replaces the inherited set. Without this option or another explicit target selection, use the saved production targets or every board account under target inheritance. |
| `--at=<ISO-8601-with-offset>` | With `--delivery=queue`, schedule at this future time instead of using the queue. Example: `2026-11-02T19:00:00+07:00`. |

Publishing uses Trypost Local. Persist the provider and workspace with the target mapping; use the matching MCP connection for that workspace. Historical delivery records follow [publishing](publishing.md#historical-receipts). Quote option values containing spaces. `--automation` is the canonical spelling; do not introduce a second `--auto`/`--autonomous` mode with different behavior.

## Resolve once

1. Validate option names and values. An empty/unknown board, ambiguous name, contradictory duplicate option, a `--topic` value other than `auto`, an empty/unknown automation value, empty/unknown stage, conflicting stage/delivery endpoints, unknown delivery value, or `--at` outside queue delivery is an input error. Accept only bare `--automation` and the four `after-*` values above; bare and delayed forms in one invocation are contradictory duplicates. Resolve errors before side effects; show valid choices. Explicit topic text stays in the ordinary prompt. A nonexistent board never silently falls back to another board.
2. Apply current explicit choices before saved production choices, then selected-board defaults and project defaults. Resolve publishing accounts under [target inheritance](publishing.md#target-inheritance). `--board` on continuation is an explicit board change: preserve prior outputs, identify the dependencies it invalidates, and rebuild only those affected. Retain saved delivery targets/attempts unless the user also changes targets; changing creative direction alone does not migrate posts. `--automation` does not waive an invalid selector or authorize a new board's approval.
3. Resolve the topic from supplied material, a uniquely identified existing production, or explicit `--topic=auto`/equivalent selection delegation. Requests to find topics, such as "carikan topik", follow [topic discovery and selection](topic-selection.md) and wait for the user's pick unless selection is explicitly delegated. On a new production, `--topic=auto` resolves the board first and follows that reference. A continuation retains its episode's topic even if the auto option is repeated. A supplied concrete topic/source takes priority over auto discovery. `--board` and automation options alone still do not delegate topic selection; without any topic/target/discovery request/delegation, follow context-free intake, or report the missing target as blocked when automation is already active.
4. Persist the resolved board, topic and angle, topic-selection provenance when delegated, execution policy (including delayed activation state and evidence below), requested endpoint (including `until` when selected), delivery, target mapping, and schedule in `EPISODE.md`. Reflect the endpoint and execution policy in `video/BRIEF.md` once that project exists. These are production decisions, not extra root tracker fields. A resume keeps the recorded run policy, endpoint, and selected topic until the user changes them. Current scope, such as "revise the caption only", still limits the current turn; a saved publish endpoint is not a fresh instruction to repost.

Active automation delegates board selection when no board was named: use the existing production's board on continuation; for a new production choose a suitable approved board and record the fit. Before delayed activation, use the normal board-choice rules unless the user separately delegates that choice. With sufficient direct creative guidance, use `board: null`. If neither a board nor supplied direction supports the subject, record the blocker instead of fabricating a board. In active automation, routine creative details are inferred with reasons; missing credentials, ambiguous account identity, unsupported required platform fields, and failed quality checks remain blockers.

## Stage endpoint

Accept these exact `--until` values in pipeline order: `brief`, `research`, `script`, `storyboard`, `audio`, `production`, `verification`, `preview`, `export`, `content_package`, `publishing`. Natural-language endpoints such as "stop after the script" resolve to the corresponding stage. Resolve contradictory explicit endpoints before work; an explicit stage that does not apply to the format, such as audio for a silent video, needs a scope correction rather than silently advancing to another stage.

- Without `--until` or a narrower natural-language endpoint, finish at `content_package`, or at `publishing` for explicitly selected external delivery. Review checkpoints still apply unless active automation or another explicit instruction delegates them.
- With `--until`, complete only the dependencies through that stage. The cap takes precedence over implicit or explicit `--delivery=package`; `--delivery=draft|queue|publish` conflicts with any cap before `publishing`. `--until=publishing` requires an explicit external-delivery action; it does not choose or authorize one. Resolve these conflicts before file creation, synthesis, uploads, or other side effects.
- `--until` alone delegates neither routine choices nor human review. Intermediate checkpoints remain in force. At the final stage, a required review uses `awaiting_review`; acceptance completes that endpoint and stops. With active automation, verify the endpoint, record `stage: <stage>`, `status: complete`, deliver it, and stop without asking for review. With delayed automation still pending, retain the applicable human checkpoints. A cap before activation is valid and ends there without advancing to activate automation; a cap at the activation stage stops after its human acceptance. Earlier-stage endpoints still receive the checks relevant to their artifacts.
- `--until=storyboard` requests the complete [visual storyboard](storyboard.md), including `video/boards/storyboard.png`, with verification. The same artifacts are required when a new production passes through storyboard toward a later endpoint. Estimate timings and update them only if later audio work is requested.
- Enforce the cap at every handoff: storyboard stops before audio synthesis and animation; audio stops before animated assembly; preview stops before the final delivery export. Create only artifacts and run only operations needed for the endpoint, including its own verification. Publishing preflight is needed only when external delivery is in scope.
- Resume interrupted work with its saved cap. Completed bounded work stays complete until the user requests a later endpoint or explicitly asks to continue beyond it; resolve that new endpoint before downstream work. Reuse valid later artifacts in an existing production without deleting them, regressing its recorded progress, or re-executing downstream delivery merely to satisfy an earlier cap.

## Automation and review

### Activation

Bare `--automation` is active immediately. A delayed value preserves the normal human checkpoints through its activation checkpoint, inclusive; it delegates later checkpoints only after that decision is accepted. Discovery still needs a request such as "carikan topik"; none of these flags alone supplies a topic or starts discovery.

| Value | Activation evidence | First automated work |
| --- | --- | --- |
| `after-topic` | User-selected or explicitly human-accepted topic and angle. A concrete topic supplied by the user already satisfies this choice. | Research, hook selection, and later work. |
| `after-hook` | User-selected or supplied hook, with any new factual implication verified. | Script drafting and later work. |
| `after-script` | Human approval of the completed script version. | Visual storyboard and later work. |
| `after-storyboard` | Human approval of the verified complete visual-storyboard version, including its PNG. | Audio, animation, and later work. |

Before activation, present choices/review artifacts and wait at the human checkpoints retained by the selected policy. Earlier choices explicitly delegated separately use [presentation and durable records](#presentation-and-durable-records). Use `awaiting_review` for a pending production checkpoint; keep topic discovery in the conversation until selection under [topic selection](topic-selection.md). The activation checkpoint is the existing choice/review, not an extra approval question. Once it is satisfied, activate automation and continue in the same turn through the resolved endpoint without requiring the user to repeat the flag.

Earlier choices may be explicitly delegated separately: for example, `--topic=auto --automation=after-hook` delegates the topic but retains human hook selection. The activation checkpoint itself remains human: `--topic=auto --automation=after-topic` for new topic discovery, or explicit hook delegation with `after-hook`, conflicts and must be resolved before dependent actions. Bare `--automation` alone retains its existing topic-selection rule; use `--topic=auto` to delegate discovery and selection.

Persist delayed state from intake in `EPISODE.md` once a production exists, and mirror it in `video/BRIEF.md` when present. For example, before hook selection:

```text
execution_policy: automation
automation_after: hook
automation_state: pending
human_review: defaults through hook selection
pre_render_authorization: pending activation
```

Use `automation_after: topic|hook|script|storyboard` for delayed values. On acceptance, set `automation_state: active`, set `human_review: none for subsequent work`, record the activating human decision and artifact/version, and set pre-render authorization to delegated by the user's selected automation option after activation. Retain earlier human approval evidence separately. For bare automation, use `automation_after: none`, `automation_state: active`, and the active policy below; legacy automation records without these fields retain immediate activation.

On resume, verify the recorded activation evidence against the current topic/artifact version. Reuse a valid prior human decision, including one made before the flag was supplied; file existence or agent verification alone does not satisfy a human activation checkpoint. If evidence is missing, keep activation pending and present the current choice/artifact for acceptance before further dependent work. If a revision invalidates the activating decision, return to pending and reapply the affected human checkpoints through activation; preserve unaffected approvals and outputs. A later explicit policy change takes precedence.

### Active automation and HyperFrames

Apply this section only when automation is active. While activation is pending, retain the normal HyperFrames review mode and checkpoints; in particular, `after-storyboard` requires its complete visual board and human approval before switching modes.

Use the project-local consolidated [HyperFrames contract](../../hyperframes/SKILL.md). Carry the resolved policy into `EPISODE.md` and `video/BRIEF.md`; initialize a video project only when the endpoint needs it. The [complete visual storyboard](storyboard.md), including its PNG, remains required before audio synthesis and animation. Perform and verify it, then continue without a human pause when automation is active. Reuse existing accepted layouts and approvals on continuation. Legacy `flow`, `storyboard`, and `mode` fields may remain in saved files; they do not require a retired workflow or replace this policy.

Also record this project-specific active policy in `EPISODE.md` and `video/BRIEF.md` once that project exists (use the actual selected automation option in the authorization record):

```text
execution_policy: automation
human_review: none
pre_render_authorization: delegated by the user's --automation instruction
```

Run the checks relevant to the endpoint. When preview is in scope, inspect the final look and record proof-frame locations and findings; present it under the policy below. Active automation authorizes the delivery render only when export is also in scope. Record the version as agent-verified under delegated authorization; keep human approval fields false/unset unless a human actually approved it. Legacy instructions such as "use approved narration" mean the agent-verified narration for this run.

In automation, fix failed checks within scope and proceed when they pass. An unresolved dependency produces a concrete blocked result, not `awaiting_review`; preserve completed work. The one human pause automation keeps is a gate verdict of `needs_human_review`: with no fresh-context reviewer, present the final preview with `awaiting_review` under [quality gate](quality-gate.md#run-the-gate). A final pending asynchronous publication is `in_progress`, not a fabricated blocker or success.

Without an automation option or a recorded equivalent, project review defaults apply. A later explicit request to review together restores human checkpoints. A delayed option intentionally combines earlier human gates with later automation. Resolve only genuinely contradictory instructions, such as delegating the activation checkpoint itself, before dependent actions.

The pre-script hook checkpoint follows [research and script](research.md): present 3 hooks after research and wait for selection by default. Active automation delegates that choice while retaining the options and rationale in `EPISODE.md`. Pending `after-hook`, `after-script`, and `after-storyboard` retain human hook selection unless an earlier choice is separately delegated under the activation rules. `--topic=auto` alone delegates only the topic choice and retains the hook checkpoint.

### Presentation and durable records

Separate artifact creation, verification, and chat presentation. Delegated decisions and reviews retain their required artifacts and quality checks. Apply the following to each delegated choice, including a separately delegated topic or hook before automation activates:

- Keep candidate comparisons, hook alternatives, research evidence, script/storyboard revisions, proof frames, check results, and routine repair history in their existing production files. Store concise decision reasons and provenance in `EPISODE.md`, evidence in `SOURCES.md` or the verification document, and delivery identities/results in the publishing receipt. Internal work must remain recoverable on resume; chat and ephemeral reasoning are not its only record.
- Summarize the selected topic and its reason. Other routine decisions can be grouped into a brief progress update. Keep intermediate scripts, storyboard links/images, preview proof sheets, package copy, and technical logs in the production unless human input is required, they are the requested endpoint, or the user asks to inspect them.
- Send brief updates during long work, focused on meaningful progress, a changed direction, or the next substantial step. Consolidate related decisions and checks; routine commands and successful repairs belong in the records. Surface unresolved blockers, material scope changes, and limitations that affect the delivered result.
- At a retained human checkpoint, present the actual choices or complete review artifact and wait. A final preview leads with the gate's [disclosure](quality-gate.md#disclose-at-checkpoints). Delayed automation preserves these checkpoints through activation. A request to see more detail changes presentation only; a request to review/approve together restores the applicable human checkpoints.
- At the requested endpoint, deliver the artifact and concise verified outcome, with links needed to use it. A storyboard endpoint includes both HTML and PNG; a preview endpoint includes its live location and proof frames. Export/package endpoints include the verified video and requested companion files/package. External delivery reports actual per-target status, account/workspace identity, schedule or publication link when applicable, and the receipt; preserve partial or pending outcomes accurately.

This production policy governs intermediate presentation by HyperFrames, packaging, and external-delivery handoffs. Pass the resolved choices, endpoint, review authorization, and presentation policy as run context; apply these project-specific instructions in place of generic human-presentation defaults without modifying the installed HyperFrames skills. During active automation, a generic storyboard or final-look pause becomes agent verification with recorded evidence, and alternative-storyline/review summaries remain in the production records. Retain technical preview inspection and lifecycle cleanup; a preview used internally during automation through export or later needs no separate chat presentation. Include relevant editing information in the final handoff when useful. Reuse valid saved decisions and evidence on continuation, with the same compact presentation default. An explicit request for detailed output takes precedence without adding a new option or changing delivery authorization.

## Delivery scope

Automation options change interaction, not the endpoint. `--delivery=draft|queue|publish` explicitly authorizes media upload/reuse through Trypost Local and the selected delivery action. Default to direct local-media upload. Fulfill the selected action without another permission question once inputs and required production checks are resolved. A delivery option alone retains earlier production review defaults; automation removes checkpoints only after its activation rules are satisfied. Creating a draft adds no separate standing review gate unless requested.

For external delivery, resolve the entire target set under [target inheritance](publishing.md#target-inheritance): explicit production selection, then saved production choices, then every account in the selected board's `ACCOUNTS.json`. Configuration alone does not select a delivery action. A sole connected channel is not a default identity for every board. Preserve known declarations; infer only routine editorial settings. Follow [publishing](publishing.md) for preflight, receipts, and completion.

The Stage endpoint contract resolves narrower endpoints and delivery conflicts. Skill-authoring requests and examples in this guide do not execute any of these deliveries.

## Examples

```text
$shortform-production --board=di-balik-benda --automation=after-hook --until=export
Carikan topik.
```

Present 10 topics and wait for the user's choice. Research the selected topic, present 3 hooks, and wait for hook selection. That selection activates automation: draft the script, create and agent-verify the complete visual storyboard, then continue through verified MP4 export without later human checkpoints. Persist the policy across both choices and any interruption.

```text
$shortform-production --board=di-balik-benda --automation=after-topic
Carikan topik.
```

Wait for topic selection, then automate research, hook selection, and production through the content package.

```text
$shortform-production topik: confirmation bias --board=berkas-polemik --automation=after-script
```

Keep human hook selection and script approval. Approval of the script activates automation through the content package.

```text
$shortform-production --board=ruang-di-antara --topic=auto --automation=after-storyboard
```

Record the topic shortlist internally and summarize the delegated pick. Retain human hook, script, and complete visual-storyboard reviews, then automate the remaining work after storyboard approval.

```text
$shortform-production topik: confirmation bias --board=berkas-polemik --automation=after-storyboard --until=script
```

Keep human hook selection and script review, then finish at the accepted script. Automation remains pending; the cap stops before storyboard creation. A later continuation beyond this cap preserves the pending policy.

```text
$shortform-production topik: confirmation bias --board=berkas-polemik --automation --until=script
```

Research, record 3 hooks and select one under automation, then write and verify the script. Deliver `SCRIPT.md` and finish at `script: complete` without review pauses or downstream video work.

```text
$shortform-production --board=ruang-di-antara --topic=auto --automation --until=storyboard
```

Evaluate and record 10 topics with short briefs and a recommendation, summarize the delegated pick, research it, and record/select one of 3 hooks internally under automation. Produce its script and complete visual storyboard, including `video/boards/storyboard.png`, without human checkpoints. Verify and deliver the HTML board and PNG because storyboard is the endpoint, then stop before audio synthesis or animation.

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

Select one non-duplicate topic from the board, research and produce it, then upload the verified export through Trypost and publish to the verified account without review pauses. If a verified board/account mapping already supplies the target, `--channel` can be omitted. This example does not establish a permanent mapping.

```text
$shortform-production topik: limerence --board=ruang-di-antara --automation
```

New production through the content package, with no review pauses. Create and agent-verify the complete visual storyboard, including `storyboard.png`, before audio and animation. Inspect existing topics for overlap before creating a new production.

```text
$shortform-production lanjut limerence --automation --delivery=draft --channel=instagram:eliansatya
```

Reuse valid existing artifacts, upload or reuse the verified MP4, and create or reconcile the requested Instagram draft in its resolved Trypost workspace.

```text
$shortform-production topik: confirmation bias --board=berkas-polemik --automation --delivery=queue --channel=instagram:ACCOUNT --at=2026-11-02T19:00:00+07:00
```

Run through scheduling without a review gate once the real target replaces `ACCOUNT` and its identity is verified. Dates and account names here illustrate syntax, not standing production choices.
