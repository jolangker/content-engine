"""One illustrated mechanism, static poses first and analytic motion after review."""
from pathlib import Path
import json,math,html,sys
V=Path(__file__).resolve().parent; animated='--animate' in sys.argv
raw=json.loads((V/('timing.json' if animated else 'scene-plan.json')).read_text(encoding='utf-8'));plan=raw['scenes'] if isinstance(raw,dict) else raw
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def esc(s):return html.escape(str(s),quote=True)
CSS="""@font-face{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:200 800}@font-face{font-family:Plex;src:url('assets/fonts/ibm-plex-mono.ttf')}*{box-sizing:border-box}#root{position:absolute;inset:0;color:#172B3B;font-family:Manrope,sans-serif}.scene{position:absolute;inset:0;background:#ECEEE9}.title{position:absolute;left:108px;top:205px;width:800px;margin:0;font-size:70px;line-height:1.1;font-weight:800;letter-spacing:-2.5px}.stage{position:absolute;left:90px;top:455px;width:900px;height:935px}.stage svg{width:100%;height:100%;overflow:hidden}.note{position:absolute;left:108px;top:1380px;width:810px;font:28px/1.3 Plex,monospace;color:#536775}.pose-caption{position:absolute;left:108px;top:1500px;width:848px;text-align:center;font:600 46px/1.3 Manrope,sans-serif}.pose-caption span{display:inline-block;background:#F8F9F5;padding:18px 26px;border-radius:14px;max-width:848px}svg .edge{stroke:#172B3B;stroke-width:2.3;stroke-linejoin:round}svg .label{font:25px Manrope,sans-serif;fill:#172B3B}svg .leader{fill:none;stroke:#536775;stroke-width:2}svg .arrow{fill:none;stroke:#C94422;stroke-width:5;stroke-linecap:round}"""
def defs(i):return f'''<defs><linearGradient id="{i}-metal" x2=".7" y2="1"><stop stop-color="#F8F9F5"/><stop offset=".45" stop-color="#BAC8CE"/><stop offset="1" stop-color="#748B98"/></linearGradient><linearGradient id="{i}-blue" x2="1" y2="1"><stop stop-color="#9CBCE6"/><stop offset=".6" stop-color="#2459C4"/><stop offset="1" stop-color="#173F83"/></linearGradient><linearGradient id="{i}-orange" x2=".5" y2="1"><stop stop-color="#E9B297"/><stop offset=".55" stop-color="#C94422"/><stop offset="1" stop-color="#8A301E"/></linearGradient><linearGradient id="{i}-teal" x2=".6" y2="1"><stop stop-color="#B3D5D0"/><stop offset=".55" stop-color="#4F9398"/><stop offset="1" stop-color="#167580"/></linearGradient></defs>'''
def gear(i,name,x,y,r,n=16,color='metal'):
 pts=[]
 for k in range(n):
  for q,rr in [(0,r*.86),(.2,r),(.6,r),(.8,r*.86)]:
   a=(k+q)*math.tau/n;pts.append(f'{rr*math.cos(a):.4f},{rr*math.sin(a):.4f}')
 path='M'+'L'.join(pts)+'Z'
 pin=f'<circle cx="{r*.65}" cy="0" r="{max(9,r*.12)}" fill="url(#{i}-orange)" class="edge"/>' if name=='disc' else ''
 return f'<g transform="translate({x} {y})"><g id="{i}-{name}"><path d="{path}" transform="translate(0 9)" fill="#536775" class="edge"/><path d="{path}" fill="url(#{i}-{color})" class="edge"/><circle r="{r*.57}" fill="none" stroke="#F8F9F5" stroke-width="3" opacity=".65"/><path d="M0 0V{-r*.65}" stroke="#172B3B" stroke-width="7" stroke-linecap="round"/><circle r="12" fill="url(#{i}-metal)" class="edge"/>{pin}</g></g>'
