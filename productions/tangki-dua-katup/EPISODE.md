# Tangki dua katup

- Board: [Di Balik Benda v4](../../boards/di-balik-benda/DIRECTION.md), [editorial](../../boards/di-balik-benda/EDITORIAL.md), [canonical frame](../../boards/di-balik-benda/frame.md).
- topic_selection: auto; explicitly delegated by --topic=auto.
- Selected angle: gravity toilet cistern with lever, chain, hinged buoyant flapper and cup-float fill valve; why it releases water and then stops refilling.
- Endpoint: publishing, delivery draft; 90 seconds, 1080x1920, 30fps, Indonesian. The 2026-10-25 continuation request extends the previous export-only cap.
- execution_policy: automation
- automation_after: none
- automation_state: active
- human_review: none
- pre_render_authorization: delegated by the user's --automation instruction
- human_approval: false
- Topic and hook decisions: agent-selected under delegation, not human approvals.
- Delivery: Trypost Local Instagram Reel draft for @dibalikbenda.id in Admin's Workspace, explicitly requested by the user on 2026-10-25. Reuse verified v1 and retain active automation.
- Static storyboard artifacts remain mandatory despite storyboard:no; agent layout verification replaces the human checkpoint.

## Topic selection

Ten candidates presented before file creation: toilet cistern, stapler, seat-belt retractor, crank pencil sharpener, bicycle freehub, automatic kettle, retractable tape measure, hydraulic door closer, geared hand whisk, windscreen wiper. Toilet cistern selected for visible linked mechanical and flow interactions, evidence availability, and a coherent 90-second tank-only boundary. Others remain unselected research candidates.

Overlap check: tracker topics cover lockstitch, cylinder lock, trigger sprayer, relationships, rainwater harvesting and rail load transfer. Unregistered `productions/roda-beda-putaran/` contains video/exports without EPISODE.md; avoid differential topic and preserve it. The new tank topic does not repeat the bottle pump's piston/check-valve mechanism.

## Hook decision before script drafting

1. “Sekali tekan, air keluar. Tapi siapa yang tahu kapan tangkinya sudah penuh?” Curiosity about the stop signal; promised answer is float control. Recommended and selected.
2. “Di dalam tangki kloset, katup pembuang dan katup pengisi punya tugas berbeda.” Parts-first distinction; promises two functional paths.
3. “Tuasnya sudah dilepas. Kenapa tangki masih bisa menyelesaikan siklusnya?” Follow the autonomous cycle after user input.

Selected option 1 under active automation, after source discovery. It states a question rather than implying electronics or a timer. Script drafting follows this decision.

## State

Verified v1 export is retained. The requested continuation through Trypost draft delivery is complete. The missing public video was diagnosed and recovered; full public download and byte-range serving now pass. See the draft receipt and recovery record below. No preview server is retained.

## Static storyboard verification

16/16 styled composition stills inspected in scene order; `video/boards/storyboard.html` and complete `video/boards/storyboard.png` (1920×4035) exist. Browser verified 16 correct ordered images with nonzero dimensions. Initial SVG overflow into titles was repaired with a visual crop; every final still was recaptured and PNG inspected. Whole assembly, controlled section, lever/chain, flapper contact, float, refill and overflow macros vary scale and explanatory task. Board fonts, semantic colors, shaded side faces and assembly landmarks retained. Agent-verified under delegated authorization, not human approval.

## Narration request

Provider ElevenLabs, model eleven_v4, voice 3mAVBNEqop5UbHtD8oxQ resolved from root `.env` ELEVENLABS_VOICE_ID; one tagged full-script input. No inherited shell or prior-production voice selection. BGM intentionally absent; material and water interaction cues are required and frozen separately.

## Preview and delegated render authorization

Final CLI check passed with zero errors and zero warnings in lint/runtime/layout/motion/contrast/craft; 80 informational entries are intentional cropped SVG geometry. 1,616 per-scene motion samples passed constant-chain-length and reverse-seek consistency. Final framework snapshots inspected for all16 scenes, caption safe area, flapper contact, float movement, below-seat overflow and visual rhythm. Static board repaired and recaptured after topology and label-anchor corrections.

Preview project: C:/Users/muhth/Documents/projects/content-pipeline/productions/tangki-dua-katup/video; created by this run, PID28056, port3002, http://127.0.0.1:3002/#project/video, HTTP200 verified. Retention: through render/export verification only; stop with project CLI preview --stop and verify listener release. No inherited preview existed.

Human approval false; agent-verification and pre-render authorization delegated by explicit --automation. Export versionv1, 90s, original-speed voice78.72s plus10.48s distributed observation pauses; one normalized placed narration89.2s at0.3s. Sound plan31 cues from6 frozen assets; no BGM. Direct perceptual listening unavailable, no claim of full-speed auditory or phone-speaker assessment. Technical waveform and export verification follow.

## Export complete

Verified version v1

