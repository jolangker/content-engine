# Bikin Kolam Ikan Gurame di Halaman

- **Script version:** v1
- **Board:** `budidaya-di-halaman` (Revision 10 — Editorial v9 / Visual v5)
- **Language & POV:** Bahasa Indonesia percakapan; `"kamu"` merujuk tunggal pada perakit/pemelihara di satu sudut halaman rumah yang sama.
- **Voice & Audio:** Rencana suara **Roger** (`CwhRBWXzGAHq8TQ4Fs17`, `eleven_v4`, fallback atas HTTP 400 `voice_not_found` pada suara default `Pribs` di tier gratis `.env`; menunggu kecukupan kuota karakter ElevenLabs sebelum sintesis), BGM `none`, SFX organik berdasar event dari pustaka Visual v5 board (`boards/budidaya-di-halaman/assets/sfx/manifest.json`).
- **Duration & word budget (estimated pre-synthesis):** **236 kata lisan** (`1.553` karakter tanpa tag / ~`1.650` karakter bertag). Pada kecepatan terukur Roger (`2,39 kata/dtk` dari `kolam-belut-dalam-drum`): prediksi narasi mentah `98,7 dtk`, prediksi komposisi 1x (termasuk jeda sunyi antar-adegan + tahan tag harga ≥3 dtk + `0,625 dtk` *end card*) **`105,4 dtk`** — masuk jendela kontrak `90,0–112,5 dtk` di 1x (**`~84,3 dtk`** pada ekspor 1,25x / 30 fps). Akan direkonsiliasi dengan waktu terukur sesudah *take* tunggal disintesis.
- **Event map:** 18 kejadian utama (1 hook bangun awal + 7 ronde masalah–perbaikan [14 kejadian] + 1 uji stabil + 1 adegan timbang estimasi panen + 1 penutup lebar & *end card*).

---

## On-screen copy (di luar caption ucapan)

- **Thumbnail & End Card (`0,625 dtk` di 1x / `0,5 dtk` di 1,25x):** Panel gelap di atas tampak lebar kolam bundar *wiremesh* gurame jadi (dalam area aman 1080 × 1080 tengah, `y 420–1500`) dengan judul 2 baris 104 px DM Sans 900:
  - Baris 1: **Kolam gurame** (`Kolam` putih hangat `#FFF9E8`, **gurame** kuning `#FFD44D`)
  - Baris 2: **di sudut halaman** (putih hangat `#FFF9E8`)
- **Price tag (Adegan 10 — Timbang Panen):** Tag kertas 400 px tergantung di paku galah/tiang timbangan gantung di samping kolam (terjangkar di *world space*):
  - Baris 1 (38 px): `40 kg × Rp45.000`
  - Chip total (44 px, latar kuning `#FFD44D`): `≈ Rp1.800.000`
  - Catatan (28 px, 2 baris): `estimasi harga pasar` / `Nov 2026`
- **Closing signature (akhir Adegan 11):** Tiga kata berurutan **bikin di halaman** tetap tersorot kuning (`#FFD44D`) sampai akhir kalimat; `@bikindihalaman.id` muncul halus (*fade in*) kecil di bawah caption tanpa menutupi sistem.

---

## Scene 1 — Bangun Awal Prematur & Jamur Setelah Hujan (`00:00–00:11`, 26 kata)

- **Shot:** `wide` sudut halaman tanah hangat kosong dengan rumah tetangga, pagar kayu, dan pohon pisang bergoyang di latar 4-lapis 2.5D; *punch-in* cepat ke sirip gurame di dalam kolam.
- **Sub-beats visual:**
  1. `00:00–00:03` (`Frame 0` + gerak `0,25 dtk`): Sudut halaman kosong dengan gulungan besi *wiremesh* dan terpal biru terlipat; tangan perakit langsung melingkarkan rangka *wiremesh* menjadi silinder bundar (*micro-impact*).
  2. `00:03–00:07`: Terpal bundar dipasang di dalam rangka, air jernih dituang mengisi kolam, dan bibit gurame dilepas berenang.
  3. `00:07–00:11`: Langit mendung hujan turun; kamera *push-in* ke irisan kolam memperlihatkan suhu turun dan bercak putih seperti kapas mulai muncul di sirip gurame.
