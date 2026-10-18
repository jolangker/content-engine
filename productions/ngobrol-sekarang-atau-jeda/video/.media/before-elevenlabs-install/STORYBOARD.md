---
format: 1080x1920
duration: 65.352s
message: "Kenali urutan mendesak–menjauh; bila perlu jeda, sepakati kapan kembali membahasnya."
arc: story-explainer with how-to
audience: orang dewasa yang merefleksikan komunikasi dalam hubungan
mode: collaborative
music: none
---

# Storyboard v1 disetujui — animasi preview v1

## Pemetaan audio terkini — v3 ElevenLabs

Pengguna mengoreksi provider menjadi ElevenLabs; v3 menggantikan take Ardi v2 sebagai acuan audio. Satu full-script request, voice George `JBFqnCBsd6RMkjVDRZzb` dari konfigurasi proyek, model `eleven_multilingual_v2`, durasi 59.118005 detik. Audio dan metadata di `assets/voice/narration-v3-elevenlabs/`. Rentang kata memakai indeks awal inklusif/akhir eksklusif, berbasis alignment native. Pemetaan ini belum diterapkan pada animasi/caption v1.

| Frame | Rentang adegan v3 (detik) | Rentang ucapan (detik) | Indeks kata |
| --- | --- | --- | --- |
| 1 | 0.000–10.403 | 0.035–9.706 | 0–19 |
| 2 | 10.403–19.157 | 10.403–18.553 | 19–40 |
| 3 | 19.157–29.966 | 19.157–29.455 | 40–62 |
| 4 | 29.966–37.013 | 29.966–36.978 | 62–75 |
| 5 | 37.013–50.492 | 37.013–49.981 | 75–105 |
| 6 | 50.492–59.118 | 50.492–58.933 | 105–124 |

Pemetaan v2 dan detail motion v1 di bawah adalah riwayat; gunakan metadata v3 untuk pekerjaan selanjutnya.

## Pemetaan audio v2 — belum diterapkan ke animasi

Regenerasi narasi utuh Ardi +15% pada 17 Oktober 2026 menghasilkan satu file berdurasi 59.448 detik. Metadata: `assets/voice/narration-v2/audio_meta.json`; audio: `assets/voice/narration-v2/narration-ardi-full.mp3`. Rentang berikut merupakan acuan sinkronisasi berikutnya, bukan timing komposisi v1 yang masih aktif. Batas adegan berikutnya mengikuti awal kata pertamanya; jeda antarbeat termasuk adegan sebelumnya. Indeks kata memakai awal inklusif dan akhir eksklusif.

| Frame | Rentang adegan v2 (detik) | Rentang ucapan v2 (detik) | Indeks kata |
| --- | --- | --- | --- |
| 1 | 0.000–11.072 | 0.100–10.343 | 0–19 |
| 2 | 11.072–19.750 | 11.072–18.930 | 19–40 |
| 3 | 19.750–28.492 | 19.750–27.761 | 40–63 |
| 4 | 28.492–35.583 | 28.492–34.854 | 63–76 |
| 5 | 35.583–50.101 | 35.583–49.373 | 76–106 |
| 6 | 50.101–59.448 | 50.101–58.721 | 106–125 |

Layout yang disetujui tetap menjadi pegangan. Catatan motion dan timing pada bagian v1 di bawah merupakan riwayat implementasi lama dan perlu disinkronkan sebelum preview v2. Audio v2 belum mendapat review pendengaran pengguna.

Narasi v1 disetujui pada 17 Oktober 2026. Enam beat editorial dari naskah dipertahankan. Layout disetujui pengguna melalui “cocok” pada 17 Oktober 2026. Timing disinkronkan dengan suara Ardi pilihan pengguna dan metadata kata native. Board PNG tetap merupakan bukti layout yang disetujui. `music: none` mencegah pemilihan musik otomatis sebelum kebutuhan audio disepakati.

## Video direction

