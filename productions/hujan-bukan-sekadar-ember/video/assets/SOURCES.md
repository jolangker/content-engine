# Asset provenance

## Original episode work

House, solid terrain layers, tank, first-flush section, gutter, screens, overflow, vegetation, articulated builder, chair, watering can and theatrical mosquito/luggage are original procedural Three.js geometry in `world.js`. No pixels or models were extracted from the board's creative-reference videos. The board's v1 identity, color tokens and character clothing guide the new geometry.

## Fonts and code dependencies

- Barlow regular, bold and black, copied byte-for-byte from `boards/bongkar-sistem/assets/`; license retained at `fonts/Barlow-OFL.txt`.
- IBM Plex Mono regular from the same board; license retained at `fonts/IBM-Plex-Mono-OFL.txt`.
- Three.js 0.181.2, frozen from the official npm package in `vendor/three.module.js` and `vendor/three.core.js`. MIT text retained at `vendor/THREE-LICENSE.txt`.
- GSAP 3.14.2, frozen from the official npm package in `vendor/gsap.min.js`; published license reference retained at `vendor/GSAP-LICENSE.txt`.
- HyperFrames CLI pinned to 0.8.195 in `package.json`. All render-time code and font assets are local.

## Audio

- Narration: one full-script ElevenLabs `eleven_v4` request; root `.env` default voice resolved and validated by the maintained workspace entry point. Immutable source MP3, native alignment, payload fingerprint and hashes are together in `.media/audio/voice/`. API credentials are never copied into production files. `audio/narration-master.wav` changes gain only and preserves native speed.
- Rain: one original ElevenLabs `eleven_text_to_sound_v2` generation, 12 seconds, looping, no music or speech requested. Full prompt, request fingerprint and source hash are in `audio/rain-loop.json`. `audio/rain-bed.wav` is a finite local repetition with a measured track envelope. This generated ambience is an illustrative sound treatment, not an acoustically calibrated recording of the model.
- An unsuitable bundled chime returned by the resolver remains in the media ledger as an unused candidate; it is never mounted on the timeline.
- No BGM or other unrecorded SFX source is used. `sound_design.json` is the definitive cue list; `.media/manifest.jsonl` records source provenance and local hashes.
