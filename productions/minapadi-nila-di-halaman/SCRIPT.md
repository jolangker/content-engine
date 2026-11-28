# Bikin Petak Minapadi Nila di Halaman

- **Script version:** v1
- **Board:** `budidaya-di-halaman` (Revision 10 — Editorial v9 / Visual v5)
- **Language & POV:** Bahasa Indonesia percakapan; `"kamu"` merujuk tunggal pada perakit/pemelihara petak minapadi di satu sudut halaman rumah yang sama.
- **Voice & Audio:** ElevenLabs **Roger** (`CwhRBWXzGAHq8TQ4Fs17`, `eleven_v4`, `episode_override` fallback konsisten seri karena suara default board Pribs `5g0yKK2JwTRka0IG61Hh` mengembalikan HTTP 400 pada API key aktif), BGM `none`, SFX organik berdasar event dari pustaka Visual v5 board (`boards/budidaya-di-halaman/assets/sfx/manifest.json`).
- **Duration & word budget (estimated pre-synthesis):** **235 kata lisan**. Pada kecepatan terukur Roger (`2,49 kata/dtk`): prediksi narasi mentah `~94,4 dtk`, prediksi komposisi 1x (termasuk jeda sunyi antar-adegan + tahan tag harga ≥3 dtk + `0,625 dtk` *end card*) **`~101–104 dtk`** — masuk jendela kontrak `90,0–112,5 dtk` di 1x (**`~81–83 dtk`** pada ekspor 1,25x / 30 fps). Akan direkonsiliasi dengan waktu terukur sesudah *take* tunggal disintesis.
- **Event map:** 18 kejadian utama (1 hook bangun awal + 7 ronde masalah–perbaikan [14 kejadian] + 1 uji stabil + 1 adegan timbang estimasi panen + 1 penutup lebar & *end card*).

---

## On-screen copy (di luar caption ucapan)

- **Thumbnail & End Card (`0,625 dtk` di 1x / `0,5 dtk` di 1,25x):** Panel gelap di atas tampak lebar petak minapadi jadi berparit *caren* dan rumpun padi menguning (dalam area aman 1080 × 1080 tengah, `y 420–1500`) dengan judul 2 baris 104 px DM Sans 900:
  - Baris 1: **Bikin minapadi** (`Bikin` putih hangat `#FFF9E8`, **minapadi** kuning `#FFD44D`)
  - Baris 2: **di sudut halaman** (putih hangat `#FFF9E8`)
- **Price tag (Adegan 10 — Timbang Panen Nila + Padi):** Tag kertas 400 px tergantung di paku tiang timbangan gantung di samping petak minapadi jadi (terjangkar di *world space*):
  - Baris 1 (38 px): `15 kg × Rp34.000`
  - Chip total (50 px, latar kuning `#FFD44D`): `≈ Rp510.000`
  - Catatan (28 px, 2 baris): `estimasi harga pasar` / `Nov 2026`
- **Closing signature (akhir Adegan 11):** Tiga kata berurutan **bikin di halaman** tetap tersorot kuning (`#FFD44D`) sampai akhir kalimat; `@bikindihalaman.id` muncul halus (*fade in*) kecil di bawah caption tanpa menutupi petak minapadi.

---

## Scene 1 — Bangun Awal Prematur & Bibit Padi Tercabut (`00:00–00:11`, 25 kata)

- **Shot:** `wide` sudut halaman tanah hangat kosong dengan rumah tetangga, pagar kayu, dan pohon pisang bergoyang di latar 4-lapis 2.5D; *punch-in* ke permukaan petak berlumpur.
- **Sub-beats visual:**
  1. `00:00–00:03` (`Frame 0` + gerak `0,25 dtk`): Sudut halaman kosong dengan bingkai kayu/bambu rendah, terpal biru terlipat, dan baki bibit padi; tangan perakit langsung membentangkan terpal, mengisi lumpur gelap dan air dangkal.
  2. `00:03–00:07`: Deretan bibit padi hijau muda ditanam berbaris di lumpur, lalu benih ikan nila langsung dilepas ke genangan dangkal di antaranya.
  3. `00:07–00:11`: Cahaya bergeser ke pagi berikutnya; kamera *push-in* memperlihatkan ikan nila mengaduk dasar dangkal hingga beberapa rumpun bibit padi mengambang tercabut di permukaan air.
