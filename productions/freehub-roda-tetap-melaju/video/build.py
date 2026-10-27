"""Build pre-audio poses or seekable 2.5D film from the same scene geometry."""
from pathlib import Path
import json,math,html,sys
V=Path(__file__).resolve().parent; animated='--animate' in sys.argv
raw=json.loads((V/('timing.json' if animated else 'scene-plan.json')).read_text(encoding='utf-8'))
plan=raw['scenes'] if isinstance(raw,dict) else raw
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def esc(s):return html.escape(str(s),quote=True)
CSS="""@font-face{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:200 800}@font-face{font-family:Plex;src:url('assets/fonts/ibm-plex-mono.ttf')}*{box-sizing:border-box}#root{position:absolute;inset:0;color:#172B3B;font-family:Manrope,sans-serif}.scene{position:absolute;inset:0;background:#ECEEE9}.title{position:absolute;left:108px;top:205px;width:800px;margin:0;font-size:72px;line-height:1.1;font-weight:800;letter-spacing:-3px}.stage{position:absolute;left:90px;top:470px;width:900px;height:900px}.stage svg{width:100%;height:100%;overflow:hidden}.note{position:absolute;left:108px;top:1380px;width:810px;font:28px/1.35 Plex,monospace;color:#536775}.pose-caption{position:absolute;left:108px;top:1500px;width:848px;text-align:center;font:600 46px/1.3 Manrope,sans-serif}.pose-caption span{display:inline-block;background:#F8F9F5;padding:18px 26px;border-radius:14px;max-width:848px}svg .edge{stroke:#172B3B;stroke-width:2.5;stroke-linejoin:round}svg .label{font:28px Manrope,sans-serif;fill:#172B3B}svg .leader{fill:none;stroke:#536775;stroke-width:2}svg .arrow{fill:none;stroke:#C94422;stroke-width:6;stroke-linecap:round}"""
def defs(i):return f'''<defs><linearGradient id="{i}-metal" x1="0" y1="0" x2=".8" y2="1"><stop stop-color="#F8F9F5"/><stop offset=".45" stop-color="#BAC8CE"/><stop offset="1" stop-color="#748B98"/></linearGradient><linearGradient id="{i}-blue"><stop stop-color="#8CB5E6"/><stop offset=".55" stop-color="#2459C4"/><stop offset="1" stop-color="#173F83"/></linearGradient><linearGradient id="{i}-orange" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#E4A281"/><stop offset=".6" stop-color="#C94422"/><stop offset="1" stop-color="#8A301E"/></linearGradient><linearGradient id="{i}-teal" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#A2C9C8"/><stop offset=".55" stop-color="#4F9398"/><stop offset="1" stop-color="#167580"/></linearGradient><marker id="{i}-arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0L7 3L0 6Z" fill="#C94422"/></marker></defs>'''
def internal_path():
 pts=[]
 for k in range(18):
  for q,r in [(0,230),(.9,258),(1,258)]:
   a=(k+q)*math.tau/18;pts.append((r*math.cos(a),r*math.sin(a)))
 return 'M'+'L'.join(f'{x:.4f} {y:.4f}' for x,y in pts)+'Z'
def ring(i):
 hole=internal_path();path=f'M 300 0 A300 300 0 1 0 -300 0 A300 300 0 1 0 300 0Z {hole}'
 spokes=''.join(f'<path d="M0 -288V-335" transform="rotate({k*30})" stroke="#688C94" stroke-width="9"/>' for k in range(12))
 front=f'<path d="{path}" fill="url(#{i}-teal)" fill-rule="evenodd" class="edge"/>'
 return f'''<g id="{i}-output">{spokes}<path d="{path}" transform="translate(0 13)" fill="#456C77" fill-rule="evenodd" class="edge"/>{front}<path d="M-206 -220A301 301 0 0 1 212 -214" fill="none" stroke="#D6E6E2" stroke-width="5"/><circle cx="0" cy="-282" r="8" fill="#F8F9F5" stroke="#172B3B" stroke-width="2"/></g>'''
