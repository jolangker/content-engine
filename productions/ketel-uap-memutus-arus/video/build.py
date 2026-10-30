"""Original layered kettle sections; static poses first, then seekable operation."""
from pathlib import Path
import json,html,sys,math
V=Path(__file__).resolve().parent;animated='--animate' in sys.argv
data=json.loads((V/('timing.json' if animated else 'scene-plan.json')).read_text(encoding='utf-8'));plan=data['scenes'] if isinstance(data,dict) else data
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def esc(x):return html.escape(str(x),quote=True)
CSS="""@font-face{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:200 800}@font-face{font-family:Plex;src:url('assets/fonts/ibm-plex-mono.ttf')}*{box-sizing:border-box}#root{position:absolute;inset:0;color:#172B3B;font-family:Manrope,sans-serif}.scene{position:absolute;inset:0;background:#ECEEE9}.title{position:absolute;left:108px;top:205px;width:810px;font:800 70px/1.1 Manrope,sans-serif;letter-spacing:-2.5px;margin:0}.stage{position:absolute;left:80px;top:430px;width:920px;height:980px}.stage svg{width:100%;height:100%;overflow:hidden}.note{position:absolute;left:108px;top:1410px;width:810px;font:28px/1 Plex,monospace;color:#536775}.pose-caption{position:absolute;left:108px;top:1500px;width:848px;text-align:center;font:600 46px/1.3 Manrope,sans-serif}.pose-caption span{display:inline-block;max-width:848px;background:#F8F9F5;padding:18px 26px;border-radius:14px}.edge{stroke:#172B3B;stroke-width:2.5;stroke-linejoin:round}.label{fill:#172B3B;font-family:Manrope,sans-serif;font-weight:600}.leader{fill:none;stroke:#536775;stroke-width:2}.flow{fill:none;stroke:#167580;stroke-linecap:round;stroke-width:10}.current{fill:none;stroke:#C94422;stroke-width:8;stroke-linecap:round}.hatch{stroke:#536775;stroke-width:2;fill:none}"""
def defs(i):
 s=''
 for k,cols in [('metal',['#E5ECEA','#A6B4BE','#536775']),('shell',['#F8F9F5','#D9DEDA','#A6B4BE']),('blue',['#B4C9ED','#2459C4','#173D81']),('orange',['#F0B18E','#C94422','#842C1B']),('teal',['#B6D7D4','#167580','#0C5058']),('brass',['#E5D7B7','#B49A62','#776135'])]:
  s+=f'<linearGradient id="{i}-{k}" x2="1" y2=".4"><stop stop-color="{cols[0]}"/><stop offset=".5" stop-color="{cols[1]}"/><stop offset="1" stop-color="{cols[2]}"/></linearGradient>'
 return '<defs>'+s+f'<pattern id="{i}-hatch" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M0 12L12 0" stroke="#536775" stroke-width="1.5"/></pattern></defs>'
