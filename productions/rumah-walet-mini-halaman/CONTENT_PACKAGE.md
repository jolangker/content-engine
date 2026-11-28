# Content Package — Bikin Rumah Burung Walet Mini di Halaman

Shared package for board `budidaya-di-halaman` (`editorial v9 / visual v5`). Use this copy unchanged across all three inherited accounts in [`boards/budidaya-di-halaman/ACCOUNTS.json`](../../boards/budidaya-di-halaman/ACCOUNTS.json): Instagram (`@bikindihalaman.id`), YouTube (`@bikindihalaman_id`), and Facebook (`Bangun Di Halaman`).

---

## Publishable Copy

### Recommended Title (40 chars — YouTube `meta.title` & first line of shared caption)

```text
Bikin Rumah Burung Walet Mini di Halaman
```

### Alternative Titles

1. **System-keys angle (53 chars):**
   ```text
   7 Kunci Rumah Walet Mini di Halaman Biar Koloni Betah
   ```
2. **Transformation angle (57 chars):**
   ```text
   Dari Dinding Bata Kosong Jadi Rumah Walet Mini di Halaman
   ```

### Shared Caption (1,100 chars — Instagram, YouTube, Facebook)

```text
Bikin Rumah Burung Walet Mini di Halaman

Mulai dari susunan dinding bata berlubang dan suara panggil di sudut halaman, rumah burung walet (RBW) mini ini berkembang lewat tujuh perbaikan nyata: sekat gelap pembatas ruang inap, pipa ventilasi PVC siku ke bawah penahan cahaya, bak air dangkal pelembap lantai, papan sirip kayu beralur kasar agar kuku walet mencengkeram kuat, suara inap pelan di papan sirip, bingkai seng licin anti tokek di sekeliling lubang masuk, hingga panen sarang kosong siang hari setelah anakan terbang.

Catatan: visualisasi halaman, skala bangunan, dan alur waktu dalam video ini adalah ilustrasi skematis. Kolonisasi walet liar sangat bergantung pada lokasi, jalur lintas burung, dan waktu berbulan-bulan hingga setahun lebih. Nilai sekitar Rp831.000 adalah estimasi kasar harga pengepul kotor untuk panen perdana 100 g (~13 sarang mangkok kering) dengan acuan Rp8.310/g (Rp8.310.000/kg) per Agustus 2026 — bukan laba bersih maupun jaminan hasil.

Habis ini, apa lagi yang mau kamu bikin di halaman?

#bikindihalaman #rumahwalet #sarangwalet #budidayawalet #budidayahalaman
```

### Hashtags (5, included at end of caption)

```text
#bikindihalaman #rumahwalet #sarangwalet #budidayawalet #budidayahalaman
```

### Editorial Keywords (comma-separated)

```text
rumah burung walet mini, rbw mini di halaman, budidaya sarang burung walet, sekat gelap rumah walet, pipa ventilasi siku walet, papan sirip walet, bingkai seng anti tokek, panen sarang walet penetasan, bikin di halaman
```

---

## Thumbnail & Video Cover

- **Thumbnail image:** [`exports/thumbnail.png`](exports/thumbnail.png) (`1080 × 1920`, PNG, `408,436` bytes, SHA-256 `c86e8eed25abfb148ce8fee879843d6a1c07d2fa141723d27ca1e54e6d30d52c`).
- **On-image cover text (implemented):** `Bikin rumah` / `walet mini` (yellow highlight `#FFD44D` on `walet mini`; identical artwork closes the video as the `0.500 s` delivered end card from `83.200 s` to `83.700 s`).
- **In-video cover offset (Trypost `meta.cover_offset_ms`):** `83450` ms (`83,700 ms - 250 ms`, midpoint of the delivered `0.500 s` end card inside the `83.700 s` MP4).
  - **Instagram (`instagram_reel`):** `supports_video_cover: true` → set `cover_offset_ms: 83450` on the attached video item.
  - **YouTube (`youtube_short`):** `supports_video_cover: false` → Trypost does not upload custom Shorts thumbnails; manually upload `exports/thumbnail.png` in YouTube Studio if desired.
  - **Facebook (`facebook_reel`):** `supports_video_cover: false` → Trypost does not upload custom Reel covers; manually upload `exports/thumbnail.png` in Meta Business Suite if desired.

