"""Editable 2.5D music-box composition, static poses first, animation after board verification."""
from pathlib import Path
import json, math, html, sys
V=Path(__file__).resolve().parent
animated='--animate' in sys.argv
plan=json.loads((V/('timing.json' if animated else 'scene-plan.json')).read_text(encoding='utf-8'))
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def e(s):return html.escape(str(s),quote=True)
CSS='''@font-face{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:200 800}@font-face{font-family:'IBM Plex Mono';src:url('assets/fonts/ibm-plex-mono.ttf')}*{box-sizing:border-box}#root{position:absolute;inset:0;color:#172B3B;font-family:Manrope,sans-serif}.scene{position:absolute;inset:0;background:#ECEEE9}.title{position:absolute;left:108px;top:205px;width:800px;margin:0;font-size:76px;line-height:1.08;font-weight:800;letter-spacing:-3px}.stage{position:absolute;left:70px;top:425px;width:910px;height:680px}.stage svg{width:100%;height:100%;overflow:visible}.note{position:absolute;left:108px;top:1098px;width:795px;font:28px/1.3 'IBM Plex Mono',monospace;color:#536775}svg .edge{stroke:#172B3B;stroke-width:3;stroke-linejoin:round}svg .label{font:36px Manrope,sans-serif;fill:#172B3B}svg .small{font:29px 'IBM Plex Mono',monospace;fill:#536775}svg .call{stroke:#536775;stroke-width:2;fill:none}'''
def defs(i):return f'''<defs>
<linearGradient id="{i}-steel" x1="0" y1="0" x2="0.8" y2="1"><stop stop-color="#E5ECEE"/><stop offset=".48" stop-color="#ABBBC5"/><stop offset="1" stop-color="#708A9A"/></linearGradient>
<linearGradient id="{i}-brass" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#E6D7A0"/><stop offset=".4" stop-color="#BBA057"/><stop offset=".8" stop-color="#D8C585"/><stop offset="1" stop-color="#877341"/></linearGradient>
<linearGradient id="{i}-blue" x1="0" y1="0" x2=".8" y2="1"><stop stop-color="#81A9E8"/><stop offset=".6" stop-color="#2459C4"/><stop offset="1" stop-color="#1C3F7B"/></linearGradient>
<linearGradient id="{i}-wood" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#B7926C"/><stop offset="1" stop-color="#79583E"/></linearGradient>
<marker id="{i}-arrow" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#C94422"/></marker></defs>'''
def call(x,y,tx,ty,word):return f'<path class="call" d="M{x} {y+15}H{x+80}L{tx} {ty}"/><circle cx="{tx}" cy="{ty}" r="5" fill="#2459C4"/><text class="label" x="{x}" y="{y}">{e(word)}</text>'
def gear(i,name,x,y,r,n,fill='steel'):
    pts=[]
    for k in range(n*4):
        a=k*math.tau/(n*4);rr=r+(6 if k%4 in (1,2) else -5);pts.append(f'{rr*math.cos(a):.2f},{rr*math.sin(a):.2f}')
    p=' '.join(pts)
    return f'''<g transform="translate({x} {y})"><g id="{i}-{name}"><polygon points="{p}" transform="translate(0 11)" fill="#536775" class="edge"/><polygon points="{p}" fill="url(#{i}-{fill})" class="edge"/><circle r="{r*.55}" fill="#D6DFE0" stroke="#536775" stroke-width="3"/><path d="M{-r*.4} 0H{r*.4}M0 {-r*.4}V{r*.4}" stroke="#536775" stroke-width="8"/><circle r="12" fill="#172B3B"/><circle r="4" fill="#F8F9F5"/></g></g>'''
