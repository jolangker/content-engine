"""Build original layered 2.5D inspection shots; static poses precede animation."""
from pathlib import Path
import json,math,html,sys
V=Path(__file__).resolve().parent; animated='--animate' in sys.argv
plan=json.loads((V/('timing.json' if animated else 'scene-plan.json')).read_text(encoding='utf-8'))
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def esc(s):return html.escape(str(s),quote=True)
CSS="""@font-face{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:200 800}@font-face{font-family:'IBM Plex Mono';src:url('assets/fonts/ibm-plex-mono.ttf')}*{box-sizing:border-box}#root{position:absolute;inset:0;font-family:Manrope,sans-serif;color:#172B3B}.scene{position:absolute;inset:0;background:#ECEEE9}.title{position:absolute;left:108px;top:205px;width:790px;margin:0;font-size:74px;line-height:1.09;font-weight:800;letter-spacing:-3px}.stage{position:absolute;left:83px;top:425px;width:850px;height:665px}.stage svg{width:100%;height:100%}.note{position:absolute;left:108px;top:1100px;width:780px;font:28px/1.35 'IBM Plex Mono',monospace;color:#536775}svg .edge{stroke:#172B3B;stroke-width:3;stroke-linejoin:round}svg .label{font:36px Manrope,sans-serif;fill:#172B3B}svg .micro{font:28px 'IBM Plex Mono',monospace;fill:#536775}svg .call{stroke:#536775;stroke-width:2;fill:none}"""
def defs(i):return f'''<defs><linearGradient id="{i}-metal" x1="0" y1="0" x2=".8" y2="1"><stop stop-color="#F8F9F5"/><stop offset=".42" stop-color="#B8C6CC"/><stop offset="1" stop-color="#748C9B"/></linearGradient><linearGradient id="{i}-blue" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#7EA9E4"/><stop offset=".55" stop-color="#2459C4"/><stop offset="1" stop-color="#153F82"/></linearGradient><linearGradient id="{i}-poly" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#657D8A"/><stop offset=".45" stop-color="#354F60"/><stop offset="1" stop-color="#172B3B"/></linearGradient><linearGradient id="{i}-belt" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#203442"/><stop offset=".3" stop-color="#4D6370"/><stop offset=".7" stop-color="#364E5C"/><stop offset="1" stop-color="#172B3B"/></linearGradient><pattern id="{i}-weave" width="9" height="9" patternUnits="userSpaceOnUse"><path d="M0 2H9M2 0V9" stroke="#D2DBDC" stroke-width="1" opacity=".18"/></pattern><marker id="{i}-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7Z" fill="#C94422"/></marker></defs>'''
def call(x,y,tx,ty,text):return f'<path class="call" d="M{x} {y+12}h65L{tx} {ty}"/><circle cx="{tx}" cy="{ty}" r="5" fill="#2459C4"/><text class="label" x="{x}" y="{y}">{esc(text)}</text>'
def wheel(i,name,r,n,material='metal',ratchet=False):
    pts=[]
    for k in range(n):
        for q,rr in ([(0,r-19),(.5,r-19),(.5,r),(.72,r)] if ratchet else [(0,r-5),(.23,r+5),(.65,r+5),(.88,r-5)]):
            a=(k+q)*math.tau/n;pts.append(f'{rr*math.cos(a):.3f},{rr*math.sin(a):.3f}')
    p=' '.join(pts)
    return f'<g id="{i}-{name}"><polygon points="{p}" transform="translate(0 11)" fill="#536775" class="edge"/><polygon points="{p}" fill="url(#{i}-{material})" class="edge"/><circle r="{r*.53}" fill="#DDE4E3" stroke="#536775" stroke-width="3"/><path d="M{-r*.4} 0H{r*.4}M0 {-r*.4}V{r*.4}" stroke="#8298A5" stroke-width="11"/><circle r="13" fill="#172B3B"/><circle r="5" fill="#F8F9F5"/></g>'
