# External delivery

Read when the requested endpoint includes hosting, a draft, scheduling, publication, or reconciliation of a previous attempt. New productions use Trypost Local. The [invocation contract](invocation.md) owns delivery authorization and automation behavior.

## Target inheritance

Publishing accounts belong to the selected board in `boards/<slug>/ACCOUNTS.json`; [board account storage](../../shortform-board/references/board-files.md#publishing-accounts) defines its format. Resolve the target set in this order:

1. **Current explicit production targets:** a natural-language selection or repeated `--channel` options replace the inherited set for this production. They do not edit the board. Resolve every selector; an ambiguous selector requires clarification rather than taking the first account. Several accounts on one platform are valid targets.
2. **Saved production targets:** retain the production's `publishing_targets` snapshot, or its previously confirmed mapping/receipts, on resume. Reconcile remote attempts before changing targets or providers. Account additions to the board do not silently expand an existing production's delivery.
3. **Board targets:** for a new production, or first target resolution without saved choices/attempts, inherit every account in the selected board's list. This is the full default set, not a pool from which automation picks one. A missing/empty list or `board: null` supplies no targets; resolve an explicit selection when external delivery is requested. A malformed list is an error, not an empty fallback.

When a production is created, read the board's local account file and record `publishing_targets` in `EPISODE.md`: `source` (`board`, `override`, or `legacy`), `accounts` (the full selected identity objects), and, for board inheritance, project-root-relative `board_accounts_file` plus the file's SHA-256 as `board_accounts_sha256`. A local account snapshot may be recorded for package destination planning without remote calls. Reuse it on continuation; refreshing live connection status or account capabilities does not replace its target membership. A later explicit target change records the new selection and retains previous attempt identities. If an old production has no snapshot, preserve confirmed legacy mappings/receipts before consulting current board defaults.

An account configuration or snapshot supplies identity, not publishing authorization. Keep package-only work local; external delivery still requires `draft`, `queue`, `publish`, or another explicit delivery request. A board-level account edit updates future defaults only and does not enqueue existing episodes.

Before external writes, verify each selected account against its provider's live workspace/organization and exact ID, including returned platform/handle and connection status. An identity mismatch or unavailable account blocks that target; keep it in the requested set and report the issue rather than silently dropping it or using another account. Use the matching connection for each workspace. Account identity tuples must be unique, so duplicate selectors cannot create duplicate posts.

Prepare destination-appropriate copy, content type, required metadata, and media checks for every account. Execute one post per account and save individual results. Queue mode uses each account's own configured queue; an explicit `--at` applies the same instant to all selected accounts unless the user supplies per-account times. Preserve partial successes and complete the requested delivery only when every selected target satisfies its endpoint. Reuse an uploaded Trypost media ID only within its workspace; another workspace requires its own upload or verified URL route.

## Preflight and handoff

1. Read `EPISODE.md`, `CONTENT_PACKAGE.md`, export verification, and any `PUBLISHING.json`. Confirm the actual file and SHA-256 match the delivered version. Reuse valid outputs; a publishing-only request does not rerender or regenerate narration.
2. Resolve the full target set under target inheritance, requested delivery, each target's provider/workspace, timezone, and required service settings. Use [trypost-mcp](../../trypost-mcp/SKILL.md) for account and content-type preflight before uploading anything. Existing Buffer work follows the legacy branch below.
3. Use direct local upload through `trypost-mcp` by default, or reuse verified workspace media or a verified public URL. Use [cloudinary-mcp](../../cloudinary-mcp/SKILL.md) when public hosting is needed or requested. Save each media receipt before a post write; confirm attachment and capture returned media IDs afterward.
4. Use `trypost-mcp` to create, promote, edit, or reconcile one post per target for the requested action. Persist each successful result immediately. In automation, proceed through these steps without introducing an extra draft-review gate.
5. Summarize actual per-channel status and next action in `EPISODE.md`; link the receipt. Update only this production's root tracker row after a stage transition. Use `publishing` only once external delivery is being attempted, keeping the verified package intact.

## Receipt

`productions/<slug>/PUBLISHING.json` is the production-local source of truth for external asset and post identities. Use valid UTF-8 JSON, preserve existing attempts and unrelated targets, and reread before merging an intervening change. Paths are relative to the production. Store provider-returned values as observed; unknown optional values stay null or absent. Credentials, signed upload URLs and upload tokens belong outside this file.

The record has these fields:

| Object | Required content |
| --- | --- |
| Root | `schema_version: 2`, `assets` array, `posts` array. Create only when an external-delivery attempt starts. Version 1 receipts remain readable under the legacy branch. |
| Shared asset fields | `provider` (`trypost` or `cloudinary`), `local_file`, full `sha256`, `bytes`, `status` (`planned`, `uploaded`, `attached`, `verified`, `unknown`, `error`), `attempt_started_at`; add observed upload/attachment/verification timestamps and errors as they become available. |
| Trypost asset fields | `workspace_id`, `source` (`local_upload`, `url`, `workspace_media`); `source_url` for a public URL route; after attachment save returned `media_id` and associated `trypost_post_id`. Upload success without attachment is only `uploaded`, not a reusable media record. A verified entry links the exact export hash to its confirmed attached media. |
| Cloudinary asset fields | `public_id` planned before upload; after upload add `asset_id`, `resource_type`, `secure_url`, `uploaded_at`; after verification add `verified_at`. Reuse follows `cloudinary-mcp`. |
| Trypost post entry | `provider: trypost`, `workspace_id`, `workspace_name`, `social_account_id`, `service`, `handle`, `content_type`, `export_sha256`, `payload_sha256`, `requested_delivery`, `requested_due_at`, `attempt_started_at`, local `status`; after creation add `trypost_post_id` and returned schedule/publication details. |
| Observed Trypost result | Preserve exact provider status (`draft`, `pending_approval`, `scheduled`, `publishing`, `published`, `failed`), `scheduled_at`, `published_at`, returned media IDs, `service_url`, and error details when returned. Save a provider UI URL only if returned. Local-only `planned`/`unknown` represent writes not yet reconciled. |

Compute `payload_sha256` from a consistently serialized object containing provider/workspace/account identity, exact audience-facing text, content type, stable media source (export hash plus public URL or workspace media ID when known), service settings, requested mode, and due time. Persist that object as `payload` alongside the hash so a later run can compare the intended request. Use the export hash for a pending local upload rather than persisting a signed URL/token. The file hash identifies the export; the payload hash identifies the posting intent. Retain prior payloads/hashes when an intent changes.

Match an existing attempt first by provider, workspace, account and export hash, then reconcile its ID and payload. Also check this episode's prior deliveries across providers before creating a replacement. A changed caption or schedule updates a suitable existing unsent post; it does not bypass duplicate checks because the payload hash changed. Record revised attempts with their outcome and retain prior identities. Before retrying an unknown upload or post creation, resolve its actual remote state. If a collision cannot be distinguished reliably, stop that write path rather than creating another candidate.

Keep prior asset versions when an authorized revision changes the export hash. Preserve partial successes: a failure on the second channel does not recreate the first channel's post. A published/sent version requires an explicit new-post request before another publication of the same episode; revising a package does not imply that request.

## Existing Buffer work

The default-provider change applies to new production publishing. Preserve a resumed production's recorded provider and attempts. Use [buffer-mcp](../../buffer-mcp/SKILL.md) for explicit Buffer work and historical reconciliation. Changing the workflow does not transfer, cancel, delete, or duplicate remote drafts, scheduled posts, or published history. Moving an existing attempt requires an explicit migration request and exact target mapping; prevent an active source schedule from publishing alongside its replacement before completing that migration.

Keep existing version 1 receipts unchanged when merely reading them. Their posts are implicitly Buffer entries identified by `buffer_post_id`, with `organization_id`, `organization_name`, `channel_id`, `service`, `handle`, export/payload hashes, intent and attempt fields. Preserve their original `payload` serialization/hash, `buffer_url`, `service_url`, `scheduled_at`, `sent_at`, errors and statuses. Their asset entries are implicitly Cloudinary. Do not relabel Buffer IDs as Trypost IDs or translate historical statuses.

If an authorized new attempt adds version 2 records to an existing receipt, upgrade only the root version and append the new records; retain all legacy entries and fields. Infer a legacy record's provider from its original fields when `provider` is absent. For explicit new Buffer entries, set `provider: buffer` and use the legacy adapter's fields and payload convention.

## Completion

| Requested delivery | Evidence required for `stage: publishing`, `status: complete` |
| --- | --- |
| Draft | Every target has a saved Trypost post ID and observed `draft` status with the requested media/copy/settings. |
| Queue or specified time | Every target has observed `scheduled` status and the actual future schedule, or has already progressed to `published`. A manual reminder does not satisfy this endpoint. |
| Publish now | Every target has observed `published` status. Save social URLs when the provider returns them; an absent optional URL does not negate a `published` result. |

For Buffer, use its actual `buffer_post_id`, `sent` publication status and `sending` pending status for these same endpoint checks. Preserve `needs_approval` as its approval dependency.

`complete` refers to the requested delivery endpoint, so a completed draft or scheduling stage does not claim a live post. Trypost `pending_approval` is not a completed automatic-delivery result: report the workspace-side approval dependency rather than bypassing it. Unknown outcomes, validation failures, or missing required inputs remain unresolved and are recorded with their concrete cause. Use `blocked` when an unresolved dependency prevents progress; use `in_progress` for an accepted immediate post still `publishing` after bounded checks.

Future queued publication is verified only when the user requests a later check or separately authorizes a monitor. Scheduling completes without holding the current run open until the future date. Report the outcome accurately if another channel is still blocked or awaiting publication.
