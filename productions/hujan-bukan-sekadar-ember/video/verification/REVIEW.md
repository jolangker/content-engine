# Agent review before final delivery

## Technical and creative evidence

The final HyperFrames 0.8.195 check passes: zero lint/runtime/layout/contrast/craft errors, 9 layout samples, 25 contrast checks and 599 craft samples. Auxiliary text was enlarged to 28px after the initial craft warnings. The first delivery render was intentionally interrupted before completion to apply that correction. The current render is the replacement. Remaining warnings are reviewed: 66 timed groups inside the single caption sub-composition are expected, and environmental canvas scenery intentionally touches the left edge in a diagnostic close-up. Neither hides a critical label or contact.

All six initial static poses and the complete 1560x2237 storyboard PNG were inspected before synthesis. They preserve board v1 identity and use wide, medium, sectional, character and whole-system views. Twelve animation proof frames, four corrected final-use views and ten before/after camera-cut frames were inspected. Sectional first-flush filling is brown, the subsequent tank route blue. The intake falls toward the tank; overflow reaches the planted receiving area away from the house. The lid visibly closes an initially open tank, with ventilation rather than an airtight seal. Watering-can spout and stream endpoints were corrected to meet. The builder's final seated pose bends the legs and retains ground contact.

## Audio evidence and limits

One continuous ElevenLabs eleven_v4 request uses the literal default voice resolved from the project root .env. Source 82.64s, 183 aligned spoken words. Native alignment exactly matches the locked script tokens; captions contain no delivery tags. Faster-whisper base independently transcribed the complete source with approximately 90.7% token agreement; differences are largely joining/splitting or spelling, with uncertain recognition of jala/saringan. This is corroboration, not perceptual approval.

The rain source was generated once after a failed reuse match returned an unsuitable chime. The chime is not placed. The exact generated source, request and hashes are retained. Sound design uses one finite rain ambience track, deliberate after-rain and visitor dips, and no BGM. Additional speculative mechanical cues are intentionally omitted. The definitive cue plan is sound_design.json.

No perceptual audio input was available in this session. No claim of having listened to the pronunciation, prosody, subjective mix or joke timing is made. Full-file decoding, native alignment, independent ASR, loudness and exported mix comparison provide objective checks only.

## Authorization

Final look is agent-verified under the user's active --automation instruction; human approval is false. Scope ends at export. No content package, hosting or publication is authorized or performed.

## Export verification

Verified final export: 84.7s, 1080x1920, 30fps, 2541 H.264 yuv420p frames, AAC 48kHz stereo, 26047542 bytes. Full decode passes, zero black segments. Measured integrated loudness -13.85 LUFS and true peak -1.22 dBTP. Native speech offset is recovered with zero sample lag; the narration/rain model correlates 0.999483 with the exported audio. Mono voice duplication into stereo accounts for the different fitted source coefficients; this is an objective cue-presence check, not subjective listening.

The first export check caught double attenuation of rain: the pinned engine multiplies static gain by the volume lane. The rain static gain was corrected from 0.09 to 1, retaining the intended 0–0.09 envelope. The exact pinned HyperFrames engine's processCompositionAudio and muxVideoWithAudio functions regenerated the audio and copied the encoded video stream without any re-encoding. Stream hashes before and after match. The original render and correction receipt remain in verification/audio-correction/. The current index and reproducible assembler carry the corrected gain. No voice synthesis or frame rendering was repeated for this correction.

Twelve proof frames extracted from the final MP4 and the final six-frame 1560x2237 board were opened and visually inspected. All scene images load; names/order agree. Frame captions, first-flush fill/bypass/reset, open/closed tank, comic visitor, overflow route and watering-can contact remain visible. The initial pre-audio board is retained separately. All verification is agent work under delegated authorization; the audio-listening limitation above remains.

Final SHA-256: f0f4605d261edd47354686641dbddfe2d31b09502a61ec1d8d1770246efcb0d1. Full report: verification/export/report.json.

Preview cleanup: pinned preview --stop returned stopped; status returned not-running. A direct TCP listener query for port 3002 returned no listener, so recorded PID 28552 no longer owns that port. Capture-board helper browsers close in finally; no pipeline preview is retained.
