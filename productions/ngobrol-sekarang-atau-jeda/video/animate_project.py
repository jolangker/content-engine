"""Animate approved poses using native voice timings; preserve board evidence."""
from pathlib import Path
import json,re,shutil,html
from bs4 import BeautifulSoup

root=Path(__file__).resolve().parent
frames=json.loads((root/'timing.json').read_text(encoding='utf-8'))
audio=json.loads((root/'audio_meta.json').read_text(encoding='utf-8'))
duration=audio['total_duration_s']
archive=root/'.media/approved-poses';archive.mkdir(parents=True,exist_ok=True)
if not (archive/'index.html').exists():shutil.copy2(root/'index.html',archive/'index.html')
old_index=(archive/'index.html').read_text(encoding='utf-8')
shared_css=BeautifulSoup(old_index,'html.parser').style.string
font_css=shared_css[:shared_css.index('*{box-sizing')]

def norm(x):return re.sub(r'[^\w]+','',x).casefold()
def cue(f,phrase,occurrence=0,default=None):
    wanted=[norm(w) for w in phrase.split()]; words=[norm(w['text']) for w in f['words']]
    matches=[i for i in range(len(words)-len(wanted)+1) if words[i:i+len(wanted)]==wanted]
    if not matches and phrase=='demand':
        matches=[i for i,w in enumerate(words) if w=='demandwithdraw']
    if occurrence<len(matches):return round(f['voice_offset']+f['words'][matches[occurrence]]['start'],3)
    if default is not None:return default
    raise ValueError((f['n'],phrase,words))

