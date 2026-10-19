---
name: cloudinary-mcp
description: Upload local production exports through Cloudinary MCP, verify public media URLs, and reuse recorded assets. Use when shortform-production needs hosted media for Buffer or when the user requests Cloudinary asset operations.
---

# Cloudinary MCP

Turn an existing verified file into a stable media URL. Cloudinary owns hosting; the caller owns which file and version may be uploaded.

## Resolve the asset

1. Read the caller's file, export verification, and existing asset receipt. For a short-form production, use the receipt contract in [publishing](../shortform-production/references/publishing.md). Compute the current file's SHA-256 and byte size; reconcile a mismatch with the verified export before uploading.
2. Discover the available Cloudinary tools and inspect their current schemas. A visible namespace alone does not prove authentication. Use a narrow `search_assets` query for the recorded public ID or intended asset to verify access and find an existing upload.
3. Reuse an asset only when its receipt identifies this file hash and its remote details agree. Otherwise choose a versioned public ID, such as `content-pipeline/<slug>/<full-sha256>`, and set `overwrite: false`. A collision without trustworthy provenance requires inspection, not replacement.

Done when the exact local file and a reusable remote asset or a collision-safe upload target are identified. For an unconnected MCP, report the connection blocker; use an existing local API configuration only when that fallback is within the requested scope.

## Upload a local file

For a local file up to 100 MB, use `sign_upload`; the remote `upload_asset` tool cannot read a local filesystem path.

1. Sign one upload with the chosen `public_id`, `overwrite: false`, delivery `type: upload`, and only needed organization fields such as tags or asset folder. For a delivery handoff, retain the original file without eager or incoming transformations.
2. Read the returned `host`, `cloud_name`, `api_key`, `signature`, and `upload_params`. POST multipart/form-data from the local environment to `https://<host>/v1_1/<cloud_name>/video/upload` for a video, or the appropriate image/raw resource endpoint.
3. Include the file bytes, `api_key`, `signature`, and **every returned `upload_params` field verbatim**. Keep signed serialized values unchanged; `resource_type` belongs in the URL. Use structured HTTP/multipart arguments or properly quoted arguments, including paths with spaces. Keep signing credentials in memory or a temporary file outside the repository and remove that file afterward; receipts contain only asset metadata.
4. Inspect both HTTP status and the response body. Capture the immutable `asset_id`, `public_id`, resource type, original `secure_url`, bytes, dimensions, duration when supplied, and upload time. Persist the receipt immediately before another external action.

For larger files, use the provider's documented chunked uploader through an authorized local SDK/CLI path. Fetch current Cloudinary documentation through Context7 before implementing that path. For an already hosted source, `upload_asset` accepts supported remote URLs; inspect its schema and set `overwrite: false` there too.

An upload timeout has an unknown outcome. Search the exact intended public ID and inspect its metadata before retrying. Retry once only after establishing that the previous upload did not succeed; an unresolved result remains a recorded blocker.

## Verify and hand off

- Request the original HTTPS media URL without authentication. Confirm it serves the file rather than a preview/login page, has the expected media type and byte size, and is stable through the requested posting time. A denied HEAD request needs a small GET/range probe before declaring failure.
- For an original-file handoff, stream a download to compute its hash when practical; reuse the download for verification rather than triggering redundant full transfers. Reconcile a different hash before claiming the hosted asset is the verified original.
- Supply the URL and receipt to the caller. Buffer posting belongs to [buffer-mcp](../buffer-mcp/SKILL.md); hosting alone does not schedule anything.
- Retain the asset while a dependent post is a draft, queued, sending, or unresolved. Cleanup, deletion, overwrite, or transformations need their own requested scope; automation is not a cleanup policy.

Done means the receipt identifies the exact source version and the verified direct URL. Report a hosting error as a hosting error rather than marking publication complete.

## Sources

- [Official Cloudinary MCP](https://cloudinary.com/documentation/cloudinary_llm_mcp)
- [Upload signatures](https://cloudinary.com/documentation/authentication_signatures)

Prefer the connected tool schema for tool arguments. Consult current official documentation through Context7 for missing API details instead of copying historical examples.