def drum(i):
    pins=''.join(f'<g id="{i}-pin-{n}"><path class="edge" fill="#C9D4D8" d="M{x} 0h8v-27h-8Z"/><ellipse cx="{x+4}" cy="-27" rx="5" ry="3" fill="#F8F9F5"/></g>' for n,x in enumerate([440,480,520,560,600,640,680,720]))
    teeth=''.join(f'<path id="{i}-tooth-{n}" d="M{x} 583V434h24v149Z" fill="url(#{i}-steel)" class="edge"/>' for n,x in enumerate(range(432,744,39)))
    return f'''<g id="{i}-drum"><path d="M412 280H755V445H412Z" fill="url(#{i}-brass)" class="edge"/><ellipse cx="755" cy="362" rx="33" ry="83" fill="#927A3E" class="edge"/><ellipse cx="412" cy="362" rx="32" ry="83" fill="url(#{i}-steel)" class="edge"/><ellipse cx="412" cy="362" rx="12" ry="38" fill="#6B8090"/><path d="M411 277H755" stroke="#F1E7BD" stroke-width="5"/>{pins}</g>
<g id="{i}-comb">{teeth}<path d="M421 570H765V617H421Z" fill="url(#{i}-steel)" class="edge"/><path d="M421 617H765L783 603V583L765 594H421Z" fill="#657E8B" class="edge"/><circle cx="445" cy="594" r="10" fill="#172B3B"/><circle cx="738" cy="594" r="10" fill="#172B3B"/></g>'''
def assembly(i,view):
    wood=f'''<g id="{i}-box"><path d="M94 271H826L903 209H171Z" fill="#BFA88C" class="edge"/><path d="M94 271V638H826V271" fill="url(#{i}-wood)" class="edge"/><path d="M826 271l77 -62v367l-77 62Z" fill="#71543C" class="edge"/><path d="M119 294H800V607H119Z" fill="#D2C0A8" class="edge"/><path d="M120 294l50 -43h700l-70 43Z" fill="#E1D2BD"/></g>'''
    # Mechanical top section retains layered thickness; gear branch is an annotated kinematic connection.
    core=f'''<ellipse cx="480" cy="670" rx="400" ry="25" fill="#172B3B" opacity=".10"/>{wood}
<g id="{i}-mechanism"><path d="M132 455H810V640H132Z" fill="url(#{i}-steel)" class="edge"/><path d="M132 455l45 -31h681l-48 31Z" fill="#D8E1E2" class="edge"/><path d="M810 455l48 -31v185l-48 31Z" fill="#698593" class="edge"/>
<g id="{i}-barrel"><ellipse cx="238" cy="420" rx="104" ry="47" fill="#6C8290" class="edge"/><path d="M134 295V420Q238 478 342 420V295Z" fill="url(#{i}-steel)" class="edge"/><ellipse cx="238" cy="295" rx="104" ry="47" fill="#E4EBEC" class="edge"/><ellipse cx="238" cy="295" rx="83" ry="34" fill="#F8F9F5" stroke="#536775" stroke-width="3"/><path id="{i}-spiral" fill="none" stroke="#C94422" stroke-width="6"/><circle cx="238" cy="295" r="13" fill="#172B3B"/></g>
{gear(i,'drive',237,477,64,16)}{gear(i,'driven',350,477,48,12,'blue')}
<path d="M350 460V362H380" stroke="#536775" stroke-width="13" fill="none"/><path d="M350 460V362H380" stroke="#C1CFD2" stroke-width="5" fill="none"/>
{drum(i)}
<g id="{i}-key"><path d="M176 626h125v38H176Z" fill="url(#{i}-steel)" class="edge"/><ellipse cx="190" cy="645" rx="20" ry="14" fill="#ECEEE9"/><ellipse cx="286" cy="645" rx="20" ry="14" fill="#ECEEE9"/><path d="M230 607v58h15v-58" fill="#C94422" class="edge"/></g>
<g id="{i}-regulator"><path d="M698 198h175v100H698Z" fill="url(#{i}-steel)" class="edge"/><ellipse cx="786" cy="204" rx="65" ry="32" fill="#536775"/><ellipse cx="786" cy="204" rx="52" ry="24" fill="#F8F9F5"/><g id="{i}-rotor"><path d="M742 199q24 -31 44 0q25 31 44 0M742 209q24 31 44 0q25 -31 44 0" fill="none" stroke="#2459C4" stroke-width="11"/></g><path d="M780 220v74l-25 8l25 8l-25 8l25 8v22" fill="none" stroke="#536775" stroke-width="7"/></g>
<path id="{i}-link" d="M392 500H667Q702 500 702 352H765" fill="none" stroke="#2459C4" stroke-width="4" stroke-dasharray="12 9"/>
</g>'''
    if view in ('whole','answer'):labels=call(95,170,235,295,'pegas')+call(480,132,570,280,'pola pin')+call(570,725,680,588,'sisir logam')
    elif view=='explode':labels=call(83,135,230,296,'rumah pegas')+call(450,110,580,275,'silinder berpaku')+call(590,719,686,585,'sisir logam')
    elif view=='gears':labels=call(98,170,235,478,'gigi penggerak')+call(530,700,680,498,'jalur ke governor')
    elif view=='governorlink':labels=call(640,115,786,204,'governor')+call(140,699,660,500,'hubungan roda gigi')
    elif view=='pattern':labels=call(390,220,480,320,'urutan petikan')
    elif view=='roles':labels=call(80,125,236,295,'tenaga')+call(410,125,580,310,'urutan')+call(670,115,787,200,'laju')+call(590,718,680,585,'nada')
    elif view=='cycle':labels=call(103,155,238,295,'tenaga → gerak')+call(518,725,680,585,'petikan → getaran')
    else:labels=call(380,225,584,310,'pin menonjol')
    return core+labels