- **SFX:** Bentang terpal (`tarp-rustle`), gali/isi lumpur (`dig-soil`), kucuran air (`water-pour`), kecipak lepas nila (`water-splash`), *whoosh* push-in (`cam-whoosh`), suasana pagi halaman (`yard-ambience`).
- **Narration:**
  Kalo kamu hamparkan terpal isi lumpur di halaman, kemudian kamu tanam padi dan lepas nila, kamu sudah punya minapadi. Tapi besoknya bibit padinya mengambang tercabut.
- **Captions (46 px, maks 2 baris):**
  `Kalo kamu hamparkan terpal isi lumpur di halaman,` / `kemudian kamu tanam padi dan lepas nila,` / `kamu sudah punya minapadi.` / `Tapi besoknya bibit padinya mengambang tercabut.`

---

## Scene 2 — Ronde 1: Akar Belum Kuat & Ikan Mengaduk → Parit Caren Keliling (`00:11–00:20`, 22 kata)

- **Shot:** `close cutaway` irisan penampang petak terpal yang memperlihatkan lapisan lumpur datar vs pembentukan parit dalam (*caren*) di tepi.
- **Sub-beats visual:**
  1. `00:11–00:14`: Irisan dekat memperlihatkan akar bibit padi baru masih pendek dan renggang sementara gerakan nila langsung mengaduk lumpur di pangkalnya.
  2. `00:14–00:17`: Tangan perakit membentuk parit *caren* lebih dalam di tepi petak dengan tanggul penahan rendah di sisi tengah (*pelataran*), lalu menahan nila sementara di dalam *caren*.
  3. `00:17–00:20`: Akar padi di *pelataran* tumbuh mencengkeram kuat; bibit berdiri tegak kokoh sementara nila berenang aman di *caren* yang dalam.
- **SFX:** Serok/bentuk lumpur (`dig-soil`), ketuk batas papan/bambu (*pelataran*) (`wood-stake`), kecipak air (`water-splash`).
- **Narration:**
  Akar padi baru belum kuat, nilanya mengaduk dasar. Kamu bentuk parit caren dalam di tepi, tahan nila di sana dulu. Padinya kokoh.
- **Captions (46 px, maks 2 baris):**
  `Akar padi baru belum kuat, nilanya mengaduk dasar.` / `Kamu bentuk parit caren dalam di tepi,` / `tahan nila di sana dulu. Padinya kokoh.`

---

## Scene 3 — Ronde 2: Panas Siang di Air Dangkal → Paranet Parsial di Atas Caren (`00:20–00:29`, 20 kata)

- **Shot:** `medium` tampak sisi petak minapadi di bawah matahari terik siang (rumpun padi di tengah dan parit *caren* di tepi jelas terlihat sebagai penanda).
- **Sub-beats visual:**
  1. `00:20–00:23`: Matahari terik memancarkan gelombang panas di atas genangan dangkal; ikan nila tampak melambat lesu mendekati tepi *caren*.
  2. `00:23–00:26`: Tangan perakit memasang tiang pendek dan menarik jaring peneduh *paranet* khusus menaungi sisi atas parit *caren* saja, tidak menutup bagian tengah padi.
  3. `00:26–00:29`: Bayangan sejuk jatuh tepat di atas *caren* sehingga nila berenang lincah kembali, sementara petak padi di tengah tetap menerima sinar matahari penuh.
- **SFX:** Ketuk tiang bambu (`wood-stake`), tarik jaring *paranet* (`fabric-net`), *whoosh* geser kamera (`cam-whoosh`).
- **Narration:**
  Pas tengah hari, air dangkal cepat panas bikin nila lesu. Kamu tarik paranet teduh di atas caren saja. Padinya tetap terang.
- **Captions (46 px, maks 2 baris):**
  `Pas tengah hari, air dangkal cepat panas` / `bikin nila lesu.` / `Kamu tarik paranet teduh di atas caren saja.` / `Padinya tetap terang.`

---

## Scene 4 — Ronde 3: Hujan Deras Meluap → Pipa Pelimpah Berkasa (`00:29–00:38`, 19 kata)

