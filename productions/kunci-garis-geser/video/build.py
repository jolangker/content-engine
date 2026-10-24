from pathlib import Path
import json,html,sys,re
V=Path(__file__).resolve().parent
ANIM='--animated' in sys.argv; AUDIO='--audio' in sys.argv
plan=json.loads((V/('timing.json' if AUDIO else 'scene-plan.json')).read_text(encoding='utf-8'))
F=V/'compositions/frames';F.mkdir(parents=True,exist_ok=True)
def make(s):
    sid=s['id'];view=s['view'];dur=s['duration'];e=html.escape
    endon=view in ['front','turn','rotated','return','summary'];cam=view=='cam'
    boxes={'stack':'270 170 220 650','blocked':'220 320 660 510','profile':'220 390 660 430','aligned':'220 320 660 510','low':'425 315 255 500','high':'425 315 255 500'}
    box=boxes.get(view,'-50 120 1050 880')
    defs=f'''<defs><linearGradient id="{sid}-metal"><stop stop-color="#687F91"/><stop offset=".32" stop-color="#D6E0E5"/><stop offset=".65" stop-color="#A6B4BE"/><stop offset="1" stop-color="#71899A"/></linearGradient><linearGradient id="{sid}-case" x2=".7" y2="1"><stop stop-color="#F8F9F5"/><stop offset=".65" stop-color="#D1DADC"/><stop offset="1" stop-color="#A6B4BE"/></linearGradient><linearGradient id="{sid}-key"><stop stop-color="#F29D63"/><stop offset=".45" stop-color="#E57D49"/><stop offset="1" stop-color="#C94422"/></linearGradient></defs>'''
    common=f'<ellipse cx="510" cy="945" rx="350" ry="23" fill="#172B3B" opacity=".08"/>'
    note='Penampang skematis · tidak berskala'
    if endon:
        box='100 100 800 880'
        svg=defs+common+f'''<path d="M400 185H600V350H400Z" fill="url(#{sid}-case)" stroke="#536775" stroke-width="5"/><circle cx="500" cy="580" r="305" fill="url(#{sid}-case)" stroke="#536775" stroke-width="6"/>
<path d="M480 210V350H520V210" fill="#ECEEE9" stroke="#536775" stroke-width="3"/>
<path id="{sid}-spring" d="M500 215L487 228L513 240L487 252L513 264L487 276L513 288L500 300" fill="none" stroke="#536775" stroke-width="6"/>
<rect id="{sid}-upper" x="481" y="300" width="38" height="80" rx="7" fill="url(#{sid}-metal)" stroke="#536775" stroke-width="3"/>
<g id="{sid}-rotor"><circle cx="500" cy="580" r="230" fill="url(#{sid}-metal)" stroke="#172B3B" stroke-width="6"/><circle cx="500" cy="580" r="201" fill="none" stroke="#E0E6E5" stroke-width="3"/>
<rect x="481" y="350" width="38" height="130" rx="8" fill="#2459C4" stroke="#172B3B" stroke-width="3"/>
<path d="M475 480H525V540H552V590H520V699H481V630H455V580H475Z" fill="#172B3B"/>
<path id="{sid}-key" d="M485 480H515V551H540V576H510V683H490V615H469V588H485Z" fill="url(#{sid}-key)"/>
<circle cx="630" cy="680" r="12" fill="#2459C4"/></g>
<path d="M450 350H555" stroke="#167580" stroke-width="5" stroke-dasharray="12 8"/>
<g id="{sid}-arrow"><path d="M690 380A280 280 0 0 1 770 700" fill="none" stroke="#C94422" stroke-width="8"/><path d="M746 685L769 714L791 685" fill="none" stroke="#C94422" stroke-width="8"/></g>
<text x="240" y="130" font-size="32" font-family="Manrope" fill="#172B3B">Tampak ujung · irisan ilustratif</text>'''
        note='Irisan ujung · rumah tetap saat inti berputar'
    elif cam:
        box='0 0 1000 1000'
        svg=defs+f'''<ellipse cx="510" cy="840" rx="370" ry="30" fill="#172B3B" opacity=".08"/><g><path d="M200 360L520 190L700 310L380 480Z" fill="#D4DDE0" stroke="#536775" stroke-width="5"/><path d="M200 360V610L380 730V480Z" fill="#A6B4BE" stroke="#536775" stroke-width="5"/><path d="M380 480L700 310V560L380 730Z" fill="url(#{sid}-metal)" stroke="#536775" stroke-width="5"/><ellipse cx="380" cy="602" rx="94" ry="118" fill="#7D93A1" stroke="#172B3B" stroke-width="5"/></g>
<path d="M380 600L730 440" stroke="#536775" stroke-width="45"/>
<path d="M380 600L730 440" stroke="#D1DADC" stroke-width="28"/>
<g id="{sid}-cam"><circle cx="730" cy="440" r="66" fill="#167580" stroke="#172B3B" stroke-width="4"/><path d="M700 430L645 300Q635 280 657 265L692 250Q710 240 720 266L760 420Z" fill="#167580" stroke="#172B3B" stroke-width="4"/><circle cx="730" cy="440" r="20" fill="#E3EBE6" stroke="#172B3B" stroke-width="4"/></g>
<path d="M560 660L790 550" stroke="#167580" stroke-width="8"/><path d="M768 541L800 544L788 575" fill="none" stroke="#167580" stroke-width="8"/>
<text x="100" y="175" font-size="36" font-family="Manrope" fill="#172B3B">Sambungan belakang</text><text x="570" y="780" font-size="33" font-family="Manrope" fill="#167580">Ke mekanisme pengunci</text>'''
        note='Penggerak belakang · bentuk berbeda antarproduk'
    else:
        svg=defs+common+f'''<g id="{sid}-shell"><rect x="190" y="220" width="650" height="650" rx="45" fill="url(#{sid}-case)" stroke="#536775" stroke-width="5"/><path d="M225 260H800M225 840H800" stroke="#F8F9F5" stroke-width="8"/></g>
<rect x="205" y="500" width="620" height="340" rx="15" fill="url(#{sid}-metal)" stroke="#172B3B" stroke-width="4"/>
<rect x="205" y="710" width="620" height="100" fill="#536775" opacity=".2"/>
<path d="M210 500H820" stroke="#167580" stroke-width="5" stroke-dasharray="14 10"/>
<g id="{sid}-key"><path id="{sid}-blade" d="" fill="url(#{sid}-key)" stroke="#8F3D27" stroke-width="4"/><rect x="75" y="705" width="135" height="115" rx="35" fill="url(#{sid}-key)" stroke="#8F3D27" stroke-width="4"/><ellipse cx="127" cy="760" rx="27" ry="33" fill="#F8F9F5" stroke="#8F3D27" stroke-width="4"/></g>'''
        for i,x in enumerate([300,405,510,615,720]):
            hidden=(view=='stack' and i!=0) or (view in ['low','high'] and i!=2)
            svg+=f'''<g opacity="{0 if hidden else 1}"><path d="M{x-26} 265H{x+26}V748H{x-26}Z" fill="#ECEEE9" opacity=".7" stroke="#71899A" stroke-width="2"/>
<path id="{sid}-spring-{i}" fill="none" stroke="#536775" stroke-width="4" stroke-linejoin="round"/>
<rect id="{sid}-upper-{i}" x="{x-19}" y="300" width="38" height="180" rx="6" fill="url(#{sid}-metal)" stroke="#536775" stroke-width="3"/>
<path id="{sid}-lower-{i}" fill="{'#2459C4' if i==2 else '#829EBA'}" stroke="#172B3B" stroke-width="3"/>
<circle cx="{x}" cy="244" r="6" fill="{'#2459C4' if i==2 else '#536775'}"/></g>'''
        keygroup=re.search(r'<g id="'+sid+r'-key">.*?</g>',svg,re.S).group()
        svg=svg.replace(keygroup,'')+keygroup.replace('<rect x="75"','<rect id="'+sid+'-bow" x="75"').replace('<ellipse cx="127"','<ellipse id="'+sid+'-hole" cx="127"')
        svg+=f'<path id="{sid}-seam" d="M250 500H780" stroke="#167580" stroke-width="9" opacity="0"/><g id="{sid}-labels" font-family="Manrope" font-size="32" fill="#172B3B">'
        if view in ['side','shell','insert','summary']:
            svg+='<text x="225" y="180">Rumah kunci</text><path d="M345 190V215" stroke="#536775" stroke-width="3"/><text x="640" y="915">Inti / plug</text><path d="M715 870V880" stroke="#536775" stroke-width="3"/>'
        if view=='stack':svg+='<text x="340" y="285" font-size="24">Pegas</text><text x="340" y="435" font-size="24">Pin atas</text><text x="340" y="630" font-size="24">Pin bawah</text>'
        if view in ['blocked','aligned']:svg+='<text x="265" y="175" font-size="30">Batas inti dan rumah</text><path d="M235 185V490H265" fill="none" stroke="#167580" stroke-width="3"/>'
        if view=='profile':svg+='<path d="M300 540H720" stroke="#167580" stroke-width="3" stroke-dasharray="8 8"/>'
        svg+='</g>'
        note='Contoh terpisah · satu gerigi terlalu rendah' if view=='low' else 'Contoh terpisah · satu gerigi terlalu tinggi' if view=='high' else note
    code=f'''const tl=gsap.timeline({{paused:true}}); const sid='{sid}';
const el=n=>document.getElementById(sid+'-'+n);
'''
    if endon:
        a0=0;a1=0
        if view=='front':a0=0;a1=0
        if view=='turn':a1=68
        if view=='rotated':a0=a1=68
        if view=='return':a0=68;a1=0
        if view=='summary':a1=45
        code+=f'''const st={{a:{a0}}}; const draw=()=>{{el('rotor').setAttribute('transform',`rotate(${{st.a}} 500 580)`);el('upper').setAttribute('y','270');}};draw();
'''
        if ANIM and a0!=a1:code+=f"tl.fromTo(st,{{a:{a0}}},{{a:{a1},duration:{dur*.66},ease:'sine.inOut',onUpdate:draw}},.7);"
        elif not ANIM:code+=f"st.a={(a0+a1)/2};draw();"
        if view=='front':code+="el('arrow').setAttribute('opacity','0');el('key').setAttribute('opacity','.25');"
    elif cam:
        code+="const st={a:0};const draw=()=>el('cam').setAttribute('transform',`rotate(${st.a} 730 440)`);draw();"
        code+=f"tl.fromTo(st,{{a:0}},{{a:65,duration:{dur*.64},ease:'sine.inOut',onUpdate:draw}},.7);" if ANIM else "st.a=35;draw();"
    else:
        # One key profile drives key and both pins; lower pins remain rigid.
        q0=q1=0
        if view in ['side','stack','blocked','shell']:q0=q1=-900
        if view=='insert':q0=-900;q1=0
        if view=='withdraw':q0=0;q1=-900
        error=55 if view=='low' else -55 if view=='high' else 0
        code+=f'''const xs=[300,405,510,615,720], ls=[120,180,140,200,160];
const ys=ls.map((l,i)=>500+l+(i===2?{error}:0));
const profile=[[190,735],[245,735],...xs.map((x,i)=>[x,ys[i]]),[780,720],[805,745]];
function height(x){{if(x<190||x>805)return 745;for(let j=1;j<profile.length;j++){{if(x<=profile[j][0]){{const a=profile[j-1],b=profile[j];return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]);}}}}return 745;}}
el('blade').setAttribute('d','M190 800L'+profile.map(p=>p.join(' ')).join('L')+'L805 800Z');
const st={{q:{q0},shell:1}};
function draw(){{el('blade').setAttribute('d',`M${{190+st.q}} 800L`+profile.map(p=>[p[0]+st.q,p[1]].join(' ')).join('L')+`L${{805+st.q}} 800Z`);el('bow').setAttribute('x',75+st.q);el('hole').setAttribute('cx',127+st.q);xs.forEach((x,i)=>{{const bottom=height(x-st.q),split=bottom-ls[i];el('lower-'+i).setAttribute('d',`M${{x-19}} ${{split}}H${{x+19}}V${{bottom-15}}L${{x}} ${{bottom}}L${{x-19}} ${{bottom-15}}Z`);el('upper-'+i).setAttribute('y',split-180);const a=265,b=split-180;let p=`M${{x}} ${{a}}`;for(let k=1;k<9;k++)p+=`L${{x+(k%2?12:-12)}} ${{a+(b-a)*k/9}}`;p+=`L${{x}} ${{b}}`;el('spring-'+i).setAttribute('d',p);}});el('shell').setAttribute('opacity',st.shell);}}
draw();
'''
        if ANIM and q0!=q1:code+=f"tl.fromTo(st,{{q:{q0}}},{{q:{q1},duration:{dur*.72},ease:'none',onUpdate:draw}},.45);"
        elif not ANIM and q0!=q1:code+="st.q=-180;draw();"
        if view=='shell' and ANIM:code+=f"tl.fromTo(st,{{shell:1}},{{shell:.22,duration:1.4,ease:'power2.inOut',onUpdate:draw}},.8);"
        if view=='aligned':code+=f"tl.fromTo('#{sid}-seam',{{opacity:0}},{{opacity:1,duration:.5}},2);" if ANIM else "el('seam').setAttribute('opacity',1);"
        if view in ['low','high']:
            target='upper' if view=='low' else 'lower'
            code+=f"tl.fromTo('#{sid}-{target}-2',{{stroke:'#536775'}},{{stroke:'#C94422',duration:.4}},1.5);" if ANIM else ''
    if ANIM:code+=f"tl.fromTo('#{sid}-sub',{{opacity:0}},{{opacity:1,duration:.35}},.2);"
    code+=f"tl.to({{}},{{duration:.01}},{dur-.02});window.__timelines['{sid}']=tl;"
    return f'''<template><style>
@font-face{{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:100 900}}
@font-face{{font-family:'IBM Plex Mono';src:url('assets/fonts/ibm-plex-mono.ttf')}}
#root{{position:absolute;inset:0;color:#172B3B;font-family:Manrope;overflow:hidden}}
.ground{{position:absolute;inset:0;background:#ECEEE9}}.bench{{position:absolute;left:64px;top:435px;width:952px;height:987px;background:#F8F9F5;border-radius:42px}}
.title{{position:absolute;left:100px;top:163px;width:850px;margin:0;font:800 77px/1.1 Manrope;letter-spacing:-3px}}
.sub{{position:absolute;left:100px;top:355px;width:840px;font:500 35px/1.35 Manrope}}
.diagram{{position:absolute;left:80px;top:455px;width:920px;height:935px;overflow:hidden}}
.note{{position:absolute;left:102px;top:1455px;width:840px;font:400 29px/1.35 'IBM Plex Mono';color:#536775}}
</style><div id="root" data-composition-id="{sid}" data-duration="{dur}" data-width="1080" data-height="1920"><div id="{sid}-ground" class="clip ground" data-start="0" data-duration="{dur}" data-track-index="0"></div><div class="bench"></div><h1 class="title">{e(s['title'])}</h1><div id="{sid}-sub" class="sub">{e(s['subtitle'])}</div><svg class="diagram" viewBox="{box}" xmlns="http://www.w3.org/2000/svg" aria-label="Original schematic {view} pin-tumbler cylinder">{svg}</svg><div class="note">{e(note)}</div></div><script>{code}</script></template>'''
for s in plan['scenes']:(F/f"{s['id']}.html").write_text(make(s),encoding='utf-8')
hosts=''.join(f'<div id="{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/frames/{s["id"]}.html" data-start="{s["start"]}" data-duration="{s["duration"]}" data-width="1080" data-height="1920" data-track-index="0"></div>' for s in plan['scenes'])
aud=cap=''
if AUDIO:
    m=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'));voice=m['voices'][0];src=m.get('placed_narration',{}).get('path',voice['path']);dd=m.get('placed_narration',{}).get('duration_s',voice['duration_s'])
    aud=f'<audio id="narration" class="clip" data-start="0.3" data-duration="{dd}" data-track-index="2" data-volume="0.85" src="{src}"></audio>'
    caps=''.join(f'<div class="clip caption" id="caption-{i:03}" data-start="{c["start"]:.3f}" data-duration="{c["end"]-c["start"]:.3f}" data-track-index="0"><span>{html.escape(c["text"])}</span></div>' for i,c in enumerate(plan['captions']))
    (V/'compositions/captions.html').write_text(f'''<template><style>@font-face{{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:100 900}}#root{{position:absolute;inset:0;pointer-events:none}}.caption{{position:absolute;left:108px!important;top:1560px!important;width:846px!important;height:180px!important;display:flex;align-items:center;justify-content:center;text-align:center;font:600 46px/1.36 Manrope;color:#172B3B;box-sizing:border-box}}.caption span{{background:#F8F9F5;border-radius:14px;padding:14px 22px;max-width:100%;box-sizing:border-box}}</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="90">{caps}</div><script>window.__timelines['captions']=gsap.timeline({{paused:true}});</script></template>''',encoding='utf-8')
    cap='<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="90" data-width="1080" data-height="1920" data-track-index="1" data-track-kind="captions" style="z-index:20"></div>'
(V/'index.html').write_text(f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>*{{box-sizing:border-box;margin:0}}html,body{{width:100%;height:100%;overflow:hidden;background:#ECEEE9}}#root{{position:relative;width:100%;height:100%}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="90" data-width="1080" data-height="1920">{hosts}{aud}{cap}</div><script>window.__timelines['main']=gsap.timeline({{paused:true}});</script></body></html>''',encoding='utf-8')
print(json.dumps(dict(animated=ANIM,audio=AUDIO,scenes=len(plan['scenes']))))
