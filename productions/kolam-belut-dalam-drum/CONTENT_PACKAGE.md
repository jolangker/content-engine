# Content package: Bikin Kolam Belut dalam Drum Bekas

Single shared package for all three accounts configured in [boards/budidaya-di-halaman/ACCOUNTS.json](../../boards/budidaya-di-halaman/ACCOUNTS.json), per `budidaya-di-halaman` Editorial v9. Use the exact title, caption, hashtags, and keywords unchanged across Instagram (`@bikindihalaman.id`), YouTube (`@bikindihalaman_id`), and Facebook (`Bangun Di Halaman`).

## Title

- **Recommended (44 chars — YouTube `meta.title` and first line of shared caption):** Bikin Kolam Belut di Halaman dari Drum Bekas
- **Alternative 1 (62 chars):** 7 Masalah Bikin Kolam Belut dalam Drum Bekas dan Cara Atasinya
- **Alternative 2 (56 chars):** Dari Drum Plastik Bekas Jadi Kolam Belut Stabil di Rumah

## Shared caption (Instagram Reels, YouTube Shorts, Facebook Reels)

```text
Bikin Kolam Belut di Halaman dari Drum Bekas

Drum plastik bekas yang direbahkan di sudut halaman bisa jadi kolam belut rumahan. Tapi tanpa persiapan lengkap, belut bisa merayap kabur saat hujan malam dan lumpur mentah bikin belut lemas. Ini tujuh perbaikan bertahap sampai kolamnya stabil dan panen pertama:

1. Pipa pelimpah berkasa di bawah bibir drum supaya air hujan keluar tapi belut tetap tertahan.
2. Fermentasi lumpur dua minggu sampai dingin dan tidak bergas sebelum bibit dimasukkan kembali.
3. Eceng gondok dan paranet peneduh di atas drum biar air tidak kepanasan dan terlalu silau saat tengah hari.
4. Geser jadwal pakan ke sore hari sesuai sifat aktif malam belut agar pakan langsung habis.
5. Keran kuras bawah dan pipa tetes air bersih untuk mencegah air keruh dan bau amonia.
6. Tutup rangka kawat kasa di atas bukaan drum buat menghalau kucing di malam hari.
7. Sortir ukuran dan pindahkan belut kecil ke drum kedua supaya tidak saling gigit dan tumbuh rata.

Catatan: Ini ilustrasi skala halaman rumah dengan alur waktu yang dipersingkat. Angka ≈ Rp435.000 adalah estimasi kotor harga pasar (6 kg × Rp72.500/kg, merujuk panel FishInfo DKP Provinsi Jawa Timur periode 20–26 Nov 2026), belum dikurangi biaya drum, bibit, maupun pakan, dan bukan janji keuntungan.

Habis ini, apa lagi yang mau kamu bikin di halaman?

#kolambelut #budidayabelut #belutdrum #ternakbelut #bikindihalaman
```

## Hashtags

`#kolambelut #budidayabelut #belutdrum #ternakbelut #bikindihalaman`

## Keywords (editorial)

`kolam belut drum bekas, budidaya belut di halaman, cara ternak belut drum plastik, fermentasi lumpur belut, pipa pelimpah kolam belut, eceng gondok kolam belut, paranet kolam, pakan belut sore hari, sortir ukuran belut, bikin di halaman`

## Thumbnail & cover

- **Shared thumbnail PNG:** [exports/thumbnail.png](exports/thumbnail.png) (`1080 × 1920`, `516,654` bytes, SHA-256 `1a4e8e448b964df6824d8c1e2edc4cae1e58a8d29d11a02b49eeecf75355e123`).
- **Cover headline (implemented):** `Bikin kolam belut` (`kolam belut` in `#FFD44D`) / `di drum bekas` on `#281D18E6` panel over dusk-slate finished dual-drum yard inside the central `1080 × 1080` safe square.
- **In-video end card:** Final `0.50 s` of [exports/kolam-belut-dalam-drum.mp4](exports/kolam-belut-dalam-drum.mp4) (`0.625 s` at 1x) is an exact match of the thumbnail.
- **Cover delivery by channel:**
  - **Instagram (`instagram_reel`, `supports_video_cover: true`):** Set video `meta.cover_offset_ms = 88050` (`88300 ms − 250 ms`).
  - **YouTube (`youtube_short`, `supports_video_cover: false`):** Manual upload of [exports/thumbnail.png](exports/thumbnail.png) in YouTube Studio.
  - **Facebook (`facebook_reel`, `supports_video_cover: false`):** Manual upload of [exports/thumbnail.png](exports/thumbnail.png) in Meta Business Suite / Facebook.

## Delivery metadata

| Field | Value |
| --- | --- |
| Production slug / board | `kolam-belut-dalam-drum` / `budidaya-di-halaman` (Revision 10 — Editorial v9 / Visual v5) |
| Language | Indonesian |
| Destinations | Instagram `@bikindihalaman.id` (`instagram_reel`), YouTube `@bikindihalaman_id` (`youtube_short`), Facebook `Bangun Di Halaman` (`facebook_reel`) |
| Delivered video (1.25x) | [exports/kolam-belut-dalam-drum.mp4](exports/kolam-belut-dalam-drum.mp4) (`26,817,959` bytes / `26.82 MB`), SHA-256 `1ede5ca2ae9d59779b9cca3317ff763182e2c78e36d245ca4bfd31cee1d8a752` |
| Format | MP4, H.264 (`yuv420p`) + AAC 48 kHz stereo (`192 kbps`), `1080 × 1920` (9:16), `30 fps`, `88.300 s` (`88300 ms`, retimed 1.25x from 24 fps `110.375 s` 1x master) |
| Loudness | `−13.99 LUFS` integrated, `−2.85 dBTP` true peak (passed export gate) |
| Captions | Burned in + sidecar [exports/kolam-belut-dalam-drum.srt](exports/kolam-belut-dalam-drum.srt) (`36` cues, SHA-256 `48d811c614c6933a7ee762f622ec98c2963644653dff7f097266098ea3075edd`) |
| Thumbnail | [exports/thumbnail.png](exports/thumbnail.png) (SHA-256 `1a4e8e448b964df6824d8c1e2edc4cae1e58a8d29d11a02b49eeecf75355e123`) |
| Quality gate | Export gate `passed` (`disclose: []`) — [video/verification/quality-gate-export.json](video/verification/quality-gate-export.json) |
| Audio credits | Narration: ElevenLabs `eleven_v4` voice `Roger` (`CwhRBWXzGAHq8TQ4Fs17`, user-authorized `episode_override`). BGM: `none`. SFX: 41 organic cues from board Visual v5 library ([video/assets/audio/CREDITS.md](video/assets/audio/CREDITS.md)). |
| Factual references | Verified in [SOURCES.md](SOURCES.md) (FishInfo DKP Prov. Jawa Timur 20–26 Nov 2026 `Belut: Rp72.500/kg`, DPMD Prov. Jatim, Kalurahan Sidoagung Sleman, Pemdes Badamita Banjarnegara, FishBase / IUCN GISD / JEB 2018 / MDPI *Antioxidants* Oct 2026). |

Queue scheduling uses each account's configured Trypost posting schedule (`Asia/Jakarta`); visibility, audience designation, and sponsorship declarations remain at provider defaults / unset.
