from pathlib import Path
import html, json, sys, shutil
V=Path(__file__).resolve().parent/'video'
S=json.loads((V/'scenes.json').read_text(encoding='utf-8'))
ANIM='--animate' in sys.argv
def w(p,s): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def g(n,body,extra=''): return f'<g class="beat b{n}" {extra}>{body}</g>'
def path(d,c='var(--ink)',sw=5,cls='draw'):
    return f'<path class="{cls}" d="{d}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
def actor(x,y,s=1,who='a'):
    d='M -83 -107 C -140 -66 -120 60 -63 102 C 6 149 99 82 102 2 C 106 -84 1 -143 -83 -107 Z' if who=='a' else 'M -67 -88 C -112 -52 -103 42 -47 84 C 13 130 93 59 89 -4 C 85 -66 3 -119 -67 -88 Z'
    return f'<g transform="translate({x} {y}) scale({s})"><path d="{d}" fill="'+('var(--ink)' if who=='a' else '#A34F3F')+'"/></g>'
def bubble(x,y,ww,hh,side='left'):
    # Directed speech space adapted from registry hw-text-cloud, without its boil/type skin.
    tail=f'L {ww*.22} {hh} L {ww*.12} {hh+60} L {ww*.14} {hh}' if side=='left' else f'L {ww*.85} {hh} L {ww*.92} {hh+60} L {ww*.72} {hh}'
    return f'<g transform="translate({x} {y})"><path d="M 35 0 H {ww-35} Q {ww} 0 {ww} 35 V {hh-35} Q {ww} {hh} {ww-35} {hh} {tail} H 35 Q 0 {hh} 0 {hh-35} V 35 Q 0 0 35 0 Z" fill="var(--bg)" stroke="#D8C8B5" stroke-width="5"/></g>'
def waves(x,y,ww=320,rows=2,c='#A34F3F'):
    return ''.join(path(f'M {x} {y+j*42} C {x+ww*.3} {y-28+j*42} {x+ww*.6} {y+30+j*42} {x+ww} {y+j*42}',c) for j in range(rows))
def txt(x,y,s,size=48,c='var(--ink)'):
    return f'<text x="{x}" y="{y}" font-family="DM Sans" font-size="{size}" fill="{c}">{html.escape(s)}</text>'
def dot(x,y,r=12,c='#A34F3F'):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def card(x,y,ww=230,hh=170,rot=0,mark=False):
    return f'<g transform="translate({x} {y}) rotate({rot})"><rect width="{ww}" height="{hh}" rx="12" fill="#D8C8B5"/>'+path(f'M 30 45 H {ww-30} M 30 79 H {ww-60}','#302B28',5,'')+(path(f'M 30 {hh-35} Q {ww/2} {hh-65} {ww-30} {hh-35}','#A34F3F',6,'') if mark else '')+'</g>'
def clock(x,y,r=150,hand=True):
    lines=''.join(path(f'M {x+dx*(r-15)} {y+dy*(r-15)} L {x+dx*(r-32)} {y+dy*(r-32)}','var(--ink)',5,'') for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)])
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="var(--bg)" stroke="#D8C8B5" stroke-width="7"/>'+lines+(path(f'M {x} {y-r*.52} V {y} L {x-r*.43} {y+r*.25}','var(--ink)',7,'') if hand else '')
def table(y=1190): return path(f'M 335 {y} H 720 M 390 {y} V {y+210} M 665 {y} V {y+210}','var(--ink)',7,'')
def pause(x,y,s=1):
    return f'<g transform="translate({x} {y}) scale({s})"><rect x="-43" y="-65" width="25" height="130" rx="8" fill="#A34F3F"/><rect x="18" y="-65" width="25" height="130" rx="8" fill="#A34F3F"/></g>'
def appointment(x,y,ww=380,hh=350):
    return f'<g transform="translate({x} {y})"><rect width="{ww}" height="{hh}" rx="20" fill="var(--bg)" stroke="#D8C8B5" stroke-width="7"/>'+path(f'M 0 80 H {ww} M 75 -20 V 30 M {ww-75} -20 V 30','var(--ink)',7,'')+'</g>'

