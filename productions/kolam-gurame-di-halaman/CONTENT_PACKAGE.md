# Content Package — Bikin Kolam Ikan Gurame di Halaman

Shared package for board `budidaya-di-halaman` (`editorial v9 / visual v5`). Use this copy unchanged across all three inherited accounts in [`boards/budidaya-di-halaman/ACCOUNTS.json`](../../boards/budidaya-di-halaman/ACCOUNTS.json): Instagram (`@bikindihalaman.id`), YouTube (`@bikindihalaman_id`), and Facebook (`Bangun Di Halaman`).

---

## Publishable Copy

### Recommended Title (40 chars — YouTube `meta.title` & first line of shared caption)

```text
Bikin Kolam Ikan Gurame di Sudut Halaman
```

### Alternative Titles

1. **Frame-hook angle (60 chars):**
   ```text
   Kolam Gurame Wiremesh Terpal di Halaman Sampai Panen Pertama
   ```
2. **Transformation angle (58 chars):**
   ```text
   Dari Wiremesh dan Terpal Jadi Dua Kolam Gurame di Halaman
   ```

### Shared Caption (891 chars — Instagram, YouTube, Facebook)

```text
Bikin Kolam Ikan Gurame di Sudut Halaman

Mulai dari rangka besi wiremesh melingkar berlapis terpal di sudut halaman, sistem ini berkembang lewat tujuh perbaikan khusus gurame: rendam garam dan atap paranet penahan dingin hujan, karpet talang pelindung kawat, daun talas layu di bingkai pakan apung, pipa pelimpah berkasa, pembuangan dasar plus aerasi halus, jaring anti-predator, hingga kolam kedua untuk sortir ukuran agar semua tumbuh rata.

Catatan: visualisasi halaman, perbandingan ukuran kolam, dan jumlah ikan dalam video ini adalah ilustrasi skematis. Nilai sekitar Rp1.800.000 adalah estimasi kasar harga pasar kotor untuk panen pertama 40 kg ikan konsumsi dengan acuan harga Rp45.000/kg per November 2026 (bukan laba bersih maupun jaminan penghasilan).

Habis ini, apa lagi yang mau kamu bikin di halaman?

#bikindihalaman #kolamgurame #budidayagurame #kolambundar #budidayaikan
```

### Hashtags (5, included at end of caption)

```text
#bikindihalaman #kolamgurame #budidayagurame #kolambundar #budidayaikan
```

### Editorial Keywords (comma-separated)

```text
kolam gurame di halaman, budidaya gurame kolam terpal, kolam bundar wiremesh, karpet talang kolam ikan, pakan daun talas gurame, panen ikan gurame, bikin di halaman
```

---

## Thumbnail & Video Cover

- **Thumbnail image:** [`exports/thumbnail.png`](exports/thumbnail.png) (`1080 × 1920`, PNG, `477,217` bytes, SHA-256 `fd33a0e7e1761382ca4972f782f4b998cf286e64e9d868976b45e043e`).
- **On-image cover text (implemented):** `Kolam gurame` / `di sudut halaman` (yellow highlight `#FFD44D` on `gurame`; identical artwork closes the video as the `0.500 s` delivered end card from `84.100 s` to `84.600 s`).
- **In-video cover offset (Trypost `meta.cover_offset_ms`):** `84350` ms (`84,600 ms - 250 ms`, midpoint of the delivered `0.500 s` end card inside the `84.602 s` MP4).
  - **Instagram (`instagram_reel`):** `supports_video_cover: true` → set `cover_offset_ms: 84350` on the attached video item.
  - **YouTube (`youtube_short`):** `supports_video_cover: false` → Trypost does not upload custom Shorts thumbnails; manually upload `exports/thumbnail.png` in YouTube Studio if desired.
  - **Facebook (`facebook_reel`):** `supports_video_cover: false` → Trypost does not upload custom Reel covers; manually upload `exports/thumbnail.png` in Meta Business Suite if desired.

---

## Delivery Metadata & Verification

| Field | Value |
| --- | --- |
| **Production slug** | `kolam-gurame-di-halaman` |
| **Board** | `budidaya-di-halaman` (rev 10, `editorial v9 / visual v5`, contract SHA-256 `28cb1f61279ad4254be43cabebf6967412d9e3f964e0eb4d4e3af48127c24e77`) |
| **Language** | Indonesian (`id-ID`, conversational second-person `"kamu"`) |
| **Intended destinations** | Inherited board set (`boards/budidaya-di-halaman/ACCOUNTS.json`, SHA-256 `1a909556b9081ab0a43a037baba6888e03306d539bd13e8b891a32ea336b7f30`): Instagram `@bikindihalaman.id` (`instagram_reel`), YouTube `@bikindihalaman_id` (`youtube_short`), Facebook `Bangun Di Halaman` (`facebook_reel`) |
| **Delivered video** | [`exports/kolam-gurame-di-halaman.mp4`](exports/kolam-gurame-di-halaman.mp4) (`28,704,162` bytes / `28.70 MB`, SHA-256 `1a1f1c3b7364dca876c8569098935cec63d289c46dcec8e09a2507caeddfc49e`) |
| **Video format** | `1080 × 1920` (9:16), H.264 / AAC, `30.0 fps` (1.25× restamped from 24 fps 1× master `105.750 s`), exact duration **`84.602 s`** |
| **Audio loudness** | Integrated **`-14.04 LUFS`**, true peak **`-2.42 dBTP`** (two-pass loudnorm, `bgm: none`, 41 word-anchored organic SFX cues) |
| **Captions** | **Both:** burned-in progressive 46 px DM Sans captions + sidecar SRT [`exports/kolam-gurame-di-halaman.srt`](exports/kolam-gurame-di-halaman.srt) (`51` cues, 1.25× scaled, SHA-256 `c2825ac013445948b5e49b402941ce1bba34297db293a51f74fb06d2c698da40`) |
| **Quality gate** | `episode_qa.py --stage export` **passed** (`disclose: []`, [`video/verification/quality-gate-export.json`](video/verification/quality-gate-export.json)); independent jury Pass 2 **APPROVE FOR DELIVERY RENDER** (`18/18` judged rules pass, `0` open P0s, 7/7 rubric dimensions `8.5–9.3/10`, [`video/REVIEW.md`](video/REVIEW.md)) |
| **Optional platform settings** | Unset / platform defaults (no paid sponsorship, no audience override) |

---

## Credits & Source Traceability

- **Narration:** ElevenLabs `eleven_v4` voice **Roger** (`CwhRBWXzGAHq8TQ4Fs17`, user-authorized `episode_override`, single 236-word continuous take).
- **Sound effects:** 41 word-anchored organic SFX cues from the board Visual v5 CC0/Pixabay library (`boards/budidaya-di-halaman/assets/sfx/manifest.json`); BGM `none`.
- **Factual & price references:** See [`SOURCES.md`](SOURCES.md) — Minapoli, BBPP Kupang Kementan RI (15 Apr 2024), IPB Digitani (25 Jun 2024), Distankan Kab. Buleleng, UGM Aquaculture Repository (2022), RRI Cirebon, DKP Kab. Bantul (Apr 2026: Rp43.000/kg), and FishInfo Jatim DKP Provinsi Jawa Timur (updated 27 Nov 2026: **Gurami Rp45.250/kg**; conservative rounded `Rp45.000/kg × 40 kg ≈ Rp1.800.000` gross estimate).
