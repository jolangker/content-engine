# One stitch inside a sewing machine

## Selection and scope

- slug: satu-jahitan-mesin-jahit
- topic_selection: user
- selection_evidence: the user replied "setuju" to the recommended first topic, sewing-machine stitch formation, on 2026-10-24
- topic: single-needle two-thread type-301 lockstitch, using JUKI's documented horizontal full-rotary-hook variant
- audience_question: how can the visible needle movement make two threads interlock inside fabric?
- board: di-balik-benda, approved v3
- editorial: [EDITORIAL.md](../../boards/di-balik-benda/EDITORIAL.md)
- visual_spec: [frame.md](../../boards/di-balik-benda/frame.md)
- choreography: [SHOT-DIRECTION.md](../../boards/di-balik-benda/SHOT-DIRECTION.md)
- explicit_visual_direction: 2.5D
- requested_endpoint: export
- until: export
- delivery: local verified export; no content package or external delivery requested
- language: Indonesian, inherited from the board
- audience: curious general viewers without engineering prerequisites, inherited from the board
- duration: 90 seconds, inherited from board v3
- inferred_format: platform-neutral vertical 1080x1920 at 30 fps, matching prior board productions; no publishing destination is selected
- planned_shot_density: approximately 16 explanatory shots, adaptable within the board's 14–18-shot guidance
- intent: explain one coherent stitch-forming cycle through interacting parts and visible causal handoffs
- route_candidate: faceless-explainer, a narrated mechanical topic with original diagrams and no captured website or existing footage

## Execution and review policy

- execution_policy: automation
- automation_after: none
- automation_state: active
- option_validation: the user explicitly corrected --automation=after-hooks to --automation=after-hook
- human_review: none
- pre_render_authorization: delegated by the user's latest --automation instruction
- activation_evidence: latest user requested continuation with immediate --automation on 2026-10-24; supersedes pending after-hook policy
- human_approved_topic: true
- human_approved_hook: true; the user replied "setuju" after hook 1 and its selected direction were presented on continuation
- script_status: agent-verified v1 under delegated selection
- storyboard_artifacts: required before audio synthesis and animated assembly, including the complete PNG, even after automation activates
- workflow_initialization: initialized once inside video/ with HyperFrames 0.8.188; the maintained consolidated HyperFrames explainer workflow replaces the retired faceless-explainer skill
- preview: pipeline preview PID 15340 / port 3002 was opened for final look and render, then verified stopped after export

## Candidate comparison and overlap

Ten candidates were presented: lockstitch formation, open differential, lever escapement, bicycle rear derailleur, seatbelt retractor, drill torque clutch, single-lever ceramic mixer, automatic kettle switch, automatic umbrella, and spring-energized stapler. Sewing-machine stitch formation was recommended for its linked needle, hook, thread-handling, and fabric-feed actions and its strong visual payoff in a sectional 2.5D view. The user accepted this recommendation; selection is human, not delegated.

The tracker and on-disk production folders were checked. Existing mechanism episodes cover ballpoint ink transfer, zipper engagement, clothespin spring action, cable-tie locking, and alternating soap-pump valves. None explains interlocking two threads through a synchronized stitch cycle. No conflicting production slug exists.

## Research needs

1. Establish stitch type and exact hook variant, with credible technical diagrams.
2. Verify needle descent and rise, loop formation, hook pickup, passage around the bobbin case, release, and take-up.
3. Verify the fabric-feed phase relative to the needle and presser foot.
4. Separate illustrative coloring, removed housing, exaggerated clearance, and slowed timing from physical behavior.
5. Keep hook implications within the supported explanation; avoid implying every stitch type or sewing machine uses this mechanism.

