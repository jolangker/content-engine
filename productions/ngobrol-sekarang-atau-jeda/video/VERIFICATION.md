# Preview v1 — 17 Oktober 2026

- Tahap terkini: export / complete. Final preview v1 disetujui pengguna melalui “ekspor”. Tidak ada publikasi.
- Narasi v1 dan layout storyboard v1 diterima pengguna. Ardi / Microsoft Edge dipilih eksplisit. Seluruh spoken text dipertahankan.
- Runtime: 65.352 detik authored; 30 fps membulatkan ke 65.366667 detik di Studio.
- Preview: http://localhost:8732/#project/video — HTTP 200 dan halaman Studio terverifikasi.

## Bukti teknis

`npx hyperframes check --json --snapshots` berhasil, browser tidak dilewati. Lint, runtime, layout, motion dan kontras masing-masing 0 error, 0 warning. Motion sidecar diperiksa pada 300 sampel. Kontras 51 dari 51 lolos.

Laporan: `.hyperframes/artifacts/checks/518a6c03-9ed2-4279-8fd1-9f5e77e09a5c.json`, revision `7903784e-4ce3-4f2a-9653-6a53f20da678`.

Snapshot tambahan pada 4, 11.188, 15.5, 20.748, 24.3, 30.404, 35, 38.38, 46.5, 53.82, 61 dan 64.652 detik di `boards/preview-v1/`. Lembar kontak diperiksa untuk pengungkapan bertahap, diagram, caption dan penutup; pose statis yang disetujui tetap di `boards/stills/`. CLI memakai hardware GPU Intel Iris Xe / ANGLE D3D11; screenshot path. Font lokal Newsreader normal, Newsreader italic dan DM Sans berhasil dimuat.

## Audio dan caption

- Enam MP3 Ardi tersedia; durasi aktual 11.088, 8.760, 8.856, 7.176, 14.640 dan 9.432 detik. Lead dan tail antaradegan ditambahkan pada timeline, bukan dengan pembagian kata merata.
- Teks native boundary cocok dengan narasi sumber pada keenam klip setelah normalisasi tanda baca. Seluruh word interval positif, monoton dan berada di dalam audio terkait.
- Mean volume per klip -18.7 hingga -17.5 dB; puncak -4.0 hingga -3.0 dB. Tidak terdeteksi clipping numerik pada pengukuran peak. Ini pengukuran berkas, bukan penilaian dengar manusia.
- Caption diadaptasi dari registry `caption-pill-karaoke`: DM Sans, palet board, 3–5 kata, timing native Microsoft WordBoundary, hard kill tiap grup. Satu track caption, enam adegan graphics, satu track audio narasi.
- Musik dan efek suara belum dipilih. Preview v1 memiliki narasi dan jeda; tidak dibuat musik pengganti secara diam-diam.

## Pemeriksaan Studio

Pemutaran nyata dari awal mencapai 01:05/01:05 dan kembali ke tombol Play. Pada sekitar detik 35, elemen voice-04 diamati berjalan (paused false), currentTime 3.856, durasi 7.176, readyState 4, tanpa media error. Seek balik dari akhir ke 30.404 dan ke 4 detik berhasil. Halaman preview, kontrol pemutar dan susunan adegan terlihat.

Peringatan lint UI yang menyebut `boards/storyboard.html` hilang setelah halaman review diberi metadata still (`data-no-timeline`). Ada toast editor caption tersimpan dari sesi UI; pada tab pemeriksaan, toast ditutup dan mode editor ditinggalkan tanpa mengubah copy. Penyimpanan edit kata melalui UI caption belum disertifikasi; revisi caption dapat dilakukan dari sumber. Playback dan source checks tetap berfungsi.

## Batas hasil

Pemeriksaan preview di atas mendahului encode. Video tidak dinyatakan sudah dinilai oleh pendengar manusia; audio diperiksa secara teknis. Persetujuan final preview dan hasil delivery kini dicatat di bawah.

Untuk menghentikan server setelah review: jalankan `npx hyperframes preview --stop` dari direktori video. Tetap nyalakan selama review.

## Delivery MP4 v1 — selesai

Persetujuan: pengguna meminta “ekspor” pada 17 Oktober 2026.

Perintah: `npx hyperframes render --quality delivery --fps 30 --workers 2 --output ../exports/ngobrol-sekarang-atau-jeda-v1.mp4`.

Render job `5cfb6dc0-de8d-485d-878d-3833069aa99a`, composition hash `fb4a7169a7d99be4`. Selesai dalam sekitar 2 menit 9 detik, screenshot capture dan hardware GPU. Compile 8.3s, audio 3.6s, setup 2.0s, capture 89.5s, encode 21.4s, assemble 3.8s.

- Output: ../exports/ngobrol-sekarang-atau-jeda-v1.mp4, 3,977,780 byte.
- Video: H.264, 1080x1920, yuv420p, 30 fps, 1961 frame; format duration 65.366667s.
- Audio: AAC, stereo 48kHz, duration 65.366s, mean -18.4 dB, peak -3.0 dB.
- Decode seluruh berkas melalui FFmpeg selesai tanpa error.
- Enam frame dari MP4 diekstrak pada 4, 20.748, 30.404, 38.38, 53.82 dan 64.652 detik, lalu ditinjau visual. Layout, warna, teks, caption dan isi keenam adegan sesuai preview. Pixel MAE terhadap proof preview antara 1.0847 dan 1.2079/255.
- Bukti: ../exports/verification-v1/export-verification.json dan decoded-contact-sheet.jpg.
- SHA-256: 5d26c952d0a1816588c54b5c15f0831fd5426cb8427417e0684959f674e03c3b.

Hasil yang diminta sudah diserahkan sebagai MP4. Caption sudah berada di dalam gambar video; cover, sidecar subtitle dan upload copy tidak termasuk permintaan ekspor ini. Tidak ada unggahan atau publikasi eksternal.
