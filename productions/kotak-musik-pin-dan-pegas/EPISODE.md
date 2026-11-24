# Music box: pins and spring

board: di-balik-benda v4 (2026-10-25)
topic_selection: auto, delegated by --topic=auto
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
human_approval: false
pre_render_authorization: delegated by the user's --automation instruction
requested_endpoint: publishing
delivery: queue (next configured slot; no custom time)
format: 1080x1920, 30 fps, exactly 90 seconds
language: Indonesian
audience: curious general viewers

## Direction
Follow energy from a wound spring to gears, a pinned cylinder, comb vibration and a centrifugal friction governor. Scope: original explanatory model based on US5449856A; not every music box. Do not combine this friction governor with the air-brake variant. Exaggerated clearances, slowed motion, removed shell and enlarged pins are labelled. Pitch/tune and gear ratios are illustrative, never measurements of a particular product.

Inherited [editorial](../../../boards/di-balik-benda/EDITORIAL.md), [visual tokens](../../../boards/di-balik-benda/frame.md), and [choreography](../../../boards/di-balik-benda/SHOT-DIRECTION.md). Medium: layered 2.5D illustrated metal/polymer, upper-left light, dark blue contours, pale mineral bench. No flat infographic scenes. Sixteen explanatory shots, including pin/comb and governor contact macros.

Narration: ElevenLabs eleven_v4, root .env voice, one tagged full-script recording at native speed. SFX: existing library first, illustrative material contact and a distinct editorial inspection cue. No BGM: the subject is sound production, so keep the explanation and diagnostic plucking/release cues exposed without a competing tune. Reused sounds are illustrations, not an acoustic measurement or a reproduction of the pinned melody.

## Topic decision and overlap
Compared ten topics in conversation: music box, wing corkscrew, manual can opener, derailleur, seatbelt retractor, pawl hub, ratchet wrench, impact sprinkler, mechanical clock, crank pencil sharpener. Music box selected for five linked interactions, visual discovery and technical evidence. Not selected merely for implementation ease. Other candidates remain research leads, not verified scripts.
Checked TRACKER and all production folder names. No music-box episode exists. Existing sewing machine, differential (unregistered historical folder), lock, sprayer, toilet, stapler and simple fasteners have distinct central questions. Preserve all existing productions.

## Hook decision (before script)
1. “Kotak ini bisa memainkan lagu tanpa baterai. Siapa yang menyimpan nadanya?” Energy and note-pattern mystery; can be answered with spring, pins and comb.
2. “Tonjolan kecil ini menentukan kapan sebuah nada berbunyi.” Pin-contact-first macro story.
3. “Pegas ingin lepas cepat. Kenapa lagu kotak musik tetap teratur?” Governor-first story.
Recommended/selected: 1, agent choice under delegated automation, presented before script drafting. It covers both stored energy and stored note sequence. Human approval is not asserted.

## Publishing targets
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
Live preflight: Trypost Admin's Workspace 01a171dd-5281-730d-af07-f2168d17add7; exact Instagram account connected; caller requires_approval=false, publishes_directly=true. instagram_reel supports 90 seconds and up to 300 MiB; caption limit 2200, five hashtags. Queue configured daily 10:00 Asia/Jakarta. Actual future slot comes from Trypost at creation.

## Current state
publishing: complete (queue endpoint). Scheduled 2026-10-28 10:00 Asia/Jakarta; Trypost post 01a17988-f297-7132-b544-280282b68403. Verified 90-second MP4, complete content package and remote served-file hash. Preview stopped and temporary upload credentials removed. No future-publication monitor started. Requested repository commit follows the completed pipeline; see Git history. Detailed historical checkpoints follow in EPISODE.md.

## Static storyboard verification
All 16 scene stills, boards/storyboard.html and boards/storyboard.png verified before synthesis/animation. PNG 1920×4221, complete ordered s01–s16, no missing images; opened saved PNG and both still contact sheets. Repaired cropped pin labels in s06/s07; distinct contact/release and pre-contact/contact governor poses. Agent-verified under delegated automation; human approval false.

