# Content Package — Ternak Ikan Cupang di Halaman

Shared package for board `budidaya-di-halaman` (`editorial v9 / visual v5`). Use this copy unchanged across all three inherited accounts in [`boards/budidaya-di-halaman/ACCOUNTS.json`](../../boards/budidaya-di-halaman/ACCOUNTS.json): Instagram (`@bikindihalaman.id`), YouTube (`@bikindihalaman_id`), and Facebook (`Bangun Di Halaman`).

---

## Publishable Copy

### Recommended Title (71 chars — YouTube `meta.title` & first line of shared caption)

```text
Bikin Tempat Ternak Ikan Cupang di Halaman dari Boks sampai Rak Soliter
```

### Alternative Titles

1. **Problem-arc hook (73 chars):**
   ```text
   Ternak Ikan Cupang di Halaman: 7 Perbaikan dari Boks Pijah ke Rak Soliter
   ```
2. **Direct build hook (61 chars):**
   ```text
   Cara Bikin Tempat Ternak Ikan Cupang di Sudut Halaman Sendiri
   ```

### Shared Caption (987 chars — Instagram, YouTube, Facebook)

```text
Bikin Tempat Ternak Ikan Cupang di Halaman dari Boks sampai Rak Soliter

Mulai dari satu boks plastik berisi air dan sepasang ikan cupang di sudut halaman, sistemnya berkembang lewat tujuh perbaikan nyata: sekat bening perjodohan dan daun ketapang, atap plastik bening plus paranet penahan hujan dan terik, pakan mikro untuk burayak hari keempat, pindah ke bak pembesaran dengan sipon selang berkasa, rak bertingkat berisi toples soliter di bulan kedua, sekat kardus antarkedok agar cupang jantan tidak terus ngembang, serta permukaan air aman dengan tutup kasa pencegah lompat.

Catatan: visualisasi halaman, perbandingan wadah, dan jumlah ikan dalam video ini adalah ilustrasi skematis. Angka sekitar Rp500.000 adalah estimasi kasar nilai grosir untuk 50 ekor cupang siap jual (acuan harga grosir cupang Grade C Halfmoon Rp10.000–Rp20.000/ekor, Super Koi Nusantara, 4 September 2026), bukan laba bersih ataupun jaminan penghasilan.

Habis ini, apa lagi yang mau kamu bikin di halaman?

#bikindihalaman #ikancupang #ternakcupang #budidayacupang #cupanghias
```

### Hashtags (5, included at end of caption)

```text
#bikindihalaman #ikancupang #ternakcupang #budidayacupang #cupanghias
```

### Editorial Keywords (comma-separated)

```text
ternak ikan cupang, budidaya ikan cupang di halaman, cara ternak cupang pemula, pemijahan cupang daun ketapang, pakan burayak cupang, bak pembesaran cupang, rak toples soliter cupang, sekat kardus cupang, tutup kasa cupang, bikin di halaman
```

---

## Thumbnail & Video Cover

- **Thumbnail image:** [`exports/thumbnail.png`](exports/thumbnail.png) (`1080 × 1920`, PNG, `439,242` bytes, SHA-256 `726bf946327fd4e996e6888c50c0370ce4ec575768a21c03508d885c9575aa49`).
- **On-image cover text (implemented):** `Ternak cupang` / `di sudut halaman` (yellow highlight `#FFD44D` on `cupang`; identical artwork closes the video as the `0.500 s` delivered end card from `85.900 s` to `86.400 s`).
- **In-video cover offset (Trypost `meta.cover_offset_ms`):** `86150` ms (midpoint of the delivered `0.500 s` end card inside the `86400 ms` MP4).
  - **Instagram (`instagram_reel`):** `supports_video_cover: true` → set `media[0].meta.cover_offset_ms = 86150`.
  - **YouTube (`youtube_short`):** `supports_video_cover: false` → Trypost does not upload custom Shorts thumbnails; manually set `exports/thumbnail.png` in YouTube Studio if desired.
  - **Facebook (`facebook_reel`):** `supports_video_cover: false` → Trypost does not upload custom Reel covers; manually set `exports/thumbnail.png` in Meta Business Suite if desired.