- **SFX:** Gemerincing rangka logam (`scale-chain` / `wood-stake`), bentangan terpal (`tarp-rustle`), kucuran air (`water-pour`), kecipak bibit (`water-splash`), hujan (`rain-shower`), *whoosh* kamera (`cam-whoosh`).
- **Narration:**
  Kalo kamu lingkarkan besi wiremesh di halaman, lalu kamu lapis terpal dan tebar bibit gurame, kamu sudah punya kolam gurame. Tapi setelah kehujanan, sirip ikannya berjamur putih.
- **Captions (46 px, maks 2 baris):**
  `Kalo kamu lingkarkan besi wiremesh di halaman,` / `lalu kamu lapis terpal dan tebar bibit gurame,` / `kamu sudah punya kolam gurame.` / `Tapi setelah kehujanan, sirip ikannya berjamur putih.`

---

## Scene 2 — Ronde 1: Suhu Dingin Hujan → Karantina Garam, Atap Bening & Paranet (`00:11–00:20`, 22 kata)

- **Shot:** `medium` irisan kolam bundar di bawah hujan menuju teduh cerah; *pan* ke rangka atap di atas kolam.
- **Sub-beats visual:**
  1. `00:11–00:14`: Irisan kolam menunjukkan air hujan dingin menjatuhkan suhu kolam terpal tanpa pelindung.
  2. `00:14–00:18`: Ikan berbercak diangkat ke ember karantina berlarutan garam sebentar, sementara rangka tiang atas dipasang atap plastik bening plus jaring *paranet* peneduh.
  3. `00:18–00:20`: Matahari hangat dan hujan tertahan di atas atap; gurame kembali sehat berenang bersih di kolam utama.
- **SFX:** Kecipak serok (`water-splash`), ketuk tiang (`wood-stake`), bentang atap/paranet (`fabric-net`), gemericik hujan teredam (`rain-shower`).
- **Narration:**
  Air hujan bikin suhu kolam terpal turun mendadak. Kamu rendam ikan sakit dengan garam, lalu pasang atap bening dan paranet. Jamurnya hilang.
- **Captions (46 px, maks 2 baris):**
  `Air hujan bikin suhu kolam terpal turun mendadak.` / `Kamu rendam ikan sakit dengan garam,` / `lalu pasang atap bening dan paranet.` / `Jamurnya hilang.`

---

## Scene 3 — Ronde 2: Tepi Wiremesh Menekan Terpal → Lapis Karpet Talang (`00:20–00:29`, 19 kata)

- **Shot:** `close cutaway` dinding samping terpal yang menempel ke besi *wiremesh* dengan tanah di luarnya mulai basah gelap.
- **Sub-beats visual:**
  1. `00:20–00:24`: Tekanan air mendorong dinding terpal menekan ujung las kawat *wiremesh* yang tajam hingga muncul rembesan dan tanah luar menghitam basah.
  2. `00:24–00:29`: Terpal ditahan sebentar di sisi itu, lembaran karpet talang hitam diselipkan melingkari dinding dalam di antara besi dan terpal, lalu permukaan air teruji kembali penuh bertahan.
- **SFX:** *Whoosh* push (`cam-whoosh`), geser karpet talang (`tarp-rustle`), ketuk pasang klip (`pvc-snap`).
- **Narration:**
  Seminggu jalan, airnya rembes di samping. Ujung kawat menekan terpal. Kamu selipkan karpet talang di dinding dalam. Airnya bertahan.
- **Captions (46 px, maks 2 baris):**
  `Seminggu jalan, airnya rembes di samping.` / `Ujung kawat menekan terpal.` / `Kamu selipkan karpet talang di dinding dalam.` / `Airnya bertahan.`

