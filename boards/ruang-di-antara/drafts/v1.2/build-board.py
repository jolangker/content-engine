"""Author the editable static board and freeze its inherited local resources."""
from pathlib import Path
from html import escape
import shutil

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent.parent
for name in ('newsreader.ttf', 'newsreader-italic.ttf', 'dm-sans.ttf', 'Newsreader-OFL.txt', 'DM-Sans-OFL.txt'):
    (ROOT / 'assets').mkdir(exist_ok=True)
    shutil.copy2(BASE / 'assets' / name, ROOT / 'assets' / name)
shutil.copytree(BASE / 'components', ROOT / 'components', dirs_exist_ok=True)
shutil.copy2(BASE / 'export-board.py', ROOT / 'export-board.py')

spec = (BASE / 'frame.md').read_text(encoding='utf-8')
front = spec.split('---', 2)[1]
front = front.replace('name: ruang-di-antara-v1.1', 'name: ruang-di-antara-v1.2-draft').replace('implementation_revision: 2026-10-20', 'implementation_revision: 2026-10-21')
front += '''sequence:
  frameCount: 16
  dramaticFrameCount: 2
  lightFrameCount: 14
  targetDurationSeconds: 90
  planningDurationRangeSeconds: [85, 95]
  planningBeatsPerFrame: [3, 5]
paletteModes:
  light: { background: "#F3EDE3", text: "#302B28", metadata: "#302B28", captions: "#302B28" }
  dramatic: { background: "#302B28", text: "#F3EDE3", metadata: "#F3EDE3", captions: "#F3EDE3" }
contentDirection:
  primary: visual-action
  planningEmphasisWords: [0, 5]
  supportingParagraphs: false
  captions: full-spoken-words
'''
body = '''
# Ruang di Antara — frame contract v1.2

Draft implementation of user requirements dated 2026-10-21; awaiting visual review. See DIRECTION.md. The active approved package is retained at the board root.

## Identity and safe areas

Use local Newsreader regular/italic and DM Sans assets. Shared chrome is frozen in components/: header x88–936 / top101 / height34, footer x88–936 / bottom82 / height34. Copy these sources into each production. Header shows the series and current frame / 16; footer shows @eliansatya. Geometry and visibility persist across shots and palette changes. Chrome does not join content choreography.

Keep key content in x88–936 / y230–1480 and captions in y1550–1740. Captions contain spoken words only. One reading priority is visible at a time. Use Newsreader for selective short emphasis; DM Sans for essential labels and captions. Display scale is chosen for the composition and verified at phone size.

## Less text, richer visual storytelling — user revision

Let the visual action occupy most of the content field. Start with 0–5 emphasis words as an implementation guideline, allowing frames without emphasis text. A necessary definition or communication example can be longer, staged over time. Remove supporting paragraphs and labels that only restate narration. The relatable question remains in the spoken hook and full captions; the emphasis layer may show a short question or appear as successive phrases. Caption coverage is not reduced by reducing emphasis copy.

Enrich scenes through context-bearing illustrated objects, voice ribbons, speech spaces, unresolved time, shared event markers, meaningful occlusion and changes in spatial relationships. Keep faceless organic participants, the four-color palette and consistent illustration language. Large interaction scenes and close details should carry meaning when emphasis text is hidden. Use a phone only when attention to a phone is part of the fictional scene; objects do not establish psychological explanations by themselves. Composition should make the action legible before extra labels are considered.

## Sixteen frames and two dramatic palette switches

Exactly sixteen meaningful compositions per standard episode. Fourteen have cream background and charcoal text. Exactly two dramatic frames use charcoal background and cream text. Invert main copy, explanatory labels, captions and metadata together; keep their geometry fixed. Use cream/sand for fine lines and readable text on charcoal. Brick remains a graphic accent, not small text on charcoal.

Select the two dramatic script lines before storyboarding and justify both switches. Their positions follow the story; 04 and 12 in the rhythm strip are illustrative. Separate dramatic frames with cream where the story permits. At the beginning of a dramatic frame, land the inversion together on the dramatic phrase or at its cut; maintain the dark mode for that frame and return to cream for the next light frame. Avoid repeated flashes within a shot. These two frames are not an instruction to alternate background every beat.

Preserve participant identity across palette changes: silhouette, position and trajectory remain locatable. A charcoal participant may invert to cream on charcoal while its established silhouette/continuity identifies it. Distinguish actors through shape as well as color. Color, size and diagram arrows must not imply gender, blame, diagnosis, worth or stronger evidence than the narration provides.

## Multiple internal beats

Every frame develops through meaningful visual changes. Start with 3–5 internal beats as a planning guideline, adapting to reading time and measured speech. Specify starting state → action → response → visible consequence. A beat may redirect attention, change distance, extend a path, expose a boundary, reframe an established element or reveal a decisive phrase. Subtitle changes alone do not count.

Avoid leaving the complete landed composition unchanged through most of a shot. Distribute semantic developments across its duration; a final still hold is purposeful after movement has resolved. A five-second frame can carry four distinct actions without four separate title animations. Some shapes or paths may persist into the next frame to preserve continuity.

Vary timing, scale, direction, focal placement and the relation between typography and diagram. Do not repeat a fixed entrance–diagram–support sequence in every frame. Richness comes from a sequence of readable actions; unnecessary floating, continuous zooms and movement unrelated to meaning do not fulfill the requirement. Use brief stillness to punctuate a dramatic phrase or final reflection.

## Visual vocabulary

Faceless organic forms, illustrated everyday objects, meaningful distance, connections, boundaries, position traces and introduced event markers form one visual vocabulary. B-roll is excluded. Intentional flat color fields keep the explanatory action clear. Build depth through foreground overlaps, large actions and context-bearing objects. Added elements must make the scene or its evolution more legible; general creative recipes do not override this board's relational concept.

## Handoff and review

For every frame, record its focal composition, narration range, timed internal beats, visual consequence, palette mode and sound events. Review all sixteen landed compositions and actual intermediate poses, not just titles or label changes. Exactly two palette entries must be dramatic. Inspect inversion contrast, actor continuity, caption bands and stationary chrome at boundaries. Technical checks do not replace creative review.

The style-board samples are independent fictional studies, not an episode storyboard. The four-pose motion strip describes one frame's evolution; it is not four additional frames. Motion and audio remain conceptual until a production or explicit demonstration is made. Audio direction is in AUDIO.md; editorial and sourcing standards are in EDITORIAL.md.
'''
(ROOT / 'frame.md').write_text('---' + front + '---\n' + body, encoding='utf-8')

