---
format: 1080x1920
duration: 60s
message: "Suka itu senang sama orangnya; limerence itu bergantung sama jawabannya"
arc: concept-explainer
audience: "Penonton short-form Indonesia (lo-gua) yang sedang mengamati pola hubungannya sendiri"
mode: collaborative
music: "soft warm minimal piano underscore, thin and intimate, deliberate silence before the closing question"
---

## Video direction

- **Palette (dari `frame.md`, board Ruang di Antara v1):** krem `#F3EDE3` latar dominan · tile `#EEE7DF`/`#D8C8B5` setengah-langkah untuk kartu · ink `#302B28` untuk teks · coral `#A34F3F` sebagai satu-satunya voltage per frame (satu momen saja — garis hasrat, badge, atau emphasis) · arang `#181615` HANYA untuk frame 4 (tekanan emosional, alternatif frame gelap board). Warna tidak pernah menjadi kode gender/makna.
- **Type (per role):** Newsreader display = suara batin/refleksi (kata "limerence", pertanyaan penutup); DM Sans = penjelasan, label, caption, chrome; angka/tahun sebagai mono-label role. Hero display mendekati full-bleed (40–60% frame).
- **Motion grammar:** long-tail settle (`power3`) — tanpa bouncy/overshoot default. **Reveal mengikuti VO:** di t=0 hanya yang sedang diucapkan tampil; setiap potongan baru muncul pada cue-nya, tersebar ke ~50% belakang. Seek-safe: `fromTo`, tanpa `repeat`/`yoyo`, tanpa CSS transition, tanpa `Math.random`. Aliveness saat hold hanya **subtle jitter** (`sine-wave-loop`, amplitude rendah).
- **Rhythm / held frames:** frame 6 adalah breather yang dipegang penuh (sengaja); frame 4 punya satu beat hold sebelum eskalasi; frame 7 ditutup dengan hold baca. Frame lain mengikuti ritme VO.
- **Negative list:** slideshow (front-load lalu freeze) · screensaver (elemen melayang sendiri-sendiri) · lazy breathing · pan/push lambat di paruh akhir · wajah/manusia · bokeh/gradien "AI" biru-ungu · teks di bawah 83% atas (band caption bawah ±17% tetap kosong; hero berjangkar di y ≈ 0.42 × tinggi).
- **Tata letak portrait:** split-screen/triptych menjadi tumpukan vertikal (band/stack), kata per baris lebih sedikit dengan ukuran lebih besar.

## Frame 1 — Kepikiran terus

- scene: Satu bentuk membulat di krem lapang; gema jejak berulang (chat dibaca ulang) melayang mengelilinginya, satu garis pendek berdenyut mengikuti "mood"
- voiceover: "Lo baru kenal seseorang, belum seberapa. Tapi dia udah ngisi kepala lo seharian — chat dibaca ulang, satu balasan pendek bisa nentuin mood lo."
- duration: 11s
- transition_in: cut
- status: outline
- src: compositions/frames/01-kepikiran-terus.html
- type: hook
- persuasion: Pain validation + Direct address (skenario yang penonton kenali)
- beat: recognition + tension
- blueprint: compose
- focal: bentuk A (diri penonton, blob membulat tanpa wajah)
- roles: bentuk A = foreground subject · gema pill "chat" + garis mood = supporting · latar krem + garis halus = background
- sfx: soft-tick

narrativeRole: Menyandingkan pengalaman yang akrab (baru kenal tapi kepikiran terus) supaya penonton langsung mengenali dirinya.
keyMessage: Ada satu pengalaman romantis yang terasa seperti jatuh cinta tapi lebih mengganggu dari itu.

Adapt/Compose: compose dari kosakata motion board (jejak posisi, gema berulang).
Scene 1 (0.0–3.5s): VO "Lo baru kenal seseorang, belum seberapa." — latar krem lapang dengan lapisan garis halus (background, dim); bentuk A masuk dengan long-tail settle (`spring-pop-entrance`, register smooth) berjangkar y ≈ 0.42 × tinggi, ~45% lebar; satu titik kecil "dia" (B) muncul jauh di atas sebagai supporting. Layout: centered hero, 3 depth layers.
Scene 2 (3.5–7.5s): VO "Tapi dia udah ngisi kepala lo seharian — chat dibaca ulang," — gema pill "chat" (3–4 pill kecil) muncul berurutan mengelilingi A (`dynamic-content-sequencing`, reveal per cue "seharian" lalu "dibaca ulang"); pill yang sama memunculkan gema keduanya (jejak berulang). Layout: layered-depth asymmetric 60/40.
Scene 3 (7.5–11.0s): VO "satu balasan pendek bisa nentuin mood lo." — satu pill "balasan" pendek muncul dekat B (`spring-pop-entrance`, smooth), lalu garis mood di bawah A berdenyut naik-turun sekali mengikuti (`asr-keyword-glow` pada kata "mood"); selesai → hold, maksimal subtle jitter (`sine-wave-loop`, amplitude rendah).