---

## Scene 4 — Ronde 3: Getah & Sisa Daun Talas → Layukan & Bingkai Apung (`00:29–00:38`, 21 kata)

- **Shot:** `medium` tampak atas-serong permukaan kolam bundar, dengan fokus pada pakan daun talas di air.
- **Sub-beats visual:**
  1. `00:29–00:33`: Daun talas segar dilempar langsung; getahnya menyebar dan potongan sisa membusuk di tepi sehingga air cepat keruh kecokelatan dan berbuih tipis.
  2. `00:33–00:38`: Daun talas dilayukan terlebih dahulu lalu diletakkan di dalam cincin pipa PVC apung (*bingkai pakan*), dan tangkai sisa diangkat bersih memakai serokan; air kembali jernih kehijauan segar.
- **SFX:** Tebar daun/pelet (`pellet-scatter`), klik pipa cincin apung (`pvc-snap`), kecipak angkat sisa (`water-splash`).
- **Narration:**
  Giliran dikasih daun talas segar, airnya keruh dan berbusa. Kamu layukan daunnya, taruh di bingkai apung, lalu angkat sisanya. Airnya jernih.
- **Captions (46 px, maks 2 baris):**
  `Giliran dikasih daun talas segar,` / `airnya keruh dan berbusa.` / `Kamu layukan daunnya, taruh di bingkai apung,` / `lalu angkat sisanya. Airnya jernih.`

---

## Scene 5 — Ronde 4: Hujan Deras Meluap → Pipa Pelimpah Berkasa (`00:38–00:47`, 20 kata)

- **Shot:** `medium-wide` sisi kanan kolam bundar saat badai hujan mengguyur halaman dan membasahi petak tanaman di sampingnya.
- **Sub-beats visual:**
  1. `00:38–00:42`: Hujan deras memicu tampias dan air kolam naik mendekati bibir terpal di sisi terbuka.
  2. `00:42–00:47`: Pipa pelimpah berujung kasa halus dipasang di bawah bibir atas; air hujan berlebih mengalir keluar ke petak tanah samping sementara gurame tertahan aman di dalam kolam.
- **SFX:** Deras hujan (`rain-shower`), klik pasang pipa PVC (`pvc-snap`), kucuran buangan pelimpah (`water-drain`).
- **Narration:**
  Begitu hujan deras turun, air kolam naik sampai bibir terpal. Kamu pasang pipa pelimpah berkasa di atas. Air keluar, ikannya aman.
- **Captions (46 px, maks 2 baris):**
  `Begitu hujan deras turun,` / `air kolam naik sampai bibir terpal.` / `Kamu pasang pipa pelimpah berkasa di atas.` / `Air keluar, ikannya aman.`

---

## Scene 6 — Ronde 5: Endapan Dasar & Oksigen Tenang → Pembuangan Tengah & Aerasi Halus (`00:47–00:57`, 21 kata)

- **Shot:** `close cutaway` dasar tengah kolam bundar dan permukaan air dengan gelembung udara.
- **Sub-beats visual:**
  1. `00:47–00:51`: Kotoran ikan dan remahan pakan mengumpul di titik tengah dasar kolam sementara beberapa gurame menyembul lama di permukaan.
  2. `00:51–00:57`: Keran pipa pembuangan dasar tengah dibuka untuk menyipon endapan keluar, lalu batu aerasi halus dipasang dengan gelembung lembut tanpa arus deras; gurame kembali berenang tenang di tengah kolom air.
- **SFX:** *Whoosh* masuk (`cam-whoosh`), putar keran & buangan dasar (`pvc-snap` + `water-drain`), alas gelembung halus (`water-bubbles`).
- **Narration:**
  Lama-lama, kotoran menumpuk di tengah dan ikannya sering menyembul. Kamu buka pembuangan dasar plus aerasi halus tanpa arus deras. Ikannya aktif lagi.