def text(lines, x=88, y=340, size=112, fill='currentColor', leading=1.06, italic=False, sans=False):
    family = 'DM Sans' if sans else 'Newsreader'
    style = 'italic' if italic else 'normal'
    weight = 500 if sans else 400
    return '<text x="%s" y="%s" fill="%s" font-family="%s" font-size="%s" font-weight="%s" font-style="%s">%s</text>' % (x, y, fill, family, size, weight, style, ''.join('<tspan x="%s" dy="%s">%s</tspan>' % (x, 0 if i == 0 else size * leading, escape(s)) for i, s in enumerate(lines)))

def actor(x, y, size=1, fill='#A34F3F'):
    return f'<path transform="translate({x} {y}) scale({size})" d="M-75 -88 C-16 -132 77 -102 94 -25 C111 54 56 114 -18 104 C-88 95 -111 -32 -75 -88Z" fill="{fill}"/>'

def path(d, color='#A34F3F', dashed=False, width=4):
    dash = ' stroke-dasharray="10 14"' if dashed else ''
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{dash}/>'

def bubble(x, y, w, h, color='#D8C8B5', filled=False, tail='left'):
    tip = x + w * (.18 if tail == 'left' else .82)
    fill = color if filled else 'none'
    return f'<path d="M{x+55} {y} H{x+w-55} Q{x+w} {y} {x+w} {y+55} V{y+h-55} Q{x+w} {y+h} {x+w-55} {y+h} H{tip+45} L{tip-20} {y+h+70} L{tip-7} {y+h} H{x+55} Q{x} {y+h} {x} {y+h-55} V{y+55} Q{x} {y} {x+55} {y} Z" fill="{fill}" stroke="{color}" stroke-width="5"/>'

def speech(x, y, w=300, color='#A34F3F'):
    return ''.join(path(f'M{x} {y+i*45} C{x+w*.25} {y+i*45-30} {x+w*.5} {y+i*45+30} {x+w*.72} {y+i*45} S{x+w*.9} {y+i*45-15} {x+w} {y+i*45}', color, width=5) for i in range(3))