A=[]
A.append(g(1,actor(245,1230,1.2)+actor(800,1240,1.15,'b')+bubble(125,560,470,270)) +g(2,waves(170,630,340)+path('M 365 1110 Q 495 1000 590 1020','#A34F3F'))+g(3,clock(760,780,135,False))+g(4,txt(705,825,'?',115)+dot(600,1020)))
A.append(g(1,actor(260,1250,1.2)+actor(780,1250,1.2,'b')+path('M 370 1220 Q 520 1120 680 1220','#D8C8B5'))+g(2,pause(520,720,1.5))+g(3,clock(520,1020,125))+g(4,path('M 370 1270 C 440 1420 630 1420 680 1270','#A34F3F')+dot(520,1370)))
A.append(g(1,actor(235,1220,1.08)+actor(815,1220,1.08,'b')+table()+card(380,800,290,225,-5))+g(2,card(490,920,275,195,6,True))+g(3,bubble(120,555,390,190)+waves(155,610,280,2))+g(4,bubble(640,590,250,150,'right')+waves(675,645,175,1)))
A.append(g(1,table()+actor(250,1235,1.15)+card(420,1010,240,170,0,True))+g(2,actor(705,1180,1.18,'b'))+g(3,path('M 365 1195 Q 535 875 690 1065','#D8C8B5')+bubble(130,580,460,245)+waves(175,660,330,2,'#D8C8B5'))+g(4,txt(640,790,'?',145,'var(--ink)')))
A.append(g(1,actor(250,1140,1.55)+actor(800,1140,1.3,'b'))+g(2,path('M 120 930 Q 245 800 400 930','#D8C8B5')+pause(245,720,.9))+g(3,bubble(600,570,300,240,'right')+txt(705,745,'?',120))+g(4,path('M 450 690 V 1350','#D8C8B5',4)))
A.append(g(1,actor(235,1290,.9)+path('M 390 1260 Q 585 1230 750 1320','#D8C8B5'))+g(2,txt(600,820,'?',240))+g(3,card(155,620,300,210,-6))+g(4,bubble(390,1000,480,240)+waves(440,1080,365,2)))
A.append(g(1,actor(245,1250,1.12)+actor(800,1250,1.12,'b')+table()+card(415,1015,245,175))+g(2,pause(320,700,1.0))+g(3,clock(745,740,125))+g(4,path('M 350 1170 Q 490 920 540 1050 M 700 1170 Q 620 970 540 1050','#A34F3F')+dot(540,1050)))
A.append(g(1,actor(310,1170,1.7)+actor(830,1350,.65,'b'))+g(2,waves(180,1110,260,2,'#D8C8B5'))+g(3,bubble(130,565,650,320)+waves(180,660,490,2))+g(4,path('M 510 1080 Q 695 1015 825 1245','#A34F3F')))
A.append(g(1,clock(530,960,280,False))+g(2,path('M 180 1350 Q 120 960 270 960','#A34F3F')+actor(205,1330,.8))+g(3,txt(365,990,'20:00',108)+path('M 530 740 V 780','#A34F3F',12))+g(4,actor(820,1310,.9,'b')+path('M 760 1260 Q 900 970 815 960','#A34F3F')+dot(815,960)))
A.append(g(1,appointment(200,575,640,600))+g(2,'<rect x="280" y="780" width="480" height="130" rx="12" fill="#D8C8B5"/>'+txt(360,865,'20:00',86))+g(3,actor(215,1320,1.02)+actor(820,1320,1.02,'b')+dot(680,1020,25))+g(4,path('M 320 1250 Q 390 1030 520 1060 M 730 1250 Q 640 1070 520 1060','#A34F3F')+dot(520,1060,16)))
A.append(g(1,'<rect x="520" y="570" width="370" height="500" rx="8" fill="#D8C8B5"/>'+path('M 705 570 V 1070 M 520 825 H 890','var(--ink)',6,'')+actor(330,1200,1.5)+path('M 165 1370 H 490 M 190 1370 V 1460 M 460 1370 V 1460','var(--ink)',7,''))+g(2,card(175,620,215,160,-8))+g(3,path('M 180 1000 Q 340 900 480 1000','#D8C8B5'))+g(4,'<path d="M 735 1280 H 875 L 852 1420 H 760 Z" fill="#D8C8B5"/>'+path('M 805 1280 V 1105 M 805 1200 Q 730 1135 760 1090 M 805 1170 Q 880 1100 855 1075','#A34F3F',7,'')+path('M 535 1350 H 625 V 1420 H 535 Z M 625 1370 Q 670 1360 650 1400 H 625','var(--ink)',6,'')))
A.append(g(1,table()+actor(250,1240,1.1)+card(425,1020,235,170,0,True))+g(2,actor(850,1190,1.15,'b'))+g(3,bubble(130,590,370,220)+waves(170,665,265,2,'#D8C8B5'))+g(4,path('M 360 1220 Q 535 930 705 1220','#D8C8B5')+dot(535,1075,15,'#D8C8B5')))
A.append(g(1,appointment(515,620,345,310)+txt(565,825,'20:00',69))+g(2,actor(235,1270,1.13)+actor(800,1280,1.1,'b')+bubble(120,580,320,225)+waves(155,645,235,2))+g(3,dot(680,1010,25)+path('M 680 1010 Q 600 1115 520 1070','#A34F3F'))+g(4,path('M 345 1220 Q 440 1040 520 1070 M 705 1220 Q 660 1110 520 1070','#A34F3F')+dot(520,1070,16)))
A.append(g(1,card(380,850,320,240,-4,True))+g(2,actor(220,1240,1.1)+actor(830,1240,1.1,'b')+table())+g(3,bubble(125,565,400,220)+waves(165,640,280,2))+g(4,path('M 340 1210 Q 510 1120 710 1210','#A34F3F')+dot(530,1172)))
A.append(g(1,card(180,630,260,195,-6,True))+g(2,card(390,775,260,195,3,True)+card(590,925,260,195,-4,True))+g(3,actor(235,1310,1.0)+actor(810,1320,1.0,'b')+path('M 335 1240 Q 510 1100 705 1240','#A34F3F'))+g(4,bubble(150,1120,700,135)+waves(205,1182,565,1)))
A.append(g(1,actor(310,1280,1.1)+actor(735,1280,1.1,'b')+card(400,1040,235,170,0,True))+g(2,clock(305,740,140))+g(3,bubble(575,590,310,240,'right')+dot(730,710,22))+g(4,path('M 305 895 Q 510 1060 730 895 M 420 1260 Q 525 1170 630 1260','#A34F3F')+dot(520,975,13)))

