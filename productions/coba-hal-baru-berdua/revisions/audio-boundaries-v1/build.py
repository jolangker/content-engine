"""Pose the sixteen scenes, then assemble measured worker-owned animations."""
from pathlib import Path
import argparse
import html
import json

P=Path(__file__).resolve().parent;V=P/'video';C='#F3EDE3';I='#302B28';A='#A34F3F';S='#D8C8B5'
def path(d,c=I,w=5,fill='none',extra=''):return f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def line(x,y,xx,yy,c=I,w=5):return path(f'M{x} {y}L{xx} {yy}',c,w)
def circle(x,y,r,c=I,fill='none',w=5):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{w}"/>'
def rect(x,y,w,h,c=S,fill='none',r=25):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" stroke="{c}" stroke-width="5" fill="{fill}"/>'
def group(n,body):return f'<g id="beat{n}">{body}</g>'
def actor(x,y,k=1,c=I,other=False):
    d='M-72 -94C-15 -130 65 -102 88 -39C111 24 65 103 9 111C-54 121 -100 83 -105 15C-111 -35 -105 -73 -72 -94Z' if not other else 'M-75 -77C-34 -112 34 -100 72 -66C110 -31 105 24 75 71C41 120 -26 104 -63 77C-96 53 -110 -36 -75 -77Z'
    return f'<g transform="translate({x} {y}) scale({k})">{path(d,c,1,c)}</g>'
def plate(x,y,r=95,c=I):return circle(x,y,r,c)+circle(x,y,r*.64,S,w=3)+line(x-r-28,y-r*.7,x-r-28,y+r*.7,c,4)+line(x+r+30,y-r*.7,x+r+30,y+r*.7,c,4)
def bowl(x,y,k=1,c=I):return f'<g transform="translate({x} {y}) scale({k})">'+path('M-170 0Q0 260 170 0Z',c,6,S)+path('M-170 0Q0 -50 170 0',c,6)+path('M-115 5Q0 35 115 5',A,5)+'</g>'
def recipe(x,y,k=1,c=I):return f'<g transform="translate({x} {y}) scale({k})">'+rect(-110,-165,220,330,c,C)+line(-65,-100,55,-100,c,5)+circle(-62,-30,9,A,A)+line(-25,-30,65,-30,c,4)+circle(-62,30,9,A,A)+line(-25,30,65,30,c,4)+circle(-62,90,9,A,A)+line(-25,90,45,90,c,4)+'</g>'
def bubble(x,y,w=360,h=160,c=I):return path(f'M{x+25} {y}H{x+w-25}Q{x+w} {y} {x+w} {y+25}V{y+h-25}Q{x+w} {y+h} {x+w-25} {y+h}H{x+100}L{x+50} {y+h+60}L{x+60} {y+h}H{x+25}Q{x} {y+h} {x} {y+h-25}V{y+25}Q{x} {y} {x+25} {y}Z',c,5)
def ribbon(x,y,w=220,c=A):return path(f'M{x} {y}C{x+w*.3} {y-45} {x+w*.6} {y+45} {x+w} {y}',c,5)
def dough(x,y,k=1,c=I):return f'<g transform="translate({x} {y}) scale({k})">'+path('M-115 30C-145 -30 -45 -85 20 -60C70 -90 165 -10 110 50C70 100 -90 100 -115 30Z',c,5,S)+path('M-40 -15Q-10 0 -20 35M35 -20Q55 0 45 30',A,4)+'</g>'

