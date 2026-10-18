---
name: ruang-di-antara-v2
source: ../../../boards/ruang-di-antara/DIRECTION.md
colors:
  background: "#F3EDE3"
  foreground: "#302B28"
  accent: "#A34F3F"
  secondary: "#D8C8B5"
typography:
  display:
    family: Newsreader
    weight: 400
    size: 108
  body:
    family: DM Sans
    weight: 400
  caption:
    family: DM Sans
    weight: 500
    size: 48
    line_height: 1.22
spacing:
  action_safe: 54
  title_safe_x: 108
  title_safe_y: 192
  caption_left: 112
  caption_right: 160
  caption_top: 1510
  caption_height: 150
---

# Ruang di Antara v2 — episode kabar baik

Spec khusus dari board yang dipilih, bukan adaptasi preset generik. Referensi editorial: [EDITORIAL.md](../../../boards/ruang-di-antara/EDITORIAL.md). Referensi visual: [DIRECTION.md](../../../boards/ruang-di-antara/DIRECTION.md).

## Bahasa ilustrasi

Bentuk potongan kertas yang tegas, bidang warna datar, gestur yang terbaca. Dua pemeran abstrak tanpa detail gender: A berbaju bata dan B berbaju arang. Warna tidak menandai benar/salah. Kepala, tangan, tubuh, benda dan ruang digambar sebagai elemen SVG terpisah supaya tahap animasi dapat melanjutkan pose yang disetujui.

Satu ruang tamu menjadi jangkar: pintu di kiri, jendela di kanan, dua kursi dan meja bundar. A tetap di kiri, B di kanan pada two-shot; close-up memakai arah pandang yang sama. Kilas balik latihan dan presentasi memakai pakaian yang konsisten. Detail HP, kartu catatan, tangan, dan cangkir membawa perkembangan cerita.

## Komposisi

Ilustrasi utama mengambil bidang 1080×1920; tindakan penting berakhir sebelum y=1440. Ruang subtitle y=1510–1660, dalam title-safe. Tidak menanam ruler atau safe-box ke dalam frame. Bidang lantai/dinding boleh full bleed; kepala, gestur kunci, HP, dan teks dipertahankan dalam ruang aman.

Default shot tanpa headline. Teks penekanan hanya pada tiga shot: “Ikut senang.”, “Aktif-konstruktif”, “Ceritain.”; satu kelompok pada satu waktu, 0–5 kata. Newsreader 400 (termasuk italic) hanya untuk penekanan tersebut, DM Sans untuk subtitle. Contoh subtitle statis memperlihatkan hierarki, bukan alignment final.

## Tahap ini

Empat belas pose statis; timing estimasi 90 detik. Tidak ada gerak dekoratif, audio, atau video export. Rencana tindakan/gerak ditulis di storyboard, bukan diklaim sudah dianimasikan. Layout menjadi dasar animasi setelah review visual.