def springpath():
    pts=[]
    for k in range(150):
        a=k/149*math.tau*3.1;r=16+74*k/149;pts.append(f'{410+r*math.cos(a):.2f},{400+r*math.sin(a):.2f}')
    return 'M'+'L'.join(pts)
def whole(i):return f'''<ellipse cx="450" cy="650" rx="330" ry="29" fill="#172B3B" opacity=".12"/><path d="M145 155Q75 75 150 55H755Q830 75 775 155L740 604Q730 638 687 638H224Q177 638 170 598Z" fill="#D8DFDE" class="edge"/><path d="M145 155h630l-23 46H166Z" fill="#A6B4BE" class="edge"/><g id="{i}-ribbon"><path d="M330 65H565V442H330Z" fill="url(#{i}-belt)" class="edge"/><path d="M330 65H565V442H330Z" fill="url(#{i}-weave)"/><path d="M329 73h236" stroke="#A6B4BE" stroke-width="7"/></g><path d="M196 380Q155 375 155 425V575Q160 615 204 615H714Q756 615 756 575V425Q752 379 712 380Z" fill="url(#{i}-poly)" class="edge"/><path d="M220 421H685V570H220Z" fill="#172B3B"/><g id="{i}-whole-reel"><path d="M235 443H675V550H235Z" fill="url(#{i}-belt)"/><path d="M235 443H675V550H235Z" fill="url(#{i}-weave)"/><ellipse cx="235" cy="496" rx="23" ry="56" fill="url(#{i}-metal)" class="edge"/><ellipse cx="675" cy="496" rx="23" ry="56" fill="url(#{i}-metal)" class="edge"/><path d="M265 473H643M265 505H643M265 532H643" stroke="#718791" stroke-width="5"/></g><path d="M308 60V20H588V60" fill="none" stroke="#536775" stroke-width="12"/><path d="M635 250v-115" fill="none" stroke="#C94422" stroke-width="8" marker-end="url(#{i}-arrow)"/><text x="186" y="702" class="micro">Ilustrasi potongan retractor</text>'''
def assembly(i):
    # Axial layers are separated in depth, while their side-view shaft landmark is shared.
    return f'''<ellipse cx="440" cy="650" rx="338" ry="22" fill="#172B3B" opacity=".12"/>
<g id="{i}-housing"><path d="M155 190H738V607H155Z" fill="#D9E0DE" stroke="#A6B4BE" stroke-width="4"/><path d="M155 190l27 -27h584l-28 27Z" fill="#F8F9F5" class="edge"/><path d="M738 190l28 -27v417l-28 27Z" fill="#A6B4BE" class="edge"/><circle cx="189" cy="222" r="9" fill="#536775"/><circle cx="700" cy="570" r="9" fill="#536775"/></g>
<g id="{i}-ribbon"><path d="M255 75H395V342H255Z" fill="url(#{i}-belt)" class="edge"/><path d="M255 75H395V342H255Z" fill="url(#{i}-weave)"/></g>
<g id="{i}-spool"><path d="M242 282H410V518H242Z" fill="url(#{i}-belt)" class="edge"/><ellipse cx="242" cy="400" rx="28" ry="118" fill="url(#{i}-metal)" class="edge"/><path d="M253 308H397M253 339H397M253 370H397M253 431H397M253 462H397M253 493H397" stroke="#6A828F" stroke-width="5"/></g>
<g transform="translate(410 400)">{wheel(i,'ratchet',165,18,ratchet=True)}</g>
<g id="{i}-carrier"><path d="M408 372L520 233Q548 211 577 237L591 263Q603 288 573 310L438 427Z" fill="#BCC9CD" class="edge"/><path d="M408 383L526 246L570 269L424 413Z" fill="#E0E7E5"/><g transform="translate(410 400) rotate(12.559)"><path d="M0 -12H300V12H0Z" fill="url(#{i}-metal)" class="edge"/><path d="M292 -22H355V22H292V10H342V-10H292Z" fill="url(#{i}-metal)" class="edge"/></g>
<g transform="translate(517.988 271.302)">{wheel(i,'pinion',56,12)}<g id="{i}-inertia"><circle r="87" cy="-17" fill="#172B3B" opacity=".14"/><circle r="79" fill="url(#{i}-blue)" class="edge"/><path d="M-56 -40A69 69 0 0 1 48 -47" fill="none" stroke="#B8CDEE" stroke-width="6"/><circle r="47" fill="#2D5C9E" stroke="#92B1D8" stroke-width="3"/><path d="M-33 0H33M0 -33V33" stroke="#D8E3E9" stroke-width="7"/><circle r="13" fill="url(#{i}-metal)" class="edge"/></g></g></g>
<g transform="translate(410 400)">{wheel(i,'driver',112,24)}</g>
<g id="{i}-bias"><path id="{i}-bias-coil" d="M775 260L703 465" fill="none" stroke="#172B3B" stroke-width="5"/><circle cx="775" cy="260" r="9" fill="#536775"/></g>
<g id="{i}-pawl-wrap"><g id="{i}-pawl"><path d="M-150 0L-115 -22L16 -22L40 -4L16 22L-102 22Z" transform="translate(0 10)" fill="#405D6D" class="edge"/><path d="M-150 0L-115 -22L16 -22L40 -4L16 22L-102 22Z" fill="url(#{i}-metal)" class="edge"/><circle r="15" fill="#536775" stroke="#172B3B" stroke-width="4"/><circle r="6" fill="#F8F9F5"/><circle cx="29" cy="0" r="8" fill="#C94422" stroke="#172B3B" stroke-width="3"/></g></g>
<path id="{i}-force" d="M806 484H744M610 515L554 481M412 563V510" fill="none" stroke="#C94422" stroke-width="6" marker-end="url(#{i}-arrow)"/>
<g id="{i}-spring"><ellipse cx="410" cy="412" rx="119" ry="119" fill="#536775" class="edge"/><circle cx="410" cy="400" r="119" fill="url(#{i}-metal)" class="edge"/><path id="{i}-spiral" d="{springpath()}" fill="none" stroke="#536775" stroke-width="8"/><path d="M410 400H523V420" fill="none" stroke="#172B3B" stroke-width="8"/><circle cx="410" cy="400" r="12" fill="#C94422"/></g>
'''
notes={
'whole':'Satu contoh mekanisme sensor tarikan', 'reel':'Pita dan gulungan terhubung', 'spring':'Potongan pegas balik · bentuk skematis', 'explode':'Lapisan dibuka · jarak diperbesar',
'train':'Potongan sisi · roda inersia digeser aksial', 'normal':'Pelat diam, kedua roda berputar', 'bias':'Pegas menahan pelat di posisi bebas', 'jerk':'Sentakan = perubahan putaran mendadak', 'resist':'Gaya antargigi melawan pegas', 'climb':'Gerak diperlambat · sudut diperbesar', 'arm':'Hubungan lengan dipisahkan untuk inspeksi', 'engage':'Kontak diperlambat · celah diperbesar', 'stop':'Gigi tertahan, pelepasan pita berhenti', 'roles':'Roda sensor memicu; pengunci menahan', 'compare':'Ulangan potongan untuk membuktikan sebab', 'answer':'Contoh US3918658A · geometri disederhanakan'}
# Carrier/arm are shown in separated inspection layers. The pinion mesh is exact;
# arm/pawl transfer gets a separate enlarged view rather than an invented in-plane linkage.
states={
'whole':(0,65.7,0,36),'reel':(0,80,0,0),'spring':(80,0,0,0),'explode':(0,0,0,0),'train':(0,70,0,0),'normal':(70,140,0,0),'bias':(47.7,47.7,0,0),
'jerk':(47.7,53.7,0,4),'resist':(53.7,62.7,4,10),'climb':(62.7,86.7,10,26),'arm':(86.7,95.7,26,32),'engage':(95.7,105.7,32,36),
'stop':(105.7,105.7,36,36),'roles':(105.7,105.7,36,36),'compare':(0,105.7,0,36),'answer':(105.7,105.7,36,36)}
# 101.7 degree final ratchet phase aligns the pawl tip with the steep radial tooth face.
events=[]
for n,s in enumerate(plan):
    i=s['id'];d=s['duration'];view=s['view'];a0,a1,p0,p1=states[view]
    vb='70 65 800 650'
    if view in ('train','normal','bias','resist'):vb='170 115 700 570'
    if view=='climb':vb='325 155 400 395'
    if view=='arm':vb='440 335 395 300'
    if view=='engage':vb='470 305 365 330'
    if view=='spring':vb='210 190 410 410'
    art=whole(i) if view=='whole' else assembly(i)
    labels=''
    if view=='reel':labels=call(490,150,410,400,'gulungan')
    elif view=='train':labels=call(595,600,410,400,'penggerak')+call(565,145,518,271,'roda inersia')
    elif view=='normal':labels=call(565,145,518,271,'ikut berputar')
    elif view=='bias':labels=call(520,145,740,355,'pegas penahan')
    elif view=='climb':labels=''
    elif view=='arm':labels=''
    elif view=='engage':labels=''
    elif view=='roles':labels=call(112,100,518,271,'pemicu')+call(630,675,615,470,'penahan')
    elif view=='answer':labels=call(115,690,563,448,'ini yang menahan')
    art+=labels
    initial=.58*d if not animated else 0
    # Fully seekable, all SVG state derived from local time. External-gear relation
    # theta_pin = 3*phi_carrier - 2*theta_driver enforces a 24:12 illustrative mesh.
    script=f'''
const st={{t:{initial}}},D={d},view='{view}',I='{i}';
const el=n=>document.getElementById(I+'-'+n),cl=(v)=>Math.max(0,Math.min(1,v));
const tr=(n,v)=>{{if(el(n))el(n).setAttribute('transform',v)}},op=(n,v)=>{{if(el(n))el(n).style.opacity=v}};
function draw(){{
 const t=st.t,u=cl((t-.35)/Math.max(.1,D*.69));let theta={a0}+({a1-a0})*u,phi={p0}+({p1-p0})*u;
 if(view==='whole'||view==='compare'){{const slow=cl((t-.2)/(D*.34)),jerk=cl((t-D*.51)/(D*.27));theta=47.7*slow+58*jerk;phi=36*jerk;}}
 const progress=phi/36,pawl=-25+42*progress;
 const projectionX=700+29*Math.cos(pawl*Math.PI/180),projectionY=485+29*Math.sin(pawl*Math.PI/180);
 phi=Math.atan2(projectionY-400,projectionX-410)*180/Math.PI-12.559;
 const pin=3*phi-2*theta;
 if(view==='whole'){{tr('ribbon',`translate(0 ${{-theta*.65}})`);tr('whole-reel',`translate(0 0)`);}}
 else{{
  op('housing',view==='reel'||view==='answer'?.8:.2);op('spring',view==='spring'?1:0);
  op('inertia',view==='climb'||view==='train'?.42:1);op('force',view==='resist'||view==='stop'?.95:0);
  const orbit=phi*Math.PI/180,px=410+168*Math.cos((-50)*Math.PI/180+orbit),py=400+168*Math.sin((-50)*Math.PI/180+orbit);
  tr('driver',`rotate(${{theta}})`);tr('ratchet',`rotate(${{theta}})`);
  tr('carrier',`rotate(${{phi}} 410 400)`);tr('pinion',`rotate(${{pin-phi}})`);tr('inertia',`rotate(${{pin-phi}})`);
  // Pawl tip reaches the locking face only at the final inspected angle.
  tr('pawl-wrap','translate(700 485)');tr('pawl',`rotate(${{pawl}})`);
  const ex=410+293*Math.cos((12.559+phi)*Math.PI/180),ey=400+293*Math.sin((12.559+phi)*Math.PI/180),dx=ex-775,dy=ey-260,L=Math.hypot(dx,dy);let coil='M775 260';
  for(let k=1;k<=16;k++){{let f=k/17,z=k<3||k>14?0:(k%2?9:-9);coil+=`L${{775+dx*f-dy/L*z}} ${{260+dy*f+dx/L*z}}`;}}coil+=`L${{ex}} ${{ey}}`;el('bias-coil').setAttribute('d',coil);
  tr('ribbon',`translate(0 ${{-theta*.55}})`);
  if(view==='spring'){{for(const name of ['housing','carrier','driver','ratchet','pawl-wrap','bias','ribbon','spool'])op(name,0);let pp='';for(let k=0;k<150;k++){{let f=k/149,r=16+74*f,a=(f*3.1+theta/360*(1-f))*Math.PI*2;pp+=(k?'L':'M')+(410+r*Math.cos(a))+' '+(400+r*Math.sin(a));}}el('spiral').setAttribute('d',pp);}}
  if(view==='explode'){{op('housing',.12);tr('carrier',`translate(${{u*66}} ${{-u*42}})`);}}
  if(view==='arm'){{op('inertia',.2);op('driver',.3);op('ratchet',.65);}}
  if(view==='engage'||view==='stop'){{op('inertia',.16);op('driver',.35);}}
  window['state_'+I]={{t,theta,phi,pin,pawl,px,py,projectionX,projectionY,meshResidual:pin-3*phi+2*theta,locked:progress>=.99999}};
 }}
}}
draw();const tl=gsap.timeline({{paused:true,onUpdate:draw}});
'''
    if animated:script+=f"tl.to(st,{{t:{d-.001},duration:{d-.001},ease:'none'}},0);"
    else:script+=f"tl.to({{}},{{duration:{d-.001}}},0);"
    script+=f"window.__timelines['{i}']=tl;"
    write(V/f'compositions/{i}.html',f'''<template><style>{CSS}</style><div id="root" data-composition-id="{i}" data-width="1080" data-height="1920"><div id="{i}-scene" class="scene clip" data-start="0" data-duration="{d}"><h1 id="{i}-title" class="title" data-var-text="title">{esc(s['title'])}</h1><div id="{i}-stage" class="stage"><svg viewBox="{vb}" role="img" aria-label="{esc(s['purpose'])}">{defs(i)}{art}</svg></div><div class="note">{esc(notes[view])}</div></div></div><script>{script}</script></template>''')
    if animated:
        local=[(.35,'editorial','section attention')]
        if view in ('whole','compare'):local=[(.2,'travel','gentle belt withdrawal'),(DUMMY:=d*.51,'travel','accelerating belt withdrawal'),(d*.78,'metal','pawl seated; reel stops')]
        elif view in ('reel','spring','train','normal'):local=[(.35,'travel' if view in ('reel','spring') else 'metal',view+' coupled motion onset')]
        elif view in ('jerk','resist','climb','arm'):local=[(.35,'travel' if view in ('jerk','climb') else 'metal',view+' interaction onset')]
        elif view=='engage':local=[(.35,'travel','pawl approach'),(.35+d*.69,'metal','pawl tooth contact and reel stop')]
        elif view in ('stop','roles','answer'):local=[]
        for at,role,action in local:
            if at<d:events.append(dict(scene=i,time=round((s['start']+at)*30)/30,role=role,action=action))
