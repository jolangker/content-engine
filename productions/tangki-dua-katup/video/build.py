from pathlib import Path
import json, html, sys, shutil
from mechanism import svg, rotated, pose
V=Path(__file__).resolve().parent
ANIM='--animate' in sys.argv
AUDIO='--audio' in sys.argv
plan=json.loads((V/('timing.json' if AUDIO else 'scene-plan.json')).read_text(encoding='utf-8'))
F=V/'compositions/frames';F.mkdir(parents=True,exist_ok=True)
(V/'vendor').mkdir(exist_ok=True)
source=V.parents[2]/'productions/rel-bukan-dua-batang-besi/video/vendor/gsap.min.js'
if not (V/'vendor/gsap.min.js').exists():shutil.copy2(source,V/'vendor/gsap.min.js')
E=html.escape
def state(**kw):return dict(water=1,flapAngle=0,leverAngle=0,exterior=0,lidY=-58,fill=0,flush=0,refill=0,overflow=0,**kw)
# Key poses are normalized positions within each shot. Successive shots preserve
# state unless the shot explicitly replays or changes to a labeled fault example.
poses=[
[(0,dict(exterior=1,lidY=0)),(.35,dict(exterior=.08,lidY=-58)),(.7,dict(leverAngle=-14,flapAngle=48,flush=1,water=.8)),(1,dict(leverAngle=0,flapAngle=48,water=.65,flush=1))],
[(0,dict(exterior=.8,lidY=0)),(.45,dict(exterior=.035,lidY=-70)),(1,dict(exterior=.035,lidY=-70))],
[(0,{}),(.45,{}),(1,{})],
[(0,{}),(.2,{}),(.65,dict(leverAngle=-5,flapAngle=13)),(1,dict(leverAngle=-5,flapAngle=13))],
[(0,dict(leverAngle=-5,flapAngle=13)),(.2,dict(leverAngle=-5,flapAngle=13)),(.66,dict(leverAngle=-14,flapAngle=48,flush=1)),(1,dict(leverAngle=-14,flapAngle=48,flush=1,water=.97))],
[(0,dict(leverAngle=-14,flapAngle=48,flush=1,water=.97)),(.85,dict(leverAngle=-14,flapAngle=48,flush=1,water=.7)),(1,dict(leverAngle=-14,flapAngle=48,flush=1,water=.7))],
[(0,dict(leverAngle=-14,flapAngle=48,flush=1,water=.7)),(.3,dict(leverAngle=0,flapAngle=48,flush=1,water=.67)),(1,dict(flapAngle=48,flush=1,water=.5))],
[(0,dict(flapAngle=48,flush=1,water=.5)),(.65,dict(flapAngle=48,flush=1,fill=1,refill=1,water=.28)),(1,dict(flapAngle=48,flush=1,fill=1,refill=1,water=.22))],
[(0,dict(flapAngle=48,flush=1,fill=1,refill=1,water=.22)),(.85,dict(flapAngle=35,flush=1,fill=1,refill=1,water=.08)),(1,dict(flapAngle=35,flush=1,fill=1,refill=1,water=.08))],
[(0,dict(flapAngle=35,flush=1,fill=1,refill=1,water=.08)),(.58,dict(flapAngle=0,flush=0,fill=1,refill=1,water=.08)),(1,dict(fill=1,refill=1,water=.16))],
[(0,dict(fill=1,refill=1,water=.16)),(.88,dict(fill=1,refill=1,water=.8)),(1,dict(fill=1,refill=1,water=.8))],
[(0,dict(fill=1,refill=1,water=.8)),(.65,dict(fill=1,refill=1,water=1)),(.75,dict(water=1)),(1,dict(water=1))],
[(0,dict(fill=1,refill=1,water=.6)),(.15,dict(fill=1,refill=1,water=.62)),(.85,dict(fill=1,refill=1,water=.83)),(1,dict(fill=1,refill=1,water=.86))],
[(0,dict(fill=1,water=1)),(.45,dict(fill=1,water=1.18)),(.55,dict(fill=1,overflow=1,water=1.18)),(1,dict(fill=1,overflow=1,water=1.18))],
[(0,{}),(.14,dict(leverAngle=-14,flapAngle=48,flush=1,water=.95)),(.4,dict(flapAngle=48,flush=1,fill=1,refill=1,water=.1)),(.54,dict(fill=1,refill=1,water=.1)),(.88,dict(fill=1,refill=1,water=1)),(.96,{}),(1,{})],
[(0,{}),(.45,{}),(.8,dict(exterior=.55,lidY=0)),(1,dict(exterior=.55,lidY=0))],
]
def complete(p):
    z=dict(water=1,flapAngle=0,leverAngle=0,exterior=0,lidY=-58,fill=0,flush=0,refill=0,overflow=0);z.update(p);return z