## Narration and measured audio
ElevenLabs eleven_v4, project-env voice, one continuous request; native 88.88 seconds, 192 exact aligned words. Placed at 0.3 seconds with native speech speed; peak-controlled gain and exact 90-second padding only. No synthesis retry. Captions and timing.json map all words to the locked script. SFX: reused material/editorial cues, plus three CC BY 4.0 real single-note music-box recordings by UbikPhonik; source credits included in publishing copy. BGM intentionally absent. Listening unavailable; objective evidence only, no phone-speaker or perceptual listening claimed.

## Motion verification
Version v1: 16 mounted scene files, measured timing, 57 caption groups and 62 designed cues. All 2723 30fps samples passed finite-state/reverse-seek checks, fixed comb-root and governor-wall checks, gear direction/ratio checks and continuity at both macro seams. Fixed premature tooth vibration before release. CLI full layout/runtime/contrast check and contact sheets being rerun on this version.

## Final-look checkpoint
Agent-verified version v1 under delegated render authorization: clean full check v2, 32 beat frames, phone sheets, all 15 seams, two 8-pose critical-action strips and independent still review. No unresolved P0/P1. Delivery render started; export/audio verification still pending. See video/REVIEW.md for limits.

## Verified export and package
Version v1: 90.0 seconds, 1080×1920, 30fps, 2700 frames, 18349001 bytes; SHA-256 de6a383a5763b69cd6814ce048233ddd77566c4f182dd2d8a7c5dc8e95564fc8. Full decode passed. All 62 cues detected in the decoded MP4 with their planned gains/onsets. Loudness -13.82 LUFS, true peak -1.68 dBTP. Decoded proof sheet inspected. CONTENT_PACKAGE.md and CAPTION.txt match this exact export and include all CC BY credits. Next: explicit queue delivery already authorized; no human approval claimed.

## Export and preview closure
Delivery v1 verified: 2700 frames / 90.000s, H.264 yuv420p, AAC 48kHz; full decode passed. All 62 cue waveforms detected; maximum offset 0.334 ms, below one output frame. Actual audio -13.82 LUFS, -1.68 dBTP. Twelve decoded MP4 frames and proof sheet visually inspected. No perceptual listening claimed. Pipeline preview PID 34160 stopped through the project command, status not-running, port 3002 has no listener. Hold released before packaging/upload.

## Queue delivery completed
Trypost post 01a17988-f297-7132-b544-280282b68403, observed scheduled; actual schedule 2026-10-28 03:00:00 UTC / 2026-10-28T10:00:00+07:00 Asia/Jakarta. Exact caption, instagram_reel type, account and attached media read back. Public served MP4 HTTP 200, bytes and SHA-256 equal the verified local export. Endpoint is scheduling, not a claim of live publication. Receipt: PUBLISHING.json. No future monitoring started. Next: requested repository commit after completed pipeline.

## Transport reconciliation
One post only. The first shell-to-tool JSON transfer altered non-ASCII punctuation; readback caught it. Updated the same scheduled post with ASCII-escaped JSON transport, retaining original intent and provider snapshots. Final exact-caption comparison passed. Windows text readers in episode helpers now explicitly use UTF-8. No duplicate upload/post retry, no changed schedule. Temporary upload contract deleted after attachment.

## Preview startup evidence (consolidated)

## Preview ownership
Pipeline-owned preview created for C:\Users\muhth\Documents\projects\content-pipeline\productions\kotak-musik-pin-dan-pegas\video; PID 34160, port 3002, Studio URL http://127.0.0.1:3002/#project/video, HTTP 200 verified. Hold: final-look review and delivery render, then release before packaging/upload. No pre-existing server was running for this project. Automation delegates final-look/render authorization; no human approval claimed.