def phone(x, y, w=240, h=410, color='#D8C8B5', screen='#302B28'):
    return f'<g transform="translate({x} {y}) rotate(8 {w/2} {h/2})"><rect x="0" y="0" width="{w}" height="{h}" rx="35" fill="{color}"/><rect x="12" y="30" width="{w-24}" height="{h-52}" rx="18" fill="{screen}"/><path d="M{w*.4} 16H{w*.6}" stroke="{screen}" stroke-width="5" stroke-linecap="round"/><rect x="35" y="76" width="{w-70}" height="82" rx="16" fill="#D8C8B5"/><path d="M50 106H{w-57} M50 129H{w-85}" stroke="#302B28" stroke-width="5"/><circle cx="{w-44}" cy="76" r="23" fill="#A34F3F"/></g>'

def frame(num, dark, content, captions):
    fg, bg = ('#F3EDE3', '#302B28') if dark else ('#302B28', '#F3EDE3')
    chrome = f'''<foreignObject x="0" y="0" width="1080" height="1920"><div xmlns="http://www.w3.org/1999/xhtml" style="position:relative;width:1080px;height:1920px;--rda-meta-ink:{fg}"><div class="rda-header" data-board-chrome="header"><span>Ruang di Antara</span><span>{num:02d} / 16</span></div><div class="rda-footer" data-board-chrome="footer">@eliansatya</div></div></foreignObject>'''
    return f'<article class="frame" data-palette="{"dramatic" if dark else "light"}"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" style="color:{fg};background:{bg}" role="img" aria-label="Studi komposisi independen {num}">{chrome}{content}{text(captions, x=108, y=1620, size=46, sans=True, leading=1.25)}</svg></article>'

studies = []
studies.append(('A / Cerita bertemu solusi', 'Ruang cerita terbuka → suara bergerak → respons datang beruntun → cerita tertahan.', frame(1, False,
    text(['Cuma mau cerita?'], y=320, size=99)
    + bubble(100, 500, 485, 300) + speech(150, 585, 350)
    + '<g transform="rotate(-8 750 580)"><rect x="660" y="460" width="210" height="160" rx="18" fill="#D8C8B5"/><path d="M700 510H825 M700 550H795" stroke="#302B28" stroke-width="8"/></g>'
    + '<g transform="rotate(7 755 800)"><rect x="655" y="700" width="215" height="160" rx="18" fill="#A34F3F"/><path d="M695 753H825 M695 795H790" stroke="#F3EDE3" stroke-width="8"/></g>'
    + actor(250, 1115, 1.45, '#302B28') + actor(785, 1180, 1.12)
    + path('M385 1115 Q510 1035 606 1108', dashed=True)
    + path('M790 1000 V935 M772 950 L790 930 L808 950', '#302B28'),
    ['Lo cuma pengen cerita,', 'tapi dia langsung ngasih solusi?'])))
studies.append(('B / Perhatian berpindah', 'Cerita mengalir → ponsel mengambil fokus → pendengar beralih → sambungan tertinggal.', frame(4, True,
    text(['Belum selesai.'], y=320, size=102)
    + phone(615, 470, 245, 430)
    + bubble(105, 470, 360, 245, '#D8C8B5') + speech(145, 535, 270, '#D8C8B5')
    + path('M385 1145 Q570 1020 600 1150', '#D8C8B5', True)
    + path('M785 1070 Q910 965 840 915', '#D8C8B5', width=6)
    + actor(270, 1175, 1.52, '#F3EDE3') + actor(785, 1190, 1.02)
    + path('M765 974 L800 943 M860 994 L895 978', '#D8C8B5', width=3),
    ['Lo belum selesai ngomong,', 'perhatiannya udah ke tempat lain.'])))

clock = '<circle cx="525" cy="825" r="310" fill="#D8C8B5"/><circle cx="525" cy="825" r="280" fill="#F3EDE3"/>'
for i in range(12):
    clock += f'<path d="M525 575V600" transform="rotate({i*30} 525 825)" stroke="#302B28" stroke-width="5"/>'
