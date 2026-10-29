"""Editable layered 2.5D pencil: static storyboard, then deterministic motion."""
from pathlib import Path
import html,json,sys
V=Path(__file__).resolve().parent;animated='--animate' in sys.argv
data=json.loads((V/('timing.json' if animated else 'scene-plan.json')).read_text(encoding='utf-8'));plan=data['scenes'] if isinstance(data,dict) else data
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def e(x):return html.escape(str(x),quote=True)
CSS="""@font-face{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:200 800}@font-face{font-family:Plex;src:url('assets/fonts/ibm-plex-mono.ttf')}*{box-sizing:border-box}#root{position:absolute;inset:0;font-family:Manrope,sans-serif;color:#172B3B}.scene{position:absolute;inset:0;background:#ECEEE9}.title{position:absolute;left:108px;top:205px;width:810px;font-size:70px;line-height:1.1;font-weight:800;letter-spacing:-2.5px;margin:0}.stage{position:absolute;left:80px;top:440px;width:920px;height:920px}.stage svg{width:100%;height:100%;overflow:hidden}.note{position:absolute;left:108px;top:1395px;width:800px;font:28px/1.3 Plex,monospace;color:#536775}.pose-caption{position:absolute;left:108px;top:1500px;width:848px;text-align:center;font:600 46px/1.3 Manrope,sans-serif}.pose-caption span{display:inline-block;background:#F8F9F5;max-width:848px;padding:18px 26px;border-radius:14px}.edge{stroke:#172B3B;stroke-width:2;stroke-linejoin:round}.label{fill:#172B3B;font:29px Manrope,sans-serif;font-weight:600}.leader{stroke:#536775;stroke-width:2;fill:none}.ghost{fill:#F8F9F5;stroke:#536775;stroke-width:2}.dim{stroke:#167580;stroke-width:3;stroke-dasharray:6 6;fill:none}"""
def defs(i):
 gradients=''
 for name,colors in [('metal',['#E5ECEA','#A6B4BE','#536775']),('blue',['#B4C9ED','#2459C4','#173D81']),('orange',['#F0B18E','#C94422','#842C1B']),('teal',['#9EC7C5','#167580','#0C5058']),('brass',['#E8D7AF','#B49A62','#776135'])]:
  gradients+=f'<linearGradient id="{i}-{name}" x1="0" y1="0" x2="1" y2=".25"><stop stop-color="{colors[0]}"/><stop offset=".5" stop-color="{colors[1]}"/><stop offset="1" stop-color="{colors[2]}"/></linearGradient>'
 return '<defs>'+gradients+f'<pattern id="{i}-hatch" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8L8 0" stroke="#536775" stroke-width="1"/></pattern></defs>'
def body(i,external=False):
 if external:
  return f'''<ellipse cx="469" cy="830" rx="98" ry="15" fill="#172B3B" opacity=".1"/><g id="{i}-button"><path d="M411 56H489V121H411Z" transform="translate(10 8)" fill="#536775" class="edge"/><path d="M411 56H489V121H411Z" fill="url(#{i}-orange)" class="edge"/><ellipse cx="450" cy="56" rx="39" ry="13" fill="#F0B18E" class="edge"/></g><path d="M390 116H510V596L469 720H431L390 596Z" transform="translate(12 10)" fill="#0C5058" class="edge"/><path d="M390 116H510V596H390Z" fill="url(#{i}-teal)" class="edge"/><ellipse cx="450" cy="116" rx="60" ry="17" fill="#9EC7C5" class="edge"/><path d="M390 595H510L469 720H431Z" fill="url(#{i}-metal)" class="edge"/><path d="M435 720H465V776H435Z" fill="url(#{i}-metal)" class="edge"/><path d="M496 135H528V327Q528 346 512 346" fill="none" stroke="#536775" stroke-width="13" stroke-linejoin="round"/>'''
 return f'''<ellipse cx="462" cy="817" rx="138" ry="18" fill="#172B3B" opacity=".08"/><path d="M339 100H561V570L483 750H417L339 570Z" transform="translate(14 12)" fill="#536775" class="edge"/><path d="M339 100H561V570L483 750H417L339 570Z" fill="url(#{i}-metal)" class="edge"/><path d="M360 118H540V565L470 730H430L360 565Z" fill="#F8F9F5" class="edge"/><path d="M339 100H360V570L430 730H417L339 570Z" fill="url(#{i}-hatch)"/><path d="M540 100H561V570L483 750H470L540 565Z" fill="url(#{i}-hatch)"/><path d="M360 539H390V555H360ZM510 539H540V555H510Z" fill="url(#{i}-blue)" class="edge"/><path d="M360 456H390V469H360ZM510 456H540V469H510Z" fill="#536775" class="edge"/><path d="M430 730H470V780H430Z" fill="url(#{i}-metal)" class="edge"/><path d="M442 730H458V780H442Z" fill="#F8F9F5" class="edge"/>'''