css='''@font-face{font-family:Newsreader;src:url("assets/board/newsreader.ttf");font-weight:400;font-display:block}@font-face{font-family:DM Sans;src:url("assets/board/dm-sans.ttf");font-weight:100 900;font-display:block}*{box-sizing:border-box}body{margin:0;background:#F3EDE3}#root{position:relative;width:100%;height:100%;overflow:hidden}.art{position:absolute;inset:0;width:100%;height:100%}.emphasis{position:absolute;left:88px;top:266px;width:848px;margin:0;font:400 108px/1.04 Newsreader,serif;letter-spacing:-.035em;color:var(--ink)}.emphasis.long{font-size:91px}.caption{position:absolute;left:88px;top:1550px;width:848px;height:190px;display:flex;align-items:center;font:500 46px/1.25 'DM Sans',sans-serif;color:var(--ink)}.clip{position:absolute;inset:0}'''+(V/'components/chrome.css').read_text(encoding='utf-8')
chrome=(V/'components/chrome.html').read_text(encoding='utf-8')
hosts=[]
for s,art in zip(S,A):
    i=s['n']; ident=f'f{i:02}';dur=s['duration'];bg,ink=('#302B28','#F3EDE3') if s['dark'] else ('#F3EDE3','#302B28')
    if not ANIM:
        landed={4:(2,'translate(115 0)',''),6:(3,'translate(-25 55)',''),11:(2,'translate(-45 -15)','opacity=".4"'),12:(2,'translate(-100 0)',''),13:(3,'translate(0 60)',''),14:(1,'translate(0 45)','')}
        if i in landed:
            group,transform,extra=landed[i];art=art.replace(f'class="beat b{group}"',f'class="beat b{group}" transform="{transform}" {extra}')
    body=f'<div id="{ident}" data-composition-id="{ident}" data-width="1080" data-height="1920" data-duration="{dur:.4f}" style="position:relative;width:100%;height:100%;overflow:hidden;--bg:{bg};--ink:{ink};--rda-meta-ink:{ink}"><div id="{ident}-background" class="clip" data-start="0" data-duration="{dur:.4f}" data-track-index="0" style="background:{bg};pointer-events:none"></div>'
    body+=chrome.replace('{{frame_number}}',f'{i:02}').replace('{{frame_count}}','16')
    body+=f'<h1 class="emphasis {"long" if len(s["emphasis"])>20 else ""}">{html.escape(s["emphasis"])}</h1><svg class="art" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg" aria-label="{html.escape(s["purpose"])}">{art}</svg>'
    if not ANIM:body+=f'<div class="caption">{html.escape(" ".join(s["vo"].split()[:9]))}</div>'
    body+='</div>'
    motion=''
    if ANIM:
        for j,frac in enumerate([.02,.22,.45,.68],1):
            at=round(frac*dur,4);dd=min(.85,dur*.16);sel=f'#{ident} .b{j}'
            if j==1: fr='opacity:.65,y:12';to='opacity:1,y:0'
            elif (i,j)==(4,2):fr='opacity:1,x:-130';to='opacity:1,x:115'
            elif (i,j)==(12,2):fr='opacity:1,x:65';to='opacity:1,x:-100'
            elif (i+j)%3==0:fr='opacity:0,x:-38';to='opacity:1,x:0'
            elif (i+j)%3==1:fr='opacity:0,y:35';to='opacity:1,y:0'
            else:fr='opacity:0,scale:.9,transformOrigin:"50% 50%"';to='opacity:1,scale:1'
            motion+=f'tl.fromTo("{sel}",{{{fr}}},{{{to},duration:{dd},ease:"power2.out"}},{at});\n'
            motion+=f'document.querySelectorAll("{sel} .draw").forEach(p=>{{const len=p.getTotalLength();tl.fromTo(p,{{strokeDasharray:len,strokeDashoffset:len}},{{strokeDashoffset:0,duration:{dd+.25},ease:"power2.inOut"}},{at});}});\n'
        if i==6:motion+=f'tl.fromTo("#f06 .b3",{{x:0,y:0}},{{x:-25,y:55,duration:.8,immediateRender:false}},{dur*.72});'
        if i==11:motion+=f'tl.fromTo("#f11 .b2",{{x:0,y:0}},{{x:-45,y:-15,opacity:.4,duration:.9,immediateRender:false}},{dur*.6});'
        if i==13:motion+=f'tl.fromTo("#f13 .b3",{{y:0}},{{y:60,duration:.8,immediateRender:false}},{dur*.72});'
        if i==14:motion+=f'tl.fromTo("#f14 .b1",{{y:0}},{{y:45,duration:.85,immediateRender:false}},{dur*.72});'
    script=f'<script>(function(){{const tl=gsap.timeline({{paused:true}});{motion}\nwindow.__timelines["{ident}"]=tl;}})();</script>'
    w(V/f'compositions/frames/{ident}.html',f'<template><style>{css}</style>{body}{script}</template>')
    hosts.append(f'<div id="host-{ident}" class="clip" data-composition-id="{ident}" data-composition-src="compositions/frames/{ident}.html" data-start="{s["start"]:.4f}" data-duration="{dur:.4f}" data-track-index="0" data-width="1080" data-height="1920"></div>')