def pawl(i,k):
 return f'''<g transform="rotate({k*180})"><g transform="translate(185 -50)"><g id="{i}-pawl{k}"><path d="M-16 -11Q-23 0 -10 13L50 56L65 50L58 36L12 -12Z" transform="translate(0 7)" fill="#153D6C" class="edge"/><path d="M-16 -11Q-23 0 -10 13L50 56L65 50L58 36L12 -12Z" fill="url(#{i}-blue)" class="edge"/><path d="M7 -5L53 40" stroke="#9BC0EB" stroke-width="4"/><circle r="8" fill="url(#{i}-metal)" class="edge"/><circle r="3" fill="#172B3B"/></g><path id="{i}-spring{k}" d="M-18 32Q8 4 29 25" fill="none" stroke="#536775" stroke-width="4" stroke-linecap="round"/><circle cx="-18" cy="32" r="4" fill="#172B3B"/></g></g>'''
def assembly(i):
 slots=''.join(f'<path d="M-10 -157H10V-126H-10Z" transform="rotate({k*30})" fill="#9F351F" stroke="#172B3B" stroke-width="2"/>' for k in range(12))
 return ring(i)+f'''<g id="{i}-input"><circle cy="12" r="180" fill="#7E3525" class="edge"/><circle r="180" fill="url(#{i}-orange)" class="edge"/>{slots}<path d="M145 -112L200 -71L205 -27L158 -16Z" fill="url(#{i}-orange)" class="edge"/><path d="M145 -112L200 -71L205 -27L158 -16Z" transform="rotate(180)" fill="url(#{i}-orange)" class="edge"/>{pawl(i,0)}{pawl(i,1)}<circle r="93" fill="url(#{i}-metal)" class="edge"/><circle r="62" fill="#536775" stroke="#172B3B" stroke-width="3"/><path d="M-36 0H36M0 -36V36" stroke="#A6B4BE" stroke-width="12"/></g><circle r="25" fill="url(#{i}-metal)" class="edge"/><path d="M-12 -7H12V7H-12Z" fill="#172B3B"/><circle id="{i}-contact" cx="250" cy="0" r="11" fill="none" stroke="#2459C4" stroke-width="3"/>'''
def bike(i):
 spokes=''.join(f'<path d="M0 -184V184" transform="rotate({k*30})" stroke="#7F949F" stroke-width="3"/>' for k in range(6))
 wheels=''.join(f'<g transform="translate({x} 470)"><circle cy="10" r="190" fill="none" stroke="#536775" stroke-width="24"/><circle r="190" fill="#F8F9F5" stroke="#172B3B" stroke-width="18"/><g id="{i}-wheel{k}">{spokes}<circle cx="0" cy="-182" r="9" fill="#167580"/></g><circle r="16" fill="url(#{i}-metal)" class="edge"/></g>' for k,x in enumerate([235,665]))
 return wheels+f'''<path d="M235 470L359 258L461 470L235 470L535 258L665 470M359 258H535L461 470M359 258L344 221M535 258L526 208" fill="none" stroke="#536775" stroke-width="25" stroke-linejoin="round"/><path d="M235 458L359 246L461 458L235 458L535 246L665 458M359 246H535L461 458M359 246L344 209M535 246L526 196" fill="none" stroke="url(#{i}-teal)" stroke-width="18" stroke-linejoin="round"/><path d="M316 207H378" stroke="#172B3B" stroke-width="17" stroke-linecap="round"/><path d="M526 196L570 180L589 201" fill="none" stroke="#172B3B" stroke-width="11" stroke-linecap="round"/><path d="M235 448L461 438A32 32 0 0 1 461 502L235 492A23 23 0 0 1 235 448" fill="none" stroke="#536775" stroke-width="7"/><g id="{i}-crank" transform="translate(461 470)"><circle r="30" fill="url(#{i}-orange)" class="edge"/><path d="M0 0L45 54H77" fill="none" stroke="#C94422" stroke-width="11" stroke-linecap="round"/></g><path d="M150 729H740" stroke="#CDD4D4" stroke-width="3"/><text x="292" y="765" class="label">Meluncur · pedal diam</text>'''