def jug(i,section):
 # The handle and the dry duct retain their identity across all whole/section views.
 s=f'''<ellipse cx="472" cy="815" rx="320" ry="28" fill="#172B3B" opacity=".09"/>
 <path d="M666 230H756Q850 230 850 330V545Q850 635 741 635H690V576H746Q790 576 790 527V336Q790 289 748 289H673Z" transform="translate(12 10)" fill="#536775" class="edge"/><path d="M666 230H756Q850 230 850 330V545Q850 635 741 635H690V576H746Q790 576 790 527V336Q790 289 748 289H673Z" fill="url(#{i}-metal)" class="edge"/>
 <path d="M250 274L103 221L181 408L252 423Z" transform="translate(12 10)" fill="#536775" class="edge"/><path d="M250 274L103 221L181 408L252 423Z" fill="url(#{i}-shell)" class="edge"/>
 <path d="M259 189Q466 151 665 189L706 693Q706 762 641 777H271Q214 762 217 693Z" transform="translate(12 10)" fill="#536775" class="edge"/>
 <path d="M259 189Q466 151 665 189L706 693Q706 762 641 777H271Q214 762 217 693Z" fill="url(#{i}-shell)" class="edge"/>
 <path d="M250 191Q461 140 673 191L669 214Q460 174 255 215Z" fill="url(#{i}-metal)" class="edge"/>
 <ellipse cx="461" cy="185" rx="211" ry="37" fill="url(#{i}-shell)" class="edge"/><path d="M411 149Q459 124 512 149V166H411Z" fill="url(#{i}-metal)" class="edge"/>
 <path d="M216 754H710V793H216Z" fill="url(#{i}-metal)" class="edge"/><ellipse cx="462" cy="794" rx="249" ry="19" fill="#536775"/>
 <path id="{i}-knob" d="M689 653H772V677H689Z" fill="url(#{i}-orange)" class="edge"/>
 <path id="{i}-lamp" d="M272 699H310V716H272Z" fill="#C94422" class="edge"/>'''
 if not section:
  s+=f'<g id="{i}-vapour"><path d="M103 219Q68 184 99 148Q117 124 91 91M133 228Q103 193 134 159Q153 134 133 105" stroke="#536775" stroke-width="6" fill="none" opacity=".6"/></g>'
 if section:
  s+=f'''<path d="M277 231Q461 201 646 231L683 688Q686 729 638 738H279Q240 727 242 685Z" fill="#F8F9F5" class="edge"/>
 <path d="M250 455H665L683 686Q686 729 638 738H279Q240 727 242 685Z" fill="#B6D7D4" opacity=".82"/><ellipse cx="456" cy="455" rx="207" ry="17" fill="#D5E7E1"/>
 <path d="M259 212L277 231L242 685Q240 727 279 738L271 754Q220 740 220 685Z" fill="url(#{i}-hatch)"/>
 <path id="{i}-heater" d="M294 705H617V724H294Z" fill="url(#{i}-orange)" class="edge"/>
 <path id="{i}-heat" d="M320 673V534M445 673V525M565 673V537" stroke="#C94422" stroke-width="9" stroke-dasharray="18 18" fill="none"/>
 <path d="M602 246H692V674H660V277H602" fill="#D9DEDA" class="edge"/><path id="{i}-steam-path" d="M591 261H677V660H717" class="flow"/>
 <path d="M670 648H748V704H670Z" fill="url(#{i}-blue)" class="edge"/><path id="{i}-micro-disc" d="M682 674Q709 655 736 674" stroke="#F8F9F5" stroke-width="7" fill="none"/>
 <path id="{i}-micro-link" d="M710 689H766" stroke="#172B3B" stroke-width="7"/>
 <circle id="{i}-micro-contact" cx="766" cy="689" r="7" fill="#B49A62"/><circle cx="781" cy="689" r="7" fill="#A6B4BE"/>
 <path id="{i}-power" d="M782 701V735H612M300 725H268V745H782" class="current"/>
 <g id="{i}-vapour">'''
  for x,y,r in [(340,330,18),(410,285,23),(490,350,22),(560,300,17),(465,240,13)]:s+=f'<path d="M{x-25} {y}Q{x} {y-25} {x+25} {y}" stroke="#167580" stroke-width="5" opacity=".5" fill="none"/>'
  s+='</g><g id="'+i+'-bubbles">'
  for n in range(16):s+=f'<circle id="{i}-bubble-{n}" cx="{285+n%5*72}" cy="{660-n%4*35}" r="{8+n%3*3}" fill="#F8F9F5" stroke="#167580" stroke-width="2"/>'
  s+='</g>'
 return s
