from pathlib import Path
import json,html,re,hashlib,importlib.util
P=Path(__file__).resolve().parent; V=P/'video';ROOT=P.parents[1]
t=json.loads((V/'timing.json').read_text(encoding='utf-8'));scenes=t['scenes'];D=t['duration']
meta=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'));voice=meta['voices'][0]
E=html.escape
paper='#F3EDE3';ink='#302B28';brick='#A34F3F';sand='#D8C8B5'
chrome=(V/'components/chrome.html').read_text(); chrome_css=(V/'components/chrome.css').read_text()
fonts="@font-face{font-family:Newsreader;src:url('../../assets/fonts/newsreader.ttf')}@font-face{font-family:Newsreader;src:url('../../assets/fonts/newsreader-italic.ttf');font-style:italic}@font-face{font-family:'DM Sans';src:url('../../assets/fonts/dm-sans.ttf')}"
def js(x):return json.dumps(x,ensure_ascii=False)

for d in scenes:
    fid=d['id'];du=d['duration'];c1=d['cue1'];c2=d['cue2'];dark=d['number']==3
    fg=paper if dark else ink;bg=ink if dark else paper
    nodes=[];anims=[];n=0
    def node(tag,txt,x,y,w,h=None,size=42,color=None,serif=False,extra=''):
        global n
        n+=1;ident=f'el-{fid}-{n}'
        style=f'left:{x}px;top:{y}px;width:{w}px;font-size:{size}px;color:{color or fg};'+(f'height:{h}px;' if h else '')+('font-family:Newsreader,serif;line-height:1.08;' if serif else 'line-height:1.3;')+extra
        nodes.append(f'<{tag} id="{ident}" class="item" style="{style}">{txt}</{tag}>');return '#'+ident
    def text(txt,x,y,w=848,size=100,color=None,serif=True):
        lines=txt.split('|');return node('div',''.join(f'<span style="display:block">{E(s)}</span>' for s in lines),x,y,w,size=size,color=color,serif=serif)
    def actor(x,y,w,h,color,variant=0):
        return node('div','',x,y,w,h,extra=f'background:{color};border-radius:{"43% 55% 44% 49%" if not variant else "54% 43% 52% 44%"};transform-origin:50% 50%;')
    def path(pathstr,color=brick,width=4,dashed=False):
        global n
        n+=1;ident=f'el-{fid}-{n}';dash='stroke-dasharray="9 13"' if dashed else ''
        nodes.append(f'<svg class="diagram" viewBox="0 0 1080 1920" aria-hidden="true"><path id="{ident}" d="{pathstr}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {dash}/></svg>');return '#'+ident
    def enter(sel,at=0.08,axis='y',amount=20,dur=.62,scale=None):
        start={'opacity':0,axis:amount};end={'opacity':1,axis:0,'duration':dur,'ease':'power3.out'}
        if scale:start['scale']=scale;end['scale']=1
        anims.append(f'tl.fromTo({js(sel)},{js(start)},{js(end)},{at:.6f});')
    def move(sel,at,fr,to,dur=.9):
        anims.append(f'tl.fromTo({js(sel)},{js(fr)},{js(dict(to,duration=dur,ease="power3.inOut",immediateRender=False))},{at:.6f});')
    def draw(sel,at,dur=.9):
        anims.append(f'{{const p=document.querySelector({js(sel)});const l=p.getTotalLength();tl.fromTo(p,{{strokeDasharray:l,strokeDashoffset:l,opacity:1}},{{strokeDashoffset:0,duration:{dur},ease:"power2.inOut"}},{at:.6f});}}')
    def support(txt=None,y=1360,at=None):
        if txt is None:txt=d['support']
        if txt:enter(text(txt,88,y,848,36,serif=False),c2 if at is None else at,amount=10,dur=.5)
    kind=d['layout']
    if kind=='quote':
        enter(text('“Gue dapat|promosi.”',88,320,size=142),.06)
        a1=actor(155,920,230,285,brick);enter(a1,.18,amount=18)
        a2=actor(735,1045,130,175,ink,1);enter(a2,c1+.12,'x',24)
        p=path('M395 1050 Q555 930 715 1110',sand,5);draw(p,c1,.95)
        dot=actor(420,975,42,47,sand);enter(dot,c1,.0 if False else 'y',10,dur=.35)
        move(dot,c2,{'x':0,'y':0},{'x':235,'y':85},.8);support()
    elif kind=='distraction':
        enter(text('“Oh,|bagus.”',88,300,580,132),.06,'x',-25)
        a1=actor(140,1110,155,200,brick);enter(a1,.18)
        a2=actor(590,890,175,220,ink,1);enter(a2,.1)
        screen=node('div','',770,680,120,175,extra=f'border:4px solid {ink};border-radius:14px;');enter(screen,c1,'x',18)
        move(a2,c1,{'x':0,'y':0},{'x':65,'y':-35},.7)
        pp=path('M760 880 Q830 860 825 855',ink);draw(pp,c1+.2,.5)
        support(y=1400)
    elif kind=='shrink':
        enter(text('Senangnya|belum selesai.',88,290,size=115),.05)
        opening=node('div','',150,785,730,440,extra=f'border:4px solid {sand};border-radius:45% 53% 47% 40%;transform-origin:0% 50%;');enter(opening,.12,'x',0,dur=.7)
        a1=actor(285,900,190,230,brick);enter(a1,.15)
        move(opening,c1,{'scaleX':1},{'scaleX':.60},1.05)
        move(a1,c2,{'scale':1},{'scale':.79},.75);support(y=1365)
    elif kind=='boundary':
        enter(text('Satu respons.',88,330,size=126),.05)
        enter(text('yang terlihat',88,710,760,38,serif=False),c1)
        pp=path('M88 835 L936 835',sand,3);draw(pp,c1+.15)
        enter(text('“Oh, bagus.”',88,605,820,78),c1+.08,'x',-20)
        enter(text('Yang belum|kita tahu:',88,950,570,80),c2)
        enter(text('alasannya.',88,1160,848,105,brick),c2+.18,'x',20)
        # Deliberately no additional support paragraph.
    elif kind=='concept':
        enter(text('Capitalization',88,430,848,118),.08)
        enter(text('Berbagi kejadian positif|dengan orang dekat.',88,680,820,43,serif=False),c1)
        for j,word in enumerate(['kejadian','dibagi','disambut']):
            x=88+j*290
            mark=actor(x+50,1060,78,92,brick if j==0 else sand, j%2);enter(mark,c1+j*.4,scale=.90)
            enter(text(word,x,1210,260,34,serif=False),c2+j*.12,'x',-15,dur=.4)
        draw(path('M230 1107 L380 1107 M520 1107 L670 1107',ink,3),c2-.2,.8)
    elif kind=='share':
        enter(text('Dari kabar gue,',88,270,848,96),.05)
        a1=actor(150,620,245,290,brick);enter(a1,.12)
        enter(text('ke cerita kita.',260,1240,670,91),c2,'x',22)
        a2=actor(670,1000,210,250,ink,1);enter(a2,c1,'x',25)
        draw(path('M375 820 C740 580 410 1210 680 1120',sand,6),c1+.15,1.1)
        enter(text('menikmati lagi',480,745,420,36,serif=False),c2,amount=10)
    elif kind=='response':
        enter(text('Aktif-konstruktif',88,270,848,91),.05)
        for j,word in enumerate(['Terlibat.','Tertarik.','Membuka cerita.']):
            at=[c1,c1+1.0,c2][j]
            s=text(word,88,560+j*250,790,87,brick if j==2 else ink);enter(s,at,'x',-36,dur=.65)
        a1=actor(785,1210,105,130,sand,1);enter(a1,c2+.15,scale=.90)
    elif kind=='quiet':
        enter(text('Tenang.',88,355,848,166),.04)
        enter(text('Tetap terasa hadir.',88,650,848,59),c1,'x',20)
        a1=actor(225,1040,175,210,brick);enter(a1,.2,amount=14)
        a2=actor(550,1045,145,190,ink,1);enter(a2,c1+.1,amount=12)
        draw(path('M405 1150 Q477 1120 545 1147',sand,5),c2-.3,.75)
        support(y=1390)
    elif kind=='evidence':
        enter(text('Respons yang|terlibat',88,310,848,107),.05)
        left=actor(160,820,150,190,brick);enter(left,.18)
        draw(path('M340 915 C480 915 500 850 610 850 M340 915 C480 915 500 1110 610 1110',sand,4),c1,1.0)
        enter(text('Kedekatan',620,815,316,57),c1+.18,'x',14)
        enter(text('Kepuasan|hubungan',620,1070,316,52),c1+.5,'x',14)
        enter(text('berkaitan',365,745,245,31,serif=False),c1+.2,amount=8)
        support('Kaitan, bukan jaminan.',y=1390)
    elif kind=='question':
        enter(text('“Bagian mana',88,330,848,108),.06)
        enter(text('yang paling bikin',88,475,848,102),c1-.3,'x',-25)
        enter(text('lo senang?”',88,610,848,121,brick),c1+.25,'x',-25)
        draw(path('M170 1040 Q490 1270 810 1040',sand,6),c2-.25,1.0)
        a1=actor(135,1010,95,115,brick);a2=actor(775,990,120,150,ink,1)
        enter(a1,c2-.25,amount=12);enter(a2,c2,amount=12)
        support('Buka ceritanya.',y=1370,at=c2+.25)
    elif kind=='effort':
        enter(text('“Gue inget|usaha lo.”',88,340,848,120),.05)
        draw(path('M120 1040 L870 1040',sand,5),c1,1.0)
        for j in range(4):
            draw(path(f'M{140+j*170} 1015 L{140+j*170} 1065',brick,4),c1+j*.22,.35)
        a1=actor(750,870,155,200,ink,1);enter(a1,c2,amount=18)
        enter(text('berbulan-bulan',88,1160,660,42,serif=False),c1+.5)
        support(y=1400)
    elif kind=='sequence':
        enter(text('Menikmati|kabar baik.',88,300,848,110),.05)
        draw(path('M170 675 C170 810 790 785 790 940',sand,5),c1,.9)
        enter(text('Membahas juga|kekhawatiran.',88,1010,848,100),c2,'x',20)
        enter(text('Beri keduanya tempat.',88,1380,848,36,serif=False),c2+.18,amount=10)
    elif kind=='offer':
        a1=actor(130,315,210,255,brick);enter(a1,.1,amount=20)
        enter(text('“Gue mau bagi',88,780,848,109),c1-.2,'x',-28)
        enter(text('momen ini.”',88,925,848,124),c2-.3,'x',-28)
        draw(path('M360 480 Q675 480 850 675',sand,5),c1,.8)
        support('Sebentar untuk ikut senang.',y=1360,at=c2+.25)
    elif kind=='reflection':
        enter(text('Ada ruang untuk',88,400,848,104),.05)
        enter(text('ikut senang?',88,540,848,133,brick),c1,'y',20,dur=.75)
        a1=actor(290,1130,150,185,brick);a2=actor(580,1140,130,165,ink,1)
        enter(a1,.2,amount=10,dur=.65);enter(a2,.25,amount=10,dur=.65)
        draw(path('M445 1230 Q510 1260 575 1225',sand,5),c2,.85)
    css=fonts+chrome_css+f'''#root{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden;color:{fg};--rda-meta-ink:{fg};font-family:'DM Sans',sans-serif}}
    .ground{{position:absolute;inset:0;background:{bg}}}.item{{position:absolute;margin:0;font-weight:400;box-sizing:border-box}}.diagram{{position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none}}
    '''
    ch=chrome.replace('{{frame_number}}',f'{d["number"]:02}').replace('{{frame_count}}','14')
    out=f'<template><style>{css}</style><div id="root" data-composition-id="{fid}" data-width="1080" data-height="1920" data-duration="{du:.6f}" data-layout="{kind}" data-board-revision="2026-10-20"><div id="el-{fid}-ground" class="clip ground" data-start="0" data-duration="{du:.6f}" data-track-index="0"></div>'+''.join(nodes)+ch+'</div><script>const tl=gsap.timeline({paused:true});\n'+'\n'.join(anims)+f'\nwindow.__timelines[{js(fid)}]=tl;</script></template>'
    (V/f'compositions/frames/{fid}.html').write_text(out,encoding='utf-8')