def axial(i):
 teeth=''.join(f'<path d="M0 -180V-203" transform="translate(290 420) rotate({k*20})" stroke="#536775" stroke-width="16"/>' for k in range(18))
 splines=''.join(f'<path d="M330 {y}H578L612 {y-13}" fill="none" stroke="#8A301E" stroke-width="11"/>' for y in [341,380,420,460,499])
 return f'''<ellipse cx="470" cy="690" rx="357" ry="24" fill="#172B3B" opacity=".1"/><path d="M125 420H815" stroke="#536775" stroke-width="22"/><path d="M125 413H815" stroke="#DCE5E3" stroke-width="8"/><g id="{i}-shell"><path d="M560 317H700V523H560Z" fill="url(#{i}-teal)" class="edge"/><ellipse cx="700" cy="420" rx="72" ry="172" fill="#326F7B" class="edge"/><ellipse cx="560" cy="420" rx="72" ry="172" fill="url(#{i}-teal)" class="edge"/><path d="M700 248V198M700 592V642M560 248V198M560 592V642" stroke="#688C94" stroke-width="10"/><ellipse cx="700" cy="420" rx="21" ry="46" fill="#536775" class="edge"/><circle id="{i}-shell-mark" cx="560" cy="254" r="8" fill="#F8F9F5"/></g><g id="{i}-sprocket"><path d="M290 304H563V536H290Z" fill="url(#{i}-orange)" class="edge"/><ellipse cx="563" cy="420" rx="47" ry="116" fill="#8A301E" class="edge"/>{splines}{teeth}<ellipse cx="290" cy="420" rx="162" ry="180" fill="url(#{i}-metal)" class="edge"/><ellipse cx="290" cy="420" rx="90" ry="106" fill="#CDD4D4" class="edge"/><ellipse cx="290" cy="420" rx="39" ry="54" fill="url(#{i}-orange)" class="edge"/><path id="{i}-spoke-mark" d="M290 306V252" stroke="#C94422" stroke-width="10"/></g><path id="{i}-chain" d="M95 225H295Q480 235 473 420Q465 610 290 612H90" fill="none" stroke="#172B3B" stroke-width="12" stroke-dasharray="14 13"/><path d="M130 152H340" class="arrow" marker-end="url(#{i}-arr)"/><path d="M240 420H345" stroke="#DCE5E3" stroke-width="14"/><text x="170" y="739" class="label">sproket</text><text x="446" y="739" class="label">penggerak</text><text x="668" y="739" class="label">rumah roda</text>'''
def bearing(i):
 balls=''.join(f'<circle cx="{115*math.cos(k*math.tau/10):.2f}" cy="{115*math.sin(k*math.tau/10):.2f}" r="21" fill="url(#{i}-metal)" class="edge"/>' for k in range(10))
 return f'''<path d="M-325 0H325" stroke="#536775" stroke-width="31"/><path d="M-325 -9H325" stroke="#DCE5E3" stroke-width="10"/><circle cy="15" r="190" fill="#456C77" class="edge"/><circle r="190" fill="url(#{i}-teal)" class="edge"/><circle r="155" fill="url(#{i}-metal)" class="edge"/><circle r="133" fill="#536775"/><g id="{i}-balls">{balls}</g><circle r="88" fill="url(#{i}-metal)" class="edge"/><circle r="40" fill="#536775" class="edge"/><path d="M-28 -9H28V9H-28Z" fill="#DCE5E3"/>'''
