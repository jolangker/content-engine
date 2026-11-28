# Bikin Kandang Panggung Ayam Kampung di Halaman

- **Script version:** v1
- **Board:** `budidaya-di-halaman` (Revision 10 — Editorial v9 / Visual v5)
- **Language & POV:** Bahasa Indonesia percakapan; `"kamu"` merujuk tunggal pada perakit/pemelihara kandang di satu sudut halaman rumah yang sama.
- **Voice & Audio:** ElevenLabs **Roger** (`CwhRBWXzGAHq8TQ4Fs17`, `eleven_v4`, `episode_override` fallback untuk free tier karena suara default board Pribs `5g0yKK2JwTRka0IG61Hh` ditolak HTTP 400), BGM `none`, SFX organik berdasar event dari pustaka Visual v5 board (`boards/budidaya-di-halaman/assets/sfx/manifest.json`).
- **Duration & word budget (terukur):** **234 kata lisan** (`93,840 dtk` take tunggal → `99,060 dtk` penempatan jeda hening → total komposisi 1x **`100,250 dtk`** termasuk tahan tag `3,679 dtk` dan *end card* `0,625 dtk`; **`80,200 dtk`** pada rilis `1,25x` / 30 fps, masuk jendela kontrak `90,0–112,5 dtk` di 1x / `72–90 dtk` rilis).
- **Event map:** 18 kejadian utama (1 hook bangun awal + 7 ronde masalah–perbaikan [14 kejadian] + 1 uji stabil + 1 adegan hitung estimasi panen + 1 penutup lebar & *end card*).

---

## On-screen copy (di luar caption ucapan)

- **Thumbnail & End Card (`0,625 dtk` di 1x / `0,5 dtk` di 1,25x):** Panel gelap di bagian atas tampak lebar kandang panggung ayam kampung jadi (dalam area aman 1080 × 1080 tengah, `y 420–1500`) dengan judul 2 baris 104 px DM Sans 900:
  - Baris 1: **Kandang panggung** (putih hangat `#FFF9E8`)
  - Baris 2: **ayam kampung** (kuning `#FFD44D`)
- **Price tag (Adegan 10 — Hitung Panen 20 Ekor):** Tag kertas 400 px tergantung pada paku di tiang kayu depan kandang di samping keranjang panen ayam kampung (terjangkar di *world space*):
  - Baris 1 (38 px): `20 ekor × Rp70.000`
  - Chip total (44 px, latar kuning `#FFD44D`): `≈ Rp1.400.000`
  - Catatan (28 px, 2 baris): `estimasi harga pasar` / `Nov 2026`
- **Closing signature (akhir Adegan 11):** Tiga kata berurutan **bikin di halaman** tetap tersorot kuning (`#FFD44D`) sampai akhir kalimat; `@bikindihalaman.id` muncul halus (*fade in*) kecil di bawah caption tanpa menutupi kandang.

---

## Scene 1 — Bangun Awal Prematur & Pakan Jatuh ke Kolong (`00:00–00:11`, 26 kata)

- **Shot:** `wide` sudut halaman tanah hangat kosong dengan rumah tetangga, pagar kayu, dan pohon pisang bergoyang di latar 4-lapis 2.5D; *punch-in* ke celah lantai bambu dan kolong bawah.
- **Sub-beats visual:**
  1. `00:00–00:03` (`Frame 0` + gerak `0,25 dtk`): Sudut halaman kosong dengan tumpukan tiang dan bilah bambu siap; tangan perakit langsung menancapkan empat tiang panggung dan merangkai lantai bilah bambu bercelah setinggi ~60 cm.
  2. `00:03–00:07`: Nampan pakan terbuka ditaruh di lantai bambu, lalu kawanan ayam kampung muda dilepas masuk ke atas panggung tanpa atap, tirai, maupun alas kolong.
  3. `00:07–00:11`: Cahaya bergeser ke sore; kamera *push-in* ke lantai panggung saat ayam-ayam mencakar nampan terbuka hingga separuh butiran pakan berhamburan jatuh menembus celah bambu ke tanah kolong.
