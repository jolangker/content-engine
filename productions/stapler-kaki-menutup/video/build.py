"""Author static poses first, then the same editable scenes with seekable motion."""
from pathlib import Path
import json,html,sys,hashlib
V=Path(__file__).resolve().parent
plan=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'))
animated='--animate' in sys.argv
if animated and (V/'timing.json').exists():plan=json.loads((V/'timing.json').read_text(encoding='utf-8'))
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def e(s):return html.escape(str(s))
COL={'ink':'#172B3B','blue':'#2459C4','orange':'#C94422','teal':'#167580'}
CSS='''@font-face{font-family:Manrope;src:url('assets/fonts/manrope.ttf')}@font-face{font-family:PlexLocal;src:url('assets/fonts/ibm-plex-mono.ttf')}
*{box-sizing:border-box}#root{position:absolute;inset:0;color:#172B3B;font-family:Manrope;background:#ECEEE9;overflow:hidden}.scene{position:absolute;inset:0}.kicker{position:absolute;left:110px;top:198px;font:30px PlexLocal;color:#536775}.title{position:absolute;left:108px;top:270px;width:848px;margin:0;font-size:78px;line-height:1.1;font-weight:800;letter-spacing:-3px}.stage{position:absolute;left:48px;top:500px;width:984px;height:850px}.note{position:absolute;left:110px;top:1380px;width:820px;font:28px PlexLocal;color:#536775;line-height:1.45}svg{width:100%;height:100%;overflow:visible}svg text{font-family:Manrope;font-size:35px;font-weight:700;fill:#172B3B}.label{font-size:33px}.tiny{font:30px PlexLocal;fill:#536775}.leader{fill:none;stroke:#536775;stroke-width:2.2}.outline{stroke:#172B3B;stroke-width:3;stroke-linejoin:round}.wire{fill:none;stroke:#2459C4;stroke-width:13;stroke-linejoin:round;stroke-linecap:round}'''
def defs(i):return f'''<defs>
<linearGradient id="{i}-metal" x1="0" y1="0" x2="0.4" y2="1"><stop stop-color="#EDF3F4"/><stop offset=".4" stop-color="#B7C5CE"/><stop offset="1" stop-color="#7A919F"/></linearGradient>
<linearGradient id="{i}-poly" x1="0" y1="0" x2=".2" y2="1"><stop stop-color="#5B7C92"/><stop offset="1" stop-color="#172B3B"/></linearGradient>
<linearGradient id="{i}-blue" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#77A2EA"/><stop offset="1" stop-color="#2459C4"/></linearGradient>
<marker id="{i}-arrow" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0 0L7 3L0 6Z" fill="#C94422"/></marker></defs>'''
def label(x,y,tx,ty,text):return f'<path class="leader" d="M{x} {y+9}L{x} {y+32}L{tx} {ty}"/><circle cx="{tx}" cy="{ty}" r="4" fill="#536775"/><text class="label" x="{x}" y="{y}">{text}</text>'
def side(i,whole=False,exploded=False):
    strip=''.join(f'<path d="M{x} 478l34 -12v30l-34 12Z" fill="url(#{i}-metal)" class="outline"/>' for x in range(455,790,38))
    return f'''<ellipse cx="510" cy="723" rx="390" ry="25" fill="#172B3B" opacity=".09"/>
<g id="{i}-base"><path d="M90 661L835 661L888 633L152 633Z" fill="#BAC8CC" class="outline"/><path d="M90 661H835V701H90Z" fill="url(#{i}-poly)" class="outline"/><path d="M835 661l53 -28v40l-53 28Z" fill="#324F63" class="outline"/>
<path d="M135 640V464q0 -45 42 -45h27v221Z" fill="url(#{i}-metal)" class="outline"/>
<path d="M738 638h96v-17h-96Z" fill="#667E8D" class="outline"/><path d="M738 621l40 -23h96l-40 23Z" fill="url(#{i}-metal)" class="outline"/><path d="M764 612q11 16 25 0M800 610q11 16 25 0" fill="none" stroke="#172B3B" stroke-width="5"/>
</g>
<g id="{i}-paper"><path d="M520 599H879L933 571H575Z" fill="#F8F9F5" class="outline"/><path d="M520 599H879V618H520Z" fill="#D8DEDC" class="outline"/><path d="M528 605H875M528 612H875" stroke="#A6B4BE" stroke-width="2"/></g>
<g id="{i}-magazine"><path d="M171 497H836V531H171Z" fill="url(#{i}-metal)" class="outline"/><path d="M171 497L220 469H884L836 497Z" fill="#D8E1E4" class="outline"/>{strip}
<path d="M825 489V555H848V477" fill="#172B3B"/><path d="M829 494V546" stroke="#F8F9F5" stroke-width="5"/>
<g id="{i}-follower"><path d="M391 476l31 -14v42l-31 14Z" fill="#C94422" class="outline"/><path d="M240 490l12 -12l12 12l12 -12l12 12l12 -12l12 12l12 -12l12 12l12 -12l12 12l12 -12l12 12" stroke="#536775" stroke-width="5" fill="none"/></g></g>
<g id="{i}-cover"><path d="M157 426Q350 312 813 342L860 377L164 463Z" fill="url(#{i}-poly)" class="outline"/><path d="M157 426Q350 312 813 342L848 322Q355 283 190 401Z" fill="#66869B" class="outline"/><path d="M164 463l696 -86v33l-689 81Z" fill="#172B3B" opacity=".94"/>
<path d="M250 405Q540 341 785 365" stroke="#A6B4BE" stroke-width="4" opacity=".5" fill="none"/></g>
<g id="{i}-blade"><path d="M792 414H820V514H792Z" fill="url(#{i}-blue)" class="outline"/><path d="M820 414l18 -10v100l-18 10Z" fill="#193E83" class="outline"/></g>
<g id="{i}-wire"><path d="M797 518h22v47" stroke="#2459C4" stroke-width="9" fill="none"/></g>
<circle cx="172" cy="455" r="24" fill="url(#{i}-metal)" class="outline"/><circle cx="172" cy="455" r="8" fill="#536775"/>
<g id="{i}-force"><path d="M690 200v110" stroke="#C94422" stroke-width="10" marker-end="url(#{i}-arrow)"/><text x="572" y="176" fill="#C94422">tekan</text></g>
<g id="{i}-return"><path d="M310 464q60 -85 115 -5" stroke="#167580" stroke-width="7" fill="none" marker-end="url(#{i}-arrow)"/></g>'''
def feed(i):
    wires=''.join(f'<g id="{i}-staple-{n}"><path d="M{x} 570V420l55 -30v150" fill="none" stroke="{COL["blue"] if n==0 else "#8599A6"}" stroke-width="12"/><path d="M{x+2} 565V421l53 -29" stroke="#DCE7EA" stroke-width="3" fill="none"/></g>' for n,x in enumerate([750,705,660,615,570,525]))
    return f'''<ellipse cx="520" cy="680" rx="400" ry="24" opacity=".09" fill="#172B3B"/>
<path d="M150 400L220 360H905L835 400Z" fill="#D3DDE1" class="outline"/><path d="M150 400h685v235H150Z" fill="url(#{i}-metal)" class="outline"/><path d="M835 400l70 -40v235l-70 40Z" fill="#77909E" class="outline"/>
<path d="M170 420h655v175H170Z" fill="#F8F9F5" stroke="#172B3B" stroke-width="3"/>
<g id="{i}-row">{wires}</g><g id="{i}-follower"><path d="M435 427l60 -30h40v180l-60 30h-40Z" fill="#C94422" class="outline"/><path d="M435 427h40v180h-40Z" fill="#A42C13"/>
<path d="M210 520l20 -28l20 28l20 -28l20 28l20 -28l20 28l20 -28l20 28l20 -28l20 28l20 -28" stroke="#536775" stroke-width="7" fill="none"/></g>
<g id="{i}-gate"><path d="M818 305h28v280h-28Z" fill="url(#{i}-blue)" class="outline"/><path d="M846 305l35 -20v280l-35 20Z" fill="#193E83" class="outline"/></g>
<g id="{i}-force"><path d="M270 690h200" stroke="#C94422" stroke-width="8" marker-end="url(#{i}-arrow)"/><text x="190" y="750">gaya pegas ke depan</text></g>
{label(180,250,470,427,'pengumpan')}{label(650,220,830,305,'jalur bilah')}
<text class="tiny" x="170" y="335">magazen · sisi atas dibuka</text>'''
def front(i,result=False):
    return f'''<ellipse cx="505" cy="704" rx="340" ry="25" fill="#172B3B" opacity=".09"/>
<g id="{i}-anvil"><path d="M200 490H800V618H200Z" fill="url(#{i}-metal)" class="outline"/><path d="M800 490l30 -24v128l-30 24Z" fill="#657F8E" class="outline"/><path d="M200 490l30 -24h600l-30 24Z" fill="#CFDADF" class="outline"/>
<path d="M339 486V493Q339 531 381 531H465V509H381Q362 509 362 486Z" fill="#ECEEE9"/><path d="M661 486V493Q661 531 619 531H535V509H619Q638 509 638 486Z" fill="#ECEEE9"/>
<path d="M339 490Q339 531 381 531H465M661 490Q661 531 619 531H535" fill="none" stroke="#536775" stroke-width="4"/></g>
<g id="{i}-paper"><path d="M178 430H822V475H178Z" fill="#F8F9F5" class="outline"/><path d="M178 430l30 -24h644l-30 24Z" fill="#FFF" class="outline"/><path d="M822 430l30 -24v45l-30 24Z" fill="#D5DDDC" class="outline"/>
<path d="M182 444H818M182 458H818" stroke="#BBC7CA" stroke-width="2"/></g>
<g id="{i}-blade"><path d="M332 106H668V215H332Z" fill="url(#{i}-blue)" class="outline"/><path d="M332 106l25 -18h336l-25 18Z" fill="#739CDE" class="outline"/><path d="M668 106l25 -18v109l-25 18Z" fill="#193E83" class="outline"/></g>
<path id="{i}-staple-shadow" d="M350 410V220H650V410" fill="none" stroke="#172B3B" stroke-width="19" opacity=".2" transform="translate(5 3)"/>
<path id="{i}-staple" d="M350 410V220H650V410" class="wire"/>
<g id="{i}-force"><path d="M500 20v55" stroke="#C94422" stroke-width="8" marker-end="url(#{i}-arrow)"/></g>
<g id="{i}-labels">{label(170,310,280,440,'kertas')}{label(620,710,732,560,'landasan diam')}</g>
<g id="{i}-bendhint"><path d="M315 560q15 47 97 47M685 560q-15 47 -97 47" fill="none" stroke="#167580" stroke-width="6"/><text x="350" y="665" fill="#167580">alur → tekukan</text></g>'''