def caption_html():
    if not AUDIO:return ''
    groups=json.loads((V/'caption_groups.json').read_text(encoding='utf-8'))
    return '\n'.join(f'<div id="cap-{i:03d}" class="clip caption" data-start="{g["start"]}" data-duration="{g["end"]-g["start"]:.5f}" data-track-index="2"><span>{E(g["text"])}</span></div>' for i,g in enumerate(groups))
def label_svg(view,sid,st):
    d={
      'tank':[(360,555,285,475,'katup isi'),(465,720,565,797,'katup buang')],
      'lever':[(250,420,155,300,'poros'),(545,565,535,440,'rantai')],
      'flapper':[(423,664,*rotated((568,789),(650,795),st['flapAngle']),'flapper'),(425,912,550,820,'dudukan')],
      'float':[(360,590,315,430+pose(**st)['floatY'],'pelampung')],
      'fill':[(350,755,315,650,'air masuk')],
      'refill':[(350,430,450,286,'selang kecil'),(450,650,645,510,'pipa limpasan')],
      'overflow':[(433,520,640,360,'limpasan')],
    }.get(view,[])
    return ''.join(f'<g class="part-label"><path id="{sid}-lead-{txt.replace(" ","-")}" d="M{x} {y+10} L{tx} {ty}" fill="none" stroke="#536775" stroke-width="1.6"/><circle id="{sid}-dot-{txt.replace(" ","-")}" cx="{tx}" cy="{ty}" r="4" fill="#2459C4"/><text x="{x}" y="{y}" fill="#172B3B" font-family="Manrope" font-size="25" font-weight="600">{txt}</text></g>' for x,y,tx,ty,txt in d)
def write_storyboard():
    out='---\nformat: 1080x1920\nduration: 90s\nmode: autonomous\nflow: automation\nstoryboard: no\nmusic: none\nmessage: Two valves coordinate one tank cycle\n---\n\n# Video direction\n\nBoard Di Balik Benda v4. Shaded 2.5D SVG throughout. Orange input, blue active part, teal flow. Camera crops preserve shared landmarks. Timings '+('measured against full narration' if AUDIO else 'are estimated before synthesis')+'. Caption keep-out y1600–1800; all meaningful scene content stays above y1580. Agent verification replaces human layout approval. Static storyboard artifacts are mandatory.\n\nNormal chronology includes overlapping drainage and refill. Shots 2–3 are an anatomy reset after opening teaser; shot13 is a labeled alternate inspection of refill, shot14 a labeled fault example, shot15 an explicitly announced replay. Time slowed for inspection and compressed for refill; not a dimensional simulation.\n\n'
    for i,s in enumerate(plan):
        a=s['action'];p=poses[i]
        out+=f"## Frame {i+1} — {s['title']} ({s['start']:.3f}–{s['end']:.3f}s)\n\n- status: {'animated' if ANIM else 'built'}\n- src: compositions/frames/{s['id']}.html\n- duration: {s['duration']:.5f}s\n- transition_in: cut\n- scene: {s['sub']}\n- voiceover: {s['vo']}\n- poster: {s['duration']*.62:.3f}s\n- blueprint: compose\n- focal: shaded 2.5D {s['view']} view of the same cistern\n- rules: causal state interpolation, anchored emphasis, svg-path-draw\n\nPurpose: {s['title']}. New information: {s['sub']}.\n\nScene 1 (0–{s['duration']*.2:.2f}s): Orient to {s['view']}; preserve state and cue the active part. Scene 2 ({s['duration']*.2:.2f}–{s['duration']*.75:.2f}s): Input → contact or flow transfer → dependent response, action `{a}`. Scene 3 ({s['duration']*.75:.2f}–{s['duration']:.2f}s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.\n\nDiagnostic poses (normalized shot time): `{json.dumps(p,ensure_ascii=False)}`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.\n\n"
    (V/'STORYBOARD.md').write_text(out,encoding='utf-8')
