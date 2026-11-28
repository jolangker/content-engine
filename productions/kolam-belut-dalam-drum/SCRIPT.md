# Bikin Kolam Belut dalam Drum Bekas

- **Script version:** v1
- **Board:** `budidaya-di-halaman` (Revision 10 — Editorial v9 / Visual v5)
- **Language & POV:** Bahasa Indonesia percakapan; `"kamu"` merujuk tunggal pada perakit/pemelihara kolam di satu sudut halaman rumah yang sama.
- **Voice & Audio:** ElevenLabs **Roger** (`CwhRBWXzGAHq8TQ4Fs17`, `eleven_v4`, user-authorized `episode_override` karena suara default board `Pribs` `5g0yKK2JwTRka0IG61Hh` ditolak `voice_not_found` pada free-tier API key), BGM `none`, 41 SFX organik berdasar event dari pustaka Visual v5 board (`assets/sfx/manifest.json`).
- **Duration & word budget (measured):** **250 kata lisan** (`2,37 kata/dtk` -> narasi mentah `105,48 dtk` -> narasi terpasang dengan jeda sunyi `109,47 dtk` -> komposisi 1x **`110,38 dtk`** [`2649` frame @ 24 fps], masuk kontrak `90,0–112,5 dtk` di 1x dan **`88,30 dtk`** di ekspor 1,25x / 30 fps).
- **Event map:** 18 kejadian utama (1 hook bangun awal + 7 ronde masalah–perbaikan [14 kejadian] + 1 uji stabil + 1 adegan timbang estimasi hasil + 1 penutup lebar & *end card*).

---

## On-screen copy (di luar caption ucapan)

- **Thumbnail & End Card (`0,625 dtk` di 1x / `0,5 dtk` di 1,25x):** Panel gelap di atas tampak lebar kolam drum belut jadi (dalam area aman 1080 × 1080 tengah, `y 420–1500`) dengan judul 2 baris 104 px DM Sans 900:
  - Baris 1: **Bikin kolam belut** (`Bikin` putih hangat `#FFF9E8`, **kolam belut** kuning `#FFD44D`)
  - Baris 2: **di drum bekas** (putih hangat `#FFF9E8`)
- **Price tag (Adegan 10 — Timbang Panen):** Tag kertas 400 px tergantung di paku tiang timbangan (terjangkar di *world space*):
  - Baris 1 (38 px): `6 kg × Rp72.500`
  - Chip total (54 px, latar kuning `#FFD44D`): `≈ Rp435.000`
  - Catatan (28 px, 2 baris): `estimasi pasar Jatim` / `Nov 2026`
- **Closing signature (akhir Adegan 11):** Tiga kata berurutan **bikin di halaman** tetap tersorot kuning (`#FFD44D`) sampai akhir kalimat; `@bikindihalaman.id` muncul halus (*fade in*) kecil di bawah caption tanpa menutupi drum.

---

## Scene 1 — Bangun Awal Prematur & Kabur Saat Hujan Malam (`00:00–00:11`, 29 kata)

- **Shot:** `wide` sudut halaman tanah kosong dengan rumah dan daun pisang bergoyang di latar 4-lapis 2.5D; *push-in* cepat ke bibir drum saat hujan malam.
- **Sub-beats visual:**
  1. `00:00–00:04` (`Frame 0` + gerak `0,25 dtk`): Sudut halaman kosong dengan drum plastik biru 200 L berdiri di tanah; tangan perakit langsung merebahkan drum ke ganjal kayu dengan sisi atas terbelah memanjang (*micro-impact* saat drum mendarat).
  2. `00:04–00:08`: Sekop menuang lumpur sawah ke dalam irisan drum, air diisi hingga mendekati bibir, lalu bibit belut (*Monopterus albus* 10–12 cm) dilepas masuk.
  3. `00:08–00:11`: Langit gelap bergulung membawa hujan malam (lampu jendela rumah menyala, daun pisang bergoyang kencang); muka air naik menyentuh bibir basah, dan kamera *punch-in* mengikuti belut licin yang mulai merayap melewati tepi drum.
