"""Build the timed scene plan and seek-safe board-based composition."""
import json, pathlib, re, math, html, difflib
P=pathlib.Path(__file__).resolve().parent; V=P/'video'
S=json.loads((P/'scenes.json').read_text(encoding='utf-8'))
A=json.loads((V/'audio_meta.json').read_text(encoding='utf-8')); W=A['voices'][0]['words']
def norm(s): return re.sub(r'[^\w]','',s.lower())
expected=[norm(w) for s in S for w in s['vo'].split()]
actual=[norm(w['text']) for w in W]
assert expected==actual, list(difflib.unified_diff(expected,actual))
PRE=.4; END=1.2; D=math.ceil((A['total_duration_s']+PRE+END)*30)/30
offset=0
for i,s in enumerate(S):
    n=len(s['vo'].split()); words=W[offset:offset+n]; offset+=n
    s.update(number=i+1,id=f'{i+1:02d}-{s["kind"]}',word_start=offset-n,word_end=offset,words=words)
    s['start']=0 if i==0 else PRE+words[0]['start']-.07
for i,s in enumerate(S):
    s['end']=S[i+1]['start'] if i+1<len(S) else D
    s['duration']=s['end']-s['start']
    s['cue1']=max(.8,min(s['duration']*.45,PRE+s['words'][min(4,len(s['words'])-1)]['start']-s['start']))
    s['cue2']=min(s['duration']-1.0,max(s['duration']*.55,PRE+s['words'][min(8,len(s['words'])-1)]['start']-s['start']))
(V/'timing.json').write_text(json.dumps({'duration':D,'pre_roll':PRE,'tail':END,'scenes':S},ensure_ascii=False,indent=2),encoding='utf-8')
story=f'''---
format: 1080x1920
duration: 90s
message: A pause needs an explicit and kept agreement to return.
arc: interrupted conversation → interaction pattern → distinction → example → follow-through → reflection
audience: Indonesian adults
mode: autonomous
music: none
layout_approved: false
execution_policy: automation
---

## Video direction

Board Ruang di Antara v1.1; see frame.md. Measured narration is {A['total_duration_s']:.2f}s; composition {D:.3f}s. One full-script Brian/eleven_v4 request. Every scene has a different relational state. No native delegation permission: frame-worker contract executed inline serially, one scene at a time. No human approval fabricated.

Use two solid, faceless forms, meaningful open space and a shared path. Keep typography x88–936, y160–650, relational graphics y740–1290, supporting words above y1480, captions y1550–1740. Cream except pressure frame 04. Headline → response → consequence are separated in time. Motion is smooth and bounded, with still reading time. Main copy follows exact scenes.json text.

'''
for s in S:
    story+=f'''## Frame {s['number']} — {s['title']}

- scene: {s['title']}; state {s['kind']}.
- duration: {s['duration']:.6f}s
- start: {s['start']:.6f}s
- end: {s['end']:.6f}s
- transition_in: cut
- poster: {min(s['duration']-.5,s['cue2']+.5):.3f}s
- status: animated
- voiceover: "{s['vo']}"
- src: compositions/frames/{s['id']}.html
- blueprint: compose
- asset_candidates: []
- focal: {s['text']}
- roles: two faceless actors, relationship path, exact support text
- words: {s['word_start']}–{s['word_end']-1}

Scene 1 (0.0–{s['cue1']:.2f}s): headline introduces the single understanding point; first actor establishes the current distance. Layout: editorial title above, large relationship diagram below. Smooth positional entrance.
Scene 2 ({s['cue1']:.2f}–{s['cue2']:.2f}s): second response changes the relationship geometry; path or boundary develops with the narration. Bounded x/y movement; no camera move.
Scene 3 ({s['cue2']:.2f}–{s['duration']:.2f}s): exact supporting text “{s['support']}” enters as the consequence becomes clear. Hold the landed pose for reading. No mid-video exit.

'''
(V/'STORYBOARD.md').write_text(story,encoding='utf-8')

