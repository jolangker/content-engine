---
workflow: faceless-explainer
flow: automation
storyboard: no
mode: autonomous
message: "Setiap lapisan di bawah rel punya tugas."
angle: narrative
destination: shorts
aspect: '9:16'
language: id
audience: curious general Indonesian viewers
length: 90s
board: bongkar-sistem
board_revision: 2
until: export
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
pre_render_authorization: delegated by the user's --automation instruction
human_approval: false
---

## Intent

Explicit invocation: `$shortform-production --board=bongkar-sistem --topic=auto --until=export --automation`. Selected topic: conventional ballasted railway track, progressively revealing load support, restraint, drainage and maintenance. Retain the board's full-screen semi-realistic environment, adult builder, 24 meaningful developments and camera travel within shots. This is a functional explanatory reconstruction, not construction instructions or historical chronology. Slab track exists and the closing copy must bound this episode to ballasted track.

## Confirmed and inferred

Confirmed: selected draft board, delegated topic and routine decisions, automation and export cap. Inferred from board: vertical 1080x1920 at 30fps, approximately 90 seconds, Indonesian narration and captions, original continuous 3D worksite, designed discrete Foley, no BGM. Narrative: incomplete attempt -> successive supported repairs -> whole-system result -> chair callback away from the railway.

## Production overrides

Project shortform-production requires complete static storyboard artifacts before audio synthesis and animation even in autonomous mode: STORYBOARD.md, boards/stills/, boards/storyboard.html and boards/storyboard.png. Perform and verify this pass, then proceed without a human checkpoint. Root board frame.md takes precedence over shipped design presets. Use one continuous ElevenLabs eleven_v4 narration request with root .env default voice and native alignment via maintained narration.py. Do not use workflow automatic provider fallback or split-per-frame TTS. Human approval remains false; final-look and render authorization are delegated by --automation.

## Assets and output

Local frozen Barlow and IBM Plex fonts from selected board; original Three.js world and character. Match material/contact SFX from reusable assets first. Deliver verified MP4 and SRT only; no package or external delivery. Keep production files inside this folder and exports in ../exports. Record listening limitations honestly. Release owned preview after export verification.