- **Captions (46 px, maks 2 baris):**
  `Lama-lama, kotoran menumpuk di tengah` / `dan ikannya sering menyembul.` / `Kamu buka pembuangan dasar plus aerasi halus` / `tanpa arus deras. Ikannya aktif lagi.`

---

## Scene 7 — Ronde 6: Predator Kucing & Burung → Jaring Penutup Rangka (`00:57–01:06`, 18 kata)

- **Shot:** `medium` bagian atas rangka *wiremesh* pada pagi hari dengan siluet burung/kucing di pagar belakang.
- **Sub-beats visual:**
  1. `00:57–01:01`: Pagi hari terlihat jejak cakaran di pinggir karpet talang dan jumlah gurame di permukaan tampak berkurang.
  2. `01:01–01:06`: Jaring penutup nilon dibentangkan rapat melingkari bibir rangka *wiremesh* dan dijepit klip; keesokan harinya burung/kucing melintas tanpa bisa menjangkau air dan semua ikan utuh.
- **SFX:** Bentang jaring (`fabric-net`), klik klip pengunci (`pvc-snap`), suasana pagi halaman (`yard-ambience`).
- **Narration:**
  Suatu pagi, ada bekas cakaran dan ikannya berkurang. Kamu bentangkan jaring penutup di atas rangka. Besoknya semuanya utuh.
- **Captions (46 px, maks 2 baris):**
  `Suatu pagi, ada bekas cakaran` / `dan ikannya berkurang.` / `Kamu bentangkan jaring penutup di atas rangka.` / `Besoknya semuanya utuh.`

---

## Scene 8 — Ronde 7: Persaingan Pakan & Ukuran → Sortir ke Kolam Kedua (`01:06–01:16`, 20 kata)

- **Shot:** `close cutaway` → *pan* ke kanan saat sebagian gurame kecil dipindahkan ke kolam bundar kedua di samping kolam utama.
- **Sub-beats visual:**
  1. `01:06–01:10`: Memasuki bulan keempat, gurame berukuran besar mendominasi bingkai pakan dan mengusir gurame yang lebih kecil sehingga ukurannya timpang.
  2. `01:10–01:16`: Tangan memakai serokan lembut menyortir gurame kecil ke kolam terpal bundar kedua tepat di sebelah; kedua kelompok makan tenang dan tumbuh merata.
- **SFX:** Kecipak serok & pindah ikan (`water-splash`), tebar pelet (`pellet-scatter`), *whoosh* geser kamera (`cam-whoosh`).
- **Narration:**
  Masuk bulan keempat, gurame besar mendominasi pakan. Kamu serok dan sortir yang kecil ke kolam kedua. Semuanya tumbuh rata.
- **Captions (46 px, maks 2 baris):**
  `Masuk bulan keempat, gurame besar mendominasi pakan.` / `Kamu serok dan sortir yang kecil ke kolam kedua.` / `Semuanya tumbuh rata.`

---

## Scene 9 — Sistem Stabil (`01:16–01:24`, 18 kata)

- **Shot:** `wide` sudut halaman penuh menampilkan dua kolam bundar *wiremesh* lengkap di bawah atap bening dan *paranet*.
- **Sub-beats visual:**
  1. `01:16–01:20`: Hujan turun lalu mereda ke cahaya sore cerah; air berlebih mengalir keluar lewat pelimpah berkasa sementara suhu air tetap teduh terjaga.
  2. `01:20–01:24`: Gelembung aerasi halus naik teratur, air tampak jernih, jaring pelindung terpasang rapi, dan seluruh gurame ukuran konsumsi menyambar pelet serta daun talas di bingkai apung.
- **SFX:** Hujan singkat (`rain-shower`), aliran pelimpah (`water-drain`), alas udara halus (`water-bubbles`), tebar pakan (`pellet-scatter`).
- **Narration:**
  Sekarang, hujan atau terik, suhu terjaga, air jernih bergelembung halus, dan semua gurame makan lahap di bingkai daunnya.