# Spoken-only captions, segmented by measured words and punctuation.
groups=[]
for d in scenes:
    chunk=[]
    for w in d['words']:
        if chunk and (len(' '.join(q['text'] for q in chunk+[w]))>48 or len(chunk)>=7):
            groups.append(chunk);chunk=[]
        chunk.append(w)
        if w['text'].endswith(('.', '?', '!')) and len(chunk)>=3:
            groups.append(chunk);chunk=[]
    if chunk:groups.append(chunk)
caps=[];cap_anims=[];srt=[];vtt=['WEBVTT\n']
def stamp(x,sep=','):
    ms=round(x*1000);s,ms=divmod(ms,1000);m,s=divmod(s,60);h,m=divmod(m,60);return f'{h:02}:{m:02}:{s:02}{sep}{ms:03}'
for i,group in enumerate(groups):
    start=t['pre_roll']+group[0]['start'];end=t['pre_roll']+group[-1]['end']+.10
    if i+1<len(groups):end=min(end,t['pre_roll']+groups[i+1][0]['start']-.015)
    words=[w['text'] for w in group];lines=[];line=''
    for word in words:
        if line and len(line+' '+word)>28:lines.append(line);line=word
        else:line=(line+' '+word).strip()
    if line:lines.append(line)
    assert len(lines)<=2,(lines,group)
    display=''.join(f'<span style="display:block">{E(line)}</span>' for line in lines)
    caps.append(f'<div id="caption-{i:03}" class="cap"><div>{display}</div></div>')
    cap_anims.append(f'tl.set("#caption-{i:03}",{{opacity:1}},{start:.6f});tl.set("#caption-{i:03}",{{opacity:0}},{end:.6f});')
    srt.append(f'{i+1}\n{stamp(start)} --> {stamp(end)}\n'+ '\n'.join(lines)+'\n')
    vtt.append(f'{stamp(start,".")} --> {stamp(end,".")}\n'+'\n'.join(lines)+'\n')
