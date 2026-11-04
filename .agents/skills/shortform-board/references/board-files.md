# Board files and state

## Root tracker

`TRACKER.json` remains the shared registry with only `boards` and `productions`. Read before editing, preserve other entries and user-maintained fields, and update only the board being worked on. If the file is missing and board artifact work is requested, create the minimal structure with both arrays empty. Resolve malformed JSON instead of replacing it with an empty registry.

A board row has only:

```json
{
  "slug": "example-direction",
  "status": "draft",
  "path": "boards/example-direction"
}
```

- `draft`: development is incomplete or underway.
- `awaiting_review`: a specific artifact or proposal is ready for feedback; its phase is recorded in the board documents.
- `approved`: the current board package's editorial and visual direction have been accepted by the user.

Do not add discussion histories, conventions, extra top-level configuration, or production entries for board work. Detail and review context belong in the board folder. Keep UTF-8 JSON with two-space indentation, preserve concurrent updates by rereading before a write, and verify parsing and referenced folder existence afterward.

## Folder and artifacts

Use `boards/<slug>/`, with a stable lowercase slug containing letters, numbers, and hyphens. Inspect the tracker and filesystem for collisions. A display-name change does not require renaming the slug. A new concept gets its own board; a requested revision can remain under the existing slug.

Create files as their stage needs them:

```text
boards/<slug>/
  DIRECTION.md       Purpose, concept, decisions, scope, phase, reviews, next action
  frame.md           Canonical visual tokens and implementation guidance
  EDITORIAL.md       Board-specific content and storytelling framework
  ACCOUNTS.json      Publishing-account list inherited by new productions
  AUDIO.json         Optional narration voice ID; null inherits the root default
  style-board.html   Editable static board source; another suitable source format is acceptable
  style-board.png    Inspected review image
  style-board.pdf    Optional shareable export
  assets/           Fonts, licenses, or imagery actually used
```

`DIRECTION.md` records the board's working name, intended audience/experience, chosen creative concept, source references and provenance, current phase, requested endpoint, accepted versus proposed decisions, review results, and next action. Record enough to resume without reconstructing the conversation. Keep it concise; link detailed editorial and visual information instead of duplicating it.

Use HyperFrames' [look reference](../../hyperframes/references/look.md) for `frame.md`: visual tokens belong in its YAML frontmatter and intent/usage guidance in the body. Keep exact colors, families, and supported weights consistent with the exported board. If an earlier board stores its visual values in `DIRECTION.md` or another existing spec, resume that format without a forced migration.

For a board using 3D, follow [reusable 3D treatment](visual-craft.md#define-a-reusable-3d-treatment) for the canonical visual decisions, editable study source/assets, rendered evidence, and production handoff. Keep these within the existing board package and revision policy.

`EDITORIAL.md` records the content purpose, niche or scope, intended audience experience, and reusable format rules. Include account identity, pillars, story structures, sourcing rules, voice, and endings where relevant to the concept. Use illustrative examples to clarify choices and mark unresolved choices as open fields. This guidance applies to productions that select the board.

The style-board source and its export show the same revision. Review at board scale and zoom into sample frames. Check font loading, contrast/readability, overflow, and layout; inspect actual output rather than relying only on source syntax. Image/PDF existence is not evidence that the user approved the board.

## Narration voice

`AUDIO.json` is the board's source of truth for its narration voice override. Use UTF-8 JSON with two-space indentation:

```json
{
  "schema_version": 1,
  "voice_id": null
}
```

Set `voice_id` to the selected ElevenLabs voice ID. `null`, an empty/whitespace string, an omitted `voice_id`, or an absent file inherits the root project `.env` default. Create this file with `null` for a new board whose voice is undecided. Validate the schema and value type; malformed configuration is an error rather than an implicit fallback. Preserve unrelated fields when editing.

Link the file from `DIRECTION.md` and record the user's voice selection there. This operational change preserves the board's creative version, approval, and static exports. Voice precedence, production request provenance, and synthesis validation belong to [audio generation](../../shortform-production/references/audio.md#voiceover-elevenlabs). Configuration changes leave completed recordings and historical metadata intact; regenerate only within an authorized production revision.

## Publishing accounts

`ACCOUNTS.json` is the board's source of truth for default publishing targets. Keep it as UTF-8 JSON with two-space indentation, root `schema_version: 1`, and an `accounts` array. An empty array (or an older board without this file) means no configured targets. A board may have any number of accounts, across platforms or on the same platform; every listed account is a default target, not an alternative to choose among.

Each account contains `provider: trypost`, `workspace_id`, `workspace_name`, `social_account_id`, `service` (the MCP platform value), and `handle` (the returned username). Resolve these against the connected workspace and paginated account list with [trypost-mcp](../../trypost-mcp/SKILL.md). Use exact provider-returned IDs. Account identity needs the user's selection or unambiguous board/account evidence; a connection's sole account is not a default for unrelated boards. Record selection provenance in `DIRECTION.md`. Keep credentials, tokens, live connection state, capabilities, and posting schedules out of this identity file; refresh those through MCP when delivering.

Require nonempty identity fields and unique `(provider, workspace_id, social_account_id)` tuples. Validate JSON and identities before saving; preserve unrelated accounts on an addition or removal. Record unresolved requested accounts in `DIRECTION.md` rather than inventing IDs or inserting partial entries. An unavailable or malformed configuration must not silently shrink a requested target list.

Link this file from `DIRECTION.md`; editorial guidance may link to it rather than duplicating handles. Create an empty list for a new board whose targets are undecided. For a requested operational account change, update this file and its direction note in place; unchanged creative approval and visual artifacts remain valid, so the board tracker status does not change. Account-list history is independent of creative revision numbers. Existing productions retain their saved target snapshots and remote attempts under [target inheritance](../../shortform-production/references/publishing.md#target-inheritance); configuring accounts does not publish anything.

## Review and completion

At a review checkpoint, save the current artifact and set `awaiting_review`. Identify the layer and revision awaiting feedback in `DIRECTION.md`. On feedback, record the result for that layer and update the next action; keep `draft` while other required layers remain unfinished.

An approved concept alone is not an approved board package. A visual-only delivery can complete the user's current request while the reusable board remains draft pending its editorial layer. Conversely, if the user approves already-present visual and editorial work together, record that approval without splitting it into unnecessary new gates.

Creation is complete when the requested package exists, visual output has been inspected, and its status accurately reflects the approvals received. A full approved board is ready for production selection; a delivered draft is ready for review.

## Revising an approved board

Prepare substantial changes in board-local draft files and keep the approved documents available while review is pending. Leave the registry's current approved entry pointing to the usable approved version; record the pending revision in `DIRECTION.md` without representing draft content as approved.

When an accepted revision replaces an approved version, preserve the previous approved documents, visual source, exports, and required assets under `revisions/<version>/` when existing productions reference that direction. Record the new version and approval in the current documents. Board revision changes do not rewrite existing production briefs, specs, or tracker selections.

For a small correction that does not alter the agreed direction, update the affected source/spec/export consistently and describe the correction. Follow the user's requested revision scope.
