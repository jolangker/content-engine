# Bikin Rumah Burung Walet Mini di Halaman

- **Script version:** v1
- **Board:** `budidaya-di-halaman` (Revision 10 — Editorial v9 / Visual v5)
- **Language & POV:** Bahasa Indonesia percakapan; `"kamu"` merujuk tunggal pada pembuat dan pengelola rumah walet mini di satu sudut halaman yang sama.
- **Voice & Audio:** ElevenLabs board default **Pribs – Friendly Casual Narration** (`5g0yKK2JwTRka0IG61Hh`, `eleven_v4`, resolved via `boards/budidaya-di-halaman/AUDIO.json`; Starter API key confirmed access in `my voices`), BGM `none`, SFX organik berdasar event dari pustaka Visual v5 board (`boards/budidaya-di-halaman/assets/sfx/manifest.json`).
- **Duration & word budget (estimasi pra-sintesis):** **240 kata lisan** (`25 + 21 + 21 + 21 + 22 + 20 + 21 + 22 + 18 + 26 + 23`). Pada laju terukur Pribs di preview board (`2,57 kata/dtk`) sampai laju cadangan (`2,40 kata/dtk`), narasi mentah diprediksi `93,4–100,0 dtk` dan total komposisi 1x `~99,5–106,2 dtk` (termasuk jeda antaradegan, tahan tag `>= 3,0 dtk`, dan *end card* `0,625 dtk`), masuk di tengah jendela kontrak `90,0–112,5 dtk` (`79,6–85,0 dtk` pada rilis `1,25x`). Akan direkonsiliasi tepat dengan audio terukur setelah sintesis.
- **Event map:** 18 kejadian utama (1 hook bangun awal + 7 ronde masalah–perbaikan [14 kejadian] + 1 uji stabil + 1 adegan timbang panen perdana + 1 penutup lebar & *end card*).

---

## On-screen copy (di luar caption ucapan)

- **Thumbnail & End Card (`0,625 dtk` di 1x / `0,5 dtk` di 1,25x):** Panel gelap di atas tampak lebar rumah burung walet mini jadi (dalam area aman 1080 × 1080 tengah, `y 420–1500`) dengan judul 2 baris 104 px DM Sans 900:
  - Baris 1: **Bikin rumah** (putih hangat `#FFF9E8`)
  - Baris 2: **walet mini** (kuning `#FFD44D`)
- **Price tag (Adegan 10 — Timbang Panen Perdana `100 g`):** Tag kertas 400 px tergantung tali pada paku palang timbangan gantung di samping rumah walet mini jadi (terjangkar di *world space*):
  - Baris 1 (38 px): `100 g × Rp8.310`
  - Chip total (48 px, latar kuning `#FFD44D`): `≈ Rp831.000`
  - Catatan (28 px, 2 baris): `estimasi harga pengepul` / `Agu 2026`
- **Closing signature (akhir Adegan 11):** Tiga kata berurutan **bikin di halaman** tetap tersorot kuning (`#FFD44D`) sampai akhir kalimat; `@bikindihalaman.id` muncul halus (*fade in*) kecil di bawah caption tanpa menutupi rumah walet mini.

---

## Scene 1 — Bangun Awal Prematur & Burung Cuma Mampir Lalu Kabur (`00:00–00:10`, 25 kata)

- **Shot:** `wide` sudut halaman tanah hangat kosong dengan rumah tetangga, pagar kayu, dan pohon pisang bergoyang di latar 4-lapis 2.5D; *punch-in* ke lubang masuk atas dan ruang dalam yang silau.
- **Sub-beats visual:**
  1. `00:00–00:03` (`Frame 0` + gerak `0,25 dtk`): Sudut halaman kosong dengan tumpukan bata abu-abu, papan kayu polos, dan pemutar suara panggil siap; tangan langsung menyusun dinding bata kotak dua tingkat dengan lubang masuk atas (LMB) terbuka dan atap polos.
  2. `00:03–00:07`: Pemutar suara panggil dipasang di bibir lubang atas dan memancarkan gelombang bunyi lembut; beberapa burung walet menyambar turun dari langit sore masuk melewati lubang atas.
  3. `00:07–00:10`: Kamera *push-in* ke potongan dalam bangunan — berkas sinar matahari menyorot lurus membanjiri ruang polos; walet cuma berputar satu kali di tengah ruang terang lalu langsung melesat keluar lagi.