- **SFX:** Hentakan drum & ganjal (`wood-stake`), cedokan lumpur (`dig-soil`), kucuran air (`water-pour`), kecipak bibit (`water-splash`), derai hujan malam (`rain-shower`), *whoosh* kamera (`cam-whoosh`).
- **Narration:**
  Kalo kamu rebahkan drum plastik di sudut halaman, habis itu kamu isi lumpur dan lepas bibit belut, kamu sudah punya kolam belut. Tapi pas hujan malamnya belutnya merayap keluar.
- **Captions (46 px, maks 2 baris):**
  `Kalo kamu rebahkan drum plastik di sudut halaman,` / `habis itu kamu isi lumpur dan lepas bibit belut,` / `kamu sudah punya kolam belut.` / `Tapi pas hujan malamnya belutnya merayap keluar.`

---

## Scene 2 — Ronde 1: Luapan Hujan → Pipa Pelimpah Berkasa (`00:11–00:20`, 22 kata)

- **Shot:** `close` irisan bibir atas drum menghadap langit hujan malam (tepi drum dan dinding rumah sebagai penanda).
- **Sub-beats visual:**
  1. `00:11–00:14`: Sorot dekat air hujan yang menyentuh bibir drum basah dengan belut licin meluncur keluar melewati tepi.
  2. `00:14–00:17`: Tangan perakit melubangi dinding drum beberapa senti di bawah bibir dan memasang pipa pelimpah PVC pendek berujung kawat kasa halus (*snap* + *micro-impact*).
  3. `00:17–00:20`: Hujan tetap turun, kelebihan air memancar keluar lewat pipa pelimpah menjaga ruang bebas di bawah bibir, sementara belut tertahan kasa di dalam drum.
- **SFX:** Hujan tipis (`rain-shower`), klik pasang pipa PVC (`pvc-snap`), aliran air pelimpah (`water-drain`), kecipak tertahan (`water-splash`).
- **Narration:**
  Air penuh sampai bibir bikin belut licin gampang lolos. Kamu pasang pipa pelimpah berkasa di bawah bibir drum. Air keluar, belut tertahan.
- **Captions:**
  `Air penuh sampai bibir bikin belut licin gampang lolos.` / `Kamu pasang pipa pelimpah berkasa di bawah bibir drum.` / `Air keluar, belut tertahan.`

---

## Scene 3 — Ronde 2: Lumpur Mentah Panas & Bergas → Fermentasi Dua Minggu (`00:20–00:30`, 22 kata)

- **Shot:** `medium` potongan penampang drum saat pagi cerah (pipa pelimpah berkasa tetap terlihat di sisi kanan).
- **Sub-beats visual:**
  1. `00:20–00:23`: Langit bergeser ke pagi; gelembung gas dan pendaran hangat naik dari lapisan lumpur mentah di dasar drum sementara belut muncul lemas di permukaan air.
  2. `00:23–00:27`: Belut dipindahkan sementara ke ember air bersih di samping drum; tangan perakit menuang larutan starter EM4 ke campuran lumpur-jerami, menutup sebentar sambil indikator waktu bergeser 14 hari hingga lumpur berubah cokelat gelap dan sejuk, lalu mengganti air atasnya.
  3. `00:27–00:30`: Belut dikembalikan ke drum; mereka langsung menyelam lincah dan menyusup membuat lubang di lumpur matang.
- **SFX:** Gelembung gas lumpur (`water-bubbles`), ciduk pindah ember (`water-splash`), tuang starter (`water-pour`), aduk lumpur (`dig-soil`), kecipak menyelam (`water-splash`).
- **Narration:**
  Besok paginya, belut naik lemas. Lumpur mentahnya panas dan bergas. Kamu pindahkan belutnya, fermentasi lumpur dua minggu. Setelah dingin, mereka menyusup lagi.
- **Captions:**
  `Besok paginya, belut naik lemas.` / `Lumpur mentahnya panas dan bergas.` / `Kamu pindahkan belutnya, fermentasi lumpur dua minggu.` / `Setelah dingin, mereka menyusup lagi.`

---

## Scene 4 — Ronde 3: Terik Siang & Silau → Eceng Gondok & Paranet (`00:30–00:39`, 22 kata)