for i,s in enumerate(plan):
    sid=s['id'];dur=s['duration'];ps=poses[i];initial=complete(ps[0][1]);poster=complete(ps[min(len(ps)-1,2)][1])
    drawing=svg(s['view'],initial if ANIM else poster,sid)
    drawing=drawing.replace('</svg>',label_svg(s['view'],sid,initial if ANIM else poster)+'</svg>')
    tag=''
    if i==0:tag='TIPE TUAS + FLAPPER'
    if i==12:tag='INSPEKSI JALUR ISI'
    if i==13:tag='CONTOH KONDISI ABNORMAL'
    if i==14:tag='ULANG SIKLUS · WAKTU DIPADATKAN'
    script=''
    if ANIM:
        # Every state is derived from an explicit GSAP proxy, no accumulated offsets.
        keys=json.dumps([(t*dur,complete(p)) for t,p in ps])
        script=f'''const pfx="{sid}", dur={dur}, keys={keys}, obj={{...keys[0][1]}};
const el=n=>document.getElementById(pfx+'-'+n);
function rot(x,y,px,py,a){{let r=a*Math.PI/180;return [px+(x-px)*Math.cos(r)-(y-py)*Math.sin(r),py+(x-px)*Math.sin(r)+(y-py)*Math.cos(r)];}}
function draw(){{
 let dy=(1-obj.water)*365; el('water').setAttribute('transform',`translate(0 ${{dy}})`);
 el('float').setAttribute('transform',`translate(0 ${{Math.min(332,Math.max(-45,dy))}})`);
 el('flapper').setAttribute('transform',`rotate(${{obj.flapAngle}} 650 795)`);
 el('lever').setAttribute('transform',`rotate(${{obj.leverAngle}} 155 300)`);
 let a=rot(535,300,155,300,obj.leverAngle),b=rot(525,778,650,795,obj.flapAngle),dx=b[0]-a[0],dyc=b[1]-a[1],dist=Math.hypot(dx,dyc),nx=-dyc/dist,ny=dx/dist;
 const curve=bow=>{{let cx=(a[0]+b[0])/2+nx*bow,cy=(a[1]+b[1])/2+ny*bow,px=a[0],py=a[1],len=0;for(let j=1;j<=20;j++){{let t=j/20,u=1-t,x=u*u*a[0]+2*u*t*cx+t*t*b[0],y=u*u*a[1]+2*u*t*cy+t*t*b[1];len+=Math.hypot(x-px,y-py);px=x;py=y;}}return [len,cx,cy];}};
 let lo=0,hi=980;for(let j=0;j<18;j++){{let mid=(lo+hi)/2;if(curve(mid)[0]<490)lo=mid;else hi=mid;}}let c=curve((lo+hi)/2);
 let d=`M ${{a[0]}} ${{a[1]}} Q ${{c[1]}} ${{c[2]}} ${{b[0]}} ${{b[1]}}`;
 el('chain').setAttribute('d',d);el('chain-shadow').setAttribute('d',d);
 el('tank-front').setAttribute('opacity',obj.exterior);el('lid').setAttribute('transform',`translate(0 ${{obj.lidY}})`);
 for(let n of ['fill','flush','refill','overflow'])el(n+'-flow').setAttribute('opacity',obj[n]);
 if(el('lead-pelampung')){{let y=430+Math.min(332,Math.max(-45,dy));el('lead-pelampung').setAttribute('d',`M360 600 L315 ${{y}}`);el('dot-pelampung').setAttribute('cy',y);}}
 if(el('lead-flapper')){{let a=rot(568,789,650,795,obj.flapAngle);el('lead-flapper').setAttribute('d',`M423 674 L${{a[0]}} ${{a[1]}}`);el('dot-flapper').setAttribute('cx',a[0]);el('dot-flapper').setAttribute('cy',a[1]);}}
}}
draw();
for(let k=1;k<keys.length;k++)tl.fromTo(obj,keys[k-1][1],{{...keys[k][1],duration:keys[k][0]-keys[k-1][0],ease:'none',immediateRender:false,onUpdate:draw}},keys[k-1][0]);
tl.fromTo('#{sid}-headline',{{y:16,opacity:.6}},{{y:0,opacity:1,duration:.45,ease:'power2.out'}},0);
tl.fromTo('#{sid}-detail',{{opacity:.35}},{{opacity:1,duration:.55}},Math.min(1,dur*.18));
const labels=document.querySelectorAll('#{sid}-visual .part-label');if(labels.length)tl.fromTo(labels,{{opacity:0}},{{opacity:1,duration:.35,stagger:.4}},dur*.25);
tl.fromTo('#{sid}-visual .flow-path,#{sid}-visual .supply-path,#{sid}-visual .hose-flow',{{strokeDashoffset:0}},{{strokeDashoffset:-130,duration:dur,ease:'none'}},0);
'''
        if i==2:
            script+=f"tl.fromTo('#{sid}-flapper',{{opacity:.3}},{{opacity:1,duration:.35}},{dur*.2});tl.fromTo('#{sid}-fill-assembly',{{opacity:.3}},{{opacity:1,duration:.35}},{dur*.6});"
    styles=f'''#{sid}{{position:absolute;inset:0;color:#172B3B;font-family:Manrope,sans-serif}} #{sid} .ground{{background:#ECEEE9}} #{sid} .brand{{position:absolute;left:72px;top:100px;font-family:Plex,monospace;font-size:28px;letter-spacing:3px;color:#536775}} #{sid} h1{{position:absolute;left:72px;top:173px;margin:0;width:920px;font-size:76px;line-height:1.1;font-weight:800;letter-spacing:-3.6px}} #{sid} .visual{{position:absolute;left:35px;top:420px;width:1010px;height:950px;overflow:hidden}} #{sid} svg{{width:100%;height:100%;overflow:hidden}} #{sid} .detail{{position:absolute;left:72px;top:1420px;width:920px;font-size:44px;line-height:1.2;font-weight:600}} #{sid} .tag{{position:absolute;left:72px;top:1530px;font-family:Plex,monospace;font-size:28px;letter-spacing:.2px;color:#536775}}'''
    fontcss="@font-face{font-family:Manrope;src:url('../../assets/fonts/manrope.ttf')}@font-face{font-family:Plex;src:url('../../assets/fonts/ibm-plex-mono.ttf')}"
    content=f'''<template><style>{fontcss}{styles}</style><div id="{sid}" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{dur:.5f}"><div id="{sid}-ground" class="clip ground" data-start="0" data-duration="{dur:.5f}" data-track-index="0" style="position:absolute;inset:0"></div><div class="brand">DI BALIK BENDA</div><h1 id="{sid}-headline">{E(s['title'])}</h1><div id="{sid}-visual" class="visual">{drawing}</div><div id="{sid}-detail" class="detail">{E(s['sub'])}</div><div class="tag">{E(tag or 'POTONGAN ILUSTRATIF · GERAK DIPERLAMBAT')}</div></div><script>{{const tl=gsap.timeline({{paused:true}});{script}window.__timelines["{sid}"]=tl;}}</script></template>'''
    (F/f'{sid}.html').write_text(content,encoding='utf-8')