# Functional state at storyboard pose; scene states continue across corresponding cuts.
poses=[{'press':.22},{'press':0},{'explode':1},{'feed':1},{'drop':.35},{'press':.42},{'press':.7},{'press':.35},{'press':.6},{'press':1},{'press':1},{'press':1},{'press':0},{'feed':1},{'press':1},{'press':1}]
# p: cover and magazine compression; front p maps to continuous wire forming.
transitions=[
[(.6,1.2,{'press':.65}),(3.2,.9,{'press':0})],[],[(.5,1.3,{'explode':1})],[(1.1,1.3,{'feed':1})],[(1.3,1.1,{'drop':.65})],[(1,1.4,{'press':.42})],[(.8,1.4,{'press':.7})],[(.7,2.3,{'press':.35})],[(1.1,2,{'press':.6})],[(.7,4,{'press':1})],[(.6,2.6,{'press':1})],[(.5,.8,{'lift':1})],[(.8,1.5,{'press':0})],[(1.1,1.4,{'feed':1,'gate':0})],[(.4,1.3,{'press':1}),(3.5,1.2,{'press':0}),(5.1,.8,{'feed':1})],[(.5,1,{'lift':1})]]
initial=[{}, {},{}, {},{}, {},{'press':.42},{'press':0},{'press':.35},{'press':.6},{'press':.6},{'press':1},{'press':1},{'gate':1},{},{'press':1}]
notes={'whole':'Ilustrasi skematis · bukan skala asli','explode':'Cangkang diangkat untuk inspeksi','feed':'Pembesaran jalur · jarak diperlebar','side':'Penampang samping · gerak diperlambat','front':'Penampang depan · kawat diperbesar','clinch':'Penampang depan · alur diperjelas','result':'Tekukan ke dalam · skema diperbesar','cycle':'Ulangan satu siklus · diperlambat'}
events=[]
for n,s in enumerate(plan):
    i=s['id'];kind=s['view'];d=s['duration'];isfront=kind in ['front','clinch','result']
    art=front(i) if isfront else feed(i) if kind=='feed' else side(i,kind=='whole',kind=='explode')
    kindlabels={'whole':'stapler manual','explode':'bagian tersembunyi','side':'jalur gaya','front':'kaki menembus','clinch':'kontak & pembentukan','result':'hasil tekukan','feed':'pengumpanan','cycle':'siklus utuh'}
    # All custom state uses timeline-local numeric properties, never wall time.
    state={'press':0,'feed':0,'drop':0,'explode':0,'lift':0,'gate':0,**(initial[n] if animated else poses[n])}
    anim=[]
    for at,dur,props in transitions[n] if animated else []:
        scale=s.get('motion_scale',1)
        anim.append(f'tl.to(st,{{...{json.dumps(props)},duration:{dur*scale:.6f},ease:"power2.inOut"}},{at*scale:.6f});')
    if not anim:anim=['tl.to(clock,{v:1,duration:'+str(d-.03)+',ease:"none"},0);']
    # For metal strain the centerline length is preserved: straight + radius*angle + horizontal.
    wirepos='55' if n==12 else '55*p'
    render=f'''const st={json.dumps(state)},clock={{v:0}}; const el=(x)=>document.getElementById('{i}-'+x);
function tr(x,v){{const a=el(x);if(a)a.setAttribute('transform',v)}}
function op(x,v){{const a=el(x);if(a)a.setAttribute('opacity',v)}}
function wire(cy){{let L=190,straight=Math.min(L,490-cy),rem=Math.max(0,L-straight),ang=Math.min(Math.PI/2,rem/30),dx=30*(1-Math.cos(ang)),dy=30*Math.sin(ang),tail=Math.max(0,rem-30*ang);let a=`M350 ${{cy}}V${{cy+straight}}`,b=`M650 ${{cy}}V${{cy+straight}}`;if(rem>0){{a+=` A30 30 0 0 0 ${{350+dx}} ${{490+dy}} L${{350+dx+tail}} ${{490+dy}}`;b+=` A30 30 0 0 1 ${{650-dx}} ${{490+dy}} L${{650-dx-tail}} ${{490+dy}}`}}return a+` M350 ${{cy}}H650 `+b}}
function draw(){{
const p=st.press;
if({str(isfront).lower()}){{let cy=220+200*p;let path=wire(cy);el('staple').setAttribute('d',path);el('staple-shadow').setAttribute('d',path);tr('blade',`translate(0 ${{200*p-120*st.lift}})`);op('blade',{'.12' if kind=='result' else '1'});op('bendhint',{ '1' if kind in ['clinch','result'] else '0'});op('force',{ '0' if kind=='result' else '1'});}}
else if({str(kind=='feed').lower()}){{tr('follower',`translate(${{42*st.feed}} 0)`);tr('row',`translate(${{42*st.feed}} 0)`);tr('staple-0',`translate(0 ${{150*st.drop}})`);tr('gate',`translate(0 ${{st.gate*100}})`);}}
else{{tr('cover',`translate(0 ${{-185*st.explode}}) rotate(${{12*p}} 172 455)`);tr('magazine',`translate(0 ${{-58*st.explode}}) rotate(${{8*p}} 172 455)`);tr('blade',`translate(0 ${{110*p-115*st.explode}})`);tr('wire',`translate(0 ${{{wirepos}}})`);tr('follower',`translate(${{38*st.feed}} 0)`);op('cover',{'.3' if kind in ['side','cycle'] else '1'});op('force',{ '0' if kind=='explode' else '1'});op('return',{ '1' if n==12 else '0'});}}
window['state_{i}']={{...st}};
}}
draw();const tl=gsap.timeline({{paused:true,onUpdate:draw}});
{''.join(anim)}
window.__timelines['{i}']=tl;
'''
    # Specific part annotations only where they teach a new relation.
    annotation=''
    if not isfront and kind!='feed':
        if n==2:annotation=label(220,140,410,305,'magazen & pengumpan')+label(690,80,809,304,'bilah')
        elif n==5:annotation=label(120,270,172,455,'engsel')
        elif n==6:annotation=label(590,260,810,490,'bilah → staples')
        elif n==12:annotation=label(210,250,400,465,'gerak kembali')
    if n==9:
        # The decisive forming beat deserves a genuine contact macro, not another unchanged front view.
        art=art.replace(f'<g id="{i}-labels">',f'<g id="{i}-labels" opacity="0">')
    vb='185 265 640 520' if n==9 else '0 0 1000 850'
    crop=' style="overflow:hidden"' if n==9 else ''
    svg=f'<svg viewBox="{vb}"{crop} aria-label="{e(kindlabels[kind])}" role="img">{defs(i)}{art}{annotation}</svg>'
    note='Ulangan jalur gaya · landasan tetap' if n==10 else notes[kind]
    content=f'''<template><style>{CSS}</style><div id="root" data-composition-id="{i}" data-width="1080" data-height="1920"><div class="scene clip" id="{i}-scene" data-start="0" data-duration="{d}"><div class="kicker">DI BALIK BENDA / {n+1:02}</div><h1 class="title" id="{i}-title">{e(s['title'])}</h1><div class="stage" id="{i}-stage">{svg}</div><div class="note">{e(note)}</div></div></div><script>{render}</script></template>'''
    write(V/f'compositions/{i}.html',content)
    for k,(at,dur,props) in enumerate(transitions[n]):
        # Event at start of purposeful movement; contact-specific cues additionally below.
        if props and (animated):events.append({'scene':i,'time':round(s['start']+at*s.get('motion_scale',1),6),'role':'editorial' if 'explode' in props or 'lift' in props else 'illustrative material','action':','.join(props)})

