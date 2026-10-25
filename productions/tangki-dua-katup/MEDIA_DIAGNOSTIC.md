# Draft media diagnosis and recovery — 2026-10-25

## Confirmed cause

The existing Trypost post `01a172da-a2ef-7179-a14f-f5828338b158` is still a draft for Instagram @dibalikbenda.id in Admin's Workspace. Its 697-character caption is intact and the preview tool reports no truncation. The post references media `01a172da-764e-7098-9f4f-bef64eaeb2e9` at `medias/94f8a6cd-5fea-410b-81cc-0e962c20a4b6.mp4`.

Public full and Range requests both returned HTTP 404. The local web listener on port 8000 also returned 404 for the same media path. The website and account avatar were accessible. This isolates the failure beyond the initial client-specific 403.

The running local Docker container is `trypost`. Its named volume `trypost-local_storage` is mounted at `/var/www/html/storage/app`. The `public/storage` symlink resolves correctly to `/var/www/html/storage/app/public`.

The media file does not exist on disk. Directory `/var/www/html/storage/app/public/medias` has owner/group root:root and mode 0755. PHP-FPM request workers run as www-data; `docker exec --user www-data trypost test -w /var/www/html/storage/app/public/medias` returns exit 1. The parent public directory and the working social-account image directory belong to www-data:www-data.

The installed `app/Models/Traits/HasMedia.php` calls `Storage::writeStream` without checking its return value, then creates the media row with the intended path and measured metadata. The installed public disk uses `throw: false` and `report: false`. Laravel's current filesystem documentation confirms that failed writes can return false without throwing. This explains the upload HTTP 201 and valid-looking media row despite the missing file.

## Recovery scope

Repair only the ownership of the media directory (root:root -> www-data:www-data; retain mode 0755). Restore the exact verified local v1 file to the already referenced missing media path as www-data. Check absence before writing and refuse to overwrite an existing file. Preserve post ID, media ID, caption, metadata and draft status. Do not modify application source, database records, existing media files, or publication state.

The local source must have 16,237,215 bytes and SHA-256 `5632b1f013288fb6fa2136d3e997791e5d1fa067e8b0b2089381a9b5b0560e6d`. Verify the restored file and public full download against the same SHA-256, and test a public byte-range request for video playback.

## Recovery result

Recovery completed at 2026-10-25 11:45 UTC (18:45 Asia/Jakarta).

- Changed only the media directory owner/group to www-data:www-data, retaining 0755. The www-data write-access check now passes.
- Streamed the verified local export into the missing target file using the container's www-data user, with shell noclobber enabled. The restored file is www-data:www-data, mode 0644, 16,237,215 bytes.
- Container `sha256sum` matches the verified export hash.
- Public download of the original media URL returned HTTP 200, Content-Type video/mp4, Accept-Ranges bytes, and all 16,237,215 bytes. Its SHA-256 matches the export exactly.
- Public `Range: bytes=0-1023` request returned HTTP 206 with `Content-Range: bytes 0-1023/16237215`. All 1,024 bytes match the local file prefix.
- Separate MCP get_post confirmed the original post ID, original media ID, draft status, unchanged caption, and null scheduled_at/published_at.

The missing-video incident is resolved. This verifies stored-file integrity and HTTP delivery; it does not claim a new audiovisual listening review or an actual Instagram publication. The upload writer's unchecked failure remains an observed application behavior; no source changes were made as part of this focused recovery. Detailed results and historical failures are retained in PUBLISHING.json.
