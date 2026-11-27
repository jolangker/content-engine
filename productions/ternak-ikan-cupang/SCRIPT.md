# Bikin Tempat Ternak Ikan Cupang di Halaman

- **Script version:** v1
- **Board:** `budidaya-di-halaman` (Revision 10 — Editorial v9 / Visual v5)
- **Language & POV:** Bahasa Indonesia percakapan; `"kamu"` merujuk tunggal pada perakit/pemelihara di satu sudut halaman rumah yang sama.
- **Voice & Audio:** ElevenLabs **Roger** (`CwhRBWXzGAHq8TQ4Fs17`, `eleven_v4`, user-authorized `episode_override` pada 2026-11-27), BGM `none`, SFX organik berdasar event dari pustaka Visual v5 board (`boards/budidaya-di-halaman/assets/sfx/manifest.json`).
- **Duration & word budget (estimated pre-synthesis):** **242 kata lisan**. Pada kecepatan terukur Roger (`2,37 kata/dtk` dari `kolam-belut-dalam-drum`; fallback `2,40 kata/dtk`): prediksi narasi mentah `100,8–102,1 dtk`, prediksi komposisi 1x (termasuk jeda sunyi antar-adegan + tahan tag harga ≥3 dtk + `0,625 dtk` *end card*) **`105,6–106,9 dtk`** — masuk jendela kontrak `90,0–112,5 dtk` di 1x (**`84,5–85,5 dtk`** pada ekspor 1,25x / 30 fps). Akan direkonsiliasi dengan waktu terukur sesudah *take* tunggal disintesis.
- **Event map:** 18 kejadian utama (1 hook bangun awal + 7 ronde masalah–perbaikan [14 kejadian] + 1 uji stabil + 1 adegan hitung & kemas estimasi hasil + 1 penutup lebar & *end card*).

---

## On-screen copy (di luar caption ucapan)

- **Thumbnail & End Card (`0,625 dtk` di 1x / `0,5 dtk` di 1,25x):** Panel gelap di atas tampak lebar sudut ternak cupang jadi (dalam area aman 1080 × 1080 tengah, `y 420–1500`) dengan judul 2 baris 104 px DM Sans 900:
  - Baris 1: **Ternak cupang** (`Ternak` putih hangat `#FFF9E8`, **cupang** kuning `#FFD44D`)
  - Baris 2: **di sudut halaman** (putih hangat `#FFF9E8`)
- **Price tag (Adegan 10 — Hitung & Kemas Panen):** Tag kertas 400 px tergantung di paku tiang rak soliter (terjangkar di *world space*):
  - Baris 1 (38 px): `50 ekor × Rp10.000`
  - Chip total (54 px, latar kuning `#FFD44D`): `≈ Rp500.000`
  - Catatan (28 px, 2 baris): `estimasi grosir` / `Sep 2026`
- **Closing signature (akhir Adegan 11):** Tiga kata berurutan **bikin di halaman** tetap tersorot kuning (`#FFD44D`) sampai akhir kalimat; `@bikindihalaman.id` muncul halus (*fade in*) kecil di bawah caption tanpa menutupi sistem.

---

## Scene 1 — Bangun Awal Prematur & Langsung Saling Serang (`00:00–00:11`, 26 kata)

- **Shot:** `wide` sudut halaman tanah kosong dengan rumah, pagar kayu, dan pohon pisang bergoyang di latar 4-lapis 2.5D; *push-in* cepat ke dalam boks saat cupang bertarung.
- **Sub-beats visual:**
  1. `00:00–00:03` (`Frame 0` + gerak `0,25 dtk`): Sudut halaman tanah kosong; tangan perakit langsung menaruh boks plastik bening-biru di atas alas kayu (*micro-impact*).
  2. `00:03–00:07`: Selang/gayung menuang air jernih ke dalam boks, lalu sepasang ikan cupang (jantan merah-biru bersirip lebar dan betina pucat berbadan bulat) dilepas langsung bersamaan.
  3. `00:07–00:11`: Kamera *punch-in* ke potongan boks; tanpa jeda perkenalan, jantan langsung menerjang betina hingga cipratan kecil naik dan potongan sirip terlepas melayang.
