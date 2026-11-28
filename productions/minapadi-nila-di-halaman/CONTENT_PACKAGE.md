# Content Package — Bikin Petak Minapadi Nila di Halaman

Shared package for board `budidaya-di-halaman` (`editorial v9 / visual v5`). Use this copy unchanged across all three inherited accounts in [`boards/budidaya-di-halaman/ACCOUNTS.json`](../../boards/budidaya-di-halaman/ACCOUNTS.json): Instagram (`@bikindihalaman.id`), YouTube (`@bikindihalaman_id`), and Facebook (`Bangun Di Halaman`).

---

## Publishable Copy

### Recommended Title (40 chars — YouTube `meta.title` & first line of shared caption)

```text
Bikin Petak Minapadi Nila di Halaman
```

### Alternative Titles

1. **Hybrid-hook angle (57 chars):**
   ```text
   Panen Padi dan Ikan Nila Sekaligus dari Minapadi Halaman
   ```
2. **Transformation angle (58 chars):**
   ```text
   Dari Terpal Lumpur Jadi Kebun Minapadi Nila di Sudut Rumah
   ```

### Shared Caption (914 chars — Instagram, YouTube, Facebook)

```text
Bikin Petak Minapadi Nila di Halaman

Mulai dari terpal isi lumpur datar untuk tanam padi dan ikan nila sekaligus di sudut halaman, sistem hybrid minapadi ini berkembang lewat tujuh perbaikan nyata: parit caren dalam di tepi agar akar padi kokoh, paranet parsial khusus di atas caren, pipa pelimpah berkasa penahan hujan, ajir jebakan bambu untuk pungut keong mas tanpa obat kimia, aerasi halus di dasar caren, jaring lengkung anti burung pipit, hingga saluran surut pelan agar nila berkumpul mudah diserok saat panen.

Catatan: visualisasi halaman, ukuran petak, dan jumlah ikan dalam video ini adalah ilustrasi skematis. Nilai sekitar Rp510.000 adalah estimasi kasar harga pasar kotor untuk panen pertama 15 kg ikan nila dengan acuan harga Rp34.000/kg per November 2026 (bukan laba bersih maupun jaminan penghasilan), sedangkan padinya untuk kebutuhan dapur sendiri.

Habis ini, apa lagi yang mau kamu bikin di halaman?

#bikindihalaman #minapadi #budidayanila #tanampadi #budidayahalaman
```

### Hashtags (5, included at end of caption)

```text
#bikindihalaman #minapadi #budidayanila #tanampadi #budidayahalaman
```

### Editorial Keywords (comma-separated)

```text
minapadi di halaman, budidaya minapadi terpal, ikan nila dan padi, parit caren minapadi, pengendalian keong mas tanpa kimia, jaring anti burung pipit, bikin di halaman
```

---

## Thumbnail & Video Cover

- **Thumbnail image:** [`exports/thumbnail.png`](exports/thumbnail.png) (`1080 × 1920`, PNG, `303,410` bytes, SHA-256 `fcf34f0d0c4220a47a506f56f9bc54bd814442eee041c3ace0b39fbf430ff662`).
- **On-image cover text (implemented):** `Bikin minapadi` / `di sudut halaman` (yellow highlight `#FFD44D` on `minapadi`; identical artwork closes the video as the `0.500 s` delivered end card from `83.700 s` to `84.200 s`).
- **In-video cover offset (Trypost `meta.cover_offset_ms`):** `83950` ms (`84,200 ms - 250 ms`, midpoint of the delivered `0.500 s` end card inside the `84.200 s` MP4).
  - **Instagram (`instagram_reel`):** `supports_video_cover: true` → set `cover_offset_ms: 83950` on the attached video item.
  - **YouTube (`youtube_short`):** `supports_video_cover: false` → Trypost does not upload custom Shorts thumbnails; manually upload `exports/thumbnail.png` in YouTube Studio if desired.
  - **Facebook (`facebook_reel`):** `supports_video_cover: false` → Trypost does not upload custom Reel covers; manually upload `exports/thumbnail.png` in Meta Business Suite if desired.