duration=S[-1]['start']+S[-1]['duration'];audio='';caps=''
if ANIM:
    meta=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'));voice=meta['voices'][0]['path']
    if (V/'mix.json').exists():voice=json.loads((V/'mix.json').read_text())['path']
    placed_duration=json.loads((V/'mix.json').read_text())['duration_s']
    audio=f'<audio id="narration" src="{voice}" data-start="0" data-duration="{placed_duration}" data-track-index="2" data-volume="1"></audio>'
    cues=json.loads((V/'captions.json').read_text());caplines=''
    for j,c in enumerate(cues):
        col='#F3EDE3' if c['dark'] else '#302B28'
        caplines+=f'<div id="cap-{j}" class="clip capline" data-start="{c["start"]:.4f}" data-duration="{c["end"]-c["start"]:.4f}" data-track-index="0" style="color:{col}">{html.escape(c["text"])}</div>'
    capcss=css[:css.index('*{box-sizing')]+".capline{position:absolute;left:88px;top:1550px;right:auto;bottom:auto;width:848px;height:190px;display:flex;align-items:center;font:500 46px/1.25 'DM Sans',sans-serif}"
    w(V/'compositions/captions.html',f'<template><style>{capcss}</style><div id="caption-root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{duration:.4f}" style="position:relative;width:100%;height:100%;background:transparent;pointer-events:none">{caplines}</div><script>window.__timelines["captions"]=gsap.timeline({{paused:true}});</script></template>')
    caps=f'<div id="caption-layer" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{duration:.4f}" data-track-index="1" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:50;pointer-events:none"></div>'