Dua pemeran organik tanpa wajah; warna bukan kode gender/kebenaran. Krem dominan, satu frame arang untuk pengalaman batin. Newsreader untuk suara batin/refleksi; DM Sans untuk konsep. Jarak dan garis menyatakan urutan respons. Tidak ada sentuhan dramatis atau pemulihan ajaib pada penutup. Sisihkan y=1500–1650 bagi caption nanti; isi utama berakhir sebelum y=1500; area bawah y>=1650 dan sisi kanan x>=930 bebas isi utama. Preview animasi memakai satu track caption Pill Karaoke yang diadaptasi ke DM Sans dan palet board; band caption y=1600–1716 menjaga footer pose yang disetujui.

Referensi langsung: board ruang-di-antara v1; SCRIPT.md dan SOURCES.md di folder induk. Penamaan pola berdasarkan S1; opsi jeda dan rencana kembali berdasarkan S2. Monolog batin dan jam 20.00 adalah ilustrasi.

Pencarian katalog: `cycle diagram circular arrows connected nodes` (tier words). Flowchart/sticky notes dan constellation hub tersedia; belum cocok dengan metafora dua pemeran serta urutan umpan balik board ini. Diagram SVG khusus mempertahankan bahasa visual board, tanpa efek baru.

## Frame 1 — Sekarang / nanti (0-11.888s)

- act: Pengenalan
- status: animated
- review: layout_approved
- src: compositions/frames/01-sekarang-nanti.html
- duration: 11.888s
- poster: 11.188s
- transition_in: cut
- type: hook
- persuasion: Concretization
- beat: recognition
- scene: Sekarang. / Nanti aja.
- voiceover: Lo pengen beresin sekarang. Dia bilang, “Nanti aja.” Lo tanya lagi. Dia makin diam. Lo makin mendesak. Dia pergi.

narrativeRole: Mengenali situasi kecil yang menahan percakapan.

keyMessage: Keinginan membahas dan respons menunda dapat berbenturan.

Pose statis: lihat boards/stills/ dan board HTML. Teks layar utama: Sekarang. / Nanti aja.

Saat animasi nanti: pertahankan layout ini setelah disetujui; pecah kemunculan sesuai frasa narasi dan timing rekaman. Gerak tidak dibuat sebelum review visual. Sumber dan batas: Dialog/monolog ilustratif; kemungkinan pengalaman batin.

- blueprint: compose
- focal: Sekarang. / Nanti aja.
- roles: dua pemeran = foreground subject; tipografi = supporting; field krem/arang = background

Scene 1 (0.120–0.920s): sequential reveal pada #scene-01-display-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 2 (0.120–0.920s): sequential reveal pada #scene-01-figure-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 3 (0.120–0.920s): relational position change pada #scene-01-figure-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 4 (2.350–3.150s): sequential reveal pada #scene-01-figure-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 5 (2.350–3.150s): relational position change pada #scene-01-figure-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 6 (3.263–4.063s): sequential reveal pada #scene-01-display-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 7 (4.817–5.617s): relational position change pada #scene-01-figure-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 8 (4.817–5.617s): sequential reveal pada #scene-01-figure-3, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 9 (6.426–7.226s): sequential reveal pada #scene-01-foot-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 10 (8.600–9.400s): relational position change pada #scene-01-figure-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 11 (10.143–10.943s): relational position change pada #scene-01-figure-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 12 (10.343–11.143s): sequential reveal pada #scene-01-figure-2, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing

## Frame 2 — Dua kemungkinan suara batin (11.888-21.448s)

- act: Pengenalan
- status: animated
- review: layout_approved
- src: compositions/frames/02-suara-batin.html
- duration: 9.56s
- poster: 20.748s
- transition_in: cut
- type: pain_point
- persuasion: Concretization
- beat: recognition
- scene: Kapan gue didengerin? / Gue lagi kewalahan.
- voiceover: Di kepala lo, mungkin: “Kalau ditunda, kapan gue didengerin?” Di kepala dia, bisa jadi: “Gue udah nggak bisa dengerin kalau begini.”