---

## Delivery Metadata & Verification

| Field | Value |
| --- | --- |
| **Production slug** | `minapadi-nila-di-halaman` |
| **Board** | `budidaya-di-halaman` (rev 10, `editorial v9 / visual v5`, contract SHA-256 `6681a52a9464efab8b2c846a0b08b731e06fde1e9a947e9772b333d54eac9626`) |
| **Language** | Indonesian (`id-ID`, conversational second-person `"kamu"`) |
| **Intended destinations** | Inherited board set (`boards/budidaya-di-halaman/ACCOUNTS.json`, SHA-256 `1a909556b9081ab0a43a037baba6888e03306d539bd13e8b891a32ea336b7f30`): Instagram `@bikindihalaman.id` (`instagram_reel`), YouTube `@bikindihalaman_id` (`youtube_short`), Facebook `Bangun Di Halaman` (`facebook_reel`) |
| **Delivered video** | [`exports/minapadi-nila-di-halaman.mp4`](exports/minapadi-nila-di-halaman.mp4) (`33,732,623` bytes / `32.17 MB`, SHA-256 `07318c436a631f29134a51157a36c260594bb9a4a685d5304219be4befb1abfb`) |
| **Video format** | `1080 × 1920` (9:16), H.264 / AAC, `30.0 fps` (1.25× restamped from 24 fps 1× master `105.250 s`), exact duration **`84.200 s`** |
| **Audio loudness** | Integrated **`-14.05 LUFS`**, true peak **`-2.76 dBTP`** (two-pass loudnorm, `bgm: none`, 37 word-anchored organic SFX cues, natively listened at 1× and 1.25×) |
| **Captions** | **Both:** burned-in progressive 46 px DM Sans captions + sidecar SRT [`exports/minapadi-nila-di-halaman.srt`](exports/minapadi-nila-di-halaman.srt) (`49` cues, 1.25× scaled, SHA-256 `4a6b7d92d7704b9aa010c36a98f758ed196d68f2d26523f4affddf20fa70a1b1`) |
| **Quality gate** | `episode_qa.py --stage export` **passed** (`disclose: []`, [`video/verification/quality-gate-export.json`](video/verification/quality-gate-export.json)); independent jury Pass 2 **APPROVE FOR DELIVERY RENDER** (`18/18` judged rules pass, `0` open P0s, 6/7 rubric dimensions `8.0/10` and `finish_texture 7.0/10`, [`video/REVIEW.md`](video/REVIEW.md)) |
| **Optional platform settings** | Unset / platform defaults (no paid sponsorship, no audience override) |

---

## Credits & Source Traceability

- **Narration:** ElevenLabs `eleven_v4` voice **Roger** (`CwhRBWXzGAHq8TQ4Fs17`, `episode_override`, single 242-word continuous take).
- **Sound effects:** 37 word-anchored organic SFX cues from the board Visual v5 CC0/Pixabay library (`boards/budidaya-di-halaman/assets/sfx/manifest.json`); BGM `none`.
- **Factual & price references:** See [`SOURCES.md`](SOURCES.md) — Pustaka BPPSDMP Kementerian Pertanian RI (*Keunggulan Budidaya Mina Padi*), KKP RI (*Pedoman Teknis Minapadi*), BRMP DIY Kementan RI (*Pengendalian OPT Burung Pipit*), KKP/FAO Minapadi Sleman benchmark, SISKAPERBAPO Jawa Timur (27 Nov 2026: Beras Medium Rp13.034/kg, Beras Premium Rp15.091/kg), and FishInfo Jatim DKP Provinsi Jawa Timur (update **28 Nov 2026**: **Nila Rp33.783/kg**; rounded `Rp34.000/kg × 15 kg ≈ Rp510.000` gross estimate).