- **SFX:** Hentakan boks (`wood-stake`), kucuran air (`water-pour`), kecipak lepas ikan (`water-splash`), *whoosh* kamera (`cam-whoosh`), kecipak serang (`water-splash`).
- **Narration:**
  Kalo kamu taruh boks di halaman, terus kamu isi air dan sepasang cupang, kamu sudah punya ternak cupang. Tapi baru sebentar, siripnya langsung robek saling serang.
- **Captions (46 px, maks 2 baris):**
  `Kalo kamu taruh boks di halaman,` / `terus kamu isi air dan sepasang cupang,` / `kamu sudah punya ternak cupang.` / `Tapi baru sebentar, siripnya langsung robek saling serang.`

---

## Scene 2 — Ronde 1: Teritorial → Sekat Bening & Daun Ketapang (`00:11–00:21`, 22 kata)

- **Shot:** `close cutaway` potongan dalam boks pemijahan (tepi boks dan dinding rumah tetap terlihat sebagai penanda).
- **Sub-beats visual:**
  1. `00:11–00:14`: Kedua ikan masih berhadapan agresif di air jernih tanpa pelindung.
  2. `00:14–00:17`: Tangan perakit menyelipkan sekat bening di tengah boks (*snap* + *micro-impact*) dan menjatuhkan daun ketapang kering; air berangsur berubah warna cokelat teh hangat yang menenangkan.
  3. `00:17–00:21`: Jantan tenang meniup sarang busa putih di bawah daun ketapang; sekat diangkat singkat saat telur menempel di busa, serokan mengangkat betina keluar, dan jantan tetap menjaga sarang busa.
- **SFX:** Klik sekat bening (`pvc-snap`), kecipak daun ketapang (`water-splash`), gelembung sarang busa (`water-bubbles`), ciduk serokan betina (`fabric-net`).
- **Narration:**
  Cupang sangat teritorial kalau belum kenal. Kamu pasang sekat bening dan daun ketapang. Setelah bertelur, kamu angkat betina, jantan jaga sarang busa.
- **Captions:**
  `Cupang sangat teritorial kalau belum kenal.` / `Kamu pasang sekat bening dan daun ketapang.` / `Setelah bertelur, kamu angkat betina, jantan jaga sarang busa.`

---

## Scene 3 — Ronde 2: Hujan Deras Rusak Sarang Busa → Atap Plastik & Paranet (`00:21–00:30`, 20 kata)

- **Shot:** `medium-wide` boks pemijahan terbuka di halaman saat awan gelap dan hujan deras turun (daun ketapang dan sarang busa tetap terlihat).
- **Sub-beats visual:**
  1. `00:21–00:24`: Langit menggelap dan rintik hujan deras menghantam permukaan boks terbuka; gelombang air dingin memecah sarang busa hingga buyar.
  2. `00:24–00:27`: Tiang kayu tertancap di sudut boks (*micro-impact*), lalu atap plastik bening miring dan jaring paranet peneduh dibentangkan di atas rangka (*tracking* lateral).
  3. `00:27–00:30`: Hujan mengalir turun melewati kemiringan atap plastik ke tanah di samping, sementara air boks di bawahnya tenang dan sarang busa utuh kembali.
- **SFX:** Derai hujan (`rain-shower`), hantaman tiang kayu (`wood-stake`), bentang plastik & paranet (`tarp-rustle` + `fabric-net`).
- **Narration:**
  Begitu hujan deras turun, air dingin merusak sarang busa. Kamu pasang atap plastik bening dan paranet. Sarang busanya tetap utuh.
- **Captions:**
  `Begitu hujan deras turun, air dingin merusak sarang busa.` / `Kamu pasang atap plastik bening dan paranet.` / `Sarang busanya tetap utuh.`

---

## Scene 4 — Ronde 3: Burayak Menetas Tak Bisa Makan Pelet → Pakan Mikro (`00:30–00:39`, 20 kata)