---

## Delivery Metadata & Verification

| Field | Value |
| --- | --- |
| **Production slug** | `rumah-walet-mini-halaman` |
| **Board** | `budidaya-di-halaman` (rev 10, `editorial v9 / visual v5`, contract SHA-256 `6681a52a9464efab8b2c846a0b08b731e06fde1e9a947e9772b333d54eac9626`) |
| **Language** | Indonesian (`id-ID`, conversational second-person `"kamu"`) |
| **Intended destinations** | Inherited board set (`boards/budidaya-di-halaman/ACCOUNTS.json`, SHA-256 `098943ff65eaf188fd7ea3a1b4e769e0729f78269e896a789af8e13c624e1d94`): Instagram `@bikindihalaman.id` (`instagram_reel`), YouTube `@bikindihalaman_id` (`youtube_short`), Facebook `Bangun Di Halaman` (`facebook_reel`) — local package only (`delivery: package`; no external Trypost upload/publishing performed) |
| **Delivered video** | [`exports/rumah-walet-mini-halaman.mp4`](exports/rumah-walet-mini-halaman.mp4) (`19,080,060` bytes / `18.20 MB`, SHA-256 `8801d5999d8a4538945ccfa366afd1e66dd30a1e291e446a793206df9e448ace`) |
| **Video format** | `1080 × 1920` (9:16), H.264 High (`yuv420p`) / AAC 48 kHz (`187 kbps`), `30.0 fps` (`2,511` frames; 1.25× restamped from 24 fps 1× master `104.625 s`), exact duration **`83.700 s`** |
| **Audio loudness** | Integrated **`-14.03 LUFS`**, true peak **`-2.44 dBTP`** (two-pass linear `loudnorm`, `bgm: none`, 44 frame-locked organic SFX cues, natively listened at 1× and 1.25×) |
| **Captions** | **Both:** burned-in centered 46 px DM Sans karaoke captions + sidecar SRT [`exports/rumah-walet-mini-halaman.srt`](exports/rumah-walet-mini-halaman.srt) (`42` cues, 1.25× scaled, `3,000` bytes, SHA-256 `b582d481f3733f6f01b633fe28d458109cb081c4b5b59cdb4ec23c62223d0484`) |
| **Quality gate** | `episode_qa.py --stage export` **passed** (`disclose: []`, [`video/verification/quality-gate-export.json`](video/verification/quality-gate-export.json)); independent jury Pass 2 **APPROVE FOR DELIVERY RENDER** (`18/18` judged rules pass, `0` open P0s, all `7/7` rubric dimensions `8.0/10`, [`video/REVIEW.md`](video/REVIEW.md)) |
| **Optional platform settings** | Unset / platform defaults (no paid sponsorship, no audience override) |

---

## Credits & Source Traceability

- **Narration:** ElevenLabs `eleven_v4` board default voice **Pribs – Friendly Casual Narration** (`5g0yKK2JwTRka0IG61Hh`, `board_config`, single 240-word continuous take).
- **Sound effects:** 44 frame-locked organic SFX cues from the board Visual v5 CC0/Pixabay library (`boards/budidaya-di-halaman/assets/sfx/manifest.json`); BGM `none`.
- **Factual & price references:** See [`SOURCES.md`](SOURCES.md) — PUSTAKA BPPSDMP Kementerian Pertanian RI (*Beternak Burung Walet*, Sep 2024; *Mengenal dan Mencegah Hama Burung Walet*, Mar 2023), Markas Walet technical & national price guides (Nov–Dec 2024; national collector raw-nest benchmark **03 Aug 2026**: **Mangkok Rp8.310.000/kg** = `Rp8.310/g`, used for `100 g × Rp8.310 ≈ Rp831.000` gross estimate), Dunia Walet (2023), PT Rumah Burung Indonesia Jaya (Dec 2025), Jurnal Teknik Sipil UAJY Vol. 12 No. 2 (2013), Jurnal Peternakan Lingkungan Tropis UNMUL Vol. 4 No. 2 (2021), JSSM Universiti Malaysia Terengganu Vol. 16 No. 4 (2021), and Universitas Brawijaya Repository (2023).