clock += path('M525 825 L415 745', '#302B28', width=12) + path('M525 825 L680 655', '#A34F3F', True, 8)
clock += '<circle cx="525" cy="825" r="18" fill="#302B28"/>'
studies.append(('C / Waktu yang belum pasti', 'Jam terbentuk → kemungkinan waktu bergerak → belum ada titik temu → jeda terasa.', frame(7, False,
    text(['Kapan?'], y=320, size=118) + clock
    + actor(220, 1320, .68, '#302B28') + actor(820, 1320, .68)
    + path('M305 1320 H460 M590 1320 H730', '#A34F3F', True)
    + '<circle cx="525" cy="1320" r="47" fill="none" stroke="#A34F3F" stroke-width="5" stroke-dasharray="9 12"/>',
    ['Yang lo dengar: nanti.', 'Waktunya masih belum jelas.'])))
studies.append(('D / Percakapan punya ruang', 'Cerita dikirim → pertanyaan kembali → ruang balasan terbuka → hubungan bergerak dua arah.', frame(10, False,
    bubble(110, 340, 505, 295) + speech(170, 425, 375)
    + path('M615 490 Q915 490 868 760', '#A34F3F', width=7)
    + bubble(460, 825, 440, 240, '#A34F3F', tail='right')
    + text(['?'], x=610, y=1000, size=170, fill='#A34F3F')
    + path('M450 930 Q250 920 250 1090', '#302B28', width=7)
    + actor(230, 1205, 1.38, '#302B28') + actor(795, 1310, 1.02),
    ['Dia nanya lagi,', 'lo jadi punya ruang buat lanjut.'])))
studies.append(('E / Suara yang tertahan', 'Suara dibuka → lintasan menurun → batas menahan → permintaan akhirnya mendapat tempat.', frame(12, True,
    text(['Dengerin dulu.'], y=320, size=105, italic=True)
    + actor(292, 780, 1.83, '#F3EDE3')
    + bubble(545, 490, 365, 270, '#D8C8B5', filled=True)
    + speech(590, 565, 265, '#302B28')
    + path('M465 810 Q685 885 665 1035', '#D8C8B5', width=7)
    + path('M510 1100 H910', '#F3EDE3', width=6)
    + '<circle cx="665" cy="1060" r="12" fill="#D8C8B5"/>'
    + actor(795, 1320, 1.04)
    + path('M795 1190 V1150', '#D8C8B5', True, 4),
    ['Gue masih pengen cerita.', 'Bisa dengerin dulu sebentar?'])))
studies.append(('F / Kabar jadi milik bersama', 'Kabar dibuka → perhatian bertemu → ruang bersama meluas → cerita diundang lagi.', frame(16, False,
    text(['Ceritain lagi.'], y=320, size=112)
    + bubble(220, 490, 620, 490, '#D8C8B5', filled=True)
    + '<g transform="rotate(-7 525 730)"><rect x="380" y="620" width="290" height="215" rx="14" fill="#F3EDE3"/><path d="M380 635L525 750L670 635" fill="none" stroke="#A34F3F" stroke-width="6"/><path d="M380 825L475 735 M670 825L575 735" fill="none" stroke="#A34F3F" stroke-width="4"/></g>'
    + path('M525 545 V508 M680 590 L710 560 M370 590 L340 560', '#A34F3F', width=7)
    + path('M290 1170 Q380 1030 470 1010 M755 1170 Q670 1030 605 1010', '#A34F3F', width=5)
    + actor(240, 1325, 1.17, '#302B28') + actor(790, 1325, 1.06),
    ['Bagian mana yang paling', 'bikin lo senang?'])))

cards = ''.join(f'<div class="study">{svg}<h3>{title}</h3><p>{note}</p></div>' for title,note,svg in studies)
durations = [5,5,6,5,6,6,6,6,5,6,6,6,5,6,5,6]
timeline = ''.join(f'<div class="rhythm-cell {"dark" if i in (4,12) else ""}"><strong>{i:02}</strong><span>{duration}s</span></div>' for i,duration in enumerate(durations,1))

