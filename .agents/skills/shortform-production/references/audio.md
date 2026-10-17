# Audio generation and resolution

Gunakan panduan ini untuk mengeksekusi tahap `audio` pada produksi short-form: menghasilkan narasi (voiceover), sound effects (SFX), background music (BGM), serta mengunci durasi nyata dan timestamp kata untuk caption.

## 1. Peran dan Kriteria Tahap Audio

Tahap audio menjembatani naskah (`SCRIPT.md`) dan visual storyboard (`STORYBOARD.md`) dengan produksi animasi final di HyperFrames:
- Mengonversi narasi naskah menjadi file audio nyata.
- Mengukur durasi sebenarnya audio utuh (`duration_s`) dan rentang waktu tiap adegan untuk menggantikan estimasi kasar di storyboard.
- Menghasilkan word-level timestamps (alignment) yang dibutuhkan oleh sistem caption HyperFrames.
- Selesai ketika seluruh narasi, SFX, dan musik yang diminta brief/board tersedia, durasinya terukur, dan timing adegan diperbarui.

## Default voiceover: full script, satu request

Untuk produksi di workspace ini, gabungkan seluruh teks narasi yang sudah disetujui menjadi satu input TTS dan kirim dalam satu request sintesis agar alur dan karakter suara konsisten. Pertahankan tanda baca dan jeda paragraf; arahan visual dan teks layar tetap berada di luar input narasi.

Pada shared engine, gunakan tepat satu entri `lines` dengan ID `narration` berisi full script. Setiap entri diproses sebagai request TTS terpisah, sehingga pembagian adegan dilakukan setelah sintesis melalui timestamp kata pada audio utuh. Simpan pemetaan rentang kata/waktu ke scene di `STORYBOARD.md`; gunakan satu track voiceover kontinu sebagai acuan animasi dan caption. SFX ditata mengikuti timing adegan tersebut.

Jika batas input provider mengharuskan pemecahan, jelaskan batas yang ditemukan dan gunakan sesedikit mungkin bagian pada jeda narasi alami. Permintaan eksplisit pengguna untuk sintesis per bagian juga dapat mengganti default ini. Saat naskah direvisi, regenerasi full narasi secara default; reuse audio yang masih sesuai tanpa request ulang.

## 2. Pemilihan Engine dan Provider

### Voiceover (TTS) — Khususnya Bahasa Indonesia
TTS lokal bawaan (Kokoro) **tidak mendukung** Bahasa Indonesia. Oleh karena itu, gunakan provider dengan dukungan multibahasa berkualitas tinggi:
1. **ElevenLabs (Rekomendasi Utama)**:
   - Gunakan skill `text-to-speech` yang terpasang di workspace atau integrasi ElevenLabs di `media-use`.
   - Model: `eleven_multilingual_v2` (sangat stabil untuk narasi berdurasi panjang) atau `eleven_v4` (ekspresif, mendukung audio tags).
   - **Otomatisasi `.env`**: Engine audio secara otomatis membaca file `.env` di root workspace.
     - `ELEVENLABS_API_KEY`: Otomatis dimuat untuk autentikasi panggilan TTS.
     - `ELEVENLABS_VOICE_ID`: Otomatis menjadi voice ID default jika tidak di-override di naskah/request.
2. **HeyGen TTS**:
   - Digunakan bila lingkungan terhubung dengan akun HeyGen aktif (`heygen auth login` / `HEYGEN_API_KEY`).
3. **Rekaman Pengguna (Host Audio)**:
   - Jika pengguna memilih merekam suara sendiri, simpan audio di lokasi aset dan lewati sintesis otomatis.

### Sound Effects (SFX)
1. **Library Bawaan**: Gunakan 19-file library SFX bawaan di `.agents/skills/media-use/assets/sfx/` untuk efek transisi standar (*whoosh*, *pop*, *click*, *riser*).
2. **ElevenLabs Sound Effects**: Gunakan skill `sound-effects` untuk menghasilkan efek suara spesifik atau tekstur atmosfer dari deskripsi teks.

### Background Music (BGM)
- Pilih trek musik instrumen yang tipis/halus sesuai mood board (misal: *calm reflective*, *cinematic lofi*).
- Hindari musik yang menabrak frekuensi narasi vokal (gunakan teknik ducking/voiceover carve di tahap assembly HyperFrames).