---

## Delivery Metadata & Verification

| Field | Value |
| --- | --- |
| **Production slug** | `ternak-ikan-cupang` |
| **Board** | `budidaya-di-halaman` (rev 10, `editorial v9 / visual v5`, contract SHA-256 `6681a52a9464efab8b2c846a0b08b731e06fde1e9a947e9772b333d54eac9626`) |
| **Language** | Indonesian (`id-ID`, conversational second-person `"kamu"`) |
| **Intended destinations** | Inherited board set (`boards/budidaya-di-halaman/ACCOUNTS.json`, SHA-256 `1a909556b9081ab0a43a037baba6888e03306d539bd13e8b891a32ea336b7f30`): Instagram `@bikindihalaman.id` (`instagram_reel`), YouTube `@bikindihalaman_id` (`youtube_short`), Facebook `Bangun Di Halaman` (`facebook_reel`) |
| **Delivered video** | [`exports/ternak-ikan-cupang.mp4`](exports/ternak-ikan-cupang.mp4) (`21,142,701` bytes / `21.14 MB`, SHA-256 `102e77d4d6fb1bea0612a8fd4b41e539f6488a65bcf80ab2d458cef03f1247c3`) |
| **Video format** | `1080 × 1920` (9:16), H.264 / AAC, `30.0 fps` (1.25× restamped from 24 fps 1× master `108.000 s`), exact duration **`86.400 s` (`86400 ms`)** |
| **Audio loudness** | Integrated **`-14.04 LUFS`**, true peak **`-2.79 dBTP`** (two-pass loudnorm, zero clipping, `bgm: none`, 43 word-anchored organic SFX cues) |
| **Captions** | **Both:** burned-in progressive 46 px DM Sans captions + sidecar SRT [`exports/ternak-ikan-cupang.srt`](exports/ternak-ikan-cupang.srt) (`35` cues, 1.25× scaled, SHA-256 `7010f276553c1c64bcad5277d0aa4a73a99515a8726423999c79df63ad89daf4`) |
| **Quality gate** | `episode_qa.py --stage export` **passed** (`disclose: []`, [`video/verification/quality-gate-export.json`](video/verification/quality-gate-export.json)); independent jury Pass 2 **APPROVE FOR DELIVERY RENDER** (`18/18` judged rules pass, `0` open P0s, 7/7 rubric dimensions `8–9/10`, [`video/REVIEW.md`](video/REVIEW.md)) |
| **Optional platform settings** | Unset / platform defaults (YouTube `privacy_status: public`, `made_for_kids: false`, `notify_subscribers: true`; Instagram `share_to_feed: true`; no sponsorship or paid-partnership disclosure) |

---

## Credits & Source Traceability

- **Narration:** ElevenLabs `eleven_v4` voice **Roger** (`CwhRBWXzGAHq8TQ4Fs17`, user-authorized `episode_override` on `elevenlabs_api`, single 242-word take).
- **Sound effects:** 43 word-anchored organic SFX cues from the board Visual v5 CC0/Pixabay library (`boards/budidaya-di-halaman/assets/sfx/manifest.json`); BGM `none`.
- **Factual & price references:** See [`SOURCES.md`](SOURCES.md) — RRI Bengkalis / KKP (28 Sep 2026), Distankan Kab. Buleleng, Perpustakaan KKP (*Moina sp.*), UF/IFAS *Betta splendens* extension, and Super Koi Nusantara (4 Sep 2026, Grade C *Halfmoon* wholesale Rp10.000–Rp20.000/ekor; conservative Rp10.000 lower bound used for `50 ekor × Rp10.000 ≈ Rp500.000`).
