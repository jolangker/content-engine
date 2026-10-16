# Episode — kerja-rodi-daendels

## Konteks & Brief v1 — 17 Oktober 2026

- **Topik Dipilih Pengguna:** "Kerja Rodi Jalan Daendels — Benarkah Tanpa Upah?" (Topik 02 dari Pilar 02: *Mitos Buku Teks vs Fakta Lapangan*).
- **Board Terpilih:** `berkas-polemik` ([Editorial Framework v1](../../boards/berkas-polemik/EDITORIAL.md) dan [Visual Direction v1](../../boards/berkas-polemik/DIRECTION.md)).
- **Konsep Kreatif:** *Forensic Dossier* (Meja Investigasi Sejarah). Membuka dokumen kas kolonial dan surat keputusan Daendels 1808 yang bertolak belakang dengan narasi umum buku teks sekolah.
- **Tujuan Konten:** Penonton menyadari adanya anomali dalam mitos sejarah sekolah (bahwa Daendels tidak membayar sepeser pun), melihat bukti dokumen tandingan (anggaran 30.000 ringgit perak dan upah bertingkat), dan memahami kenyataan pahit rantai feodal di mana upah ditahan oleh bupati lokal sementara rakyat jelata tetap menjadi korban.
- **Audiens Sasaran:** Generasi muda dan audiens digital yang ingin melihat sejarah Indonesia secara kritis, berbasis dokumen dan data primer, bukan simplifikasi hitam-putih.
- **Bahasa & Diksi:** Bahasa Indonesia formal-aksesibel, lugas, terukur, dan objektif. Menghindari bahasa santai gaul (lo–gua) agar menjaga gravitasi tragedi kemanusiaan, namun bebas dari kalimat pasif bertele-tele.
- **Format Spesifikasi:** 9:16 vertical short-form (1080x1920), 30 fps, target durasi 68 detik.
- **Identitas Visual:** Token visual mengikuti `boards/berkas-polemik/frame.md` (latar karbon `#121110`, kertas manila `#EAE0D0`, merah stempel `#C32822`, tipografi Space Grotesk, Space Mono, Newsreader).
- **Arahan Audio:** Narator bertindak sebagai penyidik arsip yang tenang dan presisi; jeda 0.5 detik sebelum pengungkapan bukti krusial. SFX pengetikan mesin tik / geseran berkas / stempel dokumen.

## Kebutuhan Riset & Batasan Historiografi

1. **Bukti Dokumen Primer:** Pelacakan arsip keputusan (*Resolutie*) Mei 1808 era Herman Willem Daendels dan bukti alokasi anggaran 30.000 ringgit perak serta ransum beras-garam.
2. **Historiografi Akademis:** Mengacu pada temuan disertasi Prof. Dr. Djoko Marihandono (FIB UI) mengenai sentralisasi pemerintahan Daendels dan De Grote Postweg, serta analisis Peter Carey mengenai kekerasan kolonial dan konteks klaim Mayor William Thorn (12.000 korban).
3. **Pembeda Fakta vs Tafsir:**
   - Menyatakan dengan jujur bahwa Daendels memang mengalokasikan anggaran untuk upah dan logistik pada tahap awal (Cisarua–Cirebon).
   - Menjelaskan bahwa pada tahap kedua (Cirebon–Panarukan), kas menipis akibat blokade laut Inggris, sehingga Daendels menuntut bupati mengerahkan kerja wajib feodal (*heerendiensten*).
   - Menganalisis alasan mengapa rakyat merasa tidak digaji: kebuntuan dan korupsi di tingkat feodal lokal di mana bupati/priyayi menahan uang upah dan menganggap pengerahan rakyat adalah hak tradisional.
   - Menghindari pembenaran kekejaman Daendels: target waktu militer yang sangat kejam dan wabah penyakit tetap menyebabkan ribuan nyawa rakyat jelata melayang.

## Endpoint & Perilaku Review

- **Endpoint:** Menghasilkan produksi video short-form lengkap hingga pratinjau dan ekspor terverifikasi.
- **Checkpoint Default Proyek:**
  1. *Review Naskah (`SCRIPT.md`)* — **disetujui pengguna pada 17 Oktober 2026 ("setuju")**.
  2. *Review Storyboard Visual (`STORYBOARD.md` & layout board visual)* — **disetujui pengguna pada 17 Oktober 2026 ("setuju")**.
  3. *Review Pratinjau Final Audiovisual* — **tahap aktif saat ini (`awaiting_review`)**.

## Status dan Tindakan Berikutnya

- Naskah v1 dan Storyboard Visual v1 telah disetujui pengguna.
- Audio voiceover disintesis lengkap untuk 7 adegan menggunakan model `id-ID-ArdiNeural` (+8% rate) dengan ekstraksi penanda waktu kata (word boundaries) sinkron presisi. Total durasi komposisi: **69.508 detik** (2086 frame @ 30 fps).
- Sub-komposisi *Pill Karaoke Captions* selesai diintegrasikan di `video/compositions/captions.html` pada area aman y=1580–1690px.
- Animasi GSAP terpasang pada seluruh 7 frame (stempel bertinta dengan back easing, redaction sweep, counter angka dinamis, alur rantai feodal, dan slide penutup).
- Pemeriksaan teknis `npx hyperframes check` lolos sempurna: 0 error, 0 warning, 63/63 WCAG contrast checks passed.
- Server HyperFrames Studio aktif pada port 8740: `http://localhost:8740/#project/video`.
- Lembar kontak bukti pratinjau diekspor ke [preview-v1/contact-sheet.jpg](video/boards/preview-v1/contact-sheet.jpg).
- Status dicatat di tracker: `stage: preview`, `status: awaiting_review`.
- **Menunggu persetujuan/umpan balik pengguna atas Pratinjau Final Audiovisual (Checkpoint 3)** sebelum mengekspor MP4 delivery final.