def control(i):
 # Paired C-springs, pivot, slotted lever tab and horizontal link are all visible.
 return f'''<ellipse cx="460" cy="704" rx="355" ry="23" fill="#172B3B" opacity=".08"/>
 <path d="M119 307H813V674H119Z" transform="translate(12 12)" fill="#536775" class="edge"/><path d="M119 307H813V674H119Z" fill="url(#{i}-shell)" class="edge"/><path d="M145 331H789V647H145Z" fill="#F8F9F5" class="edge"/>
 <path d="M142 270H189V337H157V302H90" fill="#D9DEDA" class="edge"/><path id="{i}-steam-path" d="M91 286H173V354H357" class="flow"/>
 <path d="M441 510H465V647H441Z" fill="url(#{i}-metal)" class="edge"/><ellipse cx="453" cy="510" rx="12" ry="5" fill="#E5ECEA" class="edge"/>
 <path d="M304 479H335V623H304Z" fill="url(#{i}-metal)" class="edge"/>
 <g id="{i}-lever">
 <path d="M288 466H603V491H288Z" transform="translate(7 7)" fill="#173D81" class="edge"/><path d="M288 466H603V491H288Z" fill="url(#{i}-blue)" class="edge"/>
 <path d="M294 486H309V583H294Z" fill="url(#{i}-blue)" class="edge"/><circle cx="300" cy="580" r="9" fill="#172B3B"/>
 <path d="M571 449H628V481H571Z" fill="url(#{i}-orange)" class="edge"/>
 <path d="M363 416H377V466H363ZM532 416H546V466H532Z" fill="url(#{i}-metal)" class="edge"/>
 <path d="M367 395H538V417H367Z" fill="url(#{i}-metal)" class="edge"/>
 <path id="{i}-disc-back" d="M370 410Q455 367 540 410L540 424Q455 381 370 424Z" fill="url(#{i}-brass)" class="edge"/>
 <path id="{i}-disc-front" d="M370 408Q455 365 540 408L540 417Q455 374 370 417Z" fill="url(#{i}-metal)" class="edge"/>
 <path id="{i}-tongue" d="M442 399H464V441H442Z" fill="url(#{i}-metal)" class="edge"/>
 </g>
 <path id="{i}-spring-back" d="" fill="none" stroke="#536775" stroke-width="11"/><path id="{i}-spring" d="" fill="none" stroke="#B49A62" stroke-width="7"/>
 <circle cx="220" cy="480" r="10" fill="url(#{i}-metal)" class="edge"/>
 <circle cx="320" cy="480" r="16" fill="url(#{i}-metal)" class="edge"/><circle cx="320" cy="480" r="5" fill="#172B3B"/>
 <path d="M164 608H187V632H164ZM680 608H702V632H680Z" fill="url(#{i}-metal)" class="edge"/>
 <g id="{i}-link"><path d="M259 592H760V610H259Z" transform="translate(6 6)" fill="#536775" class="edge"/><path d="M259 592H760V610H259Z" fill="url(#{i}-metal)" class="edge"/><path d="M265 544H292V617H265Z" fill="url(#{i}-metal)" class="edge"/><path d="M275 555V602" stroke="#172B3B" stroke-width="9"/><path d="M744 548H760V610H744Z" fill="url(#{i}-metal)" class="edge"/></g>
 <path d="M690 525H740V550H690Z" fill="url(#{i}-metal)" class="edge"/><circle cx="740" cy="550" r="10" fill="url(#{i}-brass)" class="edge"/>
 <path id="{i}-contact-strip" d="M775 641Q794 600 760 550" fill="none" stroke="#A6B4BE" stroke-width="12"/><circle id="{i}-contact" cx="760" cy="550" r="10" fill="url(#{i}-brass)" class="edge"/>
 <path id="{i}-power" d="M686 536H713M777 641H805V710H90" class="current"/>
 <path id="{i}-hot" d="M362 374H549" stroke="#C94422" stroke-width="8" stroke-dasharray="12 12" fill="none"/>
 '''