- **SFX:** Ketukan susun bata (`wood-stake`), klik pasang pemutar suara (`pvc-snap`), *whoosh* sapuan burung & *push-in* (`cam-whoosh`), suasana halaman sore (`yard-ambience`).
- **Narration:**
  Kalo kamu susun dinding bata berlubang di halaman, setelah itu kamu putar suara panggil, kamu sudah punya rumah walet. Tapi burungnya cuma mampir lalu kabur.
- **Captions (46 px, maks 2 baris):**
  `Kalo kamu susun dinding bata berlubang di halaman,` / `setelah itu kamu putar suara panggil,` / `kamu sudah punya rumah walet.` / `Tapi burungnya cuma mampir lalu kabur.`

---

## Scene 2 — Ronde 1: Ruang Terlalu Terang → Sekat Gelap Pembatas (`00:10–00:19`, 21 kata)

- **Shot:** `close cutaway` potongan dalam bagian atas-tengah rumah walet mini memperlihatkan lubang masuk (*void*) dan ruang inap di belakangnya.
- **Sub-beats visual:**
  1. `00:10–00:13`: Berkas cahaya kuning terang menembus lurus dari lubang masuk menyinari seluruh ruang dalam; walet melesat berbalik menghindari ruang silau.
  2. `00:13–00:16`: Tangan perakit memasang dinding sekat gelap pembatas (*sekat lar*) antara ruang putar depan dan ruang inap belakang dengan bukaan bawah untuk jalur masuk burung.
  3. `00:16–00:19`: Cahaya matahari berhenti di ruang putar depan; ruang inap belakang berubah teduh gelap khas gua dan walet menukik masuk lalu bertahan di dalam.
- **SFX:** Ketukan pasang papan sekat (`wood-stake`), klik klem/siku pengikat (`pvc-snap`), *whoosh* gerak kamera (`cam-whoosh`).
- **Narration:**
  Cahaya matahari masuk lurus bikin ruang terlalu terang. Kamu pasang sekat gelap pembatas di dalam. Ruang inap jadi gelap, walet bertahan.
- **Captions (46 px, maks 2 baris):**
  `Cahaya matahari masuk lurus bikin ruang terlalu terang.` / `Kamu pasang sekat gelap pembatas di dalam.` / `Ruang inap jadi gelap, walet bertahan.`

---

## Scene 3 — Ronde 2: Suhu Siang Melewati 30 °C → Pipa Ventilasi Siku ke Bawah (`00:19–00:28`, 21 kata)

- **Shot:** `medium-wide` tampak samping potongan rumah walet mini di bawah terik matahari siang (sekat gelap dan lubang masuk tetap tampak sebagai penanda).
- **Sub-beats visual:**
  1. `00:19–00:22`: Matahari siang terik memanggang atap; garis gelombang panas oranye terperangkap di ruang atas (> 30 °C) sehingga walet terbang keluar lewat lubang masuk.
  2. `00:22–00:25`: Tangan perakit memasang deretan pipa PVC ventilasi berbentuk siku L menghadap bawah di dinding samping (berkasa halus di ujung luar).
  3. `00:25–00:28`: Panah udara panas mengalir keluar sementara sinar matahari tertahan lekukan siku; warna panas ruang atas mereda menjadi sejuk nyaman dan walet kembali masuk.
- **SFX:** Klik pasang pipa PVC siku (`pvc-snap`), ketukan rangka (`wood-stake`), *whoosh* hembusan udara (`cam-whoosh`).
- **Narration:**
  Pas tengah hari, suhunya naik di atas tiga puluh derajat. Kamu pasang pipa ventilasi siku ke bawah. Panas keluar, ruangan adem.
- **Captions (46 px, maks 2 baris):**
  `Pas tengah hari, suhunya naik` / `di atas tiga puluh derajat.` / `Kamu pasang pipa ventilasi siku ke bawah.` / `Panas keluar, ruangan adem.`

---

## Scene 4 — Ronde 3: Udara Kering Bikin Liur Rapuh → Bak Air Dangkal di Lantai (`00:28–00:37`, 21 kata)