def fan(i):
 spokes=''.join(f'<path d="M0 -213V213" transform="rotate({k*20})" stroke="#536775" stroke-width="3"/>' for k in range(9))
 blades=''.join(f'<path d="M-10 -18C-140 -157 -108 -230 -26 -200C58 -170 68 -66 14 -7Z" transform="rotate({k*120})" fill="url(#{i}-teal)" class="edge"/>' for k in range(3))
 return f'''<ellipse cx="450" cy="838" rx="265" ry="27" fill="#172B3B" opacity=".1"/><path d="M391 567H509L538 797H362Z" fill="#536775" class="edge"/><path d="M402 565H498L517 797H383Z" fill="url(#{i}-metal)" class="edge"/><path d="M285 795Q450 752 615 795V831Q450 875 285 831Z" fill="url(#{i}-metal)" class="edge"/><g id="{i}-fanhead"><path d="M432 515H468V581H432Z" fill="url(#{i}-blue)" class="edge"/><ellipse cx="470" cy="335" rx="228" ry="237" fill="#536775" class="edge"/><ellipse cx="450" cy="320" rx="228" ry="237" fill="#F8F9F5" stroke="#172B3B" stroke-width="9"/><g transform="translate(450 320)"><g id="{i}-blades">{blades}</g>{spokes}<circle r="213" fill="none" stroke="#536775" stroke-width="5"/><circle r="160" fill="none" stroke="#536775" stroke-width="2"/><circle r="105" fill="none" stroke="#536775" stroke-width="2"/><circle r="39" fill="url(#{i}-metal)" class="edge"/><circle r="12" fill="#172B3B"/></g><path d="M658 306H731V356H658Z" fill="url(#{i}-metal)" class="edge"/><g id="{i}-knob"><path d="M705 263V308" stroke="#536775" stroke-width="13"/><ellipse cx="705" cy="260" rx="24" ry="13" fill="url(#{i}-blue)" class="edge"/></g></g>'''
def side(i):
 blades=''.join(f'<path d="M0 0L-12 -156Q-53 -190 -57 -136L-23 0Z" transform="rotate({k*120})" fill="url(#{i}-teal)" class="edge"/>' for k in range(3))
 helix=''.join(f'<path d="M{x} 368q-16 18 0 37" fill="none" stroke="#8A301E" stroke-width="7"/>' for x in range(540,651,17))
 return f'''<ellipse cx="450" cy="727" rx="340" ry="25" fill="#172B3B" opacity=".1"/><path d="M402 480H455L473 694H382Z" fill="url(#{i}-metal)" class="edge"/><path d="M310 690H558V726H310Z" fill="url(#{i}-metal)" class="edge"/><path d="M280 300H540V470H280Z" fill="url(#{i}-teal)" class="edge"/><ellipse cx="540" cy="385" rx="31" ry="85" fill="#167580" class="edge"/><ellipse cx="280" cy="385" rx="31" ry="85" fill="url(#{i}-metal)" class="edge"/><path d="M163 385H658" stroke="#536775" stroke-width="20"/><path d="M163 379H658" stroke="#DCE5E3" stroke-width="6"/><g transform="translate(184 385)"><g id="{i}-blades">{blades}</g><circle r="23" fill="url(#{i}-metal)" class="edge"/></g><ellipse cx="184" cy="385" rx="72" ry="191" fill="none" stroke="#536775" stroke-width="9"/><path d="M540 368H660V405H540Z" fill="url(#{i}-orange)" class="edge"/>{helix}{gear(i,'wheel',618,478,64,16)}<path d="M618 478V565" stroke="#536775" stroke-width="16"/>{gear(i,'disc',618,578,82,20,'orange')}<g id="{i}-power"><path d="M285 220H529M565 220H710V534" fill="none" stroke="#C94422" stroke-width="5" stroke-dasharray="14 8"/><text x="278" y="185" class="label">poros motor</text></g><text x="118" y="634" class="label">baling-baling</text><text x="542" y="706" class="label">jalur ayunan</text>'''
def gears(i):
 helix=''.join(f'<path d="M{x} 165q-19 26 0 55" fill="none" stroke="#8A301E" stroke-width="8"/>' for x in range(170,570,27))
 return f'''<path d="M95 179H724V227H95Z" fill="#536775" class="edge"/><path d="M142 164H590V218H142Z" fill="url(#{i}-orange)" class="edge"/>{helix}<path d="M391 319V612" stroke="#536775" stroke-width="27"/><path d="M384 319V612" stroke="#CDD4D4" stroke-width="8"/>{gear(i,'wheel',390,323,110,20)}{gear(i,'spindle',390,563,62,12)}{gear(i,'disc',584,563,134,26,'orange')}<circle cx="584" cy="563" r="18" fill="#172B3B"/><g id="{i}-worm-mark"><path d="M188 163v54" stroke="#F8F9F5" stroke-width="6"/></g><path d="M152 736H746" stroke="#CDD4D4" stroke-width="3"/><text x="154" y="793" class="label">ulir</text><text x="318" y="793" class="label">poros gigi</text><text x="552" y="793" class="label">piringan</text>'''
