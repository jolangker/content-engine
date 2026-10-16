---
version: alpha
name: Berkas Polemik — Frame (video / frame layer)
description: >
  Spesifikasi desain frame-scale untuk seri video edukasi sejarah polemik Indonesia "Berkas Polemik".
  Unit utama adalah vertikal 9:16 (1080×1920). Mengusung bahasa visual Forensic Dossier / Meja Investigasi
  dengan kontras tinggi: latar arsip karbon gelap, lembaran berkas manila otentik, cap bukti merah menyala,
  dan tipografi hibrida (Space Grotesk + Space Mono + Newsreader).
unit: the frame — 1080×1920 (9:16 vertical shortform) primary
principle: data arsip memimpin · kontras tajam tanpa dekorasi hampa · bukti sebelum kesimpulan

colors:
  bg: "#121110"        # Karbon arsip gelap (latar utama video)
  paper: "#EAE0D0"     # Kertas berkas manila / dokumen tua
  ink: "#1A1816"       # Tinta hitam arsip pada lembar kertas
  red: "#C32822"       # Merah stempel rahasia / aksen anomali
  steel: "#7C756B"     # Abu-abu baja / garis ukur / metadata netral
  tape: "#D4A359"      # Kuning map kusam / penanda highlight bukti
  surface: "#1D1B19"   # Panel kartu sekunder gelap

typography:
  display-hero:
    fontFamily: "Space Grotesk"
    weight: 700
    letterSpacing: "-0.03em"
    lineHeight: 1.05
    color: "paper"
  display-quote:
    fontFamily: "Newsreader"
    weight: 400
    fontStyle: "italic"
    letterSpacing: "-0.02em"
    lineHeight: 1.2
    color: "paper"
  mono-header:
    fontFamily: "Space Mono"
    weight: 700
    letterSpacing: "0.14em"
    textTransform: "uppercase"
    color: "red"
  mono-data:
    fontFamily: "Space Mono"
    weight: 400
    letterSpacing: "0.04em"
    lineHeight: 1.4
    color: "steel"
  body-sans:
    fontFamily: "Space Grotesk"
    weight: 500
    lineHeight: 1.4
    color: "paper"

spacing:
  safe-zone-top: "140px"      # Menghindari UI platform (TikTok/Reels)
  safe-zone-bottom: "280px"   # Menghindari caption & tombol action
  pad-edge: "54px"
  gap-block: "32px"

components:
  dossier-card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    border: "1px solid rgba(26,24,22,0.18)"
    borderRadius: "0px"
    padding: "36px"
    description: "Kartu dokumen primer fisik di atas kanvas gelap; tepi tajam tanpa lengkungan."
  stamp-badge:
    border: "2.5px solid {colors.red}"
    textColor: "{colors.red}"
    font: "{typography.mono-header}"
    padding: "6px 14px"
    transform: "rotate(-2.5deg)"
    description: "Stempel status bukti (e.g. RAHASIA, DIVERIFIKASI, DISKREDITKAN, VERSI ANRI)."
  redacted-bar:
    backgroundColor: "{colors.red}"
    textColor: "{colors.paper}"
    padding: "2px 8px"
    description: "Batang sensor yang merepresentasikan informasi yang pernah ditutup atau dipalsukan."
  evidence-split:
    layout: "Dua kartu berkas berdampingan atau bertumpuk vertikal dengan label VERSI A vs VERSI B"
    divider: "1px dashed {colors.steel}"
    description: "Modul komparasi langsung dua klaim sejarah atau dua dokumen yang bertolak belakang."
---

# Berkas Polemik — Design Intent & Rules

## 1. Overview & Brand Intent

*Berkas Polemik* memposisikan penonton sebagai penyelidik sejarah yang sedang duduk di depan meja berkas deklasifikasi. Desain visual tidak boleh terlihat seperti materi kuliah sekolah yang kaku atau infografis korporat yang steril. Setiap elemen grafis—garis kisi, nomor arsip, stempel miring, dan potongan naskah—harus berfungsi sebagai **instrumen forensik bukti**.

## 2. Aturan Tipografi & Skala

1. **Space Grotesk** memimpin saat menyampaikan *urgensi, hook masalah, dan pertentangan argumen*. Karakternya yang lugas dan sedikit brutalist memberi kesan berani dan modern.
2. **Space Mono** selalu digunakan untuk *metadata otentik*: nomor kearsipan, tanggal telegram, pasal konstitusi, kode lembaga (`KEMLU-1946`, `ANRI-1966`, `CIA-RDP90`). Ini menciptakan ilusi "membaca berkas asli".
3. **Newsreader** adalah suara saksi dan suara sejarah masa lalu. Setiap kali ada kutipan lisan dari Sukarno, Hatta, Sjahrir, saksi mata, atau potongan koran lama, gunakan Newsreader italic agar terasa memiliki martabat waktu dan humanisme.

## 3. Aturan Warna & Kontras

- **Latar belakang gelap (`#121110`)** adalah ruang kerja/arsip. Ini mengarahkan 100% fokus mata ke dokumen manila (`#EAE0D0`) yang sedang disorot lampu meja.
- **Merah stempel (`#C32822`)** dipakai secara hemat dan bernilai tinggi: hanya untuk kata kunci paling kontroversial, stempel verifikasi, atau garis penanda kontradiksi fatal.
- Dilarang menggunakan warna neon, gradien holografik, atau ilustrasi kartun santai.

## 4. Hirarki Komposisi Short-form (9:16)

- **Top Safe Zone (0–140px):** Bersih dari teks kunci; hanya diisi header seri minimalis.
- **Eye-level Hook Zone (180–850px):** Tempat judul utama, dokumen kontroversial yang dipaparkan, dan stempel visual.
- **Evidence Comparison Zone (850–1450px):** Kartu berkas dokumen, perbandingan teks silang A vs B, dan garis kronologi.
- **Bottom Safe Zone (1450–1920px):** Dikosongkan dari informasi esensial agar tidak tertutup deskripsi, suara, dan antarmuka TikTok/Reels.

## 5. Kosakata Gerak (Motion Guidance)

- **Tanpa bouncy / spring berlebihan:** Gerak elemen berkas harus terasa memiliki berat kertas dan logam (easing `power2.out` atau `power3.out`).
- **Punch-in Terukur:** Kamera bergerak mendekat secara tajam ke tanggal dokumen atau tanda tangan janggal saat narator menyebut keanehan tersebut.
- **Redaction Sweep:** Batang sensor tersapu ke samping dengan kecepatan tinggi (0.2s) tepat pada ketukan suara pengungkapan fakta.
