---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "Buku sejarah mencatat kerja rodi tanpa upah; namun arsip 1808 membuktikan Daendels mengalokasikan 30.000 ringgit perak yang diduga mengendap di tangan elite bupati feodal."
aspect: 1080x1920
language: id
audience: audiens digital muda dan pemerhati sejarah kritis Indonesia
length: 68s
angle: forensic-dossier
VO_MODE: verbatim
voice: id-ID-ArdiNeural
voice_provider: edge-tts
---

## Intent

Pengguna menyetujui Naskah v1 (`SCRIPT.md`) pada 17 Oktober 2026 melalui respons "setuju". Episode ini membedah mitos buku pelajaran sekolah mengenai pembangunan Jalan Raya Pos (*De Grote Postweg*) Anyer–Panarukan menggunakan pendekatan *Forensic Dossier* (Meja Investigasi Sejarah). Tujuh beat editorial forensik dipertahankan secara utuh, dengan format 9:16 (1080x1920), 30 fps, estimasi durasi ~68 detik.

## Assets

- `../../../boards/berkas-polemik/DIRECTION.md` — visual direction v1 yang disetujui.
- `../../../boards/berkas-polemik/EDITORIAL.md` — editorial framework v1 yang disetujui.
- `../../../boards/berkas-polemik/frame.md` — spesifikasi desain kanonikal.
- Font lokal Space Grotesk, Space Mono, dan Newsreader beserta lisensi OFL disalin ke `assets/fonts/`.
- `../SCRIPT.md` dan `../SOURCES.md` — naskah terkunci dan pemetaan bukti arsip primer (Resolutie Daendels Mei 1808 di ANRI, riset Prof. Dr. Djoko Marihandono FIB UI, dan analisis Peter Carey atas William Thorn 1815).

## Customizations

- Palet resmi *Berkas Polemik*: Karbon arsip `#121110`, kertas manila `#EAE0D0`, tinta arsip `#1A1816`, merah stempel `#C32822`, abu-abu baja `#7C756B`, kuning map `#D4A359`.
- Tipografi hibrida forensik: Space Grotesk (700 bold) untuk judul/hook berani; Space Mono untuk kode arsip/stempel/nominal; Newsreader (italic) untuk kutipan otentik dan refleksi batin sejarah.
- Komponen visual: Map berkas terbuka, stempel miring berbingkai (*bordered stamp badge*), batang sensor (*redacted bars*), garis ukur mikro, perbandingan silang Versi A vs Versi B.
- Zona aman short-form: Safe zone atas 140px, safe zone bawah 280px (bebas dari konten kritis agar tidak tertutup antarmuka TikTok/Reels).

## Notes

- Checkpoint 1 (Review Naskah) telah disetujui pengguna ("setuju").
- Tahap aktif saat ini: Pembuatan layout visual storyboard dan kompilasi board still (`boards/storyboard.html`).
- Berhenti di Checkpoint 2 (Review Storyboard Visual) untuk tinjauan pengguna sebelum memulai sintesis audio dan animasi gerak.