def linkage(i,key):
 # O=(0,0), A=(140cos70,140sin70); C=(230,0) in moving head frame.
 bladeart=''.join(f'<path d="M-8 -10C-90 -115 -75 -142 -12 -123C45 -100 43 -45 8 -5Z" transform="rotate({k*120})" fill="url(#{i}-teal)" class="edge"/>' for k in range(3))
 housing=f'''<path d="M-179 -98Q-199 0 -179 98H217Q279 72 279 0Q279 -72 217 -98Z" transform="translate(0 13)" fill="#28616C" class="edge"/><path d="M-179 -98Q-199 0 -179 98H217Q279 72 279 0Q279 -72 217 -98Z" fill="url(#{i}-teal)" fill-opacity=".32" class="edge"/><path d="M-179 -81V81" stroke="#172B3B" stroke-width="11"/><path d="M-232 -138V138" stroke="#536775" stroke-width="11"/><ellipse cx="-232" cy="0" rx="37" ry="143" fill="#F8F9F5" stroke="#536775" stroke-width="5"/><g transform="translate(-232 0) scale(.25 1)"><g id="{i}-blades">{bladeart}</g></g><path d="M-169 0H186" stroke="#A6B4BE" stroke-width="16"/>{gear(i,'carrier',230,0,85,24,'orange')}<path id="{i}-crank-radius" d="M230 0H285" stroke="#8A301E" stroke-width="6"/>'''
 fixed=f'''<path d="M-69 208H143L126 250H-88Z" fill="#536775" class="edge"/><path d="M-54 0L68 0L99 225H-68Z" fill="url(#{i}-metal)" class="edge"/><path d="M0 0L47.883 131.557" stroke="#536775" stroke-width="42" stroke-linecap="round"/><path d="M0 -7L47.883 124.557" stroke="url(#{i}-metal)" stroke-width="28" stroke-linecap="round"/>'''
 return fixed+f'''<g id="{i}-head">{housing}</g><path id="{i}-rod-back" d="M48 142L270 68" fill="none" stroke="#173F83" stroke-width="28" stroke-linecap="round"/><path id="{i}-rod" d="M48 132L270 58" fill="none" stroke="url(#{i}-blue)" stroke-width="25" stroke-linecap="round"/><path id="{i}-rod-shine" d="M48 126L270 52" fill="none" stroke="#9CBCE6" stroke-width="4"/><circle cx="47.883" cy="131.557" r="18" fill="url(#{i}-metal)" class="edge"/><circle cx="47.883" cy="131.557" r="7" fill="#2459C4"/><circle id="{i}-pin" cx="270" cy="58" r="16" fill="url(#{i}-orange)" class="edge"/><circle r="25" fill="url(#{i}-metal)" class="edge"/><circle r="9" fill="#172B3B"/><path d="M-1 25L-160 250" class="leader"/><text x="-245" y="285" class="label">poros kepala</text><path d="M48 152L70 292" class="leader"/><text x="-30" y="329" class="label">jangkar tetap</text><g id="{i}-length"><path id="{i}-measure" d="M48 169L270 95" stroke="#2459C4" stroke-width="2" stroke-dasharray="7 6"/></g>'''
def clutch(i):
 teeth=''.join(f'<path d="M{x} 359v20h15v-20" fill="url(#{i}-orange)" class="edge"/>' for x in range(342,532,30))
 lower=''.join(f'<path d="M{x} 413v-20h15v20" fill="url(#{i}-metal)" class="edge"/>' for x in range(357,547,30))
 return f'''<path d="M445 218V685" stroke="#536775" stroke-width="28"/><path d="M437 218V685" stroke="#DCE5E3" stroke-width="8"/><g id="{i}-upper"><path d="M342 315H552V359H342Z" fill="url(#{i}-orange)" class="edge"/>{teeth}<path d="M447 190V315" stroke="#536775" stroke-width="17"/><ellipse cx="447" cy="187" rx="74" ry="25" fill="url(#{i}-blue)" class="edge"/></g><path d="M342 414H552V458H342Z" fill="url(#{i}-metal)" class="edge"/>{lower}{gear(i,'disc',447,594,141,24,'orange')}<text x="170" y="807" class="label">kopling ditunjukkan secara konsep</text>'''