notes={
'mystery':'Contoh meluncur · mekanisme di roda belakang', 'independent':'Potongan freehub tipe pawl · poros tetap', 'input':'Lapisan samping · jarak aksial diperjelas', 'inside':'Cangkang dibuka · bentuk gigi skematis', 'spring':'Makro pengait dan pegas · ukuran diperbesar', 'approach':'Gerak diperlambat · celah diperjelas', 'contact':'Kontak diperlambat · sisi penahan gigi', 'drive':'Jari-jari mengikuti rumah roda', 'stop':'Meluncur · roda melampaui putaran penggerak', 'overtake':'Penggerak diam · cincin terus maju', 'ramp':'Makro sisi miring · gerak diperlambat', 'reset':'Pegas mengembalikan pengait', 'clicks':'Bunyi ilustratif mengikuti kontak', 'bearing':'Bantalan dan pengait punya tugas berbeda', 'resume':'Celah ilustratif · bukan sudut baku', 'answer':'Roda melaju · penggerak dari pedal diam'}
notes['spring']='Pengait diisolasi; pegas skematis'
# Shared analytic motion definitions are copied into each independently editable scene.
RUNTIME=r'''
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const lerp=(a,b,t)=>a+(b-a)*clamp(t);
function polarTip(alpha){const a=alpha*Math.PI/180;return {x:185+65*Math.cos(a)-50*Math.sin(a),y:-50+65*Math.sin(a)+50*Math.cos(a)}}
function toothRadius(angle){const p=((angle%20)+20)%20;return p<18?230+28*p/18:258;}
function gap(alpha,relative){const p=polarTip(alpha),a=Math.atan2(p.y,p.x)*180/Math.PI;return toothRadius(a-relative)-Math.hypot(p.x,p.y);}
function pawlAngle(relative){if(gap(0,relative)>=0)return 0;let last=0;for(let a=.1;a<=42;a+=.1){if(gap(a,relative)>=0){let l=last,h=a;for(let j=0;j<16;j++){let m=(l+h)/2;if(gap(m,relative)>=0)h=m;else l=m;}return h;}last=a;}return 42;}
function state(u){
 let input=0,output=0,alpha=null;
 if(key==='mystery'||key==='answer'){output=u*88;}
 if(key==='independent'){input=0;output=u*48;}
 if(key==='input'){input=lerp(0,44,(u-.13)/.7);output=input;}
 if(key==='inside'){input=0;output=1;}
 if(key==='spring'){output=18;alpha=lerp(27,0,(u-.18)/.48);}
 if(key==='approach'){output=0;input=lerp(-9,-4,(u-.12)/.6);}
 if(key==='contact'){input=lerp(-4,0,(u-.1)/.24);output=0;if(u>.42){input=output=lerp(0,9,(u-.42)/.37);}}
 if(key==='drive'){input=output=lerp(9,71,(u-.12)/.78);}
 if(key==='stop'){input=26*Math.min(u,.32)/.32;output=u*78;}
 if(key==='overtake'){input=0;output=lerp(1,34,(u-.08)/.78);}
 if(key==='ramp'){input=0;output=lerp(2,16.5,(u-.15)/.65);}
 if(key==='reset'){input=0;output=lerp(16.5,22.5,(u-.15)/.65);}
 if(key==='clicks'){input=0;output=1+u*99;}
 if(key==='resume'){output=0;input=lerp(-7,0,(u-.12)/.44);if(u>.67)input=output=lerp(0,9,(u-.67)/.22);}
 if(alpha===null){const r=output-input;alpha=Math.abs(r)<.00001?0:pawlAngle(r);const phase=((r%20)+20)%20;if(r>0&&phase>0&&phase<2&&['ramp','reset','clicks','overtake','independent','answer'].includes(key))alpha=Math.max(alpha,pawlAngle(19.999)*(1-phase/2));}
 if(!['spring'].includes(key)&&Math.abs(output-input)>.00001&&gap(alpha,output-input)<0){let start=alpha;for(let q=start;q<=42;q+=.03){if(gap(q,output-input)>=0){alpha=q;break;}}}
 return {input,output,alpha,relative:output-input,gap:gap(alpha,output-input)};
}
const el=name=>document.getElementById(id+'-'+name);
const rot=(name,a)=>{const e=el(name);if(e)e.setAttribute('transform','rotate('+a+')');};
function renderAt(t){const u=clamp(t/duration),s=state(u);
 rot('output',s.output);rot('input',s.input);
 for(let k=0;k<2;k++){rot('pawl'+k,s.alpha);const spring=el('spring'+k);if(spring){const p=polarTip(s.alpha);spring.setAttribute('d','M-18 32Q-3 '+(8+s.alpha*.4)+' '+((p.x-185)*.44)+' '+((p.y+50)*.44));}}
 const c=el('contact');if(c){const a=s.input*Math.PI/180,p=polarTip(s.alpha);c.setAttribute('cx',p.x*Math.cos(a)-p.y*Math.sin(a));c.setAttribute('cy',p.x*Math.sin(a)+p.y*Math.cos(a));c.setAttribute('opacity',key==='contact'||key==='resume'?(u>.34&&u<.9?1:0):0);}
 rot('wheel0',s.output);rot('wheel1',s.output);
 const crank=el('crank');if(crank)crank.setAttribute('transform','translate(461 470) rotate('+s.input+')');
 const chain=el('chain');if(chain)chain.setAttribute('stroke-dashoffset',-s.input*2);
 const sm=el('spoke-mark');if(sm)sm.setAttribute('transform','rotate('+s.input+' 290 420)');
 const shellmark=el('shell-mark');if(shellmark){shellmark.setAttribute('cx',560+66*Math.sin(s.output*Math.PI/180));shellmark.setAttribute('cy',420-166*Math.cos(s.output*Math.PI/180));}
 rot('balls',u*100);window.__mechanism=Object.assign({scene:id,time:t},s);
}
'''
events=[]
for n,s in enumerate(plan):
 i=s['id'];key=s['key'];d=s['duration'];view=s['view'];vb='-350 -350 700 700'
 art=assembly(i)
 if key=='spring':art=art.replace(f'<g id="{i}-output">',f'<g id="{i}-output" opacity=".12">')
 if view=='bike':art=bike(i);vb='0 0 900 900'
 elif view=='axial':art=axial(i);vb='0 0 900 900'
 elif view=='macro':vb='120 -156 208 230'
 elif view=='bearing':art=bearing(i);vb='-225 -225 450 450'
 elif view=='proof':
  # The same wheel/spoke landmark returns around the now-exposed coupling.
  art=assembly(i)+f'<path d="M-310 300H-190" stroke="#C94422" stroke-width="8"/><path d="M-250 300v-45M-250 300v45" stroke="#C94422" stroke-width="8"/><text x="-170" y="312" class="label"></text>'
 if False and view=='ring':
  labels={'independent':('penggerak','rumah roda'),'inside':('pengait','cincin bergigi'),'drive':('masukan','keluaran'),'overtake':('diam','terus berputar'),'clicks':('pengait','gigi lewat')}
  a,b=labels[key];art+=f'<text x="-295" y="-302" class="label">{a}</text><text x="44" y="310" class="label">{b}</text>'
 if view=='macro':
  # Mark the actual pivot and adjoining tooth face without covering contact.
  art+=f'<path d="M140 -113L185 -50" class="leader"/><text x="126" y="-121" style="font:12px Manrope;fill:#536775">poros</text>'
 initial=.58*d
 script=f"const id={json.dumps(i)},key={json.dumps(key)},duration={d:.12f};\n"+RUNTIME
 if animated:script+=f"\nconst clock={{t:0}},tl=gsap.timeline({{paused:true}});tl.to(clock,{{t:duration,duration:duration,ease:'none',onUpdate:()=>renderAt(clock.t)}},0);renderAt(0);window.__timelines[id]=tl;"
 else:script+=f"\nrenderAt({initial});const tl=gsap.timeline({{paused:true}}).to({{}},{{duration:duration}},0);window.__timelines[id]=tl;"
 pose='' if animated else f'<div class="pose-caption"><span>{esc(" ".join(s["text"].split()[:5]))}</span></div>'
 markup=f'''<template><style>{CSS}</style><div id="root" data-composition-id="{i}" data-width="1080" data-height="1920" data-duration="{d:.12f}"><div class="scene"><h1 class="title" data-var-text="{i}-title">{esc(s['title'])}</h1><div class="stage"><svg viewBox="{vb}" aria-label="{esc(s['job'])}">{defs(i)}{art}</svg></div><div class="note">{esc(notes[key])}</div>{pose}</div></div><script>{script}</script></template>'''
 write(V/f'compositions/{i}.html',markup)
 if animated:
  marks={'mystery':[(.25,'metal','representative coasting contact'),(.70455,'metal','representative coasting contact')], 'independent':[(.45833,'metal','coasting pawl reset')], 'overtake':[(.08,'travel','ring overtakes pawl')], 'answer':[(.32,'metal','coasting proof contact'),(.65,'metal','coasting proof contact')], 'input':[(.13,'travel','chain input begins')], 'inside':[(.27,'editorial','section inspection')], 'spring':[(.66,'travel','spring raises pawl')], 'approach':[(.72,'metal','pawl reaches tooth face')], 'contact':[(.34,'metal','drive-face contact'),(.42,'travel','coupled output begins')], 'drive':[(.12,'travel','coupled wheel rotation')], 'stop':[(.32,'travel','input comes to rest')], 'ramp':[(.38054,'travel','ramp depresses pawl')], 'reset':[(.529167,'metal','pawl resets after tooth')], 'resume':[(.56,'metal','renewed drive contact'),(.67,'travel','renewed coupled output')]}.get(key,[])
  if key=='clicks':marks=[(q,'metal','pawl reset after tooth') for q in [.192,.394,.596,.798]]
  for fraction,role,action in marks:
   events.append(dict(scene=i,time=round((s['start']+d*fraction)*30)/30,local_fraction=fraction,role=role,action=action))