w(V/'index.html',f'<!doctype html><html lang="id"><head><meta charset="utf-8"><title>Jeda punya waktu kembali</title><script src="vendor/gsap.min.js"></script><style>{css}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{duration:.4f}">{"".join(hosts)}{caps}{audio}</div><script>const tl=gsap.timeline({{paused:true}});window.__timelines["main"]=tl;</script></body></html>')
story='''---
format: 1080x1920
duration: 90s
message: A pause needs a shared return plan and actual follow-through
arc: story-explainer with how-to
audience: Indonesian adults in close relationships
mode: autonomous
music: none
---

## Video direction

Board v1.2 exact local fonts, palette and stationary chrome. Sixteen illustrated compositions; cream fourteen, charcoal 04 (unfinished conversation) and 12 (return in action). Irregular silhouette A and rounder brick silhouette B preserve identity through inversions, with no gender or blame coding. The same changed-plan card links conflict, pause and return. Vary two-shots, asymmetrical close-ups, speech space, clock detail, appointment, calming window and shared table. Selective short emphasis, no support paragraphs, full captions in their own band. No B-roll, decorative loops or generic transition sounds. Directed speech-space construction adapted from registry hw-text-cloud; board typography/flat geometry override handwriting and boil.

The static board is required before synthesis under shortform-production. Agent verification under --automation replaces human layout review. No human approval recorded. Four semantic developments per scene, distributed across its duration; captions do not count. Cuts preserve the established actors/props. No effect is needed merely for the two palette changes. Source bounds: ../SOURCES.md; 20:00 is a fictional appointment, not a prescribed interval.

'''
for s in S:
    n=s['n'];start=s['start'];dur=s['duration'];role='hook' if n==1 else 'resolution' if n>=14 else 'explanation'
    story+=f'''## Frame {n} — {s['title']}

- status: {'animated' if ANIM else 'built'}
- src: compositions/frames/f{n:02}.html
- duration: {dur:.4f}s
- start: {start:.4f}s
- end: {start+dur:.4f}s
- transition_in: cut
- scene: {s['purpose']}
- voiceover: "{s['vo']}"
- emphasis: "{s['emphasis']}"
- palette: {'dramatic' if s['dark'] else 'light'}
- type: {'hook' if n==1 else 'benefit_highlight' if n>=12 else 'feature_showcase'}
- persuasion: concrete fictional example
- beat: {'uncertainty' if n<7 else 'understanding'}
- blueprint: compose
- focal: {s['title']}
- asset_candidates: []
- timing_basis: {'measured continuous narration alignment' if ANIM else 'estimated before synthesis'}
- poster: {dur*.85:.3f}s

narrativeRole: {role}: {s['purpose']}
keyMessage: {s['purpose']}
Starting state: {s['beats'][0]}. '''
    story+=' '.join(f'Scene {j+1} ({[.02,.22,.45,.68][j]*dur:.2f}s local): {beat}.' for j,beat in enumerate(s['beats']))
    story+=f' Final state: {s["beats"][-1]}. Continuity: retain the actors and topic, carrying the action into the next composition. Final quiet hold is intentional.\n\n'
    if s['dark']:story+=f'Dramatic line: “{s["vo"]}” — {"The departure leaves an unfinished issue visible" if n==4 else "The return makes the agreement visible in action"}. Invert background, captions and stationary chrome together; keep participant silhouette continuity.\n\n'
w(V/'STORYBOARD.md',story)
print(json.dumps(dict(frames=len(S),duration=duration,animated=ANIM)))