def spring(i):
    return f'''<ellipse cx="490" cy="643" rx="294" ry="32" fill="#172B3B" opacity=".1"/><path d="M235 286V531Q489 681 743 531V286Z" fill="url(#{i}-steel)" class="edge"/><ellipse cx="489" cy="286" rx="254" ry="121" fill="#DCE5E7" class="edge"/><ellipse cx="489" cy="286" rx="224" ry="99" fill="#F8F9F5" stroke="#536775" stroke-width="4"/><path id="{i}-spiral" fill="none" stroke="#C94422" stroke-width="8"/><circle cx="489" cy="286" r="25" fill="#172B3B"/><path d="M474 280V567H505V280" fill="url(#{i}-steel)" class="edge"/><g id="{i}-key"><path d="M359 568H620V627H359Z" fill="url(#{i}-steel)" class="edge"/><ellipse cx="393" cy="596" rx="23" ry="17" fill="#ECEEE9"/><ellipse cx="585" cy="596" rx="23" ry="17" fill="#ECEEE9"/></g>{call(170,110,489,240,'pegas pita')}{call(620,720,490,597,'kunci pemutar')}
<path d="M779 349q95 110 -8 185" stroke="#C94422" stroke-width="8" fill="none" marker-end="url(#{i}-arrow)"/>'''
def pluck(i):
    return f'''<ellipse cx="420" cy="678" rx="340" ry="27" opacity=".1" fill="#172B3B"/>
<path d="M330 240H382A180 180 0 1 1 382 600H330Z" fill="#8A743F" class="edge"/><circle cx="330" cy="420" r="180" fill="url(#{i}-brass)" class="edge"/><circle cx="330" cy="420" r="145" fill="none" stroke="#E6D6A1" stroke-width="3"/><circle cx="330" cy="420" r="20" fill="url(#{i}-steel)" class="edge"/>
<g id="{i}-pinmacro"><path d="M510 409h49v20h-49Z" fill="url(#{i}-blue)" class="edge"/><path d="M510 409l10 -7h49l-10 7Z" fill="#81A9E8"/><path d="M559 409l10 -7v20l-10 7Z" fill="#173F8A"/></g>
<path id="{i}-leafside" fill="#6C8390" class="edge"/><path id="{i}-leaf" fill="url(#{i}-steel)" class="edge"/>
<path d="M32 174H96V284H32Z" fill="url(#{i}-steel)" class="edge"/><path d="M32 174l24 -16h64v110l-24 16V174Z" fill="#77909C" class="edge"/><circle cx="65" cy="205" r="12" fill="#172B3B"/>
{call(92,110,65,207,'pangkal tetap')}{call(577,160,346,218,'ujung bebas')}{call(640,570,330,420,'silinder')}
<path id="{i}-ring1" d="M386 181q64 38 0 77" stroke="#167580" stroke-width="6" fill="none"/><path id="{i}-ring2" d="M424 165q83 53 0 109" stroke="#167580" stroke-width="4" fill="none"/>'''
def comb(i):
    teeth=''.join(f'<path id="{i}-combtooth-{k}" d="M{x} 554V{240+k*18}h49V554Z" fill="url(#{i}-steel)" class="edge"/>' for k,x in enumerate(range(180,800,77)))
    return f'''<ellipse cx="486" cy="625" rx="350" ry="24" opacity=".1" fill="#172B3B"/>{teeth}<path d="M153 541H815V606H153Z" fill="url(#{i}-steel)" class="edge"/><path d="M153 606H815L847 584v-43l-32 23H153Z" fill="#657D8A" class="edge"/><circle cx="185" cy="571" r="14" fill="#172B3B"/><circle cx="783" cy="571" r="14" fill="#172B3B"/>{call(95,125,205,290,'gigi yang disetel')}{call(552,710,700,569,'pangkal terikat')}'''