mounts='\n'.join(f'<div id="slot-{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/frames/{s["id"]}.html" data-start="{s["start"]:.5f}" data-duration="{s["duration"]:.5f}" data-track-index="1" data-width="1080" data-height="1920"></div>' for s in plan)
audio=''
if AUDIO:
    meta=json.loads((V/'placed_audio.json').read_text(encoding='utf-8'))
    audio=f'<audio id="narration" src="{meta["path"]}" data-start="{meta["offset"]}" data-duration="{meta["duration"]:.5f}" data-volume="0.9" data-track-index="3"></audio>'
root=f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><title>Tangki dua katup</title><script src="vendor/gsap.min.js"></script><style>@font-face{{font-family:Manrope;src:url('assets/fonts/manrope.ttf')}}@font-face{{font-family:Plex;src:url('assets/fonts/ibm-plex-mono.ttf')}}*{{box-sizing:border-box}}html,body{{margin:0;width:100%;height:100%;background:#ECEEE9}}#root{{position:relative;width:100%;height:100%;overflow:hidden;background:#ECEEE9}}.clip{{position:absolute;inset:0}}.caption{{display:flex;align-items:flex-start;justify-content:center;padding:1625px 100px 0;font-family:Manrope,sans-serif;font-size:49px;line-height:1.26;font-weight:700;text-align:center;color:#F8F9F5;z-index:30}}.caption span{{background:#172B3B;padding:15px 27px 21px;border-radius:13px;max-width:880px}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="90" data-fps="30">{mounts}{caption_html()}{audio}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines['main']=gsap.timeline({{paused:true}});</script></body></html>'''
(V/'index.html').write_text(root,encoding='utf-8')
write_storyboard()
print(json.dumps({'animated':ANIM,'audio':AUDIO,'scenes':len(plan),'duration':90}))