DESIGNS=[
('Overhead familiar dinner and repeated route','Place the two plates on the sand table; trace the familiar return; repeat its curve; locate the pair at the same endpoint.',['table and plates','familiar return route','second matching trace','pair at endpoint']),
('One self, opening toward more experience','Begin with a large charcoal participant; open an arc around it; place a new experience mark; add a second differently shaped mark.',['participant','opening perspective arc','first experience marker','second marker']),
('Two people enter one unfamiliar path','Locate the pair; join a shared curved path; add an unfamiliar branch; land an event shape on that branch.',['two participants','shared route','new branch','new event']),
('Three repetitions of the weekend','Locate one overhead dinner; reveal the same dinner lower and offset; reveal a third; trace one continuous routine through them.',['first dinner','second dinner','third dinner','repeated route']),
('The space inside the familiar','Keep the pair on either side of a large quiet interval; make the known path; open a second gap; leave a small possible new event there.',['pair and interval','familiar connecting arc','opening gap','possible new experience']),
('Recipe and bowl close view','Start at the large empty mixing bowl; bring in the recipe; let flour meet the bowl; lower the spoon toward the mixture.',['bowl','recipe','flour','spoon']),
('A small difficulty, then a role change','Locate both actors and the countertop; bring in the irregular dough; place the recipe by the reader; exchange attention with an arc across the working surface.',['counter and pair','dough','recipe by reader','exchange arc']),
('A new angle on the partner','Keep both silhouettes locatable on charcoal; reveal the partner beside the dough; open a cream viewing arc from the observer; land a new experience mark near the partner.',['observer and partner','unfamiliar task','new view arc','experience mark']),
('The finding is a short before and after','Locate two pairs around a short interval; introduce the novel task between them; trace the immediate passage; place a small bounded clock without a long-term projection.',['paired observations','shared task','short passage','bounded clock']),
('A shared activity leaves other issues open','Hold the bowl on charcoal; introduce a separate speaking space; expose an unresolved ribbon inside that space; stop the path before joining them.',['bowl','separate speaking space','unresolved ribbon','limited connecting route']),
('Mutual choice joins in the middle','Place the pair at opposite sides; offer a small choice from the left; offer one from the right; let both paths meet at the shared bowl.',['pair','left preference','right preference','shared choice']),
('A concrete invitation with room for an answer','Keep the speaker and listener apart; open a large invitation space; show a recipe in the space; extend a small open reply curve toward the listener.',['pair','invitation space','recipe offered','room for reply']),
('Another choice is allowed','Start with the pair and a recipe choice; add a walking route alternative; add a simple making-object alternative; separate the options with open space rather than a forced selection.',['pair and recipe','walking option','making option','open alternative route']),
('Reflect on the experience together','Locate the bowl between the pair; open a speaking space from the left; echo an answering space from the right; place the shared memory trace between them.',['pair and bowl','question space','answer space','shared trace']),
('Imperfect bread, shared experience','Begin with an uneven loaf; divide a portion without making it perfect; reveal two plates; connect both portions to the shared making trace.',['uneven loaf','shared portion','two plates','shared making trace']),
('Return to the familiar table, leave a new route open','Return to the original pair at a table; place the mixing bowl between them; open a route beyond the table; leave the final experience marker unfilled as a quiet question.',['pair and table','bowl together','open route','unfilled possibility']),
]