def governor(i):
    # Patent FIG 4 topology: two curved flexible wings around a central shaft, fixed circular friction wall.
    return f'''<ellipse cx="500" cy="663" rx="294" ry="30" opacity=".1" fill="#172B3B"/>
<path d="M271 392V462A230 230 0 0 0 731 462V392Z" fill="#647E8F" class="edge"/>
<circle id="{i}-fixedwall" cx="501" cy="392" r="230" fill="url(#{i}-steel)" class="edge"/><circle cx="501" cy="392" r="197" fill="#F8F9F5" stroke="#172B3B" stroke-width="4"/>
<g transform="translate(501 392)"><g id="{i}-wings"><g id="{i}-wingradial"><path d="M30 -28Q155 -132 157 -20Q149 82 62 95L66 48Q132 22 102 -34Q87 -63 30 14Z" fill="url(#{i}-blue)" class="edge"/><path d="M-30 28Q-155 132 -157 20Q-149 -82 -62 -95L-66 -48Q-132 -22 -102 34Q-87 63 -30 -14Z" fill="url(#{i}-blue)" class="edge"/></g><circle r="38" fill="url(#{i}-steel)" class="edge"/><circle r="13" fill="#172B3B"/></g></g>
<path d="M467 392h68v12h-68Z" fill="#C7D3D7" class="edge"/>
<path id="{i}-contact" d="M695 363A197 197 0 0 1 694 429M307 363A197 197 0 0 0 308 429" stroke="#C94422" stroke-width="10" fill="none"/>
{call(110,120,501,178,'dinding diam')}{call(640,686,623,421,'sayap lentur')}
<path d="M775 311q55 75 0 156" stroke="#C94422" stroke-width="7" fill="none" marker-end="url(#{i}-arrow)"/>'''