## 3. Jalur Eksekusi (Execution Paths)

Pilih salah satu dari dua jalur berikut sesuai kebutuhan:

### Jalur A: Shared HyperFrames Audio Engine (`media-use`) — Disukai untuk Full Pipeline
Engine `media-use/audio/scripts/audio.mjs` mengotomatisasi TTS, SFX, transkripsi Whisper (word timestamps), dan penyusunan `audio_meta.json` dalam satu kali jalan:

1. Buat `productions/<slug>/video/audio_request.json`:
   ```json
   {
     "provider": "elevenlabs",
     "lang": "id",
     "voice": "<VOICE_ID_DARI_ENV_ATAU_BOARD>",
     "speed": 1.0,
     "lines": [
       { "id": "narration", "text": "Seluruh narasi yang disetujui, dari awal sampai akhir. Pertahankan tanda baca dan jeda paragraf." }
     ],
     "bgm": {
       "mode": "none"
     }
   }
   ```
2. Jalankan engine dari root proyek atau folder video:
   ```bash
   node .agents/skills/media-use/audio/scripts/audio.mjs --request ./productions/<slug>/video/audio_request.json --hyperframes ./productions/<slug>/video --out ./productions/<slug>/video/audio_meta.json
   ```
3. Untuk ElevenLabs, engine memakai `convert_with_timestamps`: audio dan alignment karakter dikembalikan oleh satu request TTS. Engine mengubah alignment menjadi timestamp kata (mengutamakan `normalized_alignment`, lalu `alignment`). Transkripsi lokal dipakai hanya jika keduanya tidak tersedia atau tidak valid; kegagalan request TTS tidak memicu sintesis ulang otomatis. Gunakan SDK ElevenLabs yang menyediakan metode tersebut.
4. Engine menghasilkan aset di `video/.media/audio/` dan memetakan word timestamps di `audio_meta.json`.

### Jalur B: Direct CLI / SDK Invocation (`text-to-speech`)
Bila menggunakan jalur langsung, kirim full narasi dalam satu pemanggilan sintesis. Contoh di bawah memakai placeholder teks; saat eksekusi gunakan seluruh narasi yang disetujui:

1. Gunakan CLI ElevenLabs atau script Python:
   ```bash
   elevenlabs text-to-speech convert \
     --voice-id <VOICE_ID> \
     --model-id eleven_multilingual_v2 \
     --text "Seluruh teks narasi yang disetujui..." \
     --output ./productions/<slug>/video/assets/audio/vo_full.mp3
   ```
2. Jalur CLI langsung di atas belum mengambil alignment native. Jika membutuhkan timestamp tanpa transkripsi tambahan, gunakan Jalur A. Untuk audio manual atau hasil tanpa alignment, jalankan transkripsi lokal:
   ```bash
   npx hyperframes transcribe ./productions/<slug>/video/assets/audio/vo_full.mp3 --language id --dir ./productions/<slug>/video
   ```

## 4. Standar Lokasi Penyimpanan File

Semua file audio yang digunakan untuk rendering wajib berada di dalam struktur folder `video/` agar dapat diakses oleh runtime HyperFrames:

```text
productions/<slug>/video/
  audio_request.json        Konfigurasi permintaan audio (opsional jika pakai engine)
  audio_meta.json           Metadata durasi nyata, word timestamps, dan path file
  .media/audio/
    voice/                  File WAV/MP3 voiceover full script
    sfx/                    File efek suara
    bgm/                    File musik latar
  assets/audio/             Alternatif penempatan file audio manual
```

## 5. Sinkronisasi ke Storyboard dan Tahap Lanjutan

Setelah file audio ter-generate:
1. **Perbarui `STORYBOARD.md`**: Petakan timestamp kata dari `audio_meta.json` ke batas tiap adegan pada audio utuh, lalu perbarui durasi dan waktu mulai/akhir adegan. Durasi total voiceover bukan durasi setiap adegan.
2. **Perbarui `EPISODE.md`**: Catat model suara, voice ID, durasi total riil, dan status approval audio.
3. **Update `TRACKER.json`**:
   - Jika audio selesai: ubah `stage: "production"`, `status: "in_progress"`.
4. Lanjutkan ke tahap `production` untuk mengompilasi adegan di HyperFrames.