def art(n,dark):
    ink=C if dark else I
    if n==1:return [group(1,rect(175,560,675,470,S,S,90)+plate(380,795,110)+plate(665,795,110)),group(2,path('M235 1150C140 1240 260 1380 520 1375C820 1370 920 1190 790 1140',A,6)),group(3,path('M280 1180C225 1265 340 1320 520 1320C730 1320 820 1240 755 1190',I,4)),group(4,actor(365,1100,.58)+actor(675,1100,.58,A,True))]
    if n==2:return [group(1,actor(510,1010,1.7)),group(2,path('M290 1120C80 870 260 565 570 600C840 635 920 865 805 1110',A,6)),group(3,rect(215,645,145,145,S,S,45)+path('M250 720L280 685L325 740',I,5)),group(4,circle(800,925,80,A)+path('M755 925L790 950L840 895',I,5))]
    if n==3:return [group(1,actor(270,1220,.85)+actor(790,1220,.85,A,True)),group(2,path('M290 1090Q530 880 770 1090',I,6)),group(3,path('M530 988Q430 830 565 680',A,6)),group(4,rect(480,540,185,145,S,S,55)+circle(575,610,32,A))]
    if n==4:return [group(1,plate(310,650,85)+plate(570,650,85)),group(2,plate(470,940,85)+plate(730,940,85)),group(3,plate(310,1240,85)+plate(570,1240,85)),group(4,path('M755 650C915 745 890 825 850 940C800 1110 805 1260 715 1280',A,6))]
    if n==5:return [group(1,actor(240,1100,1)+actor(810,1100,1,A,True)),group(2,path('M310 1270Q525 1390 755 1270',S,5)),group(3,path('M370 920Q520 680 690 920',I,5)),group(4,circle(530,785,58,A)+path('M515 785H545M530 770V800',A,4))]
    if n==6:return [group(1,bowl(510,1030,1.65)),group(2,recipe(780,685,.83)),group(3,circle(400,800,10,S,S)+circle(455,855,8,S,S)+circle(510,920,11,S,S)+circle(560,850,9,S,S)),group(4,path('M625 650L495 1035',I,18)+circle(493,1038,30,A,S))]
    if n==7:return [group(1,actor(280,700,1)+actor(790,700,.95,A,True)+path('M145 1005H910L870 1190H185Z',S,4,S)),group(2,dough(500,985,1.3)),group(3,recipe(775,915,.53)),group(4,path('M285 1190Q525 1380 785 1185',A,6)+path('M755 1175L790 1185L775 1225',A,5))]
    if n==8:return [group(1,actor(265,1120,1.15,ink)+actor(785,850,.85,A,True)),group(2,dough(760,1130,.72,ink)),group(3,path('M370 1010C430 690 680 570 845 690',S,6)),group(4,circle(805,600,38,C)+line(805,550,805,530,S)+line(850,580,875,565,S))]
    if n==9:return [group(1,actor(265,730,.6)+actor(465,730,.6,A,True)+actor(625,1230,.6)+actor(825,1230,.6,A,True)),group(2,bowl(530,955,.8)),group(3,path('M350 825C160 1000 395 1230 520 1230',I,5)),group(4,circle(805,760,72,A)+line(805,760,805,717,I,4)+line(805,760,842,775,I,4))]
    if n==10:return [group(1,bowl(300,1130,.9,ink)),group(2,bubble(545,620,335,220,S)),group(3,path('M590 725C635 640 740 825 785 725C830 640 695 715 720 770',C,5)),group(4,path('M405 1110C550 1080 595 980 610 910',S,5)+circle(610,910,10,C,C))]
    if n==11:return [group(1,actor(250,1170,.9)+actor(810,1170,.9,A,True)),group(2,recipe(260,735,.55)+path('M260 865Q320 950 460 1035',I,5)),group(3,circle(790,730,70,A)+path('M790 810Q740 950 600 1035',A,5)),group(4,bowl(530,1050,.63)+circle(530,980,12,A,A))]
    if n==12:return [group(1,actor(245,1210,.8)+actor(815,1210,.8,A,True)),group(2,bubble(150,565,680,325,I)),group(3,recipe(480,720,.72)),group(4,path('M670 990C750 965 825 1020 825 1090',A,5))]
    if n==13:return [group(1,actor(255,1240,.65)+actor(790,1240,.65,A,True)+recipe(255,680,.58)),group(2,path('M550 585C435 690 665 755 530 835',A,7)+circle(530,835,13,I,I)),group(3,path('M720 665Q790 610 865 665L845 800H740Z',I,5,S)+line(725,665,860,665,A)),group(4,path('M310 1070Q530 930 780 1070',S,5))]
    if n==14:return [group(1,actor(245,1230,.8)+actor(810,1230,.8,A,True)+bowl(530,1220,.55)),group(2,bubble(135,625,360,185,I)+ribbon(180,705,235,A)),group(3,bubble(575,845,335,175,A)+ribbon(620,925,225,I)),group(4,path('M340 1095Q520 995 695 1100',S,5))]
    if n==15:return [group(1,dough(500,775,1.75)),group(2,path('M505 680C470 720 535 795 495 855',A,5)),group(3,plate(275,1200,100)+plate(775,1200,100)),group(4,path('M405 910Q330 970 285 1080M615 910Q715 970 765 1080',I,5)+circle(280,1120,22,S,S)+circle(775,1120,22,S,S))]
    return [group(1,rect(175,920,675,270,S,S,70)+actor(290,760,.95)+actor(770,760,.95,A,True)),group(2,bowl(530,990,.65)),group(3,path('M525 1185C530 1360 800 1350 825 1170',A,6)),group(4,circle(825,1120,36,I))]

