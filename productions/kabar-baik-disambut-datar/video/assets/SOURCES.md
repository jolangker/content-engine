# Provenance aset storyboard v1

- Seluruh ilustrasi SVG: dibuat khusus untuk episode dari skenario narasi yang disetujui; bentuk dan gestur mengikuti board ruang-di-antara v2. Tidak berasal dari foto, stok, atau temuan penelitian.
- Font lokal disalin dari boards/ruang-di-antara/assets/: Newsreader regular/italic dan DM Sans. Lisensi OFL ikut disalin ke assets/fonts/.
- GSAP 3.14.2: https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js, disimpan lokal di assets/vendor/gsap.min.js; header lisensi asli dipertahankan.
- Bukti klaim dan batas penjelasan: ../SOURCES.md pada folder produksi.

## Audio dan motion preview v1 ? 18 Oktober 2026

- Narasi: dibuat melalui ElevenLabs convert_with_timestamps, George (JBFqnCBsd6RMkjVDRZzb), eleven_multilingual_v2. Input persis assets/approved-narration.txt, satu full-script request yang berhasil, tanpa retry otomatis. Audio asli MP3 dan normalized_alignment disimpan di voice/narration-v1/.
- narration-preview.wav: turunan lokal dari narration.mp3 melalui FFmpeg atempo=0.85, PCM 44100 mono. Durasi 88.385283s. Kata tidak ditambah, dipotong, atau disintesis ulang; timestamp disesuaikan terhadap tempo, dengan potensi perbedaan lokal kecil dari time-stretch.
- Metadata dan alignment: audio_meta.json, voice/narration-v1/words.json (asli), words-preview.json (preview), captions.json. Dokumentasi filter: https://ffmpeg.org/ffmpeg-all.html#atempo.
- Motion: joint wrappers pada SVG original dari storyboard yang diterima; tanpa stok tambahan atau perubahan identitas karakter. Sumber GSAP tetap lokal.