## Frame 2 — Ada namanya

- scene: Ruang kosong krem; kata "limerence" muncul besar (Newsreader, sentence case) sebagai satu nama untuk pengalaman tadi; kredit kecil "Tennov, 1979" di pojok
- voiceover: "Sebagian lo nyebut ini jatuh cinta. Psikolog Dorothy Tennov nyebutnya: limerence."
- duration: 5s
- transition_in: crossfade
- status: outline
- src: compositions/frames/02-ada-namanya.html
- type: product_intro
- persuasion: Coined term / mnemonic (menamai pengalaman supaya mudah diingat)
- beat: clarity + orientation
- blueprint: kinetic-type-beats (Adapt)
- focal: kata "limerence" (Newsreader display, mendekati full-bleed)
- roles: "limerence" = foreground subject · frasa pengantar + kredit "Tennov, 1979" = supporting · latar krem = background

narrativeRole: Memberi nama pada pengalaman dari Frame 1 — sang "protagonis" video ini adalah idenya.
keyMessage: Pengalaman ini punya nama dalam psikologi: limerence.

Adapt: pertahankan signature in-place word change (motion IS the words); kontennya penamaan istilah, bukan brand.
Scene 1 (0.0–2.0s): VO "Sebagian lo nyebut ini jatuh cinta." — frasa kecil DM Sans masuk per kata (`dynamic-content-sequencing`) di sepertiga atas; ruang bawah masih kosong. Layout: rule-of-thirds vertikal.
Scene 2 (2.0–3.5s): VO "Psikolog Dorothy Tennov nyebutnya: limerence." — token "jatuh cinta" berganti in-place ke "limerence" (`discrete-text-sequence`, hard-cut word-swap = signature) lalu naik ke skala display (Newsreader, y ≈ 0.42 × tinggi, ~55% lebar). Layout: centered hero.
Scene 3 (3.5–5.0s): kredit kecil "Tennov, 1979" (mono-label role) naik pelan di bawah hero (`spring-pop-entrance`, smooth); hold baca.

## Frame 3 — Definisi

- scene: Dua bentuk membulat muncul berjauhan di latar krem; dari bentuk A ada lintasan energi/kecenderungan yang kuat ke arah B — intensitas hasrat yang tidak diminta
- voiceover: "Limerence itu hasrat romantis yang intens dan datang tanpa diundang."
- duration: 5s
- transition_in: crossfade
- status: outline
- src: compositions/frames/03-definisi.html
- type: feature_showcase
- persuasion: Concretization (hasrat abstrak → lintasan fisik antar-bentuk)
- beat: comprehension
- blueprint: compose
- focal: lintasan kurva hasrat A → B
- roles: bentuk A & B = foreground subject · lintasan coral = supporting (voltage tunggal) · latar krem = background

narrativeRole: Mendefinisikan limerence dalam satu kalimat visual: intens, satu arah, tidak disengaja.
keyMessage: Limerence adalah hasrat romantis yang intens dan datang tanpa diundang.

Compose: pasangan dua bentuk board sebagai panggung; lintasan sebagai definisi visual.
Scene 1 (0.0–2.0s): VO "Limerence itu hasrat romantis yang intens" — dua bentuk (A di atas, B di bawah — tumpukan vertikal portrait) masuk berurutan dengan long-tail settle (`spring-pop-entrance`, smooth). Layout: stacked vertical, ~50% area, jarak besar terbaca.
Scene 2 (2.0–5.0s): VO "...dan datang tanpa diundang." — lintasan kurva dari A ke B menggambar sendiri (`svg-path-draw`) dengan intensitas (tebal/glow coral — voltage tunggal frame ini); arah A→B kuat, B tidak merespons (tanpa gerak balik); hold.

## Frame 4 — Siklus ketidakpastian