- **Shot:** `medium` potongan lantai dasar dan dinding bawah ruang inap (pipa ventilasi siku dan sekat gelap tetap terlihat di atas).
- **Sub-beats visual:**
  1. `00:28–00:31`: Transisi seminggu; udara kering ditandai partikel kering keemasan, membuat polesan liur putih tipis pertama di plafon retak kering dan mengelupas jatuh.
  2. `00:31–00:34`: Tangan perakit membuat dinding tepi bak dangkal di lantai bawah lalu menuangkan air jernih dari selang sampai permukaan kolam terisi rata.
  3. `00:34–00:37`: Aliran udara dari pipa ventilasi menyapu permukaan bak, mengangkat pita uap lembap lembut ke atas; ruang inap berubah sejuk lembap dan walet tenang di atas.
- **SFX:** Susun tepi bak (`dig-soil`), kucur air mengisi bak (`water-pour`), percik halus (`water-splash`).
- **Narration:**
  Seminggu jalan, udara kering bikin sarang liurnya rapuh dan terlepas. Kamu buat bak air dangkal di lantai. Uapnya melembapkan ruang inap.
- **Captions (46 px, maks 2 baris):**
  `Seminggu jalan, udara kering bikin sarang` / `liurnya rapuh dan terlepas.` / `Kamu buat bak air dangkal di lantai.` / `Uapnya melembapkan ruang inap.`

---

## Scene 5 — Ronde 4: Plafon Licin Kuku Terpeleset → Papan Sirip Kayu Beralur Kasar (`00:37–00:46`, 22 kata)

- **Shot:** `close cutaway` sudut langit-langit ruang inap (sekat gelap di kiri dan uap bak air tipis di bawah tetap tampak sebagai penanda).
- **Sub-beats visual:**
  1. `00:37–00:40`: Walet mendekati balok plafon licin mengilap; cakar melengkungnya terpeleset beberapa kali sehingga gagal bertengger lama.
  2. `00:40–00:43`: Tangan perakit memasang jajaran papan sirip kayu meranti kering dengan alur garis kasar melintang di langit-langit ruang inap.
  3. `00:43–00:46`: Kuku walet langsung mengait kokoh pada alur kasar kayu sirip; beberapa ekor bertengger rapi berdampingan di deretan sirip.
- **SFX:** Ketukan pasang papan sirip (`wood-stake`), klik sekrup/penjepit (`pvc-snap`), *whoosh* sapuan sayap (`cam-whoosh`).
- **Narration:**
  Giliran walet hinggap, kukunya terus terpeleset di papan plafon yang licin. Kamu ganti dengan papan sirip kayu beralur kasar. Cengkeramannya kuat menempel.
- **Captions (46 px, maks 2 baris):**
  `Giliran walet hinggap, kukunya terus terpeleset` / `di papan plafon yang licin.` / `Kamu ganti dengan papan sirip kayu beralur kasar.` / `Cengkeramannya kuat menempel.`

---

## Scene 6 — Ronde 5: Suara Panggil Terlalu Keras → Suara Inap Pelan di Papan Sirip (`00:46–00:55`, 20 kata)

- **Shot:** `medium` potongan keseluruhan ruang inap dan ruang putar (papan sirip beralur, sekat gelap, pipa siku, dan bak air tetap tampak).
- **Sub-beats visual:**
  1. `00:46–00:49`: Gelombang suara merah-oranye keras memantul dari lubang atas masuk ke ruang sempit; walet hanya berputar-putar gelisah menyambar udara tanpa hinggap.
  2. `00:49–00:52`: Tangan perakit memasang unit kecil pemutar suara inap pelan menempel di sudut papan sirip bagian dalam sambil meredam gelombang keras dari luar.
  3. `00:52–00:55`: Riak gelombang suara pelan hangat menyebar lembut di sepanjang sirip; burung-burung berhenti berputar, bertengger tenang, dan mulai membentuk mangkok sarang putih.
- **SFX:** Klik pasang tweeter inap (`pvc-snap`), ketukan pelan (`wood-stake`), *whoosh* halus (`cam-whoosh`).
- **Narration:**
  Masalahnya, suara panggil keras bikin walet cuma berputar gelisah. Kamu pasang suara inap pelan di papan sirip. Mereka tenang bersarang.
- **Captions (46 px, maks 2 baris):**
  `Masalahnya, suara panggil keras bikin walet` / `cuma berputar gelisah.` / `Kamu pasang suara inap pelan di papan sirip.` / `Mereka tenang bersarang.`

