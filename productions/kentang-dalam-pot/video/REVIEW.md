# Review

## Creative and factual review

- Delegated choice: follow the first build through its mature harvest. Drainage sets up a later repeat test, the hilling shot shows why an opaque pot still needs covered tubers, and the same clay rim identifies the pot through the harvest. Narrower drainage-only and tuber-only storylines were considered.
- The nine static storyboard poses and the full HTML/PNG board were inspected. The timed review covers full beat order, all eight cuts, phone-size captions and targeted frames of the opening, watered profile, pot tipping and last question. Evidence in `verification/final-review/` and `verification/final-fixes/`.
- The proof pass caught future words appearing ahead of narration and one caption persisting into the next shot. The final version sets each word's hidden state in CSS, reveals it at its measured onset and ends each group by its scene boundary. Rechecked the opening at 0.3, 0.7 and 1.2 s and checked the 82.867 s cut.
- The shaded water front and growing tubers are illustrative. The top view of leaf movement and the flattened soil profile in the tipped pot use schematic perspective. The harvest mat and pot retain their position from the preceding shot's setup.
- The intended caption y=1392 follows the approved board. HyperFrames' generic platform safe-area warning is explicitly waived on these caption groups. The phone-width proof shows the board's warm-white, yellow and dark outline treatment. Platform overlays were not previewed.
- The yield is illustrative, and the growing period is compressed. The local technical check and narration transcript do not establish a human listening test. Perceptual loudness and conversation-natural delivery were not separately listened to in this session.

## Technical review

- Final HyperFrames 0.9.52 check, 15 browser samples and 600 craft samples, returned `ok: true`. Zero lint, runtime, layout, contrast, craft or audio findings. The automatic motion sidecar sweep is not enabled in the root report. Motion evidence comes from sampled poses on the timeline and encoded proof frames.
- 62 progressive caption phrases, one narration track, four aligned SFX cues. BGM none per board. The eight acoustic cuts passed preflight on decoded placed narration.
- Actual encoded file evidence is recorded under `verification/` after final render.
## Encoded export

Verified ../exports/kentang-dalam-pot.mp4. H.264 yuv420p, 1080 × 1920 at 30 fps, 3,097 frames, 103.233333 s, AAC / 48 kHz, 31,958,574 bytes. SHA-256 5e8f67571e079e8f293d270b4c800421f0499b9ea737958f629cf6dbb254714a. Full video and audio decode passed. Integrated loudness −13.4 LUFS, true peak −1.6 dBFS. All eight scene-boundary tests and all four waveform-template SFX tests passed against this hash. Encoded frames for all nine scenes were extracted and inspected in verification/encoded-proof.png. Audio review was objective only. The planned visual and subtitle checks passed. The rendered export is the requested endpoint.
