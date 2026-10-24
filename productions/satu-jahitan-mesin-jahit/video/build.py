from pathlib import Path
import json,html,sys

V=Path(__file__).resolve().parent
animated='--animated' in sys.argv
audio='--audio' in sys.argv
plan=json.loads((V/('timing.json' if audio else 'scene-plan.json')).read_text(encoding='utf-8'))

def diagram(s):
    sid=s['id'];view=s['view']
    boxes={'whole':'40 0 1040 1250','reveal':'40 0 1040 1250','anatomy':'50 0 1000 1250','needle':'285 280 530 690','loop':'365 565 425 540','pickup':'380 620 400 440','wrap':'230 495 690 730','rear':'170 490 800 760','interlock':'285 550 570 620','takeup':'90 70 920 1100','tighten':'330 500 490 650','cycle':'80 0 970 1250','result':'40 0 1040 1250'}
    if view in ['seam','feed','reset']:
        return special(s)
    box=boxes[view]
    return f'''<svg id="{sid}-diagram" class="diagram" viewBox="{box}" xmlns="http://www.w3.org/2000/svg" aria-label="Schematic rotary hook lockstitch mechanism" data-layout-allow-overflow="true">
<defs>
<linearGradient id="{sid}-steel"><stop stop-color="#748A9B"/><stop offset=".28" stop-color="#D5E0E5"/><stop offset=".6" stop-color="#A6B4BE"/><stop offset="1" stop-color="#617A8C"/></linearGradient>
<linearGradient id="{sid}-case" x2=".85" y2="1"><stop stop-color="#DCE4E7"/><stop offset=".5" stop-color="#A6B4BE"/><stop offset="1" stop-color="#71899A"/></linearGradient>
<linearGradient id="{sid}-housing" x2=".8" y2="1"><stop stop-color="#F8F9F5"/><stop offset=".7" stop-color="#CDD4D4"/><stop offset="1" stop-color="#9EB0B5"/></linearGradient>
<pattern id="{sid}-weave" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M0 0H16M0 0V16" stroke="#536775" stroke-width="1" opacity=".2"/></pattern>
</defs>
<ellipse cx="580" cy="1185" rx="390" ry="28" fill="#172B3B" opacity=".09"/>
<g id="{sid}-shell">
 <path d="M435 95H905Q975 95 975 165V1090H160V1035H815V380H655V510H430V180Q430 100 435 95Z" transform="translate(23 18)" fill="#9EAFB7" stroke="#536775" stroke-width="4"/>
 <path d="M435 95H905Q975 95 975 165V1090H160V1035H815V380H655V510H430V180Q430 100 435 95Z" fill="url(#{sid}-housing)" stroke="#536775" stroke-width="4"/>
 <path d="M790 135V335M470 140H755" stroke="#F8F9F5" stroke-width="10" opacity=".65"/>
 <circle cx="929" cy="252" r="50" fill="url(#{sid}-steel)" stroke="#536775" stroke-width="5"/>
 <circle cx="929" cy="252" r="25" fill="#CDD4D4" stroke="#536775" stroke-width="3"/>
</g>
<g id="{sid}-spool"><path d="M695 54V155" stroke="#536775" stroke-width="10"/><rect x="656" y="68" width="82" height="76" rx="8" fill="#C94422"/><path d="M650 66H744M650 146H744" stroke="#617A8C" stroke-width="10" stroke-linecap="round"/>
<path d="M660 80H734M660 94H734M660 108H734M660 122H734M660 136H734" stroke="#F8D4BE" stroke-width="3" opacity=".65"/></g>
<g id="{sid}-takeup"><path id="{sid}-lever" d="M400 225L310 290" stroke="url(#{sid}-steel)" stroke-width="25" stroke-linecap="round"/><circle cx="400" cy="225" r="19" fill="#A6B4BE" stroke="#536775" stroke-width="4"/><circle id="{sid}-lever-eye" cx="310" cy="290" r="13" fill="#F8F9F5" stroke="#536775" stroke-width="4"/></g>
<circle cx="330" cy="410" r="36" fill="url(#{sid}-steel)" stroke="#536775" stroke-width="4"/>
<path id="{sid}-upper-route" fill="none" stroke="#C94422" stroke-width="6" stroke-linecap="round"/>
<g id="{sid}-fabric">
 <path d="M160 608L835 608L898 573H223Z" fill="#D4DCCF" stroke="#829689" stroke-width="3"/>
 <path d="M160 608H835V639H160Z" fill="#D2DCCB" stroke="#829689" stroke-width="3"/>
 <path d="M160 641H835V673H160Z" fill="#B4C7B3" stroke="#829689" stroke-width="3"/>
 <rect x="160" y="608" width="675" height="65" fill="url(#{sid}-weave)"/>
 <path d="M215 605H476" stroke="#C94422" stroke-width="5" stroke-dasharray="30 21"/>
 <path d="M215 675H476" stroke="#167580" stroke-width="5"/>
</g>
<g id="{sid}-plate"><path d="M180 689H848L904 657H840L825 681H180Z" fill="#C3CFD6" stroke="#536775" stroke-width="3"/><path d="M180 690H848V708H180Z" fill="url(#{sid}-steel)" stroke="#536775" stroke-width="3"/></g>
<g id="{sid}-foot"><path d="M615 378V563L585 593H485V607H616L655 569V378Z" fill="url(#{sid}-steel)" stroke="#536775" stroke-width="4"/><path d="M526 590V609" stroke="#F8F9F5" stroke-width="14"/></g>
<g id="{sid}-dog"><path d="M342 704V683L354 674L366 683L378 674L390 683L402 674L414 683L426 674L438 683V704Z" fill="#71899A" stroke="#536775" stroke-width="3"/><path d="M640 704V683L652 674L664 683L676 674L688 683L700 674L712 683L724 674L736 683V704Z" fill="#71899A" stroke="#536775" stroke-width="3"/></g>
<path id="{sid}-back-thread" fill="none" stroke="#C94422" stroke-width="6" stroke-dasharray="13 9" stroke-linecap="round"/>
<g id="{sid}-hook-rotor"><circle cx="570" cy="915" r="186" fill="none" stroke="#536775" stroke-width="20"/><path d="M570 730A185 185 0 1 1 407 1002" fill="none" stroke="#2459C4" stroke-width="12"/>
<path d="M598 730L620 746L612 778L595 758L578 751Z" fill="#2459C4" stroke="#172B3B" stroke-width="3"/>
<path d="M570 1099L610 1087" stroke="#D5E0E5" stroke-width="8" stroke-linecap="round"/></g>
<g id="{sid}-case-unit"><ellipse cx="581" cy="928" rx="146" ry="145" fill="#617A8C"/>
<circle cx="570" cy="915" r="144" fill="url(#{sid}-case)" stroke="#536775" stroke-width="4"/>
<path d="M474 811Q527 765 587 778L636 800L612 844L552 833Z" fill="#7F96A3" stroke="#536775" stroke-width="3"/>
<circle cx="570" cy="915" r="93" fill="#8BABB0" stroke="#536775" stroke-width="4"/>
<circle cx="570" cy="915" r="74" fill="#167580" opacity=".42"/>
<path d="M502 892H638M500 909H640M502 926H638M512 943H628" stroke="#B9DCDD" stroke-width="5"/>
<path d="M457 884H665V944H457Z" fill="url(#{sid}-steel)" stroke="#536775" stroke-width="4"/>
<rect x="534" y="890" width="52" height="46" rx="6" fill="#617A8C" stroke="#172B3B" stroke-width="3"/>
<circle cx="560" cy="913" r="9" fill="#DCE4E7"/>
<path d="M667 875L701 865L710 885L678 907Z" fill="url(#{sid}-steel)" stroke="#536775" stroke-width="3"/>
</g>
<path id="{sid}-lower-thread" fill="none" stroke="#167580" stroke-width="7" stroke-linecap="round"/>
<path id="{sid}-front-thread" fill="none" stroke="#C94422" stroke-width="7" stroke-linecap="round"/>
<g id="{sid}-needle"><path d="M528 320H551V454L545 563L538 581L532 563Z" fill="url(#{sid}-steel)" stroke="#536775" stroke-width="3"/><rect x="535" y="529" width="8" height="26" rx="4" fill="#ECEEE9" stroke="#536775" stroke-width="2"/><path d="M549 505L547 535" stroke="#536775" stroke-width="3"/>
<rect x="513" y="295" width="53" height="60" rx="8" fill="#71899A" stroke="#536775" stroke-width="4"/>
</g>
<g id="{sid}-annotations" fill="#172B3B" font-family="Manrope" font-size="32" font-weight="600"></g>
</svg>'''