hosts=''.join(f'<div id="host-{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-start="{s["start"]:.12f}" data-duration="{s["duration"]:.12f}" data-width="1080" data-height="1920" data-track-index="0" data-track-kind="graphics" style="z-index:1"></div>' for s in plan)
audio='';caps=''
if animated:
 groups=json.loads((V/'caption-groups.json').read_text(encoding='utf-8'))
 caption=''.join(f'<div id="cap-{k:03}" class="clip cap" data-start="{g["start"]:.12f}" data-duration="{g["end"]-g["start"]:.12f}" data-layout-allow-caption-zone="true"><span>{esc(g["text"])}</span></div>' for k,g in enumerate(groups))
 # Registry editorial-emphasis grouping adapted to the board's explicit static phrase treatment.
 write(V/'compositions/captions.html',f'''<template><style>@font-face{{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:200 800}}#root{{position:absolute;inset:0;pointer-events:none}}.cap{{position:absolute;left:108px;top:1500px;width:848px;text-align:center;font:600 46px/1.3 Manrope,sans-serif;color:#172B3B}}.cap span{{display:inline-block;max-width:848px;background:#F8F9F5;padding:18px 26px;border-radius:14px}}</style><div id="root" data-composition-id="captions" data-duration="90" data-width="1080" data-height="1920">{caption}</div><script>window.__timelines.captions=gsap.timeline({{paused:true}}).to({{}},{{duration:90}},0);</script></template>''')
 caps='<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="90" data-width="1080" data-height="1920" data-track-index="2" data-track-kind="captions" style="z-index:3"></div>'
 audio='<audio id="narration" class="clip" src="assets/audio/narration-master.wav" data-start="0" data-duration="90" data-volume="1" data-track-index="3"></audio>'
