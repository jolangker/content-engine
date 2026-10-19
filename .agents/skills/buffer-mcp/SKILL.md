---
name: buffer-mcp
description: Create or revise Buffer drafts, queue or publish verified media, and reconcile posting status through Buffer MCP. Use for a shortform-production publishing handoff or direct Buffer requests, including interrupted attempts and duplicate prevention.
---

# Buffer MCP

Deliver the requested version to the requested accounts and record the actual result. The caller supplies the delivery intent; a connected account is not an account-selection rule.

## Resolve scope and channels

1. Read the requested endpoint, copy, media receipt, and any previous posting attempt. For a short-form production, follow [publishing](../shortform-production/references/publishing.md) for receipt fields and stage completion. Preserve the caller's review policy: an authorized automated delivery proceeds without adding a draft-review pause.
2. Inspect current Buffer tool schemas. Use `get_account` to obtain organizations and time context, then reuse that data within the session. Select the organization using an explicit choice or an unambiguous recorded mapping, and tell the user its name. Resolve unknown channel IDs with `list_channels`; retain the exact returned IDs.
3. Match each target against the requested service and handle or a verified board/account mapping. Use `get_channel` for missing capabilities, connection state, or queue schedule. A sole connected account does not establish that it belongs to the selected board. Resolve ambiguous identity before writing; in an automated run, record the blocker and finish independent work.

Done when each target is an exact connected channel in the selected organization and the requested action is explicit. Account details and limits come from current responses, not hardcoded handles or plan quotas.

## Prepare the post

- Use the verified direct media URL. Buffer accepts a hosted URL rather than local bytes; [cloudinary-mcp](../cloudinary-mcp/SKILL.md) owns uploading a local export. Keep source media available through publication, including future scheduled posts.
- Take audience-facing copy from the verified content package. Preserve source attribution and claim boundaries when adapting to platform limits; fetch current requirements through Context7 or the project's research workflow when needed.
- For video, use the tool's `assets` shape: `[{"video":{"url":"<verified-url>"}}]`. Choose a cover frame with `video.metadata.thumbnailOffset` in milliseconds only when supported and within the actual duration. A separate video thumbnail URL is not a general substitute.
- Instagram Reels require `metadata.instagram.type: reel` and an explicit `shouldShareToFeed` decision. YouTube requires `metadata.youtube.title` and `categoryId`. Resolve other required fields from current schema, channel data, and the production brief. Audience, rights, AI, and commercial declarations must reflect known provenance and current platform rules; optional unknown fields can stay unset. An unsupported required declaration is a blocker, not permission to omit it.

## Execute the requested action

Use `schedulingType: automatic` for actual automatic publication. `notification` is a manual-post reminder and does not fulfill an automatic publishing request.

| Requested result | `create_post` arguments |
| --- | --- |
| Draft | `saveToDraft: true`, `mode: addToQueue` |
| Next configured queue slot | `saveToDraft: false`, `mode: addToQueue` |
| Specified future time | `saveToDraft: false`, `mode: customScheduled`, `dueAt` |
| Publish now | `saveToDraft: false`, `mode: shareNow` |

Resolve relative dates in the confirmed posting timezone with its UTC offset and compare against fresh current time. Report a mismatch between the user's requested timezone and the account timezone. A `dueAt` must be in the future; a missing queue schedule needs a resolved time rather than an invented slot. If the caller requests multiple channels, make and record one post per channel; preserve partial successes.

Before each write, reconcile any recorded post ID with `get_post`. Before an unrecorded or interrupted creation, inspect a narrowly filtered `list_posts` result for the channel, relevant statuses, and attempt window; paginate enough to establish whether the attempt landed. Compare text, asset URL, settings, and timing. Persist the planned payload fingerprint and attempt time before creating, then save the returned post ID and status immediately.

Reuse an already matching result. Promote an existing draft with the current tool's supported draft/edit path; a changed caption or schedule normally updates an existing unsent post. A sent post is not silently duplicated by a rerun or replaced by a new version. Resolve an ambiguous candidate before writing.

## Verify and resume

- Treat the successful write response as evidence of saved content and settings; read again only for an unresolved or asynchronous status. `sending` means pending, `scheduled` means scheduled, and `sent` is evidence of publication. Save returned social URLs when available; never construct one from an assumed ID.
- Reconcile a timed-out write before retrying. Correct a definite rejected request and retry at most once; if acceptance cannot be established, preserve `unknown` locally and stop that write path. Inspect MCP error flags and error bodies even when transport succeeded.
- Respect reported rate-limit windows and `Retry-After`. Do not poll a future scheduled post until its publication time. For publish-now, use bounded status checks; if still sending, return the pending receipt and next status-check action rather than claiming publication.
- Complete only the caller's requested endpoint. Draft or queue creation can finish its delivery stage without the post being live. Report per-channel successes, failures, and pending results accurately.

## Sources

- [Official Buffer MCP](https://developers.buffer.com/guides/integrations/mcp.html)
- [Hosting media](https://developers.buffer.com/guides/hosting-media.html)
- [Efficient API usage](https://developers.buffer.com/guides/efficient-api-usage.html)

Prefer current tool schemas for argument names and available actions. Use Context7 for missing Buffer API details.