- **SFX:** Ketukan tiang bambu (`wood-stake`), susun lantai (`pvc-snap`), tabur pakan (`pellet-scatter`), *whoosh* push-in (`cam-whoosh`), suasana halaman (`yard-ambience`).
- **Narration:**
  Kalo kamu dirikan panggung bambu di halaman, begitu kamu masukkan ayam dan nampan pakan, kamu sudah punya kandang ayam. Tapi sorenya separuh pakannya jatuh ke kolong.
- **Captions (46 px, maks 2 baris):**
  `Kalo kamu dirikan panggung bambu di halaman,` / `begitu kamu masukkan ayam dan nampan pakan,` / `kamu sudah punya kandang ayam.` / `Tapi sorenya separuh pakannya jatuh ke kolong.`

---

## Scene 2 — Ronde 1: Pakan Dicakar Tumpah → Tempat Pakan Gantung Sejajar Punggung (`00:11–00:20`, 20 kata)

- **Shot:** `close cutaway` bagian dalam kandang panggung dan celah lantai bambu (tiang rangka dan kolong tetap tampak sebagai penanda).
- **Sub-beats visual:**
  1. `00:11–00:14`: Potongan dekat memperlihatkan ceker ayam mengais nampan rendah di lantai sehingga butiran pakan terus jatuh menembus celah bambu ke kolong.
  2. `00:14–00:17`: Tangan perakit menyingkirkan nampan ceper dan menggantung tabung pakan berbibir/bersekat tepat sejajar tinggi punggung ayam.
  3. `00:17–00:20`: Ayam mematuk pakan rapi tanpa bisa memasukkan ceker; butiran tetap utuh di wadah dan kolong di bawah bersih dari tumpahan pakan.
- **SFX:** Hambur pakan (`pellet-scatter`), kait/klik tali gantung (`pvc-snap`), tuang pakan rapi (`pellet-scatter`).
- **Narration:**
  Ayam suka mengais, jadi pakan di nampan tumpah lewat celah lantai. Kamu pasang tempat pakan gantung sejajar punggung. Pakannya utuh.
- **Captions (46 px, maks 2 baris):**
  `Ayam suka mengais, jadi pakan di nampan` / `tumpah lewat celah lantai.` / `Kamu pasang tempat pakan gantung sejajar punggung.` / `Pakannya utuh.`

---

## Scene 3 — Ronde 2: Kolong Kotoran & Bau Amonia → Sekam Kering & Tabur Kapur (`00:20–00:29`, 21 kata)

- **Shot:** `medium` potongan kolong bawah kandang panggung (lantai bambu dan ayam di atas tetap terlihat sebagai penanda).
- **Sub-beats visual:**
  1. `00:20–00:23`: Transisi tiga hari; tumpukan kotoran ayam lembap di tanah kolong mengeluarkan garis uap bau amonia kehijauan dan mengundang lalat kecil berdengung.
  2. `00:23–00:26`: Tangan perakit menghamparkan lapisan sekam padi kering keemasan merata di kolong lalu menaburkan bubuk kapur putih tipis di atasnya.
  3. `00:26–00:29`: Permukaan kolong tampak kering dan rapi, garis uap bau amonia lenyap, dan lalat menghilang.
- **SFX:** Gali/serok sekam (`dig-soil`), tabur kapur/sekam (`pellet-scatter`), *whoosh* geser kamera (`cam-whoosh`).
- **Narration:**
  Tiga hari jalan, kotoran di kolong mulai bau amonia mengundang lalat. Kamu hampar sekam kering dan tabur kapur. Baunya mereda.
- **Captions (46 px, maks 2 baris):**
  `Tiga hari jalan, kotoran di kolong mulai bau` / `amonia mengundang lalat.` / `Kamu hampar sekam kering dan tabur kapur.` / `Baunya mereda.`

---

## Scene 4 — Ronde 3: Mangkuk Minum Kotor → Pipa Minum Nipel Gantung (`00:29–00:38`, 20 kata)