hosts='\n'.join(f'<div id="{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-variable-values=\'{json.dumps({"title":s["title"]},ensure_ascii=False)}\' data-start="{s["start"]:.6f}" data-duration="{s["duration"]:.6f}" data-width="1080" data-height="1920" data-track-index="1" data-track-kind="graphics"></div>' for s in plan)
audio='';caps=''
if animated:
    am=json.loads((V/'placed_audio.json').read_text(encoding='utf-8'));audio=f'<audio id="narration" class="clip" src="{am["path"]}" data-start="0" data-duration="90" data-volume="1" data-track-index="3"></audio>'
    groups=json.loads((V/'caption-groups.json').read_text(encoding='utf-8'))
    caption=''.join(f'<div id="cap-{k:03}" class="clip cap" data-start="{g["start"]:.6f}" data-duration="{g["end"]-g["start"]:.6f}"><span>{esc(g["text"])}</span></div>' for k,g in enumerate(groups))
    write(V/'compositions/captions.html',f'''<template><style>@font-face{{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:200 800}}#root{{position:absolute;inset:0;pointer-events:none}}.cap{{position:absolute;left:108px;top:1190px;width:790px;font:600 44px/1.25 Manrope,sans-serif;color:#172B3B;background:#ECEEE9;padding:4px 0}}</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920">{caption}</div><script>window.__timelines['captions']=gsap.timeline({{paused:true}}).to({{}},{{duration:90}},0);</script></template>''')
    caps='<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="90" data-width="1080" data-height="1920" data-track-index="2" data-track-kind="captions" style="z-index:3"></div>'
