# Content packaging

Read this guide for the `content_package` stage after verified export, or when creating or revising a package for an existing export. Store the package at `productions/<slug>/CONTENT_PACKAGE.md`.

## Establish the delivered version

Read `EPISODE.md`, the selected board's editorial and account direction, the final script, relevant sources, and the export verification. Tie the package to the actual delivered version and filenames. Use the production's audience-facing language and account voice.

Reuse the intended platforms recorded in the brief. When no platform is specified, prepare a platform-neutral package and record that assumption; ask only if destination-specific requirements materially affect completion. Adapt copy for each confirmed destination when useful, unless the selected board's editorial guidance sets a shared package: then write one title set, description, hashtag set and keyword list used unchanged for every destination, kept within the strictest destination limit. Check current official requirements through the project's research workflow before asserting platform limits or required upload fields.

## Write the package

Keep publishable copy separate from editorial notes so it can be copied directly. Include:

| Field | Content |
| --- | --- |
| Title | One recommended title and two alternatives with different hooks, faithful to the video's actual promise. |
| Description / caption | One ready-to-paste version for each confirmed destination, or one neutral version. Carry the central idea, useful context, and a CTA when it serves the board's purpose. Include source credits or disclosures where the production requires them. |
| Hashtags | A concise, relevant set aligned with topic and audience. Keep these separate from discovery keywords. |
| Tags / keywords | Topic and search phrases in a copyable comma-separated list. Identify these as editorial keywords when the destination has no dedicated tag field. |
| Cover text | A short recommendation consistent with the existing cover or opening frame. Label an unimplemented suggestion; creating or changing cover artwork follows the accepted production scope. When the board defines a thumbnail, link its PNG and record the delivered-file offset of any in-video cover frame. |
| Delivery metadata | Production slug, board/account identity when known, language, intended destination, delivered version, and relative links to video, caption files, and cover when present. Record actual video duration, dimensions/aspect ratio, format, and caption mode (burned in, sidecar, both, or none) from the file and verification evidence. |

Add a pinned comment, engagement prompt, account mentions, credits, or content notices only when supported by the content and board. Keep unknown optional upload settings explicitly unset. Publication date, timezone, visibility, audience designation, sponsorship, and rights declarations require actual production context or a user decision; do not invent them to fill a template.

Titles and descriptions must preserve the final script's claim boundaries. Keep research links traceable to `SOURCES.md` where factual context needs attribution. Avoid unsupported claims, unrelated trending tags, and promises that the video does not fulfill. Reuse known attribution or disclosure obligations from the production assets.

## Verify and deliver

Compare copy against the final script and exported content, verify metadata against the delivered file or recorded verification, and resolve every linked delivery path. If a required fact is missing, obtain or verify it before marking the stage complete; optional unresolved publishing choices can remain unset.

Record the delivered version, destination assumptions, and next action in `EPISODE.md`, then update the tracker to `stage: content_package`, `status: complete`.

After `CONTENT_PACKAGE.md` is verified, run the automatic non-blocking Google Drive archive sync under [Google Drive deliverables archive](drive-archive.md):

```bash
python .agents/skills/shortform-production/scripts/gdrive.py sync <slug> --graceful
```

Record the Drive archive outcome in `EPISODE.md` (folder URL, folder ID, synced files with MD5/action, or `not_configured` / failure + retry command). A missing configuration skips cleanly, and a Drive upload error never blocks local `content_package` completion or downstream Trypost delivery—report the failure and retry command clearly in chat.

Present the recommended title, a short package summary, and links to the verified video, package, and Drive folder (when synced) when package is the endpoint, a package review is required, or the user requests inspection. In automation continuing to external delivery, retain the copy and metadata internally and combine the package and Drive archive links with the final delivery report under [presentation and durable records](invocation.md#presentation-and-durable-records). If the run explicitly requires package review, use `awaiting_review` until that review is resolved. This stage adds no standing approval checkpoint. Preparing the package alone does not authorize uploading, scheduling, or publishing; when the run already requests external delivery under the [invocation contract](invocation.md), continue to [publishing](publishing.md) without another intake or permission question.

For revisions, refresh only affected copy and metadata. A changed export requires checking the package against the new version; a metadata-only revision reuses valid video and audio artifacts.