poses=[]
for i,(label,action) in enumerate([('0–0,7s / buka','Pertanyaan terdengar; ruang cerita terbuka.'),('0,7–2s / kirim','Cerita bergerak ke pendengar.'),('2–3,8s / beralih','Ponsel mengambil perhatian.'),('3,8–5,5s / tertahan','Percakapan tertinggal di tengah.')]):
    x2=245 if i<2 else 285
    y2=78 if i<2 else 42
    svg=f'<svg viewBox="0 0 350 150" role="img" aria-label="Pose beat {i+1}">{actor(70,82,.26,"#302B28")}{actor(x2,y2,.25)}'
    svg+= '<path d="M95 25H170Q180 25 180 35V49Q180 60 167 60H110L100 70L103 60H95Z" fill="none" stroke="#D8C8B5" stroke-width="2"/>'
    if i>0: svg+=path('M105 82 Q165 45 215 77', '#A34F3F', i>1, 2) + path('M115 40H158','#A34F3F',False,2)
    if i>1: svg+= '<rect x="300" y="8" width="27" height="45" rx="4" fill="#302B28"/><rect x="304" y="16" width="19" height="23" fill="#D8C8B5"/>' + path('M260 55 Q280 20 297 30','#302B28',False,2)
    if i==3: svg+='<path d="M190 90V130" stroke="#A34F3F" stroke-width="3"/>'
    poses.append(f'<div class="pose">{svg}</svg><h3>{label}</h3><p>{action}</p></div>')

