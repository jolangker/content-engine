# Final composition review — export v1

Agent-verified under the user's 2026-11-22 automation-through-export instruction. Human-approved script and storyboard v1 remain the basis. No human approval of the animated final is claimed.

The film follows the keeper's mixed scoop, the prepupal-stage distinction, a connected exit, a partial collection, and the container lift. Eight editable SVG scene compositions preserve the approved materials, geometry, focal scales, and yard landmarks. A single native-speed Pribs / eleven_v4 recording drives caption timing. Alternative shortlist topics and hook framings were not built.

Final composition check: verification/film-check.json (`ok: true`, browser ran), saved as .hyperframes/artifacts/checks/d85111b6-1cae-4f87-b226-c5490d805195.json. Lint, runtime, layout, contrast and craft have zero errors and zero warnings. The motion section reports zero samples, so this is not claimed as automated motion-sidecar coverage. Motion was checked through seeked snapshots instead.

Opened the full beat and phone sheets and all seven seam strips in .hyperframes/artifacts/snapshots/a8f1b824-60c3-49f9-9608-ea64092b8347/. Inspected five-frame inset progression and six-frame falling-prepupa progression in verification/inset-motion/ and verification/drop-motion/. Inspected waiting-light and final-caption frames in verification/final-adjustments/. The primary actions read at phone scale; moving larvae stay on the ramp, the drop enters the collector, and the final bin still contains feeding larvae.

P0 repaired: at the beginning of scene 7, the magnified larva initially appeared before its inset backing. Grouped it with the backing/anchor so the entire inset enters together. Re-snapshotted that move and rechecked the composition.

P1 repaired: the waiting-light cue initially sat behind the background. Moved it over the illustration for a single ambient-light change before the climb. P1 repaired: held the final caption phrase through the final 1.6-second visual hold. These changes preserve accepted narration and layout.

Seven scene cuts use measured quiet intervals with at least the maintained verifier's required guards, on the same integer 30fps map as captions and scene hosts. Sound-design preflight passed all three contact cues and current file/timing/motion hashes. The 116-word recording was transcribed locally; the only lexical differences were alternative magot/maggot spelling, restored to the accepted caption spelling.

Audio roles: one narration, low-gain acoustic music, three soft contact accents; insect footsteps and mismatched electronic scoop effects intentionally absent. Carefree by Kevin MacLeod is used under CC BY 4.0 and its attribution must accompany publication. The original track page was read using Scrapling after ordinary reading omitted its JavaScript content. Official audio was ingested via media-use; no generated music or additional narration take was made.

No subjective listening was available. Waveform silence, decoding, source matching, levels and encoded audio will be verified; they do not establish a perceptual listening judgment. Individual word timing remains a transcription estimate, distinct from measured acoustic scene anchors.

The weakest shot is the partial-collection wide in scene 7: the remaining pale organisms need magnification to be legible at yard scale. The accepted anchored inset addresses that tradeoff. Avoid adding more explanatory labels or shrinking captions.

No remaining final-check warnings were retained. The generic subtitle safe-zone exception preserves the board's accepted lower-third placement, and the SVG crop exceptions apply only to intentional close-shot illustration crops. The background remains a flat yard, rather than a generic abstract card layout.

The final local preview was opened and returned HTTP 200 before rendering. Pipeline-owned PID 20420 on port 3002 is retained only through export inspection, then must be stopped and its release verified. Export results are recorded in verification/export.json after actual-file checks.

## Actual export verification

The final MP4 is 1080 × 1920, 30 fps, 51.933333 seconds, H.264 video and AAC audio. All frames/audio decoded without error. The saved export-proof.jpg was opened and all eight scene representatives, the opening and the last-frame hold were inspected. Video packet-stream SHA-256 matches the original HyperFrames delivery render: the audio refinement did not re-encode or change its video frames.

After the initial render, the music was smoothly reduced around the seven measured scene cuts. finalize_export.py retained the HyperFrames video stream with codec copy and rebuilt the audio from the same authored narration, music, and three SFX. This makes quiet-cut verification meaningful despite continuous music. Full source files, the initial render, and the final mix are preserved. These are local mix corrections under delegated export authorization, not another voice generation.

Actual encoded export: seven acoustic seams pass (cut RMS approximately -66 to -75 dBFS); all three SFX match their authored positions within 0.34 ms, with measured waveform similarities 0.82–0.97. Integrated loudness is -16.40 LUFS and true peak -4.63 dBTP. No clipping was detected. These are technical measurements, not a listening claim. Subjective listening remains unperformed.

The soundtrack source/attribution is in ../exports/CREDITS.txt; include its music credit when publishing. An SRT and separate cover image accompany the requested export. The endpoint is export; content-package authoring and publication were not requested for this run.

## Music-free export verification

For v2 the mix was rebuilt from the recorded narration and the three existing contact cues by request. The v2 video packet hash matches v1, so the original proof frames, cover, and captions still apply. All seven cut checks and all three cue waveform matches passed. The encoded mix measures −16.40 LUFS integrated and −4.57 dBTP. [Export verification](verification/export-v2-no-bgm.json) and [v2 credits](../exports/CREDITS-v2-no-bgm.txt).
