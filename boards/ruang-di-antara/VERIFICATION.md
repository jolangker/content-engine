# Pemeriksaan board approved v2 — 17 Oktober 2026

- Diekspor dengan `python boards/ruang-di-antara/drafts/v2/export-board.py`.
- PNG board: 1600 × 2328 piksel; tiga studi frame diekspor terpisah.
- Font lokal Newsreader regular, Newsreader italic, dan DM Sans: seluruhnya termuat.
- Pemeriksaan overflow judul, paragraf, dan frame: kosong. Page errors: kosong.
- PNG keseluruhan board serta studi close-up pengganti diperiksa secara visual; studi 01–02 mempertahankan ilustrasi dan hierarki dari ekspor sebelumnya yang sudah diperiksa. Tidak ada clipping teks atau font yang hilang; crop ilustrasi disengaja; subtitle contoh tetap terbaca.
- PDF diperiksa dengan pypdf: satu halaman.
- Semua visual board kini SVG ilustrasi. Foto referensi yang ditolak telah dihapus; sumber HTML dan ekspor terbaru tidak memakai foto/footage eksternal. Font dan lisensi tetap tersedia secara lokal.
- Contoh pacing terdiri dari 14 slot berdurasi 5, 6, 6, 5, 7, 6, 8, 7, 8, 7, 7, 6, 6, 6 detik: total 90 detik. Pembagian bagian cerita di DIRECTION.md, EDITORIAL.md, dan board konsisten. Slot adalah contoh alokasi waktu; belum ada storyboard atau episode 14 shot yang dibuat.
- Setelah persetujuan "cocok", metadata pada dokumen dan visual ditandai approved. Board diekspor ulang dengan ukuran yang sama; font termuat, overflow dan page errors tetap kosong.
- V1 diarsipkan sebelum penggantian ke `boards/ruang-di-antara/revisions/v1/` bersama asetnya. Kesamaan sembilan berkas utama salinan arsip diverifikasi melalui SHA-256.
- Paket v2 dipromosikan ke folder utama. Tracker berhasil diparse; semua path board/produksi yang terdaftar ada. Entry ruang-di-antara tetap `approved` dengan path yang sama, yang kini berisi paket aktif v2. TRACKER.json tidak memerlukan perubahan isi.
- Tidak ada berkas produksi yang diedit oleh revisi board ini. Perubahan produksi dan TRACKER.json yang sudah ada di working tree tidak disentuh.
- Belum ada demonstrasi animasi, voiceover, pengukuran durasi audio, atau video episode. Target 85–95 detik dan estimasi 170–200 kata adalah panduan perencanaan; gerak/audio di board tetap konseptual.
