# Ngobrol sekarang atau jeda

## Brief v1 — 17 Oktober 2026

- Topik dipilih pengguna: ide 2, ketika satu orang ingin membahas masalah sekarang dan pasangannya meminta jeda.
- Arah episode: memperlihatkan urutan saling mendesak dan menjauh dalam skenario ilustratif, kemudian membedakan jeda dengan percakapan yang dibiarkan menggantung.
- Board: `ruang-di-antara`, editorial v1 dan visual direction v1. Pengguna memilih ide yang ditawarkan dalam konteks board ini; pemakaian board mengikuti konteks pilihan tersebut.
- Pegangan: [editorial](../../boards/ruang-di-antara/EDITORIAL.md) dan [visual direction](../../boards/ruang-di-antara/DIRECTION.md).
- Tujuan: penonton mengenali urutan respons dan membawa pulang contoh meminta jeda yang mencakup rencana kembali berbicara.
- Audiens usulan: orang dewasa yang ingin merefleksikan komunikasi dalam hubungan romantis.
- Bahasa: Indonesia, register lo–gua sesuai board.
- Format final: 9:16, 1080x1920, 30 fps, 65.366667 detik; narasi Ardi dan dua pemeran abstrak. Platform unggah belum ditentukan. Versi v1 memakai narasi dan jeda tanpa musik/SFX tambahan.
- Format editorial: pola yang diperlihatkan; satu situasi, satu pola, satu kemungkinan respons.
- Narasi SCRIPT.md v1 disetujui dan dibuat dengan Ardi / Microsoft Edge pilihan pengguna. Timing animasi dan caption memakai metadata kata native. Runtime komposisi 65,352 detik; pada timeline 30 fps tampil sekitar 65,367 detik.
- Jalur HyperFrames: faceless-explainer; workflow terpasang dan proyek diinisialisasi di `video/`. Konteks eksekusi tersedia di `video/BRIEF.md`; pilihan suara/provider serta musik tetap terbuka sebelum audio.
- Hasil akhir: delivery MP4 v1 selesai dan terverifikasi. Final preview v1 disetujui melalui perintah “ekspor” pada 17 Oktober 2026.

## Kebutuhan riset

1. Definisi dan batas pola demand–withdraw pada konflik pasangan.
2. Dukungan untuk jeda saat percakapan memanas dan pentingnya kembali ke percakapan.
3. Hindari menyimpulkan motif, diagnosis, attachment style, perbedaan gender, atau tanggung jawab yang selalu setara dari satu adegan.

## Status dan langkah berikutnya

Riset selesai dalam batas kebutuhan naskah; bukti dan batasnya dicatat di SOURCES.md. SCRIPT.md v1 disetujui pengguna pada 17 Oktober 2026 melalui respons “cocok” atas narasi lengkap yang ditampilkan. Storyboard v1 diterima melalui “cocok” berikutnya. Narasi Ardi dipilih secara eksplisit lewat pertanyaan suara. Final preview v1 diterima melalui “ekspor”. Status: export / complete.

Storyboard v1: [board HTML](video/boards/storyboard.html), [gambar keseluruhan](video/boards/storyboard.png), dan [rencana adegan](video/STORYBOARD.md). Enam adegan mencakup keenam beat naskah pada estimasi 0–65 detik. Semua adegan memiliki pose HTML yang dimuat pada index utama dan still berukuran 1080x1920. Narasi sumber 124 kata tetap identik; salinan siap TTS tersegmentasi di video/SCRIPT.md.

Verifikasi storyboard: snapshot HyperFrames pada 4,13,25,35,48,60 detik berhasil; tiga font lokal dimuat. Keenam still diperiksa visual pada resolusi penuh. Garis umpan balik frame 3 dipindah agar tidak menabrak label. Board memuat keenam PNG secara utuh, tanpa page error atau overflow teks pada pemeriksaan board. Bukti di video/boards/verification.json. Ini verifikasi pose statis; belum mengklaim kelulusan check animasi, timing audio, caption, atau audiovisual preview.

Preview v1: http://localhost:8732/#project/video . Server berjalan di background; respons HTTP 200 diverifikasi. Enam adegan dianimasikan dari layout yang disetujui, enam klip narasi Ardi ada di video/assets/voice/, caption ada dalam satu sub-komposisi/track. Narasi 124 kata tidak berubah; metadata berisi 125 token karena istilah demand–withdraw terpisah menjadi dua boundary. Perbandingan teks ternormalisasi cocok untuk keenam klip. Preview ini memakai narasi dan jeda; musik/SFX belum dipilih.

Final preview v1 disetujui pengguna pada 17 Oktober 2026 melalui perintah “ekspor”. Berkas final: [ngobrol-sekarang-atau-jeda-v1.mp4](exports/ngobrol-sekarang-atau-jeda-v1.mp4), 3,977,780 byte (3.8 MiB), H.264/yuv420p, 1080x1920, 30 fps, 1961 frame, durasi 65.366667 detik; audio AAC stereo 48 kHz. Full decode tidak melaporkan error. Enam decoded frames ditinjau visual dan dibandingkan dengan preview (mean absolute pixel error 1.08–1.21/255, sesuai kompresi video). Bukti: exports/verification-v1/export-verification.json dan decoded-contact-sheet.jpg. Tidak ada publikasi yang diminta atau dilakukan.

Verifikasi animasi: `hyperframes check --json --snapshots` lolos tanpa error/warning pada lint, runtime, layout, motion dan kontras; 300 sampel motion, 51/51 pemeriksaan kontras lolos. Dua belas proof frames di video/boards/preview-v1/ ditinjau, termasuk adegan awal, proses diagram dan penutup. Playback Studio mencapai 01:05/01:05; audio adegan 4 diamati aktif, readyState 4 dan tanpa media error. Tidak mengklaim pemeriksaan pendengaran manusia atau encode MP4 final. Bukti rinci: video/VERIFICATION.md.

CLI proyek dinaikkan 0.8.164 → 0.8.165 dan lolos check setelah upgrade. Panggilan awal Edge TTS 7.2.8 ditolak HTTP 403; dependensi 7.3.1 dipasang terisolasi di video/.media/tts-packages dan berhasil. Tidak ada kredensial/provider berbayar yang dipakai. Pengaturan Ardi +15% memberi runtime sesuai target; take awal -12% terlalu panjang dan tidak dipakai dalam preview.

Catatan workflow: enam beat editorial telah ditampilkan bersama naskah dan diterima melalui “cocok”; review storyboard sekarang mencakup layout dan visualnya, sehingga persetujuan atas narasi yang sama tidak diminta ulang. Custom frame.md mengadaptasi board yang telah disetujui, bukan mengganti identitas dengan preset generik.

Pemeriksaan penggunaan HyperFrames pada awal pekerjaan berhasil: status known. Angka ini hanya snapshot awal, bukan reservasi; periksa lagi pada milestone eksekusi berikutnya.