FONTS="@font-face{font-family:'Newsreader';src:url('assets/fonts/newsreader.ttf')}@font-face{font-family:'DM Sans';src:url('assets/fonts/dm-sans.ttf')}"
def schedule(lines):
    if (V/'timing.json').exists():return json.loads((V/'timing.json').read_text(encoding='utf-8'))['scenes']
    weights=[len(x['text'].split()) for x in lines];total=sum(weights);ts=[];start=0
    for x,w in zip(lines,weights):
        end=start+90*w/total;ts.append(dict(id=x['id'],start=start,end=end,duration=end-start));start=end
    return ts
def pose(x,t):
    n=x['id'];cid=f'f{n:02d}';d=t['duration'];ink=C if x['dramatic'] else I;bg=I if x['dramatic'] else C
    chrome=(V/'assets/board/components/chrome.html').read_text(encoding='utf-8').replace('{{frame_number}}',f'{n:02d}').replace('{{frame_count}}','16')
    css=FONTS+(V/'assets/board/components/chrome.css').read_text(encoding='utf-8')+f"#root{{position:absolute;inset:0;width:100%;height:100%;color:{ink};--rda-meta-ink:{ink};font-family:'DM Sans',sans-serif}}.ground{{position:absolute;inset:0;background:{bg}}}.drawing{{position:absolute;inset:0;width:1080px;height:1920px}}.heading{{position:absolute;left:88px;top:270px;width:848px;margin:0;font:400 {80 if n==2 else 88}px/1.06 'Newsreader',serif;letter-spacing:-.02em}}.pose-caption{{position:absolute;left:88px;top:1550px;width:848px;text-align:center;font:500 46px/1.25 'DM Sans',sans-serif}}"
    main=f'<div id="root" data-composition-id="{cid}" data-start="0" data-duration="{d:.5f}" data-width="1080" data-height="1920"><div id="ground" class="clip ground" data-start="0" data-duration="{d:.5f}" data-track-index="0"></div>{chrome}<svg id="drawing" class="clip drawing" data-start="0" data-duration="{d:.5f}" data-track-index="1" viewBox="0 0 1080 1920" aria-label="{html.escape(DESIGNS[n-1][0])}">{"".join(art(n,x["dramatic"]))}</svg>'
    if x['emphasis']:main+=f'<h1 id="heading" class="clip heading" data-start="0" data-duration="{d:.5f}" data-track-index="2">{html.escape(x["emphasis"])}</h1>'
    main+=f'<div class="pose-caption">{html.escape(" ".join(x["text"].split()[:6]))}</div></div>'
    return f'<template><style>{css}</style>{main}<script>const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration:{d:.5f}}},0);window.__timelines["{cid}"]=tl;</script></template>'
def index(lines,ts,animated):
    total=ts[-1]['end'];hosts=[]
    for x,t in zip(lines,ts):
        n=x['id'];hosts.append(f'<div id="scene-{n:02d}" class="clip scene-host" data-composition-id="f{n:02d}" data-composition-src="compositions/frames/f{n:02d}.html" data-start="{t["start"]:.5f}" data-duration="{t["duration"]:.5f}" data-width="1080" data-height="1920" data-track-index="1" data-track-kind="graphics" style="z-index:{n}"></div>')
    if animated:
        pl=json.loads((V/'placement.json').read_text(encoding='utf-8'))
        hosts+=[f'<audio id="narration" class="clip" src="{pl["path"]}" data-start="0" data-duration="{pl["duration"]:.5f}" data-volume="1" data-track-index="3"></audio>',f'<div id="caption-host" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{total:.5f}" data-width="1080" data-height="1920" data-track-index="2" data-track-kind="captions" style="z-index:100"></div>']
    return f'<!doctype html><html lang="id" data-resolution="portrait"><head><meta charset="UTF-8"><title>Coba hal baru berdua</title><script src="vendor/gsap.min.js"></script><style>{FONTS}*{{box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:{C}}}#root{{position:relative;width:100%;height:100%;background:{C}}}.scene-host{{position:absolute;inset:0}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{total:.5f}" data-width="1080" data-height="1920">{"".join(hosts)}</div><script>const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration:{total:.5f}}},0);window.__timelines.main=tl;</script></body></html>'
