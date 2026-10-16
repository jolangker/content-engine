---
name: shortform-production
description: Orchestrate new or resumed short-form video productions using project-provided creative direction, a root TRACKER.json, slug folders, and HyperFrames. Use to develop a topic or source into a production, continue an episode, or revise its artifacts; pure discussion or board exploration stays at the requested scope.
---

# Shortform Production

Move the requested production from its actual current state to the requested deliverable. Use the selected board or supplied creative direction for content and style decisions; resolve production-specific choices in the brief.

## Start with context and scope

1. Locate the project root from the user's path or current workspace and read its `TRACKER.json`. Read [storage and state](references/storage.md) before creating a production or updating its status. Follow existing workspace instructions.
2. Identify whether the user wants discussion, a new production, continuation, a partial deliverable, or a revision. A discussion ends with the requested explanation; create production artifacts when production work is requested. Honor endpoints such as research only, script only, or storyboard only.
3. For a video or motion request, load the installed `hyperframes` entry skill before making production decisions. It owns workflow routing, intake requirements, installation, run shape, usage checks, and technical execution. Locate dependencies through the skill catalog or project-installed skills rather than embedding a machine-specific path. If a necessary dependency is unavailable, identify what is missing and continue only independent work that remains possible.
4. For continuation, read the named production's artifacts. If the target is ambiguous among multiple productions, ask which one; do not select the most recently listed item by accident. For a new topic, inspect existing production topics and flag a close overlap with its path before repeating substantial work. A requested new angle can be a separate production.

## Resolve creative direction

- An explicit current board choice takes priority. When continuing a production, preserve its recorded board unless the user changes it.
- For a new production, select a board when the user names it, requests continuity with its direction, or delegates selection. Otherwise, use sufficient direct creative guidance with `board: null`. If direction is missing, recommend relevant boards or a new direction and ask for the choice. Assess fit against the requested niche, audience, purpose, format, and style; a board's availability alone does not establish fit.
- Read the chosen board's actual documents, including its domain-specific sourcing rules when researching claims. Use the registry path to discover them; link to its editorial guidance and visual spec. Record the selection and available revision in the production brief, and retain the resolved production-specific direction.
- Approved board direction is reusable context, not approval of a new episode's claims, script, or layout. Treat draft board use as an explicit choice when the user requests it.
- When no board fits, show the mismatch and offer an appropriate direction adjustment or separate board exploration. A supplied brief or direct creative guidance can be sufficient without a board; record `board: null` and state the direction used. Ask only when the missing choice materially changes the result.
- A board change triggers review of affected work. New boards added to the registry do not change existing productions automatically.

## Produce from the earliest unfinished dependency

Use the following as a dependency map. Reuse completed artifacts, skip inapplicable stages, and load downstream instructions only when their stage is needed.

| Stage | Work and completion criterion |
| --- | --- |
| `brief` | Capture the content purpose, topic or source material, intended audience experience, destination/aspect, language, duration target, creative direction, audio needs, requested endpoint, and review behavior as relevant. Use supplied answers and HyperFrames intake once. Store durable context in `EPISODE.md`; distinguish confirmed choices from proposed defaults and unresolved fields. |
| `research` | Resolve factual claims, context, or reference needs identified in the brief. Record sources, findings, and limitations in `SOURCES.md`; map substantive factual claims to evidence when present. Done when each identified need is resolved or the brief is revised to reflect the available support. |
| `script` | Write `SCRIPT.md` when the format needs planned copy, dialogue, narration, or action. Follow the selected board or brief's structure and tone, with researched claim boundaries and realistic timing. A supplied final script is reused within its authorized editing scope. |
| `storyboard` | Through the selected HyperFrames workflow, develop the scene plan and styled static frames when requested. Follow its canonical `STORYBOARD.md` and storyboard-board format. Every scene has a purpose, legible content, a visual idea, and estimated timing. Confirmed layouts remain the basis for animation. |
| `audio` | Resolve only the narration, music, and sound effects called for by the brief. Use real voice/word timings to refine the scene plan before final animation and captions. Silent or unnarrated work skips the irrelevant audio dependencies. |
| `production` | Build the composition through HyperFrames using the selected project direction. Follow its core contract and load creative, registry, animation, keyframes, media, or audio skills as needed. The registry skill precedes hand-building named effects. |
| `verification` | Run the owning workflow's technical checks and inspect representative rendered frames, transitions, caption placement, and the complete audiovisual preview as applicable. Repair actual problems and rerun the affected checks. Done means the requested artifact has evidence of passing the relevant checks. |
| `preview` | Present the final composition preview with its location and relevant proof frames. Apply feedback to the affected parts and reverify. Follow HyperFrames' final-look approval before rendering; an existing approval of that exact preview does not need to be requested twice. |
| `export` | Export the approved version through HyperFrames, inspect the produced file and actual duration, and deliver paths. Produce captions, a cover, or upload copy when requested or included in the accepted brief. Mark complete only after the required files exist and the export is verified. |

For research, factual claim revision, or script development, read [research and script](references/research.md) and apply its relevant branch. For narration synthesis, sound effects, BGM, or word alignment, read [audio generation](references/audio.md). Follow workspace preferences for research tools; use Context7 for library/SDK/CLI documentation where required.

## Review without repeating intake

Recommend reviewing the script, visual storyboard, and final preview for a fresh multi-scene production. Present these as a working recommendation when review preferences are unknown, rather than treating earlier project discussion as blanket acceptance. Explicit user instructions and the selected HyperFrames run shape govern checkpoint behavior.

Bundle related editorial choices into a concrete script/plan review where the owning workflow allows it. Reuse HyperFrames' plan, sketch, and final-look checkpoints instead of placing duplicate approvals around the same artifact. A board selection is resolved only when needed; it is not another standing review step.

Ask for material missing inputs when they become necessary and continue independent work. In delegated or autonomous work, state routine choices and reasons. Existing authorizations persist; execute within their scope. Export and external publication are separate actions.

## Resume and revise

- Read the tracker, then `EPISODE.md` and the current stage's artifacts. Verify that the files support the recorded status before continuing; reconcile stale status with the actual work and current feedback.
- Preserve completed decisions and reuse valid outputs. Never equate file existence with user approval or successful verification.
- Trace revisions through dependencies: changed claims affect research/script; changed narration affects voice, timing, and captions; changed layout affects the relevant scene and verification. Return only the affected stages to active work, and revisit changed checkpoints when applicable.
- Update the production row after a meaningful stage transition or user review, with enough context in `EPISODE.md` to identify the accepted version and the next action. The tracker stays small.
- At a requested endpoint, deliver that artifact, record its actual stage/status, and stop. A completed script or storyboard does not imply a completed video.