notes={'whole':'Model pegas · pola pin ilustratif','explode':'Cangkang diangkat · bukan skala asli','spring':'Penampang pegas · gerak diperlambat','gears':'Rasio & jarak ilustratif · garis = hubungan','drum':'Pin diperbesar · putaran diperlambat','pattern':'Pola contoh · bukan lagu tertentu','pluck':'Penampang samping · lenturan diperbesar','release':'Getaran diperlambat agar terlihat','comb':'Panjang & nada ilustratif · bukan pengukuran','governorlink':'Jalur transmisi disederhanakan','governor':'Penampang governor gesek · tutup dibuka','brake':'Kontak diperjelas · dinding tetap diam','roles':'Tenaga, urutan, nada, dan laju','cycle':'Semua bagian terhubung · gerak diperlambat','answer':'Pegas memberi tenaga · pin membawa pola'}
events=[]
for n,s in enumerate(plan):
    i=s['id'];view=s['view'];d=s['duration']
    art=spring(i) if view=='spring' else pluck(i) if view in ('pluck','release') else comb(i) if view=='comb' else governor(i) if view in ('governor','brake') else assembly(i,view)
    # A deterministic clock is the sole driver. Each view has a distinct, meaningful state change.
    pose=3.8 if view in ('release','brake') else 2.7 if view=='explode' else 2.2
    scr=f'''const st={{t:{0 if animated else pose}}};const el=(x)=>document.getElementById('{i}-'+x);const tr=(x,v)=>{{if(el(x))el(x).setAttribute('transform',v)}};const op=(x,v)=>{{if(el(x))el(x).setAttribute('opacity',v)}};
const view='{view}',dur={d};const clamp=(v)=>Math.max(0,Math.min(1,v));
function spiral(cx,cy,rx,ry,turns){{let p='';for(let k=0;k<=300;k++){{let u=k/300,a=u*turns*Math.PI*2,r=.12+.86*u;p+=(k?'L':'M')+(cx+rx*r*Math.cos(a)).toFixed(2)+' '+(cy+ry*r*Math.sin(a)).toFixed(2)}}return p}}
function draw(){{let t=st.t,local=clamp(t/dur),theta=local*260,active=local;
if(view==='spring'){{let winding={str(n==2).lower()},q=clamp((t-.4)/Math.max(1,dur-1));el('spiral').setAttribute('d',spiral(489,286,214,90,winding?3+q*2:5-q*1.4));tr('key',`translate(${{489*(1-Math.cos(t*1.3))}} 0) scale(${{Math.cos(t*1.3)}} 1)`);}}
else if(view==='pluck'||view==='release'){{
 let begin=view==='pluck'?-140:-92,span=view==='pluck'?48:42,u=clamp((t-.45)/(dur*.56)),a=(begin+span*u)*Math.PI/180,px=330+230*Math.cos(a),py=420+230*Math.sin(a);
 // Release when pin passes the fixed free-end x=345; analytical contact deflection before it.
 let aRel=Math.asin(-Math.sqrt(1-(15/230)**2)),uRel=(aRel*180/Math.PI-begin)/span;
 let contact=px>65&&px<=345&&py<230&&u<=uRel;
 let bend=contact?(230-py)/Math.pow((px-65)/280,2):0;
 let relTime=.45+uRel*dur*.56,tau=view==='pluck'?-1:t-relTime,relBend=230-(420+230*Math.sin(aRel));
 if(tau>0)bend=relBend*Math.exp(-2.7*tau)*Math.cos(19*tau);
 let y=230-bend;
 el('leaf').setAttribute('d',`M65 230Q205 230 345 ${{y}}v12Q205 242 65 242Z`);
 el('leafside').setAttribute('d',`M65 242Q205 254 345 ${{y+12}}l13 10Q205 265 65 255Z`);
 tr('pinmacro',`rotate(${{a*180/Math.PI}} 330 420)`);op('ring1',tau>0?Math.exp(-1.8*tau):0);op('ring2',tau>0?Math.exp(-1.4*tau)*.6:0);
 window['state_{i}']={{t,px,py,bend,contact,released:tau>0,rootX:65,rootY:230,freeX:345}};
}}
else if(view==='governor'||view==='brake'){{
 let expand=view==='brake'?1:clamp((t-.7)/(dur*.35)),scale=1+expand*.245,angle=t*100+(view==='brake'?{plan[11]['duration']*100}:0);tr('wings',`rotate(${{angle}})`);tr('wingradial',`scale(${{scale}})`);tr('contact',`rotate(${{angle}} 501 392)`);op('contact',expand>.98?.8:0);window['state_{i}']={{t,expand,scale,wallAngle:0,wingAngle:angle}};
}}
else if(view==='comb'){{for(let k=0;k<8;k++){{let tau=t-.5-k*.32,b=tau>0?Math.exp(-2*tau)*Math.sin(tau*(16+k*2))*14:0,x=180+k*77,y=240+k*18;el('combtooth-'+k).setAttribute('d',`M${{x}} 554Q${{x}} 400 ${{x+b}} ${{y}}h49Q${{x+49}} 400 ${{x+49}} 554Z`);}}}}
else{{
 let q=view==='explode'?clamp((t-.4)/1.8):0;
 tr('box',`translate(0 ${{q*100}})`);op('box',view==='whole'||view==='answer'?.95:.12);tr('drum',`translate(0 ${{-q*95}})`);tr('comb',`translate(0 ${{q*48}})`);tr('regulator',`translate(${{q*35}} ${{-q*100}})`);
 if(el('spiral'))el('spiral').setAttribute('d',spiral(238,295,77,29,4-.5*local));
 tr('drive',`rotate(${{theta}})`);tr('driven',`rotate(${{-theta*16/12}})`);tr('rotor',`rotate(${{t*120}} 786 204)`);
 for(let k=0;k<8;k++){{let a=t*.95+k*.72,y=362+76*Math.cos(a),z=Math.cos(a);tr('pin-'+k,`translate(0 ${{y}}) scale(1 ${{-Math.cos(a)}})`);op('pin-'+k,z>-.12?1:.08);let lift=Math.max(0,362+103*Math.cos(a)-434),x=432+k*39;el('tooth-'+k).setAttribute('d',`M${{x}} 583Q${{x}} 510 ${{x}} ${{434+lift}}h24Q${{x+24}} 510 ${{x+24}} 583Z`);}}
 op('link',view==='gears'||view==='governorlink'||view==='roles'?.8:.13);op('barrel',view==='pattern'||view==='drum'?.32:1);
 window['state_{i}']={{t,driveAngle:theta,drivenAngle:-theta*16/12,explode:q,cylinderAngle:t*.95}};
}}
}}
draw();const tl=gsap.timeline({{paused:true,onUpdate:draw}});tl.to(st,{{t:{d-.001},duration:{d-.001},ease:'none'}},0);window.__timelines['{i}']=tl;
'''
    if not animated:scr=scr.replace(f"tl.to(st,{{t:{d-.001},duration:{d-.001},ease:'none'}},0);",f"tl.to({{}},{{duration:{d-.001}}},0);")
    # Different inspection scales preserve the cylinder/comb relationship rather than repeating whole views.
    vb='0 0 1000 750'
    if view=='pattern':vb='350 185 495 485'
    elif view=='drum':vb='330 170 550 530'
    elif view=='gears':vb='70 245 805 530'
    svg=f'<svg viewBox="{vb}" role="img" aria-label="{e(s["title"])}">{defs(i)}{art}</svg>'
    content=f'''<template><style>{CSS}</style><div id="root" data-composition-id="{i}" data-width="1080" data-height="1920"><div id="{i}-scene" class="scene clip" data-start="0" data-duration="{d}"><h1 class="title" id="{i}-title" data-var-text="title">{e(s['title'])}</h1><div class="stage" id="{i}-stage">{svg}</div><div class="note">{e(notes[view])}</div></div></div><script>{scr}</script></template>'''
    write(V/f'compositions/{i}.html',content)
    if animated:
        times=[(.5,'editorial','inspection attention')]
        if view in ('whole','answer','cycle','drum','pattern','roles'):
            times=[(.2,'contact','coupled mechanism onset')]
            for k in range(8):
                first=((math.acos(72/103)-k*.72)%math.tau)/.95
                for turn in range(2):
                    at=first+turn*math.tau/.95
                    if .08<at<d-.2:times.append((at,'note',f'illustrative tooth {k+1} release from rotating pin'))
        elif view=='explode':times=[(.4,'editorial','explanatory shell separation')]
        elif view=='spring':times=[(.4,'contact','key winding' if n==2 else 'spring release')]
        elif view in ('gears','governorlink'):times=[(.5,'contact','gear transmission onset')]
        elif view in ('pluck','release'):
            if view=='pluck':
                contact_angle=-180-math.asin((230-420)/230)*180/math.pi
                times=[(.45+.56*d*(contact_angle+140)/48,'contact','pin lifts tooth, held through cut')]
            else:
                aRel=math.asin(-math.sqrt(1-(15/230)**2));uRel=(aRel*180/math.pi+92)/42
                times=[(.45+uRel*d*.56,'note','pin leaves free tooth; vibration begins')]
        elif view=='comb':times=[(.5,'note','illustrative tuned tooth response'),(1.46,'note','next illustrative tooth response')]
        elif view in ('governor','brake'):times=[(.7,'contact','wing acceleration'),(.7+d*.35,'friction','wings reach stationary wall')] if view=='governor' else [(.1,'friction','continued wing/wall friction after matching contact state')]
        for at,role,action in times:
            if at<d:events.append(dict(scene=i,time=round((s['start']+at)*30)/30,role=role,action=action))