- **Shot:** `medium-wide` sisi kanan petak minapadi saat hujan deras mengguyur halaman dan petak tanaman di sampingnya (*caren* dan *paranet* tetap tampak).
- **Sub-beats visual:**
  1. `00:29–00:32`: Langit mendung gelap dan hujan deras mengguyur; permukaan air naik cepat hingga menyentuh bibir pematang/bingkai terpal.
  2. `00:32–00:35`: Tangan perakit memasang pipa pelimpah PVC dengan ujung tertutup kasa rapat tepat di batas ketinggian air aman.
  3. `00:35–00:38`: Kelebihan air hujan mengucur keluar lewat pipa ke petak tanah samping sementara ikan nila tertahan aman oleh saringan kasa.
- **SFX:** Derai hujan (`rain-shower`), klik pasang pipa PVC (`pvc-snap`), kucuran buangan pelimpah (`water-drain`).
- **Narration:**
  Begitu hujan deras turun, air naik sampai bibir pematang. Kamu pasang pipa pelimpah berkasa di tepi. Air keluar, nila aman.
- **Captions (46 px, maks 2 baris):**
  `Begitu hujan deras turun, air naik` / `sampai bibir pematang.` / `Kamu pasang pipa pelimpah berkasa di tepi.` / `Air keluar, nila aman.`

---

## Scene 5 — Ronde 4: Hama Keong Mas → Ajir Jebakan Bambu & Pungut Manual (`00:38–00:47`, 22 kata)

- **Shot:** `close cutaway` pangkal rumpun padi muda dan tepian air *caren* (bingkai terpal dan *pelimpah* di latar tetap tampak).
- **Sub-beats visual:**
  1. `00:38–00:41`: Seminggu berjalan; beberapa keong mas merayap memotong pangkal batang padi muda dan kelompok telur berwarna merah muda menempel di batang/dinding.
  2. `00:41–00:44`: Tanpa memakai semprotan kimia (ikon botol kimia ditiadakan, langsung aksi fisik), tangan perakit menancapkan bilah ajir bambu di tepi *caren* sebagai tempat keong berkumpul dan bertelur lalu memungut keong serta gugusan telur secara manual ke ember.
  3. `00:44–00:47`: Pangkal batang padi kembali bersih utuh tumbuh hijau sementara ikan nila di air bawahnya tetap sehat tanpa racun.
- **SFX:** Ketuk tancap ajir bambu (`wood-stake`), kecipak angkat keong (`water-splash`), klik ember (`tag-click`).
- **Narration:**
  Seminggu jalan, keong mas memotong batang muda dan menaruh telur merah muda. Tanpa obat kimia, kamu tancap ajir jebakan lalu pungut. Batang selamat.
- **Captions (46 px, maks 2 baris):**
  `Seminggu jalan, keong mas memotong batang muda` / `dan menaruh telur merah muda.` / `Tanpa obat kimia, kamu tancap ajir jebakan` / `lalu pungut. Batang selamat.`

---

## Scene 6 — Ronde 5: Air Caren Keruh & Oksigen Pagi Rendah → Aerasi Halus di Caren (`00:47–00:56`, 19 kata)

- **Shot:** `medium` irisan parit *caren* pada pagi hari berkabut tipis (*paranet* atas dan rumpun padi yang sudah meninggi di tengah tetap tampak).
- **Sub-beats visual:**
  1. `00:47–00:50`: Memasuki bulan kedua, air di parit *caren* tampak keruh kecokelatan dan beberapa ikan nila menyembul di permukaan mencari udara pagi.
  2. `00:50–00:53`: Tangan perakit meletakkan selang dan batu aerasi halus di dasar *caren* yang terhubung ke pompa udara kecil di pinggir bingkai.
  3. `00:53–00:56`: Tirai gelembung oksigen halus naik teratur, air berangsur jernih kehijauan segar, dan nila kembali berenang aktif di dasar hingga tengah kolom air.
- **SFX:** *Whoosh* masuk (`cam-whoosh`), klik sambungan selang (`pvc-snap`), gelembung aerasi halus (`water-bubbles`).
- **Narration:**
  Masuk bulan kedua, air caren keruh dan nila menyembul pagi hari. Kamu pasang aerasi halus di dasar caren. Airnya segar.
- **Captions (46 px, maks 2 baris):**
  `Masuk bulan kedua, air caren keruh` / `dan nila menyembul pagi hari.` / `Kamu pasang aerasi halus di dasar caren.` / `Airnya segar.`