def storyboard(lines,ts,animated):
    doc=f'''---
format: 1080x1920
duration: {ts[-1]['end']:.5f}s
message: "Make room for one mutually wanted new experience."
arc: routine → self-expansion → cooking together → evidence and limits → invitation → shared reflection
audience: Indonesian adults
mode: autonomous
music: none
---

# Coba hal baru berdua — visual storyboard v1

## Video direction

Canonical editorial v1.3 / visual v1.2. Exactly sixteen shots, fourteen cream and two charcoal (8 and 10). Keep the two organic silhouettes consistent: irregular charcoal form and rounded brick form; no gender or blame coding. New experience marks are metaphors, not empirical measurements. Fixed series chrome never joins motion. Full spoken captions occupy y1550–1740, key content x88–936/y230–1480. Alternate overhead dinner, single-self view, pair/path, repeated dinner detail, negative-space interval, bowl/recipe close-up, working counter, viewpoint change, bounded research illustration, two separate concerns, mutual selection, invitation, alternatives, reciprocal reflection, imperfect result and open ending. This changes focal geometry, scale, density and relation across the sequence.

Motion: compose three later semantic phases after an already-visible opening situation. Use SVG path draws, finite transform-only shifts and restrained opacity reveals. Typical beat fractions 0.14 / 0.43 / 0.73, varied by narration. No independent loops, decorative drifting or repeated heading entrance. Final frame holds quietly after the open question.

Registry discovery queried organic conversation/shared activity. Organic Light Leak Overlay and Message Thread Reveal are unsuitable for the canonical flat illustration and full plain captions; no named effect is recreated. Reuse board identity and draw story-specific cooking objects.

Automation override: static poses, sixteen stills, HTML board and complete PNG are required and agent-verified before synthesis and motion. No human storyboard approval is claimed. The script was agent-selected and verified under --automation.

Audio: one full-script ElevenLabs request, eleven_v4, root .env voice. No BGM because quiet action and open pauses carry the small experiment. Sparse licensed board contact/air/connection cues will follow measured visual actions, silence for the limitation and closing hold. See sound_design.json after audio placement.

'''
    for x,t in zip(lines,ts):
        n=x['id'];title,idea,beats=DESIGNS[n-1]
        doc+=f'''## Frame {n} — {x['title']}

- status: {'animated' if animated else 'built'}
- src: compositions/frames/f{n:02d}.html
- duration: {t['duration']:.5f}s
- start: {t['start']:.5f}s
- end: {t['end']:.5f}s
- poster: {t['duration']*.9:.5f}
- transition_in: cut
- scene: {title}
- voiceover: "{x['text']}"
- palette: {'dramatic' if x['dramatic'] else 'light'}
- emphasis: "{x['emphasis']}"
- blueprint: compose
- act: {'recognition' if n==1 else 'explanation' if n<=10 else 'application'}

Purpose/layout: {title}. {idea}
Scene 1 (0–{t['duration']*.14:.2f}s): {beats[0]} is already locatable. Scene 2 ({t['duration']*.14:.2f}–{t['duration']*.43:.2f}s): {beats[1]} enters or develops. Scene 3 ({t['duration']*.43:.2f}–{t['duration']*.73:.2f}s): {beats[2]} changes the relation. Scene 4 ({t['duration']*.73:.2f}–{t['duration']:.2f}s): {beats[3]} lands; allow a short deliberate read. These are semantic state changes, not caption counts. Preserve the verified static landed composition.
'''
        if x['dramatic']:doc+=f'Dramatic line: "{x["text"]}". Reason: {"the unfamiliar shared task reveals another view of the partner" if n==8 else "the evidence limit interrupts any promise of a lasting cure"}. Invert ground, emphasis, captions and chrome together; retain silhouettes.\n'
        doc+='\n'
    return doc
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--assemble',action='store_true');args=ap.parse_args()
    lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));ts=schedule(lines);(V/'compositions/frames').mkdir(parents=True,exist_ok=True)
    if not args.assemble:
        for x,t in zip(lines,ts):(V/f'compositions/frames/f{x["id"]:02d}.html').write_text(pose(x,t),encoding='utf-8')
    (V/'index.html').write_text(index(lines,ts,args.assemble),encoding='utf-8');(V/'STORYBOARD.md').write_text(storyboard(lines,ts,args.assemble),encoding='utf-8');(V/'scene_schedule.json').write_text(json.dumps(ts,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(frames=16,duration=ts[-1]['end'],snapshot_at=','.join(f'{t["start"]+t["duration"]*.9:.3f}' for t in ts))))
if __name__=='__main__':main()