html='''<!doctype html><html lang="id"><head><meta charset="utf-8"><title>Ruang di Antara / v1.2</title><style>
@font-face{font-family:Newsreader;src:url('assets/newsreader.ttf');font-weight:100 900;font-style:normal}
@font-face{font-family:Newsreader;src:url('assets/newsreader-italic.ttf');font-weight:100 900;font-style:italic}
@font-face{font-family:'DM Sans';src:url('assets/dm-sans.ttf');font-weight:100 900}
*{box-sizing:border-box}html,body{margin:0;background:#F3EDE3;color:#302B28}body{font-family:'DM Sans',sans-serif}main{width:1600px;padding:55px 72px 42px}h1,h2,h3,p{margin:0}p{font-size:18px;line-height:1.5}.meta{display:flex;justify-content:space-between;font-size:14px;letter-spacing:.12em;text-transform:uppercase;border-bottom:1px solid #302B28;padding-bottom:20px}.hero{display:grid;grid-template-columns:1.4fr 1fr;align-items:center;gap:60px;padding:46px 0 38px}.hero h1{font:400 100px/.96 Newsreader}.hero h1 em{color:#A34F3F}.hero p{font-size:22px;max-width:480px}.kicker{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:#A34F3F;margin-bottom:14px}.tokens{display:grid;grid-template-columns:1fr 1fr;gap:60px;padding:26px 0 32px;border-top:1px solid #D8C8B5;border-bottom:1px solid #D8C8B5}.swatches{display:flex;gap:12px}.swatch{width:116px;height:48px;border:1px solid #D8C8B5;margin-bottom:8px}.token{font-size:12px}.type{font:italic 400 38px/1.2 Newsreader;margin-bottom:10px}.tokens p{font-size:16px}.section-title{display:flex;align-items:baseline;justify-content:space-between;margin:32px 0 22px}.section-title h2{font:400 42px/1.1 Newsreader}.section-title p{font-size:15px;max-width:640px;text-align:right}.studies{display:grid;grid-template-columns:repeat(3,1fr);gap:32px 28px}.frame{width:100%;aspect-ratio:1080/1920;border:1px solid #D8C8B5;overflow:hidden}.frame>svg{display:block;width:100%;height:100%}.study h3,.pose h3{font-size:17px;line-height:1.35;font-weight:500;margin:13px 0 7px}.study p{font-size:16px;line-height:1.45}.motion{border-top:1px solid #D8C8B5;margin-top:30px;padding-top:3px}.poses{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}.pose svg{display:block;width:100%;height:145px;border:1px solid #D8C8B5}.pose p{font-size:16px}.rhythm{display:grid;grid-template-columns:repeat(16,1fr);gap:9px;margin-top:20px}.rhythm-cell{border:1px solid #D8C8B5;padding:14px 5px;text-align:center}.rhythm-cell strong{display:block;font-size:21px;font-weight:500}.rhythm-cell span{display:block;margin-top:8px;font-size:14px}.dark{background:#302B28;color:#F3EDE3;border-color:#302B28}.notes{display:grid;grid-template-columns:1fr 1fr;gap:50px;margin:23px 0}.notes h3{font-size:14px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;margin-bottom:10px}.notes p{font-size:17px}.footer{border-top:1px solid #302B28;margin-top:30px;padding-top:18px;display:flex;justify-content:space-between;font-size:12px}
''' + (ROOT/'components/chrome.css').read_text(encoding='utf-8') + '''</style></head><body><main>
<div class="meta"><span>ELIAN SATYA / RUANG DI ANTARA</span><span>V1.2 / VISUAL REVISION 02 / 21 OKTOBER 2026</span></div>
<section class="hero"><h1>Lebih terasa.<br><em>Lewat visual.</em></h1><div><div class="kicker">Hook bertanya. Adegan bercerita.</div><p>Teks singkat.<br>Interaksi besar.<br>Beberapa aksi dalam satu frame.</p></div></section>
<section class="tokens"><div><div class="kicker">01 / Palet + dua momen dramatis</div><div class="swatches">''' + ''.join(f'<div class="token"><div class="swatch" style="background:{v}"></div>{k}<br>{v}</div>' for k,v in [('Krem','#F3EDE3'),('Arang','#302B28'),('Bata','#A34F3F'),('Pasir','#D8C8B5')]) + '''</div><p style="margin-top:14px">14 frame krem · 2 frame arang dengan teks krem.</p></div><div><div class="kicker">02 / Dua cara berbicara</div><div class="type">“Lo juga pernah ngerasain?”</div><p>Newsreader 400 / regular + italic: pertanyaan, kutipan, refleksi.<br>DM Sans 400–500: penjelasan, label, caption, identitas seri.</p></div></section>
<section><div class="section-title"><h2>Visual mengambil ruang utama.</h2><p>Enam studi independen. Copy ilustratif; caption tetap lengkap.<br>0–5 kata penekanan sebagai panduan awal, boleh tanpa teks utama.</p></div><div class="studies">''' + cards + '''</div></section>
<section class="motion"><div class="section-title"><h2>Satu frame. Beberapa hal terjadi.</h2><p>Empat pose statis dari satu komposisi selama 5,5 detik.<br>Ini arahan gerak, belum demonstrasi animasi.</p></div><div class="poses">''' + ''.join(poses) + '''</div></section>
<section><div class="section-title"><h2>16 frame / sekitar 90 detik.</h2><p>Contoh ritme: total 90 detik. Frame 04 + 12 mendemonstrasikan<br>dua inversi; penempatannya mengikuti momen dramatis naskah.</p></div><div class="rhythm">''' + timeline + '''</div><div class="notes"><div><h3>Setiap frame berkembang</h3><p>Mulai dari 3–5 beat aksi, respons, perubahan perhatian atau konsekuensi. Jeda muncul setelah perubahan terbaca. Timing menyesuaikan narasi dan waktu baca.</p></div><div><h3>Audio mengikuti kejadian</h3><p>Narasi dekat, bunyi material terpilih, hening yang disengaja. Momen dramatis boleh dipertegas lewat jeda. Musik dipilih sesuai episode; audio di board ini masih konseptual.</p></div></div></section>
<footer class="footer"><span>Ruang di Antara / v1.2 · Visual revision 02 · Draf untuk review</span><span>Font lokal · SVG editable · 6 studi independen · Pose gerak & audio konseptual</span></footer>
</main></body></html>'''
(ROOT/'style-board.html').write_text(html, encoding='utf-8')
(ROOT/'assets/SOURCES.md').write_text('''# Asset provenance — v1.2 draft

Local font files and licenses are copied from the approved board assets. Original sources: https://github.com/google/fonts/tree/main/ofl/newsreader and https://github.com/google/fonts/tree/main/ofl/dmsans . Font binaries are not modified.

The independent SVG studies and static motion poses were authored locally for this revision in build-board.py and emitted into style-board.html. Copy is fictional, not researched episode content. No photo, B-roll or generated raster imagery is used. Shared series chrome is copied from the active board components.

The SFX library is inherited from ../../../assets/audio/sfx/manifest.json at the board root; this draft does not generate, change or audition audio assets.
''', encoding='utf-8')
print(f'Authored {ROOT / "style-board.html"}; 6 independent studies, 16-cell rhythm, 2 dramatic cells, {sum(durations)} seconds.')