def mechanism(i):
 # Exposed front half-section: two jaw sections flank the lead on the shared axis.
 return f'''<g id="{i}-button"><path d="M397 54H503V126H397Z" transform="translate(10 9)" fill="#842C1B" class="edge"/><path d="M397 54H503V126H397Z" fill="url(#{i}-orange)" class="edge"/><ellipse cx="450" cy="54" rx="53" ry="14" fill="#F0B18E" class="edge"/></g><g id="{i}-tube"><path d="M397 124H503V377H397Z" fill="url(#{i}-orange)" class="edge"/><path d="M420 124H480V377H420Z" fill="#F8F9F5" class="edge"/><path d="M397 362H503V388H397Z" fill="url(#{i}-orange)" class="edge"/></g><path id="{i}-spring-back" d="" fill="none" stroke="#536775" stroke-width="12"/><path id="{i}-spring" d="" fill="none" stroke="url(#{i}-metal)" stroke-width="7"/><g id="{i}-stem"><path d="M415 388H485V464H415Z" fill="url(#{i}-brass)" class="edge"/><path d="M441 388H459V464H441Z" fill="#F8F9F5" class="edge"/></g><g id="{i}-jaw-left"><path d="M415 459L396 508L414 550H442V464Z" transform="translate(6 6)" fill="#776135" class="edge"/><path d="M415 459L396 508L414 550H442V464Z" fill="url(#{i}-brass)" class="edge"/><path d="M437 479V541" stroke="#172B3B" stroke-width="3"/></g><g id="{i}-jaw-right"><path d="M485 459L504 508L486 550H458V464Z" transform="translate(6 6)" fill="#776135" class="edge"/><path d="M485 459L504 508L486 550H458V464Z" fill="url(#{i}-brass)" class="edge"/><path d="M463 479V541" stroke="#172B3B" stroke-width="3"/></g><g id="{i}-ring"><path d="M386 470H409V515H386ZM491 470H514V515H491Z" transform="translate(7 6)" fill="#173D81" class="edge"/><path d="M386 470H409V515H386ZM491 470H514V515H491Z" fill="url(#{i}-blue)" class="edge"/><path d="M386 471H514M386 515H514" stroke="#2459C4" stroke-width="3" stroke-dasharray="7 6" opacity=".45"/></g><path d="M422 650H442V700H422ZM458 650H478V700H458Z" transform="translate(5 5)" fill="#0C5058" class="edge"/><path d="M422 650H442V700H422ZM458 650H478V700H458Z" fill="url(#{i}-teal)" class="edge"/><path d="M422 651Q450 638 478 651M422 700Q450 712 478 700" fill="none" stroke="#167580" stroke-width="4"/>'''
def lead(i):return f'''<g id="{i}-lead"><path d="M443 186H457V795H443Z" fill="#172B3B"/><path d="M445 186H448V795H445Z" fill="#536775"/><path d="M443 795L450 806L457 795Z" fill="#172B3B"/><path d="M440 623H460V629H440Z" fill="#167580"/></g>'''
def label(i,text,x,y,tx,ty,name):
 anchor='end' if x<450 else 'start';edge=x+12 if x<450 else x-12
 return f'<g id="{i}-label-{name}"><path d="M{edge} {y-8}H{(edge+tx)/2}L{tx} {ty}" class="leader"/><circle cx="{tx}" cy="{ty}" r="4" fill="#2459C4"/><text x="{x}" y="{y}" text-anchor="{anchor}" class="label">{e(text)}</text></g>'
