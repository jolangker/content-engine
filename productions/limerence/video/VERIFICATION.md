# Verification record

## Historical styled static storyboard verification

Date: 2026-10-19. Historical scope: 14 styled static compositions and the review page. At this checkpoint no animation, synthesized audio, or MP4 had been produced. Ninety seconds is the current estimated scene schedule, not measured voiceover duration.

## Captured composition

- HyperFrames project: this directory; owning workflow `faceless-explainer`.
- Actual root composition: `index.html`, mounting all 14 sub-compositions from `compositions/frames/`.
- Canvas: 1080×1920. Local Newsreader normal/italic and DM Sans loaded; local GSAP 3.14.2.
- Snapshot command: `npx hyperframes snapshot --at "2.5,8.5,15.5,22,29.5,36,41.5,48,54,59.5,65,71,79,87" --no-end --describe false --output boards/stills`.
- All 14 stills exist at 1080×1920 and were inspected in the contact sheets. Opening compositions 01–05 were also examined at full resolution; frame 03 was re-examined after the final label correction.
- Corrected label/path collisions in 01, 03, 07, 09, and 12, and increased clearance below the actor in 04.
- Captures used Windows Chromium hardware GPU through Intel Iris Xe / ANGLE Direct3D11, as reported by HyperFrames.

## Full framework check

- Scaffolded pin was 0.8.172. A read-only freshness check reported 0.8.173; applied `npx hyperframes@latest upgrade --project .` and verified the updated project.
- Final command: `npx hyperframes check --json --at "2.5,8.5,15.5,22,29.5,36,41.5,48,54,59.5,65,71,79,87"`.
- Result: `ok: true`, `browserSkipped: false`.
- Lint: 15 files, 0 errors, 0 warnings.
- Runtime: 0 findings.
- Layout: 14 midpoint samples, 0 findings.
- Contrast: 42/42 text checks passed WCAG AA at the tool's five contrast sample times. This is not a claim that every text element was contrast-audited at every midpoint.
- Motion assertions disabled, appropriate to static poses; no animation verification is claimed.
- Report: `.hyperframes/artifacts/checks/43257077-3e60-4ca7-b4cc-771c3c33cb91.json`.

## Review page

- Canonical page: [boards/storyboard.html](boards/storyboard.html).
- Fourteen `.frame` cards in film order, each with its real still, `.title`, `.time`, a description, and expandable approved narration.
- `package_storyboard.py` validates one full-size PNG per frame.
- `verify_storyboard.py` opened the local review page in Chromium, verified all 14 images, checked desktop width 1440 and mobile width 390 for horizontal overflow, and exercised the narration disclosure.
- Result: no page errors or horizontal overflow; all images loaded; disclosure opens and closes.
- Evidence: `boards/page-verification.json`, `boards/storyboard.png`, `boards/storyboard-mobile.png`, and `boards/storyboard-overview.png`.
- Overview and mobile screenshot were visually inspected. Every individual still can be opened from its review card.

## Approval boundary

The script and 14-frame text plan are approved. The styled layouts were subsequently accepted by the user with “cocok” on 2026-10-19. The current STORYBOARD.md records `layout_approved: true`. At the original static checkpoint, `built` meant a posed composition and inspected still existed. No approval of motion, narration audio, a final preview, or export is inferred.

Generic HeyGen auth reports signed out. Static work is local. The project's explicitly selected ElevenLabs/Brian/eleven_v4 choices remain recorded for the later authorized audio stage; no provider fallback was used.

## Narrated animation verification — 2026-10-19

The user accepted the exact 14-frame static storyboard with “cocok”. The current authorized deliverable is the audiovisual preview. MP4 export has not been performed.

- All 14 compositions are animated and retain the approved visible copy, inline layout, and painted SVG geometry. `verification/layout-preservation.json` records the comparison. Frame 12 splits one continuous solid path into two exact contiguous paths for separate cues; its painted geometry is unchanged.
- The original continuous ElevenLabs/Brian/eleven_v4 narration is preserved at `.media/audio/voice/narration-full.mp3`, with native alignment. All 180 approved words match in order after punctuation normalization. Six delivery-tag sections guide synthesis; tags do not appear in captions.
- Narration duration: 83.76 seconds. Voice offset: 0.4 seconds. Composition duration: 85.366667 seconds at 30 fps. Boundaries derive mechanically from native word timing, with no time stretch.
- The mix copy is 48 kHz PCM with measured -18.48 LUFS integrated and -1.99 dBTP. An independently assembled diagnostic mix including both quiet ticks measures -18.49 LUFS / -1.99 dBTP; `verification/preview-mix.wav` is audio-only verification, not a video export. No music bed is used.
- Forty-one caption groups contain all 180 spoken words exactly once, at most two short lines. Captions occupy one transparent sub-composition / timeline track, within y=1570–1760.
- Solid traces are measured once; dashed paths retain their original dash pattern through masks or opacity. Actors retain their authored SVG transforms. No camera move, B-roll, or diagnostic labeling was added.
- Final full check: `npx hyperframes check --json --at "0.5,2.166667,4.833333,7.633333,11.433333,14.483333,18.533333,20.4,23.266667,28,33.733333,35.433333,38.133333,41.066667,45,47.466667,50.933333,52.7,55.466667,57.15,59.833333,62.4,65.966667,68.3,71.633333,75.6,80.566667,82.716667"`.
- Result: `ok: true`, `browserSkipped: false`. Lint: 16 files, zero errors/warnings. Runtime: zero findings. Layout: 28 entrance/midpoint samples, zero errors/warnings. Motion: enabled from `index.motion.json`, 300 seek samples, zero findings across 31 assertions. Contrast: 35/35 text checks passed at five sampled times.
- Three informational connector heuristics remain on frames 03/06. These diagrams intentionally have open unknown endpoints; the frame-06 heuristic even associates a hidden frame-12 label with an endpoint. Inspected snapshots show the intended open geometry, with no layout defect. No audit suppression was added.
- Initial motion assertions targeted static parent containers rather than animated child lines; they were corrected to the actual animated elements. Frame 02's first heading begins at scene start, making its early introduction reliable under the coarse 300-sample whole-film sweep. The approved settled pose is unchanged.
- Passing report: `.hyperframes/artifacts/checks/5fa604a2-85d7-4a9b-8519-19e50bd5f957.json` (CLI 0.8.173).
- Fourteen mounted late-state captures exist in `verification/animated-stills/`, captured by HyperFrames with local fonts and hardware GPU. Both contact sheets were inspected; opening frames 01–05 were also inspected at full resolution. Partly revealed labels/actors in these captures are deliberate narration-timed entrances, not missing elements.
- All 13 scene handoffs remain cuts, with no overlaps. Workflow transition verification passed with zero transition effects.
- Studio: `http://localhost:3002/#project/video`. Started with managed `preview --background`; `preview --status` confirms the persistent server, and HTTP responds 200. The server remains running for user review.