---

## Scene 7 — Ronde 6: Burung Pipit Mematuk Bulir Menguning → Jaring Pelindung Melengkung (`00:56–01:05`, 19 kata)

- **Shot:** `medium-wide` bagian atas rumpun padi yang mulai merunduk menguning di bawah langit cerah (*paranet* *caren* dan aerasi tetap terlihat).
- **Sub-beats visual:**
  1. `00:56–00:59`: Bulir-bulir padi berubah keemasan merunduk; kawanan kecil burung pipit menukik hinggap mematuk gabah matang.
  2. `00:59–01:02`: Tangan perakit memasang lengkungan bambu tipis di atas bingkai petak dan membentangkan jaring pelindung ringan menutupi seluruh kanopi padi.
  3. `01:02–01:05`: Burung pipit yang datang tertahan di luar jaring lalu terbang menjauh; bulir-bulir gabah keemasan tetap penuh utuh.
- **SFX:** Ketuk lengkung bambu (`wood-stake`), bentang jaring pelindung (`fabric-net`), suasana sore halaman (`yard-ambience`).
- **Narration:**
  Giliran bulir padi menguning, burung pipit turun mematuk gabah. Kamu pasang jaring pelindung melengkung di atas petak. Bulirnya utuh.
- **Captions (46 px, maks 2 baris):**
  `Giliran bulir padi menguning,` / `burung pipit turun mematuk gabah.` / `Kamu pasang jaring pelindung melengkung` / `di atas petak. Bulirnya utuh.`

---

## Scene 8 — Ronde 7: Nila Bersembunyi Saat Panen → Saluran Surut Pelan ke Caren (`01:05–01:14`, 21 kata)

- **Shot:** `close cutaway` saluran pembuangan bawah dan transisi ketinggian air dari *pelataran* padi turun menuju parit *caren*.
- **Sub-beats visual:**
  1. `01:05–01:08`: Menjelang panen, tangan mencoba menyerok ikan namun nila-nila besar menyelinap bersembunyi di sela pangkal rumpun padi yang rapat.
  2. `01:08–01:11`: Tangan perakit membuka sumbat/keran saluran surut di tepi bawah secara perlahan sehingga air di *pelataran* padi turun terkendali.
  3. `01:11–01:14`: Mengikuti surutnya air, kawanan ikan nila besar otomatis berkumpul rapi di dalam parit *caren* yang masih berair dalam sehingga mudah diserok tanpa menginjak rumpun padi.
- **SFX:** Klik buka keran/sumbat (`pvc-snap`), aliran air surut pelan (`water-drain`), kecipak serok nila (`water-splash`).
- **Narration:**
  Masalahnya, saat mau panen, nilanya bersembunyi di sela rumpun padi. Kamu buka saluran surut pelan, nila otomatis berkumpul di caren. Gampang diserok.
- **Captions (46 px, maks 2 baris):**
  `Masalahnya, saat mau panen, nilanya bersembunyi` / `di sela rumpun padi.` / `Kamu buka saluran surut pelan, nila otomatis` / `berkumpul di caren. Gampang diserok.`

---

## Scene 9 — Sistem Stabil (`01:14–01:22`, 18 kata)

- **Shot:** `wide` penuh pojok halaman menampilkan seluruh petak minapadi lengkap yang beroperasi mantap di bawah sinar cerah dan hujan singkat.
- **Sub-beats visual:**
  1. `01:14–01:18`: Cuaca bergeser dari hujan ringan ke cerah hangat; pipa pelimpah mengalirkan kelebihan hujan, *paranet* menaungi *caren*, dan jaring lengkung menjaga rumpun padi keemasan.
  2. `01:18–01:22`: Gelembung aerasi halus naik di air *caren* yang jernih, ikan nila ukuran konsumsi berenang lincah, dan seluruh bulir padi menguning lebat tanpa kimia.
- **SFX:** Rintik hujan singkat (`rain-shower`), aliran pelimpah (`water-drain`), gelembung halus (`water-bubbles`), tebar pelet (`pellet-scatter`).
- **Narration:**
  Sekarang, terik atau hujan, air jernih beroksigen, rumpun padi menguning lebat tanpa kimia, dan nila gemuk aktif di carennya.
