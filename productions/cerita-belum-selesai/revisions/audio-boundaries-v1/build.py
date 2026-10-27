from pathlib import Path
import json, sys, html, shutil

V=Path(__file__).resolve().parent/'video'
S=json.loads((V/'scenes.json').read_text(encoding='utf-8'))
ANIM='--animate' in sys.argv
def w(p,s):
    p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding='utf-8')
def g(n,body,extra=''): return f'<g class="beat b{n}" {extra}>{body}</g>'
def path(d,stroke='var(--ink)',width=5,cls='',extra=''):
    return f'<path class="{cls}" d="{d}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def actor(x,y,s=1,who='a'):
    # Shape, not color alone, maintains participant identity through inversions.
    d='M -83 -107 C -140 -66 -120 60 -63 102 C 6 149 99 82 102 2 C 106 -84 1 -143 -83 -107 Z' if who=='a' else 'M -67 -88 C -112 -52 -103 42 -47 84 C 13 130 93 59 89 -4 C 85 -66 3 -119 -67 -88 Z'
    color='var(--ink)' if who=='a' else '#A34F3F'
    return f'<g transform="translate({x} {y}) scale({s})"><path d="{d}" fill="{color}"/></g>'
def bubble(x,y,ww,hh,side='left',fill='var(--bg)',stroke='#D8C8B5'):
    # Adapted registry hw-text-cloud: rounded speech space with a directed tail.
    tail=f'L {ww*.2} {hh} L {ww*.12} {hh+65} L {ww*.13} {hh}' if side=='left' else f'L {ww*.85} {hh} L {ww*.91} {hh+65} L {ww*.72} {hh}'
    d=f'M 35 0 H {ww-35} Q {ww} 0 {ww} 35 V {hh-35} Q {ww} {hh} {ww-35} {hh} {tail} H 35 Q 0 {hh} 0 {hh-35} V 35 Q 0 0 35 0 Z'
    return f'<g transform="translate({x} {y})"><path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="5"/></g>'
def waves(x,y,ww=320,rows=3,color='#A34F3F'):
    return ''.join(path(f'M {x} {y+j*42} C {x+ww*.3} {y-28+j*42} {x+ww*.52} {y+32+j*42} {x+ww*.8} {y+j*42} S {x+ww*.96} {y-6+j*42} {x+ww} {y+j*42}',color,5,'draw') for j in range(rows))
def note(x,y,ww=220,hh=155,fill='#D8C8B5',rot=0):
    col='var(--bg)' if fill=='#A34F3F' else 'var(--ink)'
    return f'<g transform="translate({x} {y}) rotate({rot})"><rect width="{ww}" height="{hh}" rx="12" fill="{fill}"/>'+path(f'M 32 48 H {ww-35} M 32 78 H {ww-60}',col,6)+'</g>'
def text(x,y,s,size=50,color='var(--ink)'):
    return f'<text x="{x}" y="{y}" font-family="DM Sans" font-size="{size}" fill="{color}">{html.escape(s)}</text>'
def dot(x,y,r=9,color='#A34F3F'): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'