(P/'exports').mkdir(exist_ok=True)
(P/'exports/kabar-baik.srt').write_text('\n'.join(srt),encoding='utf-8')
(P/'exports/kabar-baik.vtt').write_text('\n'.join(vtt),encoding='utf-8')
(V/'caption_groups.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2),encoding='utf-8')
hostfonts=fonts.replace('../../assets/','assets/')
capstyle=".cap{position:absolute;left:88px;top:1550px;width:848px;height:190px;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none}.cap>div{max-width:848px;padding:14px 22px;background:#F3EDE3;color:#302B28;font:500 46px/1.25 'DM Sans',sans-serif;text-align:center;box-sizing:border-box}"
caphtml='<template><style>'+fonts.replace('../../assets/','../assets/')+'#root{position:absolute;inset:0;width:100%;height:100%;overflow:hidden}'+capstyle+'</style>'+f'<div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{D}">'+''.join(caps)+'</div><script>const tl=gsap.timeline({paused:true});'+''.join(cap_anims)+"window.__timelines['captions']=tl;</script></template>"
(V/'compositions/captions.html').write_text(caphtml,encoding='utf-8')
mounts='\n'.join(f'<div id="slot-{d["id"]}" class="clip" data-composition-id="{d["id"]}" data-composition-src="compositions/frames/{d["id"]}.html" data-start="{d["start"]:.6f}" data-duration="{d["duration"]:.6f}" data-track-index="1" data-width="1080" data-height="1920"></div>' for d in scenes)
index=f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><title>Kabar baik juga butuh disambut</title><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>{hostfonts}
html,body{{margin:0;background:{paper};width:100%;height:100%;overflow:hidden}}#root{{position:relative;width:100%;height:100%;background:{paper};overflow:hidden}}.clip{{position:absolute;inset:0;width:100%;height:100%}}.cap{{position:absolute;left:88px;right:auto;top:1550px;bottom:auto;width:848px;height:190px;display:flex;align-items:center;justify-content:center;z-index:50;pointer-events:none}}.cap>div{{max-width:848px;padding:14px 22px;background:{paper};color:{ink};font:500 46px/1.25 'DM Sans',sans-serif;text-align:center;box-sizing:border-box}}
</style></head><body><div id="root" data-composition-id="kabar-baik" data-width="1080" data-height="1920" data-duration="{D:.6f}" data-fps="30">
{mounts}
<div id="caption-slot" class="clip" data-track-kind="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{D}" data-track-index="2" data-width="1080" data-height="1920" style="z-index:50"></div>
<audio id="narration" src="{voice['path']}" data-start="{t['pre_roll']}" data-duration="{voice['duration_s']}" data-volume="1" data-track-index="3"></audio>
</div><script>const tl=gsap.timeline({{paused:true}});window.__timelines['kabar-baik']=tl;</script></body></html>'''
(V/'index.html').write_text(index,encoding='utf-8')
assertions=[]
for d in scenes:
    assertions.append(dict(kind='appearsBy',selector=f'#el-{d["id"]}-1',bySec=round(d['start']+.85,6)))
    for part in ['header','footer']:
        assertions.append(dict(kind='staysInFrame',selector=f'[data-composition-id="{d["id"]}"] [data-board-chrome="{part}"]'))
(V/'index.motion.json').write_text(json.dumps(dict(duration=D,assertions=assertions),indent=2),encoding='utf-8')
story=(V/'STORYBOARD.md').read_text(encoding='utf-8').replace('- status: outline','- status: animated')
(V/'STORYBOARD.md').write_text(story,encoding='utf-8')

spec=importlib.util.spec_from_file_location('sound',ROOT/'.agents/skills/shortform-production/scripts/sound_design.py');sd=importlib.util.module_from_spec(spec);spec.loader.exec_module(sd)
manifest=json.loads((ROOT/'boards/ruang-di-antara/assets/audio/sfx/manifest.json').read_text());assets=manifest['assets']
cue_specs=[(1,'contact','event','The good-news mark begins travelling into the shared space.', 'cue2',.52), (2,'air','attention','Listener turns toward the screen; attention changes direction.','cue1',.40),(6,'connection','sharing','The shared connection path completes.','cue1',.55),(10,'connection','invitation','The open listening curve finishes drawing.','cue2',.52),(11,'contact','effort','The final past-effort trace is acknowledged.','cue1',.50),(13,'contact','offer','The sharing gesture becomes concrete.','cue1',.48)]
cues=[]
for scene,asset,slug,purpose,key,gain in cue_specs:
    d=scenes[scene-1];offset=d[key]
    if scene==6:offset+=1.25
    if scene==10:offset+=.75
    if scene==11:offset+=1.0
    if scene==13:offset+=.8
    a=next(x for x in assets if x['id']==asset)
    cues.append(dict(id='sfx-'+slug,scene=str(scene),asset=asset,purpose=purpose,trigger=f'compositions/frames/{d["id"]}.html at local {offset:.6f}s: {purpose}',start=round(d['start']+offset,6),duration=a['duration'],volume=gain,track=4))
plan=dict(version=1,revision='v1',board_audio_revision='2026-10-20',authorization='User --automation --delivery=draft',decisions=dict(narration=dict(mode='use',reason='One native-speed ElevenLabs full-script recording; words drive timing.'),bgm=dict(mode='none',reason='Intimate spoken attention, sparse material sounds and silence carry this exchange.'),sfx=dict(mode='use',reason='Six meaningful attention, sharing and recognition actions; never automatic transition accents.')),silence='Uncued beats and the final reflective question have no effects.',timing_sha256=sd.digest(V/'timing.json'),narration_sha256=sd.digest(V/voice['path']),motion_sources={f'compositions/frames/{d["id"]}.html':sd.motion_digest(V/f'compositions/frames/{d["id"]}.html') for d in scenes},assets=assets,cues=cues)
(V/'sound_design.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
tracker=json.loads((ROOT/'TRACKER.json').read_text(encoding='utf-8-sig'));next(x for x in tracker['productions'] if x['slug']=='kabar-baik').update(stage='production',status='in_progress');(ROOT/'TRACKER.json').write_text(json.dumps(tracker,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(scenes=len(scenes),duration=D,caption_groups=len(groups),sfx_cues=len(cues))))