- **Captions (46 px, maks 2 baris):**
  `Sekarang, hujan atau terik, suhu terjaga,` / `air jernih bergelembung halus,` / `dan semua gurame makan lahap di bingkai daunnya.`

---

## Scene 10 — Monetisasi: Timbang Panen Pertama (`01:24–01:36`, 26 kata + tahan tag ≥3 dtk)

- **Shot:** `medium` area samping kolam bundar jadi (kolam tetap terlihat jelas di belakang sebagai landmark); keranjang ikan & timbangan gantung mengisi ≥40% lebar frame.
- **Sub-beats visual:**
  1. `01:24–01:28`: Enam bulan berjalan, jaring dibuka sebagian dan gurame ukuran konsumsi diserok masuk ke keranjang timbangan gantung di samping kolam.
  2. `01:28–01:31`: Jarum timbangan berayun mantap ke `40 kg`; pada kata *"empat puluh kilo"*, tag harga kertas jatuh dari paku tiang timbangan (*drop* `0,2 s`, ayun redam `0,5 s`) menampilkan `40 kg × Rp45.000`.
  3. `01:31–01:36`: Chip kuning `≈ Rp1.800.000` muncul mekar `0,15 s` bersama catatan `estimasi harga pasar / Nov 2026`, lalu ditahan penuh `≥3,0 s` (di 1x) sebelum memotong ke penutup lebar.
- **SFX:** Kecipak panen (`water-splash`), rantai timbangan gantung (`scale-chain`), klik jatuh tag (`tag-click`), pop total kuning (`tag-pop`).
- **Narration:**
  Enam bulan kemudian, panen pertama kamu timbang, sekitar empat puluh kilo. Di pasar empat puluh lima ribu per kilo, jadi sekitar satu juta delapan ratus ribu.
- **Captions (46 px, maks 2 baris):**
  `Enam bulan kemudian, panen pertama kamu timbang,` / `sekitar empat puluh kilo.` / `Di pasar empat puluh lima ribu per kilo,` / `jadi sekitar satu juta delapan ratus ribu.`

---

## Scene 11 — Penutup Lebar & End Card (`01:36–01:47`, 24 kata + 0,625 dtk *end card*)

- **Shot:** `wide` tarik mundur penuh menampilkan sudut halaman hidup dengan kolam bundar gurame, tanaman subur di samping, rumah hangat, dan dedaunan bergoyang di latar 4-lapis 2.5D; ditutup *hard cut* ke *end card* identik thumbnail.
- **Sub-beats visual:**
  1. `01:36–01:43`: Kamera *pull-out* lembut memperlihatkan kolam gurame beroperasi penuh di halaman bersama keranjang hasil panen.
  2. `01:43–01:46.4`: Pada kalimat tanya penutup, kata berurutan **`bikin di halaman`** tetap menyala kuning `#FFD44D` hingga akhir kalimat sementara handle `@bikindihalaman.id` muncul halus di bawah caption.
  3. `01:46.4–01:47.1` (`0,625 s` di 1x / `0,5 s` di 1,25x): *Hard cut* ke *end card* yang identik dengan thumbnail PNG (caption terhapus, panel gelap atas di area aman 1080 × 1080 dengan judul **Kolam gurame** / **di sudut halaman**).
- **SFX:** Suasana pagi/sore halaman lembut (`yard-ambience`), *whoosh* tarik kamera (`cam-whoosh`).
- **Narration:**
  Selamat, kamu sudah punya kolam gurame di halaman, lengkap dengan peneduh dan jaring. Habis ini, apa lagi yang mau kamu bikin di halaman?
- **Captions (46 px, maks 2 baris):**
  `Selamat, kamu sudah punya kolam gurame di halaman,` / `lengkap dengan peneduh dan jaring.` / `Habis ini, apa lagi yang mau kamu bikin di halaman?`
