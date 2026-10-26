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
