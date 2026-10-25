# Storage and state

## Root tracker

`TRACKER.json` contains only two registries:

```json
{
  "boards": [],
  "productions": []
}
```

Read an existing file before editing it. Preserve other board and production entries and any user-maintained fields. Create this minimal shape if the tracker is missing and production work is requested. A parse error needs repair or clarification; do not replace an unreadable tracker with empty data.

A board entry contains `slug`, `status`, and root-relative `path`. Existing approved boards are input data; production work does not mark a new board approved.

Each production uses one row with these fields:

| Field | Meaning |
| --- | --- |
| `slug` | Stable folder identifier. |
| `topic` | Human-readable topic; lets the next agent detect what has already been covered. |
| `board` | Selected board slug, or `null` for sufficient direct creative guidance. |
| `stage` | Actual stage: `brief`, `research`, `script`, `storyboard`, `audio`, `production`, `verification`, `preview`, `export`, `content_package`, or optional `publishing`. |
| `status` | Condition of that stage: `in_progress`, `awaiting_review`, `needs_revision`, `complete`, or `blocked`. |
| `path` | Root-relative `productions/<slug>` path. |

`complete` describes the recorded stage. `stage: export` with `status: complete` denotes a verified final video export; `stage: content_package` with `status: complete` denotes that export plus its finished content package. An export-only request can finish at export; full productions finish at content packaging by default. A script-only request can end at `stage: script`, `status: complete`; the requested endpoint and any future work are recorded in the episode brief. A blocker names a concrete missing input or failed dependency in that brief; it does not erase valid work.

For requested external delivery, `stage: publishing` uses the endpoint-specific completion rules in [publishing](publishing.md). A complete draft or scheduling endpoint is not a claim that the post is live. Detailed asset IDs, post IDs, attempts, and service status belong in the production's `PUBLISHING.json` receipt, not in root tracker fields.

Keep pipeline rules in the skill and creative details in the board or production. Add no decisions, discussions, conventions, approval histories, or project configuration objects to the tracker.

Write valid UTF-8 JSON with two-space indentation. Make the narrow entry update, preserve other entries, and verify JSON parsing and referenced folder existence afterward. If the file changed since it was read, reread and merge instead of overwriting the intervening update.

## Production folder

Use lowercase letters, numbers, and hyphens for the slug. Keep it stable if the display title changes. Inspect both the tracker and filesystem before assigning it: reuse the existing production for continuation, or choose a distinguishing suffix for a genuinely new production. Resolve target paths within the project root and keep writes inside the intended production folder.

Create only files needed by the requested stage:

```text
productions/<slug>/
  EPISODE.md       Production context, brief choices, requested endpoint, reviews, next action
  SOURCES.md       Researched claims and their sources
  SCRIPT.md        Narration and on-screen text
  CONTENT_PACKAGE.md Upload copy and verified delivery metadata, created after export
  PUBLISHING.json  Optional external media/post receipts, created when delivery is attempted
  video/           HyperFrames-owned project and its generated artifacts
  exports/         Delivered outputs, when requested
```

`EPISODE.md` carries the chosen board/reference revision when available, links to the source direction, resolved editorial and visual choices, requested endpoint (including `until` when selected), execution/review policy, remaining material questions, current review outcome, and next action. Store hook options, the recommendation, and the selected hook with its selection provenance here under [research and script](research.md). While the hook choice is pending, `stage: script`, `status: awaiting_review` identifies that checkpoint; `SCRIPT.md` is created after selection. For external delivery, include confirmed account mappings, timing, and a link to `PUBLISHING.json`. Identify the artifact/version each human approval or delegated authorization covers. This is production-local context, not another root-level tracker. Reflect the resolved endpoint in `video/BRIEF.md` when present so downstream workflow handoffs retain the cap.

Store `publishing_targets` in `EPISODE.md` under [target inheritance](publishing.md#target-inheritance), including the full selected account set and board-file provenance when inherited. Board account edits affect future defaults; existing production targets and delivery receipts retain their identities. A package-only production can snapshot local account identities without MCP calls or external delivery.

For delayed automation, persist `automation_after`, `automation_state`, retained human checkpoints, and the activating decision/version under [automation activation](invocation.md#activation); mirror them in `video/BRIEF.md` when present. Before topic selection, retain the requested policy in the conversation rather than creating a production early. A resume preserves pending/active state and verifies its evidence instead of interpreting every automation policy as immediately active.

HyperFrames initializes **inside `video/`**, initially empty; it refuses a nonempty target. Read the installed entry/CLI/workflow setup before invoking initialization. The workflow then writes its canonical `video/BRIEF.md`, `video/STORYBOARD.md`, `video/frame.md`, and composition files according to its own contract. Do not prefill that directory with notes, assets, or a brief to bypass intake. Resume an existing HyperFrames project without initializing it again.

When storyboard is in scope, store and verify the complete artifact set under [visual storyboard](storyboard.md), including `video/boards/storyboard.png`. Record its paths and review/verification outcome in `EPISODE.md`; active automation retains these deliverables while delegating the human checkpoint to the agent.

The production brief supplies answers to HyperFrames intake. Its canonical `video/BRIEF.md` owns execution choices once created; reflect confirmed changes in the appropriate documents without repeating the interview. Store assets required for rendering inside `video/` using the workflow's paths. Keep required font files and licenses with the project as needed. Preserve board-specific decisions in the resulting project spec rather than depending on a mutable global default.

Existing production layouts are resumed in place. If a HyperFrames project already lives at the production root, recognize its configuration and resume there; do not move it merely to match the new-folder convention.
