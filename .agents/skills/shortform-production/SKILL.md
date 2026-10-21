---
name: shortform-production
description: Create, continue, or revise short-form productions through export and packaging, with optional Cloudinary hosting and Buffer delivery. Supports board selection, automatic topic discovery, and review-free automation through skill-prompt options. Use for production artifacts and publishing handoffs; discussion and board exploration stay at their requested scope.
---

# Shortform Production

Move the requested production from its actual current state to the requested deliverable. Use the selected board or supplied creative direction for content and style decisions; resolve production-specific choices in the brief.

## Invocation

Read [invocation options](references/invocation.md) before intake when the prompt contains options such as `--board=<name>`, `--topic=auto`, `--automation`, `--until=<stage>`, or `--delivery=<endpoint>`, delegates topic selection, requests review-free execution or a partial endpoint, or resumes a production with a recorded automation policy or stage cap. It owns option validation, board precedence, topic delegation, stage endpoints, execution policy, and delivery authorization. These are skill-prompt options, not shell commands. Default delivery is a content package; external delivery is explicit.

## Start with context and scope

1. Locate the project root from the user's path or current workspace and read its `TRACKER.json`. Read [storage and state](references/storage.md) before creating a production or updating its status. Follow existing workspace instructions.
2. Identify whether the user wants discussion, a new production, continuation, a partial deliverable, or a revision. A discussion ends with the requested explanation; create production artifacts when production work is requested. Honor endpoints such as research only, script only, or storyboard only.
3. For a video or motion request, load the installed `hyperframes` entry skill before making production decisions. It owns workflow routing, intake requirements, installation, run shape, usage checks, and technical execution. Locate dependencies through the skill catalog or project-installed skills rather than embedding a machine-specific path. If a necessary dependency is unavailable, identify what is missing and continue only independent work that remains possible.
4. For continuation, read the named production's artifacts. If the target is ambiguous among multiple productions, ask which one; do not select the most recently listed item by accident. For a new topic, inspect existing production topics and flag a close overlap with its path before repeating substantial work. A requested new angle can be a separate production.
5. For topic discovery requests, including "carikan topik", or delegated selection such as `--topic=auto`, follow [topic discovery and selection](references/topic-selection.md): present 10 topics with short briefs and a recommended pick. Discovery alone waits for the user's choice; explicit selection delegation follows the invocation contract. Complete selection before assigning a slug or creating production files. A resumed production keeps its recorded topic.

## Resolve creative direction

- An explicit current board choice takes priority. When continuing a production, preserve its recorded board unless the user changes it.
- For a new production, select a board when the user names it, requests continuity with its direction, or delegates selection. `--board` resolves through the invocation contract; `--automation` delegates an unnamed board's selection within that contract. Otherwise, use sufficient direct creative guidance with `board: null`. If direction is missing, recommend relevant boards or a new direction and ask for the choice. Assess fit against the requested niche, audience, purpose, format, and style; a board's availability alone does not establish fit.
- Read the chosen board's actual documents, including its domain-specific sourcing rules when researching claims. Use the registry path to discover them; link to its editorial guidance and visual spec. Record the selection and available revision in the production brief, and retain the resolved production-specific direction.
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
| `script` | After the topic is locked and research is resolved, present 3 distinct hooks and resolve the hook choice under [research and script](references/research.md) before writing `SCRIPT.md`. Then develop the copy, dialogue, narration, or action with the selected hook, board/brief, researched claim boundaries, and realistic timing. A supplied final script is reused within its authorized editing scope. |
| `storyboard` | Create and verify the scene plan, styled scene stills, HTML board, and `video/boards/storyboard.png` under [visual storyboard](references/storyboard.md). These artifacts are required whenever a new production reaches this stage, including automation and runs continuing to export or publishing. Every scene has a purpose, legible content, a visual idea, and estimated timing. Verified layouts remain the basis for animation; the run's review policy determines who accepts them. |
| `audio` | Resolve separate narration, BGM, and SFX decisions from the brief and board using [audio generation](references/audio.md). Record planned cues or a reason for intentional absence; a quiet mood alone does not resolve SFX. Use measured voice timings to place cues and refine scenes. |
| `production` | Build the composition through HyperFrames using the selected project direction. Follow its core contract and load creative, registry, animation, keyframes, media, or audio skills as needed. The registry skill precedes hand-building named effects. |
| `verification` | Run the owning workflow's technical checks and inspect representative rendered frames, transitions, caption placement, and the complete audiovisual preview as applicable. Reconcile planned audio cues with placed tracks; verify cue presence and timing in the export, separately from mix loudness. Record creative listening evidence and any limits honestly. Repair actual problems and rerun affected checks. |
| `preview` | Present the final composition preview with its location and proof frames. Apply feedback and reverify. Follow HyperFrames' final-look approval by default; a recorded automation policy replaces the human gate with agent verification and delegated render authorization under the invocation contract. Reuse an existing approval of this exact version. |
| `export` | Export the version authorized by the run's execution policy through HyperFrames, inspect the produced file and actual duration, and deliver paths. Produce caption files or a cover when requested or included in the accepted brief. Mark this stage complete only after the required files exist and the export is verified. |
| `content_package` | After verified export, create `CONTENT_PACKAGE.md` following [content packaging](references/content-package.md). Prepare upload copy and verified delivery metadata for the intended destinations. Done when the package matches the delivered version, required fields are resolved, and all linked delivery files exist. |
| `publishing` | Only for requested external delivery: follow [publishing](references/publishing.md), preflight channels with [buffer-mcp](../buffer-mcp/SKILL.md), host or reuse the verified file with [cloudinary-mcp](../cloudinary-mcp/SKILL.md), then execute the selected Buffer action. Done when each target meets that endpoint's evidence requirement and its receipt is saved. |