Evidence lead: [Coats — Basic Stitch Types](https://www.coats.com/en/info-hub/basic-stitch-types). Further evidence and claim mapping belong in SOURCES.md.

## Audio planning

Completed with one ElevenLabs eleven_v4 request and the project-root .env voice. Original audio and alignment are preserved. See Audio v1 and video/audio_meta.json for pitch-preserving tempo processing and measured placement. Narration only is intentional; BGM and SFX decisions are recorded in video/sound_design.json.

## Current state

- current_stage: export
- current_status: complete
- requested_endpoint: export; preserved from the original request
- next_action: none within the requested scope
- completed: researched explanation, script, 16-shot verified static board, continuous narration, captions, animated composition, agent final-look verification and verified MP4
- review_policy: immediate automation from the latest instruction; no human final-video approval claimed

## Continuation and delegated hook selection

Latest scope retains until=export. Immediate --automation supersedes the prior delayed option. No human hook/script/layout/final-look approval is claimed.

1. **Jarumnya cuma naik turun. Tapi bagaimana dua benang bisa saling mengunci di dalam kain?** Familiar visible action leads directly to the hidden two-thread interaction; selected because its promise is answered by the entire chain.
2. **Ada benang kedua di bawah kain. Bagaimana benang ini bisa bertemu dengan benang di jarum?** Hidden-source mystery; begin below the fabric and trace toward the needle.
3. **Satu jahitan lahir dari satu loop kecil. Mari ikuti lintasannya di dalam mesin jahit.** Follow one orange thread loop through a continuous macro journey; a bolder thread-led film.

Selected: hook 1, by the agent under immediate automation. Research is complete within SOURCES.md. Sixteen explanatory shots will retain 90 seconds at 30 fps.

## Static storyboard verification

All 16 original styled stills inspected in order, then the complete boards/storyboard.png opened and inspected. PNG is 1920 x 4268; all 16 scene images loaded at 1080 x 1920, no HTML text overflow. The take-up label was moved inward and hook retention was attached to its physical beak before final board capture. Paths: video/boards/storyboard.html and video/boards/storyboard.png. Agent-verified under automation; latest user ?setuju? accepts the selected hook/direction, not a fabricated final-video approval. Proceed to one full-script narration request.

## Audio v1

Provider elevenlabs; voice 3mAVBNEqop5UbHtD8oxQ resolved from root .env; model eleven_v4. One request produced 91.60s and 211 aligned spoken words, with tags excluded. A pitch-preserving 1.05 tempo adjustment fits the exact board duration without paid resynthesis; placed master 87.241333s. All words and source audio preserved, word timestamps scaled consistently. Voice-only is intentional; no BGM/SFX cues planned. Audio has not been perceptually listened to.

## Preview lifecycle

Pipeline-created preview: project productions/satu-jahitan-mesin-jahit/video; PID 15340; port 3002; Studio http://127.0.0.1:3002/#project/video. Started after a not-running status result. Hold: final agent review and delivery render. Release: stop after verified export; no ongoing user review hold is required in automation.

## Final-look authorization

Final check passed with no error or warning. Agent inspected phone/beat/cut sheets and targeted diagnostic frames. Opened Studio and verified HTTP 200, same pipeline preview PID 15340/port 3002. Composition v1 is agent-verified for render under latest immediate --automation; no human final approval is claimed. See video/REVIEW.md for fixes and perceptual limits. Stage: export in progress.

## Verified delivery v1

- MP4: exports/satu-jahitan-mesin-jahit.mp4
- Captions: exports/satu-jahitan-mesin-jahit.srt
- Decoded export proof: exports/proof-sheet.jpg
- Static planning board: video/boards/storyboard.html and video/boards/storyboard.png
- Duration: 90.0 seconds; 1080 x 1920; 30 fps; 2700 frames; H.264 video and AAC audio.
- Export SHA-256: 6ea685efae3fa0f0c86cde089b6f27c01f0c14dc55c2050987f1f5a1c6202e53
- Full decode: no errors. Audio: -15.84 LUFS integrated; -3.16 dBTP; sample peak below clipping.
- Technical final check: passed without errors or warnings. Diagnostic and exported proof frames inspected. Audio measurement does not establish perceptual listening; uninterrupted audiovisual watching was unavailable.
- Export authorization: delegated by latest --automation, after agent verification; human final approval false.
- Preview cleanup: managed stop, not-running status, and listener/process checks verified. PID 15340 no longer owns port 3002. No preview hold remains.
- Scope fulfilled: export only. No content-package or external delivery action was executed.

Detailed evidence: video/verification/export.json, video/verification/final-check.json, video/verification/preview-cleanup.json and video/REVIEW.md.