arts=[]
arts.append(g(1,actor(250,1240,1.22)+actor(795,1280,1.15,'b'))+g(2,bubble(120,580,480,300)+waves(165,655,360))+g(3,path('M 365 1160 Q 520 1015 680 1140','#A34F3F',5,'draw'))+g(4,note(670,580,235,150,rot=-8)+note(695,790,220,145,'#A34F3F',8)))
arts.append(g(1,actor(245,1250,1.1)+actor(800,1240,1.1,'b'))+g(2,bubble(155,590,730,370))+g(3,waves(210,685,600))+g(4,path('M 350 1215 Q 535 1045 715 1210','#A34F3F',5,'draw')+dot(535,1130)))
arts.append(g(1,'<rect x="650" y="555" width="245" height="675" rx="8" fill="#D8C8B5"/>'+path('M 680 1200 V 590 L 850 640 V 1210')+dot(818,930,7,'var(--ink)'))+g(2,actor(675,1230,1.15)+path('M 760 1290 H 892 V 1425 H 760 Z M 795 1290 V 1250 H 850 V 1290',width=6))+g(3,note(150,610,330,255,rot=-6)+path('M 205 770 L 375 680','#A34F3F',6,'draw'))+g(4,bubble(120,1010,330,180)+waves(160,1060,245,2)))
arts.append(g(1,actor(230,1195,1.3)+actor(800,1040,1.22,'b'))+g(2,bubble(120,585,490,280,fill='var(--bg)',stroke='#D8C8B5')+waves(165,650,350,color='#D8C8B5'))+g(3,path('M 360 1115 Q 510 900 620 1070','#D8C8B5',6,'draw'))+g(4,note(665,605,240,180,'#A34F3F',8)+path('M 630 980 V 1240','#D8C8B5',8)))
arts.append(g(1,bubble(125,560,600,370)+waves(175,650,455,2))+g(2,path('M 175 800 C 320 770 400 840 520 800','#A34F3F',5,'draw'))+g(3,note(655,1050,235,170,rot=7))+g(4,actor(260,1240,1.05)+path('M 380 1250 Q 500 1165 600 1250','#A34F3F',5,'draw')+dot(620,1250,7)))
arts.append(g(1,actor(750,1045,1.8,'b'))+g(2,actor(225,1300,.65)+path('M 340 1280 Q 500 1280 550 1140','#D8C8B5',5,'draw'))+g(3,note(565,590,285,180,rot=-7))+g(4,text(260,820,'?',210)+path('M 335 880 Q 355 1010 500 1040','#A34F3F',5,'draw')))
arts.append(g(1,bubble(130,555,450,270)+waves(175,625,330,2)+actor(220,1000,.85))+g(2,note(645,610,250,175,'#A34F3F',6))+g(3,bubble(380,1070,510,275,'right')+waves(440,1150,380,2,'var(--ink)')+actor(800,940,.85,'b'))+g(4,path('M 405 895 Q 575 950 535 1060','#D8C8B5',5,'draw')+path('M 550 880 L 585 915 M 585 880 L 550 915','#A34F3F',4)))
arts.append(g(1,actor(230,1170,1.05)+actor(800,1170,1.05,'b'))+g(2,bubble(120,565,405,255)+waves(160,630,305,2))+g(3,path('M 335 1085 C 400 865 680 865 710 1085','#A34F3F',5,'draw'))+g(4,path('M 700 1260 C 570 1440 315 1400 325 1270','var(--ink)',5,'draw')+bubble(610,620,285,170,'right')+text(720,745,'?',76)))
arts.append(g(1,actor(265,1125,1.6)+actor(810,1320,.75,'b'))+g(2,bubble(120,555,650,300)+waves(165,630,515,1))+g(3,waves(165,685,515,1))+g(4,waves(165,740,515,1)+'<g class="advice-wait">'+note(700,980,180,125,rot=8)+'</g>'))
arts.append(g(1,bubble(125,555,760,420,'right',fill='#D8C8B5',stroke='#D8C8B5'))+g(2,waves(185,660,590,2,'var(--ink)'))+g(3,text(685,880,'?',120,'#A34F3F'))+g(4,actor(250,1270,1.15)+actor(800,1310,1.02,'b')+path('M 720 1060 Q 530 1040 365 1190','#A34F3F',6,'draw')))
arts.append(g(1,actor(225,1190,1.15)+actor(800,1190,1.1,'b'))+g(2,bubble(125,560,400,250)+waves(170,630,300,2))+g(3,path('M 350 1090 Q 540 900 705 1090','#D8C8B5',5,'draw'))+g(4,path('M 350 1090 C 410 1200 645 1260 705 1090','#A34F3F',6,'draw')+bubble(605,695,275,180,'right')+waves(640,750,205,2,'var(--ink)')))
arts.append(g(1,actor(350,1300,1.1)+actor(700,1320,1.05,'b'))+g(2,path('M 525 1170 V 970 Q 525 925 410 865 M 525 970 Q 640 935 740 865','#D8C8B5',6,'draw'))+g(3,bubble(125,570,350,260,fill='var(--bg)',stroke='#D8C8B5')+waves(170,640,255,2,'#D8C8B5'))+g(4,bubble(600,570,300,260,'right',fill='#D8C8B5')+note(650,620,180,125,'#A34F3F')+dot(525,1020,14,'#D8C8B5')))
arts.append(g(1,bubble(125,570,310,220)+waves(165,635,220,2)+note(615,580,275,210,rot=7))+g(2,path('M 270 970 Q 490 1110 760 965','#D8C8B5',6,'draw'))+g(3,dot(290,980,25))+g(4,actor(330,1280,1.08)+actor(720,1280,1.02,'b')+path('M 430 1280 Q 525 1160 625 1280','#A34F3F',5,'draw')))
arts.append(g(1,actor(260,1280,1.25)+actor(815,1310,.82,'b'))+g(2,bubble(120,560,750,400)+waves(175,665,570,2))+g(3,path('M 410 1160 Q 620 1050 750 1200','#A34F3F',6,'draw'))+g(4,note(690,1070,180,125,rot=-8)))
arts.append(g(1,actor(235,1230,1.1)+actor(800,1230,1.1,'b')+path('M 355 1210 H 690 M 400 1210 V 1390 M 650 1210 V 1390',width=7))+g(2,bubble(125,570,350,210)+waves(170,630,240,2))+g(3,path('M 360 1040 Q 530 865 695 1040','#A34F3F',5,'draw'))+g(4,note(440,1040,220,155,rot=-4)))
arts.append(g(1,actor(320,1290,1.05)+actor(710,1290,1.05,'b'))+g(2,bubble(125,555,760,440,fill='#D8C8B5',stroke='#D8C8B5'))+g(3,waves(190,665,590,3))+g(4,path('M 425 1280 Q 520 1100 615 1280','#A34F3F',6,'draw')))

