"""Pose approved-script beats as static HyperFrames scenes and a review board."""
from pathlib import Path
import json, re, shutil

ROOT = Path(__file__).resolve().parent
if (ROOT / 'audio_meta.json').exists():
    raise RuntimeError('Static pose generation is closed after audio/animation begins. Revise the affected composition instead of rebuilding approved work.')
BOARD = ROOT.parents[2] / 'boards' / 'ruang-di-antara'
for folder in ('assets/fonts', 'compositions/frames', 'boards/stills', 'capture/extracted'):
    (ROOT / folder).mkdir(parents=True, exist_ok=True)
for name in ('newsreader.ttf', 'newsreader-italic.ttf', 'dm-sans.ttf', 'Newsreader-OFL.txt', 'DM-Sans-OFL.txt'):
    shutil.copy2(BOARD / 'assets' / name, ROOT / 'assets/fonts' / name)

source = (ROOT.parent / 'SCRIPT.md').read_text(encoding='utf-8')
narration = source.split('## Narasi utuh', 1)[1].split('## Pembagian beat', 1)[0].strip()
paragraphs = narration.split('\n\n')
assert len(paragraphs) == 11, 'Approved narration structure changed; inspect before rebuilding.'
groups = [(0,2), (2,4), (4,5), (5,7), (7,9), (9,11)]
voices = [' '.join(paragraphs[a:b]) for a,b in groups]
assert ' '.join(voices) == ' '.join(paragraphs)
(ROOT / 'user_script.txt').write_text(narration+'\n', encoding='utf-8')
(ROOT / 'capture/extracted/visible-text.txt').write_text(narration+'\n', encoding='utf-8')
(ROOT / 'capture/extracted/tokens.json').write_text(json.dumps({
    'title':'Ngobrol sekarang atau jeda',
    'description':'Kenali urutan mendesak–menjauh dan perjelas kapan kembali membahas masalah.',
    'colors':['#F3EDE3','#302B28','#A34F3F','#D8C8B5'],
    'fonts':['Newsreader','DM Sans']}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

fonts = '''@font-face{font-family:Newsreader;src:url('assets/fonts/newsreader.ttf') format('truetype');font-weight:200 800;font-display:block}
@font-face{font-family:Newsreader;src:url('assets/fonts/newsreader-italic.ttf') format('truetype');font-weight:200 800;font-style:italic;font-display:block}
@font-face{font-family:'DM Sans';src:url('assets/fonts/dm-sans.ttf') format('truetype');font-weight:100 1000;font-display:block}'''
css = fonts + '''
*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#F3EDE3}
body{color:#302B28;font-family:'DM Sans',sans-serif;-webkit-font-smoothing:antialiased}
#root{width:100%;height:100%;position:relative;overflow:hidden}
.shot{position:absolute;inset:0;width:100%;height:100%;overflow:hidden}
.ground{position:absolute;inset:0;background:#F3EDE3}.dark .ground{background:#302B28}
.dark{color:#F3EDE3}.eyebrow{position:absolute;left:96px;top:148px;font-size:25px;letter-spacing:3px;text-transform:uppercase;font-weight:500}
.page-number{position:absolute;right:150px;top:148px;font-size:25px;letter-spacing:3px}
h1,h2,p{margin:0} .display{position:absolute;left:96px;top:285px;width:820px;font-family:Newsreader,serif;font-weight:400;font-size:135px;line-height:1.04;letter-spacing:-4px}
.display span{display:block}.display em{font-weight:400;color:#A34F3F}.dark .display em{color:#D8C8B5}
.body{position:absolute;left:96px;width:800px;font-size:42px;line-height:1.4}
.small{font-size:28px;letter-spacing:1px}.figure{position:absolute;display:block}
.foot{position:absolute;left:96px;top:1470px;right:168px;font-size:30px;line-height:1.4}
.foot:before{content:'';display:block;width:80px;height:3px;background:currentColor;margin-bottom:28px}
.quote{position:absolute;left:96px;width:635px;font-family:Newsreader,serif;font-size:100px;line-height:1.07;letter-spacing:-2px;font-weight:400}
.quote span{display:block}.maybe{position:absolute;left:100px;font-size:27px;letter-spacing:2px;text-transform:uppercase}
.line{position:absolute;height:3px;background:#D8C8B5}
.rail-label{position:absolute;left:310px;font-size:53px;font-weight:500;line-height:1.15}
.rail-sub{position:absolute;left:310px;font-size:29px;line-height:1.3;max-width:450px}
.appointment{position:absolute;left:96px;top:960px;width:800px;border-top:3px solid #302B28;border-bottom:3px solid #302B28;padding:35px 0 33px}
.appointment .time{font-family:Newsreader,serif;font-size:156px;line-height:1;letter-spacing:-4px;color:#A34F3F}
.appointment .note{font-size:35px;line-height:1.4;margin-top:16px}
'''

def blob(x,y,w,color,variant=0,ghost=False):
    path = ('M12 118 C5 43 66 9 122 24 C201 43 217 106 184 167 C153 221 38 220 12 118Z'
            if variant==0 else 'M29 70 C66 9 137 21 177 76 C219 137 165 209 112 202 C40 195 0 128 29 70Z')
    style = f'fill="{color}"' if not ghost else f'fill="none" stroke="{color}" stroke-width="2.5" stroke-dasharray="5 7"'
    return f'<svg class="figure" style="left:{x}px;top:{y}px;width:{w}px;height:{w}px" viewBox="0 0 220 220" aria-hidden="true"><path d="{path}" {style}/></svg>'

def svg(content,x,y,w,h,view=None):
    return f'<svg class="figure" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px" viewBox="0 0 {view or str(w)+" "+str(h)}" aria-hidden="true">{content}</svg>'

arrow = '<path d="M0 0 L-16 -10 M0 0 L-16 10" fill="none" stroke="#A34F3F" stroke-width="3"/>'
scenes = []
scenes.append('''<h1 class="display" style="top:340px">Sekarang.</h1>
<p class="display" style="left:350px;top:700px;width:560px;font-size:125px;color:#A34F3F">Nanti aja.</p>'''
    + blob(96,1060,290,'#302B28') + blob(660,1060,280,'#A34F3F',1)
    + blob(500,1060,280,'#D8C8B5',1,True)
    + svg('<path d="M5 30 H115 M100 20 L115 30 L100 40" fill="none" stroke="#A34F3F" stroke-width="3"/>',400,1160,160,60)
    + '<p class="foot">Lo tanya lagi. Dia makin diam.</p>')

scenes.append('''<span class="maybe" style="top:315px">Di kepala lo, mungkin</span>
<h1 class="quote" style="top:390px"><span>Kapan gue</span><span>didengerin?</span></h1>
<div class="line" style="left:96px;top:820px;width:800px;opacity:.45"></div>
<span class="maybe" style="top:920px;color:#D8C8B5">Di kepala dia, bisa jadi</span>
<p class="quote" style="top:995px;color:#D8C8B5"><span>Gue lagi</span><span>kewalahan.</span></p>'''
    + blob(744,570,175,'#F3EDE3') + blob(744,1170,175,'#A34F3F',1))

scenes.append('''<h1 class="display" style="font-size:102px;top:285px"><span>Pola</span><em>demand–withdraw</em></h1>'''
    + svg('''<path d="M92 210 V337 M92 467 V587" stroke="#A34F3F" stroke-width="3" fill="none"/>
<path d="M81 322 L92 337 L103 322 M81 572 L92 587 L103 572" stroke="#A34F3F" stroke-width="3" fill="none"/>
<path d="M92 720 V770 H640 Q690 770 690 720 V65 Q690 20 640 20 H92 V80" stroke="#A34F3F" stroke-width="3" fill="none"/>
<path d="M81 65 L92 80 L103 65" stroke="#A34F3F" stroke-width="3" fill="none"/>''',105,630,790,800)
    + blob(123,700,150,'#302B28') + blob(123,955,150,'#A34F3F',1) + blob(123,1210,150,'#302B28')
    + '<p class="rail-label" style="top:750px">Mendesak</p><p class="rail-sub" style="top:825px">“Bahas sekarang.”</p>'
    + '<p class="rail-label" style="top:1005px">Menjauh</p><p class="rail-sub" style="top:1080px">Percakapan terhenti.</p>'
    + '<p class="rail-label" style="top:1260px;font-size:49px">Makin mendesak</p>'
    + '<p class="foot">Urutan respons yang berulang.</p>')

scenes.append('''<h1 class="display" style="top:310px;font-size:150px"><span>Kapan</span><span>kita <em>lanjut?</em></span></h1>'''
    + blob(110,1070,265,'#302B28') + blob(660,1070,265,'#A34F3F',1)
    + svg('''<path d="M0 60 C80 60 100 15 175 15 C250 15 270 60 350 60" stroke="#A34F3F" stroke-width="3" fill="none" stroke-dasharray="5 10"/>
<path d="M175 -4 V29 M161 12 H189" stroke="#A34F3F" stroke-width="3" fill="none"/>''',370,1145,290,70,'350 70')
    + '<p class="foot"><span style="display:block">Meminta jeda belum tentu</span><span style="display:block">berarti menghindar.</span></p>')

scenes.append('''<h1 class="display" style="top:300px;font-size:117px"><span>Gue tetap</span><span>mau <em>bahas ini.</em></span></h1>
<p class="body" style="top:650px;width:740px"><span style="display:block">Gue lagi kewalahan.</span><span style="display:block">Gue butuh jeda buat tenang.</span></p>
<div class="appointment"><p class="small">LANJUT JAM DELAPAN, YA?</p><p class="time">20.00</p><p class="note"><span style="display:block">Sepakati. Tepati.</span><span style="display:block">Kalau belum siap, kabari.</span></p></div>'''
    + blob(610,1310,130,'#302B28') + blob(770,1310,130,'#A34F3F',1))

scenes.append('''<h1 class="display" style="top:285px;font-size:113px"><span>Setelah jeda,</span><span>apa kalian</span><span>kembali</span><em>membahasnya?</em></h1>'''
    + blob(225,1100,240,'#302B28') + blob(570,1100,240,'#A34F3F',1)
    + svg('<path d="M0 30 C38 30 50 12 76 12 C102 12 115 30 151 30" stroke="#A34F3F" stroke-width="3" fill="none"/>',435,1200,160,60)
    + '<p class="foot">Obrolannya tetap perlu dilanjutkan.</p>')

titles=['Sekarang / nanti','Dua kemungkinan suara batin','Pola yang berulang','Jeda yang diperjelas','Rencana kembali','Kembali membahasnya']
slugs=['sekarang-nanti','suara-batin','pola-berulang','kapan-lanjut','rencana-kembali','refleksi']
starts=[0,8,18,31,40,55]; durations=[8,10,13,9,15,10]; posters=[4,13,25,35,48,60]
roles=['Mengenali situasi kecil yang menahan percakapan.','Membuka dua kemungkinan pengalaman batin tanpa menetapkan motif.','Memperlihatkan urutan respons sebagai pola, bukan tipe orang.','Membedakan satu permintaan jeda dari pola menghindar.','Memberi contoh jeda dengan rencana kembali yang dapat disepakati.','Menilai tindak lanjut melalui pertanyaan refleksi.']
keymessages=['Keinginan membahas dan respons menunda dapat berbenturan.','Kita belum tahu alasan masing-masing hanya dari perilakunya.','Desakan dan penarikan diri dapat membentuk urutan berulang.','Kapan kembali berbicara perlu diperjelas.','Jadwal kembali adalah contoh kesepakatan yang perlu ditindaklanjuti.','Jeda belum menyelesaikan masalah; percakapan perlu dilanjutkan.']
screen=['Sekarang. / Nanti aja.','Kapan gue didengerin? / Gue lagi kewalahan.','Mendesak → menjauh → makin mendesak; Pola demand–withdraw','Kapan kita lanjut?','Gue tetap mau bahas ini. / Lanjut jam delapan, ya?','Setelah jeda, apa kalian kembali membahasnya?']
types=['hook','pain_point','product_intro','benefit_highlight','feature_showcase','cta']

hosts=[]; frames=[]; script=['# Narasi dikunci — v1\n\n**Voice:** belum dipilih; tidak ada TTS pada tahap storyboard.\n**Voice direction:** intim, tenang, observatif; bahasa lo–gua.\n\nNarasi identik dengan SCRIPT.md v1 yang disetujui di folder induk.\n']
for i,content in enumerate(scenes):
    n=i+1; identity=f'scene-{n:02d}'; file=f'compositions/frames/{n:02d}-{slugs[i]}.html'
    dark=' dark' if i==1 else ''
    template=f'''<!doctype html><html lang="id"><head><meta charset="utf-8"></head><body><template>
<style>#{identity}-root{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden}}</style>
<div id="{identity}-root" data-composition-id="{identity}" data-width="1080" data-height="1920" data-duration="{durations[i]}">
<section class="shot{dark}"><div class="ground"></div><div class="eyebrow">Ruang di Antara</div><div class="page-number">{n:02d}</div>{content}</section>
</div><script>window.__timelines['{identity}']=gsap.timeline({{paused:true}});</script>
</template></body></html>'''
    (ROOT / file).write_text(template,encoding='utf-8')
    hosts.append(f'<div class="clip shot" id="mount-{n:02d}" data-composition-id="{identity}" data-composition-src="{file}" data-start="{starts[i]}" data-duration="{durations[i]}" data-track-index="{n}" data-width="1080" data-height="1920"></div>')
    frames.append({'n':n,'title':titles[i],'start':starts[i],'duration':durations[i],'poster':posters[i],'file':file,'role':roles[i],'key':keymessages[i],'vo':voices[i],'screen':screen[i],'type':types[i]})
    script += [f'## Line {n} — {titles[i]} (Frame {n})\n\n**Time:** {starts[i]}–{starts[i]+durations[i]}s\n**Delivery:** observatif, beri ruang pada batas kalimat.\n\n    {voices[i]}\n']
(ROOT/'SCRIPT.md').write_text('\n'.join(script),encoding='utf-8')
(ROOT/'index.html').write_text(f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><title>Ngobrol sekarang atau jeda — storyboard statis</title><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>{css}</style></head><body><div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="65">{''.join(hosts)}</div><script>window.__timelines['main']=gsap.timeline({{paused:true}});</script></body></html>''',encoding='utf-8')
(ROOT/'boards/frame-manifest.json').write_text(json.dumps(frames,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

story=['''---
format: 1080x1920
duration: 65s
message: "Kenali urutan mendesak–menjauh; bila perlu jeda, sepakati kapan kembali membahasnya."
arc: story-explainer with how-to
audience: orang dewasa yang merefleksikan komunikasi dalam hubungan
mode: collaborative
music: none
---

# Storyboard v1 — untuk tinjauan visual

Narasi v1 disetujui pada 17 Oktober 2026. Enam beat editorial dari naskah dipertahankan. Layout berikut masih menunggu review; `status: built` berarti pose statis tersedia, bukan persetujuan pengguna. Semua timing perkiraan, belum ada audio atau animasi. `music: none` mencegah pemilihan musik otomatis sebelum kebutuhan audio disepakati.

## Video direction

Dua pemeran organik tanpa wajah; warna bukan kode gender/kebenaran. Krem dominan, satu frame arang untuk pengalaman batin. Newsreader untuk suara batin/refleksi; DM Sans untuk konsep. Jarak dan garis menyatakan urutan respons. Tidak ada sentuhan dramatis atau pemulihan ajaib pada penutup. Sisihkan y=1500–1650 bagi caption nanti; isi utama berakhir sebelum y=1500; area bawah y>=1650 dan sisi kanan x>=930 bebas isi utama. Still ini tidak menyertakan caption bergerak.

Referensi langsung: board ruang-di-antara v1; SCRIPT.md dan SOURCES.md di folder induk. Penamaan pola berdasarkan S1; opsi jeda dan rencana kembali berdasarkan S2. Monolog batin dan jam 20.00 adalah ilustrasi.

Pencarian katalog: `cycle diagram circular arrows connected nodes` (tier words). Flowchart/sticky notes dan constellation hub tersedia; belum cocok dengan metafora dua pemeran serta urutan umpan balik board ini. Diagram SVG khusus mempertahankan bahasa visual board, tanpa efek baru.
''']
for f in frames:
    story.append(f'''## Frame {f['n']} — {f['title']} ({f['start']}-{f['start']+f['duration']}s)

- act: {'Pengenalan' if f['n']<3 else 'Memahami pola' if f['n']<5 else 'Kemungkinan respons'}
- status: built
- review: awaiting_review
- src: {f['file']}
- duration: {f['duration']}s
- poster: {f['poster']}s
- transition_in: cut
- type: {f['type']}
- persuasion: {'Demonstration' if f['n']==3 else 'Concretization' if f['n']<3 else 'Worked example' if f['n']==5 else 'Question→answer pairing'}
- beat: {'recognition' if f['n']<3 else 'clarity' if f['n']<5 else 'resolve'}
- scene: {f['screen']}
- voiceover: {f['vo']}

narrativeRole: {f['role']}

keyMessage: {f['key']}

Pose statis: lihat boards/stills/ dan board HTML. Teks layar utama: {f['screen']}

Saat animasi nanti: pertahankan layout ini setelah disetujui; pecah kemunculan sesuai frasa narasi dan timing rekaman. Gerak tidak dibuat sebelum review visual. Sumber dan batas: {'S1; urutan ilustratif, bukan kesimpulan sebab-akibat.' if f['n']==3 else 'Dialog/monolog ilustratif; kemungkinan pengalaman batin.' if f['n']<3 else 'S2; opsi komunikasi, bukan jaminan keberhasilan.'}
''')
(ROOT/'STORYBOARD.md').write_text('\n'.join(story),encoding='utf-8')
print(json.dumps({'frames':len(frames),'duration':65,'narration_words':len(narration.split()),'narration_unchanged':True}))
