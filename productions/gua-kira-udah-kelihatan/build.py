"""Build board poses or the measured seek-safe film from the same scene geometry."""
from pathlib import Path
import argparse
import html
import json
import math
import re

P=Path(__file__).resolve().parent
V=P/'video'
C='#F3EDE3'; I='#302B28'; A='#A34F3F'; S='#D8C8B5'

def group(n,body): return f'<g id="beat{n}">{body}</g>'
def path(d,color=I,width=5,fill='none',extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def actor(x,y,k=1,color=I,other=False):
    d='M-72 -94C-15 -130 65 -102 88 -39C111 24 65 103 9 111C-54 121 -100 83 -105 15C-111 -35 -105 -73 -72 -94Z' if not other else 'M-75 -77C-34 -112 34 -100 72 -66C110 -31 105 24 75 71C41 120 -26 104 -63 77C-96 53 -110 -36 -75 -77Z'
    return f'<g transform="translate({x} {y}) scale({k})"><path d="{d}" fill="{color}"/></g>'
def bubble(x,y,w=390,h=210,color=S,fill='none',tail=True):
    return path(f'M{x+35} {y}H{x+w-35}Q{x+w} {y} {x+w} {y+35}V{y+h-35}Q{x+w} {y+h} {x+w-35} {y+h}H{x+95}L{x+45} {y+h+65}L{x+58} {y+h}H{x+35}Q{x} {y+h} {x} {y+h-35}V{y+35}Q{x} {y} {x+35} {y}Z',color,5,fill)
def waves(x,y,w=250,rows=3,color=A):
    return ''.join(path(f'M{x} {y+30*j}C{x+w*.25} {y+30*j-30} {x+w*.5} {y+30*j+30} {x+w*.72} {y+30*j}S{x+w*.9} {y+30*j-15} {x+w} {y+30*j}',color,4) for j in range(rows))
def line(x1,y1,x2,y2,color=A,dash=False):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="4" stroke-linecap="round"'+(' stroke-dasharray="4 16"' if dash else '')+'/>'
def circle(x,y,r,color=A,fill='none',width=4): return f'<circle cx="{x}" cy="{y}" r="{r}" stroke="{color}" stroke-width="{width}" fill="{fill}"/>'
def label(x,y,text,color=I,size=34): return f'<text x="{x}" y="{y}" fill="{color}" font-family="DM Sans" font-size="{size}" font-weight="400">{html.escape(text)}</text>'
def calendar(x,y,w=470):
    return f'<rect x="{x}" y="{y}" width="{w}" height="350" rx="24" fill="{S}"/>'+line(x+25,y+85,x+w-25,y+85,I)+line(x+110,y-25,x+110,y+35,I)+line(x+w-110,y-25,x+w-110,y+35,I)+''.join(circle(x+100+j*120,y+155+k*95,7,I,I) for j in range(3) for k in range(2))
def mug(x,y,k=1):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M0 0H100V90Q100 115 75 115H25Q0 115 0 90Z',I,5,S)+path('M100 20C165 5 165 85 100 75',I,5)+path('M30 -25C15 -55 50 -60 30 -95',A,4)+path('M65 -25C50 -55 85 -60 65 -95',A,4)+'</g>'

def art(n,dark):
    ink=C if dark else I
    if n==1:
        return [group(1,calendar(275,560)+actor(270,1170,.7)+actor(750,1170,.7,A,True)),group(2,path('M350 680L675 820M675 680L350 820',A,10)),group(3,bubble(140,905,280,100)+waves(175,950,180,1)),group(4,line(255,954,335,954,ink))]
    if n==2:
        return [group(1,actor(280,1050,1.6)+actor(820,1170,.55,A,True)),group(2,bubble(130,540,480,230,fill=S)+waves(185,610,350,4)),group(3,path('M435 1050C560 965 670 1100 748 1155',A,4,extra='stroke-dasharray="5 17"')),group(4,circle(690,820,43,S)+label(678,838,'?',ink,48))]
    if n==3:
        return [group(1,actor(320,1170,.9)),group(2,bubble(160,650,430,230,fill=S)+waves(205,725,310,3)),group(3,path('M645 610V1220',A,4,extra='stroke-dasharray="5 19"')),group(4,actor(825,1000,.65,A,True)+line(600,920,735,970,A,True))]
    if n==4:
        return [group(1,actor(255,1170,.8)+actor(805,1170,.8,A,True)),group(2,bubble(115,630,390,250,fill=S)+waves(170,720,270,3)),group(3,bubble(640,730,265,120)+line(680,785,815,785,ink)),group(4,path('M525 825C565 785 575 785 615 825',A,5))]
    if n==5:
        return [group(1,path('M160 1030Q530 980 905 1030L885 1130H180Z',S,5,S)+line(240,1130,240,1380,ink)+line(820,1130,820,1380,ink)),group(2,mug(300,850,1.2)),group(3,mug(650,850,1.2)),group(4,actor(275,660,.65)+path('M750 1220V1315M695 1315H805M695 1315V1390M805 1315V1390',A,6))]
    if n==6:
        return [group(1,actor(330,1050,1.4)),group(2,waves(175,720,380,4)),group(3,path('M510 1050C650 1040 700 890 840 900',ink,5)+circle(840,900,24,ink)),group(4,path('M460 680C700 660 780 800 815 885',A,5,extra='stroke-dasharray="5 18"'))]
    if n==7:
        return [group(1,actor(770,1140,1.15,A,True)),group(2,actor(240,940,.7)),group(3,bubble(120,620,310,135)+line(165,680,275,680,ink)),group(4,path('M370 930C480 870 620 940 690 1090',S,5,extra='stroke-dasharray="4 18"'))]
    if n==8:
        return [group(1,actor(250,1110,.82,ink)+actor(805,1110,.82,A,True)),group(2,line(365,1100,685,1100,S,True)),group(3,bubble(600,700,310,180,S)+label(724,817,'?',C,80)),group(4,path('M405 790C500 730 540 760 570 790',S,5,extra='stroke-dasharray="4 19"'))]
    if n==9:
        return [group(1,actor(280,1075,1.25)),group(2,circle(280,1075,210,S)),group(3,actor(790,1075,.85,A,True)),group(4,path('M500 1075H650',ink,4)+circle(575,1075,38,C,C)+label(559,1091,'?',A,48))]
    if n==10:
        return [group(1,actor(300,1000,1.4,ink)),group(2,waves(172,900,240,4,A)),group(3,bubble(600,650,305,155,S)+line(640,705,825,705,C)),group(4,path('M545 635V1310',S,4)+label(160,1310,'rasa',C,40)+label(695,1150,'pesan',C,40))]
    if n==11:
        return [group(1,actor(245,1150,.8)+actor(805,1150,.8,A,True)),group(2,bubble(120,650,440,240)),group(3,path('M165 725C240 700 310 760 380 725S440 710 480 725',A,5)),group(4,path('M565 850C680 850 740 970 775 1050',ink,5))]
    if n==12:
        return [group(1,actor(260,1175,1.05)),group(2,bubble(140,600,680,280,fill=S)),group(3,waves(210,690,470,3)),group(4,path('M700 920C750 990 765 1020 790 1090',A,5)+actor(830,1195,.65,A,True))]
    if n==13:
        return [group(1,calendar(290,620,440)),group(2,mug(160,1115,.9)),group(3,mug(740,1115,.9)),group(4,path('M300 1000Q540 880 805 1000',A,5)+circle(540,940,15,A,A))]
    if n==14:
        return [group(1,actor(240,1170,.8)+actor(810,1170,.8,A,True)),group(2,bubble(120,630,330,180,fill=S)+waves(165,690,220,2)),group(3,path('M370 1050C510 870 650 870 750 1050',ink,5)),group(4,bubble(600,650,300,165,A)+waves(640,710,210,2,ink))]
    if n==15:
        return [group(1,path('M220 700V1250',S,5)+actor(220,1315,.48)),group(2,circle(220,785,16,A,A)+line(250,785,680,785,ink)),group(3,circle(220,960,16,A,A)+line(250,960,680,960,ink)),group(4,circle(220,1135,16,A,A)+line(250,1135,680,1135,ink)+actor(820,960,.7,A,True))]
    return [group(1,actor(250,1180,.8)+actor(805,1180,.8,A,True)),group(2,bubble(130,650,430,225,fill=S)+waves(180,720,300,3)),group(3,path('M380 1100C500 970 640 970 745 1100',ink,5)),group(4,circle(560,1005,17,A,A))]

PURPOSES=[
 'Establish a canceled shared plan and the speaker becoming quieter.',
 'Contrast a large internal feeling with an uncertain external reception.',
 'Name the established concept early while retaining the two participants.',
 'Distinguish the rich internal experience from a sparse observable signal.',
 'Make the lost expectation concrete with two cups and an unoccupied place.',
 'Show the inside perspective remaining present while estimating another view.',
 'Reverse the focal scale so the observer sees only the short answer.',
 'Hold the missing meaning without assigning a motive to the observer.',
 'Keep a single event within its evidence boundary rather than judge care.',
 'Make the central distinction between feeling and communicated message.',
 'Open a space for giving information rather than demanding a guess.',
 'Name disappointment directly as the one practical application.',
 'Add the reason the canceled time mattered, using the established objects.',
 'Let an actual response become possible without promising agreement.',
 'Show a repeated response pattern as something to observe, without diagnosis.',
 'Resolve the opening by looking at what has actually been communicated.'
]
MOTIONS={
1:[(2,'draw',.12),(3,'reveal',.34),(4,'shrink',.73)],
2:[(2,'grow',.18),(3,'draw',.45),(4,'reveal',.75)],
3:[(2,'reveal',.16),(3,'draw',.45),(4,'move-left',.72)],
4:[(2,'grow',.15),(3,'reveal',.43),(4,'draw',.75)],
5:[(2,'move-right',.13),(3,'reveal',.4),(4,'reveal',.73)],
6:[(2,'grow',.12),(3,'draw',.42),(4,'draw',.7)],
7:[(2,'move-right',.1),(3,'reveal',.38),(4,'draw',.7)],
8:[(2,'draw',.12),(3,'reveal',.4),(4,'draw',.73)],
9:[(2,'grow',.15),(3,'move-left',.42),(4,'reveal',.7)],
10:[(2,'reveal',.15),(3,'reveal',.4),(4,'draw',.7)],
11:[(2,'grow',.12),(3,'draw',.4),(4,'draw',.7)],
12:[(2,'grow',.12),(3,'draw',.4),(4,'move-left',.7)],
13:[(2,'move-right',.1),(3,'move-left',.4),(4,'draw',.72)],
14:[(2,'grow',.12),(3,'draw',.4),(4,'reveal',.7)],
15:[(2,'draw',.12),(3,'draw',.39),(4,'draw',.69)],
16:[(2,'grow',.12),(3,'draw',.37),(4,'reveal',.65)]}

FONTS="""@font-face{font-family:'Newsreader';src:url('assets/fonts/newsreader.ttf')}@font-face{font-family:'DM Sans';src:url('assets/fonts/dm-sans.ttf')}"""

def timings(lines):
    if (V/'timing.json').exists(): return json.loads((V/'timing.json').read_text(encoding='utf-8'))['scenes']
    weights=[max(8,len(x['text'].split())) for x in lines]
    total=sum(weights); start=0; result=[]
    for x,w in zip(lines,weights):
        dur=round(90*w/total,5)
        result.append({'id':x['id'],'start':start,'duration':dur,'end':start+dur})
        start+=dur
    result[-1]['end']=90;result[-1]['duration']=90-result[-1]['start']
    return result

def scene_html(x,t,animated):
    n=x['id']; cid=f'f{n:02d}'; dur=t['duration']; ink=C if x['dramatic'] else I; bg=I if x['dramatic'] else C
    parts=art(n,x['dramatic'])
    header=(V/'assets/board/components/chrome.html').read_text(encoding='utf-8').replace('{{frame_number}}',f'{n:02d}').replace('{{frame_count}}','16')
    chrome=(V/'assets/board/components/chrome.css').read_text(encoding='utf-8')
    css=FONTS+chrome+f'''#root{{position:absolute;inset:0;width:1080px;height:1920px;color:{ink};--rda-meta-ink:{ink};font-family:'DM Sans',sans-serif;}}
    .ground{{position:absolute;inset:0;background:{bg};z-index:0;}}
    .drawing{{position:absolute;inset:0;width:1080px;height:1920px;z-index:2;}}
    .heading{{position:absolute;left:88px;top:270px;width:848px;font:400 {72 if n==3 else 88}px/1.06 'Newsreader',serif;letter-spacing:-.02em;z-index:5;margin:0;}}
    .pose-caption{{position:absolute;left:88px;top:1550px;width:848px;text-align:center;font:500 46px/1.25 'DM Sans',sans-serif;}}
    '''
    content=f'<div id="ground" class="clip ground" data-start="0" data-duration="{dur:.5f}" data-track-index="0"></div>'+header
    content+=f'<svg id="drawing" class="clip drawing" data-start="0" data-duration="{dur:.5f}" data-track-index="1" viewBox="0 0 1080 1920" aria-label="{html.escape(PURPOSES[n-1])}">'+''.join(parts)+'</svg>'
    if x['emphasis']: content+=f'<h1 id="heading" class="clip heading" data-start="0" data-duration="{dur:.5f}" data-track-index="2">{html.escape(x["emphasis"])}</h1>'
    if not animated: content+=f'<div class="pose-caption">{html.escape(" ".join(x["text"].split()[:6]))}</div>'
    js='const tl=gsap.timeline({paused:true});\n'
    if animated:
        for b,move,f in MOTIONS[n]:
            at=max(.05,dur*f); d=min(.65,dur*.16)
            if move=='draw':
                js+=f'''{{const el=document.querySelector('#beat{b}');const lines=document.querySelectorAll('#beat{b} path,#beat{b} line,#beat{b} circle');tl.fromTo(el,{{opacity:0}},{{opacity:1,duration:.12}}, {at:.5f});lines.forEach(p=>{{if(p.getTotalLength){{const len=p.getTotalLength();tl.fromTo(p,{{strokeDasharray:len,strokeDashoffset:len}},{{strokeDashoffset:0,duration:{d:.5f},ease:'power2.inOut'}},{at:.5f});}}}});}}\n'''
            elif move=='grow':
                js+=f"tl.fromTo('#beat{b}',{{scale:.72,opacity:0,transformOrigin:'50% 75%'}},{{scale:1,opacity:1,duration:{d:.5f},ease:'power2.out'}},{at:.5f});\n"
            elif move=='shrink':
                js+=f"tl.fromTo('#beat{b}',{{scaleX:1.9,opacity:0,transformOrigin:'0% 50%'}},{{scaleX:1,opacity:1,duration:{d:.5f},ease:'power2.inOut'}},{at:.5f});\n"
            elif move=='move-left' or move=='move-right':
                dx=65 if move=='move-left' else -65
                js+=f"tl.fromTo('#beat{b}',{{x:{dx},opacity:0}},{{x:0,opacity:1,duration:{d:.5f},ease:'power3.out'}},{at:.5f});\n"
            else: js+=f"tl.fromTo('#beat{b}',{{opacity:0}},{{opacity:1,duration:{d:.5f},ease:'power2.out'}},{at:.5f});\n"
        if n==1:
            js+=f"tl.to('#beat3',{{scaleX:.63,transformOrigin:'0% 50%',duration:.45,ease:'power2.inOut'}},{dur*.68:.5f});\n"
    js+=f"tl.to({{}},{{duration:{dur:.5f}}},0);window.__timelines=window.__timelines||{{}};window.__timelines['{cid}']=tl;"
    return f'<!doctype html><html><head><meta charset="UTF-8"></head><body><template><style>{css}</style><div id="root" data-composition-id="{cid}" data-start="0" data-duration="{dur:.5f}" data-width="1080" data-height="1920">{content}</div><script>{js}</script></template></body></html>'

def index_html(lines,ts,animated):
    total=ts[-1]['end']; hosts=[]
    for x,t in zip(lines,ts):
        n=x['id'];cid=f'f{n:02d}'
        hosts.append(f'<div id="scene-{n:02d}" class="clip scene-host" data-composition-id="{cid}" data-composition-src="compositions/frames/{cid}.html" data-start="{t["start"]:.5f}" data-duration="{t["duration"]:.5f}" data-width="1080" data-height="1920" data-track-index="1" data-track-kind="graphics" style="z-index:{n}"></div>')
    if animated:
        meta=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'))
        placement=json.loads((V/'placement.json').read_text(encoding='utf-8'))
        audio=placement['path']
        hosts.append(f'<audio id="narration" class="clip" src="{audio}" data-start="0" data-duration="{placement["duration"]:.5f}" data-volume="1" data-track-index="3"></audio>')
        hosts.append(f'<div id="captions-host" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{total:.5f}" data-width="1080" data-height="1920" data-track-index="2" data-track-kind="captions" style="z-index:100"></div>')
    return f'''<!doctype html><html lang="id" data-resolution="portrait"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><title>Gua kira udah kelihatan</title><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>{FONTS}*{{box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:{C}}}#root{{position:relative;width:1080px;height:1920px;background:{C};}}.scene-host{{position:absolute;inset:0}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{total:.5f}" data-width="1080" data-height="1920">{''.join(hosts)}</div><script>const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration:{total:.5f}}},0);window.__timelines=window.__timelines||{{}};window.__timelines.main=tl;</script></body></html>'''

def storyboard(lines,ts,animated):
    doc='''---
format: 1080x1920
duration: 90s
message: "A strong feeling is not necessarily an equally clear message."
arc: canceled plan → internal experience → concept → external view → distinction → expression → response
audience: Indonesian adults
mode: autonomous
music: none
---

# Gua kira udah kelihatan — visual storyboard v1

## Video direction

Follow one canceled-plan interaction, preserving the charcoal speaker's and brick listener's silhouettes. The camera alternates interaction, internal close view, external close view and concrete cups/calendar. A thought space is metaphorical, never data. Figures do not encode gender, blame or a diagnosis. Approved board editorial v1.3 and visual v1.2 govern fonts, colors, fixed chrome and captions. Exactly 16 meaningful compositions; charcoal inversion at 8 and 10 only. All other shots are cream. No B-roll, decorative floating, generic cards, notification pings or repeated transition sounds.

The user accepted Hook 2. Later verification and rendering are delegated by --automation=after-hook; the static board remains required and agent-verified before audio and animation. Narrative and layouts are not claimed human-approved.

Motion: absolute seek-safe GSAP with power2.out for revealing information, power2.inOut for traced relations, power3.out for a participant's motivated shift; finite 0.3-0.65s actions. Main typography and chrome land without drift. Each scene has an existing opening situation and three later semantic developments, distributed through the shot. Hold only after the explanation has landed.

Sound: one continuous ElevenLabs narration, native speed, root .env voice and eleven_v4. No BGM: the gap between internal feeling and externally available information benefits from unfilled pauses, without music suggesting a partner's intention. Sparse frozen board material cues on cancellation, shift of viewpoint and connection. Silence at the uncertain-meaning turn and final reflection is deliberate. Estimated cues are resolved to measured narration before placement.

Registry discovery: searched conversational captions and organic faceless conversation diagrams. Caption Weight Shift and Thread Message Stack were reviewed as candidates; neither preserves the board's fixed plain-caption identity or organic illustrative vocabulary. Reuse canonical board sources and draw the episode-specific objects. No named visual effect is recreated.

'''
    for x,t in zip(lines,ts):
        n=x['id']; dur=t['duration']; doc+=f'''## Frame {n} — {x['title']}

- status: {'animated' if animated else 'built'}
- src: compositions/frames/f{n:02d}.html
- duration: {dur:.5f}s
- start: {t['start']:.5f}s
- end: {t['end']:.5f}s
- poster: {dur*.87:.5f}
- transition_in: cut
- scene: {PURPOSES[n-1]}
- voiceover: "{x['text']}"
- palette: {'dramatic' if x['dramatic'] else 'light'}
- emphasis: "{x['emphasis']}"
- act: {'recognition' if n<=2 else 'explanation' if n<=10 else 'application'}

Purpose: {PURPOSES[n-1]}
Layout: {['shared interaction with a large calendar','asymmetric internal close view','concept above an opening thought space','large internal view and sparse external view','table and two cups with an empty place','speaker close view and curved perspective path','listener foreground, speaker reduced','wide uncertain relation on charcoal','single event isolated without a verdict','two distinct reading zones on charcoal','two participants with open speaking space','large speaking space with an explicitly directed path','calendar and two established cups','reciprocal relation made visible','three observed response traces','return to the initial pair with a completed path'][n-1]}.
Initial state: {PURPOSES[n-1].split('.')[0]}; the first group is already locatable on frame entry.
'''
        for b,move,f in MOTIONS[n]: doc+=f'- At {dur*f:.2f}s: beat {b}, {move}, develops the next information-bearing group in the shot; duration {min(.65,dur*.16):.2f}s.\n'
        doc+=f"Final state: the full scene is readable at {dur*.87:.2f}s; fixed chrome and actor identities persist. Handoff: cut from the established relation or object to the next perspective.\n"
        if x['dramatic']: doc+=f'Dramatic line: "{x["text"]}". Reason: {"the missing meaning becomes visible without judging intent" if n==8 else "the central distinction changes the interpretation of the opening"}. All text, captions and chrome invert together.\n'
        doc+='\n'
    return doc

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--animated',action='store_true');args=parser.parse_args()
    lines=json.loads((V/'script_data.json').read_text(encoding='utf-8')); ts=timings(lines)
    (V/'compositions/frames').mkdir(parents=True,exist_ok=True)
    for x,t in zip(lines,ts): (V/f'compositions/frames/f{x["id"]:02d}.html').write_text(scene_html(x,t,args.animated),encoding='utf-8')
    (V/'index.html').write_text(index_html(lines,ts,args.animated),encoding='utf-8')
    (V/'STORYBOARD.md').write_text(storyboard(lines,ts,args.animated),encoding='utf-8')
    (V/'scene_schedule.json').write_text(json.dumps(ts,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'frames':16,'dramatic':[8,10],'animated':args.animated,'duration':ts[-1]['end'],'snapshot_at':','.join(f'{t["start"]+t["duration"]*.87:.3f}' for t in ts)}))

if __name__=='__main__':main()