hosts=[];media=[];sequences={};proof=[]
for f in frames:
    n=f['n'];identity=f'scene-{n:02d}';path=root/f['file'];saved=archive/path.name
    if not saved.exists():shutil.copy2(path,saved)
    soup=BeautifulSoup(saved.read_text(encoding='utf-8'),'html.parser')
    template=soup.template;node=template.find(attrs={'data-composition-id':identity})
    node['data-duration']=str(f['duration'])
    ground=node.select_one('.ground');ground['class']=['ground','clip'];ground['data-start']='0';ground['data-duration']=str(f['duration']);ground['data-track-index']='0'
    ground['id']=identity+'-ground'
    elements={}
    for selector in ['.display','.quote','.maybe','.figure','.rail-label','.rail-sub','.foot','.line','.appointment','.body']:
        found=node.select(selector);elements[selector]=[]
        for j,el in enumerate(found):
            if not el.get('id'):el['id']=f'{identity}-{selector[1:]}-{j}'
            elements[selector].append('#'+el['id'])
    def q(selector,i=0):return elements[selector][i]
    def identify_children(selector):
        parent=node.select_one(selector);selectors=[]
        for j,el in enumerate(parent.find_all(recursive=False)):
            el['id']=f'{identity}-part-{parent.get("id")}-{j}'
            el['style']=(el.get('style','')+';display:block').strip(';')
            selectors.append('#'+el['id'])
        return selectors
    calls=[];notes=[]
    def reveal(selector,at,y=22,secs=.55):
        calls.append(f'tl.fromTo({json.dumps(selector)},{{opacity:0,y:{y}}},{{opacity:1,y:0,duration:{secs},ease:"power3.out"}},{at});')
        notes.append((at,selector,'sequential reveal'))
    def move(selector,at,fromx,tox,secs=.8):
        calls.append(f'tl.fromTo({json.dumps(selector)},{{x:{fromx}}},{{x:{tox},duration:{secs},ease:"power3.inOut",immediateRender:false}},{at});')
        notes.append((at,selector,'relational position change'))
    def draw(selector,at,secs=.7):
        calls.append(f'{{const p=document.querySelector({json.dumps(selector)});const L=p.getTotalLength();tl.fromTo(p,{{strokeDasharray:L,strokeDashoffset:L}},{{strokeDashoffset:0,duration:{secs},ease:"power2.out"}},{at});}}')
        notes.append((at,selector,'svg-path-draw'))
    def fade(selector,at,secs=.5):reveal(selector,at,y=0,secs=secs)
    if n==1:
        reveal(q('.display'),.12);reveal(q('.display',1),cue(f,'Nanti'))
        reveal(q('.figure'),.12,y=0);move(q('.figure'),.12,-95,-95,.01)
        move(q('.figure'),cue(f,'Lo tanya'),-95,-45,.8)
        move(q('.figure'),cue(f,'mendesak'),-45,0,.65)
        reveal(q('.figure',1),cue(f,'Dia bilang'),y=0)
        move(q('.figure',1),cue(f,'Dia bilang'),-160,-160,.01)
        move(q('.figure',1),cue(f,'pergi'),-160,0,.85)
        fade(q('.figure',2),cue(f,'pergi')+.2)
        fade(q('.figure',3),cue(f,'Lo tanya'))
        reveal(q('.foot'),cue(f,'Dia makin'))
    elif n==2:
        reveal(q('.maybe'),.12);reveal(q('.quote'),cue(f,'Kalau ditunda'))
        reveal(q('.figure'),cue(f,'kapan'),y=10)
        fade(q('.line'),cue(f,'Di kepala dia')-.25)
        reveal(q('.maybe',1),cue(f,'Di kepala dia'))
        reveal(q('.quote',1),cue(f,'Gue udah'))
        reveal(q('.figure',1),cue(f,'Gue udah')+.12,y=10)
    elif n==3:
        titleparts=identify_children(q('.display'))
        reveal(titleparts[0],cue(f,'pola'));reveal(titleparts[1],cue(f,'demand'))
        for j,phrase in enumerate(['desakan','menjauh','didesak']):
            at=cue(f,phrase);reveal(q('.figure',j+1),at,y=0);reveal(q('.rail-label',j),at+.04,y=12)
        reveal(q('.rail-sub'),cue(f,'menekan'));reveal(q('.rail-sub',1),cue(f,'menarik'))
        diagram=node.select(q('.figure'))[0];paths=diagram.find_all('path')
        # Split the two vertical legs so each lands on the response it connects.
        paths[0]['d']='M92 210 V337';paths[0]['id']=identity+'-leg-a'
        leg=soup.new_tag('path',attrs={'d':'M92 467 V587','stroke':'#A34F3F','stroke-width':'3','fill':'none','id':identity+'-leg-b'});paths[0].insert_after(leg)
        paths[1]['id']=identity+'-heads';paths[2]['id']=identity+'-return';paths[3]['id']=identity+'-return-head'
        draw('#'+identity+'-leg-a',cue(f,'menjauh')-.15,.5)
        draw('#'+identity+'-leg-b',cue(f,'didesak')-.15,.5)
        fade('#'+identity+'-heads',cue(f,'didesak')+.3,.2)
        draw('#'+identity+'-return',cue(f,'menarik'),.9);fade('#'+identity+'-return-head',cue(f,'menarik')+.8,.2)
        reveal(q('.foot'),cue(f,'diri')+.1,y=10,secs=.4)
    elif n==4:
        parts=identify_children(q('.display'))
        reveal(q('.figure'),.12,y=0);reveal(q('.figure',1),.25,y=0)
        reveal(q('.foot'),cue(f,'meminta'))
        reveal(parts[0],cue(f,'kapan'));reveal(parts[1],cue(f,'dilanjutkan'))
        fade(q('.figure',2),cue(f,'perjelas'))
    elif n==5:
        body=identify_children(q('.body'));title=identify_children(q('.display'))
        reveal(body[0],.15);reveal(body[1],cue(f,'butuh'))
        reveal(title[0],cue(f,'Gue tetap'));reveal(title[1],cue(f,'mau bahas'))
        ap=node.select_one('.appointment');ap['style']='border-top-color:transparent;border-bottom-color:transparent'
        aparts=identify_children(q('.appointment'))
        reveal(aparts[0],cue(f,'Kita lanjut'));reveal(aparts[1],cue(f,'delapan'),y=16)
        notesparts=identify_children(aparts[2]);reveal(notesparts[0],cue(f,'disepakati'))
        reveal(notesparts[1],cue(f,'Kalau belum siap'))
        # Dedicated line layers preserve the approved rail geometry as it draws.
        for suffix,top,at in [('top',960,cue(f,'Kita lanjut')),('bottom',1339,cue(f,'disepakati'))]:
            rail=soup.new_tag('div',attrs={'id':identity+'-rail-'+suffix,'style':f'position:absolute;left:96px;top:{top}px;width:800px;height:3px;background:#302B28'})
            node.section.append(rail)
            calls.append(f'tl.fromTo("#{identity}-rail-{suffix}",{{scaleX:0,transformOrigin:"left center"}},{{scaleX:1,duration:.7,ease:"power3.out"}},{at});')
        reveal(q('.figure'),cue(f,'ditepati'),y=0);reveal(q('.figure',1),cue(f,'sepakati ulang'),y=0)
    else:
        parts=identify_children(q('.display'))
        reveal(q('.figure'),.12,y=0);reveal(q('.figure',1),.28,y=0)
        move(q('.figure'),.12,-45,-45,.01);move(q('.figure',1),.28,45,45,.01)
        reveal(q('.foot'),cue(f,'Obrolannya'))
        for sel,phrase in zip(parts,['setelah jeda','apa kalian','kembali','membahasnya']):reveal(sel,cue(f,phrase),y=16,secs=.45)
        move(q('.figure'),cue(f,'kembali'),-45,0,.8);move(q('.figure',1),cue(f,'kembali'),45,0,.8)
        draw(q('.figure',2)+' path',cue(f,'kembali')+.2,.8)
    for old in template.find_all('script'):old.decompose()
    style=template.style
    style.string=font_css+'\n'+style.get_text()
    script=soup.new_tag('script')
    script.string='const tl=gsap.timeline({paused:true});\n'+'\n'.join(calls)+f'\nwindow.__timelines["{identity}"]=tl;'
    template.append(script)
    path.write_text(str(template)+'\n',encoding='utf-8')
    hosts.append(f'<div class="clip shot" id="mount-{n:02d}" data-label="{html.escape(f["title"])}" data-composition-id="{identity}" data-composition-src="{f["file"]}" data-start="{f["start"]}" data-duration="{f["duration"]}" data-track-index="{n}" data-track-kind="graphics" data-width="1080" data-height="1920"></div>')
    if not audio.get('continuous_narration'):
        media.append(f'<audio id="voice-{n:02d}" src="{f["audio"]}" data-start="{round(f["start"]+f["voice_offset"],3)}" data-duration="{f["voice_duration"]}" data-track-index="8" data-volume="1"></audio>')
    sequences[n]=sorted(notes,key=lambda x:x[0])
    proof.append(round(f['start']+f['duration']-.7,3))

