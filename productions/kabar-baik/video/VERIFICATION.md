# Verification — Kabar baik v1

## Authorization and scope

Agent verification under the user's --automation instruction. Human approval is unset. Pre-render authorization is delegated through the recorded publishing/draft endpoint. Studio preview was opened/exposed at http://localhost:3005/#project/video and returned HTTP 200 before delivery render.

## Editorial and creative review

The 200 spoken words match the single recording's 200 aligned words, in order. Tags are absent from word alignment and captions. Claim map is in ../SOURCES.md. Capitalization, active–constructive responding and the association claim are bounded; no diagnosis or causal guarantee is made. Quiet interest is clearly an editorial application rather than a claim of equivalent experimental effects across response types.

Both contact sheets from snapshot run 16ba0a75-5736-43ea-9b0d-7e2e37ec60c2 were visually inspected. All fourteen scene landings are present, including charcoal frame 3. Large first quote, attention diversion, contracting space, observation/unknown split, concept flow, diagonal sharing diagram, three-line response qualities, quiet small pair, association diagram, invitation quote, effort trace, vertical sequence, first-person gesture and final reflective pair provide distinct compositions. Source fonts and fixed chrome geometry are inherited from the board. Frame 1 and frame 9 were also inspected at full 1080x1920 resolution; type and captions are legible and within their bands.

After this review, frame 10's redundant supporting quotation was shortened to “Buka ceritanya.” Captions were consolidated into one independently seekable composition/track and marked with data-track-kind=captions. These changes preserve narration and timing.

## Technical pre-render gate

verification/check-final.json: ok true; lint 0 errors/0 warnings; runtime and layout pass; motion assertions pass over 300 samples; contrast 42/42. Root duration 86.10 s, 1080x1920, 30 fps. CLI pinned to 0.8.181 at initialization, no version upgrade was required.

sound_design.json resolves narration, BGM and SFX separately. Native-speed narration 84.48 s at 0.30 s; tail 1.32 s. Six board-library effects at authored visual events, final reflection deliberately unaccented. sound_design.py --check passes and verifies asset/motion/timing hashes and placed tracks. Project npm precheck/prerender wrappers include that check.

## Listening boundary

No realtime creative listen or human listening approval is claimed. Alignment, original-source and rendered-mix comparisons, full audiovisual decoding, loudness/peak measurements and cue waveform matching provide objective evidence; they do not prove subjective pronunciation or perceptual mix balance. The preview and final file remain available for listening. Export-specific evidence will be appended after encoding.

## Verified export

[MP4](../exports/kabar-baik-v1.mp4): 86.1 s, 1080x1920, 30 fps, H.264/AAC stereo 48 kHz, 6128655 bytes. SHA-256 `5f868a1633e2179a7dea9c0173acd5c3dee77f62ccbe436df3f32b4d0200e9a4`. Full audiovisual decode passes. Integrated loudness -21.8 LUFS and true peak -3.0 dBTP; no clipping. All six effects match decoded export near authored time with zero detected timing offsets (similarity 0.815–0.994). See exports/verification-v1.json and verification/sound-design-export.json.

The decoded 14-scene contact sheet was visually inspected; scene 10 now reads “Buka ceritanya.” Captions, fixed chrome, layout, actor shapes and paths match the intended final sequence. Each scene's landed pose was extracted from the encoded file. No human listening approval is inferred from objective waveform evidence.

Render: HyperFrames 0.8.181, drawelement capture / hardware Intel GPU; 2583 frames; completed in 113.0 s. No desktop-app offer line was emitted.

## External delivery evidence

Hosted original was downloaded without authentication; content-type video/mp4, byte size and SHA-256 exactly match the local export. Buffer creation returned saved draft 6ad72c86c4a5f1eea4c8e5b6 with the requested caption/media/settings and null due/sent times. PUBLISHING.json retains the observed response and payload fingerprint. Draft endpoint complete; no live-post claim.