- **Shot:** `close cutaway` interior air kecokelatan di bawah sarang busa (tiang peneduh dan tepi boks sebagai penanda).
- **Sub-beats visual:**
  1. `00:30–00:33`: Cahaya pagi cerah; puluhan burayak mungil berenang bebas sementara butiran pelet biasa jatuh kebesaran ke dasar tanpa disentuh.
  2. `00:33–00:36`: Serokan halus mengangkat induk jantan keluar dengan lembut, lalu pipet meneteskan awan pakan mikro (infusoria/artemia) ke permukaan air.
  3. `00:36–00:39`: Burayak-burayak kecil langsung melesat menyambar titik-titik pakan mikro dengan lincah.
- **SFX:** Taburan pelet jatuh (`pellet-scatter`), ciduk angkat jantan (`water-splash`), tetesan pakan mikro (`water-pour`), riak lincah (`water-bubbles`).
- **Narration:**
  Empat hari jalan, burayak menetas dan pelet biasa terlalu besar. Kamu angkat jantannya, lalu teteskan pakan mikro. Burayaknya langsung menyambar.
- **Captions:**
  `Empat hari jalan, burayak menetas dan pelet biasa terlalu besar.` / `Kamu angkat jantannya, lalu teteskan pakan mikro.` / `Burayaknya langsung menyambar.`

---

## Scene 5 — Ronde 4: Wadah Sempit & Selang Sedot Burayak → Bak Besar & Selang Berkasa (`00:39–00:48`, 22 kata)

- **Shot:** `medium` sudut naungan paranet menampilkan boks pemijahan di kiri dan masuknya bak pembesaran besar di sebelah kanan.
- **Sub-beats visual:**
  1. `00:39–00:42`: Sebulan jalan, boks pemijahan penuh anakan remaja dengan endapan kotoran gelap di dasar; ujung selang polos sempat menarik seekor anakan mendekat bahaya.
  2. `00:42–00:45`: Bak pembesaran plastik besar diletakkan di samping boks di bawah kanopi yang sama (*micro-impact*), anakan dipindah, lalu selang tipis berujung kain kasa halus menyedot kotoran dasar keluar.
  3. `00:45–00:48`: Endapan kotoran mengalir keluar lewat selang sipon, anakan tertahan aman oleh kasa, dan air bak kembali jernih.
- **SFX:** Hentakan bak besar (`wood-stake`), kecipak pindah anakan (`water-splash`), klik ujung kasa selang (`pvc-snap`), sedotan sipon (`water-drain`).
- **Narration:**
  Sebulan kemudian, wadah sempit cepat kotor dan selang biasa menyedot burayak. Kamu pindah ke bak besar, kuras pakai selang berkasa. Airnya jernih.
- **Captions:**
  `Sebulan kemudian, wadah sempit cepat kotor` / `dan selang biasa menyedot burayak.` / `Kamu pindah ke bak besar, kuras pakai selang berkasa. Airnya jernih.`

---

## Scene 6 — Ronde 5: Bulan Kedua Jantan Saling Gigit → Rak Toples Soliter (`00:48–00:57`, 22 kata)

- **Shot:** `medium-wide` di bawah atap plastik/paranet (boks dan bak pembesaran di kiri, ruang rak soliter masuk di kanan).
- **Sub-beats visual:**
  1. `00:48–00:51`: Di dalam bak pembesaran, cupang-cupang jantan berwarna cerah mulai saling kejar dan menggigit ekor sesamanya.
  2. `00:51–00:54`: Rangka rak kayu dua tingkat dirakit di sisi kanan bawah kanopi (*micro-impact*), diisi deretan toples bening berair daun ketapang.
  3. `00:54–00:57`: Serokan kecil menyortir cupang jantan satu per satu masuk ke toples soliternya sendiri; sirip mereka bebas tanpa kejaran.
- **SFX:** Kecipak kejaran (`water-splash`), rakit rak kayu (`wood-stake`), susun toples (`pvc-snap`), serok sortir (`fabric-net` + `water-splash`).
- **Narration:**
  Masuk bulan kedua, cupang jantan mulai saling gigit sirip. Kamu rakit rak toples soliter, lalu sortir jantannya satu per satu. Semuanya aman.
- **Captions:**
  `Masuk bulan kedua, cupang jantan mulai saling gigit sirip.` / `Kamu rakit rak toples soliter,` / `lalu sortir jantannya satu per satu. Semuanya aman.`

---

