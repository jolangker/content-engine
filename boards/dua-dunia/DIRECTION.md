# Dua Dunia — Board Direction & Review State

- **Board slug:** `dua-dunia`
- **Status:** `approved` (approved by user on 2026-11-23 after Rev 2 review)
- **Last updated:** 2026-11-24
- **Pending revision:** `editorial v2` drafted in `drafts/r2/` at user request (locked simulation-hook formula + soft closing CTA with the account name woven in). Awaiting user acceptance; approved `v1` remains the usable version until promoted.

## Approved Vision & Adaptation Decisions

- **Source reference:** `Korupsi Hilang Total, Negara Langsung Makmur, Simulasi 20 Tahun.mp4` (`101.98s`, `608x1080`, `24 fps`). Full analysis and provenance in `references/ANALYSIS.md`.
- **Hybrid 3D craft (Option A — approved by user):**
  - **Environments, buildings, vehicles, and props:** Locally vendored low-poly `.glb` models from Polyfork (`nyc-city-kit-fbca88`, CC BY 4.0): `city-bus-49fd97.glb`, `compact-hatchback-386417.glb`, `town-car-56eeb6.glb`, `one-storey-shop-row-83c958.glb`, `brick-tenement-7d2014.glb`, `street-tree-0d33f3.glb`. Placed at real metre scale (`y = 0`, Y-up) with `THREE.NoToneMapping` and `THREE.SRGBColorSpace`.
  - **Characters:** Procedural Three.js capsule citizens (`assets/kit-3d.js`) with readable dot eyes, smile/frown curves, and optional sunglasses/ties for fast phone-size emotion recognition.
- **Typography:** Locally bundled open-licensed `Fredoka-Variable.ttf` (SIL OFL 1.1) with dark navy (`#142A36`) stroke and hard drop shadow.
- **Illustrative transfer topic:** *"Angkutan Umum Gratis? Simulasi 10 Tahun"* (original non-reference topic used across all 4 studies and the 15-second motion preview).

## Artifacts & Verification Summary

### Static Style Board & Studies
- `style-board.html` → `style-board.png`
- `studies/studies.html` → `studies/hook.png`, `studies/split.png`, `studies/mechanism.png`, `studies/data.png`
- Visual inspection fixes applied before delivery:
  - Centered `HALTE BUS` diegetic plaque inside the hook frame (`x = 0.35`) so the right edge no longer clips.
  - Shortened hook and mechanism captions to a single crisp line inside the `[54, 1380, 972, 200]` band.
- Reference look comparison (`compare_frames.py`):
  - Hook study vs reference `shot_001_first.jpg`: **72.3%** palette neighborhood overlap.
  - Data HUD study vs reference `shot_022_last.jpg`: **96.0%** palette neighborhood overlap.

### Playable Motion Preview (HyperFrames — Rev 2)
- Source: `motion-preview/index.html` + `motion-preview/assets/pilot-3d.js` + `motion-preview/audio/pilot-mix.wav`
- Rendered output: `motion-preview.mp4` (`17.0s`, `1080x1920`, `30.0 fps`, `10.6 MB`, AAC 48 kHz stereo)
- Revision fixes applied after user review:
  1. **Audio added & verified:** Indonesian `eleven_v4` narration (`Samsul - Warm & Clear Narrator`, `AfkBqzsATOuueGnLAvJi`) + deterministic playful acoustic-guitar/mallet BGM (`112 BPM`, F major) with sidechain ducking, mixed to `-14.13 LUFS` / `-1.41 dBTP` and verified via `describe_audio` (clean pronunciation, zero read-aloud tags, balanced vocal-over-BGM mix). Captions word-synced via `faster-whisper` timestamps.
  2. **Bustling city crowd:** Added 22–26 walking procedural capsule NPCs along both sidewalks (`populatePedestrians` / `stepPedestrians`), plus additional Polyfork skyline tenements, trees, and traffic across all scenes and static studies.
  3. **Natural character animation:** Replaced vertical hopping on standing characters with hip/waist/neck/shoulder-pivoted articulation (`animateStandingCitizen`: feet planted, subtle breathing + head look/nod + relaxed arm sway) and real alternating leg/arm stride cycles (`animateWalkingCitizen`) for walking NPCs.
- `hyperframes check`: **Passed** (`0` runtime errors, `0` motion errors/warnings, `0` craft warnings, `0` audio warnings, `40/40` WCAG AA contrast checks passed).
- `episode_qa.py --fingerprint motion-preview.mp4 --caption-region 54,1380,972,200`:
  - `first_motion_seconds`: `0.2s` (contract `<= 0.5s`)
  - `longest_static_seconds`: `0.0s` (contract `<= 1.5s`)
  - `held_share`: `0.0` (contract `<= 0.10`)
  - `integrated_lufs`: `-14.13` (contract `-15.5..-12.5`)
  - `true_peak_dbtp`: `-1.41` (contract `<= -0.5`)
  - `caption_region_masked`: `true`
- `episode_qa.py --contract boards/dua-dunia`: **Valid**.

## Approved Configuration & Remaining Optional Setup

- **Board voice config (`AUDIO.json`):** Configured to `AfkBqzsATOuueGnLAvJi` (*Samsul — Warm & Clear Narrator*, Indonesian male, `eleven_v4`).
- **Publishing accounts (`ACCOUNTS.json`):** Empty (`[]`) until configured.
- **Next step:** Review `drafts/r2/` (editorial v2); on acceptance, promote to the board root and preserve `v1` under `revisions/1/`.
