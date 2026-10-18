# Verifikasi preview v1 — 18 Oktober 2026

## Hasil

- 14 shot animasi, 1080×1920, 89.885 detik; suara kontinu 88.385283 detik dan hold akhir 1.5 detik.
- Naskah 175 kata dan seluruh subtitle cocok persis dengan narasi yang diterima. 45 frasa, maksimal dua baris; waktu naik berurutan, tidak ada dua frasa terlihat bersamaan atau gap antarshot.
- Full `npm run check` lolos: browser benar-benar berjalan, lint/runtime/layout/motion/contrast tanpa error atau warning. Lihat [check-preview-v1.json](boards/check-preview-v1.json).
- Penanda motion: root harus terus mengalami perubahan; semua host tampil pada waktunya dan tetap dalam frame. Audit ini memakai selector host karena ID dalam sub-komposisi mendapat namespace saat bundling. Assertion liveness per host sepanjang 90 detik sengaja tidak dipakai: host sebelum/sesudah durasinya memang tidak aktif.
- Gerak tiap ilustrasi dibuktikan terpisah dengan pasangan snapshot di wilayah y=430–1460, tanpa headline/subtitle. Semua 14 shot menunjukkan perubahan piksel. Bukti rinci di [verification-preview-v1.json](boards/verification-preview-v1.json), gambar di boards/motion-proof-v1/.
- Keyframes berhasil diekstrak dari 14 komposisi dan caption. Bukti HP juga dicapture sebagai strip; strip yang mengikuti crop objek tidak cukup menunjukkan jarak gerak, sehingga frame penuh sebelum/selama/setelah penempatan ikut diperiksa.
- Seluruh shot diperiksa sebagai PNG ukuran penuh, termasuk pembuka, tiga penekanan, aksi melepas HP, dan pertanyaan penutup. Koreksi: tangan tetap di canvas, subtitle memakai frasa yang utuh, pertanyaan terakhir ditahan sampai akhir.
- WAV lolos decode penuh FFmpeg, tidak kosong, tidak ada sampel clipping. Sumber asli MP3 dan alignment disimpan; tidak ada sintesis ulang setelah request berhasil.

## Batas pemeriksaan

CUA tidak menyediakan browser yang dapat dikontrol. Pemeriksaan UI Studio dan penilaian audio lewat pendengaran tidak diklaim sudah dilakukan. Chromium HyperFrames menjalankan audit/snapshot dengan GPU hardware Intel Iris Xe / ANGLE D3D11. Durasi file, decode, batas peak, dan kesesuaian teks/alignment diperiksa; intonasi dan tempo perlu didengar di preview. Alignment native diskalakan terhadap atempo=0.85, sehingga selisih lokal kecil dari time-stretch tetap mungkin.

## Gate

Status: **preview / awaiting_review**. Naskah v1 dan storyboard visual v1 sudah disetujui. Preview ini belum mendapat persetujuan; belum ada render/export MP4. Sesuai HyperFrames CLI, render dilakukan setelah pengguna meninjau dan menerima preview.