narrativeRole: Membuka dua kemungkinan pengalaman batin tanpa menetapkan motif.

keyMessage: Kita belum tahu alasan masing-masing hanya dari perilakunya.

Pose statis: lihat boards/stills/ dan board HTML. Teks layar utama: Kapan gue didengerin? / Gue lagi kewalahan.

Saat animasi nanti: pertahankan layout ini setelah disetujui; pecah kemunculan sesuai frasa narasi dan timing rekaman. Gerak tidak dibuat sebelum review visual. Sumber dan batas: Dialog/monolog ilustratif; kemungkinan pengalaman batin.

- blueprint: compose
- focal: Kapan gue didengerin? / Gue lagi kewalahan.
- roles: dua pemeran = foreground subject; tipografi = supporting; field krem/arang = background

Scene 1 (0.120–0.920s): sequential reveal pada #scene-02-maybe-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 2 (2.139–2.939s): sequential reveal pada #scene-02-quote-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 3 (3.117–3.917s): sequential reveal pada #scene-02-figure-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 4 (4.546–5.346s): sequential reveal pada #scene-02-line-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 5 (4.796–5.596s): sequential reveal pada #scene-02-maybe-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 6 (6.730–7.530s): sequential reveal pada #scene-02-quote-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 7 (6.850–7.650s): sequential reveal pada #scene-02-figure-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing

## Frame 3 — Pola yang berulang (21.448-31.104s)

- act: Memahami pola
- status: animated
- review: layout_approved
- src: compositions/frames/03-pola-berulang.html
- duration: 9.656s
- poster: 30.404s
- transition_in: cut
- type: product_intro
- persuasion: Demonstration
- beat: clarity
- scene: Mendesak → menjauh → makin mendesak; Pola demand–withdraw
- voiceover: Kalau desakan dibalas dengan menjauh, lalu makin didesak lagi, percakapannya bisa masuk pola demand–withdraw: satu terus menekan pembahasan, satu terus menarik diri.

narrativeRole: Memperlihatkan urutan respons sebagai pola, bukan tipe orang.

keyMessage: Desakan dan penarikan diri dapat membentuk urutan berulang.

Pose statis: lihat boards/stills/ dan board HTML. Teks layar utama: Mendesak → menjauh → makin mendesak; Pola demand–withdraw

Saat animasi nanti: pertahankan layout ini setelah disetujui; pecah kemunculan sesuai frasa narasi dan timing rekaman. Gerak tidak dibuat sebelum review visual. Sumber dan batas: S1; urutan ilustratif, bukan kesimpulan sebab-akibat.

- blueprint: compose
- focal: Mendesak → menjauh → makin mendesak; Pola demand–withdraw
- roles: dua pemeran = foreground subject; tipografi = supporting; field krem/arang = background

Scene 1 (0.578–1.378s): sequential reveal pada #scene-03-figure-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 2 (0.618–1.418s): sequential reveal pada #scene-03-rail-label-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 3 (1.222–2.022s): svg-path-draw pada #scene-03-leg-a, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → svg-path-draw
Scene 4 (1.372–2.172s): sequential reveal pada #scene-03-figure-2, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 5 (1.412–2.212s): sequential reveal pada #scene-03-rail-label-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 6 (2.374–3.174s): svg-path-draw pada #scene-03-leg-b, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → svg-path-draw
Scene 7 (2.524–3.324s): sequential reveal pada #scene-03-figure-3, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 8 (2.564–3.364s): sequential reveal pada #scene-03-rail-label-2, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 9 (2.824–3.624s): sequential reveal pada #scene-03-heads, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 10 (4.459–5.259s): sequential reveal pada #scene-03-part-scene-03-display-0-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 11 (4.622–5.422s): sequential reveal pada #scene-03-part-scene-03-display-0-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 12 (6.274–7.074s): sequential reveal pada #scene-03-rail-sub-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 13 (7.817–8.617s): sequential reveal pada #scene-03-rail-sub-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 14 (7.817–8.617s): svg-path-draw pada #scene-03-return, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → svg-path-draw
Scene 15 (8.146–8.946s): sequential reveal pada #scene-03-foot-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 16 (8.617–9.417s): sequential reveal pada #scene-03-return-head, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing

