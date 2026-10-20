"""Build a visual-first static revision using local, editable SVG illustrations."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / 'v2'
source = (PREVIOUS / 'style-board.html').read_text(encoding='utf-8')

common = '''<defs><filter id="shadow-{key}" x="-30%" y="-30%" width="170%" height="170%"><feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#121110" flood-opacity=".65"/></filter></defs>'''

comparison = '''
<g transform="rotate(-9 345 435)" filter="url(#shadow-a)">
 <rect x="65" y="75" width="555" height="735" fill="#D4A359"/>
 <rect x="79" y="90" width="527" height="706" fill="#EAE0D0"/>
 <rect x="114" y="127" width="78" height="70" fill="#1A1816"/>
 <text x="153" y="176" fill="#EAE0D0" text-anchor="middle" font-size="48" font-family="Space Mono" font-weight="700">A</text>
 <path d="M114 251H515 M114 287H460 M114 323H510 M114 399H480 M114 435H510 M114 471H400" stroke="#7C756B" stroke-width="9"/>
 <circle cx="184" cy="665" r="65" fill="none" stroke="#C32822" stroke-width="13"/>
 <path d="M140 674C153 632 165 695 183 654S204 684 229 647" fill="none" stroke="#1A1816" stroke-width="8"/>
</g>
<g transform="rotate(7 552 610)" filter="url(#shadow-a)">
 <rect x="280" y="279" width="546" height="643" fill="#EAE0D0"/>
 <path d="M772 279H826V333Z" fill="#D4A359"/>
 <rect x="320" y="319" width="78" height="70" fill="#1A1816"/>
 <text x="359" y="368" fill="#EAE0D0" text-anchor="middle" font-size="48" font-family="Space Mono" font-weight="700">B</text>
 <path d="M320 443H750 M320 479H690 M320 515H746 M320 591H720 M320 627H740" stroke="#7C756B" stroke-width="9"/>
 <circle cx="553" cy="788" r="76" fill="none" stroke="#C32822" stroke-width="10" stroke-dasharray="16 13"/>
</g>
<path d="M188 754C192 894 330 936 448 855" fill="none" stroke="#D4A359" stroke-width="7"/>
<path d="M424 854L451 853L445 880" fill="none" stroke="#D4A359" stroke-width="7"/>
'''

close_reading = '''
<g transform="rotate(-8 407 480)" filter="url(#shadow-b)">
 <rect x="104" y="83" width="641" height="802" fill="#EAE0D0"/>
 <rect x="143" y="124" width="92" height="14" fill="#C32822"/>
 <path d="M152 212H655 M152 254H616 M152 296H650 M152 356H620 M152 722H620 M152 764H650 M152 806H530" stroke="#7C756B" stroke-width="10"/>
 <text x="155" y="500" font-family="Newsreader" font-style="italic" font-size="74" fill="#1A1816">ditunda</text>
</g>
<path d="M692 701L833 892" stroke="#7C756B" stroke-width="85" stroke-linecap="round"/>
<path d="M727 747L833 892" stroke="#1D1B19" stroke-width="64" stroke-linecap="round"/>
<circle cx="514" cy="490" r="263" fill="#121110" filter="url(#shadow-b)"/>
<circle cx="514" cy="490" r="249" fill="#EAE0D0" stroke="#7C756B" stroke-width="18"/>
<circle cx="514" cy="490" r="227" fill="none" stroke="#1A1816" stroke-width="3"/>
<path d="M349 354H677 M349 385H630 M349 625H663" stroke="#7C756B" stroke-width="7"/>
<text x="514" y="535" text-anchor="middle" font-family="Newsreader" font-style="italic" font-size="118" fill="#1A1816">ditunda</text>
<path d="M330 565H699" stroke="#C32822" stroke-width="12"/>
<path d="M320 331C345 293 375 276 405 267" fill="none" stroke="#EAE0D0" stroke-width="12" stroke-linecap="round"/>
'''

missing = '''
<g transform="rotate(-4 450 260)" filter="url(#shadow-c)">
 <path d="M126 87H776V361L742 373L715 354L683 378L645 358L611 376L575 358L544 376L508 355L471 379L432 361L400 381L361 360L327 378L289 359L252 378L217 356L178 375L150 358L126 376Z" fill="#EAE0D0"/>
 <rect x="178" y="135" width="110" height="16" fill="#D4A359"/>
 <path d="M178 218H705 M178 259H663 M178 300H700" stroke="#7C756B" stroke-width="10"/>
</g>
<path d="M122 407L153 394L188 414L226 397L259 416L297 399L331 420L368 400L402 418L437 397L474 417L511 397L548 418L583 397L620 417L656 395L690 415L726 398L777 413V585L746 598L706 579L673 599L632 578L597 598L559 578L525 597L485 578L450 597L411 578L375 600L334 579L300 597L262 578L223 599L188 578L154 595L122 579Z" fill="#1D1B19" stroke="#C32822" stroke-width="7" stroke-dasharray="17 13"/>
<text x="450" y="559" text-anchor="middle" font-family="Space Grotesk" font-weight="700" font-size="172" fill="#D4A359">?</text>
<g transform="rotate(4 450 750)" filter="url(#shadow-c)">
 <path d="M126 639L156 623L190 644L227 623L264 644L300 626L337 644L372 626L410 645L446 625L484 643L520 624L557 643L594 625L631 644L669 625L706 643L741 627L776 643V918H126Z" fill="#EAE0D0"/>
 <path d="M178 713H704 M178 754H650 M178 795H700" stroke="#7C756B" stroke-width="10"/>
 <path d="M547 859C569 813 593 895 623 858S669 883 704 846" fill="none" stroke="#1A1816" stroke-width="7"/>
</g>
'''

def svg(key, content, label):
    return f'<svg class="visual" viewBox="0 0 900 1000" role="img" aria-label="{label}">{common.format(key=key)}{content}</svg>'

def frame(key, headline, illustration, caption, note):
    return f'''<div><div class="study-window"><article class="frame frame-{key}">
      <div class="brand"><span>BERKAS POLEMIK</span><span>STUDI {key.upper()}</span></div>
      <div class="sample-label">SIMULASI · BUKAN ARSIP</div>
      <h3>{headline}</h3>{illustration}
    </article></div><div class="study-caption"><b>{caption}</b><p>{note}</p></div></div>'''

frames = '<div class="frames">' + ''.join([
    frame('a', 'Satu tanda<br><span class="mark">hilang.</span>', svg('a', comparison, 'Dua salinan; tanda pada A tidak ditemukan pada B.'), 'A / Perbandingan sebagai objek', 'Tanda utuh dan ruang kosong ditunjukkan langsung pada dua lembar.'),
    frame('b', 'Periksa kata<br><span class="mark">kuncinya.</span>', svg('b', close_reading, 'Kaca pembesar mengisolasi kata rekaan ditunda.'), 'B / Kata menjadi titik fokus', 'Kaca pembesar membawa mata ke satu kata. Konteks dijelaskan lewat narasi.'),
    frame('c', 'Jejaknya<br><span class="mark">belum utuh.</span>', svg('c', missing, 'Dua fragmen dokumen mengapit area kosong yang ditandai tanda tanya.'), 'C / Kekosongan punya bentuk', 'Bagian terputus menjadi metafora keterbatasan bukti, bukan klaim kerusakan arsip nyata.'),
]) + '</div>'

start = source.index(' <div class="frames">')
end = source.index('</section>', start)
source = source[:start] + frames + '\n' + source[end:]
css_start = source.index('.frame .sheet{')
css_end = source.index('.study-caption{', css_start)
source = source[:css_start] + '''.frame .visual{position:absolute;left:84px;top:578px;width:846px;height:900px;overflow:visible}
''' + source[css_end:]
source = source.replace('top:332px;font-size:108px', 'top:324px;font-size:108px')
source = source.replace('V2', 'V3').replace('v2', 'v3')
source = source.replace('IDENTITAS TETAP / CARA BACA DIPERTAJAM', 'VISUAL MEMBAWA PENJELASAN')
source = source.replace('Buka sumbernya.<br>Uji penafsirannya.<br>Nyatakan batasnya.', 'Satu gagasan.<br>Satu visual utama.<br>Sedikit kata.')
source = source.replace('Temuan yang jelas, dengan kesimpulan yang sebanding dengan bukti.', 'Narasi memberi konteks. Objek, hubungan, dan ruang kosong membawa makna di layar.')
source = source.replace('03 / Tiga kebutuhan. Tiga cara membaca.', '03 / Lebih sedikit teks. Lebih banyak yang terlihat.')
source = source.replace('Seluruh isi dokumen di bawah adalah simulasi desain. Tidak memuat kutipan tokoh, kode arsip, atau angka historis. Cuplikan sumber dan komentar editorial dipisahkan secara visual.', 'Tiga studi mandiri: perbedaan tanda, pembacaan detail, dan celah bukti. Semua dokumen adalah ilustrasi; penjelasan panjang berada di narasi.')
source = source.replace('Pada 1080px: judul 108px · bacaan 52px · kutipan 72px · metadata 32–34px. Bukti mendapat ruang baca yang nyata.', 'Judul 3–4 kata. Tanpa paragraf di frame. Visual utama mengisi sekitar dua pertiga area isi.')
source = source.replace('04 / Gerak mengikuti pekerjaan membaca.', '04 / Arah gerak: benda dulu, penjelasan menyusul.')
source = source.replace('Durasi usulan 60–90 detik; ruang baca mengikuti naskah dan materi.', 'Target ±90 detik · 16 adegan utama. Ritme bervariasi mengikuti narasi dan bukti.')
source = source.replace('V1 TETAP DISETUJUI · EDITORIAL & VISUAL V3 MENUNGGU TINJAUAN', 'V1 TETAP DISETUJUI · VISUAL V3 MENUNGGU TINJAUAN')
(ROOT / 'style-board.html').write_text(source, encoding='utf-8')

# Keep the established deterministic export workflow, extending it to check visual bounds.
exporter = (PREVIOUS / 'export-board.py').read_text(encoding='utf-8')
exporter = exporter.replace(".brand,.sample-label,h3,.sheet,.annotation,.limit,.source", ".brand,.sample-label,h3,.visual")
exporter = exporter.replace('if index == 1:', 'if True:')
exporter = exporter.replace('"phone-study-02.png"', 'f"phone-study-{index + 1:02d}.png"')
exporter = exporter.replace('    dimensions = page.evaluate(', '''    page.locator('.frames').screenshot(path=ROOT / "frame-studies.png", animations="disabled")
    frame_copy = page.evaluate(r"""() => [...document.querySelectorAll('.frame')].map(e => ({
      headline_words: e.querySelector('h3').innerText.trim().split(/\\s+/).filter(Boolean).length,
      explanatory_paragraphs: e.querySelectorAll('p').length
    }))""")
    dimensions = page.evaluate(''')
exporter = exporter.replace('"human_approval": False,', '"frame_copy": frame_copy, "human_approval": False,')
(ROOT / 'export-board.py').write_text(exporter, encoding='utf-8')
print('Built v3 editable HTML and exporter.')