- **Shot:** `close cutaway` zona minum sisi kanan kandang panggung (tempat pakan gantung di kiri tetap tampak).
- **Sub-beats visual:**
  1. `00:29–00:32`: Mangkuk air minum terbuka di sudut lantai cepat keruh kecokelatan terciprat bulu dan kotoran saat ayam melangkah melewatinya.
  2. `00:32–00:35`: Tangan perakit memasang pipa PVC horizontal berisi mata nipel gantung yang tersambung ke jeriken/tandon kecil tertutup di luar kandang.
  3. `00:35–00:38`: Ayam mendongak mematuk ujung nipel dengan tetesan air jernih tanpa tumpahan; air di tandon tetap bersih dan lantai tetap kering.
- **SFX:** Kecipak air keruh (`water-splash`), klik sambungan pipa PVC (`pvc-snap`), kucur isi tandon (`water-pour`).
- **Narration:**
  Masalahnya, air di mangkuk terbuka cepat kotor kena kotoran dan bulu. Kamu pasang pipa minum nipel gantung. Airnya selalu bersih.
- **Captions (46 px, maks 2 baris):**
  `Masalahnya, air di mangkuk terbuka cepat kotor` / `kena kotoran dan bulu.` / `Kamu pasang pipa minum nipel gantung.` / `Airnya selalu bersih.`

---

## Scene 5 — Ronde 4: Stres Panas Siang → Atap Miring Bercelah Udara (`00:38–00:47`, 20 kata)

- **Shot:** `medium-wide` tampak samping kandang panggung di bawah terik matahari siang (kolong sekam, pakan gantung, dan pipa nipel tetap tampak).
- **Sub-beats visual:**
  1. `00:38–00:41`: Matahari terik di puncak langit dengan gelombang panas tipis; ayam-ayam membuka paruh terengah-engah (*panting*) dan merenggangkan kedua sayapnya.
  2. `00:41–00:44`: Tangan perakit memasang kaso dan lembar atap miring berpeneduh dengan celah sirkulasi udara terbuka di bagian atas dinding.
  3. `00:44–00:47`: Bayangan teduh jatuh merata, panah udara hangat keluar lewat celah atas, dan ayam menutup paruh kembali aktif tenang.
- **SFX:** Ketukan rangka atap (`wood-stake`), pasang lembar atap (`tarp-rustle`), *whoosh* udara (`cam-whoosh`).
- **Narration:**
  Pas tengah hari, ayamnya buka paruh kepanasan dan sayapnya melebar. Kamu pasang atap miring bercelah angin di atas. Kandang teduh.
- **Captions (46 px, maks 2 baris):**
  `Pas tengah hari, ayamnya buka paruh kepanasan` / `dan sayapnya melebar.` / `Kamu pasang atap miring bercelah angin di atas.` / `Kandang teduh.`

---

## Scene 6 — Ronde 5: Hujan Angin & Angin Dingin → Tirai Terpal Gulung Samping (`00:47–00:56`, 21 kata)

- **Shot:** `medium` dinding samping kandang panggung di bawah langit mendung hujan miring (atap miring bercelah dan kolong sekam tetap terlihat).
- **Sub-beats visual:**
  1. `00:47–00:50`: Langit gelap mendung; hujan miring dan garis angin dingin menerobos dinding bambu terbuka sehingga ayam berkerumun menggigil.
  2. `00:50–00:53`: Tangan perakit memasang dan menurunkan tirai terpal gulung di sisi datangnya angin dengan tetap menyisakan celah ventilasi atas.
  3. `00:53–00:56`: Hujan miring memantul di luar terpal, bagian dalam tetap hangat kering, dan ayam kembali tenang.
- **SFX:** Derai hujan angin (`rain-shower`), ulur kain terpal (`tarp-rustle`), klik kait pengikat (`pvc-snap`).
- **Narration:**
  Begitu hujan angin turun, tampias dan angin dingin masuk membuat ayam menggigil. Kamu pasang tirai terpal gulung di samping. Ayam hangat.
- **Captions (46 px, maks 2 baris):**
  `Begitu hujan angin turun, tampias dan angin dingin` / `masuk membuat ayam menggigil.` / `Kamu pasang tirai terpal gulung di samping.` / `Ayam hangat.`