views={
'whole':('210 0 480 890',[('tombol',300,90,403,90,'input'),('isi maju',300,800,450,797,'lead')]),
'section':('70 0 760 850',[('penjepit',280,490,415,500,'jaw'),('penahan ujung',290,700,425,675,'tip')]),
'jaw':('245 355 410 440',[('cincin',340,435,395,485,'ring'),('rahang',340,608,425,541,'jaw')]),
'spring':('160 45 580 620',[('tabung isi',330,230,398,220,'tube'),('pegas',325,432,392,420,'spring')]),
'stop':('245 355 410 440',[('cincin',342,430,390,500,'ring'),('pembatas tetap',355,615,375,547,'stop')]),
'retainer':('250 540 400 425',[('penahan ringan',360,613,425,661,'tip'),('isi ditahan',350,833,450,804,'lead')]),
'return':('245 355 410 440',[('penjepit kembali',346,438,418,480,'return'),('isi tetap',343,708,450,680,'lead')]),
'compare':('160 40 580 730',[('posisi awal',320,661,450,626,'start'),('hasil klik',320,733,450,650,'result')]),
'proof':('70 0 760 850',[('jepit kembali',280,490,415,500,'jaw'),('isi tetap maju',290,780,450,794,'result')])}
RUNTIME=r'''
const clamp=x=>Math.max(0,Math.min(1,x)),smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
function state(p){p=clamp(p);let q,r,o,l;
 if(p<=.55){let u=smooth(p/.55);q=24*u;r=q;o=0;l=q;}
 else if(p<=.78){let u=smooth((p-.55)/.23);q=24+20*u;r=24;o=u;l=24;}
 else if(p<=.84){q=44;r=24;o=1;l=24;}
 else if(p<=.96){let u=smooth((p-.84)/.12);q=44-24*u;r=24-24*u;o=1;l=24;}
 else {let u=smooth((p-.96)/.04);q=20*(1-u);r=0;o=1-u;l=24;}
 return {p,q,r,o,l};
}
const el=n=>document.getElementById(id+'-'+n),attr=(n,a,v)=>{let z=el(n);if(z)z.setAttribute(a,v)};
function renderAt(t){const u=smooth((t-.4)/(duration-.95)),p=a+(b-a)*u,s=state(p);
 for(const n of ['button','tube','stem'])attr(n,'transform','translate(0 '+s.q+')');
 attr('jaw-left','transform','translate(0 '+s.q+')');attr('jaw-right','transform','translate(0 '+s.q+')');
 const flex=s.o*10;
 for(const side of ['left','right']){const sign=side==='left'?-1:1;const outer=450+sign*(36+flex),inner=450+sign*(8+flex),top=450+sign*35,shoulder=450+sign*(40+flex);const path='M'+top+' 459L'+shoulder+' 508L'+outer+' 550H'+inner+'V464Z';const g=el('jaw-'+side);if(g){const paths=g.querySelectorAll('path');paths[0].setAttribute('d',path);paths[1].setAttribute('d',path);}}
 attr('ring','transform','translate(0 '+s.r+')');attr('lead','transform','translate(0 '+(s.l+baseLead)+')');
 let path='M388 '+(388+s.q);for(let k=0;k<=70;k++){let v=k/70;path+='L'+(450+Math.sin(v*Math.PI*14)*61)+' '+((388+s.q)+(456-388-s.q)*v)}
 attr('spring','d',path);attr('spring-back','d',path);
 if(key==='grip')attr('housing-front','opacity',.08);
 window.__mechanisms=window.__mechanisms||{};window.__mechanisms[id]=Object.assign({time:t,baseLead,stop:539,tipFixed:true},s);
}
'''
events=[]
for n,s in enumerate(plan):
 i=s['id'];d=s['duration'];key=s['key'];view=s['view'];vb,labels=views[view]
 external=view=='whole';art=body(i,external)
 if not external:art+=mechanism(i)
 if external:
  art+=f'<defs><clipPath id="{i}-exposed"><rect x="420" y="778" width="60" height="100"/></clipPath></defs><g clip-path="url(#{i}-exposed)">'+lead(i)+'</g>'
 else:art+=lead(i)
 if not external:
  # Translucent enclosing wall preserves context but the removed front wall is not a cover.
  art+=f'<path id="{i}-housing-front" d="M339 100H561V568L483 750H417L339 568Z" fill="#167580" opacity=".035"/>'
 if view=='compare':art+=f'<path d="M455 626H530M455 650H530M520 626V650" class="dim"/>'
 if view=='proof':art+=f'<path d="M300 795H580" class="dim"/>'
 art+=''.join(label(i,*z) for z in labels)
 notes='Potongan memanjang · gerak diperbesar'
 if external:notes='Pensil mekanik tekan · contoh ilustratif'
 if view=='jaw':notes='Detail penjepit · gerak diperlambat'
 if view=='retainer':notes='Gesekan ringan · posisi penahan tetap'
 pose=s['phase_start']+(s['phase_end']-s['phase_start'])*.7
 # Wide views scale down labels, so retain >=30px at output. Macro labels shrink in local units.
 ratio=min(920/float(vb.split()[2]),920/float(vb.split()[3]))
 label_size=30/ratio
 stage=f'<div class="stage"><svg viewBox="{vb}" role="img" aria-label="{e(s["title"])}" data-layout-allow-overlap="true">{defs(i)}<g>{art}</g></svg></div>'
 words=s['text'].split();preview=[]
 for word in words:
  if len(' '.join(preview+[word]))>52:break
  preview.append(word)
 posecap='' if animated else f'<div class="pose-caption"><span>{e(" ".join(preview))}</span></div>'
 script=f'const id={json.dumps(i)},key={json.dumps(key)},duration={d},a={s["phase_start"]},b={s["phase_end"]},baseLead={24 if n>=13 else 0};\n'+RUNTIME
 if animated:
  script+='const clock={t:0};const tl=gsap.timeline({paused:true});tl.fromTo(clock,{t:0},{t:duration,duration,ease:"none",onUpdate:()=>renderAt(clock.t)},0);renderAt(0);window.__timelines[id]=tl;'
 else:script+=f'renderAt({d*.7});const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration}});window.__timelines[id]=tl;'
 write(V/'compositions'/f'{i}.html',f'<template><style>{CSS}#{i}-art .label{{font-size:{label_size:.5f}px}}</style><div id="root" data-composition-id="{i}" data-width="1080" data-height="1920"><div id="{i}-art" class="scene clip" data-start="0" data-duration="{d}" data-layout-allow-overlap="true"><h1 id="{i}-title" class="title" data-var-text="{key}">{e(s["title"])}</h1>{stage}<div class="note">{notes}</div>{posecap}</div></div><script>{script}</script></template>')
 if animated:
  for p,kind in [(.12,'input'),(.55,'ring-stop'),(.78,'release'),(.86,'return'),(1,'regrip')]:
   a,b=s['phase_start'],s['phase_end']
   if b>a and a<p<=b:
    # Invert the outer smoothstep numerically, matching renderAt's clock.
    target=(p-a)/(b-a);lo=0;hi=1
    for _ in range(48):
     mid=(lo+hi)/2
     if mid*mid*(3-2*mid)<target:lo=mid
     else:hi=mid
    t=.4+(d-.95)*(lo+hi)/2
    events.append(dict(id=f'{i}-{kind}',scene=i,kind=kind,start=round((s['start']+t)*30)/30,phase=p))