---

## Scene 7 — Ronde 6: Tokek Merayap ke Lubang Masuk → Bingkai Seng Licin Keliling Lubang (`00:55–01:04`, 21 kata)

- **Shot:** `medium-wide` tampak luar-potongan bagian atas dinding rumah walet mini saat malam (lubang masuk, pipa ventilasi siku, dan sarang dalam tetap tampak).
- **Sub-beats visual:**
  1. `00:55–00:58`: Suasana malam dengan lampu rumah tetangga menyala hangat; siluet tokek bertutul merayap naik di tembok bata kasar mendekati bibir lubang masuk menuju sarang bertelur di dalam.
  2. `00:58–01:01`: Tangan perakit memasang bingkai pelat seng lebar mengilap licin mengelilingi bingkai lubang masuk bagian luar.
  3. `01:01–01:04`: Tokek kembali mencoba merayap naik, kakinya terpeleset jatuh dari permukaan seng licin lalu pergi; sarang bertelur di papan sirip dalam tetap aman.
- **SFX:** Gemerisik pelat/lembar pelindung (`tarp-rustle`), ketukan paku klem (`wood-stake`), suasana malam halaman (`yard-ambience`).
- **Narration:**
  Masuk bulan ketiga, tokek merayap ke lubang masuk mengincar telur. Kamu pasang bingkai seng licin di sekeliling lubang. Tokek terpeleset turun.
- **Captions (46 px, maks 2 baris):**
  `Masuk bulan ketiga, tokek merayap` / `ke lubang masuk mengincar telur.` / `Kamu pasang bingkai seng licin di sekeliling lubang.` / `Tokek terpeleset turun.`

---

## Scene 8 — Ronde 7: Panen Sarang Bertelur Bikin Kabur → Tunggu Anakan Terbang & Panen Siang (`01:04–01:13`, 22 kata)

- **Shot:** `close cutaway` dua sarang putih bersebelahan di papan sirip beralur (tweeter inap dan sekat gelap tetap tampak sebagai penanda).
- **Sub-beats visual:**
  1. `01:04–01:07`: Potongan dekat dua sarang mangkok putih — sarang kiri berisi dua telur mungil dan tanda silang/tangan menarik mundur karena gangguan membuat kawanan walet terbang panik keluar.
  2. `01:07–01:10`: Waktu bergulir tenang: anakan walet tumbuh, mengepak sayap terbang keluar dari sarang kanan; saat siang hari ruang sepi (induk mencari makan), tangan memanen hanya sarang kanan yang sudah kosong memakai sendok kape baja bersih.
  3. `01:10–01:13`: Langit beralih sore; induk walet pulang tenang lewat lubang masuk dan langsung bertengger nyaman kembali di papan sirip.
- **SFX:** *Whoosh* kepakan anakan terbang (`cam-whoosh`), klik rapi kape melepas sarang (`tag-click`), suasana sore (`yard-ambience`).
- **Narration:**
  Begitu sarang jadi, ambil sarang bertelur bikin koloni kabur. Kamu tunggu anakan terbang, lalu panen sarang kosong siang hari. Induknya tetap pulang.
- **Captions (46 px, maks 2 baris):**
  `Begitu sarang jadi, ambil sarang bertelur` / `bikin koloni kabur.` / `Kamu tunggu anakan terbang, lalu panen sarang` / `kosong siang hari. Induknya tetap pulang.`

---

## Scene 9 — Sistem Stabil (`01:13–01:21`, 18 kata)

- **Shot:** `wide` penuh sudut halaman menampilkan seluruh potongan hidup rumah walet mini yang telah dilengkapi ketujuh perbaikan.
- **Sub-beats visual:**
  1. `01:13–01:17`: Cahaya bergeser dari siang terik ke sore keemasan; pipa siku membuang panas, bak lantai menjaga kabut uap lembap, sekat gelap melindungi ruang inap, dan bingkai seng menjaga lubang masuk.
  2. `01:17–01:21`: Sekelompok kecil walet meluncur tenang masuk lubang atas melewati sekat menuju jajaran papan sirip beralur yang penuh sarang mangkok putih rapi.