css='''@font-face{font-family:Newsreader;src:url("assets/board/newsreader.ttf");font-weight:400;font-display:block}@font-face{font-family:DM Sans;src:url("assets/board/dm-sans.ttf");font-weight:100 900;font-display:block}*{box-sizing:border-box}body{margin:0;background:#F3EDE3}#root{position:relative;width:100%;height:100%;overflow:hidden}.scene{position:relative;width:100%;height:100%;overflow:hidden;background:var(--bg);color:var(--ink)}.art{position:absolute;inset:0;width:100%;height:100%}.emphasis{position:absolute;left:88px;top:266px;width:848px;margin:0;font:400 108px/1.04 Newsreader,serif;letter-spacing:-.035em;color:var(--ink)}.emphasis.long{font-size:94px;max-width:800px}.caption{position:absolute;left:88px;top:1550px;width:848px;height:190px;display:flex;align-items:center;font:500 46px/1.25 'DM Sans',sans-serif;color:var(--ink)}.clip{position:absolute;inset:0}.rda-header{position:absolute;left:88px;right:144px;top:101px;height:34px;display:flex;justify-content:space-between;align-items:flex-start;font:500 26px/1.3 'DM Sans',sans-serif;letter-spacing:.095em;text-transform:uppercase;color:var(--ink);z-index:20}.rda-footer{position:absolute;left:88px;right:144px;bottom:82px;height:34px;font:400 26px/1.3 'DM Sans',sans-serif;color:var(--ink);z-index:20}'''
# Use the exact inherited chrome source; its geometry does not join choreography.
css=css[:css.index('.rda-header')]+(V/'components/chrome.css').read_text(encoding='utf-8')
css=css.replace('.scene{position:relative;width:100%;height:100%;overflow:hidden;background:var(--bg);color:var(--ink)}','')
chrome=(V/'components/chrome.html').read_text(encoding='utf-8')
beat_notes=[
['Actors face each other','Story space opens','Story ribbon travels','Solution cards interrupt the route'],
['Participants settle','Speech space expands','More story becomes visible','Connection lands beneath it'],
['Door establishes home','Speaker arrives with bag','Critiqued paper is revealed','Unfinished account opens'],
['Charcoal cut preserves actors','Speech is underway','Ribbon tries to cross','Response blocks it; hold'],
['Unfinished bubble dominates','Last sentence trails off','Solution remains available','Speaker still has more to say'],
['Listener occupies focal field','Speaker remains in view','Possible helping note appears','Question mark withholds verdict'],
['Speaker experience appears','Offered solution arrives','Received story occupies separate space','Gap remains visible'],
['Listeners stay anchored','Story is sent','Understanding path arrives','Return question closes the loop'],
['Speaker is given scale','First part of account','Second part unfolds','Final part appears; advice waits aside'],
['Tentative reply opens','Meaning is paraphrased','Question mark keeps inference open','Question returns to speaker'],
['Actors hold their identities','Correction bubble enters','Old route is tentative','Route changes to follow correction'],
['Dramatic inversion on invitation','Two routes open','Listening is available','Joint solution is available; hold'],
['Both possibilities remain visible','Path connects their timing','Choice marker can move','Connection stays open'],
['Original speaker owns the field','Request gets space','Request reaches listener','Later problem-solving remains available'],
['Shared table establishes cooperation','Story remains acknowledged','Connection settles','Solution note lands on shared table'],
['Participants share the frame','Shared speech space opens','Story is held inside it','Connecting ribbon settles; quiet hold']]