Scope: automated seek/layout/motion checks, audio-content/timing/loudness measurements, and visual inspection of rendered stills. These do not establish a human listening judgment of synthesized pronunciation or prosody; the audiovisual preview is the review surface for those qualities. No MP4 has been encoded.


## Live Studio playback

Studio opened the actual root composition with all 14 scenes and the caption composition registered. HTTP 200, no page errors; narration decoded at 83.76 seconds. A full 1× playback sampled 274 states through 85.3406 seconds, observed all 14 scene IDs and all 41 caption groups, and reached the end of the narration without page or media errors. Evidence: `verification/studio-ready.json`, `verification/playback-check.json`, and `verification/studio-playing.png`. This is a live playback/decoding test, not an auditory judgment of pronunciation or prosody.

Studio's all-HTML lint scan separately discovers the historical plain `boards/storyboard.html` review page and reports `root_missing_composition_id` there. That document is deliberately a review page, is not mounted by index.html, and remains preserved at its approved location. The full mounted-video check above passes with zero errors and warnings. No composition was changed to hide the review-page diagnostic.

Preview v1 is awaiting user review. The persistent server remains alive. MP4 export has not been authorized for this preview yet.


## Approved final export — 2026-10-19

The user approved the exact presented preview v1 with “gas”. The CLI pin was upgraded from 0.8.173 to 0.8.174 as required by the freshness probe. Before rendering, the same full 28-time layout check and 300-sample / 31-assertion motion audit passed on 0.8.174 with zero errors/warnings; sampled contrast passed 35/35. The three previously reviewed informational connector heuristics are unchanged. Passing report: `.hyperframes/artifacts/checks/0e023850-ba63-4072-a53e-faf03501ef43.json`.

Render command: `npx hyperframes render --quality delivery --fps 30 --strict-all --output ../exports/limerence.mp4`. Result: exit 0, 6,433,118-byte MP4, 85.366667 seconds, 1080×1920, 30 fps / 2,561 frames, H.264 High / yuv420p / BT.709, AAC stereo / 48 kHz. DrawElement capture, hardware GPU, 152.9 seconds wall time. Four built-in drawElement-versus-screenshot self-verifications passed. An optional caption-overrides.json lookup returned a nonblocking 404; no authored resource failed and no override was needed.

`verify_export.py` decoded 14 proof frames from the actual MP4 and compared them with the approved preview stills at their nearest 30 fps timestamps. SSIM minimum 0.998466, maximum 0.999424. The encoded contact sheet and full-size frames 01/08/14 were visually inspected. Audio measures -15.53 LUFS integrated stereo / -1.88 dBTP. A unity-preserving mono downmix measures -18.54 LUFS versus the -18.49 LUFS mono diagnostic reference; the stereo difference is channel energy, not a gain change. No encoded audio clipping was measured.

Output metadata and comparisons: `../exports/verification.json`. Encoded proof: `verification/encoded/`, also copied to `../exports/limerence-contact-sheet.jpg`. The SHA-256 checksum accompanies the delivered file. No post-render HyperFrames lint/check/snapshot was run; verification examined the actual encoded artifact. Export is complete.


## SFX correction — 2026-10-20

See [current export verification](../exports/verification-sfx.json) and [cue waveform evidence](verification/sound-design-export.json). The current local export is limerence-sfx-v2.mp4. Six cue matches pass, speech metadata is unchanged, full AV decode passes, fourteen scene comparisons retain the visual output (minimum SSIM 1.0). Integrated stereo loudness -15.53 LUFS; true peak -1.79 dBTP. Prior MP4s fail the new cue-plan verification (baseline evidence is in verification/sound-design-baseline.json), so an audio stream alone cannot satisfy the gate. Contact sheets were inspected. No human or agent realtime listening is claimed; objective evidence does not replace a perceptual balance review.