def path(d,cls='path',dash=False):
    return f'<path class="{cls}" d="{d}" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"'+(' stroke-dasharray="14 13"' if dash else '')+'/>'

FONT="""@font-face{font-family:Newsreader;src:url('../../assets/fonts/newsreader.ttf')}@font-face{font-family:'DM Sans';src:url('../../assets/fonts/dm-sans.ttf')}"""

for s in S:
    i=s['number']; sid=s['id']; dur=s['duration']; c1=s['cue1']; c2=s['cue2']; dark=i==4
    bg='#302B28' if dark else '#F3EDE3'; ink='#F3EDE3' if dark else '#302B28'; acc='#D8C8B5' if dark else '#A34F3F'
    # The forms are deliberately person-neutral. Distinct states support each idea.
    posa=(170,160); posb=(620,160); extra=''; move=''; labels=[]
    if i==1:
        extra=path('M310 260 H440')+path('M535 260 H640','other-path',True)
        labels=[(190,75,'“Nanti aja.”'),(530,395,'Kapan?')]
        move=f"tl.to('#{sid}-b',{{x:85,duration:1.1,ease:'power3.inOut'}},{c1});"
    elif i==2:
        extra=path('M300 260 H670','path',True)
        labels=[(145,60,'Minta jawaban'),(600,440,'Mundur')]
        move=f"tl.to('#{sid}-a',{{x:120,duration:1.05,ease:'power3.inOut'}},{c1});tl.to('#{sid}-b',{{x:80,duration:1.05,ease:'power3.inOut'}},{c1+.5});tl.to('#{sid}-a',{{x:195,duration:.85,ease:'power3.inOut'}},{c2-.6});"
    elif i==3:
        posa=(150,170);posb=(630,170)
        extra=path('M300 185 C390 20 620 20 690 185')+path('M640 360 C550 515 325 515 265 360','other-path')
        labels=[(355,20,'Mendesak'),(335,520,'Menjauh')]
        move=f"tl.to('#{sid}-a',{{x:45,duration:.8,ease:'power3.inOut'}},{c1});tl.to('#{sid}-b',{{x:45,duration:.8,ease:'power3.inOut'}},{c1+.65});"
    elif i==4:
        posa=(180,190);posb=(600,190)
        extra=path('M360 280 L615 280','path',True)
        labels=[(275,30,'Persoalan awal'),(225,470,'Cara kita ngobrol')]
        move=f"tl.to('#{sid}-a',{{x:45,duration:.9,ease:'power3.inOut'}},{c1});tl.to('#{sid}-b',{{x:-45,duration:.9,ease:'power3.inOut'}},{c1+.4});"
    elif i==5:
        extra='<text class="question" x="475" y="300" text-anchor="middle">?</text>'+path('M320 270 H400','path',True)+path('M550 270 H635','other-path',True)
        labels=[(300,450,'Alasannya belum diketahui')]
    elif i==6:
        posa=(170,170);posb=(620,170)
        extra=path('M375 80 V420','path',True)+path('M575 80 V420','other-path',True)
        labels=[(355,470,'Ruang untuk mereda')]
        move=f"tl.to('#{sid}-a',{{x:-35,duration:1.2,ease:'power3.inOut'}},{c1});tl.to('#{sid}-b',{{x:35,duration:1.2,ease:'power3.inOut'}},{c1});"
    elif i==7:
        posa=(180,200);posb=(605,200)
        extra=path('M310 300 H645')
        labels=[(115,45,'Tujuan'),(390,45,'Waktu'),(635,45,'Tindak lanjut')]
    elif i==8:
        posa=(170,230);posb=(620,230)
        extra=path('M305 310 C410 190 525 190 645 310')
        labels=[(200,55,'Masih mau membahas')]
        move=f"tl.to('#{sid}-a',{{x:35,duration:1,ease:'power3.inOut'}},{c1});"
    elif i==9:
        posa=(160,240);posb=(620,240)
        extra='<text class="clock" x="475" y="180" text-anchor="middle">20.00</text>'+path('M315 330 H635')
        labels=[(220,510,'Waktu yang disepakati')]
    elif i==10:
        posa=(130,180);posb=(680,180)
        extra=path('M295 280 C420 80 530 80 675 280')
        labels=[(300,430,'Kembali sesuai kesepakatan')]
        move=f"tl.to('#{sid}-a',{{x:105,duration:1.4,ease:'power3.inOut'}},{c1});tl.to('#{sid}-b',{{x:-105,duration:1.4,ease:'power3.inOut'}},{c1});"
    elif i==11:
        posa=(255,180);posb=(535,180)
        extra=path('M390 280 H555')
        labels=[(265,55,'Kembali ke persoalan awal'),(315,470,'Lanjut membahas')]
        move=f"tl.to('#{sid}-a',{{x:15,duration:1,ease:'power3.inOut'}},{c1});tl.to('#{sid}-b',{{x:-15,duration:1,ease:'power3.inOut'}},{c1});"
    elif i==12:
        posa=(180,230);posb=(620,230)
        extra=path('M315 320 H475','path',True)+path('M535 320 H635','other-path',True)
        labels=[(235,50,'Sepakat. Tertunda. Terulang?')]
    elif i==13:
        posa=(180,160);posb=(620,160)
        extra=path('M490 35 V460')
        labels=[(210,470,'Keselamatan lo lebih dulu')]
        move=f"tl.to('#{sid}-a',{{x:-40,duration:1,ease:'power3.inOut'}},{c1});"
    else:
        posa=(220,200);posb=(570,200)
        extra=path('M360 300 C430 235 530 235 590 300')
        labels=[(260,475,'Jeda → kesepakatan → kembali')]
        move=f"tl.to('#{sid}-a',{{x:30,duration:1.2,ease:'power3.inOut'}},{c1});tl.to('#{sid}-b',{{x:-30,duration:1.2,ease:'power3.inOut'}},{c1});"
    label_markup=''.join(f'<text class="diag-label label{j}" x="{x}" y="{y}">{html.escape(t)}</text>' for j,(x,y,t) in enumerate(labels))
    title_size=102 if len(s['text'])<36 else 92
    css=FONT+f"""
    #root{{position:absolute;inset:0;width:100%;height:100%;font-family:'DM Sans',sans-serif;color:{ink};overflow:hidden}}
    .ground{{position:absolute;inset:0;background:{bg}}}
    .frame-content{{position:absolute;inset:0;padding:164px 144px 440px 88px;box-sizing:border-box}}
    .eyebrow{{display:flex;justify-content:space-between;align-items:center;font-size:26px;letter-spacing:.11em;text-transform:uppercase;border-top:2px solid {ink};padding-top:23px}}
    .headline{{font-family:Newsreader,serif;font-weight:400;font-size:{title_size}px;line-height:1.055;letter-spacing:-.025em;margin:100px 0 0;max-width:848px}}
    .diagram{{position:absolute;left:30px;top:755px;width:950px;height:565px;color:{acc}}}
    .actor{{position:absolute;width:160px;height:210px;border-radius:43% 55% 44% 49%;background:{ink};z-index:2}}
    .actor-b{{background:#A34F3F;border-radius:53% 44% 51% 43%}}
    svg{{position:absolute;inset:0;width:950px;height:565px;overflow:visible}}
    .diag-label{{fill:{ink};font-family:'DM Sans';font-size:29px;font-weight:500}}
    .clock{{fill:{ink};font-family:Newsreader;font-size:110px}}
    .question{{fill:{ink};font-family:Newsreader;font-size:140px}}
    .support{{position:absolute;left:88px;right:144px;top:1350px;font-size:37px;line-height:1.3;margin:0;max-width:820px}}
    .footer{{position:absolute;left:88px;right:144px;top:1483px;font-size:25px;letter-spacing:.015em;display:flex;justify-content:space-between}}
    """
    # Later elements appear only on their spoken cue; explicit fromTo endpoints are seek-safe.
    js=f"""const tl=gsap.timeline({{paused:true}});
    tl.fromTo('#{sid}-headline',{{y:24,opacity:0}},{{y:0,opacity:1,duration:.62,ease:'power3.out'}},.08);
    tl.fromTo('#{sid}-a',{{opacity:0,y:18}},{{opacity:1,y:0,duration:.65,ease:'power3.out'}},.25);
    tl.fromTo('#{sid}-b',{{opacity:0,y:18}},{{opacity:1,y:0,duration:.65,ease:'power3.out'}},{min(c1,.9)});
    tl.fromTo('#{sid}-svg .path',{{opacity:0,scaleX:0,transformOrigin:'50% 50%'}},{{opacity:1,scaleX:1,duration:.85,ease:'power3.inOut'}},{c1});
    tl.fromTo('#{sid}-svg .other-path',{{opacity:0,scaleX:0,transformOrigin:'50% 50%'}},{{opacity:1,scaleX:1,duration:.85,ease:'power3.inOut'}},{c2-.4});
    tl.fromTo('#{sid}-svg .diag-label',{{opacity:0,y:12}},{{opacity:1,y:0,duration:.5,stagger:.18,ease:'power3.out'}},{c1});
    tl.fromTo('#{sid}-svg .clock,#{sid}-svg .question',{{opacity:0}},{{opacity:1,duration:.5,ease:'power3.out'}},{c1});
    tl.fromTo('#{sid}-support',{{y:16,opacity:0}},{{y:0,opacity:1,duration:.55,ease:'power3.out'}},{c2});
    {move}
    window.__timelines['{sid}']=tl;"""
    markup=f'''<template>
<style>{css}</style>
<div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{dur:.6f}">
 <div class="clip ground" data-start="0" data-duration="{dur:.6f}" data-track-index="0"></div>
 <div class="frame-content">
  <div class="eyebrow"><span>Ruang di antara</span><span>{i:02d} / 14</span></div>
  <h1 class="headline" id="{sid}-headline">{html.escape(s['text'])}</h1>
  <div class="diagram">
   <svg id="{sid}-svg" viewBox="0 0 950 565" aria-hidden="true">{extra}{label_markup}</svg>
   <div class="actor" id="{sid}-a" style="left:{posa[0]}px;top:{posa[1]}px"></div>
   <div class="actor actor-b" id="{sid}-b" style="left:{posb[0]}px;top:{posb[1]}px"></div>
  </div>
  <p class="support" id="{sid}-support">{html.escape(s['support'])}</p>
  <div class="footer"><span>@eliansatya</span><span>percakapan &amp; tindak lanjut</span></div>
 </div>
</div>
<script>{js}</script>
</template>'''
    markup=markup.replace(f'id="{sid}-',f'id="el-{sid}-').replace(f'#{sid}-',f'#el-{sid}-')
    markup=markup.replace('class="clip ground"',f'id="el-{sid}-ground" class="clip ground"')
    markup='\n'.join(line for line in markup.splitlines() if not (
        ('svg .other-path' in line and 'other-path' not in extra) or
        ('svg .clock,' in line and 'class="clock"' not in extra and 'class="question"' not in extra)))
    (V/f'compositions/frames/{sid}.html').write_text(markup,encoding='utf-8')
    sidecar={'duration':dur,'assertions':[
        {'kind':'appearsBy','selector':f'#el-{sid}-headline','bySec':.8},
        {'kind':'before','a':f'#el-{sid}-headline','b':f'#el-{sid}-support'},
        {'kind':'staysInFrame','selector':f'#el-{sid}-a'},
        {'kind':'staysInFrame','selector':f'#el-{sid}-b'}]}
    (V/f'compositions/frames/{sid}.motion.json').write_text(json.dumps(sidecar,indent=2),encoding='utf-8')

