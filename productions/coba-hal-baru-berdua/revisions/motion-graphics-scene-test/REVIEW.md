# Motion-graphics scene integration review

Date: 2026-10-27. Status: agent verification passed; user accepted the isolated scene treatment with ?cocok?.

## Scope

An isolated 12.39562s extraction of the existing episode's scenes 11–13, corresponding to canonical time 62.16950–74.56512s. Scene 12 is the only changed scene. Its 4.25950s window starts at test time 3.68125s, corresponding to canonical time 65.85075s.

The kinetic-type module of the current project-owned motion-graphics skill supplies a restrained word entrance for “Coba bareng?”. Registry search `editorial emphasis word reveal` returned `per-word-crossfade`, whose recipe was adapted to static editable spans, the inherited Newsreader face and 88px display size, the original palette, and 10px upward travel without blur or scale decoration. “Coba” enters on the invitation opening; “bareng?” enters on its measured source word at canonical 66.99425s, local scene time 1.14350s. Original illustration choreography, fixed board chrome, and the final reading state remain.

The owner retains composition setup, scene windows, the separate full spoken-caption track, narration and SFX, verification, and review. No extra pitch, synthesis, render gate, or external delivery was introduced by the scene specialist. Canonical episode status remains complete.

## Evidence

- `check.json`: browser ran; 356 seek-grid states were sampled; runtime, layout, four motion assertions, and all 22 contrast checks passed with zero errors.
- `snapshots.json` and `video/verification/review/`: 16 captured states, a phone sheet, and two seam strips. The phone sheet and outgoing seam strip were visually inspected. The scene advances from the opening pair to the invitation space and recipe, while the heading resolves above it and captions remain in their own band.
- `runtime-report.json`: 11 forward/reverse seek operations; five repeated target times produced byte-identical screenshots. The host quantizes requested times to its 30 fps frame grid. Proof images are in `video/verification/seek/`.
- The assembled preview played to 12.39562s. Narration remained ready, its source-media time matched the extracted window, and no page or media errors were observed. The existing ElevenLabs `eleven_v4` WAV and frozen board SFX were reused; no paid request was made. This is programmatic playback evidence, not a claim of direct perceptual listening.
- `TEST_PLAN.json` records eight canonical hashes. All match, including the original composition, scene, captions, narration, export, publication receipt, package pin, and tracker. The test copies of neighboring scenes and narration are unchanged from their sources.

## Reviewed warnings

Two inherited repeated-`fromTo` selector warnings concern queries inside distinct SVG beat groups; their actual path sets are disjoint. The reverse-seek pixel comparisons support stable behavior. Three type-size warnings concern the board's fixed, approved 26px chrome. Preserve that identity rather than changing it for this isolated test.

The trial's CLI pin was upgraded from 0.8.200 to 0.8.205 after the freshness probe and verified by the full check. The canonical production retains its original 0.8.200 pin.

## Preview handoff

Preview: http://127.0.0.1:3002/#project/video. Ownership and release conditions are recorded in `PREVIEW.json` and the production's `EPISODE.md`. The review hold is released. Managed stop completed; follow-up status is `not-running`, and no listener remained on port 3002. The recorded pipeline-owned PID was 27328. No MP4 was rendered or published.

Approval recorded at 2026-10-26T18:02:07Z (27 October, Asia/Jakarta). The accepted scope is this isolated scene treatment; no render or publication is requested.

Next: commit the accepted trial artifacts. The consolidated pipeline is ready for the next production; a full new production remains a separate request.
