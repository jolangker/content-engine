# Content package: Bikin Kolam Lele di Halaman

Single shared package for all three accounts configured in [boards/budidaya-di-halaman/ACCOUNTS.json](../../boards/budidaya-di-halaman/ACCOUNTS.json), per `budidaya-di-halaman` Editorial v8. Use the exact title, caption, hashtags, and keywords unchanged across Instagram (`@bikindihalaman.id`), YouTube (`@bikindihalaman_id`), and Facebook (`Bangun Di Halaman`).

## Title

- **Recommended (54 chars — YouTube `meta.title` and first line of shared caption):** Bikin Kolam Lele di Halaman dari Patok Kayu dan Terpal
- **Alternative 1 (62 chars):** 7 Masalah Bikin Kolam Lele Terpal di Halaman dan Cara Atasinya
- **Alternative 2 (55 chars):** Dari Patok Kayu Jadi Kolam Lele Stabil di Pojok Halaman

## Shared caption (Instagram Reels, YouTube Shorts, Facebook Reels)

```text
Bikin Kolam Lele di Halaman dari Patok Kayu dan Terpal

Cuma modal patok kayu dan terpal di pojok rumah, kolam lele bisa langsung jadi. Supaya tahan panas, hujan deras, sampai panen pertama, ini tujuh perbaikan bertahap yang dipasang di kolamnya:

1. Paranet peneduh di atas rangka biar air kolam dangkal nggak cepat kepanasan.
2. Alas sekam dan karung pelapis rangka biar terpal aman dari ujung kayu tajam.
3. Pipa pelimpah berkasa supaya air hujan keluar tapi lele tetap di dalam.
4. Sambungan pipa ke bedengan sayur biar jalan setapak kering dan tanaman ikut tersiram.
5. Keran kuras dasar ke bedengan untuk buang endapan pelet dan kotoran.
6. Jaring penutup di atas rangka buat menghalau kucing di malam hari.
7. Sortir serokan dan sekat jaring biar ukuran lele seragam dan nggak saling gigit.

Catatan: Ini ilustrasi skala halaman rumah dengan alur waktu yang dipersingkat. Angka ≈ Rp345.000 adalah estimasi kotor harga pasar (15 kg × Rp23.000/kg, merujuk panel FishInfo DKP Provinsi Jawa Timur Nov 2026 Rp23.163/kg yang dibulatkan konservatif), belum dikurangi biaya pembuatan, benih, maupun pakan, dan bukan janji keuntungan.

Habis ini, apa lagi yang mau kamu bikin di halaman?

#kolamlele #budidayalele #kolamterpal #ternaklele #bikindihalaman
```

## Hashtags

`#kolamlele #budidayalele #kolamterpal #ternaklele #bikindihalaman`

## Keywords (editorial)

`kolam lele di halaman, kolam terpal rangka kayu, budidaya lele rumahan, paranet kolam lele, pipa pelimpah kolam, keran kuras kolam terpal, sortir lele, jaring penutup kolam, ternak lele pemula, bikin di halaman`

## Thumbnail & cover

- **Shared thumbnail PNG:** [exports/thumbnail.png](exports/thumbnail.png) (`1080 × 1920`, `159,986` bytes, SHA-256 `f30ce9388a5e27ef0995a6365fd9e0a0781bb8d8620e9f4776e2c67e34d0a28f`).
- **Cover headline (implemented):** `Bikin kolam lele` (`kolam lele` in `#FFD44D`) / `di halaman` on `#281D18EB` panel over dusk-slate finished yard inside the central `1080 × 1080` safe square.
- **In-video end card:** Final `0.5 s` of [exports/kolam-lele-di-halaman.mp4](exports/kolam-lele-di-halaman.mp4) (`0.625 s` at 1x) is an exact copy of the thumbnail.
- **Cover delivery by channel:**
  - **Instagram (`instagram_reel`, `supports_video_cover: true`):** Set video `meta.cover_offset_ms = 87317` (`87567 ms − 250 ms`).
  - **YouTube (`youtube_short`, `supports_video_cover: false`):** Manual upload of [exports/thumbnail.png](exports/thumbnail.png) in YouTube Studio.
  - **Facebook (`facebook_reel`, `supports_video_cover: false`):** Manual upload of [exports/thumbnail.png](exports/thumbnail.png) in Meta Business Suite / Facebook.

## Delivery metadata

| Field | Value |
| --- | --- |
| Production slug / board | `kolam-lele-di-halaman` / `budidaya-di-halaman` (Editorial v8, Visual v4) |
| Language | Indonesian |
| Destinations | Instagram `@bikindihalaman.id` (`instagram_reel`), YouTube `@bikindihalaman_id` (`youtube_short`), Facebook `Bangun Di Halaman` (`facebook_reel`) |
| Delivered video (1.25x) | [exports/kolam-lele-di-halaman.mp4](exports/kolam-lele-di-halaman.mp4) (`18,701,174` bytes / `18.70 MB`), SHA-256 `2701a63156487fbedb7cdf24bc7724725c2c1e08a17eb9546d0f1be413f64410` |
| Format | MP4, H.264 (`yuv420p`) + AAC 48 kHz stereo, `1080 × 1920` (9:16), `30 fps`, `87.567 s` (`87567 ms`, retimed 1.25x from 24 fps `109.458 s` 1x master) |
| Loudness | `−14.05 LUFS` integrated, `−2.8 dBTP` true peak (passed export gate) |
| Captions | Burned in + sidecar [exports/kolam-lele-di-halaman.srt](exports/kolam-lele-di-halaman.srt) (54 cues, SHA-256 `57d58fa29d986545a5bb4a7ec4dd2c02789c34520effb7295921efdcc2bb51b7`) |
| Thumbnail | [exports/thumbnail.png](exports/thumbnail.png) (SHA-256 `f30ce9388a5e27ef0995a6365fd9e0a0781bb8d8620e9f4776e2c67e34d0a28f`) |
| Quality gate | Export gate `passed` (`disclose: []`) — [video/verification/quality-gate-export.json](video/verification/quality-gate-export.json) |
| Audio credits | Narration: ElevenLabs `eleven_v4` voice `Roger` (`CwhRBWXzGAHq8TQ4Fs17`, user-authorized `episode_override`). BGM: `none`. SFX: bundled `media-use` library (`video/assets/audio/CREDITS.md`). |
| Factual references | Verified in [SOURCES.md](SOURCES.md) (FishInfo DKP Prov. Jawa Timur update 24 Nov 2026 `Rp23.163/kg`, DKP Bantul Apr 2026 `Rp25.000/kg`, KKP / BPPBAT / Ditjen Perikanan Budidaya & FAO *Clarias gariepinus* guidance). |

Publication date, timezone schedule, visibility, audience designation, and sponsorship declarations remain intentionally unset for draft delivery.
