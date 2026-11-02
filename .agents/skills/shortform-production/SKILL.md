---
name: shortform-production
description: Create, continue, or revise short-form productions through export and packaging, with optional Trypost Local delivery. Supports board selection, automatic topic discovery, and immediate or delayed automation through skill-prompt options. Use for production artifacts and publishing handoffs; discussion and board exploration stay at their requested scope.
---

# Shortform Production

Move the requested production from its actual current state to the requested deliverable. Use the selected board or supplied creative direction for content and style decisions; resolve production-specific choices in the brief.

Follow [presentation and durable records](references/invocation.md#presentation-and-durable-records) when a choice or review is delegated: retain production artifacts and verification evidence, and use concise progress updates until the requested deliverable. Present full choices or review artifacts when human input is required, the artifact is the endpoint, or the user asks to see it. Carry this presentation policy into HyperFrames and delivery work.

## Invocation

Read [invocation options](references/invocation.md) before intake when the prompt contains options such as `--board=<name>`, `--topic=auto`, `--automation` (bare or `=after-topic|after-hook|after-script|after-storyboard`), `--until=<stage>`, or `--delivery=<endpoint>`, delegates topic selection, requests immediate/delayed automation or a partial endpoint, or resumes a production with a recorded automation policy or stage cap. It owns option validation, board precedence, topic delegation, stage endpoints, execution policy, and delivery authorization. These are skill-prompt options, not shell commands. Default delivery is a content package; external delivery is explicit.

## Start with context and scope

For a bare invocation, show unfinished productions and wait for a continuation/new-production choice; if none exist, ask for a topic or source. Create production files only after the topic is selected and production is requested. Options and delegated discovery follow the invocation contract instead.

1. Locate the project root from the user's path or current workspace and read its `TRACKER.json`. Read [storage and state](references/storage.md) before creating a production or updating its status. Follow existing workspace instructions.
2. Identify whether the user wants discussion, a new production, continuation, a partial deliverable, or a revision. A discussion ends with the requested explanation; create production artifacts when production work is requested. Honor endpoints such as research only, script only, or storyboard only.
3. When authoring or changing a video composition, use the project-local [HyperFrames contract](../hyperframes/SKILL.md) and only the relevant task references. Carry the resolved brief, board, endpoint, and review policy into it once. Older workflow names are implementation history; reuse valid files and required helpers. Text/package/delivery work using an existing export follows its own branch below. Report missing required capabilities and continue independent work.
4. For continuation, read the named production's artifacts. If the target is ambiguous among multiple productions, ask which one; do not select the most recently listed item by accident. For a new topic, inspect existing production topics and flag a close overlap with its path before repeating substantial work. A requested new angle can be a separate production.
5. For topic discovery requests, including "carikan topik", or delegated selection such as `--topic=auto`, follow [topic discovery and selection](references/topic-selection.md): prepare a lightweight editorial shortlist of 10 topics with short briefs and a recommended pick. Deep research begins after a topic is selected. Present the shortlist for human selection; for delegated selection, record it in the episode and summarize the pick. Discovery alone waits for the user's choice; explicit selection delegation follows the invocation contract. Complete selection before assigning a slug or creating production files. A resumed production keeps its recorded topic.

## Choose the current task

After identifying the target and reading its current state, take the matching branch. Read additional guides when a real dependency requires them.

| Current request | Work and references |
| --- | --- |
| Static board or board-account work | Use `shortform-board`; its static references do not start a video production. |
| Package or post-copy revision | Use [content packaging](references/content-package.md), the relevant script/source boundaries, and verified export metadata. Load publishing/Trypost only for an authorized remote change. A changed factual claim also needs research. |
| Publishing only | Use [publishing](references/publishing.md) and Trypost with the verified export, package, saved targets, and valid authorization. Prepare a missing package within scope. A missing/invalid video input is a concrete dependency to resolve; it does not authorize rebuilding the film. |
| Existing composition edit | Use HyperFrames with the saved production spec and only the affected task references. Load audio for narration/SFX sourcing changes, or media-use mixing for placed-track changes. Verify the affected result and invalidated dependencies. |
| New production or continuation through unfinished stages | Resolve the remaining direction below and follow the stage dependency map through the requested endpoint. |

Saved automation and delivery endpoints govern continuation within the current request; a narrow revision does not reopen later stages or repost the episode.

## Resolve creative direction

Resolve missing direction for new productions or an explicit board change. Other continuations reuse the recorded board revision, project spec, and saved targets; read only the board guidance relevant to the requested change.

- An explicit current board choice takes priority. When continuing a production, preserve its recorded board unless the user changes it.
- For a new production, select a board when the user names it, requests continuity with its direction, or delegates selection. `--board` resolves through the invocation contract; active automation delegates an unnamed board's selection within that contract. Before delayed activation, retain normal board choice unless separately delegated. Otherwise, use sufficient direct creative guidance with `board: null`. If direction is missing, recommend relevant boards or a new direction and ask for the choice. Assess fit against the requested niche, audience, purpose, format, and style; a board's availability alone does not establish fit.
- Read the chosen board's actual documents, including its domain-specific sourcing rules when researching claims. Use the registry path to discover them; link to its editorial guidance and visual spec. Record the selection and available revision in the production brief, and retain the resolved production-specific direction.
- Read the board's `ACCOUNTS.json` and snapshot production targets under [target inheritance](references/publishing.md#target-inheritance). Inherit every listed account unless the current request overrides the set; retain saved targets on continuation. An account list supplies package destinations without authorizing uploads or publishing.
- When the board provides a canonical `frame.md` or shared components, inherit them before adding episode-specific layout decisions. Preserve fixed identity elements across scenes and generations; vary the content composition according to the message. Record the inherited board implementation revision.
- Approved board direction is reusable context, not approval of a new episode's claims, script, or layout. Treat draft board use as an explicit choice when the user requests it.
- When no board fits, show the mismatch and offer an appropriate direction adjustment or separate board exploration. A supplied brief or direct creative guidance can be sufficient without a board; record `board: null` and state the direction used. Ask only when the missing choice materially changes the result.
- A board change triggers revalidation of affected work and human review when the run's review policy requires it. New boards added to the registry do not change existing productions automatically.

## Produce from the earliest unfinished dependency

Use the following as a dependency map. Reuse completed artifacts, skip inapplicable stages, and load downstream instructions only when their stage is needed. Enforce the resolved endpoint at each handoff; `--until` stops after its selected stage's deliverable and verification under the invocation contract.

| Stage | Work and completion criterion |
| --- | --- |
| `brief` | Capture the content purpose, topic or source material, intended audience experience, destination/aspect, language, duration target, creative direction, audio needs, requested endpoint, and execution/review policy. For external delivery also resolve target accounts and schedule. Use supplied answers and HyperFrames intake once. Store durable context in `EPISODE.md`; distinguish confirmed choices from inferred defaults and unresolved fields. |
| `research` | Resolve factual claims, context, or reference needs identified in the brief. Record sources, findings, and limitations in `SOURCES.md`; map substantive factual claims to evidence when present. Done when each identified need is resolved or the brief is revised to reflect the available support. |
| `script` | After the topic is locked and research is resolved, develop 3 distinct hooks and resolve the hook choice under [research and script](references/research.md) before writing `SCRIPT.md`. Present the options for human selection; retain them in the episode record for delegated selection. Then develop the copy, dialogue, narration, or action with the selected hook, board/brief, researched claim boundaries, and realistic timing. A supplied final script is reused within its authorized editing scope. |
| `storyboard` | Create and verify the scene plan, styled scene stills, HTML board, and `video/boards/storyboard.png` under [visual storyboard](references/storyboard.md). These artifacts are required whenever a new production reaches this stage, including automation and runs continuing to export or publishing. Every scene has a purpose, legible content, a visual idea, and estimated timing. Verified layouts remain the basis for animation; the run's review policy determines who accepts them. |
| `audio` | Resolve separate narration, BGM, and SFX decisions from the brief and board using [audio generation](references/audio.md). Record planned cues or a reason for intentional absence; a quiet mood alone does not resolve SFX. Use measured voice timings to place cues and refine scenes. |
| `production` | Build through HyperFrames using the selected board and relevant task references. Use [motion-graphics](../motion-graphics/SKILL.md) when a scene needs kinetic type, stats/charts, maps, source cards, or overlays; it inherits the scene's style and timing. Load registry before hand-building a named visual; use media-use for assets or mixing. |
| `verification` | Run HyperFrames' checks and review the rendered result under its review reference. Inspect representative frames, motion, transitions and caption placement. Reconcile planned audio cues with placed tracks and verify their timing in the export separately from loudness. Record listening evidence and limits honestly; repair problems and rerun affected checks. |
| `preview` | Inspect the final composition preview and proof frames, recording their locations and verification. Present them for human review, a preview endpoint, or an explicit request under the presentation policy. Apply feedback and reverify. Follow HyperFrames' final-look approval by default; a recorded automation policy replaces the human gate with agent verification and delegated render authorization under the invocation contract. Reuse an existing approval of this exact version. |
| `export` | Export the version authorized by the run's execution policy through HyperFrames, inspect the produced file and actual duration, and record paths for delivery at the requested endpoint. Produce caption files or a cover when requested or included in the accepted brief. Mark this stage complete only after the required files exist and the export is verified. |
| `content_package` | After verified export, create `CONTENT_PACKAGE.md` following [content packaging](references/content-package.md). Prepare upload copy and verified delivery metadata for the intended destinations. Done when the package matches the delivered version, required fields are resolved, and all linked delivery files exist. |
| `publishing` | Only for requested external delivery: follow [publishing](references/publishing.md), preflight accounts with [trypost-mcp](../trypost-mcp/SKILL.md), upload the verified file directly or reuse verified media, then execute the selected Trypost action. Done when each target meets that endpoint's evidence requirement and its receipt is saved. |

Full production requests continue through `content_package` by default, with the run's review checkpoints. `--until=<stage>` or an explicitly narrower natural-language endpoint, including export only, takes priority over package delivery; validate external-delivery conflicts through the invocation contract. A package-only request reuses the existing verified export and approved production artifacts; it does not restart video production. Previously completed exports remain valid and gain a package when continuation or packaging is requested.

An explicit external-delivery endpoint continues from the package through `publishing`; load that reference only for this branch. A publishing-only request reuses the existing verified export, package, and still-valid approval or delegated authorization.

For research, factual claim revision, or script development, read [research and script](references/research.md) and apply its relevant branch. For narration synthesis, sound effects, BGM, or word alignment, read [audio generation](references/audio.md). Follow workspace preferences for research tools; use Context7 for library/SDK/CLI documentation where required.

Before storyboard work, read [visual storyboard](references/storyboard.md). This pipeline requires its artifacts even when automation delegates layout review to the agent.

## Review without repeating intake

For a new film or a change to shared structure, layout, or timing, review the full scene contact sheet for visual rhythm as well as individual frames. Check focal hierarchy, scale, placement, density, choreography, and fixed board identity; changing a label alone does not create composition variety. For a narrow copy or audio edit, inspect affected frames/cues and broaden review when shared styling, timing, or the overall mix is invalidated. Record creative evidence separately from technical checks. Automation delegates review to the agent; it does not remove it.

Use the hook-selection checkpoint in [research and script](references/research.md), then the project's script, visual-storyboard, and final-preview checkpoints for a fresh multi-scene production unless the current run explicitly changes them. The [invocation contract](references/invocation.md#automation-and-review) owns immediate and delayed automation, including activation evidence, resume behavior, and the final-look override. Pending automation retains human checkpoints through the selected activation decision; active automation continues after agent verification without inventing human approval. Other explicit review preferences and the selected HyperFrames run shape govern the remaining cases.

Keep hook selection before script drafting. A researched hook and accepted board resolve the relevant HyperFrames storyline and look choices; reuse those decisions instead of adding another pitch round. Combine script, layout and final-preview reviews with the corresponding HyperFrames checkpoints. Resolve board selection when needed rather than adding a standing review step.

Resolve material missing inputs when necessary and continue independent work. In automation, make routine choices with reasons and report a concrete blocker for information that cannot be inferred safely within scope. Existing authorizations persist; execute within their scope. Export and external publication remain separately selected endpoints.

## Preview lifecycle

Before starting/resuming a preview or temporary server, and before ending its work, read [preview lifecycle](references/preview.md). It owns reuse, review holds, process ownership, and verified cleanup.

## Resume and revise

- Read the tracker, then `EPISODE.md` and the current stage's artifacts. Verify that the files support the recorded status before continuing; reconcile stale status with the actual work and current feedback.
- Preserve completed decisions, the recorded execution policy, and valid outputs. Distinguish human approval, delegated authorization, and successful verification; file existence alone establishes none of them.
- Trace revisions through dependencies: changed claims affect research/script; changed narration affects voice, timing, and captions; changed layout affects the relevant scene and verification. Return only the affected stages to active work, and revisit changed checkpoints when applicable.
- Update the production row after a meaningful stage transition or user review, with enough context in `EPISODE.md` to identify the accepted version and the next action. The tracker stays small.
- At a requested endpoint, deliver that artifact, record its actual stage/status, and stop. A completed script or storyboard does not imply a completed video.