def special(s):
    sid=s['id'];seam=s['view']=='seam'
    if seam:
        return f'''<svg class="diagram" viewBox="0 0 1000 1100" xmlns="http://www.w3.org/2000/svg" aria-label="Section of interlaced upper and lower threads inside fabric">
<defs><pattern id="{sid}-hatch" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M0 24L24 0" stroke="#829689" stroke-width="2" opacity=".35"/></pattern></defs>
<path d="M100 360L800 360L895 300H195Z" fill="#D9E2D4" stroke="#829689" stroke-width="4"/><rect x="100" y="360" width="700" height="180" fill="#D2DCCB" stroke="#829689" stroke-width="4"/><rect x="100" y="540" width="700" height="180" fill="#B4C7B3" stroke="#829689" stroke-width="4"/><rect x="100" y="360" width="700" height="360" fill="url(#{sid}-hatch)"/>
<path d="M130 723H360C400 723 422 670 438 600C456 521 475 501 500 533C525 567 548 723 600 723H770" fill="none" stroke="#167580" stroke-width="13"/>
<path id="{sid}-seam-upper" d="M130 354H360C418 354 423 452 443 527C461 592 482 590 500 553C527 495 534 354 600 354H770" fill="none" stroke="#C94422" stroke-width="13"/>
<path d="M482 565L475 549" stroke="#167580" stroke-width="15"/>
<circle cx="475" cy="550" r="65" fill="none" stroke="#2459C4" stroke-width="3"/>
<path d="M540 550H820V829" fill="none" stroke="#536775" stroke-width="3"/><circle cx="540" cy="550" r="5" fill="#2459C4"/>
<text x="140" y="220" fill="#C94422" font-family="Manrope" font-weight="700" font-size="42">Benang atas</text><text x="140" y="895" fill="#167580" font-family="Manrope" font-weight="700" font-size="42">Benang bawah</text>
<text x="555" y="875" fill="#172B3B" font-family="Manrope" font-size="34">Saling mengait</text>
</svg>'''
    return f'''<svg class="diagram" viewBox="0 0 1000 1100" xmlns="http://www.w3.org/2000/svg" aria-label="Bottom-feed side section with needle clear of fabric">
<defs><linearGradient id="{sid}-metal"><stop stop-color="#71899A"/><stop offset=".4" stop-color="#D5E0E5"/><stop offset="1" stop-color="#A6B4BE"/></linearGradient></defs>
<g id="{sid}-side-needle"><path d="M480 90H500V279L490 310L480 279Z" fill="url(#{sid}-metal)" stroke="#536775" stroke-width="4"/><rect x="487" y="263" width="6" height="20" rx="3" fill="#ECEEE9"/><path d="M488 110V270L460 440" fill="none" stroke="#C94422" stroke-width="6"/></g>
<path d="M650 160V390L590 425H370V442H630L690 405V160Z" fill="url(#{sid}-metal)" stroke="#536775" stroke-width="5"/>
<g id="{sid}-side-fabric"><path d="M100 450H900V483H100Z" fill="#D2DCCB" stroke="#829689" stroke-width="3"/><path d="M100 485H900V519H100Z" fill="#B4C7B3" stroke="#829689" stroke-width="3"/>
<path d="M125 445H880" stroke="#C94422" stroke-width="6" stroke-dasharray="32 24"/>
<path d="M125 523H880" stroke="#167580" stroke-width="6"/>
</g>
<path d="M100 537H365M635 537H900" stroke="#536775" stroke-width="22"/>
<g id="{sid}-side-dog"><path d="M358 578V531L378 512L398 531L418 512L438 531L458 512L478 531L498 512L518 531L538 512L558 531L578 512L598 531L618 512L638 531V578Z" fill="url(#{sid}-metal)" stroke="#536775" stroke-width="4"/><rect x="471" y="578" width="56" height="175" rx="10" fill="#A6B4BE" stroke="#536775" stroke-width="4"/></g>
<path d="M570 800H390Q340 800 340 745V690Q340 655 390 655H610Q660 655 660 700V747Q660 800 610 800" fill="none" stroke="#536775" stroke-dasharray="12 9" stroke-width="4"/>
<path d="M425 800H383L400 783M645 700V743L628 726" fill="none" stroke="#2459C4" stroke-width="6"/>
<text x="135" y="910" font-family="Manrope" font-size="38" font-weight="700" fill="#172B3B">Naik · geser · turun · kembali</text>
</svg>'''