Full production requests continue through `content_package` by default, with the run's review checkpoints. `--until=<stage>` or an explicitly narrower natural-language endpoint, including export only, takes priority over package delivery; validate external-delivery conflicts through the invocation contract. A package-only request reuses the existing verified export and approved production artifacts; it does not restart video production. Previously completed exports remain valid and gain a package when continuation or packaging is requested.

An explicit external-delivery endpoint continues from the package through `publishing`; load that reference only for this branch. A publishing-only request reuses the existing verified export, package, and still-valid approval or delegated authorization.

For research, factual claim revision, or script development, read [research and script](references/research.md) and apply its relevant branch. For narration synthesis, sound effects, BGM, or word alignment, read [audio generation](references/audio.md). Follow workspace preferences for research tools; use Context7 for library/SDK/CLI documentation where required.

Before storyboard work or a HyperFrames handoff that reaches it, read [visual storyboard](references/storyboard.md). Its artifact requirement overrides the owning workflow's autonomous-mode sketch skip for this pipeline; automation replaces the human review with agent verification.

## Review without repeating intake

Review the full scene contact sheet for visual rhythm as well as individual frames for correctness. Check changes in focal hierarchy, scale, placement, density, and choreography; a different subtitle, diagram label, or path alone does not establish a different composition. Inspect fixed board elements across scenes and compare them with the canonical spec. Record these creative checks separately from technical render checks. Automation delegates this review to the agent; it does not remove it.

Use the hook-selection checkpoint in [research and script](references/research.md), then the project's script, visual-storyboard, and final-preview checkpoints for a fresh multi-scene production unless the current run explicitly changes them. The [invocation contract](references/invocation.md) owns `--automation`, including its final-look override. Automation continues after agent verification without inventing human approval. Other explicit review preferences and the selected HyperFrames run shape govern the remaining cases.

Keep hook selection before script drafting; bundle other related editorial choices into a concrete script/plan review where the owning workflow allows it. Reuse HyperFrames' plan, sketch, and final-look checkpoints instead of placing duplicate approvals around the same artifact. A board selection is resolved only when needed; it is not another standing review step.

Resolve material missing inputs when necessary and continue independent work. In automation, make routine choices with reasons and report a concrete blocker for information that cannot be inferred safely within scope. Existing authorizations persist; execute within their scope. Export and external publication remain separately selected endpoints.

## Preview lifecycle

Treat preview servers as production resources with an owner and a release point. Use the project's resolved HyperFrames CLI version for lifecycle commands; command completion does not mean the background server stopped.

- Before starting a preview, run `preview --status --json` from the actual video project directory. Reuse a healthy preview for that project; start `preview --background` only when none exists. If status fails for another reason, diagnose it before starting another server. Routine continuation does not need `--force-new` or a different port.
- Record the project path, PID, actual port, Studio URL, whether this run created the server, and its retention reason in `EPISODE.md`. Identify an inherited pipeline preview from that record; leave an independently opened user server under user control.
- Keep the preview alive while its visual review is pending, when a live preview is the requested endpoint (including automated `--until=preview`), or when the user asks to keep editing. Record the hold and next release condition. An unrelated blocked stage or delivery endpoint does not need a live preview.
- After review and any render work finish, release the pipeline-owned preview before packaging or external delivery. In automation through export or later, release it after export verification. On failure, cancellation, or another endpoint, clean up servers this run created unless one of the retention conditions above applies. A resumed run also releases an inherited pipeline-owned preview once its recorded hold ends.
- Stop with `preview --stop --json` from that project's directory, then query status again. Verify that the recorded process no longer owns the listening port before recording cleanup as complete. A port occupied by a different process needs identification, not termination.
- If managed stop fails, inspect the recorded process and its command line/project before any targeted process-tree termination. Never use global Node termination or `preview --kill-all` for production cleanup; unrelated projects and MCP servers may share the machine. Report any cleanup failure with the remaining PID/port and record it in `EPISODE.md`; keep the artifact's actual stage/status accurate.
- Apply the same ownership, retention, and release rules to temporary static servers or other preview processes created for the production. Record their stop method when starting them. A helper that starts a temporary server should release it in `finally` unless it deliberately hands ownership to the recorded review hold.

## Resume and revise

- Read the tracker, then `EPISODE.md` and the current stage's artifacts. Verify that the files support the recorded status before continuing; reconcile stale status with the actual work and current feedback.
- Preserve completed decisions, the recorded execution policy, and valid outputs. Distinguish human approval, delegated authorization, and successful verification; file existence alone establishes none of them.
- Trace revisions through dependencies: changed claims affect research/script; changed narration affects voice, timing, and captions; changed layout affects the relevant scene and verification. Return only the affected stages to active work, and revisit changed checkpoints when applicable.
- Update the production row after a meaningful stage transition or user review, with enough context in `EPISODE.md` to identify the accepted version and the next action. The tracker stays small.
- At a requested endpoint, deliver that artifact, record its actual stage/status, and stop. A completed script or storyboard does not imply a completed video.