hosts=[]
for i,(f,art,notes) in enumerate(zip(S,arts,beat_notes),1):
    ident=f'f{i:02}'
    bg,ink=('#302B28','#F3EDE3') if f['dark'] else ('#F3EDE3','#302B28')
    body=f'<div id="{ident}" data-composition-id="{ident}" data-width="1080" data-height="1920" data-duration="{f["duration"]:.4f}" style="position:relative;width:100%;height:100%;overflow:hidden;background:{bg};color:{ink};--bg:{bg};--ink:{ink};--rda-meta-ink:{ink}">'
    body+=chrome.replace('{{frame_number}}',f'{i:02}').replace('{{frame_count}}','16')
    body+=f'<h1 class="emphasis {"long" if len(f["emphasis"])>20 else ""}">{html.escape(f["emphasis"])}</h1><svg class="art" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg" aria-label="{html.escape(f["purpose"])}">{art}</svg>'
    if not ANIM: body+=f'<div class="caption">{html.escape(" ".join(f["vo"].split()[:9]))}</div>'
    body+='</div>'
    # Semantic actions are distributed across the measured line, not only on entry.
    motion=''
    if ANIM:
        dur=f['duration']; fractions=[.02,.20,.44,.68]
        for j,frac in enumerate(fractions,1):
            at=round(frac*dur,4); dd=min(.78,dur*.15)
            sel=f'#{ident} .b{j}'
            if j==1:
                motion+=f'tl.fromTo("{sel}",{{opacity:.55,y:18}},{{opacity:1,y:0,duration:{dd},ease:"power2.out"}},{at});\n'
            elif (i+j)%3==0:
                motion+=f'tl.fromTo("{sel}",{{opacity:0,x:-38}},{{opacity:1,x:0,duration:{dd},ease:"power3.out"}},{at});\n'
            elif (i+j)%3==1:
                motion+=f'tl.fromTo("{sel}",{{opacity:0,y:{-80 if i==15 and j==4 else 35}}},{{opacity:1,y:0,duration:{dd},ease:"power2.out"}},{at});\n'
            else:
                motion+=f'tl.fromTo("{sel}",{{opacity:0,scale:.88,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:{dd},ease:"power3.out"}},{at});\n'
            motion+=f'document.querySelectorAll("{sel} .draw").forEach(p=>{{const len=p.getTotalLength();tl.fromTo(p,{{strokeDasharray:len,strokeDashoffset:len}},{{strokeDashoffset:0,duration:{dd+.35},ease:"power2.inOut"}},{at});}});\n'
        # Scene-specific consequential actions, not a uniform entrance sequence.
        if i==4: motion+=f'tl.fromTo("#{ident} .b3",{{opacity:1}},{{opacity:.28,duration:.35,immediateRender:false}},{dur*.84});'
        if i==9: motion+=f'tl.fromTo("#{ident} .advice-wait",{{x:0,y:0}},{{x:25,y:85,duration:.7,immediateRender:false}},{dur*.81});'
        if i==11: motion+=f'tl.fromTo("#{ident} .b3",{{opacity:1}},{{opacity:.18,duration:.5,immediateRender:false}},{dur*.72});'
        if i==13: motion+=f'tl.fromTo("#{ident} .b3",{{x:0}},{{x:440,duration:1.2,ease:"power2.inOut",immediateRender:false}},{dur*.55});'
    script=f'<script>\n(function(){{const tl=gsap.timeline({{paused:true}});\n{motion}\nwindow.__timelines["{ident}"]=tl;}})();\n</script>'
    w(V/f'compositions/frames/{ident}.html',f'<template>\n<style>{css}</style>\n{body}\n{script}\n</template>')
    hosts.append(f'<div id="host-{ident}" class="clip" data-composition-id="{ident}" data-composition-src="compositions/frames/{ident}.html" data-start="{f["start"]:.4f}" data-duration="{f["duration"]:.4f}" data-track-index="0" data-width="1080" data-height="1920"></div>')
    f['beats']=notes