- **SFX:** Suasana halaman sore lembut (`yard-ambience`), *whoosh* gerakan kawanan walet (`cam-whoosh`), gemericik uap halus (`water-bubbles`).
- **Narration:**
  Sekarang, mau siang terik atau malam, ruangnya gelap, sejuk, lembap, aman dari tokek, dan koloni walet bersarang stabil.
- **Captions (46 px, maks 2 baris):**
  `Sekarang, mau siang terik atau malam,` / `ruangnya gelap, sejuk, lembap,` / `aman dari tokek, dan koloni walet bersarang stabil.`

---

## Scene 10 — Monetisasi: Timbang Panen Perdana 100 Gram (`01:21–01:35`, 26 kata + tahan tag ≥ 3 dtk)

- **Shot:** `medium` di sisi depan rumah walet mini jadi (bangunan rumah walet dengan bingkai seng dan pipa siku tetap jelas sebagai penanda di belakang; timbangan gantung berkeranjang sarang walet mengisi ≥ 40% lebar frame).
- **Sub-beats visual:**
  1. `01:21–01:25`: Setahun lebih berjalan; tangan perakit meletakkan kepingan terakhir dari sekitar 13 sarang mangkok putih bersih kering ke dalam mangkok/wadah timbangan gantung di samping rumah walet hingga jarum menunjuk 100 g.
  2. `01:25–01:28`: Pada kata *"seratus gram"*, tag harga kertas 400 px turun (`0,2 s`, ayunan reda `0,5 s`) di paku palang timbangan menampilkan `100 g × Rp8.310`.
  3. `01:28–01:35`: Pada *"delapan ratus tiga puluh ribu"*, chip kuning `≈ Rp831.000` mekar (`0,15 s`) bersama catatan `estimasi harga pengepul / Agu 2026`, lalu ditahan penuh `>= 3,0 s` di 1x.
- **SFX:** Gemerincing rantai timbangan (`scale-chain`), klik jatuh tag (`tag-click`), pop chip total kuning (`tag-pop`).
- **Narration:**
  Setahun jalan, panen perdana kira-kira seratus gram sarang mangkok. Di pengepul sekitar delapan ribu tiga ratus per gram, jadi kurang lebih delapan ratus tiga puluh ribu.
- **Captions (46 px, maks 2 baris):**
  `Setahun jalan, panen perdana kira-kira` / `seratus gram sarang mangkok.` / `Di pengepul sekitar delapan ribu tiga ratus per gram,` / `jadi kurang lebih delapan ratus tiga puluh ribu.`

---

## Scene 11 — Penutup Lebar & End Card (`01:35–01:45`, 23 kata + `0,625 dtk` *end card*)

- **Shot:** `wide` tarik mundur penuh menampilkan sudut halaman hidup dengan rumah walet mini lengkap dan keranjang sarang panen di sampingnya; diakhiri *hard cut* ke *end card* identik thumbnail.
- **Sub-beats visual:**
  1. `01:35–01:40`: Kamera *pull-out* lembut memperlihatkan rumah walet mini lengkap beroperasi (dinding bata, bingkai seng LMB, kawanan walet pulang sore, pipa ventilasi siku, sekat gelap, bak air, papan sirip beralur, suara inap, dan wadah sarang panen).
  2. `01:40–01:44.4`: Pada kalimat tanya penutup, kata berurutan **`bikin di halaman`** tetap menyala kuning `#FFD44D` sampai akhir kalimat sementara handle `@bikindihalaman.id` *fade in* kecil di bawah caption.
  3. `01:44.4–01:45.0` (`0,625 s` di 1x / `0,5 s` di 1,25x): *Hard cut* ke *end card* identik dengan thumbnail PNG (caption bersih, panel gelap atas di area aman 1080 × 1080 dengan judul **Bikin rumah** / **walet mini**).
- **SFX:** Suasana sore halaman lembut (`yard-ambience`), *whoosh* tarik kamera (`cam-whoosh`), hening bersih pada *end card*.
- **Narration:**
  Selamat, kamu sudah punya rumah walet mini sendiri, lengkap sampai panen sarang pertama. Habis ini, apa lagi yang mau kamu bikin di halaman?
- **Captions (46 px, maks 2 baris):**
  `Selamat, kamu sudah punya rumah walet mini` / `sendiri, lengkap sampai panen sarang pertama.` / `Habis ini, apa lagi yang mau kamu bikin di halaman?`