hosts='\n'.join(f'<div id="{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-start="{s["start"]:.6f}" data-duration="{s["duration"]:.6f}" data-width="1080" data-height="1920" data-track-index="1" data-track-kind="graphics"></div>' for s in plan)
media=''
if animated:
    meta=json.loads((V/'placed_audio.json').read_text())
    media=f'<audio id="narration" class="clip" src="assets/audio/narration-master.wav" data-start="0" data-duration="{meta["duration_s"]}" data-volume="1" data-track-index="3"></audio>\n<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="90" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920"></div>'
root=f'''<!doctype html><html lang="id" data-composition-variables='[{{"id":"canvas","type":"color","label":"Bench","default":"#ECEEE9"}}]'><head><meta charset="utf-8"><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>*{{box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#ECEEE9}}#root{{position:absolute;inset:0;background:var(--canvas,#ECEEE9)}}.clip{{position:absolute;inset:0}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="90" data-width="1080" data-height="1920">{hosts}{media}</div><script>const tl=gsap.timeline({{paused:true}});const clock={{v:0}};tl.to(clock,{{v:90,duration:90,ease:'none'}});window.__timelines['main']=tl;</script></body></html>'''
write(V/'index.html',root)
if animated:write(V/'motion-events.json',json.dumps(events,indent=2))
else:
    doc='''---
mode: autonomous
duration: 90
format: portrait
width: 1080
height: 1920
fps: 30
music: none
---

# Storyboard: one staple through the mechanism

Static pre-audio planning version. No human approval; agent verification under delegated automation. Board v4, locked 2.5D. All stills are posed in the actual composition. Later timing.json wins for measured time without changing shot order.

## Video direction
One blue front blade/guide landmark connects whole, magazine macro and transverse contact. Cover and magazine rotate around fixed rear hinge; anvil stays still. A wire changes shape continuously along anvil grooves; not a hinged rigid leg. Cutaways expose hidden layers; soft editorial accents identify explanatory separation. Causal events use restrained material cues. No music, no ambient loops. Titles stay fixed; only part actions and supporting attention cues move.

'''
    for n,s in enumerate(plan):
        doc+=f'''## Frame {n+1}: {s['title']} ({s['start']:g}–{s['end']:g}s)

- id: {s['id']}
- status: built
- type: mechanism
- act: {'question' if n<2 else 'inspect' if n<5 else 'operate' if n<12 else 'reset and answer'}
- purpose: {s['text']}
- on-screen: {s['title']}
- view: {s['view']}; layered 2.5D metal side faces, stable upper-left shading; {notes[s['view']]}.
- continuity: front guide/blade stays blue; anvil stays under paper. Entry state {initial[n]}; exit/diagnostic pose {poses[n]}. Whole→section and macro→section are labelled inspection transforms.
- action and diagnostic poses: {json.dumps(transitions[n])}. Inspect at approach, first contact and resulting state; look at input orange then blade blue then formed output. No alternate variant introduced.
- camera: stable framing during contact, varied scale/view by explanatory purpose; no camera-only mechanical evidence.
- sound: event onset from measured motion; cover/driver contact and return use reused light metal material accents, wire formation a restrained stylized attention accent; anatomy reveal uses soft editorial cue. Opening, identification and holds intentionally quiet between events. Sustained bending gets one shared cue rather than repeated transients.
- evidence: C1/C2 for feed/drive/return; C3/C4 for wire formation. Geometry original and not to scale.

'''
    write(V/'STORYBOARD.md',doc)
print(json.dumps({'mode':'animated' if animated else 'static storyboard','scenes':len(plan),'duration':sum(x['duration'] for x in plan)}))