def make_scene(s):
    sid=s['id'];view=s['view'];dur=s['duration']
    note={'whole':'Penampang ilustratif · gerak diperlambat','reveal':'Cangkang depan dibuka untuk memperlihatkan mekanisme','anatomy':'Letak bagian dipertahankan · ukuran tidak berskala','needle':'Mata jarum diperbesar untuk memperjelas jalur benang','loop':'Awal langkah naik · loop terbentuk di sisi jarum','pickup':'Detail lambat · ujung kait masuk ke dalam loop','wrap':'Kait luar berputar · rumah bobin tetap','rear':'Pemisahan kedalaman ilustratif · garis putus di sisi belakang','interlock':'Loop atas melingkupi jalur benang bawah','takeup':'Tuas naik → kelonggaran benang berkurang','tighten':'Loop mengecil · titik kaitan ditarik ke kain','seam':'Penampang skematis · dua warna untuk membedakan benang','feed':'Jarum sudah di atas kain saat kain digeser','reset':'Gigi kembali di bawah pelat · kain berhenti','cycle':'Satu siklus utuh · gerak diperlambat','result':'Lockstitch dua benang · hook putar penuh'}[view]
    code=f"const tl=gsap.timeline({{paused:true}});\n"
    if view in ['feed','reset']:
        # Explicit rigid DOM transforms keep the dog motion and fabric dependency observable.
        if animated:
            if view=='feed':
                code+=f"tl.fromTo('#{sid}-side-dog',{{x:0,y:35}},{{x:0,y:-4,duration:.6,ease:'sine.inOut'}},.55).to('#{sid}-side-dog',{{x:-90,y:-4,duration:{dur*.32},ease:'none'}},1.15);\n"
                code+=f"tl.fromTo('#{sid}-side-fabric',{{x:0}},{{x:-90,duration:{dur*.32},ease:'none'}},1.15);\n"
            else:
                code+=f"tl.fromTo('#{sid}-side-fabric',{{x:-90}},{{x:-90,duration:{dur-.1}}},0);tl.fromTo('#{sid}-side-dog',{{x:-90,y:-4}},{{x:-90,y:50,duration:.65,ease:'sine.inOut'}},.3).to('#{sid}-side-dog',{{x:0,y:50,duration:{dur*.28},ease:'none'}},1);tl.fromTo('#{sid}-side-needle',{{y:0}},{{y:250,duration:{dur*.35},ease:'sine.inOut'}},{dur*.58});\n"
        else:
            code+=f"gsap.set('#{sid}-side-dog',{{x:-50,y:{-4 if view=='feed' else 50}}});gsap.set('#{sid}-side-fabric',{{x:-50}});"
    elif view=='seam':
        if animated:code+=f"tl.fromTo('#{sid}-seam-upper',{{strokeWidth:9}},{{strokeWidth:13,duration:.5}},.4);"
    else:
        p=(s['p0']+s['p1'])/2 if not animated else s['p0']
        shell=1 if view in ['whole','result'] else .055
        # Whole/result sections keep the lower shell removed; top shell remains recognisable.
        code+=f"const st={{p:{p},shell:{shell},depth:{1 if view=='rear' else 0}}};\n"
        code+=r'''
const el=n=>document.getElementById('SID-'+n);
const lerp=(a,b,q)=>a+(b-a)*q;
const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
const keys=[
 [0,0,0,-28], [.24,220,0,-28], [.32,200,1,0], [.38,175,1,45],
 [.50,90,1,155], [.62,0,1,245], [.74,0,1,330], [.87,0,.48,350], [.96,0,0,360], [1,0,0,360], [1.24,220,0,370]
];
const sample=p=>{let i=0;while(i<keys.length-2&&p>keys[i+1][0])i++;let a=keys[i],b=keys[i+1],q=clamp((p-a[0])/(b[0]-a[0]),0,1);return [lerp(a[1],b[1],q),lerp(a[2],b[2],q),lerp(a[3],b[3],q)]};
const poses=[
 [.24,[540,740,552,752,558,746,560,735,558,725,550,714,540,705]],
 [.32,[540,740,554,778,598,790,616,754,617,729,583,716,540,705]],
 [.38,[540,715,618,751,701,807,731,861,747,890,706,879,540,690]],
 [.50,[540,630,690,704,803,973,625,1108,494,1168,404,1000,540,675]],
 [.62,[540,542,466,709,321,991,451,1080,590,1190,801,893,540,672]],
 [.74,[540,542,434,691,372,754,454,760,558,776,666,745,540,672]],
 [.87,[540,542,512,658,508,716,538,723,568,724,574,672,540,650]],
 [.96,[540,542,536,613,531,652,540,656,549,653,546,635,540,625]],
 [1.24,[540,740,542,740,544,730,544,720,544,710,542,700,540,674]]
];
const shape=p=>{if(p<.24)return [540,542+sample(p)[0],540,674,540,674,540,674,540,674,540,674,540,674];let i=0;while(i<poses.length-2&&p>poses[i+1][0])i++;let a=poses[i],b=poses[i+1],q=clamp((p-a[0])/(b[0]-a[0]),0,1);return a[1].map((v,j)=>lerp(v,b[1][j],q))};
const draw=()=>{
 const p=st.p,[dy,loop,ang]=sample(p),eye=542+dy;
 el('needle').setAttribute('transform',`translate(0 ${dy})`);
 el('shell').setAttribute('opacity',st.shell);
 el('hook-rotor').setAttribute('transform',`rotate(${ang} 570 915)`);
 el('case-unit').setAttribute('transform',`translate(${st.depth*70} ${st.depth*25})`);
 const leverY=p<.74?lerp(230,330,clamp(p/.7,0,1)):lerp(330,195,clamp((p-.74)/.22,0,1));
 el('lever').setAttribute('d',`M400 225L310 ${leverY}`);el('lever-eye').setAttribute('cy',leverY);
 el('upper-route').setAttribute('d',`M698 110L310 ${leverY}L330 410L540 465L540 ${eye}`);
 let v=shape(p);v[1]=eye;
 if(p>=.32&&p<.70){const a=ang*Math.PI/180;v[6]=570+42*Math.cos(a)+137*Math.sin(a);v[7]=915+42*Math.sin(a)-137*Math.cos(a);}
 el('front-thread').setAttribute('d',`M${v[0]} ${v[1]}C${v[2]} ${v[3]} ${v[4]} ${v[5]} ${v[6]} ${v[7]}C${v[8]} ${v[9]} ${v[10]} ${v[11]} ${v[12]} ${v[13]}`);
 el('back-thread').setAttribute('d',`M540 674C${lerp(540,385,loop)} ${lerp(680,826,loop)} ${lerp(540,520,loop)} ${lerp(690,1125,loop)} ${v[6]} ${v[7]}`);
 el('back-thread').setAttribute('opacity',p>.33&&p<.9?1:0);
 const lowY=p<.76?775:lerp(775,649,clamp((p-.76)/.2,0,1));
 el('lower-thread').setAttribute('d',`M${570+st.depth*70} ${880+st.depth*25}Q660 802 582 ${lowY}Q553 ${lowY-15} 540 674L215 675`);
 const feed=clamp((p-.96)/.04,0,1)*42;
 el('fabric').setAttribute('transform',`translate(${-feed} 0)`);
 el('dog').setAttribute('transform',`translate(${-feed} ${p>.96?-8:22})`);
};
draw();
'''.replace('SID',sid)
        if animated:
            if view=='whole':
                code+=f"tl.fromTo(st,{{p:0}},{{p:1,duration:{max(dur-1,2)},ease:'none',onUpdate:draw}},.5);\n"
            elif view=='reveal':
                code+=f"tl.fromTo(st,{{shell:1}},{{shell:.055,duration:1.7,ease:'power2.inOut',onUpdate:draw}},.6);\n"
            elif view=='result':
                code+=f"tl.fromTo(st,{{shell:.055}},{{shell:1,duration:1.4,onUpdate:draw}},.3);\n"
            elif view=='anatomy':
                code+=f"tl.fromTo('#{sid}-label-0',{{opacity:0}},{{opacity:1,duration:.4}},.35);tl.fromTo('#{sid}-spool',{{opacity:.4}},{{opacity:1,duration:.6}},.4);tl.fromTo('#{sid}-label-1',{{opacity:0}},{{opacity:1,duration:.4}},2.4);tl.fromTo('#{sid}-case-unit',{{opacity:.4}},{{opacity:1,duration:.6}},2.4);\n"
            else:
                code+=f"tl.fromTo(st,{{p:{s['p0']}}},{{p:{s['p1']},duration:{max(dur-1.1,1)},ease:'none',onUpdate:draw}},.5);\n"
                if view=='rear':code+=f"tl.fromTo(st,{{depth:0}},{{depth:1,duration:1,ease:'power2.inOut',onUpdate:draw}},.15);\n"
        # Functional local annotations; no decorative permanent HUD.
        labels=[]
        if view=='anatomy':labels=[(130,120,'Benang atas',730,110),(115,1040,'Bobin',560,965)]
        if view=='takeup':labels=[(125,132,'Tuas penarik',315,245)]
        if labels:
            markup=''.join(f'<g id="{sid}-label-{i}"><path d="M{x+20} {y+20}L{tx} {ty}" fill="none" stroke="#536775" stroke-width="2"/><circle cx="{tx}" cy="{ty}" r="5" fill="#2459C4"/><text x="{x}" y="{y}" fill="#172B3B" font-family="Manrope" font-size="38" font-weight="600">{text}</text></g>' for i,(x,y,text,tx,ty) in enumerate(labels))
            # SVG is authored in markup; annotations are frozen original geometry.
        else:markup=''
    if view in ['seam','feed','reset']:markup=''
    svg=diagram(s).replace(f'<g id="{sid}-annotations" fill="#172B3B" font-family="Manrope" font-size="32" font-weight="600"></g>',f'<g id="{sid}-annotations">{markup}</g>')
    if animated:
        code+=f"tl.fromTo('#{sid}-subtitle',{{opacity:0}},{{opacity:1,duration:.25}},.15);"
    code+=f"tl.to({{}},{{duration:.01}},{max(0,dur-.02)});window.__timelines=window.__timelines||{{}};window.__timelines['{sid}']=tl;"
    return f'''<template><style>
@font-face{{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:100 900}}
#root{{position:absolute;inset:0;overflow:hidden;color:#172B3B;font-family:Manrope}}
.ground{{position:absolute;inset:0;background:#ECEEE9}}
.bench{{position:absolute;left:54px;top:430px;width:972px;height:1038px;background:#F8F9F5;border-radius:38px}}
.title{{position:absolute;left:108px;top:164px;width:850px;font:800 74px/1.1 Manrope;letter-spacing:-3px;margin:0}}
.subtitle{{position:absolute;left:108px;top:345px;width:850px;font:500 36px/1.3 Manrope}}
.diagram{{position:absolute;left:70px;top:445px;width:940px;height:990px;overflow:hidden}}
.note{{position:absolute;left:108px;top:1484px;width:850px;font:500 30px/1.35 Manrope;color:#536775}}
</style><div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{dur}">
<div id="{sid}-ground" class="clip ground" data-start="0" data-duration="{dur}" data-track-index="0"></div>
<div class="bench"></div><h1 id="{sid}-title" class="title">{html.escape(s['title'])}</h1>
<div id="{sid}-subtitle" class="subtitle">{html.escape(s['subtitle'])}</div>{svg}
<div id="{sid}-note" class="note" {'data-hold="true"' if view=='result' else ''}>{html.escape(note)}</div>
</div><script>{code}</script></template>'''

