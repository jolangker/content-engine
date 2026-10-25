from pathlib import Path
import json, html, sys
V=Path(__file__).resolve().parent; F=V/'compositions/frames';F.mkdir(parents=True,exist_ok=True)
ANIM='--animate' in sys.argv; AUDIO='--audio' in sys.argv
plan=json.loads((V/('timing.json' if AUDIO else 'scene-plan.json')).read_text(encoding='utf-8'))
e=html.escape
def pump(sid, bottle=False, shell=False):
    z=f'''<defs><linearGradient id="{sid}-metal" x2="0" y2="1"><stop stop-color="#D9E1E3"/><stop offset=".45" stop-color="#A6B4BE"/><stop offset="1" stop-color="#7B909E"/></linearGradient><linearGradient id="{sid}-poly" x2=".8" y2="1"><stop stop-color="#F8F9F5"/><stop offset="1" stop-color="#B9C8CD"/></linearGradient><linearGradient id="{sid}-orange" x2="1" y2="1"><stop stop-color="#E16D44"/><stop offset="1" stop-color="#C94422"/></linearGradient></defs>'''
    if bottle:
        z+=f'''<ellipse cx="540" cy="1190" rx="300" ry="27" fill="#172B3B" opacity=".08"/><path d="M430 625V710Q310 740 310 850V1120Q310 1160 355 1160H725Q770 1160 770 1120V850Q770 740 650 710V625Z" fill="url(#{sid}-poly)" stroke="#718693" stroke-width="5"/><path d="M325 895H755V1116Q755 1144 718 1144H362Q325 1144 325 1116Z" fill="#167580" opacity=".24"/><path d="M350 920H730" stroke="#167580" stroke-width="4" opacity=".7"/><path d="M450 610H635V660H450Z" fill="url(#{sid}-metal)" stroke="#536775" stroke-width="4"/>'''
    z+=f'''<g id="{sid}-case"><path d="M125 270Q130 230 200 230H720L855 310V390H685V520L610 605H400L280 560L210 500V340H125Z" fill="url(#{sid}-poly)" stroke="#718693" stroke-width="5"/></g>
<g id="{sid}-tube"><path d="M600 510V1100" fill="none" stroke="#718693" stroke-width="30"/><path d="M600 510V1100" fill="none" stroke="#F8F9F5" stroke-width="19"/><path d="M600 510V1100" fill="none" stroke="#167580" stroke-width="8" opacity=".32"/></g>
<path id="{sid}-prime-front" d="M600 1100V1100" fill="none" stroke="#167580" stroke-width="11"/>
<rect x="245" y="325" width="425" height="190" rx="22" fill="url(#{sid}-metal)" stroke="#536775" stroke-width="5"/>
<rect x="265" y="345" width="380" height="150" rx="7" fill="#F8F9F5" stroke="#536775" stroke-width="3"/>
<rect id="{sid}-liquid" x="310" y="350" width="330" height="140" fill="#167580" opacity=".23"/>
<path id="{sid}-spring" d="" fill="none" stroke="#536775" stroke-width="6" stroke-linejoin="round"/>
<g id="{sid}-piston"><path d="M220 370H232V408H280V432H232V470H220Z" fill="url(#{sid}-metal)" stroke="#536775" stroke-width="3"/><rect x="280" y="352" width="30" height="136" rx="5" fill="#2459C4" stroke="#172B3B" stroke-width="4"/><path d="M285 355V485" stroke="#86ABEE" stroke-width="6"/></g>
<path d="M600 495V565" stroke="#536775" stroke-width="55"/><path d="M600 495V565" stroke="#F8F9F5" stroke-width="38"/>
<g id="{sid}-in-seat"><path d="M570 550H580L600 570L620 550H630" fill="none" stroke="#536775" stroke-width="8"/></g>
<circle id="{sid}-in-ball" cx="600" cy="547" r="18" fill="#2459C4" stroke="#172B3B" stroke-width="3"/>
<path d="M650 420H810" stroke="#536775" stroke-width="58"/><path d="M650 420H815" stroke="#F8F9F5" stroke-width="40"/>
<path d="M700 390V405L690 420L700 435V450" fill="none" stroke="#536775" stroke-width="8"/>
<circle id="{sid}-out-ball" cx="714" cy="420" r="18" fill="#2459C4" stroke="#172B3B" stroke-width="3"/>
<path d="M800 378H850V462H800Z" fill="url(#{sid}-metal)" stroke="#172B3B" stroke-width="4"/><path d="M810 410H850V430H810Z" fill="#172B3B"/>
<g id="{sid}-lever"><path d="M185 277Q160 275 150 300L156 421L105 650Q105 669 129 678L168 680L220 435V295Q210 275 185 277Z" fill="url(#{sid}-orange)" stroke="#8E3822" stroke-width="5"/><circle cx="185" cy="295" r="11" fill="#F8F9F5" stroke="#172B3B" stroke-width="4"/></g>
<g id="{sid}-out-flow" fill="none" stroke="#167580" stroke-width="8" stroke-linecap="round"><path d="M655 420H685M747 420H790"/><path d="M778 408L793 420L778 432"/></g>
<g id="{sid}-in-flow" fill="none" stroke="#167580" stroke-width="8" stroke-linecap="round"><path d="M600 1030V600M600 510V498"/><path d="M588 630L600 611L612 630"/></g>
<g id="{sid}-spray" fill="#167580">'''
    for i in range(22):
        x=865+(i%6)*27;y=420+(i//6-1.5)*(12+(i%6)*10)
        z+=f'<circle id="{sid}-drop-{i}" cx="{x}" cy="{y}" r="{4+(i%3)}"/>'
    z+=f'''</g><g id="{sid}-vent" fill="none" stroke="#2459C4" stroke-width="7"><path d="M795 700H700V790H670" stroke-dasharray="12 9"/><path d="M680 777L663 790L680 803"/></g>'''
    return z
def labels(sid,kind):
    if kind=='mechanism':return '<g font-family="Manrope" font-size="31" fill="#172B3B"><text x="215" y="210">Piston</text><path d="M290 225V310" stroke="#2459C4" stroke-width="3"/><text x="430" y="210">Pegas</text><path d="M490 225V360" stroke="#536775" stroke-width="3"/><text x="480" y="670">Masuk</text><text x="740" y="550">Keluar</text><path d="M780 528L750 450" stroke="#536775" stroke-width="3"/></g>'
    return ''
def make(s):
    sid=s['id'];dur=s['duration'];view=s['view'];whole=view in ['whole','vent','prime','final'];macro=view in ['inlet','outlet','close','spray']
    box='20 180 1000 1040' if whole else '65 190 890 620'
    note='Penampang ilustratif · gerak diperlambat · tidak berskala'
    z=pump(sid,whole)
    if view in ['chamber','press','spring','expand','ready']:z+=labels(sid,'mechanism')
    if view=='inlet':
        box='410 410 400 320';z+=f'<text x="438" y="695" font-size="23" fill="#172B3B" font-family="Manrope">Dudukan tetap</text><path d="M540 670L582 580" stroke="#536775" stroke-width="2"/>';note='Makro katup masuk · tekanan dari ruang pompa'
    if view in ['outlet','close']:
        box='580 290 360 310';z+='<text x="620" y="325" font-size="23" fill="#172B3B" font-family="Manrope">Katup keluar</text>';note='Makro jalur keluar · dudukan tetap, katup bergeser'
    if view=='spray':box='620 265 410 320';note='Nosel membentuk pola · partikel tidak berskala'
    if view=='refill':box='350 280 430 850';note='Langkah isi ulang · dari pipa celup ke ruang pompa'
    if view=='vent':note='Jalur udara skematis · terpisah dari saluran cairan'
    if view=='prime':note='Kondisi awal berbeda · jumlah gerakan tidak ditetapkan'
    if view=='explode':
        z=f'''<defs><linearGradient id="{sid}-metal" x2="0" y2="1"><stop stop-color="#D9E1E3"/><stop offset="1" stop-color="#A6B4BE"/></linearGradient></defs><ellipse cx="500" cy="810" rx="390" ry="35" fill="#172B3B" opacity=".07"/>
<g id="{sid}-exp-case"><path d="M140 150H700L860 240V350H660L590 420H280L180 340Z" fill="url(#{sid}-metal)" stroke="#536775" stroke-width="5"/><text x="230" y="112" font-size="38" fill="#172B3B" font-family="Manrope">Cangkang</text></g>
<path d="M180 480H800" stroke="#A6B4BE" stroke-width="3" stroke-dasharray="12 12"/>
<g id="{sid}-exp-piston"><path d="M145 450H330V540H145Z" fill="#2459C4" stroke="#172B3B" stroke-width="4"/><path d="M80 480H145" stroke="#A6B4BE" stroke-width="20"/><text x="120" y="610" font-size="38" fill="#172B3B" font-family="Manrope">Piston</text></g>
<g id="{sid}-exp-spring"><path d="M380 495L405 460L435 530L465 460L495 530L525 460L550 495" fill="none" stroke="#536775" stroke-width="8"/><text x="385" y="610" font-size="38" fill="#172B3B" font-family="Manrope">Pegas</text></g>
<g id="{sid}-exp-valves"><path d="M615 465H660V530H615M715 465H760V530H715" fill="#F8F9F5" stroke="#536775" stroke-width="4"/><circle cx="642" cy="497" r="18" fill="#2459C4"/><circle cx="742" cy="497" r="18" fill="#2459C4"/><text x="594" y="610" font-size="38" fill="#172B3B" font-family="Manrope">Dua katup</text></g>
<g id="{sid}-exp-nozzle"><rect x="830" y="455" width="80" height="85" rx="8" fill="#167580" stroke="#172B3B" stroke-width="4"/><text x="800" y="700" font-size="38" fill="#172B3B" font-family="Manrope">Nosel</text></g>'''
        box='0 20 1000 900';note='Jarak antarbagian diperbesar untuk penjelasan'
    if view=='compare':
        z=pump(sid+'a')+'';z=f'<g transform="translate(0 -80) scale(.95)">{z}</g>'
        z+=f'<g transform="translate(0 470) scale(.95)">{pump(sid+"b")}</g>'
        z+='<g font-size="44" font-family="Manrope" font-weight="800"><text x="100" y="145" fill="#C94422">TEKAN: keluar</text><text x="100" y="715" fill="#167580">LEPAS: isi ulang</text></g>'
        box='50 70 930 1030';note='Dua keadaan dibandingkan · arah aliran diberi panah'
    code=f"const tl=gsap.timeline({{paused:true}});const sid='{sid}';const el=n=>document.getElementById(sid+'-'+n);\n"
    if view=='explode':
        if ANIM:
            code+=f"tl.fromTo(el('exp-case'),{{y:150,opacity:.2}},{{y:0,opacity:1,duration:1.4,ease:'power2.out'}},.4);tl.fromTo(el('exp-piston'),{{x:160}},{{x:0,duration:1.3,ease:'power2.out'}},1);tl.fromTo(el('exp-nozzle'),{{x:-100}},{{x:0,duration:1.3,ease:'power2.out'}},1);"
    else:
        def runtime(prefix,mode,animated):
            # State q: 0=out/expanded, 1=in/compressed. Valve opening independent but causally sequenced.
            q0=q1=0;iv0=iv1=0;ov0=ov1=0;flow='none'
            if mode=='press':q1=.2;ov1=1;flow='out'
            elif mode=='inlet':q0=.2;q1=.45;ov0=ov1=1;flow='out'
            elif mode=='outlet':q0=.45;q1=.7;ov0=ov1=1;flow='out'
            elif mode=='spray':q0=.7;q1=1;ov0=ov1=1;flow='out'
            elif mode=='spring':q0=1;q1=.8;iv1=1;flow='in'
            elif mode=='expand':q0=.8;q1=.6;iv0=iv1=1;flow='in'
            elif mode=='close':q0=q1=.6;ov0=ov1=0
            elif mode=='refill':q0=.6;q1=0;iv0=iv1=1;flow='in'
            elif mode=='prime':q0=1;q1=0;iv0=iv1=1;flow='in'
            elif mode in ['ready','vent']:q0=q1=0
            # Return state has inlet open during movement, then seats at end.
            txt=f'''{{const p='{prefix}', E=n=>document.getElementById(p+'-'+n),st={{q:{q0},iv:{iv0},ov:{ov0},f:0}};
const draw=()=>{{const ang=28*st.q*Math.PI/180,x=185+35*Math.cos(ang)+140*Math.sin(ang)-220;E('piston').setAttribute('transform',`translate(${{x}} 0)`);E('liquid').setAttribute('x',310+x);E('liquid').setAttribute('width',330-x);E('liquid').setAttribute('opacity',{'.23*Math.min(1,st.f/4)' if mode=='prime' else '.23'});E('prime-front').setAttribute('opacity','{1 if mode=='prime' else 0}');E('prime-front').setAttribute('d',`M600 1100V${{1100-600*Math.min(1,st.f/4)}}`);E('lever').setAttribute('transform',`rotate(${{-28*st.q}} 185 295)`);E('in-ball').setAttribute('cy',547-32*st.iv);E('out-ball').setAttribute('cx',714+29*st.ov);let a=320+x,b=630,d=`M${{a}} 420`;for(let i=1;i<13;i++)d+=`L${{a+(b-a)*i/13}} ${{420+(i%2?23:-23)}}`;d+=`L${{b}} 420`;E('spring').setAttribute('d',d);E('case').setAttribute('opacity','.13');E('tube').setAttribute('opacity','{1 if whole or mode=='refill' else .45}');E('vent').setAttribute('opacity','{1 if mode=='vent' else 0}');E('out-flow').setAttribute('opacity',{'st.ov' if flow=='out' else 0});E('in-flow').setAttribute('opacity',{'st.iv' if flow=='in' else 0});E('in-flow').setAttribute('stroke-dasharray','20 15');E('in-flow').setAttribute('stroke-dashoffset',st.f*120);E('out-flow').setAttribute('stroke-dasharray','15 10');E('out-flow').setAttribute('stroke-dashoffset',-st.f*100);E('spray').setAttribute('opacity',{'st.ov' if mode in ['spray','whole','final'] else 0});for(let i=0;i<22;i++){{const dr=E('drop-'+i);dr.setAttribute('transform',`translate(${{((st.f*50+i*9)%90)}} ${{(i%2?1:-1)*st.f*2}})`);}}}};draw();
'''
            if not animated:
                if mode in ['whole','final']:txt+='st.q=.7;st.ov=1;'
                else:txt+=f'st.q={(q0+q1)/2};st.iv={iv1};st.ov={ov1};'
                txt+='draw();'
            elif mode in ['whole','final']:
                span=dur*.34
                txt+=f"tl.to(st,{{q:1,duration:{span},ease:'sine.inOut',onUpdate:draw}},.2);tl.to(st,{{ov:1,duration:.25,onUpdate:draw}},.65);tl.to(st,{{ov:0,duration:.15,onUpdate:draw}},{span+.25});tl.to(st,{{q:0,iv:1,duration:{span},ease:'sine.inOut',onUpdate:draw}},{span+.45});tl.to(st,{{iv:0,duration:.2,onUpdate:draw}},{span*2+.5});tl.to(st,{{f:3,duration:{dur*.8},ease:'none',onUpdate:draw}},.3);"
            else:
                txt+=f"tl.to(st,{{q:{q1},iv:{iv1},ov:{ov1},f:4,duration:{dur*.72},ease:'none',onUpdate:draw}},.4);"
                if mode in ['spring','expand','refill','prime']:txt+=f"tl.to(st,{{iv:0,duration:.2,onUpdate:draw}},{dur*.86});"
            return txt+'}\n'
        if view=='compare':code+=runtime(sid+'a','inlet',ANIM)+runtime(sid+'b','refill',ANIM)
        else:code+=runtime(sid,view,ANIM)
    if ANIM:code+=f"tl.fromTo('#{sid}-sub',{{opacity:.15}},{{opacity:1,duration:.4}},.15);"
    code+=f"window.__timelines['{sid}']=tl;"
    return f'''<meta charset="utf-8"><template><style>@font-face{{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:100 900}}@font-face{{font-family:'IBM Plex Mono';src:url('assets/fonts/ibm-plex-mono.ttf')}}#root{{position:absolute;inset:0;color:#172B3B;font-family:Manrope;overflow:hidden}}.ground{{position:absolute;inset:0;background:#ECEEE9}}.bench{{position:absolute;left:64px;top:490px;width:952px;height:940px;background:#F8F9F5;border-radius:42px}}.title{{position:absolute;left:100px;top:175px;width:865px;margin:0;font:800 76px/1.1 Manrope;letter-spacing:-3px}}.sub{{position:absolute;left:100px;top:385px;width:840px;font:500 36px/1.35 Manrope}}.diagram{{position:absolute;left:85px;top:500px;width:910px;height:900px;overflow:hidden}}.note{{position:absolute;left:102px;top:1460px;width:840px;font:400 27px/1.4 'IBM Plex Mono';color:#536775}}</style><div id="root" data-composition-id="{sid}" data-duration="{dur}" data-width="1080" data-height="1920"><div id="{sid}-ground" class="clip ground" data-start="0" data-duration="{dur}" data-track-index="0"></div><div class="bench"></div><h1 class="title">{e(s['title'])}</h1><div id="{sid}-sub" class="sub">{e(s['subtitle'])}</div><svg class="diagram" viewBox="{box}" xmlns="http://www.w3.org/2000/svg" aria-label="Original schematic {view} trigger pump">{z}</svg><div class="note">{e(note)}</div></div><script>{code}</script></template>'''
for s in plan['scenes']:(F/f'{s["id"]}.html').write_text(make(s),encoding='utf-8')
hosts=''.join(f'<div id="{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/frames/{s["id"]}.html" data-start="{s["start"]}" data-duration="{s["duration"]}" data-width="1080" data-height="1920" data-track-index="0"></div>' for s in plan['scenes'])
audio=caps=''
if AUDIO:
    m=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'));v=m['placed_narration']
    audio=f'<audio id="narration" class="clip" data-start="{v["offset"]}" data-duration="{v["duration_s"]}" data-track-index="2" data-volume="0.85" src="{v["path"]}"></audio>'
    captions=''.join(f'<div class="clip caption" id="caption-{i:03}" data-start="{c["start"]:.3f}" data-duration="{c["end"]-c["start"]:.3f}" data-track-index="0"><span>{e(c["text"])}</span></div>' for i,c in enumerate(plan['captions']))
    (V/'compositions/captions.html').write_text(f'''<meta charset="utf-8"><template><style>@font-face{{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:100 900}}#root{{position:absolute;inset:0;pointer-events:none}}.caption{{position:absolute;left:108px!important;top:1560px!important;width:846px!important;height:180px!important;display:flex;align-items:center;justify-content:center;text-align:center;font:600 46px/1.36 Manrope;color:#172B3B;box-sizing:border-box}}.caption span{{background:#F8F9F5;border-radius:14px;padding:14px 22px;max-width:100%;box-sizing:border-box}}</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="90">{captions}</div><script>window.__timelines['captions']=gsap.timeline({{paused:true}});</script></template>''',encoding='utf-8')
    caps='<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="90" data-width="1080" data-height="1920" data-track-index="1" data-track-kind="captions" style="z-index:20"></div>'
(V/'index.html').write_text(f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>*{{box-sizing:border-box;margin:0}}html,body{{width:100%;height:100%;overflow:hidden;background:#ECEEE9}}#root{{position:relative;width:100%;height:100%}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="90" data-width="1080" data-height="1920">{hosts}{audio}{caps}</div><script>window.__timelines['main']=gsap.timeline({{paused:true}});</script></body></html>''',encoding='utf-8')
print(json.dumps(dict(animated=ANIM,audio=AUDIO,scenes=len(plan['scenes']))))
