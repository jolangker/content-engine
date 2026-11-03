"""Original shaded 2.5D pin-pivot cork puller; every frame derives from state."""
from pathlib import Path
import json,sys,html,math
V=Path(__file__).resolve().parent;posed='--posed' in sys.argv
timing=json.loads((V/'timing.json').read_text()) if (V/'timing.json').exists() else None
plan=timing['scenes'] if timing else json.loads((V/'scene-plan.json').read_text())
def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def dump(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
css="""@font-face{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:200 800}@font-face{font-family:Plex;src:url('assets/fonts/ibm-plex-mono.ttf')}*{box-sizing:border-box}#root{position:absolute;inset:0;color:#172B3B;font-family:Manrope,sans-serif}.scene{position:absolute;inset:0;background:#ECEEE9}.title{position:absolute;left:108px;top:205px;width:810px;margin:0;font:800 68px/1.1 Manrope,sans-serif;letter-spacing:-2.5px}.stage{position:absolute;left:80px;top:430px;width:920px;height:980px}.stage svg{width:100%;height:100%;overflow:hidden}.note{position:absolute;left:108px;top:1420px;width:810px;font:28px/1.25 Plex,monospace;color:#536775}.pose-caption,.phrase{position:absolute;left:108px;top:1500px;width:848px;text-align:center;font:600 46px/1.3 Manrope,sans-serif}.pose-caption span,.phrase span{display:inline-block;max-width:848px;background:#F8F9F5;padding:18px 26px;border-radius:14px}.edge{stroke:#172B3B;stroke-width:2.5;stroke-linejoin:round}.anno{fill:#172B3B;font-family:Manrope,sans-serif;font-weight:600}.leader{stroke:#536775;fill:none;stroke-width:1.6}.arrow{stroke-width:5;fill:none;stroke-linecap:round;stroke-linejoin:round}"""
views={'whole':'130 55 740 790','proof':'130 55 740 790','head':'310 185 380 300','shaft':'390 55 220 650','base':'300 390 400 380','worm':'390 440 220 270','cork':'365 450 270 300','guide':'400 220 200 310','rings':'410 185 180 250','pin':'300 205 400 240','macro':'380 225 240 170','lever':'150 180 700 420'}
poses=[.62,.65,.6,.7,.65,.7,.6,.72,.65,.7,.65,.7,.7,.72,.8,.7]
js=r"""
const id=IDENT,key=KEY,duration=DURATION,posed=POSED,pose=POSE;
const clamp=x=>Math.max(0,Math.min(1,x)),ramp=(u,a,b)=>clamp((u-a)/(b-a));
const el=n=>document.getElementById(id+'-'+n),attr=(n,a,v)=>{const z=el(n);if(z)z.setAttribute(a,v)};
function model(u){let q=0,grip=0,phase=0,cover=0,cork=0,seat=0;
 if(['mystery','discover','drive','lever','reaction','lift','clear','proof'].includes(key)){const ranges={drive:[1.39,1.10],lever:[1.10,.85],reaction:[.85,.65],lift:[.65,.18],clear:[.18,-.35]},ab=ranges[key]||[1.39,-.35];q=ab[0]+(ab[1]-ab[0])*ramp(u,key==='clear'?.12:.18,key==='clear'?.65:.84);grip=1;phase=88.96/30*2*Math.PI;cork=64*q-88.96;}
 if(key==='mystery')cover=.85;
 if(key==='orient'){q=.8;phase=5;grip=.6;}
 if(key==='seat'){q=0;seat=30*(1-ramp(u,.15,.7));}
 if(key==='turn'){q=.7*ramp(u,.14,.84);phase=q*64/30*2*Math.PI;grip=q/1.39;}
 if(key==='grip'){q=.7+.25*ramp(u,.18,.85);phase=q*64/30*2*Math.PI;grip=q/1.39;}
 if(key==='guide'){q=.95+.18*ramp(u,.15,.85);phase=q*64/30*2*Math.PI;grip=q/1.39;}
 if(key==='rise'){q=1.13+.26*ramp(u,.15,.85);phase=q*64/30*2*Math.PI;grip=q/1.39;}
 if(['rings','pivot'].includes(key)){q=1.39;phase=88.96/30*2*Math.PI;grip=1;}
 const d=64*q;return {q,d,phase,grip,cover,cork,seat,leftAngle:q*180/Math.PI,rightAngle:-q*180/Math.PI};
}
function helix(phase){let p='';for(let i=0;i<=220;i++){const f=i/220,x=500+24*Math.sin(f*Math.PI*8+phase),y=470+120*f;p+=(i?'L':'M')+x.toFixed(3)+' '+y.toFixed(3);}return p;}
function renderAt(t){let u=posed?pose:clamp((t-.16)/(duration-.48)),s=model(u);attr('shaft','transform',`translate(0 ${s.d-s.seat})`);attr('worm','d',helix(s.phase));attr('worm-back','d',helix(s.phase));attr('left','transform',`rotate(${s.leftAngle} 406 300)`);attr('right','transform',`rotate(${s.rightAngle} 594 300)`);attr('cork','transform',`translate(0 ${s.cork})`);attr('assembly','transform',`translate(0 ${-s.seat})`);attr('cover','opacity',s.cover);attr('turn-arrow','opacity',['turn','grip'].includes(key)?1:0);attr('up-arrow','opacity',['mystery','discover','drive','lift','clear','proof'].includes(key)?1:0);attr('down-arrow','opacity',['turn','guide','rise'].includes(key)?1:0);attr('rim-focus','opacity',['seat','reaction','proof'].includes(key)?.8:0);attr('pin-focus','opacity',key==='pivot'?.85:0);attr('mesh-focus','opacity',['discover','drive'].includes(key)?.55:0);attr('worm-focus','opacity',['grip','lift'].includes(key)?.35:0);
 window.__mechanismStates=window.__mechanismStates||{};window.__mechanismStates[id]=s;
}
renderAt(0);const clock={t:0},tl=gsap.timeline({paused:true});tl.to(clock,{t:duration,duration:duration,ease:'none',onUpdate:()=>renderAt(clock.t)},0);window.__timelines=window.__timelines||{};window.__timelines[id]=tl;
"""
story='---\nformat: 1080x1920\nduration: 90s\nmessage: Wing sectors raise an engaged cork through a guided shaft.\narc: mystery → hidden teeth → insertion → fixed support → extraction proof\naudience: Indonesian general viewers\nmode: autonomous\n---\n\n'
events=[]
for i,s in enumerate(plan):
 ident=s['id'];key=s['key'];view=s['view'];g=lambda n:f'{ident}-{n}'
 grad=''.join(f'<linearGradient id="{g(n)}" x2="1" y2=".4"><stop stop-color="{a}"/><stop offset=".48" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></linearGradient>' for n,a,b,c in [('metal','#F0F3EF','#A6B4BE','#637C8C'),('blue','#A4C2EC','#2459C4','#173D81'),('orange','#EEB492','#C94422','#8B2A15'),('glass','#E8EEE5','#B4CBC2','#638D86'),('corkmat','#E9CC91','#BA8C50','#8B6337')])
 # Annular groove pitch matches the sampled sector teeth; teeth remain visible in the contact macro.
 pitch=math.pi*2*64/32
 grooves=''.join(f'<path d="M470 {205+j*pitch:.4f}Q500 {214+j*pitch:.4f} 530 {205+j*pitch:.4f}" fill="none" stroke="#526A79" stroke-width="4"/>' for j in range(20))
 def gear(cx):
  pts=[]
  for j in range(32*4):
   a=j*math.pi/64;r=[59,67,67,59][j%4];pts.append((cx+r*math.cos(a),300+r*math.sin(a)))
  # Full gear circle is visually masked to sector arc facing shaft; its unneeded part stays beneath lever heel.
  path='M'+'L'.join(f'{x:.3f} {y:.3f}' for x,y in pts)+'Z'
  return f'<path d="{path}" transform="translate(7 7)" fill="#173D81" class="edge"/><path d="{path}" fill="url(#{g("blue")})" class="edge"/>'
 corkspecks=''.join(f'<path d="M{466+(j*17)%63} {599+(j*23)%73}l{3+j%4} {1+j%3}" stroke="#76552F" stroke-width="2" opacity=".45"/>' for j in range(32))
 labels=''
 mapping={
 'head':[(320,190,'sektor gigi',384,260),(520,455,'batang beralur',504,393)],
 'shaft':[(405,183,'alur',478,240),(405,690,'spiral',480,562)],
 'base':[(323,470,'badan tetap',429,510),(323,743,'bibir botol',447,593)],
 'worm':[(400,466,'putaran masuk',475,553)],
 'cork':[(375,732,'spiral tertanam',485,620)],
 'guide':[(408,229,'lubang pemandu',462,350)],
 'rings':[(418,203,'alur melingkar',478,290)],
 'pin':[(315,218,'poros tetap',406,300)],
 'macro':[(386,240,'gigi → batang',470,300)],
 'lever':[(170,192,'tekan di ujung',270,420)]}
 for x,y,text,tx,ty in mapping.get(view,[]):
  fs={'head':14,'shaft':20,'base':15,'worm':9,'cork':10,'guide':10,'rings':8,'pin':15,'macro':9,'lever':24}[view]
  labels+=f'<text x="{x}" y="{y}" font-size="{fs}" class="anno">{text}</text><path d="M{x+fs*2} {y+8}L{tx} {ty}" class="leader"/>'
 # Body struts behind gear and shaft; throat cutout reveals internal parts.
 svg=f'''<svg viewBox="{views[view]}" role="img" aria-label="{s['title']}" data-layout-allow-overlap="true"><defs>{grad}<clipPath id="{g('leftsector')}"><path d="M406 300L371 239A70 70 0 0 1 441 361Z"/></clipPath><clipPath id="{g('rightsector')}"><path d="M594 300L559 361A70 70 0 0 1 629 239Z"/></clipPath></defs>
 <ellipse cx="500" cy="822" rx="245" ry="17" fill="#172B3B" opacity=".1"/>
 <path d="M428 590V750Q400 770 350 800H650Q600 770 572 750V590Z" transform="translate(9 8)" fill="#638D86" class="edge"/>
 <path d="M428 590V750Q400 770 350 800H650Q600 770 572 750V590Z" fill="url(#{g('glass')})" class="edge"/>
 <path d="M449 591V745M551 591V745" stroke="#536775" stroke-width="4"/><path d="M449 598H551V738H449Z" fill="#F8F9F5" opacity=".9"/>
 <g id="{g('assembly')}"><path d="M431 301L419 568H581L569 301" fill="none" stroke="#536775" stroke-width="24"/><path d="M425 300L413 562H575L563 300" fill="none" stroke="url(#{g('metal')})" stroke-width="19"/>
 <path d="M447 550H553L566 590H434ZM458 553L449 587H551L542 553Z" fill="url(#{g('metal')})" fill-rule="evenodd" class="edge"/>
 <g id="{g('cork')}"><rect x="458" y="590" width="84" height="90" rx="5" fill="url(#{g('corkmat')})" class="edge"/>{corkspecks}<path d="M461 594H539" stroke="#F2DFAE" stroke-width="5"/></g>
 <rect x="454" y="261" width="92" height="128" rx="15" fill="url(#{g('metal')})" class="edge"/><path d="M468 267H532V390H468Z" fill="#D2DAD5"/>
 <g id="{g('shaft')}"><path d="M480 151H520V465H480Z" transform="translate(7 7)" fill="#536775" class="edge"/><rect x="470" y="155" width="60" height="300" rx="14" fill="url(#{g('metal')})" class="edge"/>{grooves}
 <path d="M500 100V160" stroke="#A6B4BE" stroke-width="20"/>
 <path d="M440 64H560L548 113H452Z" transform="translate(7 7)" fill="#8B2A15" class="edge"/><path d="M440 64H560L548 113H452Z" fill="url(#{g('orange')})" class="edge"/><path d="M464 78H536L532 96H468Z" fill="#ECEEE9" stroke="#172B3B" stroke-width="2"/>
 <path id="{g('worm-back')}" transform="translate(5 4)" fill="none" stroke="#536775" stroke-width="10"/><path id="{g('worm')}" fill="none" stroke="url(#{g('metal')})" stroke-width="8" stroke-linecap="round"/><path d="M500 455V470" stroke="#536775" stroke-width="11"/>
 </g>
 <g id="{g('left')}"><g clip-path="url(#{g('leftsector')})">{gear(406)}</g><path d="M406 300Q385 296 370 330L214 512Q200 530 218 548Q237 563 251 541L425 330Z" transform="translate(8 8)" fill="#536775" class="edge"/><path d="M406 300Q385 296 370 330L214 512Q200 530 218 548Q237 563 251 541L425 330Z" fill="url(#{g('metal')})" class="edge"/><path d="M223 515L267 462" stroke="url(#{g('orange')})" stroke-width="26" stroke-linecap="round"/></g>
 <g id="{g('right')}"><g clip-path="url(#{g('rightsector')})">{gear(594)}</g><path d="M594 300Q615 296 630 330L786 512Q800 530 782 548Q763 563 749 541L575 330Z" transform="translate(8 8)" fill="#536775" class="edge"/><path d="M594 300Q615 296 630 330L786 512Q800 530 782 548Q763 563 749 541L575 330Z" fill="url(#{g('metal')})" class="edge"/><path d="M777 515L733 462" stroke="url(#{g('orange')})" stroke-width="26" stroke-linecap="round"/></g>
 <circle cx="413" cy="307" r="18" fill="#536775" class="edge"/><circle cx="406" cy="300" r="18" fill="url(#{g('metal')})" class="edge"/><path d="M398 300H414" stroke="#172B3B" stroke-width="3"/><circle cx="601" cy="307" r="18" fill="#536775" class="edge"/><circle cx="594" cy="300" r="18" fill="url(#{g('metal')})" class="edge"/><path d="M586 300H602" stroke="#172B3B" stroke-width="3"/>
 </g>
 <path id="{g('cover')}" d="M454 260H546V390H454Z" fill="url(#{g('metal')})" class="edge"/>
 <path id="{g('rim-focus')}" d="M432 590H568" stroke="#C94422" stroke-width="6"/>
 <g id="{g('pin-focus')}" stroke="#C94422" stroke-width="4" fill="none"><circle cx="406" cy="300" r="23"/><circle cx="594" cy="300" r="23"/></g>
 <g id="{g('mesh-focus')}" fill="#2459C4"><ellipse cx="470" cy="300" rx="7" ry="14"/><ellipse cx="530" cy="300" rx="7" ry="14"/></g>
 <ellipse id="{g('worm-focus')}" cx="500" cy="625" rx="32" ry="36" fill="#2459C4"/>
 <path id="{g('turn-arrow')}" d="M450 440Q500 420 550 440L539 429M550 440L536 450" class="arrow" stroke="#C94422"/>
 <path id="{g('up-arrow')}" d="M500 415V370M488 382L500 370L512 382" class="arrow" stroke="#167580"/>
 <path id="{g('down-arrow')}" d="M500 396V441M488 429L500 441L512 429" class="arrow" stroke="#C94422"/>
 {labels}</svg>'''
 cap=f'<div class="pose-caption"><span>{html.escape(" ".join(s["text"].split()[:6]))}</span></div>' if posed else ''
 note='Penampang / skematis / gerak diperlambat' if view not in ['whole','shaft'] else 'Contoh mekanisme bersayap / bukan skala'
 script=js.replace('IDENT',json.dumps(ident)).replace('KEY',json.dumps(key)).replace('DURATION',str(s['duration'])).replace('POSED',str(posed).lower()).replace('POSE',str(poses[i]))
 write(V/f'compositions/{ident}.html',f'<template><style>{css}</style><div id="root" data-composition-id="{ident}" data-width="1080" data-height="1920"><div class="scene"><h1 class="title" data-var-text="{key}">{s["title"]}</h1><div class="stage">{svg}</div><div class="note">{note}</div>{cap}</div></div><script>{script}</script></template>')
 story+=f'## Frame {i+1}: {s["title"]} ({s["start"]:.3f}–{s["end"]:.3f}s)\n\n- act: '+('Discovery and insertion' if i<9 else 'Extraction and proof')+f'\n- status: {"built" if posed else "animated"}\n- src: compositions/{ident}.html\n- duration: {s["duration"]:.6f}s\n- poster: {s["start"]+s["duration"]*.6:.6f}s\n- scene: {s["action"]}\n- voiceover: {s["text"]}\n- reads: title and orientation (0–1s); causal relation (1s to last0.5s); result hold (last0.5s)\n- sound: cue sheet below; no BGM\n\nQuestion: {s["title"]} Visible answer/new relation: {s["action"]} Next question follows the linked scene order. Source: S1 C1–C5; S2 cross-check. Function-first introduction; first discovery shot2, signature shot11, matched proof1/16. View: {view}, shaded layered2.5D. Stable landmarks: orange head, blue sectors, fixed pins, bottle rim. State enters/exits according to model; views preserve axes. Relevant motion is rotation→axial insertion or sector rotation→axial extraction; cork fixed during insertion, translated with worm during extraction. Attention leads with active color then carries to output. Diagnostic poses: progress .18/.5/.84 for approach/transfer/result. Bounds: useful subassembly fills80–95% stage; inactive context cropped in macro; complete contact and caption clearance preserved. Longer observation: shot11. Intentional silence: inspection holds; no invented friction chatter.\n\n'
 eventmap={'mystery':('hinge','wing-down'), 'discover':('metal','sector-drive'),'orient':('editorial','shaft-link'),'seat':('metal','base-seat'),'turn':('hinge','worm-turn'),'grip':('editorial','worm-engaged'),'guide':('editorial','guided-slide'),'rise':('hinge','wings-rise'),'rings':('editorial','annular-detail'),'pivot':('metal','pivot-support'),'drive':('metal','signature-drive'),'lever':('hinge','lever-pressure'),'reaction':('editorial','rim-reaction'),'lift':('hinge','cork-lift'),'clear':('editorial','cork-clear'),'proof':('metal','matched-drive')}
 asset,kind=eventmap[key];u={'seat':.7,'turn':.14,'guide':.15,'rise':.15,'clear':.65}.get(key,.18)
 events.append(dict(scene=ident,kind=kind,asset=asset,progress=u,start=round((s['start']+.16+u*(s['duration']-.48))*30)/30))
write(V/'STORYBOARD.md',story);dump(V/'motion-events.json',events)
hosts=''.join(f'<div id="{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-start="{s["start"]}" data-duration="{s["duration"]}" data-width="1080" data-height="1920" data-track-kind="graphics" data-track-index="1"></div>' for s in plan)
audio='';cap=''
if timing and not posed:
 caps=json.loads((V/'caption-groups.json').read_text());groups=''.join(f'<div id="cap-{i:03}" class="clip phrase" data-start="{c["start"]}" data-duration="{c["end"]-c["start"]}" data-layout-allow-caption-zone="true"><span>{html.escape(c["text"])}</span></div>' for i,c in enumerate(caps))
 write(V/'compositions/captions.html',f'<template><style>{css}</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920">{groups}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines.captions=gsap.timeline({{paused:true}});</script></template>')
 cap='<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="90" data-width="1080" data-height="1920" data-track-kind="captions" data-track-index="2" style="z-index:20"></div>'
 audio='<audio id="narration" class="clip" src="assets/audio/narration-master.wav" data-start="0" data-duration="90" data-track-index="3" data-volume="1"></audio>'
variables=[dict(id='canvas',type='color',label='Canvas',default='#ECEEE9')]+[dict(id=s['key'],type='string',label=s['title'],default=s['title']) for s in plan]
write(V/'index.html',f'<!doctype html><html lang="id" data-composition-variables=\'{json.dumps(variables,ensure_ascii=False)}\'><head><meta charset="utf-8"><title>Gabus: sayap dan gigi</title><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#ECEEE9}}.clip{{position:absolute;inset:0}}#root{{position:absolute;inset:0}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="90" data-width="1080" data-height="1920">{hosts}{cap}{audio}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines.main=gsap.timeline({{paused:true}});</script></body></html>')
print(json.dumps(dict(posed=posed,scenes=len(plan),events=len(events))))