- scene: Panggung yang sama (dua bentuk), latar berganti ke arang untuk tekanan emosional; tiga lapis muncul berurutan: (1) lintasan melingkar yang terus kembali ke B, (2) tanda harapan/timbang di ruang antara, (3) lintasan makin lebar & cepat saat jarak makin tidak pasti
- voiceover: "Pikiran soal dia terus balik, lo butuh banget dia bales perasaan yang sama, dan makin gak pasti — justru makin kencang."
- duration: 9s
- transition_in: crossfade
- status: outline
- src: compositions/frames/04-siklus-ketidakpastian.html
- type: feature_showcase
- persuasion: Progressive disclosure + Causal chain (pikiran → kebutuhan → ketidakpastian memperkuat)
- beat: fascination + unease
- blueprint: compose
- focal: lintasan melingkar (siklus pikiran → harapan → eskalasi)
- roles: bentuk A & B = foreground subject · lintasan melingkar + tanda tanya = supporting · latar arang `#181615` = background (tekanan emosional)

narrativeRole: Membongkar mekanisme limerence lapis demi lapis sampai paradoksnya terlihat: ketidakpastian justru memperkuat.
keyMessage: Pikiran intrusif, kebutuhan akan timbal balik, dan ketidakpastian saling menguatkan — sebuah siklus.

Compose: tiga lapis berirama pada panggung dua bentuk; panggung sama dengan Frame 3 (kontinuitas), latar berganti ke arang.
Scene 1 (0.0–3.0s): VO "Pikiran soal dia terus balik," — latar arang menggantikan krem (crossfade halus dari harness); dua bentuk tetap di posisi; lintasan melingkar A→B→kembali menggambar sendiri dua putaran (`svg-path-draw`, dash loop). Layout: stacked vertical, foreground naik.
Scene 2 (3.0–6.0s): VO "lo butuh banget dia bales perasaan yang sama," — pill kecil "balasan?" + tanda tanya muncul di ruang antara (`spring-pop-entrance`, smooth), garis harapan tipis A↔B menyala sekali. Layout: asymmetric 60/40, ruang antara sebagai fokus.
Scene 3 (6.0–9.0s): VO "dan makin gak pasti — justru makin kencang." — lintasan melingkar tumbuh makin lebar dan berdenyut makin cepat (amplitude tween berirama cue), keyword glow (`asr-keyword-glow`) pada "makin kencang"; selesai → hold dengan subtle jitter (`sine-wave-loop`, rendah).

## Frame 5 — Suka vs limerence

- scene: Dua jalur berdampingan (band pembanding): kiri "suka" — dua bentuk sejajar tenang, koneksi stabil; kanan "limerence" — posisi bentuk A naik-turun mengikuti sinyal pendek dari B
- voiceover: "Bedanya sama suka biasa: kalau suka, lo seneng sama orangnya. Kalau limerence, mood lo bergantung sama jawabannya."
- duration: 8s
- transition_in: cut
- status: outline
- src: compositions/frames/05-suka-vs-limerence.html
- type: benefit_highlight
- persuasion: Comparison of two options (dua lintasan hidup berdampingan)
- beat: aha
- blueprint: comparison-split (Adapt)
- focal: dua band pembanding (suka vs limerence)
- roles: dua band + pasangan bentuk di dalamnya = foreground subject · badge pill = supporting · latar krem + tile = background

narrativeRole: Menyajikan pembeda inti — yang membedakan suka dari limerence bukan intensitasnya, tapi di mana kendali mood berada.
keyMessage: Kalau suka, lo senang sama orangnya; kalau limerence, mood lo bergantung sama jawabannya.

Adapt: pertahankan signature masuk berpasangan dari sisi berlawanan + badge pill; portrait → band ditumpuk vertikal (bukan split layar lebar).
Scene 1 (0.0–2.5s): VO "Bedanya sama suka biasa:" — dua band tile masuk dari sisi berlawanan dengan tilt halus (`split-tilt-cards`, adaptasi stacked) — band atas berlabel "suka", band bawah "limerence" (DM Sans tag). Layout: full-width stacked bands, 2 depth layers.
Scene 2 (2.5–5.5s): VO "kalau suka, lo seneng sama orangnya." — band atas hidup: dua bentuk sejajar dengan garis koneksi stabil (draw-on `svg-path-draw`, garis tenang); badge pill "senang sama orangnya" pop smooth (`spring-pop-entrance`). Layout: fokus band atas.
Scene 3 (5.5–8.0s): VO "Kalau limerence, mood lo bergantung sama jawabannya." — band bawah: posisi bentuk A naik-turun mengikuti sinyal pendek dari B (gerak diskrit per sinyal, `discrete-text-sequence` untuk label sinyal); badge pill "bergantung sama jawabannya" pop; hold perbandingan.