---

## Scene 7 — Ronde 6: Tidur Berdesakan di Celah Lantai → Palang Tenggeran Kayu Bulat (`00:56–01:05`, 20 kata)

- **Shot:** `close cutaway` bagian dalam kandang saat malam hari dengan lampu hangat rumah di latar belakang (dinding tirai dan pipa nipel tetap tampak).
- **Sub-beats visual:**
  1. `00:56–00:59`: Cahaya malam; ayam berdesakan tidur langsung di bilah lantai bambu hingga salah satu cakar ayam terselip di celah bilah.
  2. `00:59–01:02`: Tangan perakit memasang dua batang palang kayu bulat sejajar setinggi ~45 cm di atas lantai sebagai tenggeran malam.
  3. `01:02–01:05`: Ayam-ayam melompat naik mencengkeram palang kayu bulat dan berjajar tidur tenang dengan kaki aman di atas lantai.
- **SFX:** Ketukan pasang palang kayu (`wood-stake`), klik ikatan/paku (`pvc-snap`), *whoosh* halus (`cam-whoosh`).
- **Narration:**
  Malam harinya, ayam berdesakan tidur di bilah lantai sampai kakinya terselip. Kamu pasang palang tenggeran kayu bulat. Mereka bertengger tenang.
- **Captions (46 px, maks 2 baris):**
  `Malam harinya, ayam berdesakan tidur di bilah lantai` / `sampai kakinya terselip.` / `Kamu pasang palang tenggeran kayu bulat.` / `Mereka bertengger tenang.`

---

## Scene 8 — Ronde 7: Tikus Malam Menyusup Celah → Kawat Ram Rapat Keliling (`01:05–01:14`, 20 kata)

- **Shot:** `medium-wide` sudut luar dinding kandang panggung saat malam (tiang panggung, kolong sekam, dan tenggeran dalam tetap tampak).
- **Sub-beats visual:**
  1. `01:05–01:08`: Siluet tikus malam memanjat tepi panggung dan menyusup melewati celah renggang dinding bambu, membuat ayam di tenggeran mengepak kaget.
  2. `01:08–01:11`: Tangan perakit membentangkan kawat ram rapat melingkari seluruh dinding samping dan menutup celah pintu rapat-rapat.
  3. `01:11–01:14`: Malam berikutnya, siluet tikus tertahan di luar kawat ram lalu berbalik pergi sementara seluruh ayam tidur aman di dalam.
- **SFX:** Bentang jaring/kawat ram (`fabric-net`), ketuk paku klem (`wood-stake`), suasana malam tenang (`yard-ambience`).
- **Narration:**
  Seminggu kemudian, tikus menyusup lewat celah dinding bikin ayam panik. Kamu lapisi keliling dinding dengan kawat ram rapat. Kandang aman.
- **Captions (46 px, maks 2 baris):**
  `Seminggu kemudian, tikus menyusup lewat celah` / `dinding bikin ayam panik.` / `Kamu lapisi keliling dinding dengan kawat ram rapat.` / `Kandang aman.`

---

## Scene 9 — Sistem Stabil (`01:14–01:22`, 19 kata)

- **Shot:** `wide` penuh pojok halaman menampilkan seluruh kandang panggung ayam kampung yang sudah lengkap beroperasi.
- **Sub-beats visual:**
  1. `01:14–01:18`: Cuaca bergeser dari hujan ringan ke pagi cerah; atap miring dan tirai gulung menahan tampias, kolong bersekam kapur tampak kering tanpa bau, dan kawat ram utuh melingkari dinding.
  2. `01:18–01:22`: Kawanan ayam kampung dewasa makan tenang di tempat pakan gantung, mematuk pipa nipel bersih, dan sebagian bertengger sehat di palang kayu.
- **SFX:** Rintik hujan singkat (`rain-shower`), tabur pakan (`pellet-scatter`), suasana halaman pagi (`yard-ambience`).
- **Narration:**
  Sekarang, mau terik atau hujan angin, kandang teduh, kolong kering tanpa bau, pakan utuh, dan ayam tumbuh sehat stabil.
