"""Episode-specific waiting table, departure, ownership and repair illustrations."""
from pathlib import Path
import argparse, json
import visuals as v
from visuals import path,line,circle,rect,group,actor,bubble,ribbon,plate,C,I,A,S
P=Path(__file__).resolve().parent;V=P/'video'

def clock(x,y,r=85,c=I,early=False):
    return circle(x,y,r,c)+line(x,y,x,y-r*.62,c,5)+line(x,y,x+r*.55,y+(0 if early else r*.23),c,5)+circle(x,y,5,c,c)
def table(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-230 -90Q0 -150 230 -90L230 95Q0 155 -230 95Z',c,5,S)+line(-160,130,-175,210,c)+line(160,130,175,210,c)+'</g>'
def door(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-110 160V-160H110V160M-140 160H140',c,6)+circle(60,10,7,c,c)+'</g>'
def work(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+rect(-115,-80,230,155,c,S,10)+path('M-115 75L-155 112H155L115 75',c,5)+line(-60,-30,60,-30,c,4)+line(-60,15,25,15,c,4)+'</g>'
def calendar(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+rect(-140,-170,280,340,c,'none',15)+line(-140,-90,140,-90,c)+line(-70,-205,-70,-135,c)+line(70,-205,70,-135,c)+line(-90,-20,85,-20,S,4)+line(-90,50,85,50,S,4)+line(-90,120,45,120,S,4)+'</g>'
def paper(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+rect(-180,-230,360,460,c,'none',10)+line(-110,-145,105,-145,c,5)+line(-110,-70,60,-70,c,4)+line(-110,10,100,10,S,4)+line(-110,85,85,85,S,4)+line(-110,160,40,160,S,4)+'</g>'
def question(x,y,c=I):
    return path(f'M{x-24} {y-23}Q{x+36} {y-65} {x+36} {y-18}Q{x+36} {y+7} {x} {y+20}V{y+38}',c,6)+circle(x,y+65,5,c,c)
def arrow(d,x,y,c=A):return path(d,c,6)+path(f'M{x-18} {y-16}L{x} {y}L{x-20} {y+14}',c,6)

DESIGNS=[
('An explanation over a waiting table','Wide pair and table; the explanation travels out while the waiting clock remains outside its speech space.',['waiting pair and table','explanation space','waiting clock','gap in reply route']),
('Responsibility inside the apology','Close speech space receives an action trace from its speaker; the receiving space remains open.',['speaker','large apology space','specific action trace','open receiving edge']),
('Trace the action to its author','Large speaker and clock are connected by a route that starts at that speaker, separate from the work context.',['speaker','late clock','own action route','context off to one side']),
('The meal has waited','Top-down table and two plates, one participant already present; the other arrives as a visible change, then the clock is noticed.',['table and waiting participant','two untouched plates','arriving participant','elapsed clock']),
('An explanation can be true','Large speech bubble holds a work laptop; the consequence sits outside it and the action route is still unfinished.',['large explanation bubble','busy work','waiting table consequence','unfinished action route']),
('Name the late departure','Door and clock beside the departing participant: a specific departure route replaces a generic explanation.',['departure door','clock','departing participant','owned departure route']),
('Two components in the research','A large research page anchors two separate speech/action spaces, describing components rather than numerical effects.',['research page','responsibility space','repair space','two distinct action traces']),
('A workplace scenario has limits','A workplace laptop on the research page remains separate from the couple below; no arrow promises acceptance.',['research page','workplace laptop','separate couple','visible gap between contexts']),
('What did I acknowledge','Charcoal: speaker and waiting clock are locatable; an incomplete route leaves the owned action absent.',['speaker continuity','waiting clock','incomplete route','empty response gap']),
('A specific apology reaches the scene','Pair at the table, an apology space and a route to the earlier clock make the admitted action specific.',['pair and table','apology space','voice to waiting partner','route to earlier clock']),
('Ask what needs rearranging','A large tabletop receives a question; a meal setting shifts to make the consequence and potential adjustment concrete.',['table and plate','question space','second meal setting','proposed rearrangement route']),
('Plan the next departure','A calendar, departure door and earlier clock carry the future plan; an open communication route leaves room for changed timing.',['next occasion calendar','departure door','earlier clock','update route']),
('Follow through on the plan','The same departure becomes an action: participant moves toward the door and the route reaches the agreed clock.',['departure door','earlier clock','moving participant','completed departure route']),
('A response may need time','Charcoal: the same pair retain distinct positions; an open receiving space and clock allow a response without a forced connection.',['pair continuity','receiving space','time to respond','open boundary']),
('Answer the unfinished apology','Close apology space now includes an action trace and a next-step calendar, answering what the opening omitted.',['opening apology space','owned action clock','next-step calendar','action-to-next-step route']),
('The words have a concrete action','Return to the table and pair; a voiced acknowledgment links to the departure plan while the receiver keeps an open reply space.',['opening table and pair','acknowledgment space','departure plan','open reply route']),
]

def art(n,dark):
    ink=C if dark else I
    if n==1:return [group(1,actor(200,1160,.9)+actor(830,1160,.9,A,True)+table(510,1170,.67)),group(2,bubble(150,610,430,185)+ribbon(195,700,310)),group(3,clock(765,870,100)),group(4,path('M365 1010Q495 900 575 980',A,6)+path('M625 1005Q665 1010 705 1050',S,5))]
    if n==2:return [group(1,actor(220,1250,.9)),group(2,bubble(165,645,700,385)),group(3,clock(510,830,87)+path('M300 1165Q335 1020 425 915',A,6)),group(4,path('M690 1120Q800 1060 895 1150',S,5))]
    if n==3:return [group(1,actor(225,1120,1.1)),group(2,clock(755,880,120)),group(3,arrow('M335 1090Q550 1100 665 955',665,955)),group(4,work(750,1280,.6))]
    if n==4:return [group(1,table(510,1000,1.2)+actor(865,1080,.7,A,True)),group(2,plate(370,960,78)+plate(670,1085,78)),group(3,actor(155,1100,.68)),group(4,clock(780,670,92))]
    if n==5:return [group(1,bubble(150,605,680,340)),group(2,work(475,775,1.1)),group(3,table(565,1250,.8)+clock(800,1100,65)),group(4,path('M290 990Q300 1140 375 1190',A,6)+path('M420 1210L465 1225',S,5))]
    if n==6:return [group(1,door(725,1000,1.45)),group(2,clock(290,740,110)),group(3,actor(320,1240,.95)),group(4,arrow('M425 1230Q555 1180 640 1080',640,1080))]
    if n==7:return [group(1,paper(490,1000,1.4)),group(2,bubble(130,660,350,185)+ribbon(170,755,235)),group(3,bubble(540,1120,350,185,A)+calendar(710,1205,.28)),group(4,path('M300 855V925M710 1010V1100',A,5))]
    if n==8:return [group(1,paper(510,825,1)),group(2,work(510,825,.8)),group(3,actor(275,1280,.82)+actor(765,1280,.82,A,True)),group(4,line(145,1120,410,1120,S,5)+line(620,1120,885,1120,S,5))]
    if n==9:return [group(1,actor(245,1160,1.1,ink)),group(2,clock(775,775,120,ink)),group(3,path('M365 1115Q500 960 575 1010',S,6)),group(4,bubble(560,1145,325,160,ink))]
    if n==10:return [group(1,actor(190,1210,.85)+actor(845,1210,.85,A,True)+table(520,1220,.65)),group(2,bubble(130,610,420,190)),group(3,ribbon(180,705,300)+path('M430 835Q610 860 750 1055',A,6)),group(4,clock(780,730,90)+path('M540 705H660',I,5))]
    if n==11:return [group(1,table(510,1110,1.35)+plate(345,1055,90)),group(2,bubble(200,620,530,185)+question(455,690)),group(3,plate(700,1150,90)),group(4,path('M675 1000Q810 970 850 1055',A,6))]
    if n==12:return [group(1,calendar(285,1010,1.05)),group(2,door(780,1080,.9)),group(3,clock(650,740,95,early=True)),group(4,path('M430 1210Q575 1300 710 1190',A,6)+bubble(510,1320,310,100))]
    if n==13:return [group(1,door(755,1000,1.45)),group(2,clock(290,740,110,early=True)),group(3,actor(465,1190,.95)),group(4,arrow('M365 1290Q610 1320 670 1110',670,1110))]
    if n==14:return [group(1,actor(230,1200,1,ink)+actor(825,1200,1,A,True)),group(2,bubble(560,620,340,210,ink)),group(3,clock(500,990,86,ink)),group(4,path('M120 1420H390M650 1420H920',S,5))]
    if n==15:return [group(1,bubble(135,625,740,360)),group(2,clock(340,795,85)),group(3,calendar(710,1200,.64)),group(4,arrow('M440 885Q565 965 650 1070',650,1070))]
    return [group(1,actor(195,1215,.85)+actor(840,1215,.85,A,True)+table(515,1225,.68)),group(2,bubble(130,610,405,180)+ribbon(170,695,285)),group(3,door(765,840,.65)+clock(625,770,58)),group(4,path('M450 825Q560 965 660 945',A,6)+path('M660 1105Q740 1040 845 1060',S,5))]

v.DESIGNS=DESIGNS;v.art=art
schedule=v.schedule;pose=v.pose

def storyboard(lines,ts,animated):
    doc=f'''---
format: 1080x1920
duration: {ts[-1]['end']:.8f}s
message: Name the action you own and offer a repair you can follow through on; acceptance is not guaranteed.
arc: unfinished apology → responsibility → waiting scene → research limits → specific apology → repair → room for response
audience: Indonesian adults
mode: autonomous
---

# Maaf yang menyebut tindakan — visual storyboard v1

Sixteen meaningful compositions; charcoal 09/14, fourteen cream. Board editorial v1.3/visual v1.2. Fixed chrome and local Newsreader/DM Sans. Content x88–936/y230–1480; captions y1550–1740. Static storyboard verification precedes synthesis and animation. Narration and dialogue are fictional illustrations; research boundaries are in ../SOURCES.md. The registry query organic conversation apology full captions produced no matching reusable board illustration; retain the canonical restrained caption treatment and original narrative drawings. No BGM; selected frozen material cues, no automatic transition effects.

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
- reads: initial state (0–{d*.14:.2f}s); context ({d*.14:.2f}–{d*.43:.2f}s); response ({d*.43:.2f}–{d*.73:.2f}s); consequence ({d*.73:.2f}–{d:.2f}s)
- sound: {'intentional SFX silence' if n in (8,9,14,16) else 'narration; selected cues in sound_design.json'}

Purpose/layout: {idea}
States: {beats[0]} at cut → {beats[1]} at {d*.14:.2f}s → {beats[2]} at {d*.43:.2f}s → {beats[3]} at {d*.73:.2f}s. Every change carries the scene's action or distinction; subtitle changes do not count. Start the next shot through its common clock, table, speech space or departure object, changing scale and viewpoint. Chrome and emphasis copy stay stationary. Hard detail cuts and two full-frame palette turns follow this board's illustrated conversation grammar rather than generic promotional transitions.
'''
        if x['dramatic']:doc+=f'\nDramatic line: "{x["text"]}". Reason: '+('the explanation leaves ownership unspecified' if n==9 else 'the receiver retains time and freedom to respond')+'. Invert ground, main text, captions and chrome together; preserve actor identity.\n'
        doc+='\n'
    return doc

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--assemble',action='store_true');a=ap.parse_args();lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));ts=schedule(lines)
    (V/'compositions/frames').mkdir(parents=True,exist_ok=True)
    if not a.assemble:
        for x,t in zip(lines,ts):(V/f'compositions/frames/f{x["id"]:02d}.html').write_text(pose(x,t),encoding='utf-8')
    (V/'index.html').write_text(v.index(lines,ts,a.assemble),encoding='utf-8');(V/'STORYBOARD.md').write_text(storyboard(lines,ts,a.assemble),encoding='utf-8');(V/'scene_schedule.json').write_text(json.dumps(ts,indent=2)+'\n',encoding='utf-8')
    (V/'SPEC.md').write_text('''GOAL: Distinguish explaining circumstances from naming the action one owns; offer concrete repair without demanding forgiveness.
OUTPUT: HyperFrames 1080x1920, 30fps, sixteen meaningful scenes.
TIME: 90s estimate; final native-speed narration, editorial quiet and integer-frame anchors replace estimates.
LOOK: Ground #F3EDE3; ink #302B28; accent #A34F3F; sand #D8C8B5. Exactly two charcoal scenes 09/14. Newsreader 400 76–82px, DM Sans 500 46px captions. Canonical fixed header/footer. Flat ink illustration, no shadows/blur/grain.
OBJECTS: Distinct organic faceless pair; table with legs, plates and cutlery; analog clock; door with jamb/knob; laptop with hinge/keyboard; bound calendar; research sheet; voice spaces and action traces. No B-roll or diagnostic/gender colors.
MOTION: Initial meaningful state at cut, three semantic developments around 14%, 43%, 73%. Drawn trace 0.6–0.9s power2.inOut; responsive arrival 0.6–0.9s power3.out. Actual arriving/departing actor movement in 04/13. No idle loops; stationary titles; final quiet hold.
SHOTS: STORYBOARD.md defines all shot ranges, purposes, scale, internal states and sound. Wide waiting pair → speech close-up → owned action → overhead table → work context → departure → study → study limit → missing ownership → specific apology → rearranged meal → future departure → follow-through → time to respond → answer → opening revisited.
BANNED: Generic card grids, background particles, gradients, neon, mock diagnostic claims, forced acceptance, identical slide-ups, drifting copy, random motion. Approved cream/serif/series numbering are board identity exceptions. No implied causal outcome from illustrative routes. Do not hide absence of responsibility by color-coded blame.
QA: Complete storyboard before synthesis; phone readability; exact two inversions; stationary chrome; actual meaningful internal motion; seek/reverse seek; all fifteen acoustic seams; caption word coverage; sparse placed cues; full decode; encoded visual seams; loudness and limits. Sound measured unless perceptual playback is available.
''',encoding='utf-8')
    print(json.dumps(dict(frames=16,duration=ts[-1]['end'])))
if __name__=='__main__':main()