## Frame 6 — Batas konsep

- scene: Kartu tenang di krem (breather): "konsep deskriptif, bukan diagnosis" dengan kredit "Tennov, 1979" (Newsreader italic untuk suara refleksi, DM Sans untuk label)
- voiceover: "Dan catet — ini konsep deskriptif dari 1979, bukan diagnosis."
- duration: 5s
- transition_in: crossfade
- status: outline
- src: compositions/frames/06-batas-konsep.html
- type: social_proof
- persuasion: Citation / source (membatasi klaim pada status istilah yang sebenarnya)
- beat: clarity + trust
- blueprint: titlecard-reveal (Reproduce)
- focal: kartu kalimat batas konsep
- roles: kartu + teks = foreground subject · kredit "Tennov, 1979" = supporting · latar krem = background

narrativeRole: Menjaga kejujuran istilah: limerence adalah alat bantu mengamati, bukan label medis.
keyMessage: Limerence adalah konsep deskriptif dari 1979 — bukan diagnosis.

Reproduce: satu gerak tenang lalu hold (payload-nya keheningan).
Scene 1 (0.0–2.0s): VO "Dan catet — ini konsep deskriptif dari 1979," — kartu hairline (card-hairline role) naik pelan + crossfade (gerak tunggal yang restrained), teks "konsep deskriptif dari 1979" terbaca (Newsreader italic). Layout: centered card, ~55% lebar, y ≈ 0.42 × tinggi.
Scene 2 (2.0–5.0s): VO "bukan diagnosis." — baris "bukan diagnosis" mendarat per kata (`dynamic-content-sequencing`), kredit kecil menyusul; hold penuh — frame breather yang disengaja, tanpa gerak lain.

## Frame 7 — Pertanyaan penutup

- scene: Ruang kosong krem; pertanyaan muncul bertahap per frasa; dua bentuk menemukan jarak yang disepakati — garis koneksi tenang di antara mereka
- voiceover: "Jadi sebelum ngejar kepastian dari dia, tanya diri lo sendiri: yang lo cari itu dia — atau kepastian bahwa lo cukup?"
- duration: 10s
- transition_in: crossfade
- status: outline
- src: compositions/frames/07-pertanyaan-penutup.html
- type: cta
- persuasion: Callback + Distillation (kembali ke "kepastian" dari Frame 1, dikompres jadi satu pertanyaan)
- beat: resolve
- blueprint: kinetic-type-beats (Adapt)
- focal: pertanyaan penutup (Newsreader display)
- roles: pertanyaan = foreground subject · dua bentuk + garis koneksi tenang = supporting · latar krem lapang + garis halus = background

narrativeRole: Membuka refleksi — mengubah penjelasan menjadi satu pertanyaan yang bisa dibawa pulang.
keyMessage: Sebelum mengejar jawaban dari dia, cek dulu apa yang sebenarnya lo cari.

Adapt: pertahankan signature statement yang membangun per beat; landing-nya pertanyaan refleksi, bukan URL/brand.
Scene 1 (0.0–3.0s): VO "Jadi sebelum ngejar kepastian dari dia," — frasa masuk per kata (`dynamic-content-sequencing`) di sepertiga atas; dua bentuk mulai bergerak pelan mencari posisi (mendekat, tertahan — kosakata gerak board). Layout: rule-of-thirds vertikal.
Scene 2 (3.0–5.5s): VO "tanya diri lo sendiri:" — frasa kedua mendarat; jeda disengaja dihormati — ruang kosong dibiarkan (brief hold, tanpa isian). Layout: space sebagai elemen.
Scene 3 (5.5–8.5s): VO "yang lo cari itu dia — atau kepastian bahwa lo cukup?" — dua frasa pilihan muncul berurutan pada cue-nya ("yang lo cari itu dia" lalu "atau kepastian bahwa lo cukup?") dengan emphasis halus (`discrete-text-sequence`), garis koneksi A–B draw-on tenang (`svg-path-draw`) saat kedua bentuk menemukan jarak yang disepakati. Layout: centered question di y ≈ 0.42 × tinggi, dua bentuk di bawahnya (di atas band caption).
Scene 4 (8.5–10.0s): hold baca penuh — pertanyaan terbaca, koneksi tenang; maksimal subtle jitter. Frame terakhir: exit ditangani harness.