# Short subtitle phrases from actual words, no delivery tags.
groups=[]
for s in S:
    group=[]
    for w in s['words']:
        proposed=' '.join(x['text'] for x in group+[w])
        if group and (len(proposed)>37 or len(group)>=6):
            groups.append(group);group=[]
        group.append(w)
        if re.search(r'[.?!:]$',w['text']) and len(group)>=2:
            groups.append(group);group=[]
    if group: groups.append(group)
cap=[]
for j,g in enumerate(groups):
    start=PRE+g[0]['start']; end=PRE+g[-1]['end']+.12
    if j+1<len(groups):end=min(end,PRE+groups[j+1][0]['start']-.025)
    cap.append(dict(id=f'caption-{j:03d}',start=start,end=end,text=' '.join(x['text'] for x in g),words=g))
(V/'caption_groups.json').write_text(json.dumps(cap,ensure_ascii=False,indent=2),encoding='utf-8')
hosts='\n'.join(f'<div id="scene-{s["id"]}" class="clip scene" data-composition-id="{s["id"]}" data-composition-src="compositions/frames/{s["id"]}.html" data-start="{s["start"]:.6f}" data-duration="{s["duration"]:.6f}" data-width="1080" data-height="1920" data-track-index="0"></div>' for s in S)
captions='\n'.join(f'<div id="{c["id"]}" class="clip caption" data-start="{c["start"]:.6f}" data-duration="{c["end"]-c["start"]:.6f}" data-track-index="2"><span class="caption-inner">{html.escape(c["text"])}</span></div>' for c in cap)
fx=html.escape(json.dumps({'version':1,'nodes':[{'type':'gain','id':'voice-level','label':'Narration level','params':{'gain':3}},{'type':'truepeak','id':'voice-ceiling','label':'Delivery ceiling','params':{'ceiling':-3,'lookahead':3,'release':80}}]},separators=(',',':')),quote=True)
index=f'''<!doctype html><html><head><meta charset="utf-8"><title>Jeda yang kembali</title>
<script src="assets/gsap.min.js"></script>
<style>@font-face{{font-family:'DM Sans';src:url('assets/fonts/dm-sans.ttf')}}
*{{box-sizing:border-box}}html,body{{margin:0;width:100%;height:100%;overflow:hidden;background:#F3EDE3}}
#root{{width:100%;height:100%;position:relative;background:#F3EDE3;overflow:hidden}}
.scene{{position:absolute;inset:0;width:100%;height:100%}}
.caption{{position:absolute;left:88px;top:1550px;width:848px;height:180px;z-index:100;display:flex;align-items:center;justify-content:center}}
.caption-inner{{font:500 46px/1.25 'DM Sans',sans-serif;color:#F3EDE3;background:#302B28;padding:17px 26px;border-radius:14px;max-width:848px;text-align:center}}
</style></head><body>
<div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{D:.6f}">
{hosts}
{captions}
<audio id="narration" src="{A['voices'][0]['path']}" data-start="{PRE}" data-duration="{A['total_duration_s']}" data-track-index="1" data-volume="1" data-fx-chain="{fx}"></audio>
</div><script>const tl=gsap.timeline({{paused:true}});window.__timelines['main']=tl;</script>
</body></html>'''
(V/'index.html').write_text(index,encoding='utf-8')
def ts(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(P/'exports').mkdir(exist_ok=True)
(P/'exports/jeda-yang-kembali.srt').write_text('\n\n'.join(f'{i+1}\n{ts(c["start"])} --> {ts(c["end"])}\n{c["text"]}' for i,c in enumerate(cap))+'\n',encoding='utf-8')
print(json.dumps({'scenes':len(S),'captions':len(cap),'duration':D,'alignment_exact':True,'midpoints':','.join(str(round(s['start']+min(s['duration']-.4,s['cue2']+.5),3)) for s in S)}))
