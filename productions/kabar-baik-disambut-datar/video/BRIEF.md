---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Kabar baik dapat diberi ruang untuk dinikmati bersama lewat perhatian dan rasa ingin tahu terhadap cerita pasangan."
destination: vertical-shortform
aspect: 1080x1920
language: id
length: 89.885s
angle: narrative
narration: yes
board: ruang-di-antara
board_revision: v2
script_version: v1
---

## Intent

Episode untuk orang dewasa yang merefleksikan hubungan romantis. Pengguna memilih ide 4, “Lo bawa kabar baik. Dia cuma jawab, ‘Oh, bagus.’”, lalu menerima narasi lengkap 175 kata pada 18 Oktober 2026 melalui “cocok”. Naskah sumber yang disetujui: [../SCRIPT.md](../SCRIPT.md). Pilar Di antara kita; satu adegan presentasi yang dipuji atasan, satu konsep berbagi pengalaman positif, satu contoh respons, satu pertanyaan pengamatan.

## Customizations

- Board pilihan pengguna: [EDITORIAL.md](../../../boards/ruang-di-antara/EDITORIAL.md) dan [DIRECTION.md](../../../boards/ruang-di-antara/DIRECTION.md), v2 approved 17 Oktober 2026. Spec khusus board digunakan, tanpa menggantinya dengan preset generik.
- Seluruh visual berupa ilustrasi dan grafis; tidak ada foto/B-roll. Palet krem, arang, bata, pasir; font Newsreader dan DM Sans lokal dengan lisensi.
- Teks penekanan default 0–5 kata, satu kelompok per shot. Subtitle satu sampai dua baris pendek pada area tersendiri, tidak menutup tindakan penting.
- Target awal 14 shot bermakna, minimal 11; sekitar 90 detik (85–95 detik). Beri variasi adegan ruang, detail tangan/HP, sudut pandang, dan gestur.

## Notes

- Confirmed: board v2, topik, isi dan register narasi v1. Contoh dialog dan adegan adalah ilustrasi; riset dan batas klaim di [../SOURCES.md](../SOURCES.md).
- Default/derived: 9:16 1080×1920 mengikuti contoh board dan format short-form; 30 fps untuk proyek. Platform unggah spesifik belum dipilih dan tidak memengaruhi storyboard ini.
- Run shape: flow automation mengikuti preferensi personal yang sudah dibaca; storyboard yes dan mode collaborative mengikuti checkpoint proyek. Ini tidak melewati review naskah/storyboard/final preview.
- Narasi dan enam beat editorial diterima pada checkpoint naskah; perincian 14 shot dan layout ditinjau bersama pada checkpoint storyboard visual, sesuai penggabungan review proyek.
- Current endpoint: final preview dengan narasi dan animasi; menunggu review sebelum export.
- Default audio: George dari ELEVENLABS_VOICE_ID workspace, eleven_multilingual_v2, tanpa BGM/SFX. Ini pilihan eksekusi, bukan preferensi voice yang dipilih eksplisit pengguna.
- Satu request sintesis full script yang berhasil; MP3 75.139773s. Shared engine tidak menghasilkan audio, lalu direct SDK dengan format MP3 dipakai; tidak ada retry sintesis otomatis.
- Preview memakai turunan WAV atempo=0.85, durasi terukur 88.385283s; hold akhir 1.5s. Timing kata berasal dari normalized_alignment native dan diskalakan 1/0.85; ada potensi selisih lokal kecil dari time-stretch.
- Layout yang disetujui dibekukan di boards/approved-storyboard-v1/. Gerak dibuat inline karena izin native delegation belum diberikan; tidak ada sub-agent.
- Registry dicari untuk gestur SVG dan caption editorial. Kandidat Lottie mengganti karakter yang sudah diterima; komponen UI/typing tidak cocok untuk sendi ilustrasi ini. Gerak pada SVG asli dipertahankan; tidak memasang efek baru.
- Final preview tetap membutuhkan persetujuan tersendiri sebelum render.

## Persetujuan storyboard dan eksekusi preview

Storyboard visual v1, seluruh 14 shot, diterima pengguna melalui “cocok” pada 18 Oktober 2026. Layout, hierarki, dan copy pada pose tersebut menjadi acuan animasi. Endpoint berikutnya: final preview dengan narasi, menunggu review tersendiri sebelum export. Narasi memakai default workspace ELEVENLABS_VOICE_ID (George), model eleven_multilingual_v2, satu request full script dengan alignment native. Rencana music none dipertahankan untuk versi ini.
