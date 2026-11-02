"""Author original layered 2.5D mechanism scenes from one deterministic state model."""
from pathlib import Path
import json,sys,shutil,html
V=Path(__file__).resolve().parent;R=V.parents[2]
posed='--posed' in sys.argv
timing=json.loads((V/'timing.json').read_text()) if (V/'timing.json').exists() else None
plan=timing['scenes'] if timing else json.loads((V/'scene-plan.json').read_text())
def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def dump(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
fonts=V/'assets/fonts';fonts.mkdir(parents=True,exist_ok=True)
for f in (R/'productions/ketel-uap-memutus-arus/video/assets/fonts').iterdir():shutil.copy2(f,fonts/f.name)
css="""@font-face{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:200 800}@font-face{font-family:Plex;src:url('assets/fonts/ibm-plex-mono.ttf')}*{box-sizing:border-box}#root{position:absolute;inset:0;color:#172B3B;font-family:Manrope,sans-serif}.scene{position:absolute;inset:0;background:#ECEEE9}.title{position:absolute;left:108px;top:205px;width:810px;font:800 70px/1.1 Manrope,sans-serif;letter-spacing:-2.5px;margin:0}.stage{position:absolute;left:80px;top:430px;width:920px;height:980px}.stage svg{width:100%;height:100%;overflow:hidden}.note{position:absolute;left:108px;top:1420px;width:810px;font:28px/1.25 Plex,monospace;color:#536775}.pose-caption{position:absolute;left:108px;top:1500px;width:848px;text-align:center;font:600 46px/1.3 Manrope,sans-serif}.pose-caption span{display:inline-block;max-width:848px;background:#F8F9F5;padding:18px 26px;border-radius:14px}.edge{stroke:#172B3B;stroke-width:2.5;stroke-linejoin:round}.fine{stroke:#536775;stroke-width:1.5;fill:none}.leader{stroke:#536775;stroke-width:2;fill:none}.anno{font-family:Manrope,sans-serif;font-weight:600;fill:#172B3B}.direction{stroke-width:6;fill:none;stroke-linecap:round;stroke-linejoin:round}"""
views={'whole':'110 135 920 740','section':'105 130 920 750','spring':'60 110 780 760','lock':'420 245 325 485','guide':'460 465 250 240','contact':'430 520 290 220','proof':'105 130 920 750'}
notes={'whole':'Tarik ke tahan ke lepaskan','section':'Sisi rumah dibuka / gerak diperlambat','spring':'Ruang pegas dibuka / skematis','lock':'Contoh pengunci geser / US5806202A','guide':'Satu sisi jalur diperlihatkan / diperbesar','contact':'Lenturan diperbesar / kecepatan ilustratif','proof':'Pegas menarik / pengunci menjepit'}
poseus=[.52,.8,.7,.7,.75,.65,.2,.7,.65,.9,.8,.8,.5,.75,.7,.82]
script=r"""
const id=ID,duration=DURATION,key=KEY,view=VIEW,posed=POSED,pose=POSE;
const clamp=x=>Math.max(0,Math.min(1,x)),ramp=(u,a,b)=>clamp((u-a)/(b-a));
const el=n=>document.getElementById(id+'-'+n),attr=(n,a,v)=>{const z=el(n);if(z)z.setAttribute(a,v)};
function model(u){let ext=300,lock=0,shell=0,load=1;
 if(key==='mystery'){ext=u<.3?70+230*ramp(u,.04,.3):u<.55?300-150*ramp(u,.32,.52):150+150*ramp(u,.55,.7);lock=ramp(u,.76,.9);shell=1;}
 if(key==='reveal'){ext=300;shell=1-ramp(u,.2,.65);}
 if(key==='pull'){ext=70+120*ramp(u,.16,.8);}
 if(key==='anchor'){ext=190+55*ramp(u,.18,.82);} if(key==='energy'){ext=245+55*ramp(u,.18,.82);}
 if(key==='return'){ext=300-230*ramp(u,.2,.82);}
 if(key==='question'){ext=300;shell=1;lock=.08;}
 if(key==='slider'){lock=.35*ramp(u,.17,.82);}
 if(key==='guide'){lock=.35+.3*ramp(u,.1,.85);}
 if(key==='touch'){lock=.65+.09*ramp(u,.15,.72);}
 if(key==='snap'){lock=.74+.26*ramp(u,.25,.7);}
 if(key==='clamp'){lock=1;}
 if(key==='held'){lock=1;}
 if(key==='unlock'){lock=1-ramp(u,.2,.78);}
 if(key==='rewind'){ext=300-230*ramp(u,.15,.85);}
 if(key==='proof'){ext=u<.2?70+230*ramp(u,0,.2):u<.7?300:300-230*ramp(u,.72,.94);lock=u<.7?ramp(u,.23,.38):1-ramp(u,.64,.72);shell=.12;}
 const contact=lock>=.74,flex=ramp(lock,.74,1);
 let px=620-54*Math.min(lock/.74,1)-20*flex,py=520+51*Math.min(lock/.74,1)+25*flex;
 const tipx=580-27*Math.min(lock/.74,1)-45*flex,tipy=Math.min(620,592+28*lock/.74);
 return {ext,lock,shell,contact,flex,px,py,tipx,tipy,angle:-ext/190*180/Math.PI,load:ext/300};
}
function spiral(ext){const pts=[];for(let i=0;i<=320;i++){const f=i/320,r=28+f*120,a=-Math.PI/2+f*Math.PI*10-(ext/190)*f*f;pts.push((i?'L':'M')+(410+r*Math.cos(a)).toFixed(3)+' '+(430+r*Math.sin(a)).toFixed(3));}return pts.join(' ');}
function renderAt(t){const u=posed?pose:clamp((t-.16)/(duration-.48)),s=model(u);
 attr('cover','opacity',s.shell);attr('annotations','opacity',s.shell>.5?0:1);attr('blade','width',270+s.ext);attr('blade-side','width',270+s.ext);attr('hook','transform',`translate(${680+s.ext} 0)`);
 attr('ticks-clip','width',270+s.ext);attr('ticks','transform',`translate(${s.ext} 0)`);attr('rotor','transform',`rotate(${s.angle} 410 430)`);
 attr('spring','d',spiral(s.ext));attr('spring-side','d',spiral(s.ext));
 const oa=-Math.PI/2+Math.PI*10-s.ext/190;attr('spring-end','cx',410+148*Math.cos(oa));attr('spring-end','cy',430+148*Math.sin(oa));
 attr('spring-view','opacity',view==='spring'?1:(key==='reveal'||key==='held'||key==='proof')?.86:0);
 const body=`M470 ${230+20*s.lock} Q650 ${245+20*s.lock} 650 ${435+25*s.lock} Q650 ${490+35*s.lock} ${s.px} ${s.py}`;
 attr('slider','d',body);attr('slider-side','d',body);attr('pad','transform',`translate(${-9*s.lock} ${38*s.lock})`);
 const tongue=`M${s.px} ${s.py} Q${s.px-8} ${s.py+28-12*s.flex} ${s.tipx+21} ${s.tipy-28+8*s.flex} L${s.tipx} ${s.tipy}`;
 attr('tongue','d',tongue);attr('tongue-side','d',tongue);attr('pin','cx',s.px);attr('pin','cy',s.py);attr('pin-side','cx',s.px+8);attr('pin-side','cy',s.py+7);
 attr('clamp-arrow','d',`M${s.tipx} 575V605M${s.tipx-9} 595L${s.tipx} 605L${s.tipx+9} 595`);attr('contact','cx',s.tipx);attr('contact','opacity',s.contact?.5:0);attr('clamp-arrow','opacity',s.contact&&s.shell<.5?1:0);
 attr('torque','opacity',['energy','held','proof'].includes(key)?.9:0);
 attr('input','opacity',(['pull','anchor'].includes(key)||(key==='mystery'&&(u<.3||u>.55&&u<.7))||(key==='proof'&&u<.2))?1:0);
 attr('output','opacity',(['return','rewind'].includes(key)||(key==='mystery'&&u>.32&&u<.52)||(key==='proof'&&u>.72))?1:0);
 attr('reel-main','opacity',view==='spring'?.12:1);
 const focus=(key==='guide'||key==='snap')?1:0;attr('guide-highlight','opacity',focus*.45);
 attr('shaft-focus','opacity',key==='anchor'?1:0);
 window.__mechanismStates=window.__mechanismStates||{};window.__mechanismStates[id]=s;
}
renderAt(0);
const clock={t:0},tl=gsap.timeline({paused:true});tl.to(clock,{t:duration,duration:duration,ease:'none',onUpdate:()=>renderAt(clock.t)},0);
window.__timelines=window.__timelines||{};window.__timelines[id]=tl;
"""
events=[];story='---\nformat: 1080x1920\nduration: 90s\nmessage: Spring return and a guided clamp control the same blade.\narc: mystery ke spring ke guided contact ke release ke matched proof\naudience: curious Indonesian general viewers\nmode: autonomous\n---\n\n'
for i,s in enumerate(plan):
 ident=s['id'];view=s['view'];g=lambda name:f'{ident}-{name}'
 grad=''.join(f'<linearGradient id="{g(n)}" x2="1" y2=".35"><stop stop-color="{a}"/><stop offset=".48" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></linearGradient>' for n,a,b,c in [('metal','#E8EFEC','#A6B4BE','#657B89'),('shell','#F8F9F5','#D7DFDB','#A6B4BE'),('blue','#A5C2EE','#2459C4','#173D81'),('orange','#EDAB8A','#C94422','#842C1B'),('tape','#F8E8B1','#DEC779','#B39543')])
 shell='M180 710V400A240 240 0 0 1 660 400V710Z'
 # Continuous reel with lower tangent blade, the brake is on the right at the mouth.
 ticks=''.join(f'<path d="M{x} 621v{13 if j%5 else 22}" stroke="#172B3B" stroke-width="2"/>' for j,x in enumerate(range(100,1100,15)))
 rings=''.join(f'<circle cx="410" cy="430" r="{r}" fill="none" stroke="{["#7D8C91","#D8DAB7"][j%2]}" stroke-width="6"/>' for j,r in enumerate(range(166,188,4)))
 strokes=''.join(f'<path d="M{675+j*3} {320+j*25}l23 6" stroke="#842C1B" stroke-width="5"/>' for j in range(4))
 annotations=''
 if view in ['section','proof']:
  reellabel='gaya pegas' if s['key'] in ['held','proof'] else 'gulungan pita'
  annotations=f'<text x="225" y="180" font-size="31" class="anno">{reellabel}</text><path d="M350 190L365 250" class="leader"/><text x="743" y="510" font-size="31" class="anno">pengunci</text><path d="M760 523L610 576" class="leader"/>'
 if view=='spring':
  annotations=f'<text x="125" y="180" font-size="29" class="anno">pegas pengembali</text><path d="M355 190L360 300" class="leader"/><text x="125" y="680" font-size="27" class="anno">poros tetap</text><path d="M300 670L410 443" class="leader"/><text x="490" y="680" font-size="27" class="anno">ke gulungan</text><path d="M550 650L540 510" class="leader"/>'
 if view=='guide':
  annotations=f'<text x="470" y="486" font-size="10" class="anno">jalur pin</text><path d="M520 490L598 544" class="leader" style="stroke-width:.8"/><text x="464" y="656" font-size="10" class="anno">tonjolan ke penahan</text><path d="M535 647L548 597" class="leader" style="stroke-width:.8"/>'
 if view=='contact':
  annotations=f'<text x="440" y="550" font-size="12" class="anno">lidah lentur</text><path d="M500 555L545 602" class="leader" style="stroke-width:.8"/><text x="440" y="705" font-size="12" class="anno">penopang tetap</text><path d="M535 695L530 648" class="leader" style="stroke-width:.8"/>'
 if view=='lock':
  annotations=f'<text x="435" y="290" font-size="14" class="anno">tombol luar</text><path d="M540 294L680 360" class="leader" style="stroke-width:1.2"/><text x="435" y="695" font-size="14" class="anno">pita →</text>'
 svg=f'''<svg viewBox="{views[view]}" role="img" aria-label="{s['title']}" data-layout-allow-overlap="true"><defs>{grad}<clipPath id="{g('blade-clip')}"><rect id="{g('ticks-clip')}" x="410" y="620" width="570" height="24"/></clipPath></defs>
 <ellipse cx="570" cy="754" rx="420" ry="25" fill="#172B3B" opacity=".10"/>
 <path d="{shell}" transform="translate(17 16)" fill="#536775" class="edge"/>
 <path d="{shell}" fill="url(#{g('shell')})" class="edge"/>
 <path d="M200 690V405A220 220 0 0 1 640 405V690Z" fill="#C9D3CF" stroke="#8C9BA1" stroke-width="2"/>
 <g id="{g('reel-main')}"><circle cx="424" cy="443" r="195" fill="#536775" class="edge"/><circle cx="410" cy="430" r="195" fill="url(#{g('metal')})" class="edge"/>{rings}<g id="{g('rotor')}"><circle cx="410" cy="430" r="156" fill="url(#{g('shell')})" class="edge"/><path d="M410 296V564M276 430H544" stroke="#A6B4BE" stroke-width="32"/><path d="M410 296V564M276 430H544" stroke="#E5EBE7" stroke-width="16"/><circle cx="410" cy="293" r="10" fill="#167580" class="edge"/></g></g>
 <g id="{g('spring-view')}"><circle cx="410" cy="430" r="171" fill="#F8F9F5" stroke="#536775" stroke-width="4"/><path id="{g('spring-side')}" transform="translate(6 6)" fill="none" stroke="#536775" stroke-width="8"/><path id="{g('spring')}" fill="none" stroke="url(#{g('blue')})" stroke-width="6"/><circle id="{g('spring-end')}" r="7" fill="#C94422" stroke="#172B3B" stroke-width="2"/></g>
 <circle cx="420" cy="439" r="27" fill="#536775" class="edge"/><circle cx="410" cy="430" r="27" fill="url(#{g('metal')})" class="edge"/><path d="M410 406V454" stroke="#172B3B" stroke-width="7"/><circle id="{g('shaft-focus')}" cx="410" cy="430" r="36" fill="none" stroke="#C94422" stroke-width="4"/>
 <rect id="{g('blade-side')}" x="410" y="636" height="8" width="570" fill="#947D3E" stroke="#172B3B" stroke-width="2"/>
 <rect id="{g('blade')}" x="410" y="620" height="18" width="570" fill="url(#{g('tape')})" stroke="#172B3B" stroke-width="2"/>
 <g clip-path="url(#{g('blade-clip')})"><g id="{g('ticks')}">{ticks}</g></g>
 <g id="{g('hook')}"><path d="M0 616L12 625V682H0Z" fill="#536775" class="edge"/><path d="M-16 616H0V680H-16Z" fill="url(#{g('metal')})" class="edge"/><circle cx="-8" cy="628" r="3" fill="#536775"/></g>
 <path d="M490 638H511V685H490ZM548 638H569V685H548ZM606 638H627V685H606Z" fill="url(#{g('metal')})" class="edge"/>
 <path d="M625 495Q610 548 580 571L548 590L538 587L548 604L558 599L588 571Q620 537 636 500Z" fill="#A6B4BE" class="edge"/>
 <path id="{g('guide-highlight')}" d="M625 495Q610 548 580 571L548 590L538 587L548 604L558 599" fill="none" stroke="#2459C4" stroke-width="8"/>
 <path d="M641 508Q627 563 600 585L565 613L566 620L578 620L608 596Q642 564 654 515Z" fill="#CAD2D1" class="edge"/>
 <path id="{g('slider-side')}" transform="translate(8 7)" fill="none" stroke="#173D81" stroke-width="18"/>
 <path id="{g('slider')}" fill="none" stroke="url(#{g('blue')})" stroke-width="15"/>
 <path id="{g('tongue-side')}" transform="translate(7 6)" fill="none" stroke="#173D81" stroke-width="12"/>
 <path id="{g('tongue')}" fill="none" stroke="url(#{g('blue')})" stroke-width="10"/>
 <circle id="{g('pin-side')}" r="12" fill="#536775" stroke="#172B3B" stroke-width="2"/><circle id="{g('pin')}" r="12" fill="url(#{g('metal')})" stroke="#172B3B" stroke-width="2"/>

 <g id="{g('cover')}"><path d="{shell}" fill="url(#{g('shell')})" class="edge"/><path d="M199 679V405A221 221 0 0 1 641 405V678Z" fill="none" stroke="#A6B4BE" stroke-width="12"/><circle cx="410" cy="430" r="106" fill="url(#{g('metal')})" class="edge"/><circle cx="410" cy="430" r="83" fill="#F8F9F5" stroke="#172B3B" stroke-width="2"/><path d="M365 430H455M410 386V474" stroke="#536775" stroke-width="9"/><path d="M185 655H270V708H185Z" fill="#536775"/></g>
 <g id="{g('pad')}"><path d="M658 302Q704 324 716 419L690 430Q689 352 647 331Z" fill="#842C1B" class="edge"/><path d="M647 294Q697 317 707 410L683 418Q676 347 638 324Z" fill="url(#{g('orange')})" class="edge"/>{strokes}<path d="M649 352L680 359" stroke="#172B3B" stroke-width="9"/></g>
 <ellipse id="{g('contact')}" cx="550" cy="620" rx="19" ry="4" fill="#C94422"/>
 <path id="{g('clamp-arrow')}" d="M505 575V605M496 595L505 605L514 595" class="direction" stroke="#C94422"/>
 <path id="{g('torque')}" d="M325 353A119 119 0 0 1 518 447L508 430M518 447L532 434" class="direction" stroke="#C94422"/>
 <path id="{g('input')}" d="M785 583H892L878 570M892 583L878 596" class="direction" stroke="#C94422"/>
 <path id="{g('output')}" d="M892 583H785L799 570M785 583L799 596" class="direction" stroke="#167580"/>
 <g id="{g('annotations')}">{annotations}</g></svg>'''
 posecap=f'<div class="pose-caption"><span>{html.escape(s["text"].split(".")[0]+".")}</span></div>' if posed else ''
 # Static board captions are short, real phrases rather than squeezing a full sentence.
 if posed:posecap=f'<div class="pose-caption"><span>{html.escape(" ".join(s["text"].split()[:6]))}</span></div>'
 js=script.replace('ID',json.dumps(ident)).replace('DURATION',str(s['duration'])).replace('KEY',json.dumps(s['key'])).replace('VIEW',json.dumps(view)).replace('POSED',str(posed).lower()).replace('POSE',str(poseus[i]))
 body=f'<template><style>{css}</style><div id="root" data-composition-id="{ident}" data-width="1080" data-height="1920"><div class="scene"><h1 class="title" data-var-text="{s["key"]}">{s["title"]}</h1><div class="stage">{svg}</div><div class="note">{notes[view]}</div>{posecap}</div></div><script>{js}</script></template>'
 write(V/f'compositions/{ident}.html',body)
 story+=f'## Frame {i+1}: {s["title"]} ({s["start"]:.3f}–{s["end"]:.3f}s)\n\n- act: '+('Discovery' if i<6 else 'Guided clamp' if i<13 else 'Release and proof')+f'\n- status: {"built" if posed else "animated"}\n- src: compositions/{ident}.html\n- duration: {s["duration"]:.6f}s\n- poster: {s["start"]+s["duration"]*.6:.6f}s\n- transition_in: cut\n- scene: {s["action"]}\n- voiceover: {s["text"]}\n- reads: title and whole landmark (0–1s); the mechanism relation (1–{s["duration"]-.5:.2f}s); result hold (last0.5s). Captions follow measured speech.\n- sound: material cue on contact/actuation; soft editorial cue for hidden spring reveal. No music.\n\nQuestion answered: {s["title"]} New relation: {s["action"]} Next causal dependency follows scene order. First-use parts are introduced by function, not catalogued. View: layered shaded {view}; stable landmark is fixed shaft, right-hand mouth and orange slider. Camera cuts preserve orientation; decisive macro holds still. Diagnostic poses: initial input, approach, contact/transfer and resulting state; no unsupported ratchet. Interaction attention leads to the active part, follows response, then holds.\n\n'
 # Sound triggers derive from the same clock as the mechanical states.
 mapping={'mystery':[(.32,'metal','release-recoil'),(.86,'hinge','lock-input')],'reveal':[(.52,'editorial','shell-reveal')],'pull':[(.17,'hinge','blade-pull')],'anchor':[(.3,'editorial','fixed-anchor')],'energy':[(.4,'editorial','spring-load')],'return':[(.2,'hinge','spring-return')],'question':[],'slider':[(.17,'hinge','slider-travel')],'guide':[(.4,'editorial','pin-guide')],'touch':[(.72,'metal','tongue-contact')],'snap':[(.527,'hinge','pin-detent')],'clamp':[(.3,'metal','clamp-load')],'held':[],'unlock':[(.2,'hinge','unlock-detent'),(.65,'metal','tongue-release')],'rewind':[(.15,'hinge','reel-return')],'proof':[(.02,'hinge','proof-pull'),(.38,'metal','proof-lock'),(.71,'hinge','proof-release')]}
 for u,asset,kind in mapping[s['key']]:events.append(dict(scene=ident,kind=kind,asset=asset,progress=u,start=round((s['start']+.16+u*(s['duration']-.48))*30)/30))
write(V/'STORYBOARD.md',story)
dump(V/'motion-events.json',events)
hosts=''.join(f'<div id="{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-start="{s["start"]}" data-duration="{s["duration"]}" data-width="1080" data-height="1920" data-track-index="1" data-track-kind="graphics"></div>' for s in plan)
audio='';cap=''
if timing and not posed:
 caps=json.loads((V/'caption-groups.json').read_text());groups=''.join(f'<div id="cap-{i:03}" class="clip phrase" data-start="{c["start"]}" data-duration="{c["end"]-c["start"]}" data-layout-allow-caption-zone="true"><span>{html.escape(c["text"])}</span></div>' for i,c in enumerate(caps))
 write(V/'compositions/captions.html',f'<template><style>{css}.phrase{{position:absolute;left:108px;top:1500px;width:848px;text-align:center;font:600 46px/1.3 Manrope,sans-serif}}.phrase span{{display:inline-block;max-width:848px;background:#F8F9F5;padding:18px 26px;border-radius:14px}}</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920">{groups}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines.captions=gsap.timeline({{paused:true}});</script></template>')
 cap='<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="90" data-width="1080" data-height="1920" data-track-index="2" data-track-kind="captions" style="z-index:20"></div>'
 audio='<audio id="narration" class="clip" src="assets/audio/narration-master.wav" data-start="0" data-duration="90" data-volume="1" data-track-index="3"></audio>'
variables=[dict(id='canvas',type='color',label='Canvas',default='#ECEEE9')]+[dict(id=s['key'],type='string',label=s['title'],default=s['title']) for s in plan]
write(V/'index.html',f'''<!doctype html><html lang="id" data-composition-variables='{json.dumps(variables,ensure_ascii=False)}'><head><meta charset="utf-8"><title>Meteran: pegas dan rem</title><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#ECEEE9}}.clip{{position:absolute;inset:0}}#root{{position:absolute;inset:0;background:var(--canvas,#ECEEE9)}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="90" data-width="1080" data-height="1920">{hosts}{cap}{audio}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines.main=gsap.timeline({{paused:true}});</script></body></html>''')
print(json.dumps(dict(posed=posed,scenes=len(plan),events=len(events))))