hosts='\n'.join(f'<div id="{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-variable-values=\'{json.dumps({"title":s["title"]},ensure_ascii=False)}\' data-start="{s["start"]:.6f}" data-duration="{s["duration"]:.6f}" data-width="1080" data-height="1920" data-track-index="1" data-track-kind="graphics"></div>' for s in plan)
audio='';captions=''
if animated:
    am=json.loads((V/'placed_audio.json').read_text(encoding='utf-8'));audio=f'<audio id="narration" class="clip" src="{am["path"]}" data-start="0" data-duration="90" data-volume="1" data-track-index="3"></audio>'
    groups=json.loads((V/'caption-groups.json').read_text(encoding='utf-8'))
    cap=[]
    for k,g in enumerate(groups):
        cap.append(f'<div id="cap-{k:03}" class="clip cap" data-start="{g["start"]:.6f}" data-duration="{g["end"]-g["start"]:.6f}">{e(g["text"])}</div>')
    captionhtml=f'''<template><style>@font-face{{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:200 800}}#root{{position:absolute;inset:0;pointer-events:none}}.cap{{position:absolute;left:108px;top:1180px;width:795px;font:600 44px/1.25 Manrope,sans-serif;color:#172B3B;text-align:left;background:#ECEEE9;padding:4px 0}}</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920">{''.join(cap)}</div><script>window.__timelines['captions']=gsap.timeline({{paused:true}}).to({{}},{{duration:90}},0);</script></template>'''
    write(V/'compositions/captions.html',captionhtml)
    captions='<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="90" data-width="1080" data-height="1920" data-track-index="2" data-track-kind="captions" style="z-index:3"></div>'