- **Captions (46 px, maks 2 baris):**
  `Sekarang, terik atau hujan, air jernih beroksigen,` / `rumpun padi menguning lebat tanpa kimia,` / `dan nila gemuk aktif di carennya.`

---

## Scene 10 — Monetisasi: Panen Ganda Nila & Padi (`01:22–01:35`, 26 kata + tahan tag ≥3 dtk)

- **Shot:** `medium` di sisi depan petak minapadi jadi (petak minapadi dengan rumpun padi & *caren* tetap jelas terlihat di belakang sebagai landmark); keranjang ikan nila, timbangan gantung, dan bakul ikatan padi mengisi ≥40% lebar frame.
- **Sub-beats visual:**
  1. `01:22–01:26`: Tiga bulan berjalan; tangan perakit menyerok ikan nila besar dari *caren* masuk ke keranjang timbangan gantung di samping petak, sementara ikatan gabah/padi hasil sabit tersusun rapi di bakul sebelahnya.
  2. `01:26–01:29`: Jarum timbangan berayun mantap ke `15 kg`; pada kata *"lima belas kilo"*, tag harga kertas 400 px jatuh dari paku tiang timbangan (*drop* `0,2 s`, ayun redam `0,5 s`) menampilkan `15 kg × Rp34.000`.
  3. `01:29–01:35`: Pada *"lima ratus sepuluh ribu"*, chip kuning `≈ Rp510.000` muncul mekar (`0,15 s`) bersama catatan `estimasi harga pasar / Nov 2026`, lalu ditahan penuh `≥3,0 s` di 1x sementara bakul padi disorot hangat saat kalimat *"Padinya masuk dapur."*
- **SFX:** Kecipak panen (`water-splash`), rantai timbangan gantung (`scale-chain`), klik jatuh tag (`tag-click`), pop total kuning (`tag-pop`).
- **Narration:**
  Tiga bulan kemudian, nilanya kamu timbang sekitar lima belas kilo. Di pasar tiga puluh empat ribu per kilo, jadi sekitar lima ratus sepuluh ribu. Padinya masuk dapur.
- **Captions (46 px, maks 2 baris):**
  `Tiga bulan kemudian, nilanya kamu timbang` / `sekitar lima belas kilo.` / `Di pasar tiga puluh empat ribu per kilo,` / `jadi sekitar lima ratus sepuluh ribu. Padinya masuk dapur.`

---

## Scene 11 — Penutup Lebar & End Card (`01:35–01:46`, 24 kata + `0,625 dtk` *end card*)

- **Shot:** `wide` tarik mundur penuh menampilkan sudut halaman hidup dengan petak minapadi lengkap (padi menguning, *caren* ber-aerasi, *paranet*, pelimpah, jaring lengkung), keranjang ikan nila, dan bakul padi; ditutup *hard cut* ke *end card* identik thumbnail.
- **Sub-beats visual:**
  1. `01:35–01:41`: Kamera *pull-out* lembut memperlihatkan seluruh ekosistem minapadi beroperasi bersih di sudut halaman yang hidup (awan bergerak, pohon pisang bergoyang, rumah hangat di belakang).
  2. `01:41–01:45.4`: Pada kalimat tanya penutup, tiga kata berurutan **`bikin di halaman`** tetap menyala kuning `#FFD44D` sampai akhir kalimat sementara handle `@bikindihalaman.id` *fade in* kecil di bawah caption.
  3. `01:45.4–01:46.0` (`0,625 s` di 1x / `0,5 s` di 1,25x): *Hard cut* ke *end card* identik dengan thumbnail PNG (caption bersih, panel gelap atas di area aman 1080 × 1080 dengan judul **Bikin minapadi** / **di sudut halaman**).
- **SFX:** Suasana sore halaman lembut (`yard-ambience`), *whoosh* tarik kamera (`cam-whoosh`), hening bersih pada *end card*.
- **Narration:**
  Selamat, kamu sudah punya petak minapadi sendiri di halaman, panen padi sekaligus ikan nila. Habis ini, apa lagi yang mau kamu bikin di halaman?
- **Captions (46 px, maks 2 baris):**
  `Selamat, kamu sudah punya petak minapadi` / `sendiri di halaman, panen padi sekaligus ikan nila.` / `Habis ini, apa lagi yang mau kamu bikin di halaman?`