def disc(i):
 return f'''<ellipse cx="460" cy="716" rx="310" ry="24" fill="#172B3B" opacity=".08"/>
 <g id="{i}-layer-bottom"><path id="{i}-disc-back" d="M150 443Q450 297 750 443L750 482Q450 336 150 482Z" fill="url(#{i}-brass)" class="edge"/><path d="M150 482L168 500Q468 354 768 500L750 482Q450 336 150 482Z" fill="#776135" class="edge"/></g>
 <g id="{i}-layer-top"><path id="{i}-disc-front" d="M150 423Q450 277 750 423L750 447Q450 301 150 447Z" fill="url(#{i}-metal)" class="edge"/><path d="M150 423L168 439Q468 293 768 439L750 423Q450 277 150 423Z" fill="#E5ECEA" class="edge"/></g>
 <path id="{i}-heat" d="M180 660V565M330 660V565M480 660V565M630 660V565" stroke="#C94422" stroke-width="8" stroke-dasharray="16 16" fill="none"/>
 <path d="M150 700H750" stroke="#536775" stroke-width="3"/>
 '''
views={'whole':('40 80 870 850',[]),'section':('40 80 870 850',[]),'duct':('460 170 355 605',[]),'heater':('180 405 570 410',[]),'control':('65 230 805 560',[]),'snapmacro':('280 300 340 310',[]),'springmacro':('150 345 520 320',[]),'contacts':('540 458 327 255',[]),'disc':('90 195 740 600',[])}
labels={
 'steam':[('saluran uap',815,160,680,350)],
 'circuit':[('permukaan kontak',697,476,750,550)],
 'heater':[('elemen pemanas',405,430,440,717)],
 'route':[('masuk',590,215,630,260)],
 'sensor':[('cakram bimetal',470,270,451,405),('ruang air di luar potongan',460,780,173,286)],
 'layers':[('logam A',320,212,365,350),('logam B',570,775,565,470)],
 'curve':[('dua lapis terikat',460,195,450,419)],
 'snap':[('penumpu tetap',490,580,453,510)],
 'spring':[('pegas lewat tengah',340,370,293,480),('acuan poros',405,637,320,480)],
 'open':[('celah pemutus',697,476,770,550)],
 'off':[('tetap mati',590,267,599,456)],
 'proof':[('uap ke pemutus',795,153,678,330)],
}
RUNTIME=r'''
const clamp=x=>Math.max(0,Math.min(1,x)),smooth=x=>{x=clamp(x);return x*x*(3-2*x)},ramp=(x,a,b)=>smooth((x-a)/(b-a));
const el=n=>document.getElementById(id+'-'+n),attr=(n,a,v)=>{let z=el(n);if(z)z.setAttribute(a,v)};
function state(u){
 let trip=0,curvature=0,steam=0,heat=0,boil=0,separate=0,closed=true;
 if(mode==='whole'){trip=ramp(u,.4,.65);steam=1;heat=1-trip;boil=1-trip*.6;curvature=trip;}
 if(mode==='steam'){steam=ramp(u,.12,.78);heat=1;boil=1;}
 if(mode==='on'){trip=1-ramp(u,.25,.5);closed=trip<=1e-8;heat=closed?1:0;}
 if(mode==='close'){trip=1-ramp(u,.12,.4);closed=trip<=1e-8;heat=closed?1:0;}
 if(mode==='heat'){heat=ramp(u,.1,.6);}
 if(mode==='boil'){heat=1;boil=ramp(u,.05,.8);steam=boil*.4;}
 if(mode==='route'){heat=1;boil=1;steam=ramp(u,.1,.82);}
 if(mode==='sensor'){steam=1;heat=ramp(u,.12,.75);curvature=heat*.15;}
 if(mode==='layers'){separate=1-ramp(u,.45,.92);heat=ramp(u,.3,.9);curvature=.1;}
 if(mode==='curve'){heat=1;curvature=ramp(u,.1,.85)*.3;}
 if(mode==='snap'){heat=1;steam=1;curvature=.3+.7*ramp(u,.38,.49);trip=.5*ramp(u,.5,.82);}
 if(mode==='trip'){heat=1;steam=1;curvature=1;trip=.35+.65*ramp(u,.18,.64);}
 if(mode==='open'){heat=1;steam=1;curvature=1;trip=ramp(u,.18,.58);}
 if(mode==='residual'){trip=1;curvature=1;heat=1-ramp(u,.2,.9);boil=(1-ramp(u,.1,.88))*.8;steam=boil;}
 if(mode==='latch'){trip=1;curvature=1-ramp(u,.2,.75);heat=0;steam=0;}
 if(mode==='proof'){steam=ramp(u,.04,.42);boil=1;curvature=ramp(u,.45,.56);trip=ramp(u,.57,.77);heat=1-trip;}
 if(!['on','close'].includes(mode))closed=trip<=1e-8;
 const angle=12-24*trip,rad=angle*Math.PI/180,tabX=320-20*Math.cos(rad)-100*Math.sin(rad),link=tabX-(320-20*Math.cos(12*Math.PI/180)-100*Math.sin(12*Math.PI/180));
 return {trip,curvature,steam,heat,boil,separate,closed,angle,link,contactGap:link,powered:closed&&heat>.01};
}
function renderAt(t){const u=clamp((t-.18)/(duration-.6)),s=state(u);
 attr('lever','transform','rotate('+s.angle+' 320 480)');attr('link','transform','translate('+s.link+' 0)');
 attr('contact','cx',760+s.link);attr('contact-strip','d','M775 641Q'+(794+s.link*.4)+' 600 '+(760+s.link)+' 550');
 attr('power','opacity',s.powered?1:0);attr('lamp','opacity',s.powered?1:.15);attr('knob','transform','translate(0 '+(-s.trip*30)+')');
 attr('steam-path','stroke-dasharray','16 20');attr('steam-path','stroke-dashoffset',-t*34);attr('steam-path','opacity',s.steam*.85);
 attr('hot','opacity',s.heat*.6);attr('heat','opacity',s.heat*.8);attr('heat','stroke-dashoffset',-t*25);attr('heater','opacity',.3+s.heat*.7);
 attr('vapour','opacity',s.steam*.7);attr('bubbles','opacity',s.boil);
 for(let n=0;n<16;n++){let phase=(t*.16+n*.137)%1;attr('bubble-'+n,'cy',685-phase*205);attr('bubble-'+n,'r',(7+n%3*3)*(1-phase*.45));}
 if(view==='disc'){
  const q=-146+s.curvature*290;
  attr('disc-front','d','M150 423Q450 '+(423+q)+' 750 423L750 447Q450 '+(447+q)+' 150 447Z');
  attr('disc-back','d','M150 447Q450 '+(447+q)+' 750 447L750 482Q450 '+(482+q)+' 150 482Z');
  attr('layer-top','transform','translate(0 '+(-s.separate*90)+')');attr('layer-bottom','transform','translate(0 '+(s.separate*48)+')');
  const top=el('layer-top'),bottom=el('layer-bottom');
  if(top)top.querySelectorAll('path')[1].setAttribute('d','M150 423L168 439Q468 '+(439+q)+' 768 439L750 423Q450 '+(423+q)+' 150 423Z');
  if(bottom)bottom.querySelectorAll('path')[1].setAttribute('d','M150 482L168 498Q468 '+(498+q)+' 768 498L750 482Q450 '+(482+q)+' 150 482Z');
  const z0=el('label-0'),z1=el('label-1');
  if(z0)z0.querySelector('path').setAttribute('d','M320 220L365 '+(433+2*(215/600)*(385/600)*q-s.separate*90));
  if(z1)z1.querySelector('path').setAttribute('d','M570 783L565 '+(465+2*(415/600)*(185/600)*q+s.separate*48));
 }else{
  const q=-43+s.curvature*110;
  attr('disc-front','d','M370 408Q455 '+(408+q)+' 540 408L540 417Q455 '+(417+q)+' 370 417Z');
  attr('disc-back','d','M370 417Q455 '+(417+q)+' 540 417L540 431Q455 '+(431+q)+' 370 431Z');
  // The flexible tongue bears on the fixed pillar without crossing its face.
  const a=s.angle*Math.PI/180,desiredY=480+133*Math.sin(a)+(432+61*s.curvature-480)*Math.cos(a);
  const worldY=Math.min(510,desiredY),worldX=320+133*Math.cos(a)-(432+61*s.curvature-480)*Math.sin(a);
  const tipX=320+(worldX-320)*Math.cos(a)+(worldY-480)*Math.sin(a),tipY=480-(worldX-320)*Math.sin(a)+(worldY-480)*Math.cos(a),baseY=408+q/2+10;
  attr('tongue','d','M442 '+baseY+'H464L'+(tipX+11)+' '+tipY+'H'+(tipX-11)+'Z');
  s.tongueTipWorldY=worldY;s.pillarTop=510;
 }
 const rad=s.angle*Math.PI/180,x=320+60*Math.cos(rad),y=480+60*Math.sin(rad);
 let sp='M220 480';for(let k=1;k<=24;k++){const q=k/24;sp+='L'+(220+(x-220)*q)+' '+(480+(y-480)*q+Math.sin(q*Math.PI*8)*8);}
 attr('spring','d',sp);attr('spring-back','d',sp);attr('spring-back','transform','translate(0 13)');
 attr('micro-disc','d','M682 674Q709 '+(655+s.curvature*35)+' 736 674');attr('micro-link','transform','translate('+(-s.trip*12)+' 0)');attr('micro-contact','cx',766-s.trip*16);
 window.__mechanisms=window.__mechanisms||{};window.__mechanisms[id]=Object.assign({time:t,u},s);
}
'''
events=[]
for n,s in enumerate(plan):
 i=s['id'];d=s['duration'];view=s['view'];vb,_=views[view]
 art=disc(i) if view=='disc' else control(i) if view in ['control','contacts','snapmacro','springmacro'] else jug(i,view!='whole')
 if view=='springmacro':art+=f'<path d="M200 480H418" stroke="#536775" stroke-width="2" stroke-dasharray="6 7" fill="none"/>'
 ratio=min(920/float(vb.split()[2]),980/float(vb.split()[3]));font=30/ratio
 for label_n,(txt,x,y,tx,ty) in enumerate(labels.get(s['key'],[])):
  art+=f'<g id="{i}-label-{label_n}"><path d="M{x} {y+8}L{tx} {ty}" class="leader"/><text x="{x}" y="{y}" text-anchor="middle" class="label" style="font-size:{font}px">{esc(txt)}</text></g>'
 note='Sakelar uap · potongan ilustratif'
 if view in ['control','contacts','disc','snapmacro','springmacro']:note='Gerak & jarak diperbesar · diperlambat'
 if s['key']=='steam':note='Sesaat sebelum mati ? saluran diperlihatkan'
 if s['key']=='input':note='Ulang dari awal · waktu pemanasan diringkas'
 if s['key']=='proof':note='Putar ulang ringkas · jalur uap diperlihatkan'
 if s['key']=='circuit':note='Ulang detail kontak · saat sakelar ditekan'
 if s['key']=='spring':note='Ulang detail pegas · sebelum & lewat tengah'
 if s['key']=='open':note='Ulang detail kontak · gerak diperbesar'
 if s['key']=='layers':note='Dua lapis terikat; pemisahan ilustratif'
 staticcaption='' if animated else f'<div class="pose-caption"><span>{esc(s["title"])}</span></div>'
 script=f"const id='{i}',duration={d},mode='{s['mode']}',view='{view}';"+RUNTIME
 if animated:
  script+="renderAt(0);const clock={t:0};const tl=gsap.timeline({paused:true});tl.fromTo(clock,{t:0},{t:duration,duration:duration,ease:'none',onUpdate:()=>renderAt(clock.t)},0);window.__timelines=window.__timelines||{};window.__timelines[id]=tl;"
 else:script+="renderAt(duration*.66);window.__timelines=window.__timelines||{};window.__timelines[id]=gsap.timeline({paused:true});"
 write(V/f'compositions/{i}.html',f'<template><style>{CSS}</style><div id="root" data-composition-id="{i}" data-width="1080" data-height="1920"><div class="scene"><h1 class="title" data-var-text="{s["key"]}">{esc(s["title"])}</h1><div class="stage"><svg viewBox="{vb}" role="img" aria-label="{esc(s["title"])}">{defs(i)}{art}</svg></div><div class="note">{esc(note)}</div>{staticcaption}</div></div><script>{script}</script></template>')
 if animated:
  write(V/f'compositions/{i}.motion.json',json.dumps(dict(duration=d,assertions=[dict(kind='staysInFrame',selector='.title'),dict(kind='appearsBy',selector='.stage',bySec=.1)]),indent=2))
  # Mark each causal event at the matching analytic progress, not arbitrary scene cuts.
  marks={'whole':[(.65,'switch-off','hinge')],'steam':[(.35,'steam-route','editorial')],'on':[(.5,'switch-on','hinge')],'close':[(.4,'contacts-close','metal')],'heat':[(.3,'heat-transfer','editorial')],'boil':[(.28,'boiling-onset','editorial')],'route':[(.35,'steam-descent','editorial')],'sensor':[(.38,'sensor-heating','editorial')],'layers':[(.7,'bonded-layers','editorial')],'curve':[(.5,'curvature','editorial')],'snap':[(.49,'disc-snap','metal')],'trip':[(.64,'overcentre-trip','hinge')],'open':[(.58,'contact-gap','metal')],'residual':[(.3,'heat-decay','editorial')],'latch':[(.65,'disc-cools-off-latched','editorial')],'proof':[(.25,'steam-proof','editorial'),(.56,'disc-proof','metal'),(.77,'off-proof','hinge')]}
  for u,kind,asset in marks[s['mode']]:events.append(dict(scene=i,kind=kind,asset=asset,start=round((s['start']+.18+u*(d-.6))*30)/30,progress=u))