- **Captions (46 px, maks 2 baris):**
  `Sekarang, mau terik atau hujan angin, kandang teduh,` / `kolong kering tanpa bau, pakan utuh,` / `dan ayam tumbuh sehat stabil.`

---

## Scene 10 — Monetisasi: Panen 20 Ekor Ayam Kampung (`01:22–01:35`, 25 kata + tahan tag ≥3 dtk)

- **Shot:** `medium` di sisi depan kandang panggung jadi (kandang tetap jelas terlihat sebagai penanda di belakang, keranjang panen ayam kampung & interaksi pemeriksaan/penghitungan mengisi ≥40% lebar frame).
- **Sub-beats visual:**
  1. `01:22–01:26`: Tiga bulan berjalan; tangan perakit memasukkan ayam kampung dewasa sehat ke dalam dua keranjang panen bambu/plastik di depan tiang kandang sambil menghitung jumlahnya.
  2. `01:26–01:29`: Pada kata *"dua puluh ekor"*, tag harga kertas 400 px turun (`0,2 s`, ayunan reda `0,5 s`) di paku tiang depan kandang menampilkan `20 ekor × Rp70.000`.
  3. `01:29–01:35`: Pada *"satu juta empat ratus ribu"*, chip kuning `≈ Rp1.400.000` muncul mekar (`0,15 s`) bersama catatan `estimasi harga pasar / Nov 2026`, lalu ditahan penuh `≥3,0 s` di 1x.
- **SFX:** Gemerisik keranjang & rantai (`scale-chain`), klik jatuh tag (`tag-click`), pop chip total kuning (`tag-pop`).
- **Narration:**
  Tiga bulan berjalan, dua puluh ekor ayam kampung siap panen. Di pasar sekitar tujuh puluh ribu per ekor, jadi kurang lebih satu juta empat ratus ribu.
- **Captions (46 px, maks 2 baris):**
  `Tiga bulan berjalan, dua puluh ekor` / `ayam kampung siap panen.` / `Di pasar sekitar tujuh puluh ribu per ekor,` / `jadi kurang lebih satu juta empat ratus ribu.`

---

## Scene 11 — Penutup Lebar & End Card (`01:35–01:46`, 24 kata + `0,625 dtk` *end card*)

- **Shot:** `wide` tarik mundur penuh menampilkan sudut halaman hidup dengan kandang panggung ayam kampung lengkap dan keranjang panen di sampingnya; diakhiri *hard cut* ke *end card* identik thumbnail.
- **Sub-beats visual:**
  1. `01:35–01:41`: Kamera *pull-out* lembut memperlihatkan kandang panggung beroperasi bersih (pakan gantung, kolong sekam kapur, pipa nipel, atap miring bercelah, tirai gulung, palang tenggeran, kawat ram rapat) bersama dua keranjang panen.
  2. `01:41–01:45.4`: Pada kalimat tanya penutup, kata berurutan **`bikin di halaman`** tetap menyala kuning `#FFD44D` sampai akhir kalimat sementara handle `@bikindihalaman.id` *fade in* kecil di bawah caption.
  3. `01:45.4–01:46.0` (`0,625 s` di 1x / `0,5 s` di 1,25x): *Hard cut* ke *end card* identik dengan thumbnail PNG (caption bersih, panel gelap atas di area aman 1080 × 1080 dengan judul **Kandang panggung** / **ayam kampung**).
- **SFX:** Suasana sore halaman lembut (`yard-ambience`), *whoosh* tarik kamera (`cam-whoosh`), hening bersih pada *end card*.
- **Narration:**
  Selamat, kamu sudah punya kandang panggung ayam kampung sendiri, bersih sampai panen. Habis ini, apa lagi yang mau kamu bikin di halaman?
- **Captions (46 px, maks 2 baris):**
  `Selamat, kamu sudah punya kandang panggung` / `ayam kampung sendiri, bersih sampai panen.` / `Habis ini, apa lagi yang mau kamu bikin di halaman?`