duration=S[-1]['start']+S[-1]['duration']
audio=''; caps=''
if ANIM:
    meta=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'))
    voice=meta['voices'][0]['path'] if 'voices' in meta else None
    if voice is None:
        voice=meta.get('narration',{}).get('path')
    if voice is None: raise ValueError('Inspect audio_meta schema before assembly')
    if (V/'mix.json').exists(): voice=json.loads((V/'mix.json').read_text(encoding='utf-8'))['path']
    audio=f'<audio id="narration" src="{voice}" data-start="0" data-duration="{meta["total_duration_s"]}" data-track-index="2" data-volume="1"></audio>'
    cues=json.loads((V/'captions.json').read_text(encoding='utf-8'))
    for j,c in enumerate(cues):
        col='#F3EDE3' if c['dark'] else '#302B28'
        caps+=f'<div id="cap-{j}" class="clip capline" data-start="{c["start"]:.4f}" data-duration="{c["end"]-c["start"]:.4f}" data-track-index="0" style="color:{col}">{html.escape(c["text"])}</div>\n'
    capcss=css[:css.index('*{box-sizing')]+''' .capline{position:absolute;left:88px;top:1550px;right:auto;bottom:auto;width:848px;height:190px;display:flex;align-items:center;font:500 46px/1.25 'DM Sans',sans-serif}'''
    w(V/'compositions/captions.html',f'<template><style>{capcss}</style><div id="caption-root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{duration:.4f}" style="position:relative;width:100%;height:100%;background:transparent;pointer-events:none">{caps}</div><script>window.__timelines["captions"]=gsap.timeline({{paused:true}});</script></template>')
    caps=f'<div id="caption-layer" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{duration:.4f}" data-track-index="1" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:50;pointer-events:none"></div>'
w(V/'index.html',f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><title>Cerita belum selesai</title><script src="vendor/gsap.min.js"></script><style>{css}.caption-clip{{z-index:50;pointer-events:none}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{duration:.4f}">{''.join(hosts)}{caps}{audio}</div><script>const tl=gsap.timeline({{paused:true}});window.__timelines["main"]=tl;</script></body></html>''')

story='''---
format: 1080x1920
duration: 90s
message: Understand and check before offering advice
arc: recognizable interruption → room for the account → check understanding → choose support
audience: Indonesian adults in close relationships
mode: autonomous
music: none
---

## Video direction

Board v1.2 exact fonts, palette and chrome inherited. Sixteen distinct illustrated compositions with faceless organic participants. Silhouette A stays irregular, B rounder/brick; no gender or blame coding. Cream 14 frames; charcoal 04 on the story stopping and 12 on the support-choice realization. A narrow emphasis layer and full captions leave the illustrated action primary. Framing moves between relational two-shots, doorway context, large speech detail, asymmetrical receiver, return-path diagram, forked choice and shared table. No B-roll or decorative ambient loops. Registry hw-text-cloud's directed speech-space construction is adapted to the board; its handwriting, boiling and typography are omitted to preserve board identity.

Execution: agent verification under active --automation; storyboard artifacts required before synthesis. No human approval recorded. Four internal semantic beats per frame; deliberate quiet final holds. Cuts preserve actor identities; no generic transition sounds. Sources in ../SOURCES.md. Dialogue fictional. No numerical research outcome illustrated.

'''
for f in S:
    story+=f'''## Frame {f['n']} — {f['title']}

- status: {'animated' if ANIM else 'built'}
- src: compositions/frames/f{f['n']:02}.html
- duration: {f['duration']:.4f}s
- start: {f['start']:.4f}s
- end: {f['start']+f['duration']:.4f}s
- transition_in: cut
- scene: {f['purpose']}
- voiceover: "{f['vo']}"
- emphasis: "{f['emphasis']}"
- palette: {'dramatic' if f['dark'] else 'light'}
- blueprint: compose
- focal: {f['title']}
- timing_basis: {'measured native narration alignment' if ANIM else 'estimated; before synthesis'}
- poster: {f['duration']*.82:.3f}s
- narrativeRole: {'hook' if f['n']==1 else 'resolution' if f['n']>=14 else 'explanation'}
- keyMessage: {f['purpose']}
- asset_candidates: []

Starting state → {f['beats'][0]}. '''
    story+=' '.join(f'Beat {j+1} ({[.02,.2,.44,.68][j]*f["duration"]:.2f}s local): {b}.' for j,b in enumerate(f['beats']))
    story+=f' Final state: {f["beats"][-1]}; hold before the next cut. Captions update independently and do not count as action.\n\n'
    if f['dark']: story+=f'Dramatic line: "{f["vo"]}". The inversion gives the {"interruption" if f["n"]==4 else "support-choice realization"} space; chrome and captions invert together, with participant silhouette continuity.\n\n'
w(V/'STORYBOARD.md',story)
w(V/'scenes.json',json.dumps(S,ensure_ascii=False,indent=2)+'\n')
print('Built',len(S),'animated' if ANIM else 'static','frames;',round(duration,3),'seconds')
