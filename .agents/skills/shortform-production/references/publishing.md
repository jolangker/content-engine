# External delivery

Read when the requested endpoint includes hosting, a Buffer draft, scheduling, publication, or reconciliation of a previous attempt. The [invocation contract](invocation.md) owns delivery authorization and automation behavior.

## Preflight and handoff

1. Read `EPISODE.md`, `CONTENT_PACKAGE.md`, export verification, and any `PUBLISHING.json`. Confirm the actual file and SHA-256 match the delivered version. Reuse valid outputs; a publishing-only request does not rerender or regenerate narration.
2. Resolve the requested delivery, organization, target accounts, timezone, and required service settings. Use [buffer-mcp](../../buffer-mcp/SKILL.md) for account discovery and channel preflight before uploading anything. Account identity is per board/production; a handle found in another episode is not a universal default.
3. Use [cloudinary-mcp](../../cloudinary-mcp/SKILL.md) to reuse or upload the verified file and obtain its stable direct URL. Save its receipt before passing it to Buffer.
4. Use `buffer-mcp` to create, promote, edit, or reconcile one post per target for the requested action. Persist each successful result immediately. In automation, proceed through these steps without introducing an extra draft-review gate.
5. Summarize actual per-channel status and next action in `EPISODE.md`; link the receipt. Update only this production's root tracker row after a stage transition. Use `publishing` only once external delivery is being attempted, keeping the verified package intact.

## Receipt

`productions/<slug>/PUBLISHING.json` is the production-local source of truth for external asset and post identities. Use valid UTF-8 JSON, preserve existing attempts and unrelated targets, and reread before merging an intervening change. Paths are relative to the production. Store provider-returned values as observed; unknown optional values stay null or absent. Credentials and upload signatures belong outside this file.

The record has these fields:

| Object | Required content |
| --- | --- |
| Root | `schema_version: 1`, `assets` array, `posts` array. Create only when an external-delivery attempt starts. |
| Asset entry | `local_file`, full `sha256`, `bytes`, `public_id` (planned before upload), `status` (`planned`, `uploaded`, `verified`, `unknown`, `error`), `attempt_started_at`; after upload add `asset_id`, `resource_type`, `secure_url`, `uploaded_at`, and after verification `verified_at`. |
| Post entry | `organization_id`, `organization_name`, `channel_id`, `service`, `handle`, `export_sha256`, `payload_sha256`, `requested_delivery`, `requested_due_at`, `attempt_started_at`, local `status`; after creation add `buffer_post_id` and returned schedule/publication details. |
| Observed post result | Preserve provider status (`draft`, `needs_approval`, `scheduled`, `sending`, `sent`, `error`), `scheduled_at`, `sent_at`, `buffer_url`, `service_url`, and error details when returned. Local-only `planned`/`unknown` represent writes not yet reconciled. |

Compute `payload_sha256` from a consistently serialized object containing channel ID, exact audience-facing text, media URL, service settings, requested mode, and due time. Persist that object as `payload` alongside the hash so a later run can compare the intended request. It contains no credentials. The file hash identifies the export; the payload hash identifies the posting intent.

Match an existing attempt first by organization, channel, and export hash, then reconcile its ID and payload. A changed caption or schedule updates a suitable existing unsent post; it does not bypass duplicate checks because the payload hash changed. Record revised attempts with their outcome and retain prior identities. Before retrying an unknown upload or post creation, resolve its actual remote state. If a collision cannot be distinguished reliably, stop that write path rather than creating another candidate.

Keep prior asset versions when an authorized revision changes the export hash. Preserve partial successes: a failure on the second channel does not recreate the first channel's post. A sent version requires an explicit new-post request before another publication of the same episode; revising a package does not imply that request.

## Completion

| Requested delivery | Evidence required for `stage: publishing`, `status: complete` |
| --- | --- |
| Draft | Every target has a saved Buffer post ID and observed `draft` status with the requested media/copy/settings. |
| Queue or specified time | Every target has observed `scheduled` status and the actual future schedule, or has already progressed to `sent`. A manual reminder does not satisfy this endpoint. |
| Publish now | Every target has observed `sent` status. Save social URLs when the provider returns them; an absent optional URL does not negate a `sent` result. |

`complete` refers to that requested delivery endpoint, so a completed draft or scheduling stage does not claim a live post. An unexpected `needs_approval` is not a completed automatic-delivery result: report the Buffer-side approval dependency rather than bypassing it. Unknown outcomes, validation failures, or missing required inputs remain unresolved and are recorded with their concrete cause. Use `blocked` when an unresolved dependency prevents progress; use `in_progress` for an accepted immediate post still `sending` after bounded checks.

Future queued publication is verified only when the user requests a later check or separately authorizes a monitor. Scheduling completes without holding the current run open until the future date. Report the outcome accurately if another channel is still blocked or sending.