- **Shot:** `medium-wide` drum di sudut halaman di bawah matahari tengah hari terik (pipa pelimpah dan lumpur gelap tetap terlihat).
- **Sub-beats visual:**
  1. `00:30–00:33`: Matahari tepat di atas kepala dengan pendaran panas; air dangkal di drum terbuka memantul terang menyilaukan dan belut bergerak gelisah keluar-masuk permukaan.
  2. `00:33–00:36`: Tangan perakit menaruh rumpun eceng gondok menutupi sekitar tiga perempat permukaan air, lalu membentangkan jaring paranet peneduh di atas rangka tiang drum (*tracking* lateral mengikuti tarikan kain).
  3. `00:36–00:39`: Bayangan sejuk jatuh di atas drum; warna air mendingin dan belut tenang bersembunyi di sela akar eceng gondok.
- **SFX:** Gesekan kain paranet (`fabric-net`), letak tanaman ke air (`water-splash`), hentakan tiang peneduh (`wood-stake`).
- **Narration:**
  Pas tengah hari, air drum memanas dan terlalu terang. Kamu isi eceng gondok lalu pasang paranet di atasnya. Airnya adem, belut tenang.
- **Captions:**
  `Pas tengah hari, air drum memanas dan terlalu terang.` / `Kamu isi eceng gondok lalu pasang paranet di atasnya.` / `Airnya adem, belut tenang.`

---

## Scene 5 — Ronde 4: Pakan Siang Tak Tersentuh → Jadwal Pakan Sore (`00:39–00:47`, 21 kata)

- **Shot:** `close` irisan lapisan air dangkal, akar eceng gondok, dan permukaan lumpur (naungan paranet terasa di bagian atas).
- **Sub-beats visual:**
  1. `00:39–00:42`: Di bawah cahaya siang terang, butiran pakan jatuh ke permukaan lumpur tanpa disentuh sementara belut tetap tersembunyi di lubang; pakan sisa mulai memudar keruh.
  2. `00:42–00:45`: Langit berputar cepat ke senja jingga–malam (lampu rumah menyala); tangan perakit menabur pakan terukur di sela akar eceng gondok.
  3. `00:45–00:47`: Begitu gelap, kepala-kepala belut langsung bermunculan serempak menyambar pakan sampai bersih.
- **SFX:** Taburan pakan (`pellet-scatter`), *cam-whoosh* transisi senja, kecipak cepat belut menyambar pakan (`water-splash`).
- **Narration:**
  Giliran kamu tebar pakan siang, belut sembunyi karena aktif malam. Kamu geser pakan ke sore hari. Begitu gelap, pakannya langsung habis.
- **Captions:**
  `Giliran kamu tebar pakan siang, belut sembunyi` / `karena aktif malam. Kamu geser pakan ke sore hari.` / `Begitu gelap, pakannya langsung habis.`

---

## Scene 6 — Ronde 5: Air Keruh & Bau Amonia → Keran Kuras & Pipa Tetes (`00:47–00:56`, 21 kata)

- **Shot:** `medium` sisi bawah dan samping drum potongan cutaway (pipa pelimpah, eceng gondok, dan paranet tetap menjadi penanda).
- **Sub-beats visual:**
  1. `00:47–00:50`: Beberapa minggu kemudian, lapisan air di atas lumpur berubah cokelat keruh dengan garis uap bau amonia tipis naik ke udara.
  2. `00:50–00:53`: Kamera *push-in* ke dinding bawah drum saat tangan perakit memasang keran kuras bawah berkasa dan menyambung pipa tetes air bersih di ujung berlawanan (*snap* PVC + *micro-impact*).
  3. `00:53–00:56`: Air keruh mengalir keluar lewat keran bawah sementara percikan tetes air segar mengisi pelan dari atas; warna air kembali jernih dan garis bau hilang.
- **SFX:** Klik pasang pipa/keran (`pvc-snap`), aliran kuras air (`water-drain`), kucuran tetes lembut (`water-pour`).
- **Narration:**
  Beberapa minggu jalan, air berubah cokelat dan bau amonia. Kamu pasang keran kuras bawah dan pipa tetes air bersih. Baunya hilang.
- **Captions:**
  `Beberapa minggu jalan, air berubah cokelat dan bau amonia.` / `Kamu pasang keran kuras bawah dan pipa tetes air bersih.` / `Baunya hilang.`

---