notes={'whole':'Kipas mekanis · contoh skematis','side':'Dua jalur dari poros yang sama','gear':'Rangkaian disederhanakan · gerak diperlambat','disc':'Pin di luar pusat piringan','link':'Tampak atas · poros dan jangkar tetap','macro':'Gerak diperlambat · batang kaku','clutch':'Kopling konseptual · bukan detail rakitan','proof':'Penyebab tersembunyi kini terlihat'}
RUNTIME=r'''
const clamp=(x)=>Math.max(0,Math.min(1,x));
const rad=Math.PI/180;
function closure(theta){const px=230+55*Math.cos(theta),py=55*Math.sin(theta),p=Math.hypot(px,py),gamma=Math.atan2(py,px);const phi=70*rad-gamma-Math.acos((p*p+140*140-220*220)/(2*p*140));const x=px*Math.cos(phi)-py*Math.sin(phi),y=px*Math.sin(phi)+py*Math.cos(phi);return {theta,phi,x,y,Cx:230*Math.cos(phi),Cy:230*Math.sin(phi),length:Math.hypot(x-140*Math.cos(70*rad),y-140*Math.sin(70*rad))};}
const el=n=>document.getElementById(id+'-'+n);
function attr(n,a,v){const e=el(n);if(e)e.setAttribute(a,v)}
function renderAt(t){const u=clamp((t-.3)/(duration-.6));let theta=phase+travel*u;let stop=false,open=0;
if(key==='clutch'){const q=clamp((u-.12)/.35);open=q;theta=phase+travel*Math.min(u,.12);stop=u>.12;}
if(key==='blade'){theta=phase;stop=true;open=1;}
if(key==='engage'){open=1-clamp((u-.08)/.2);theta=phase+travel*clamp((u-.35)/.65);stop=u<.35;}
const s=closure(theta);attr('head','transform','rotate('+(s.phi/rad)+')');attr('carrier','transform','rotate('+(theta/rad)+' 0 0)');
const Ax=140*Math.cos(70*rad),Ay=140*Math.sin(70*rad);
for(const [n,dy] of [['rod',0],['rod-back',11],['rod-shine',-6],['measure',35]])attr(n,'d','M'+Ax+' '+(Ay+dy)+'L'+s.x+' '+(s.y+dy));
attr('pin','cx',key==='eccentric'?230+55*Math.cos(theta):s.x);attr('pin','cy',key==='eccentric'?55*Math.sin(theta):s.y);if(key==='eccentric')attr('head','transform','rotate(0)');attr('crank-radius','d','M230 0L'+(230+55*Math.cos(theta))+' '+(55*Math.sin(theta)));
attr('blades','transform','rotate('+(t*290)+' 0 0)');
attr('fanhead','transform','translate('+(Math.sin(s.phi)*45)+' 0) translate(450 320) scale('+(1-Math.abs(Math.sin(s.phi))*.32)+' 1) translate(-450 -320)');
attr('wheel','transform','rotate('+(-theta/rad*134/62)+')');attr('spindle','transform','rotate('+(-theta/rad*134/62)+')');attr('disc','transform','rotate('+(theta/rad)+')');
attr('worm-mark','transform','translate('+(t*50%27)+' 0)');attr('upper','transform','translate(0 '+(14-open*87)+')');attr('knob','transform','translate(0 '+(-open*38)+')');
window.__mechanism=Object.assign({scene:id,time:t,stop,clutchOpen:open},s);
}
'''
travels=[math.tau,1.2,1.4,1.2,1.6,1.1,1.1,2,1.1,1.5,1.2,1.1,.9,0,1.9,math.tau]
phases=[];phase=0
for k,travel in enumerate(travels):
 phases.append(phase)
 phase+=travel*.12 if k==12 else 0 if k==13 else travel
