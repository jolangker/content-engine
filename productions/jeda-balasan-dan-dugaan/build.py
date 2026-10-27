"""Episode-specific phone, attribution branches, evidence and boundaries."""
from pathlib import Path
import argparse,json
import visuals as v
from visuals import path,line,circle,rect,group,actor,bubble,ribbon,C,I,A,S
P=Path(__file__).resolve().parent;V=P/'video'
def phone(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+rect(-150,-260,300,520,c,'none',42)+line(-38,-225,38,-225,c,5)+line(-40,225,40,225,c,5)+bubble(-108,-135,210,108,c)+'</g>'
def clock(x,y,r=75,c=I):return circle(x,y,r,c)+line(x,y,x,y-r*.6,c,4)+line(x,y,x+r*.5,y+r*.2,c,4)
def dash(d,c=I):return path(d,c,5,extra='stroke-dasharray="14 16"')
def question(x,y,c=I):return path(f'M{x-28} {y-25}Q{x+40} {y-75} {x+40} {y-20}Q{x+40} {y+5} {x} {y+20}V{y+45}',c,6)+circle(x,y+76,5,c,c)
DESIGNS=[
('A message with no reply','Close phone with a sent speech space and a visibly empty reply area; the clock advances attention toward an absent account.',['phone and sent space','message trace','clock','empty reply boundary']),
('An explanation is made','The observer sees a phone; a thought route reaches a separate open explanation space, leaving the partner distinct.',['observer','phone event','thought route','explanation space']),
('One event, different accounts','One phone branches toward a work context and toward a turned-away partner; dashed routes mark both as unconfirmed.',['single phone','work account','avoidance account','unconfirmed branches']),
('What the screen cannot show','An oversized phone has an empty reply space; the outline of another person remains outside the screen, beyond a boundary.',['close phone','empty reply space','partner outside screen','unresolved boundary']),
('Intention is inferred','The observer holds a message while a dashed route approaches the partner; a question remains where intentionality would be assumed.',['observer and phone','partner','inferred route','intention question']),
('From event to enduring pattern','Three calendar leaves appear one at a time; only the first has an observed message, the others remain empty before a bracket gathers them.',['one observed day','second empty day','third empty day','pattern bracket']),
('Cause and intentionality','The same message remains above two distinct inspection spaces: an activity clock and a question beside a partner; neither implies a measured cause.',['message','possible circumstance','intention judgment','separate inspection boundaries']),
('Uncertainty is not disproof','On charcoal, the observer keeps the message while a question route remains open beside the partner; no cancel mark invalidates it.',['observer and message','partner','open question','account retained']),
('Known and unknown details','A large inspection window surrounds the phone, while a separate question space waits alongside; evidence does not fill the unknown area.',['phone evidence','inspection window','unknown space','open information route']),
('A busy account is still an account','A work surface, document and clock appear within a dashed thought boundary; the observer stays outside that illustration.',['observer','work scene','clock','unconfirmed thought boundary']),
('Observation interpretation question','A phone on the left hands off to a separate thought space in the middle and then to a question on the right; the three retain clear spacing.',['observed phone','interpretation space','open question','stepwise route']),
('Ask for a possible time','Two organic participants have separate speech spaces; the sender offers a question toward a shared clock without pulling the recipient closer.',['pair','sender question','shared time','open route']),
('Answer and follow-through','A reply reaches the sender; beside the receiver a calendar marker and a continuous action route develop, keeping words and follow-through visible.',['pair','reply space','calendar agreement','follow-through trace']),
('Repeated impact still matters','On charcoal, repeated empty message spaces reach a waiting participant; an unresolved gap remains between them and the other person.',['waiting participant','second unanswered space','third unanswered space','unresolved distance']),
('A boundary remains','The original pair is present, separated by a clear boundary; a communication route reaches a negotiated opening and stops without erasing the line.',['pair','boundary','agreed opening','bounded communication']),
('Return to the observed event','Return to the first phone; one clear message remains, its inference sits in a separate speech space and an open route offers a final quiet check.',['original phone','observed message','separate explanation','open checking route']),
]
def art(n,dark):
    ink=C if dark else I
    if n==1:return [group(1,phone(500,990,1.15)),group(2,ribbon(385,920,205)),group(3,clock(825,650,70)),group(4,dash('M365 1120H635V1270H365Z',S))]
    if n==2:return [group(1,actor(240,1130,1.05)),group(2,phone(720,1190,.62)),group(3,path('M325 1020Q330 750 540 710',A,6)),group(4,bubble(490,590,360,180)+question(655,670))]
    if n==3:return [group(1,phone(505,690,.63)),group(2,rect(120,1080,290,165,I,S)+rect(165,955,180,130,I,C)+line(140,1260,140,1330)+line(390,1260,390,1330)),group(3,actor(775,1150,.95,A,True)+path('M660 1050Q625 1010 660 950',I,5)),group(4,dash('M470 900Q370 960 300 1000')+dash('M560 900Q685 950 720 1040',A))]
    if n==4:return [group(1,phone(360,980,1.08)),group(2,dash('M250 1040H465V1180H250Z',S)),group(3,actor(810,1010,.9,A,True)),group(4,dash('M625 650V1330',I)+question(800,700))]
    if n==5:return [group(1,actor(230,1140,.9)+phone(430,1200,.48)),group(2,actor(805,850,1.05,A,True)),group(3,dash('M410 1020Q440 750 670 790',A)),group(4,question(550,680))]
    if n==6:return [group(1,rect(115,620,350,300,I,C)+line(115,690,465,690)+phone(290,790,.35)),group(2,rect(425,865,350,245,I,C)+line(425,925,775,925)),group(3,rect(585,1160,315,220,I,C)+line(585,1210,900,1210)),group(4,path('M110 560H70V1430H915',A,6))]
    if n==7:return [group(1,phone(510,685,.52)),group(2,clock(270,1080,95)+line(160,1260,390,1260)),group(3,actor(765,1165,.88,A,True)+question(765,970)),group(4,path('M140 935V1320H415M620 935V1320H900',S,5))]
    if n==8:return [group(1,actor(245,1110,.95,ink)+phone(420,1260,.42,ink)),group(2,actor(800,1000,.95,A,True)),group(3,dash('M370 930Q480 730 700 840',S)+question(535,760,ink)),group(4,bubble(360,575,300,215,ink))]
    if n==9:return [group(1,phone(325,1020,.8)),group(2,path('M120 675H165M120 675V1375H165M495 675H540V1375H495',A,6)),group(3,bubble(645,680,250,240)+question(755,770)),group(4,dash('M550 1060Q730 1090 775 1000',S))]
    if n==10:return [group(1,actor(190,1230,.65)),group(2,rect(385,940,465,180,I,S)+rect(470,790,170,135,I,C)+line(420,1130,420,1220)+line(815,1130,815,1220)),group(3,clock(780,730,65)),group(4,dash('M350 625H900V1320H350Z')+question(615,1230))]
    if n==11:return [group(1,phone(230,825,.62)),group(2,bubble(420,870,270,200)+ribbon(450,960,160)),group(3,question(800,1220)),group(4,path('M340 800Q415 800 445 850M630 1130Q680 1200 720 1240',A,6))]
    if n==12:return [group(1,actor(245,1190,.95)+actor(810,1190,.95,A,True)),group(2,bubble(120,595,400,230)+question(290,690)),group(3,clock(740,750,90)),group(4,path('M365 1110Q520 970 705 1110',A,6))]
    if n==13:return [group(1,actor(245,1200,.85)+actor(810,1200,.85,A,True)),group(2,bubble(570,620,310,180,A)+ribbon(605,700,210,I)),group(3,rect(170,760,300,250,I,C)+line(170,825,470,825)+clock(320,920,65)),group(4,path('M350 1190Q530 1380 720 1190',A,6))]
    if n==14:return [group(1,actor(250,1200,.9,ink)+actor(820,1200,.65,A,True)),group(2,bubble(130,600,300,150,ink)),group(3,bubble(435,810,300,150,ink)),group(4,path('M360 1170H450M630 1170H730',S,5)+dash('M460 1170H620',ink)+bubble(580,1030,300,130,ink))]
    if n==15:return [group(1,actor(240,1130,.95)+actor(810,1130,.95,A,True)),group(2,path('M535 590V940M535 1120V1420',I,7)),group(3,path('M500 940H570M500 1120H570',S,5)),group(4,path('M350 1130Q420 1020 530 1020H705',A,6))]
    return [group(1,phone(330,1040,.87)),group(2,ribbon(235,980,185)),group(3,bubble(615,670,270,240)+question(735,760)),group(4,path('M550 1190Q735 1210 785 1020',A,6))]

v.DESIGNS=DESIGNS;v.art=art
schedule=v.schedule;pose=v.pose
def storyboard(lines,ts,animated):
    doc=f'''---
format: 1080x1920
duration: {ts[-1]['end']:.5f}s
message: Distinguish what happened from the explanation added to it; check information and preserve responsibility.
arc: message question → attribution → event and inference → uncertainty → ask → observe and keep boundaries
audience: Indonesian adults
mode: autonomous
---

# Jeda balasan dan dugaan — visual storyboard v1

Exactly 16 frames. Charcoal 08 (recognition is not disproof) and 14 (repeated impact remains); 14 cream. Static poses verified before audio/animation under delegated automation. Fixed canonical chrome; full captions y1550–1740. Key content x88–936/y230–1480. Dashed routes denote illustrative possibilities, not empirical effects. Registry queried organic conversation phone attribution caption; literal iMessage mockups, light leaks and decorative karaoke do not fit this flat board. Original episode-specific illustrations and plain captions inherit board assets, not a named effect. Sparse frozen material sounds and no BGM.

'''
    for x,t in zip(lines,ts):
        n=x['id'];title,idea,beats=DESIGNS[n-1];d=t['duration']
        doc+=f'''## Frame {n} — {x['title']}

- status: {'animated' if animated else 'built'}
- src: compositions/frames/f{n:02d}.html
- duration: {d:.5f}s
- start: {t['start']:.5f}s
- end: {t['end']:.5f}s
- poster: {d*.94:.5f}
- transition_in: cut
- scene: {title}
- voiceover: "{x['text']}"
- palette: {'dramatic' if x['dramatic'] else 'light'}
- emphasis: "{x['emphasis']}"
- reads: observed state (0–{d*.14:.2f}s); new detail ({d*.14:.2f}–{d*.43:.2f}s); account/response ({d*.43:.2f}–{d*.73:.2f}s); consequence ({d*.73:.2f}–{d:.2f}s)
- sound: {'intentional SFX silence' if n in (8,14,16) else 'narration; selected material cues only as listed in sound_design.json'}

Purpose/layout: {idea}
States: {beats[0]} already locatable → {beats[1]} at {d*.14:.2f}s → {beats[2]} at {d*.43:.2f}s → {beats[3]} at {d*.73:.2f}s. Each state changes the information or interaction; subtitle changes do not count. Preserve actor silhouettes, fixed chrome and caption clearance. Next frame develops the same scene's reasoning through a detail cut, spatial carry-over or dramatic inversion.
'''
        if x['dramatic']:doc+=f'\nDramatic line: "{x["text"]}". Reason: {"recognition does not invalidate an inference" if n==8 else "prevent uncertainty from excusing repeated impact"}. Invert ground, typography, captions and chrome together.\n'
        doc+='\n'
    return doc
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--assemble',action='store_true');a=ap.parse_args();lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));ts=schedule(lines)
    (V/'compositions/frames').mkdir(parents=True,exist_ok=True)
    if not a.assemble:
        for x,t in zip(lines,ts):(V/f'compositions/frames/f{x["id"]:02d}.html').write_text(pose(x,t),encoding='utf-8')
    (V/'index.html').write_text(v.index(lines,ts,a.assemble),encoding='utf-8');(V/'STORYBOARD.md').write_text(storyboard(lines,ts,a.assemble),encoding='utf-8');(V/'scene_schedule.json').write_text(json.dumps(ts,indent=2)+'\n',encoding='utf-8')
    (V/'SPEC.md').write_text('''GOAL: Check the information behind an account of an unanswered message, without erasing responsibility.
OUTPUT: HyperFrames, 1080x1920, 30fps, 16 meaningful scenes.
TIME: Initial 90s estimate; replace with measured native voice and acoustic-safe scene boundaries.
LOOK: Canvas #F3EDE3, ink #302B28, accent #A34F3F, sand #D8C8B5. Exactly two inversions, scenes 08 and 14. Newsreader 400 at 76–82px; DM Sans 500 captions 46px. Flat ink illustrations; no grain/shadows/blur. Fixed board chrome at canonical geometry.
OBJECTS: Organic faceless pair with distinct silhouettes; phone with rounded body/speaker/home bar and sent speech space; clock with hands; work desk and document; calendar leaves; dashed possible accounts; solid observed paths and boundaries.
MOTION: State 1 present at frame 0, developments near 14%, 43%, 73%; line traces power2.inOut 0.6–0.9s, object placement power3.out 0.6–0.9s, responsive settlement 0.6–0.9s. No idle loops. Hold after the consequence.
SHOTS: See STORYBOARD.md for each shot, exact range, reading window, sound and handoff. Vary close phone, wide interaction, calendar detail, branches, inspection and bounded exchange.
BANNED: Neon/glow, gradients, glass cards, decorative particles, B-roll, diagnostic labels, gender-coded colors, inferred motives shown as fact, motion on landed titles, identical entrances, infinite loops. Cream/serif/chrome are explicit approved board identity exceptions.
QA: All 16 landed frames; intermediate information beats; both inversions; 360px phone sheet; fixed captions/chrome; final MP4 decoded frames; full decode; acoustic seams; actual SFX presence; duration and hashes. Sound measured, not heard unless playback is available.
''',encoding='utf-8')
    print(json.dumps(dict(frames=16,duration=ts[-1]['end'],snapshot_at=','.join(f'{t["start"]+t["duration"]*.94:.5f}' for t in ts))))
if __name__=='__main__':main()