## Scene 7 — Ronde 6: Terus Ngedok di Balik Toples Bening → Sekat Kardus (`00:57–01:06`, 20 kata)

- **Shot:** `close` tiga toples soliter bersebelahan di atas papan rak kayu (tiang kanopi dan bak pembesaran tetap tampak samar sebagai penanda).
- **Sub-beats visual:**
  1. `00:57–01:00`: Tiga cupang jantan di toples bening bersebelahan terus melebarkan insang (*flaring*/*ngedok*) menabrak dinding kaca sampai mulai terkulai lemas.
  2. `01:00–01:03`: Tangan perakit menyelipkan lembaran sekat kardus cokelat buram di celah antar-toples satu per satu (*snap* halus).
  3. `01:03–01:06`: Begitu pandangan terhalang, insang menutup santai dan para cupang berenang tenang dengan sirip terurai anggun.
- **SFX:** Kecipak menabrak kaca (`water-splash`), selip sekat kardus (`tarp-rustle` + `tag-click`), *whoosh* halus (`cam-whoosh`).
- **Narration:**
  Masalahnya, dari balik toples bening, mereka terus ngedok sampai lemas. Kamu selipkan sekat kardus di antara toples. Mereka kembali tenang.
- **Captions:**
  `Masalahnya, dari balik toples bening,` / `mereka terus ngedok sampai lemas.` / `Kamu selipkan sekat kardus di antara toples. Mereka kembali tenang.`

---

## Scene 8 — Ronde 7: Cupang Lompat Keluar → Kurangi Air & Tutup Jaring (`01:06–01:15`, 20 kata)

- **Shot:** `medium` rak toples soliter saat pagi cerah (sekat kardus antar-toples tetap terpasang).
- **Sub-beats visual:**
  1. `01:06–01:09`: Pagi hari, air toples penuh sampai leher dan seekor cupang terlihat jatuh menggelepar di tepi papan rak di luar toples terbuka.
  2. `01:09–01:12`: Ikan segera dikembalikan, permukaan air tiap toples diturunkan beberapa senti memberi ruang aman, lalu tutup jaring berpori dipasang rapi di atas tiap toples (*micro-impact*).
  3. `01:12–01:15`: Transisi malam ke pagi berikutnya; seekor cupang melompat naik, tertahan lembut oleh jaring, jatuh balik ke air, dan keesokan paginya semua toples utuh terisi.
- **SFX:** Kecipak lompat (`water-splash`), tuang kurangi air (`water-drain`), pasang tutup jaring (`fabric-net` + `pvc-snap`).
- **Narration:**
  Suatu pagi, ada cupang lompat keluar dari toples terbuka. Kamu kurangi sedikit airnya dan pasang tutup jaring. Besoknya semua utuh.
- **Captions:**
  `Suatu pagi, ada cupang lompat keluar dari toples terbuka.` / `Kamu kurangi sedikit airnya dan pasang tutup jaring.` / `Besoknya semua utuh.`

---

## Scene 9 — Sistem Stabil: Uji Hujan & Pakan Lengkap (`01:15–01:24`, 20 kata)

- **Shot:** `wide` sudut halaman penuh di bawah hujan sore menampilkan seluruh sistem terpasang utuh (atap plastik + paranet, boks pemijahan, bak pembesaran ber-sipon, dan rak soliter bersekat kardus + tutup jaring).
- **Sub-beats visual:**
  1. `01:15–01:19`: Hujan sore turun lagi; aliran air meluncur aman di atas atap plastik bening tanpa mengenai boks, bak pembesaran tetap jernih di bawah paranet, tutup jaring dan sekat kardus terjaga rapi.
  2. `01:19–01:24`: Perakit membuka sedikit tutup jaring menaburkan pakan; seluruh cupang warna-warni di rak dan bak pembesaran langsung menyambar aktif.
- **SFX:** Derai hujan sore (`rain-shower`), tabur pakan (`pellet-scatter`), kecipak makan lincah (`water-splash`).
- **Narration:**
  Saat hujan turun lagi, atap menahan air, bak pembesaran tetap bersih, dan semua cupang di rak menyambar pakan. Sistemnya stabil.
- **Captions:**
  `Saat hujan turun lagi, atap menahan air,` / `bak pembesaran tetap bersih,` / `dan semua cupang di rak menyambar pakan. Sistemnya stabil.`

---

## Scene 10 — Monetisasi: Hitung & Kemas Panen Pertama (`01:24–01:36`, 26 kata)

- **Shot:** `medium` di samping rak soliter dan bak pembesaran yang sudah jadi (rak lengkap dengan atap, sekat kardus, dan tutup jaring tetap menjadi penanda; interaksi nampan kemasan kantong cupang + paku tag mengisi ≥40% lebar layar; tag terjangkar di *world space*).
- **Sub-beats visual:**
  1. `01:24–01:28`: Tangan perakit menyusun kantong-kantong plastik bening berisi cupang warna-warni siap jual berjejer rapi ke dalam nampan panen di samping rak soliter (*micro-impact*).
  2. `01:28–01:30`: Pada kata `"lima puluh"`, tag kertas 400 px jatuh (`0,2 dtk`, ayunan reda `0,5 dtk`) di paku tiang rak; `50 ekor` muncul (`0,15 dtk`).
  3. `01:30–01:33`: Pada `"sepuluh"`, `× Rp10.000` muncul (`0,15 dtk`); pada `"lima ratus"`, chip kuning `≈ Rp500.000` dan catatan `estimasi grosir / Sep 2026` muncul saat tag memanjang ke bawah.
  4. `01:33–01:36`: Tag lengkap bertahan penuh (`≥3,0 dtk` di 1x) sementara cupang-cupang berkilau di kantong kemasan.
- **SFX:** Kecipak serok kemas (`water-splash`), plastik kemasan (`tarp-rustle`), klik kertas tag (`tag-click`), tick harga satuan (`tag-click`), pop total kuning (`tag-pop`).
- **Narration:**
  Tiga bulan kemudian, panen pertama kamu hitung dan kemas. Kira-kira lima puluh ekor. Di grosir sekitar sepuluh ribuan per ekor, jadi kurang lebih lima ratus ribuan.
- **Captions:**
  `Tiga bulan kemudian, panen pertama kamu hitung dan kemas.` / `Kira-kira lima puluh ekor. Di grosir sekitar` / `sepuluh ribuan per ekor, jadi kurang lebih lima ratus ribuan.`

---

## Scene 11 — Penutup Lebar & End Card (`01:36–01:47`, 24 kata + `0,625 dtk` end card)

- **Shot:** `wide` tarik perlahan (*living drift*) ke tampak penuh sudut halaman sore hangat memperlihatkan seluruh sistem lengkap (boks pemijahan, bak pembesaran, rak toples soliter bersekat kardus + tutup jaring, atap plastik + paranet, nampan kemasan panen di depan); diakhiri *hard cut* ke *end card* thumbnail.
- **Sub-beats visual:**
  1. `01:36–01:41`: Tampak lebar sudut halaman sore hangat dengan cahaya jendela rumah menyala, kunang-kunang lembut, pohon pisang bergoyang, dan seluruh sistem ternak cupang berdiri rapi.
  2. `01:41–01:46`: Pada kalimat tanya penutup, tiga kata berurutan **bikin di halaman** tetap tersorot kuning (`#FFD44D`) sampai akhir kalimat, dan `@bikindihalaman.id` *fade in* halus di bawah caption.
  3. `01:46–01:46,625`: *Hard cut* ke *end card* (`0,625 dtk` di 1x = `0,5 dtk` di 1,25x) identik dengan thumbnail **Ternak cupang / di sudut halaman** (caption bersih).
- **SFX:** Suasana sore halaman sangat pelan (`yard-ambience`, tanpa BGM), hening bersih pada *end card*.
- **Narration:**
  Selamat, kamu sudah punya tempat ternak cupang sendiri di halaman, lengkap sampai rak soliter. Habis ini, apa lagi yang mau kamu bikin di halaman?
- **Captions:**
  `Selamat, kamu sudah punya tempat ternak cupang sendiri di halaman,` / `lengkap sampai rak soliter.` / `Habis ini, apa lagi yang mau kamu bikin di halaman?` *(kuning tertahan di **bikin di halaman** + `@bikindihalaman.id` fade in di bawah)*