## Frame 4 — Jeda yang diperjelas (31.104-39.08s)

- act: Memahami pola
- status: animated
- review: layout_approved
- src: compositions/frames/04-kapan-lanjut.html
- duration: 7.976s
- poster: 38.38s
- transition_in: cut
- type: benefit_highlight
- persuasion: Question→answer pairing
- beat: clarity
- scene: Kapan kita lanjut?
- voiceover: Tapi meminta jeda belum tentu berarti menghindar. Coba perjelas kapan obrolannya dilanjutkan. Misalnya:

narrativeRole: Membedakan satu permintaan jeda dari pola menghindar.

keyMessage: Kapan kembali berbicara perlu diperjelas.

Pose statis: lihat boards/stills/ dan board HTML. Teks layar utama: Kapan kita lanjut?

Saat animasi nanti: pertahankan layout ini setelah disetujui; pecah kemunculan sesuai frasa narasi dan timing rekaman. Gerak tidak dibuat sebelum review visual. Sumber dan batas: S2; opsi komunikasi, bukan jaminan keberhasilan.

- blueprint: compose
- focal: Kapan kita lanjut?
- roles: dua pemeran = foreground subject; tipografi = supporting; field krem/arang = background

Scene 1 (0.120–0.920s): sequential reveal pada #scene-04-figure-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 2 (0.250–1.050s): sequential reveal pada #scene-04-figure-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 3 (0.636–1.436s): sequential reveal pada #scene-04-foot-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 4 (3.510–4.310s): sequential reveal pada #scene-04-figure-2, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 5 (3.890–4.690s): sequential reveal pada #scene-04-part-scene-04-display-0-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 6 (4.553–5.353s): sequential reveal pada #scene-04-part-scene-04-display-0-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing

## Frame 5 — Rencana kembali (39.08-54.52s)

- act: Kemungkinan respons
- status: animated
- review: layout_approved
- src: compositions/frames/05-rencana-kembali.html
- duration: 15.44s
- poster: 53.82s
- transition_in: cut
- type: feature_showcase
- persuasion: Worked example
- beat: resolve
- scene: Gue tetap mau bahas ini. / Lanjut jam delapan, ya?
- voiceover: “Gue lagi kewalahan. Gue butuh jeda buat tenang. Gue tetap mau bahas ini. Kita lanjut jam delapan, ya?” Jamnya perlu disepakati, lalu ditepati. Kalau belum siap, kabari dan sepakati ulang.

narrativeRole: Memberi contoh jeda dengan rencana kembali yang dapat disepakati.

keyMessage: Jadwal kembali adalah contoh kesepakatan yang perlu ditindaklanjuti.

Pose statis: lihat boards/stills/ dan board HTML. Teks layar utama: Gue tetap mau bahas ini. / Lanjut jam delapan, ya?

Saat animasi nanti: pertahankan layout ini setelah disetujui; pecah kemunculan sesuai frasa narasi dan timing rekaman. Gerak tidak dibuat sebelum review visual. Sumber dan batas: S2; opsi komunikasi, bukan jaminan keberhasilan.

- blueprint: compose
- focal: Gue tetap mau bahas ini. / Lanjut jam delapan, ya?
- roles: dua pemeran = foreground subject; tipografi = supporting; field krem/arang = background

