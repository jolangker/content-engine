# Tangki dua katup

- Board: [Di Balik Benda v4](../../boards/di-balik-benda/DIRECTION.md), [editorial](../../boards/di-balik-benda/EDITORIAL.md), [canonical frame](../../boards/di-balik-benda/frame.md).
- topic_selection: auto; explicitly delegated by --topic=auto.
- Selected angle: gravity toilet cistern with lever, chain, hinged buoyant flapper and cup-float fill valve; why it releases water and then stops refilling.
- Endpoint: export, 90 seconds, 1080x1920, 30fps, Indonesian.
- execution_policy: automation
- automation_after: none
- automation_state: active
- human_review: none
- pre_render_authorization: delegated by the user's --automation instruction
- human_approval: false
- Topic and hook decisions: agent-selected under delegation, not human approvals.
- Delivery: local export only. No hosting, account selection or publication.
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

Research and script being finalized. Next: required static storyboard, verify its PNG, synthesize full narration, synchronize animation/SFX, verify preview and export. No preview server started.

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


Next action: requested endpoint reached; stop. Preview cleanup verified. See VERIFIED.md and video/verification/ for evidence and listening limits.
