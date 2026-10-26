---
name: trypost-mcp
description: Create or revise Trypost Local drafts, queue or publish verified media, and reconcile posting status through Trypost MCP. Use for new shortform-production publishing handoffs or direct Trypost requests, including local uploads and interrupted attempts.
---

# Trypost Local MCP

Deliver the requested version to the requested accounts through the configured Trypost MCP connection. The caller owns delivery intent and review policy. For production receipts and endpoint completion, follow [publishing](../shortform-production/references/publishing.md).

## Resolve workspace and accounts

1. Read the requested endpoint, verified media/copy, and prior delivery attempts. Inspect current MCP schemas; prefer them over examples from older REST documentation.
2. Call `get_workspace_tool` to identify the connection's workspace and `me.requires_approval` / `me.publishes_directly`. Tell the user the workspace name. The connection acts in that workspace; a different requested workspace needs its matching connection.
3. Resolve the complete selected account set under [target inheritance](../shortform-production/references/publishing.md#target-inheritance), then verify exact account IDs using `list_social_accounts_tool`, following pagination. New productions inherit every account from their board's `ACCOUNTS.json` unless explicitly overridden; direct requests without a board resolve their supplied targets. Match each platform/handle and workspace identity, and check connection status. A sole connected account is not an identity mapping for every board.
4. Call `list_content_types_tool` before selecting `content_type` or attaching media. Apply current network limits, required metadata, and the account's text limit. Use `get_posting_schedule_tool` when queue/timezone details are needed.

Done when the workspace, exact connected accounts, action, content type, required settings, and media route are resolved. Missing or ambiguous identity blocks that target; finish independent work under the caller's review policy.

## Prepare media and copy

Use the verified export's actual SHA-256, bytes, duration and dimensions. Keep audience-facing copy and source attribution consistent with the content package. For a short-form Instagram reel, select the currently returned `instagram_reel` type. Resolve feed-sharing, covers and other optional choices from the accepted brief and current supported schema; retain an unsupported requested setting as a concrete unresolved requirement.

Choose one media route:

- **Local file (default):** Call `request_media_upload_tool`, then POST multipart/form-data to its signed `upload_url` using the returned `field_name` (currently `media`). Respect returned expiry and byte ceilings as well as the content type's stricter limits. Check both HTTP status and response body. Pass the resulting `upload_token` to `create_post_tool` or `update_post_tool` in `media: [{"upload_token":"..."}]`, or attach it to an existing draft with `attach_media_from_upload_tool`. A local path cannot replace this upload.
- **Existing hosted file:** Reuse a verified direct public URL with `media: [{"url":"..."}]`. Trypost downloads its own copy. Its URL-attachment tool rejects redirects and private-network sources and reports individual `failed_urls`; transport success alone does not prove attachment.
- **Existing workspace media:** Reuse the exact returned media ID with `media: [{"id":"..."}]` after verifying provenance against the export receipt.

An upload token is single-use and unused uploads expire after 24 hours. After its first attachment, record the post's returned media ID; reuse that ID for another account's post in the same workspace rather than spending the token twice. Another workspace requires a separate upload or verified public URL route. Keep signed URLs/tokens outside durable receipts and logs. Record upload outcome and attachment outcome separately. After a timeout, reconcile the post's media and recorded post ID before creating another post or attaching a duplicate. If an unused upload cannot be reconciled, abandon that temporary upload and request a fresh one only after establishing that no post creation is unresolved.

Publication depends on the Trypost deployment's media delivery and workers. For URL-pull networks such as Instagram, verify that Trypost's served copy is publicly reachable; upload success or a reachable source URL alone does not establish publication readiness. Report actual delivery errors and identify the required deployment correction before retrying.

## Execute the requested action

Use `create_post_tool` for one account, with exact `social_account_id`, `content`, `content_type`, media and supported `meta`. Record each account's result before proceeding to the next.

| Requested result | Creation fields |
| --- | --- |
| Draft | `status: draft` |
| Next configured queue slot | `status: scheduled`, `queue: next` |
| Specified future time | `status: scheduled`, `scheduled_at` with explicit UTC offset or `Z` |
| Publish now | `status: publishing` |

`queue: top` shifts existing queued posts; use it only when the user requests that behavior. Queue delivery requires configured posting times. Use custom `scheduled_at` instead of queue fields when a time was supplied; never combine them. Resolve relative dates with fresh time and the target timezone, then save both the requested offset-aware time and the returned UTC schedule. Trypost response timestamps without an offset are UTC. A missing schedule requires a resolved time, not an invented slot.

Before writing, reconcile saved post IDs using `get_post_tool`. For an unrecorded/interrupted creation, use narrowly filtered `list_posts_tool` results for the account, status and content, paging through relevant candidates and comparing media, settings, timing and attempt window. Persist the planned payload and fingerprint before creation, then save the returned post ID and status immediately. Reuse a matching result. Update an existing unsent post with `update_post_tool`, or promote its draft with `publish_post_tool`; inspect the current schema for custom-time or queue fields. Publishing, published and failed posts cannot be edited under the current tool contract. A published version needs an explicit new-post request before another publication.

Preserve historical deliveries under the publishing contract's [historical receipt rule](../shortform-production/references/publishing.md#historical-receipts) before creating a replacement.

## Verify and resume

- Inspect MCP error flags and response bodies, including partial media failures. A successful write establishes saved settings; read again for unresolved asynchronous status or media identity/provenance.
- Preserve returned status: `publishing` is pending, `scheduled` is scheduled, and `published` establishes publication. Save actual `published_at`, social URLs and errors when supplied; never construct a social URL from an assumed ID.
- `pending_approval` is a Trypost workspace dependency, not completed automatic delivery. Report it and the required approver action; the production's automation flag does not bypass workspace permissions.
- Reconcile timed-out writes before retrying. Correct a definite rejection and retry once; acceptance that cannot be established remains `unknown` and stops that write path. Retain partial successes.
- Respect reported rate limits. For publish-now, use bounded status checks and return the pending receipt if it stays `publishing`. For future scheduled posts, stop after schedule verification; monitor only on a separate request or authorized monitoring policy.

## Sources

- [Trypost official source](https://github.com/trypost-it/trypost)
- Current connected MCP tool descriptions and `list_content_types_tool` govern supported arguments and limits. Use Context7 for missing documentation; older REST examples may have a different multi-platform payload than the current single-account MCP tools.