if audio.get('continuous_narration'):
    voice=audio['voices'][0]
    media.append(f'<audio id="voice-narration" data-label="ElevenLabs · George · narasi utuh" src="{voice["path"]}" data-start="0" data-duration="{voice["duration_s"]}" data-track-index="8" data-volume="1"></audio>')

# Adapt the registry Pill Karaoke grouping, sizing and per-word timing mechanism.
registry=BeautifulSoup((root/'compositions/components/caption-pill-karaoke.html').read_text(encoding='utf-8'),'html.parser')
captionjs=registry.find_all('script')[-1].get_text()
words=[]
for f in frames:
    for w in f['words']:
        words.append({'text':w['text'],'start':round(f['start']+f['voice_offset']+w['start'],4),'end':round(f['start']+f['voice_offset']+w['end'],4)})
captionjs=re.sub(r'var TRANSCRIPT = \[.*?\n      \];','var TRANSCRIPT = '+json.dumps(words,ensure_ascii=False)+';',captionjs,flags=re.S)
changes={'DURATION':duration,'SAFE_ZONE_WIDTH':804,'PILL_MAX_WIDTH':804,'PILL_MIN_PADDING_X':24,'PILL_MAX_PADDING_X':30,'FONT_WIDTH_SAFETY':1.04,'FONT_FAMILY':'DM Sans','FONT_WEIGHT':'500','BASE_FONT_SIZE':42,'MIN_FONT_SIZE':40,'MAX_WORDS_PER_GROUP':5,'WORD_SPACING':10,'PAUSE_THRESHOLD':.3,'GROUP_END_BUFFER':.25,'COLOR_INACTIVE':'#D8C8B5','COLOR_ACTIVE':'#F3EDE3','COLOR_FADE_DURATION':.08,'WORD_FADE_LEAD':0}
for key,value in changes.items():captionjs=re.sub(rf'var {key} = .*?;',f'var {key} = {json.dumps(value)};',captionjs)
captionjs=captionjs.replace('.toLowerCase()','')
captionjs=captionjs.replace('tl.set(groupEl, { opacity: 1 }, visibleStart);','tl.set(groupEl, { opacity: 1, visibility: "visible" }, visibleStart);')
captionjs=captionjs.replace('tl.set(groupEl, { opacity: 0 }, visibleEnd);','tl.set(groupEl, { opacity: 0, visibility: "hidden" }, visibleEnd);')
captionjs=captionjs.replace('window.__timelines["caption-pill-karaoke"] = tl;','window.__timelines["captions"] = tl;')
captioncss=font_css+'''#captions-root{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}.caption-layer{position:absolute;inset:0}.safe-zone{position:absolute;top:1600px;left:108px;width:804px;height:116px;display:flex;align-items:center;justify-content:center}.caption-group{position:absolute;inset:0;width:804px;height:116px;display:flex;align-items:center;justify-content:center;opacity:0}.caption-pill{max-width:804px;padding:14px 24px 16px;border-radius:16px;background:#302B28;text-align:center;overflow:visible}.caption-copy{display:flex;flex-direction:column;align-items:center;width:100%;font-family:'DM Sans',sans-serif;font-size:42px;font-weight:500;line-height:1.25;white-space:nowrap;overflow:visible}.caption-line{display:flex;justify-content:center;gap:10px;width:100%;line-height:1.25;white-space:nowrap;overflow:visible}.caption-word{display:inline-block;color:#D8C8B5}'''
captioncss=captioncss.replace('.caption-line{display:flex;', '.caption-line{max-width:756px;display:flex;')
(root/'compositions/captions.html').write_text(f'<template><style>{captioncss}</style><div id="captions-root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{duration}"><div class="caption-layer"><div id="caption-stage" class="safe-zone"></div></div></div><script>{captionjs}</script></template>',encoding='utf-8')
cap=f'<div id="caption-mount" class="clip shot" style="z-index:100" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{duration}" data-track-index="7" data-track-kind="captions" data-width="1080" data-height="1920"></div>'
index=f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><title>Ngobrol sekarang atau jeda — ElevenLabs preview v3</title><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>{shared_css}</style></head><body><div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{duration}">{''.join(hosts)}{cap}{''.join(media)}</div><script>window.__timelines['main']=gsap.timeline({{paused:true}});</script></body></html>'''
(root/'index.html').write_text(index,encoding='utf-8')
(root/'transcript.json').write_text(json.dumps(words,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Keep Studio's caption sidecar in step with the registry renderer. All windows
# of up to five words fit two lines, so only punctuation, pauses and count split
# this transcript; assert that precondition using the shipped font.
from PIL import ImageFont
font=ImageFont.truetype(str(root/'assets/fonts/dm-sans.ttf'),42)
def line_width(items):return sum(font.getlength(w['text'])*1.04 for w in items)+10*max(0,len(items)-1)
for i in range(len(words)):
    window=words[i:i+5]
    assert line_width(window)<=756 or any(line_width(window[:j])<=756 and line_width(window[j:])<=756 for j in range(1,len(window))), 'Caption grouping requires width-aware split'
groups=[];current=[]
for i,w in enumerate(words):
    current.append(dict(w,id=f'w{i}'))
    next_word=words[i+1] if i+1<len(words) else None
    if len(current)>=5 or not next_word or re.search(r'[,.:!?]$',w['text']) or next_word['start']-w['end']>=.3:
        groups.append({'id':f'g{len(groups)}','start':current[0]['start'],'end':current[-1]['end'],'words':current})
        current=[]
for i,g in enumerate(groups):g['end']=duration if i+1==len(groups) else min(groups[i+1]['start'],g['end']+.25)
(root/'caption_groups.json').write_text(json.dumps({'total_duration_s':duration,'width':1080,'height':1920,'groups':groups},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Update the canonical plan without altering the approved script or board images.
story=(root/'STORYBOARD.md').read_text(encoding='utf-8')
story=re.sub(r'^duration: .*$',f'duration: {duration}s',story,flags=re.M)
story=story.replace('Storyboard v1 — untuk tinjauan visual','Storyboard v1 disetujui — animasi preview v1')
story=story.replace('Layout berikut masih menunggu review; `status: built` berarti pose statis tersedia, bukan persetujuan pengguna. Semua timing perkiraan, belum ada audio atau animasi.','Layout disetujui pengguna melalui “cocok” pada 17 Oktober 2026. Timing disinkronkan dengan suara Ardi pilihan pengguna dan metadata kata native. Board PNG tetap merupakan bukti layout yang disetujui.')
story=story.replace('Still ini tidak menyertakan caption bergerak.','Preview animasi memakai satu track caption Pill Karaoke yang diadaptasi ke DM Sans dan palet board; band caption y=1600–1716 menjaga footer pose yang disetujui.')
story=story.split('\n## Persetujuan dan pelaksanaan',1)[0].rstrip()
story=story.replace('Storyboard v1 disetujui — animasi preview v1','Storyboard v1 disetujui — animasi dengan ElevenLabs v3')
story+='\n\n## Persetujuan dan pelaksanaan\n\nLayout storyboard v1 dan naskah tetap disetujui. Pengguna meminta pemasangan narasi ElevenLabs v3 melalui “gas pasang”. Satu track narasi kontinu memakai George dari konfigurasi proyek dan alignment native ElevenLabs. Runtime '+str(duration)+' detik termasuk satu detik tahan penutup. Musik/SFX tidak ditambahkan. Preview dengan audio baru menunggu review; ekspor v1 tetap merupakan hasil versi lama.\n'
for f in frames:
    pattern=rf'(## Frame {f["n"]} — .*?)(?=\n## Frame |\n## Persetujuan|\Z)'
    m=re.search(pattern,story,flags=re.S)
    block=m.group(1)
    block=block.split('\n- blueprint:',1)[0].rstrip()+'\n'
    block=re.sub(r'\([\d.-]+s\)',f'({f["start"]}-{round(f["start"]+f["duration"],3)}s)',block,count=1)
    block=block.replace('- status: built','- status: animated').replace('- review: awaiting_review','- review: layout_approved')
    block=re.sub(r'- duration: .*',f'- duration: {f["duration"]}s',block)
    block=re.sub(r'- poster: .*',f'- poster: {proof[f["n"]-1]}s',block)
    block+='\n- blueprint: compose\n- focal: '+f['screen']+'\n- roles: dua pemeran = foreground subject; tipografi = supporting; field krem/arang = background\n\n'
    for j,(at,sel,motion) in enumerate(sequences[f['n']]):
        block+=f'Scene {j+1} ({at:.3f}–{min(f["duration"],at+.8):.3f}s): {motion} pada {sel}, mengikuti frasa narasi; susunan dan posisi akhir tetap pose yang disetujui. → '+('svg-path-draw' if motion=='svg-path-draw' else 'dynamic-content-sequencing')+'\n'
    story=story[:m.start()]+block+story[m.end():]
(root/'STORYBOARD.md').write_text(story,encoding='utf-8')
script=(root/'SCRIPT.md').read_text(encoding='utf-8').replace('**Voice:** belum dipilih; tidak ada TTS pada tahap storyboard.','**Voice:** Ardi / Microsoft Edge / id-ID-ArdiNeural — dipilih pengguna pada 17 Oktober 2026.\n**Voice settings:** rate +15%; runtime dihitung dari berkas audio, bukan perkiraan.')
for f in frames:script=re.sub(rf'(## Line {f["n"]} — .*?\*\*Time:\*\* )[^\n]+',rf'\g<1>{f["start"]}–{round(f["start"]+f["duration"],3)}s',script,flags=re.S)
(root/'SCRIPT.md').write_text(script,encoding='utf-8')
(root/'proof-times.json').write_text(json.dumps(proof)+'\n',encoding='utf-8')
print(json.dumps({'duration':duration,'scenes':len(frames),'caption_words':len(words),'proof_times':proof,'source':'approved layouts + native voice timings'}))
