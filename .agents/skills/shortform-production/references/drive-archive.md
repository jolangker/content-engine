# Google Drive deliverables archive

Read when archiving verified deliverables at the end of `content_package`, configuring Google Drive credentials, running a manual retry or backfill, or managing Cloudflare R2 retention alongside Trypost.

## Hybrid role (Drive archive vs. Trypost/R2 staging)

- **Google Drive (permanent archive):** stores one clean copy of each production's deliverables (`exports/*` plus `CONTENT_PACKAGE.md`) in a private folder under the user's personal My Drive.
- **Trypost + Cloudflare R2 (temporary publishing staging):** Trypost copies uploaded media per post/account internally on R2 even when a workspace media ID is reused, and its URL attachment route downloads into R2 while rejecting HTTP redirects. Keep Trypost/R2 solely as staging for queuing and publishing, and rely on Google Drive as the durable single-copy archive.

## Folder layout and files

```text
<GOOGLE_DRIVE_ROOT_FOLDER_ID>/
  <board-slug>/                  # or _standalone/ when board is null
    <production-slug>/
      <production-slug>.mp4      # all non-hidden files from exports/
      thumbnail.png
      <production-slug>.srt
      CONTENT_PACKAGE.md
```

- Files sit flat inside `<production-slug>/` for quick download from desktop or mobile.
- Folder and file permissions remain private to the owning Google account.
- Sync is **idempotent and in-place**: [gdrive.py](../scripts/gdrive.py) compares local MD5 against Drive's `md5Checksum`. Unchanged files are skipped; modified files are updated in-place via resumable `PATCH` (preserving file IDs, URLs, and Drive's built-in version history); new files are created via resumable `POST`.

## Environment resolution (Doppler primary, `.env` fallback)

All workspace API scripts ([narration.py](../scripts/narration.py), [trypost.py](../scripts/trypost.py), and [gdrive.py](../scripts/gdrive.py)) load credentials through [env_loader.py](../scripts/env_loader.py):

1. **Doppler REST API (primary, in-memory):** when `DOPPLER_TOKEN` is set in the environment (or bootstrapped in `.env`), secrets are fetched directly from `https://api.doppler.com/v3/configs/config/secrets/download?format=json` without invoking the `doppler` CLI. If both `DOPPLER_PROJECT` and `DOPPLER_CONFIG` are set (for personal or service-account tokens), they are forwarded automatically; scoped Service Tokens omit both.
2. **Project root `.env` (per-key fallback):** Doppler values always win per key; any key absent from Doppler falls back to root `.env`. If `DOPPLER_TOKEN` is unset or the Doppler API is unreachable, all keys fall back to `.env`.
3. Ordinary non-Doppler shell environment variables are ignored, and no script ever prints credentials or tokens.

## Pipeline hook (`content_package`)

At the end of `content_package` (after `CONTENT_PACKAGE.md` and export verification succeed, whether the endpoint is `--delivery=package` or continues to Trypost):

```bash
python .agents/skills/shortform-production/scripts/gdrive.py sync <slug> --graceful
```

Handle the outcome non-blockingly:

- **`status: "ok"`:** record a concise **Google Drive archive** summary in `EPISODE.md` (folder URL, folder ID, `remote_path`, synced timestamp, and synced file names with MD5/action). Include the clickable folder URL in the user handoff.
- **`status: "not_configured"`:** skip silently (`drive_archive: not_configured` in `EPISODE.md`). Do not block `content_package` or Trypost delivery.
- **Error (exit code 1):** keep local `content_package` as `complete` and do not block downstream Trypost delivery. Record `drive_archive: failed`, the error summary, and the one-line retry command (`python .agents/skills/shortform-production/scripts/gdrive.py sync <slug>`) in `EPISODE.md`, and report the failure clearly in chat.

Do not create a separate local JSON receipt file and do not modify `TRACKER.json` or `PUBLISHING.json` schemas for Drive archive state.

## CLI commands and backfill

```bash
# 1. One-time OAuth 2.0 browser flow to obtain GOOGLE_REFRESH_TOKEN
python .agents/skills/shortform-production/scripts/gdrive.py auth

# 2. Verify OAuth token and root folder access
python .agents/skills/shortform-production/scripts/gdrive.py check

# 3. Sync one production (add --dry-run to preview without writing)
python .agents/skills/shortform-production/scripts/gdrive.py sync <slug>

# 4. Backfill all TRACKER.json productions that still have local exports/
python .agents/skills/shortform-production/scripts/gdrive.py sync-all --dry-run
python .agents/skills/shortform-production/scripts/gdrive.py sync-all
```

`sync-all` automatically skips productions without local files in `exports/` and skips files whose MD5 already matches Drive. Use `--board <slug>` to scope a backfill to one board.

## One-time OAuth 2.0 setup (personal Gmail / My Drive)

Service Accounts cannot upload new files to a personal Gmail My Drive (`storageQuotaExceeded`), so personal accounts use OAuth 2.0:

1. In Google Cloud Console, create or select a project and enable the **Google Drive API**.
2. Configure the **OAuth consent screen** (External), add your Gmail account as a test user, and **publish the app to "In Production"** so refresh tokens do not expire after 7 days (you do not need Google verification for personal use—click *Advanced → Go to <app>* once during `gdrive.py auth`).
3. Create an **OAuth client ID** of type **Desktop app** to obtain `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` (shared across Google APIs in the same GCP project).
4. Create a private root folder in Google Drive (for example, `Content Engine Deliverables`) and copy its folder ID from the URL (`https://drive.google.com/drive/folders/<GOOGLE_DRIVE_ROOT_FOLDER_ID>`).
5. Store `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `GOOGLE_DRIVE_ROOT_FOLDER_ID` in Doppler (or `.env`), then run `python .agents/skills/shortform-production/scripts/gdrive.py auth`. The helper requests the `https://www.googleapis.com/auth/drive` scope so it can read and write inside your manually created root folder.
6. Save the printed `GOOGLE_REFRESH_TOKEN` in Doppler (primary) or `.env` (fallback) and verify with `python .agents/skills/shortform-production/scripts/gdrive.py check`.

## Cloudflare R2 lifecycle recommendation

Because Trypost duplicates uploaded videos per post on its R2 bucket while permanent deliverables now live in Google Drive, configure an **Object Lifecycle Rule** on Trypost's Cloudflare R2 bucket to expire old media automatically:

1. Open Cloudflare Dashboard → **R2 Object Storage** → select Trypost's bucket → **Settings** → **Object lifecycle rules**.
2. Add a rule (for example, `expire-trypost-staging-30d`) with action **Delete uploaded objects after `30` days** (choose a retention window safely longer than your furthest scheduled queue slot).
3. Keep the bucket scoped to Trypost's media prefix if the bucket is shared with non-Trypost assets.