events=[]
for n,s in enumerate(plan):
 i=s['id'];key=s['key'];d=s['duration'];view=s['view'];vb='0 0 900 900'
 if view=='whole':art=fan(i)
 elif view=='side':art=side(i);vb='0 130 790 818'
 elif view=='gear':art=gears(i);vb='80 90 700 725'
 elif view=='clutch':art=clutch(i);vb='140 65 630 755'
 else:
  art=linkage(i,key);vb='-280 -255 620 640'
  if view=='disc':vb='125 -110 220 228';art=gear(i,'carrier',230,0,85,24,'orange')+f'<path id="{i}-crank-radius" d="M230 0H285" stroke="#8A301E" stroke-width="6"/><circle id="{i}-pin" r="16" fill="url(#{i}-orange)" class="edge"/>';art=art.replace(f'<circle id="{i}-pin" r="16" fill="url(#{i}-orange)" class="edge"/>','');art=f'<g id="{i}-head">'+art+'</g>'+f'<circle id="{i}-pin" r="16" fill="url(#{i}-orange)" class="edge"/>'
  if view=='macro':vb='-109 -185 460 475';art=art.replace(f'<text x="-245" y="285" class="label">poros kepala</text>','')
  if view=='proof':vb='-280 -255 620 640'
  if key in ['anchor','pivot']:art=art.replace(f'<g id="{i}-head">',f'<g id="{i}-head" opacity=".28">')
  if key=='rod':art=art.replace(f'<g id="{i}-head">',f'<g id="{i}-head" opacity=".65">')
 if view=='proof':art+=f'<text x="-251" y="-207" class="label">baling-baling searah</text>'
 spoken=' '.join(s['text'].split()[:5])
 caption='' if animated else f'<div class="pose-caption"><span>{esc(spoken)}</span></div>'
 script=f"const id={json.dumps(i)},key={json.dumps(key)},duration={d},phase={phases[n]},travel={travels[n]};\n"+RUNTIME
 if animated:script+="\nconst clock={t:0};const tl=gsap.timeline({paused:true});tl.fromTo(clock,{t:0},{t:duration,duration:duration,ease:'none',onUpdate:()=>renderAt(clock.t)},0);renderAt(0);window.__timelines[id]=tl;"
 else:script+=f'\nrenderAt({d*.55});'
 stillattr='' if animated else ' data-no-timeline="true"'
 body=f'''<template><style>{CSS}</style><div id="root" data-composition-id="{i}" data-width="1080" data-height="1920"{stillattr}><div class="scene"><h1 class="title">{esc(s['title'])}</h1><div class="stage"><svg viewBox="{vb}" role="img" aria-label="{esc(s['job'])}">{defs(i)}{art}</svg></div><div class="note">{esc(notes[view])}</div>{caption}</div></div><script>{script}</script></template>'''
 write(V/f'compositions/{i}.html',body)
 if animated:
  role='editorial' if key in ['branch','anchor','pivot'] else 'metal' if key in ['rod','clutch','engage'] else 'travel'
  onset=.12 if key=='clutch' else .28 if key=='engage' else 0
  events.append(dict(scene=i,time=round((s['start']+.3+(d-.6)*onset)*30)/30,role=role,action=f'{key}: '+s['job']))
hosts='\n'.join(f'<div id="{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-start="{s["start"]:.9f}" data-duration="{s["duration"]:.9f}" data-width="1080" data-height="1920" data-track-index="1" data-track-kind="graphics"'+(' data-no-timeline="true"' if not animated else '')+'></div>' for s in plan)
audio=''
if animated:
 caps=json.loads((V/'caption-groups.json').read_text(encoding='utf-8'))
 groups=''.join(f'<div id="cap-{n:03}" class="clip" data-start="{g["start"]:.9f}" data-duration="{g["end"]-g["start"]:.9f}" style="position:absolute;inset:0"><div class="pose-caption"><span>{esc(g["text"])}</span></div></div>' for n,g in enumerate(caps))
 write(V/'compositions/captions.html',f'<template><style>{CSS}</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920">{groups}</div><script>window.__timelines["captions"]=gsap.timeline({{paused:true}});</script></template>')
 hosts+='<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="90" data-width="1080" data-height="1920" data-track-index="2" data-track-kind="captions"></div>'
 audio='<audio id="narration" class="clip" src="assets/audio/narration-master.wav" data-start="0" data-duration="90" data-volume="1" data-track-index="3"></audio>'
 write(V/'motion-events.json',json.dumps(events,indent=2)+'\n')
root=f'''<!doctype html><html lang="id" data-composition-variables='[{{"id":"ink","type":"color","label":"Engineering ink","default":"#172B3B"}}]'><head><meta charset="utf-8"><title>Kipas: putaran jadi ayunan</title><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>html,body{{margin:0;padding:0;background:#ECEEE9}}#root{{position:relative;width:1080px;height:1920px;overflow:hidden}}.clip{{position:absolute;inset:0}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="90" data-width="1080" data-height="1920">{hosts}{audio}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines.main=gsap.timeline({{paused:true}});</script></body></html>'''
write(V/'index.html',root)
print(json.dumps(dict(animated=animated,scenes=len(plan))))