for s in plan['scenes']:(V/f"compositions/{s['id']}.html").write_text(make_scene(s),encoding='utf-8')
hosts='\n'.join(f'''<div id="{s['id']}" class="clip" data-composition-id="{s['id']}" data-composition-src="compositions/{s['id']}.html" data-start="{s['start']}" data-duration="{s['duration']}" data-width="1080" data-height="1920" data-track-index="0" data-track-kind="graphics"></div>''' for s in plan['scenes'])
aud='';cap=''
if audio:
    meta=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'));voice=meta['voices'][0]
    src='assets/audio/narration-master.wav' if (V/'assets/audio/narration-master.wav').exists() else voice['path']
    placed_duration=meta.get('placed_narration',{}).get('duration_s',voice['duration_s'])
    aud=f'''<audio id="narration" class="clip" data-start="0.35" data-duration="{placed_duration}" data-track-index="2" data-volume="0.8" src="{src}"></audio>'''
    groups=plan['captions']
    els='\n'.join(f'''<div id="caption-{i:03}" class="clip caption" data-start="{c['start']:.3f}" data-duration="{c['end']-c['start']:.3f}" data-track-index="0"><span>{html.escape(c['text'])}</span></div>''' for i,c in enumerate(groups))
    cs="@font-face{font-family:Manrope;src:url('assets/fonts/manrope.ttf');font-weight:100 900}#root{position:absolute;inset:0;pointer-events:none}.caption{position:absolute;left:118px!important;top:1590px!important;width:844px!important;height:180px!important;display:flex;align-items:center;justify-content:center;text-align:center;font:600 46px/1.38 Manrope;color:#172B3B;padding:15px;box-sizing:border-box}.caption span{background:#F8F9F5;padding:14px 22px;border-radius:14px;max-width:100%;box-sizing:border-box}"
    (V/'compositions/captions.html').write_text(f'''<template><style>{cs}</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="90">{els}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines['captions']=gsap.timeline({{paused:true}});</script></template>''',encoding='utf-8')
    cap='<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="90" data-width="1080" data-height="1920" data-track-index="1" data-track-kind="captions" style="z-index:20;pointer-events:none"></div>'
(V/'index.html').write_text(f'''<!doctype html><html lang="id" data-resolution="portrait"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>*{{box-sizing:border-box;margin:0}}html,body{{width:1080px;height:1920px;overflow:hidden;background:#ECEEE9}}#root{{position:relative;width:1080px;height:1920px}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="90" data-width="1080" data-height="1920">{hosts}{aud}{cap}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines['main']=gsap.timeline({{paused:true}});</script></body></html>''',encoding='utf-8')
print(json.dumps({'animated':animated,'audio':audio,'scenes':len(plan['scenes'])}))
