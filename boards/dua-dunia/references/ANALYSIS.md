# Reference Analysis — Dua Dunia

## Provenance & Coverage

- **Reference clip:** `Korupsi_Hilang_Total_Negara_Langsung_Makmur_Simulasi_20_Tahun.mp4` (`101.98s`, `608x1080`, `24.0 fps`)
- **Full local analysis archive:** `/home/ubuntu/attachments/72bba477-dec3-4bed-b5e0-60ee5a6b9ebe/_analysis/ANALYSIS.md`
- **Methods:** `rea-video decompose --no-vlm --lang en` + eye review of all 29 shots (`apply-review`), `episode_qa.py --fingerprint` (caption region masked `30,785,548,85`), `clone_measure.py`, `font_match.py`, `faster-whisper` (`small`, Indonesian word timestamps), and direct native audio listening on both full mix and isolated music stem.

## Measured Reference Fingerprint

| Metric | Reference Value | Board Contract Target |
| --- | --- | --- |
| Duration | 101.98 s | 75–115 s |
| Shot count / avg shot | 29 shots / 3.52 s | 12–34 shots (avg 2.8–4.5 s) |
| First motion / longest static | 0.20 s / 1.00 s | <= 0.50 s / <= 1.50 s |
| Held share | 1.0% | <= 10% |
| Spoken words / pace | 244 words / 2.39 wps | 180–290 words / 2.1–2.7 wps |
| First sentence end | 3.38 s | <= 4.5 s |
| Loudness / true peak | -14.0 LUFS / -1.58 dBTP | -15.5 to -12.5 LUFS / <= -0.5 dBTP |
| BGM tempo / voice margin / duck | 112.35 BPM / +28.96 dB / 2.0 dB | ~110–116 BPM / +24–30 dB / ~2 dB |

## Palette & Typography Derivation

- **Measured palette (`clone_measure.py`):** Ground/neutrals `#56595b`, `#1c3a4a`, `#777978`, `#caa584`; accents `#78afd8` (sky), `#cca683` (warm sand), `#fad668` (highlight yellow), `#78a55e` (clean green).
- **Typography substitute:** Original font name is unconfirmed (rounded geometric bold sans with thick navy outline; `font_match.py` cap height 68px, x-height 36px, stem 13px). Selected **Fredoka** (variable TTF, SIL OFL 1.1) to preserve the approachable rounded-bold silhouette.

## Deliberate User-Approved Adaptations

- **Hybrid 3D treatment (Option A, approved by user):** Instead of purely procedural boxy buildings as in the reference, `dua-dunia` uses free **Polyfork** low-poly architectural/vehicle/prop GLB assets (`nyc-city-kit-fbca88`, CC BY 4.0) vendored locally, paired with **procedural Three.js capsule characters** so facial expressions (smile/frown) remain instantly legible at phone scale.
- **No ACES tone mapping:** Adopted Polyfork's lighting rule (`NoToneMapping` / linear + sRGB output) so low-poly kit colors stay bright and clean like the reference.
- **Original illustrative subject matter:** Static studies and motion preview demonstrate the board on a completely new transfer topic (*"Angkutan Umum Gratis? Simulasi 10 Tahun: Kota Gratis vs Kota Berbayar"*).
