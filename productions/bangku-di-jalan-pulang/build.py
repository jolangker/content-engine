"""Sixteen episode-specific park compositions using the frozen board renderer."""
from pathlib import Path
import argparse,json,shutil
import visuals as v
from visuals import path,line,circle,rect,group,actor,bubble,ribbon,C,I,A,S
P=Path(__file__).resolve().parent;V=P/'video'
def bench(x=515,y=1110,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+rect(-295,-120,590,46,c,S,8)+rect(-295,-53,590,46,c,S,8)+path('M-300 50H300L320 80H-320ZM-245 80L-260 195M245 80L260 195M-270 -145V50M270 -145V50',c,6)+'</g>'
def tree(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M0 75V240M0 155L-45 115M0 120L40 80',c,5)+path('M-70 65C-150 40 -118 -60 -65 -65C-90 -150 35 -170 65 -100C145 -100 155 10 90 40C90 105 -10 120 -70 65Z',c,5)+'</g>'
def calendar(x=520,y=850,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+rect(-130,-135,260,265,c,'none',14)+line(-130,-65,130,-65,c)+path('M-70 -160V-105M70 -160V-105',c,6)+''.join(circle(xx,yy,8,c,c,1) for xx,yy in [(-65,0),(0,0),(65,0),(-65,60),(0,60),(65,60)])+'</g>'
def feet(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-29 -35C-50 -70 -75 -35 -64 -5L-36 38Q-10 45 -15 18ZM32 -65C12 -94 -12 -58 2 -30L32 9Q57 15 48 -10Z',c,3)+'</g>'
def loop(x=515,y=1020,rx=345,ry=275,c=A):
    return path(f'M{x-rx} {y}C{x-rx} {y-ry*1.35} {x+rx} {y-ry*1.35} {x+rx} {y}C{x+rx} {y+ry*1.35} {x-rx} {y+ry*1.35} {x-rx} {y}',c,6)
def pair(y=900,k=.90,c=I):return actor(340,y,k,c)+actor(690,y,k,A,True)
def route(c=I):return path('M155 1430Q300 1330 350 1260M680 1270Q780 1340 900 1400',c,5)
def door(x,y,k=1,c=I):return f'<g transform="translate({x} {y}) scale({k})">'+path('M-55 75V-95H55V75M-75 75H75',c,5)+circle(30,0,4,c,c,1)+'</g>'
def bubble_right(x,y,w,h,c=I):return path(f'M{x+25} {y}H{x+w-25}Q{x+w} {y} {x+w} {y+25}V{y+h-25}Q{x+w} {y+h} {x+w-25} {y+h}H{x+w-60}L{x+w-50} {y+h+60}L{x+w-100} {y+h}H{x+25}Q{x} {y+h} {x} {y+h-25}V{y+25}Q{x} {y} {x+25} {y}Z',c,5)
DESIGNS=[
('A Friday stop','Wide park entrance: two distinct participants arrive at a slatted bench beside a tree.',['bench and tree','viewer arrives from left','partner arrives from right','two foot trails converge']),
('Repeated joint activity','A large calendar and miniature bench pair connect repeated days to the same shared action.',['calendar','bench at lower center','viewer and partner','three repeated day marks']),
('Symbolic meaning','The same seated pair becomes surrounded by a deliberate shared enclosure.',['bench','viewer seated','partner seated','one outline holds the shared scene']),
('Time for us','Close viewer with an audible personal interpretation; the speech space contains the shared bench.',['viewer','viewer speech space','miniature seated pair and bench','personal meaning trace']),
('Stop and accompany','Bench close-up without a magical change: two partners remain beside each other.',['large slatted bench','viewer sits','partner sits','a short shared trace settles']),
('A practical rest','Partner foreground with a doorway and onward route; the viewer remains in the park.',['partner and bench','partner speech space','home doorway inside speech space','onward foot trail']),
('Same action, meanings apart','Two distinct speech spaces surround the same bench: pair-time versus a homeward stop.',['bench and pair','viewer speech outline','partner speech outline','two separate interior pictograms']),
('Special for whom','Dark close-up keeps the viewer and partner distinct; an open enclosure has not yet become shared.',['two participants','viewer-side arc','partner-side open arc','small bench between the arcs']),
('Association and agreement','Two speech spaces point to the same small bench without a causal graph or outcome meter.',['two participants','first speech space','second speech space','matching bench symbols in both spaces']),
('No promised outcome','Dark park view leaves the onward route open: one meaningful place cannot measure a whole relationship.',['bench and pair','shared local outline','open onward path','distant home without outcome symbol']),
('State your meaning','Viewer foreground tells partner why this place matters; speaker ownership is visually stable.',['viewer and partner','viewer speech space','bench detail inside speech space','shared-time trace reaches inward']),
('Ask their meaning','Partner now has a large empty reply space; the viewer leaves room instead of filling it in.',['pair with bench','viewer question route','partner reply space','open path from viewer to reply']),
('Listen and compare','Two speech spaces retain separate boundaries while their connection develops at the shared bench.',['two participants','viewer speech space','partner speech space','bench and mutually reaching trace']),
('Practical is allowed','Object detail: bench, doorway and feet remain practical without being stamped as a ritual.',['bench detail','home doorway','viewer foot trail','partner foot trail onward']),
('Meaning shared','Return to opening wide park shot with a shared enclosure and two convergent routes.',['bench and tree','viewer and partner','two foot trails','one shared enclosure']),
('Quiet way home','Close quiet ending: both identities remain, the bench has a place within an open homeward route.',['bench','two participants','onward route','small shared trace, then hold']),
]
def art(n,dark):
    c=C if dark else I
    if n==1:return [group(1,bench()+tree(830,675,.7,c)),group(2,actor(340,900,.9,c)),group(3,actor(690,900,.9,A,True)),group(4,feet(240,1360,.65,c)+feet(805,1340,.65,A))]
    if n==2:return [group(1,calendar(515,780,.95,c)),group(2,bench(515,1210,.68,c)),group(3,pair(1070,.65,c)),group(4,path('M310 980H370M485 980H545M660 980H720',A,8))]
    if n==3:return [group(1,bench(c=c)),group(2,actor(340,900,.9,c)),group(3,actor(690,900,.9,A,True)),group(4,loop(515,1000,355,275,A))]
    if n==4:return [group(1,actor(280,1250,1.3,c)),group(2,bubble(150,630,690,390,c)),group(3,bench(550,825,.43,c)+actor(475,733,.4,c)+actor(625,733,.4,A,True)),group(4,ribbon(380,1100,350,A))]
    if n==5:return [group(1,bench(515,1080,1.15,c)),group(2,actor(320,835,1.12,c)),group(3,actor(720,835,1.12,A,True)),group(4,ribbon(435,1015,160,A))]
    if n==6:return [group(1,actor(740,1240,1.2,A,True)+bench(360,1210,.45,c)+actor(360,1118,.4,c)),group(2,bubble_right(195,640,650,345,c)),group(3,door(525,805,.85,c)),group(4,feet(430,1060,.8,A)+path('M460 1100Q525 1050 585 1035',c,5))]
    if n==7:return [group(1,bench(515,1260,.8,c)+pair(1090,.73,c)),group(2,bubble(130,640,350,220,c)),group(3,bubble(560,690,350,220,c)),group(4,actor(250,735,.30,c)+actor(365,735,.30,A,True)+door(735,805,.6,c))]
    if n==8:return [group(1,actor(270,1030,1.15,c)+actor(770,1030,1.15,A,True)),group(2,path('M410 810C240 685 130 830 150 1010',c,7)),group(3,path('M655 810C820 685 905 820 900 1000',c,7)),group(4,bench(520,1275,.63,c))]
    if n==9:return [group(1,pair(1270,.95,c)),group(2,bubble(135,650,350,285,c)),group(3,bubble(560,745,350,285,c)),group(4,bench(310,805,.35,c)+bench(735,900,.35,c))]
    if n==10:return [group(1,bench(515,1090,.9,c)+pair(900,.82,c)),group(2,loop(515,995,320,250,c)),group(3,path('M155 1350Q300 1260 395 1330Q580 1470 765 1350',c,5)),group(4,door(845,1260,.67,c))]
    if n==11:return [group(1,actor(250,1260,1.15,c)+actor(800,1260,.85,A,True)),group(2,bubble(140,645,655,330,c)),group(3,bench(475,820,.49,c)),group(4,ribbon(365,1115,310,A))]
    if n==12:return [group(1,bench(515,1270,.8,c)+pair(1090,.78,c)),group(2,path('M315 915Q375 715 535 705',c,6)),group(3,bubble(555,640,340,270,c)),group(4,path('M430 950Q490 880 550 865',A,6))]
    if n==13:return [group(1,pair(1230,.97,c)),group(2,bubble(130,660,350,265,c)),group(3,bubble(565,760,330,265,c)),group(4,bench(515,1100,.40,c)+path('M380 1000Q435 1080 490 1085M650 1080Q600 1110 550 1085',A,6))]
    if n==14:return [group(1,bench(350,920,.65,c)),group(2,door(790,1230,1,c)),group(3,feet(345,1180,.95,c)),group(4,feet(580,1300,.95,A)+path('M420 1250Q520 1370 700 1370',c,5))]
    if n==15:return [group(1,bench()+tree(830,675,.7,c)),group(2,pair(900,.9,c)),group(3,feet(240,1360,.65,c)+feet(805,1340,.65,A)),group(4,loop(515,1000,355,270,A))]
    return [group(1,bench(515,1110,1.05,c)),group(2,pair(890,1,c)),group(3,path('M150 1405Q270 1320 390 1390M680 1390Q800 1300 900 1370',c,5)),group(4,ribbon(440,1030,150,A))]
v.DESIGNS=DESIGNS;v.art=art
schedule=v.schedule;pose=v.pose
def storyboard(lines,ts,animated):
    doc=f'''---
format: 1080x1920
duration: {ts[-1]['end']:.8f}s
message: Repetition becomes a relationship ritual through shared symbolic meaning.
arc: familiar park stop → concept → two meanings → evidence limits → speak, ask and listen → return
audience: Indonesian adults
mode: autonomous
---

# Bangku di jalan pulang — storyboard v1

Board editorial v1.4 / visual v1.2. Exactly 16 meaningful compositions, fourteen cream and charcoal 08/10. Distinct irregular ink viewer (left) and rounded brick partner (right); identities and fixed chrome persist through inversion. Slatted park bench, tree, calendar, doorway and shoe outlines supply context. Speech spaces represent explicitly fictional perspectives; loops show scope/shared meaning, not causal measurements. Original drawings inherit the approved board language. Caption band y1550–1740; content x88–936/y230–1480. No supporting paragraphs or B-roll.

Registry query minimal captions organic line drawing dialogue returned generic caption and line-loader components. None preserves this established board composition better than its renderer; reused board caption typography and seekable stroke principles. Narration: one native-speed ElevenLabs recording after static storyboard verification. BGM none: leave different possible feelings open. Sparse board material cues; dark turns/final hold intentionally quiet.

'''
    for x,t in zip(lines,ts):
        n=x['id'];title,idea,beats=DESIGNS[n-1];d=t['duration']
        doc+=f'''## Frame {n} — {x['title']}

- status: {'animated' if animated else 'built'}
- src: compositions/frames/f{n:02d}.html
- duration: {d:.8f}s
- start: {t['start']:.8f}s
- end: {t['end']:.8f}s
- poster: {d*.94:.8f}
- transition_in: cut
- scene: {title}
- voiceover: "{x['text']}"
- palette: {'dramatic' if x['dramatic'] else 'light'}
- emphasis: "{x['emphasis']}"
- reads: context (0–{d*.14:.2f}s); action ({d*.14:.2f}–{d*.43:.2f}s); response ({d*.43:.2f}–{d*.73:.2f}s); consequence ({d*.73:.2f}–{d:.2f}s)
- sound: {'narration and intentional SFX silence' if n in (8,10,16) else 'narration; selected cues in sound_design.json'}

Purpose/layout: {idea}
Starting state: {beats[0]}. Internal semantic changes: {beats[1]} at {d*.14:.2f}s → {beats[2]} at {d*.43:.2f}s → {beats[3]} at {d*.73:.2f}s. Final state: all original illustrated details plus optional short emphasis and stationary chrome. Continuity: same viewer/partner contours and positions; same slatted bench; variable close, wide, object and speech framing. Caption replacements do not count as action beats.
'''
        if x['dramatic']:doc+=f'\nDramatic line: "{x["text"]}". Reason: '+('recognition that personal significance is not automatically shared' if n==8 else 'a clear limit on interpreting association as a guaranteed benefit')+'. Entire background, captions, text and chrome invert together.\n'
        doc+='\n'
    return doc
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--assemble',action='store_true');args=ap.parse_args();lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));ts=schedule(lines)
    (V/'compositions/frames').mkdir(parents=True,exist_ok=True)
    if not args.assemble:
        for x,t in zip(lines,ts):(V/f'compositions/frames/f{x["id"]:02d}.html').write_text(pose(x,t),encoding='utf-8')
    (V/'index.html').write_text(v.index(lines,ts,args.assemble),encoding='utf-8');(V/'STORYBOARD.md').write_text(storyboard(lines,ts,args.assemble),encoding='utf-8');(V/'scene_schedule.json').write_text(json.dumps(ts,indent=2)+'\n',encoding='utf-8')
    (V/'SPEC.md').write_text('''GOAL: Explain repeated joint action versus shared symbolic meaning through a fictional Friday bench stop, then invite the viewer to tell and ask without assigning the partner a feeling.
OUTPUT: 1080x1920/30fps, 16 scenes, 85–95s target, Instagram Reel. Automation through queue, delegated pre-render authorization, no human approval claimed.
LOOK: Frozen board visual v1.2: cream #F3EDE3, ink #302B28, brick #A34F3F, sand #D8C8B5. Newsreader 76–82px, DM Sans captions 46px. Fixed header/frame number/footer, two dark scenes 08/10. Local fonts and licenses. Exact series geometry takes precedence over generic platform-safe defaults.
OBJECTS: Original faceless irregular viewer and differently contoured partner; slatted bench with legs, organic tree, bound calendar with repeated day marks, shoe outlines, home doorway, speech spaces. Shared enclosure is interpretive illustration, no data metric.
MOTION: Context at cut; scene-specific semantic changes at 14/43/73%, seekable paths 0.6–0.9s power2.inOut and arrivals/settles 0.6–0.9s power3.out. Readable final hold. No infinite drift. Native-speed single narration, integer-frame acoustic cuts, full spoken captions.
SHOTS: park wide; calendar/bench; shared enclosure; viewer meaning; seated close-up; partner practical perspective; distinct speech spaces; dark unshared meaning; matching symbols; dark evidence limit; viewer speech; partner response room; listening; practical journey; opening reprise; quiet bench.
SOUND: Narration plus sparse frozen dry contact/air/connection cues. No BGM: keep the answer open and the reflective pause clear. No effects on every cut. Final hold silent.
BANNED: stock footage, gradients, particles, diagnostic labels, gender/blame coding, presumed partner motives, causal satisfaction promises, numerical outcome gauges, supporting paragraphs, notification pings, identical title entrances, motion unrelated to meaning.
QA: Complete static storyboard before synthesis; narration-only POV; 16/2 palette coverage; semantic motion phases; phone-size sheets; forward/reverse seek; exact cut frames; waveform boundaries; full decoded H264/AAC export; SFX matching; hash-bound receipts. State perceptual listening limits honestly.
''',encoding='utf-8')
    (V/'STORYLINES.md').write_text('''# Storyline decision

1. Selected: Friday park stop, wide/object/dialogue views, open a specific question and return to the same bench with clearer shared meaning. Objects establish the first second; partner meaning remains an inquiry. Strongest narrative continuity.
2. One continuous overhead park path: two footprints converge every week and symbolic enclosures change. Elegant but weak for the board's sixteen distinct meaningful compositions.
3. Partner's replay from homeward rest to the viewer's interpretation: bold viewpoint change but higher risk of presuming unknown motives and shifting lo midway.

Devices considered: park approach, calendar repetition, two speech spaces, fixed overhead path, a bench object monologue. Agent selected 1 under immediate automation. Chosen hook, approved board and POV contract resolve the story/look; no extra human pitch gate.
''',encoding='utf-8')
    print(json.dumps(dict(scenes=16,duration=ts[-1]['end'],animated=args.assemble)))
if __name__=='__main__':main()