## Scene 7 — Ronde 6: Jejak Predator Pagi → Tutup Rangka Kawat Kasa (`00:56–01:04`, 20 kata)

- **Shot:** `medium-wide` sudut atas bukaan drum di pagi cerah (paranet, pipa tetes, pelimpah, dan keran bawah tetap terpasang).
- **Sub-beats visual:**
  1. `00:56–00:59`: Cahaya pagi menampakkan jejak kaki kucing basah di tepi drum dan ekor kucing menjauh di latar, sementara populasi belut di dalam drum tampak lebih sedikit.
  2. `00:59–01:02`: Tangan perakit meletakkan dan mengaitkan bingkai tutup kawat kasa yang bisa dibuka-tutup rapat di atas bukaan drum (*micro-impact*).
  3. `01:02–01:04`: Transisi malam ke pagi berikutnya; kucing hanya mengintip di luar kawat tanpa celah masuk, dan kawanan belut di dalam drum utuh.
- **SFX:** Hentakan ringan bingkai kayu/kasa (`wood-stake`), gesekan kait jaring (`fabric-net`), suasana halaman pagi pelan (`yard-ambience`).
- **Narration:**
  Suatu pagi, muncul jejak kucing di tepi drum dan belut berkurang. Kamu pasang tutup rangka kawat kasa. Besoknya jumlahnya utuh.
- **Captions:**
  `Suatu pagi, muncul jejak kucing di tepi drum` / `dan belut berkurang. Kamu pasang tutup rangka kawat kasa.` / `Besoknya jumlahnya utuh.`

---

## Scene 8 — Ronde 7: Beda Ukuran & Saling Gigit → Sortir ke Drum Kedua (`01:04–01:13`, 21 kata)

- **Shot:** `close` irisan dalam drum memperlihatkan ukuran belut, lalu menggeser mengikuti serokan ke drum kedua yang masuk di samping.
- **Sub-beats visual:**
  1. `01:04–01:07`: Masuk bulan kedua, beberapa belut tumbuh jauh lebih gemuk dan panjang lalu mengejar menggigit belut yang masih kecil di ruang yang sama.
  2. `01:07–01:10`: Tutup kasa dibuka; kamera menggeser sedikit memperlihatkan drum kedua yang sudah disiapkan di sebelah, lalu serokan halus menyortir belut kecil dan memindahkannya ke drum kedua.
  3. `01:10–01:13`: Kedua drum kini terisi belut berukuran seragam yang bergerak tenang tanpa saling kejar.
- **SFX:** Kecipak kejaran (`water-splash`), cidukan serokan (`fabric-net` + `water-splash`), hentakan drum kedua (`wood-stake`).
- **Narration:**
  Masuk bulan kedua, belut besar mulai menggigit yang kecil. Kamu sortir ukurannya, pindahkan yang kecil ke drum kedua. Semuanya tumbuh rata.
- **Captions:**
  `Masuk bulan kedua, belut besar mulai menggigit yang kecil.` / `Kamu sortir ukurannya, pindahkan yang kecil ke drum kedua.` / `Semuanya tumbuh rata.`

---

## Scene 9 — Sistem Stabil: Uji Hujan & Pakan Sore (`01:13–01:21`, 21 kata)

- **Shot:** `wide` sudut halaman penuh memperlihatkan kedua drum lengkap dengan semua komponen terpasang utuh.
- **Sub-beats visual:**
  1. `01:13–01:17`: Hujan sore turun lagi; kelebihan air mengalir tenang keluar lewat pipa pelimpah berkasa, paranet dan eceng gondok menjaga drum tetap teduh, tutup kasa terpasang rapat.
  2. `01:17–01:21`: Tutup dibuka sejenak untuk menabur pakan sore; belut-belut gemuk dan seragam muncul menyambar dengan aktif di air yang jernih.
- **SFX:** Rintik hujan (`rain-shower`), aliran pelimpah (`water-drain`), taburan pakan (`pellet-scatter`), kecipak makan serempak (`water-splash`).
- **Narration:**
  Saat hujan turun lagi, luapan keluar lewat pelimpah, air tetap teduh, tutup kasa aman, dan pakan sore habis. Kolam drumnya stabil.