hosts='\n'.join(f'<div id="{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-start="{s["start"]}" data-duration="{s["duration"]}" data-width="1080" data-height="1920" data-track-index="1" data-track-kind="graphics"></div>' for s in plan)
audio='';captions=''
if animated:
 audio='<audio id="narration" class="clip" src="assets/audio/narration-master.wav" data-start="0" data-duration="90" data-volume="1" data-track-index="3"></audio>'
 caps=json.loads((V/'caption-groups.json').read_text(encoding='utf-8'))
 caphtml=''.join(f'<div id="cap-{k:03}" class="clip cap" data-start="{g["start"]:.6f}" data-duration="{g["end"]-g["start"]:.6f}"><span>{e(g["text"])}</span></div>' for k,g in enumerate(caps))
 capcss="@font-face{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:200 800}#root{position:absolute;inset:0}.cap{position:absolute;left:108px;top:1500px;width:848px;text-align:center;font:600 46px/1.3 Manrope,sans-serif;color:#172B3B}.cap span{display:inline-block;max-width:848px;padding:18px 26px;background:#F8F9F5;border-radius:14px}"
 # Registry editorial emphasis group clock retained; fixed board typography replaces its display emphasis styling.
 capscript='const tl=gsap.timeline({paused:true});tl.to({}, {duration:90});window.__timelines["captions"]=tl;'
 write(V/'compositions/captions.html',f'<template><style>{capcss}</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920">{caphtml}</div><script>{capscript}</script></template>')
 captions='<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="90" data-width="1080" data-height="1920" data-track-index="2" data-track-kind="captions" style="z-index:20"></div>'
variables=[dict(id=s['key'],type='string',label=s['title'],default=s['title']) for s in plan]
write(V/'index.html',f'<!doctype html><html lang="id" data-composition-variables=\'{e(json.dumps(variables))}\'><head><meta charset="utf-8"><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#ECEEE9}}.clip{{position:absolute;inset:0}}#root{{width:1080px;height:1920px}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="90" data-width="1080" data-height="1920">{hosts}{captions}{audio}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines.main=gsap.timeline({{paused:true}});</script></body></html>')
if animated:write(V/'motion-events.json',json.dumps(events,indent=2)+'\n')
print(json.dumps(dict(animated=animated,shots=len(plan),events=len(events))))