Scene 1 (0.150–0.950s): sequential reveal pada #scene-05-part-scene-05-body-0-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 2 (2.459–3.259s): sequential reveal pada #scene-05-part-scene-05-body-0-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 3 (4.241–5.041s): sequential reveal pada #scene-05-part-scene-05-display-0-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 4 (4.730–5.530s): sequential reveal pada #scene-05-part-scene-05-display-0-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 5 (6.209–7.009s): sequential reveal pada #scene-05-part-scene-05-appointment-0-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 6 (6.904–7.704s): sequential reveal pada #scene-05-part-scene-05-appointment-0-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 7 (9.390–10.190s): sequential reveal pada #scene-05-part-scene-05-part-scene-05-appointment-0-2-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 8 (10.597–11.397s): sequential reveal pada #scene-05-figure-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 9 (11.912–12.712s): sequential reveal pada #scene-05-part-scene-05-part-scene-05-appointment-0-2-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 10 (13.423–14.223s): sequential reveal pada #scene-05-figure-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing

## Frame 6 — Kembali membahasnya (54.52-65.352s)

- act: Kemungkinan respons
- status: animated
- review: layout_approved
- src: compositions/frames/06-refleksi.html
- duration: 10.832s
- poster: 64.652s
- transition_in: cut
- type: cta
- persuasion: Question→answer pairing
- beat: resolve
- scene: Setelah jeda, apa kalian kembali membahasnya?
- voiceover: Jeda itu belum menyelesaikan masalah. Obrolannya tetap perlu dilanjutkan. Di hubungan lo, setelah jeda, apa kalian benar-benar kembali membahasnya?

narrativeRole: Menilai tindak lanjut melalui pertanyaan refleksi.

keyMessage: Jeda belum menyelesaikan masalah; percakapan perlu dilanjutkan.

Pose statis: lihat boards/stills/ dan board HTML. Teks layar utama: Setelah jeda, apa kalian kembali membahasnya?

Saat animasi nanti: pertahankan layout ini setelah disetujui; pecah kemunculan sesuai frasa narasi dan timing rekaman. Gerak tidak dibuat sebelum review visual. Sumber dan batas: S2; opsi komunikasi, bukan jaminan keberhasilan.


- blueprint: compose
- focal: Setelah jeda, apa kalian kembali membahasnya?
- roles: dua pemeran = foreground subject; tipografi = supporting; field krem/arang = background

Scene 1 (0.120–0.920s): sequential reveal pada #scene-06-figure-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 2 (0.120–0.920s): relational position change pada #scene-06-figure-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 3 (0.280–1.080s): sequential reveal pada #scene-06-figure-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 4 (0.280–1.080s): relational position change pada #scene-06-figure-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 5 (2.805–3.605s): sequential reveal pada #scene-06-foot-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 6 (6.249–7.049s): sequential reveal pada #scene-06-part-scene-06-display-0-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 7 (7.227–8.027s): sequential reveal pada #scene-06-part-scene-06-display-0-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 8 (8.097–8.897s): sequential reveal pada #scene-06-part-scene-06-display-0-2, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 9 (8.097–8.897s): relational position change pada #scene-06-figure-0, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 10 (8.097–8.897s): relational position change pada #scene-06-figure-1, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing
Scene 11 (8.297–9.097s): svg-path-draw pada #scene-06-figure-2 path, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → svg-path-draw
Scene 12 (8.358–9.158s): sequential reveal pada #scene-06-part-scene-06-display-0-3, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → dynamic-content-sequencing

## Persetujuan dan pelaksanaan

Storyboard v1 disetujui pengguna pada 17 Oktober 2026 melalui “cocok”. Layout, copy dan siluet yang disetujui dipertahankan. Audio Ardi dipilih eksplisit. Runtime aktual 65.352 detik; musik/SFX belum dipilih dan tidak disisipkan pada preview v1. Motion: dynamic-content-sequencing, svg-path-draw, dan gerak posisi dua pemeran. Reveal dipandu metadata kata native; tidak ada pan/breathing dekoratif. Frame 2 dan penutup memiliki jeda baca disengaja. Implementasi dilakukan serial sesuai fallback subagent-dispatch tanpa mengirim tugas ke agen lain.