write(V/'index.html',f'''<!doctype html><html lang="id" data-composition-variables='[{{"id":"ink","type":"color","label":"Engineering ink","default":"#172B3B"}}]'><head><meta charset="utf-8"><title>Sabuk: sentakan dan pengunci</title><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>*{{box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#ECEEE9}}#root{{position:relative;width:1080px;height:1920px}}.clip[data-composition-src]{{position:absolute;inset:0}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="90" data-width="1080" data-height="1920" data-fps="30">{hosts}{caps}{audio}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines.main=gsap.timeline({{paused:true}}).to({{}},{{duration:90}},0);</script></body></html>''')
if animated:write(V/'motion-events.json',json.dumps(events,indent=2))
else:
    doc='''---
format: 1080x1920
duration: 90s
message: Sudden accelerating withdrawal actuates the inertia-wheel carrier and pawl; the seated pawl holds the reel.
mode: autonomous
---

# Visual storyboard v1

All 16 scene poses built and mounted before audio or animation. Board v5; original layered 2.5D schematics with physical thickness. Agent verification under --automation, human approval not asserted. Estimated times below; timing.json will supply measured speech-based timing. Signature interaction s10; diagnostic pawl contact s12. Opening s01 paired with s15/s16 proof.

'''
    for k,s in enumerate(plan):
        doc+=f'''## Frame {k+1}: {s['title']} ({s['start']:g}–{s['end']:g}s)

- id: {s['id']}
- src: compositions/{s['id']}.html
- status: built
- duration: {s['duration']}s
- poster: {s['start']+s['duration']*.58:g}s
- scene: {s['purpose']}
- voiceover: {s['text']}
- on-screen: {s['title']}
- reads: title stable (0–1.8s); physical relationship (1.8s–end); captions occupy separate measured lower band.
- discovery link: {s['purpose']} Leads to the next mechanism dependency, not another part catalogue.
- component first use: {s['view']}; names follow function. Earlier shaft, blue wheel and fixed support remain landmarks.
- story role: {'opening mystery' if k==0 else 'first discovery' if k==1 else 'signature interaction' if k==9 else 'ending proof' if k>=14 else 'linked causal discovery'}.
- framing: {s['view']}, viewBox chosen to reveal the relevant contact; 2.5D shaded metal/polymer retained. {notes[s['view']]}.
- state continuity: normal reference through s07; s08–s12 continue acceleration, carrier and pawl progression; s13–s14 remain locked; s15 explicitly marked explanatory replay; s16 ends locked. s03 is a separate rewind demonstration; s04 an explanatory axial separation.
- action/diagnostic poses: input before motion → gear resistance/transfer → carrier response → pawl approach/seating → stopped output. For s10 inspect orbit start, approach, midway and end; s12 inspect gap, approach, tooth-face contact and held state.
- attention: orange input → blue inspected part → affected output. Stable camera on contact, then observation hold. No simultaneous decorative highlights.
- sound: frame-aligned cue at actual designed interaction; coupled motion shares onset sound. Distinct editorial cue on inspection; physical-material cue on contact. Static bias reading, load-path hold and locked ending intentionally quiet beneath narration.
- evidence: C1–C7 in ../SOURCES.md; A figures 1–3 establish topology. Altered spacing and time explicitly labelled.

'''
    write(V/'STORYBOARD.md',doc)
print(json.dumps(dict(mode='animation' if animated else 'static',scenes=len(plan),duration=sum(s['duration'] for s in plan))))