- **Captions:**
  `Saat hujan turun lagi, luapan keluar lewat pelimpah,` / `air tetap teduh, tutup kasa aman, dan pakan sore habis.` / `Kolam drumnya stabil.`

---

## Scene 10 — Monetisasi: Panen & Timbang Pertama (`01:21–01:34`, 27 kata)

- **Shot:** `medium` di samping drum belut yang sudah jadi (drum dan paranet tetap tampak sebagai penanda; interaksi timbangan gantung + baskom panen mengisi ≥40% lebar layar; paku tag terjangkar di *world space*).
- **Sub-beats visual:**
  1. `01:21–01:25`: Keran kuras dibuka sedikit, eceng gondok diangkat, lalu tangan perakit mengangkat baskom/jaring berisi belut konsumsi mengilap ke timbangan gantung di samping drum; jarum timbangan turun lalu berhenti (*micro-impact*).
  2. `01:25–01:28`: Pada kata `"enam kilo"`, tag kertas 400 px turun (`0,2 dtk`, ayunan reda `0,5 dtk`) di paku tiang timbangan; `6 kg` muncul (`0,15 dtk`).
  3. `01:28–01:31`: Pada `"tujuh puluh dua ribuan"`, `× Rp72.500` muncul (`0,15 dtk`); pada `"empat ratus"`, chip kuning `≈ Rp435.000` dan catatan `estimasi pasar Jatim / Nov 2026` muncul saat tag memanjang ke bawah.
  4. `01:31–01:34`: Tag lengkap bertahan penuh (`≥3,0 dtk` di 1x) sementara belut panen berkilau di dalam baskom.
- **SFX:** Kuras singkat (`water-drain`), kecipak panen (`water-splash`), rantai/pegas timbangan (`scale-chain`), klik kertas tag (`tag-click`), pop angka (`tag-pop`).
- **Narration:**
  Empat bulan kemudian, panen pertama kamu timbang. Kira-kira enam kilo. Di pasar sekitar tujuh puluh dua ribuan per kilo, jadi kurang lebih empat ratus tiga puluh ribuan.
- **Captions:**
  `Empat bulan kemudian, panen pertama kamu timbang.` / `Kira-kira enam kilo. Di pasar sekitar` / `tujuh puluh dua ribuan per kilo, jadi kurang lebih` / `empat ratus tiga puluh ribuan.`

---

## Scene 11 — Penutup Lebar & End Card (`01:34–01:44,6`, 24 kata + `0,625 dtk` end card)

- **Shot:** `wide` tarik perlahan (*living drift*) ke tampak penuh sudut halaman dengan kedua drum lengkap (ganjal kayu, pipa pelimpah berkasa, eceng gondok, paranet, pipa tetes, keran kuras bawah, tutup kawat kasa) dan baskom panen di sisi; diakhiri *hard cut* ke *end card* thumbnail.
- **Sub-beats visual:**
  1. `01:34–01:39`: Tampak lebar sudut halaman sore hangat dengan dedaunan bergoyang lembut, riak air drum hidup, dan seluruh komponen terpasang rapi.
  2. `01:39–01:44`: Pada kalimat tanya penutup, tiga kata berurutan **bikin di halaman** tetap tersorot kuning (`#FFD44D`) sampai akhir kalimat, dan `@bikindihalaman.id` *fade in* halus di bawah caption.
  3. `01:44–01:44,625`: *Hard cut* ke *end card* (`0,625 dtk` di 1x = `0,5 dtk` di 1,25x) identik dengan thumbnail **BIKIN KOLAM BELUT / DI DRUM BEKAS** (caption bersih).
- **SFX:** Suasana sore halaman sangat pelan (`yard-ambience`, tanpa BGM), hening bersih pada *end card*.
- **Narration:**
  Selamat, kamu sudah punya kolam belut sendiri dari drum bekas, lengkap sampai panen pertama. Habis ini, apa lagi yang mau kamu bikin di halaman?
- **Captions:**
  `Selamat, kamu sudah punya kolam belut sendiri dari drum bekas,` / `lengkap sampai panen pertama.` / `Habis ini, apa lagi yang mau kamu bikin di halaman?` *(kuning tertahan di **bikin di halaman** + `@bikindihalaman.id` fade in di bawah)*
