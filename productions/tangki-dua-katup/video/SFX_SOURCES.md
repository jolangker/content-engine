# Reused sound assets

No new paid sound generation. No narration regeneration. These are designed illustrative textures and material accents, not a field recording or calibrated acoustic simulation of the depicted cistern.

Reuse scan: board v4 has no frozen sound library; bundled library has UI/impact/whoosh textures, no water. Existing rail episode has generated water and material Foley with matching receipts. Openverse resolver queries for small metal chain rattle and rubber flap returned bundled pop/click-soft, rejected as literal Foley. Those fetched candidates are unused.

Playback listening is unavailable to this helper. Waveform/onset, duration, source receipt and hash checks were performed; perceptual approval is not claimed. Root must verify the placed mix and its export.

The source snippets are retained under `assets/audio/sfx/sources/`. Prior generated sources retain their original prompts and hashes. Their applicability here is an editorial timbre choice, not evidence of the mechanism's sound. Bundled whoosh is sourced under the Pixabay Content License; attribution is not required by that license.

| Asset | Duration | Role / use |
|---|---:|---|
| `handle-contact` | 0.520s | Restrained short hinge/latch movement for the lever press and return; not literal toilet-handle recording. |
| `chain-contact` | 0.220s | Thin brief metallic contact to mark chain take-up or engagement; not a continuous chain-rattle claim. |
| `rubber-seat` | 0.380s | Soft low wet contact accent at flap reseating; adapted puddle Foley, not actual flapper acoustics. |
| `water-flow` | 12.000s | Close small-stream water texture for sustained tank discharge or overflow; shortened in placement to follow motion. |
| `water-refill` | 12.000s | Lighter filtered water texture for incoming refill, distinct from the fuller discharge bed; source is a generated small stream. |
| `section-reveal` | 0.420s | Quiet airy cutaway/reassembly cue; never used to imply a physical internal mechanism sound. |

## Sources

- Prior production: `productions/rel-bukan-dua-batang-besi/video/assets/audio/sfx/`, original ElevenLabs `eleven_text_to_sound_v2` generated assets and request receipts. Reused water was generated as a small stream in a concrete drainage channel; flow/refill are cropped, filtered and crossfaded adaptations.
- Bundled `whoosh-short.mp3`: `.agents/skills/media-use/audio/assets/sfx/CREDITS.md`; [Pixabay Content License](https://pixabay.com/service/license-summary/).
- [ElevenLabs terms](https://elevenlabs.io/terms-of-use) retained as provider reference; no assertion of CC0 licensing for generated assets.

Exact treatment commands, input/output hashes, durations and source prompts are recorded in `assets/audio/sfx/assets.json`.