write(V/'index.html',f'''<!doctype html><html lang="id" data-composition-variables='[{{"id":"ink","type":"color","label":"Engineering ink","default":"#172B3B"}}]'><head><meta charset="utf-8"><title>Freehub: roda tetap melaju</title><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#ECEEE9}}#root{{position:relative;width:1080px;height:1920px}}.clip[data-composition-src]{{position:absolute;inset:0}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="90" data-width="1080" data-height="1920" data-fps="30">{hosts}{caps}{audio}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines.main=gsap.timeline({{paused:true}}).to({{}},{{duration:90}},0);</script></body></html>''')
if animated:write(V/'motion-events.json',json.dumps(events,indent=2))
else:
 doc='''---
format: 1080x1920
duration: 90s
message: A pawl freehub transmits drive but lets the wheel overrun the chain input.
mode: autonomous
---

# Visual storyboard v1

All16 styled scene poses built before audio and animation. Di Balik Benda v6. Timings are estimates until acoustic placement. Each shot retains the axle, orange input and teal output. Opening s01 pairs with s16. First discovery s02; signature contact s07; second detail view s11/s12. Component names follow functional first use.

'''
 for k,s in enumerate(plan):
  doc+=f'''## Frame {k+1}: {s['title']} ({s['start']:g}–{s['end']:g}s)

- id: {s['id']}
- src: compositions/{s['id']}.html
- status: built
- duration: {s['duration']}s
- poster: {s['start']+s['duration']*.58:g}s
- scene: {s['job']}
- voiceover: {s['text']}
- on-screen: {s['title']}
- reads: title stable (0–1.8s); physical cause and response (1.8s–end); short speech phrases in the lower independent band.
- story role: {'opening mystery' if k==0 else 'first discovery' if k==1 else 'signature interaction' if k==6 else 'ending proof' if k==15 else 'linked discovery'}
- discovery and next question: {s['job']} The next shot follows this causal dependency.
- first use: {s['key']}; name follows visible use. Input/output/axle remain stable landmarks across the section.
- framing: {s['view']}; shaded side faces, upper-left material gradients, visible pivot contact and shared assembly axes. {notes[s['key']]}.
- diagnostic states: before input → approach → contact/transfer or depression → changed output → reset where present. Contact shot holds camera while approach closes; ramp shot shows the pivoted response; reset crosses a tooth peak and returns by spring bias.
- state continuity: s02 is a preview of independent rotation; s03–08 follow the drive path; s09–13 follow coasting; s14 isolates bearing support; s15 is a labeled renewed-drive demonstration; s16 repeats the opening with its hidden cause visible. Macro views explicitly enlarge clearance and slow timing.
- attention: orange input cue, blue pawl/contact, teal output. Introduce geometry before its motion; stabilize contact framing; result holds have no competing camera/title animation.
- sound: material travel/contact at designed interaction; coupled movement shares onset; editorial cue at section inspection only. Bearing reading and final explanatory holds intentionally quiet under speech. All cue times resolve after measured audio.
- evidence: C1–C7 in ../SOURCES.md, primary topology A and manufacturer function B. Tooth count, angle, spacing and timing illustrative.

'''
 write(V/'STORYBOARD.md',doc)
print(json.dumps(dict(mode='animation' if animated else 'static',scenes=len(plan),events=len(events))))