root=f'''<!doctype html><html lang="id" data-composition-variables='[{{"id":"ink","type":"color","label":"Engineering ink","default":"#172B3B"}}]'><head><meta charset="utf-8"><title>Kotak musik: pin dan pegas</title><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>*{{box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#ECEEE9}}#root{{position:relative;width:1080px;height:1920px}}.clip[data-composition-src]{{position:absolute;inset:0}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="90" data-width="1080" data-height="1920" data-fps="30">{hosts}{captions}{audio}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines.main=gsap.timeline({{paused:true}}).to({{}},{{duration:90}},0);</script></body></html>'''
write(V/'index.html',root)
if animated:write(V/'motion-events.json',json.dumps(events,indent=2))
else:
    doc='''---
format: 1080x1920
duration: 90s
message: A spring supplies energy; pins encode the sequence; the comb sounds; friction regulates speed.
mode: autonomous
---

# Visual storyboard

Pre-audio static design v1, agent review delegated by --automation; no human approval. All 16 actual mounted compositions are posed before synthesis. Measured timing.json supersedes estimated seconds without changing scene identity. Black-blue contours, shaded thickness and pale inspection bench inherited from board v4. Patent A figures 1 and 4 inspected for assembly/wing topology. Illustrative spacing, ratios, pin size, bending and time are labelled. No air-brake variant mixed in.

'''
    for n,s in enumerate(plan):
        v=s['view'];purpose=s['text']
        poses='approach with tooth at rest → pin contact and lifted free end → pin leaves free end → decaying vibration, fixed root' if v in ('pluck','release') else 'low-speed wings inside wall → radial flex while rotating → first wall contact → restrained rotation, enclosure stationary' if v in ('governor','brake') else 'stored spring → drive gear rotation → opposite meshing gear rotation → cylinder and regulator driven concurrently' if v in ('gears','governorlink','cycle') else 'initial assembled state → explained component motion → labelled changed state'
        doc+=f'''## Frame {n+1}: {s['title']} ({s['start']:g}–{s['end']:g}s)

- id: {s['id']}
- src: compositions/{s['id']}.html
- status: built
- duration: {s['duration']}s
- poster: {s['start']+s['duration']/2:g}s
- scene: {purpose}
- voiceover: {purpose}
- on-screen: {s['title']}
- reads: fixed title first (0–1.7s); functional part/contact (1.7s–end). Captions after measured narration occupy a separate safe band.
- view: {v}; original 2.5D shaded layered illustration; {notes[v]}.
- action and diagnostic poses: {poses}.
- attention: cue active input, show transfer/contact, then follow affected output and hold result. Orange input, blue inspected contact, teal output.
- continuity: brass drum, silver comb and blue active pin/wing retain identity; macros are marked section views. No alternate mechanism introduced. Fixed tooth root and fixed governor wall never rotate with the moving part.
- camera: stable during physical contact; macro/pin pattern views expose relationships, not decorative reframing. Inspection transformations explicitly labelled.
- sound: synchronized material cue for input/contact; distinct reused tonal illustration at tooth release; quiet friction cue at wing/wall contact; editorial separation cue for opened shell. Sustained coupled rotations share onset cue; no constant click loop. Identification/reading holds intentionally silent.
- evidence: C1–C6 in SOURCES.md; see per-claim mapping.

'''
    write(V/'STORYBOARD.md',doc)
print(json.dumps(dict(mode='animation' if animated else 'static',scenes=len(plan),duration=sum(s['duration'] for s in plan))))