- Board: Di Balik Benda v4; original layered 2.5D SVG, Indonesian, 16 explanatory shots.
- Export: [MP4](exports/tangki-dua-katup-v1.mp4), 90.0 seconds, 1080×1920,30fps,2700 frames,H.264/AAC,16,237,215 bytes.
- SHA-256: `5632b1f013288fb6fa2136d3e997791e5d1fa067e8b0b2089381a9b5b0560e6d`.
- Captions: burned in plus [SRT](exports/tangki-dua-katup.srt) and [VTT](exports/tangki-dua-katup.vtt);167 aligned spoken words, no delivery tags.
- Full file decoding passed; measured loudness -15.26 LUFS and true peak -1.82 dBTP. Six narration waveform windows passed.
- All31 placed SFX verified in actual MP4 with waveform matching, including expected onsets; sources and treatment in video/SFX_SOURCES.md.
- Framework check: zero errors and warnings in lint,runtime,layout,motion,contrast and craft. Informational cropped SVG bounds are intentional macro framing.
- Motion:1,616 samples across16 scenes, constant illustrative chain length and reverse-seek consistency passed. Representative final rendered frames inspected for every scene plus contact macros.
- Static storyboard: [HTML](video/boards/storyboard.html) and [PNG](video/boards/storyboard.png),16 ordered frames,1920×4035. Original pre-audio planning timing is retained; final measured timing is in video/timing.json and STORYBOARD.md. Repaired topology and moving-label anchors are included in both storyboard and film.
- Preview: pipeline-owned server PID28056,port3002,HTTP200 verified while held for render; stopped after export verification and listener release verified.
- Authorization: explicit --automation delegates agent verification and final render. Human approval is false. Endpoint --until=export reached; no content package,hosting or publication executed.


Historical export-only endpoint was reached. Preview cleanup was verified. See VERIFIED.md and video/verification/ for evidence and listening limits.

## Draft delivery continuation — 2026-10-25

User request: "lanjut produksi tangki-dua-katup sampai ke delivery draft". This explicitly replaces the former export-only endpoint with publishing/draft and authorizes the required local media upload and draft creation. Active automation persists; human approval remains false. Existing v1 export hash and byte count were rechecked and match VERIFIED.md. No film or narration changes are needed.

The board account file is the first target resolution: no prior saved targets or delivery attempts exist for this production. Live MCP confirms the exact workspace and connected Instagram account. Workspace me.requires_approval=false and me.publishes_directly=true. One page contains the complete one-account set. A full-status post search for "tangki" on this account returned zero results before the attempt.

publishing_targets:
```json
{
  "source": "board",
  "board_accounts_file": "boards/di-balik-benda/ACCOUNTS.json",
  "board_accounts_sha256": "b975f156df5c9c6bb0ac33f940b2cef5191793fd2c659a027a4e75291dcc25f3",
  "accounts": [
    {
      "provider": "trypost",
      "workspace_id": "01a171dd-5281-730d-af07-f2168d17add7",
      "workspace_name": "Admin's Workspace",
      "social_account_id": "01a172c9-3761-700a-9798-00febaa9fa90",
      "service": "instagram",
      "handle": "dibalikbenda.id"
    }
  ]
}
```

[CONTENT_PACKAGE.md](CONTENT_PACKAGE.md) prepares the title, exact caption body, five hashtags, editorial keywords and verified file metadata. Content type instagram_reel; schedule and optional cover/feed-sharing settings are unset. Local upload is the selected route. Previous auditory review limits remain recorded and are not reclassified as human approval.

Current state: content package and requested saved draft delivery complete. No preview server was started or retained by this continuation; port 3002 had no listener on the cleanup check.

## Draft delivery result

- Provider/workspace: Trypost, Admin's Workspace (01a171dd-5281-730d-af07-f2168d17add7).
- Account: Instagram @dibalikbenda.id (01a172c9-3761-700a-9798-00febaa9fa90).
- Post ID: 01a172da-a2ef-7179-a14f-f5828338b158; observed status draft; content type instagram_reel.
- Media ID: 01a172da-764e-7098-9f4f-bef64eaeb2e9. Local upload returned HTTP 201. Separate get_post confirmed one video, exact original filename, 16,237,215 bytes and 90 seconds. The exact 697-character caption including five hashtags matches the package payload.
- scheduled_at and published_at are null; no queue or publication action was requested or executed.
- Receipt: [PUBLISHING.json](PUBLISHING.json). The full payload, fingerprint, upload outcome, attached media identity and draft read-back evidence are retained without signed upload URLs or tokens.
- Initial public-media limitation (resolved by the recovery below): fetching the returned media URL failed with HTTP 403 using the default Python client and HTTP 404 (Not Found) with a Mozilla user agent. Draft persistence and attachment were confirmed by MCP while the file was missing. No duplicate upload/post or hosting migration was attempted.
- Requested endpoint: complete as a saved draft. No provider UI URL was returned, so none was invented.

## Missing media recovery — 2026-10-25

The user's "coba periksa" continued diagnosis of the reported media-access failure. Read-only checks found the local Trypost container and confirmed that the referenced video was physically absent. Its media directory was root:root 0755, preventing PHP-FPM's www-data workers from writing there; the installed upload writer ignores the filesystem's false return. The public/storage symlink was correct, and website/avatar serving worked.

Restored the originally requested media delivery within the existing draft: changed only the media directory ownership to www-data:www-data, retained its mode, and restored the exact verified local v1 file to the missing recorded path using www-data and a no-overwrite guard. Existing database/post/media identities, caption and publication state were preserved.

At 18:45 Asia/Jakarta, the original public media URL returned HTTP 200 for all 16,237,215 bytes with SHA-256 matching the verified export. A separate byte-range request returned HTTP 206 with 1,024 matching bytes and the correct total size. MCP read-back reconfirmed the original draft and attached media identity; scheduled_at/published_at remain null. The incident is resolved. See [MEDIA_DIAGNOSTIC.md](MEDIA_DIAGNOSTIC.md) and [PUBLISHING.json](PUBLISHING.json) for retained before/after evidence. No new audiovisual listening assessment or publication is claimed.