hosts=''.join(f'<div id="{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-start="{s["start"]}" data-duration="{s["duration"]}" data-width="1080" data-height="1920" data-track-index="1" data-track-kind="graphics"></div>' for s in plan)
audio='';capshost=''
if animated:
 audio='<audio id="narration" class="clip" src="assets/audio/narration-master.wav" data-start="0" data-duration="90" data-volume="1" data-track-index="3"></audio>'
 groups=json.loads((V/'caption-groups.json').read_text(encoding='utf-8'))
 caps=''.join(f'<div id="phrase-{n:03}" class="clip phrase" data-start="{g["start"]}" data-duration="{g["end"]-g["start"]}"><span>{esc(g["text"])}</span></div>' for n,g in enumerate(groups))
 write(V/'compositions/captions.html','''<template><style>@font-face{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:200 800}#root{position:absolute;inset:0;pointer-events:none}.phrase{position:absolute;left:108px;top:1500px;width:848px;text-align:center;font:600 46px/1.3 Manrope,sans-serif;color:#172B3B;box-sizing:border-box}.phrase span{display:inline-block;box-sizing:border-box;max-width:848px;padding:18px 26px;background:#F8F9F5;border-radius:14px}</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920">'''+caps+'''</div><script>window.__timelines=window.__timelines||{};window.__timelines.captions=gsap.timeline({paused:true});</script></template>''')
 capshost='<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="90" data-width="1080" data-height="1920" data-track-index="2" data-track-kind="captions" style="z-index:20"></div>'
 write(V/'motion-events.json',json.dumps(events,indent=2)+'\n')
write(V/'index.html','''<!doctype html><html lang="id" data-composition-variables='[{"id":"canvas","type":"color","label":"Canvas","default":"#ECEEE9"}]'><head><meta charset="utf-8"><title>Ketel: uap memutus arus</title><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#ECEEE9}.clip{position:absolute;inset:0}#root{position:absolute;inset:0;background:var(--canvas,#ECEEE9)}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="90" data-width="1080" data-height="1920">'''+hosts+capshost+audio+'''</div><script>window.__timelines=window.__timelines||{};window.__timelines.main=gsap.timeline({paused:true});</script></body></html>''')
print(json.dumps(dict(animated=animated,scenes=len(plan),events=len(events))))
