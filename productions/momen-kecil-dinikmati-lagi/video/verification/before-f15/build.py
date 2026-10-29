"""Original kitchen-memory scenes within the approved Ruang di Antara grammar."""
from pathlib import Path
import argparse,json
import visuals as v
from visuals import path,line,circle,rect,group,actor,bubble,ribbon,C,I,A,S
P=Path(__file__).resolve().parent;V=P/'video'

def mug(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-75 -65H65V65Q-5 110 -75 65Z',c,5)+path('M65 -42Q145 -60 135 15Q125 55 65 40',c,5)+path('M-70 -65Q-5 -90 65 -65',c,4)+'</g>'
def steam(x,y,k=1,c=A):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-30 0C-65 -30 0 -45 -25 -90M25 -15C-5 -45 65 -60 35 -110',c,4)+'</g>'
def kettle(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-78 -48Q-115 10 -90 90Q0 128 90 90Q115 10 78 -48Z',c,5,S)+path('M-65 -48Q0 -80 65 -48M-90 -10L-160 -85L-125 28L-100 40M78 -25Q175 -65 145 55L95 68M-15 -67V-95H15V-67',c,5)+'</g>'
def table(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-260 -50Q0 -100 260 -50V75Q0 130 -260 75Z',c,5)+line(-200,100,-210,235,c)+line(200,100,210,235,c)+'</g>'
def chair(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-85 -170Q0 -205 85 -170V20H-85ZM-85 20H105L120 65H-90ZM-65 65L-85 190M90 65L115 190',c,5)+'</g>'
def door(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-110 170V-170H110V170M-140 170H140',c,6)+circle(60,10,7,c,c)+'</g>'
def window(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+rect(-120,-160,240,320,c,'none',5)+line(0,-160,0,160,c)+line(-120,-20,120,-20,c)+circle(65,-95,25,c,S)+'</g>'
def memory(x,y,w=720,h=480,c=I):
    return path(f'M{x+80} {y}H{x+w-80}Q{x+w} {y} {x+w} {y+80}V{y+h-80}Q{x+w} {y+h} {x+w-80} {y+h}H{x+80}Q{x} {y+h} {x} {y+h-80}V{y+80}Q{x} {y} {x+80} {y}Z',c,4)+circle(x+95,y+h+38,17,c,w=4)+circle(x+65,y+h+80,8,c,w=3)
def pair(x,y,k=1,c=I):return actor(x-180*k,y,k*.68,c)+actor(x+180*k,y,k*.68,A,True)

DESIGNS=[
('Two cups in an ordinary kitchen','Wide pair and kitchen table; two cups locate an unremarkable shared evening.',['pair and table at cut','first cup','second cup','steam and kitchen window']),
('A specific memory becomes the subject','Close remembered pair inside an unmistakable thought bubble; a foreground thinker grounds the memory.',['foreground participant','large memory outline','remembered pair','shared cups']),
('Attention connects observer to memory','Large thought-space above a recalling participant, with a deliberate attention route to the remembered pair.',['recalling participant','thought space','remembered pair','attention route']),
('Arriving home and making tea','Door at left, partner at counter; the arriving participant crosses into a tea-making context.',['door and counter','kettle','arriving participant','partner and waiting cup']),
('Sensory details on a tabletop','Top-down close view of two cups; kettle, pouring stream and steam develop concrete remembered detail.',['first cup and tabletop','kettle','second cup','water stream and steam']),
('Stay with one remembered detail','A close mug in a thought space is revisited by the recalling participant; detail receives attention.',['memory outline and cup','steam detail','foreground participant','attention trace to cup']),
('Where is the closeness in the scene','Two chairs at a kitchen table; the pair and two cups reveal shared presence.',['chairs and table','first participant','second participant','cups between them']),
('I felt accompanied','Charcoal intimate pair at a table; a shared cup detail and gentle connection trace express this speaker’s felt meaning.',['locatable pair','table','two cups','subjective connection trace']),
('One memory and its own meaning','Foreground speaker remains outside one distinct remembered vignette; the memory is specific rather than a global relationship verdict.',['foreground participant','single thought outline','remembered cups and pair','attention route']),
('A memory does not close an open issue','Charcoal: remembered tea remains inside its thought space while a separate unfinished conversation stays open below.',['remembered cup','memory outline','separate participants','unfinished reply space']),
('Choose a particular evening','A foreground participant attends to one clear kitchen vignette instead of a generic label.',['participant','single memory outline','kitchen window and table','two cups and pair']),
('Place, action, personal meaning','Kitchen close view: window locates the evening, kettle and cups establish the action, pair establish personal context.',['evening window','table and cup','kettle and second cup','pair at the table']),
('An optional shared sentence','One participant speaks toward the other; the speech space holds an image of the shared tea.',['speaker and receiver','speech space','remembered tea cups','voice ribbon reaches toward receiver']),
('No matching feeling is required','Two distinct thought spaces remain separate; one holds the speaker’s cup memory and the other stays open.',['pair','speaker thought space','cup memory','open receiving thought space']),
('Return to the opening evening','Return to the kitchen from the opening with an observer now noticing a concrete detail.',['opening pair and table','two cups','remembering observer','attention trace']),
('Two cups, one evening','Large two-cup close-up with a small pair behind; steam settles into the final quiet question.',['first cup','second cup','pair behind cups','steam detail before final hold']),
]
def art(n,dark):
    ink=C if dark else I
    if n==1:return [group(1,pair(510,1110,1.25)+table(510,1230,.88)),group(2,mug(405,1190,.46)),group(3,mug(620,1190,.46)),group(4,steam(405,1145,.5)+window(770,760,.55))]
    if n==2:return [group(1,actor(245,1370,.77)),group(2,memory(140,620,730,480)),group(3,pair(510,810,.95)),group(4,mug(410,985,.5)+mug(620,985,.5))]
    if n==3:return [group(1,actor(245,1330,.95)),group(2,memory(155,625,700,440)),group(3,pair(515,845,1.1)+mug(510,1010,.38)),group(4,path('M345 1305Q540 1320 630 1140',A,6))]
    if n==4:return [group(1,door(270,1020,1.12)+table(750,1190,.52)),group(2,kettle(760,1125,.5)),group(3,actor(470,1255,.8)),group(4,actor(800,945,.7,A,True)+mug(650,1170,.36))]
    if n==5:return [group(1,table(510,1120,1.36)+mug(300,1095,.95)),group(2,kettle(695,770,.8)),group(3,mug(700,1180,.95)),group(4,path('M565 735Q500 840 665 1110',A,5)+steam(300,1010,.8))]
    if n==6:return [group(1,memory(170,615,680,485)+mug(495,925,1.2)),group(2,steam(495,825,1.1)),group(3,actor(260,1350,.8)),group(4,path('M350 1300Q535 1340 650 1170',A,6))]
    if n==7:return [group(1,chair(215,1100,.8)+chair(810,1100,.8)+table(515,1195,.72)),group(2,actor(215,975,.75)),group(3,actor(810,975,.75,A,True)),group(4,mug(430,1170,.42)+mug(600,1170,.42))]
    if n==8:return [group(1,pair(510,955,1.45,ink)),group(2,table(510,1235,1.2,ink)),group(3,mug(375,1200,.65,ink)+mug(650,1200,.65,ink)),group(4,path('M285 1035Q510 1140 735 1035',S,6))]
    if n==9:return [group(1,actor(220,1340,.85)),group(2,memory(165,615,700,465)),group(3,pair(515,805,.8)+mug(430,960,.5)+mug(620,960,.5)),group(4,path('M325 1280Q525 1290 665 1140',A,6))]
    if n==10:return [group(1,mug(510,810,1.1,ink)),group(2,memory(160,610,710,370,ink)),group(3,pair(510,1240,1.1,ink)),group(4,bubble(360,1070,330,130,ink)+path('M405 1135H480M535 1135H610',S,5))]
    if n==11:return [group(1,actor(220,1350,.8)),group(2,memory(160,605,710,490)),group(3,window(725,750,.4)+table(510,970,.55)),group(4,pair(510,845,.65)+mug(440,950,.32)+mug(575,950,.32))]
    if n==12:return [group(1,window(275,820,.8)),group(2,table(515,1220,1.05)+mug(365,1170,.6)),group(3,kettle(735,1110,.55)+mug(655,1190,.6)),group(4,pair(510,1000,1.05))]
    if n==13:return [group(1,pair(510,1260,1.38)),group(2,bubble(160,625,690,390)),group(3,mug(365,815,.85)+mug(650,815,.85)),group(4,ribbon(280,1080,470))]
    if n==14:return [group(1,pair(510,1250,1.35)),group(2,memory(140,630,355,360)),group(3,mug(310,815,.85)),group(4,memory(570,735,300,305))]
    if n==15:return [group(1,pair(510,1050,1.05)+table(510,1190,.86)),group(2,mug(405,1150,.5)+mug(615,1150,.5)),group(3,actor(205,1400,.55)),group(4,path('M285 1390Q470 1450 615 1290',A,6))]
    return [group(1,mug(300,1120,1.32)),group(2,mug(705,1190,1.32)),group(3,pair(510,760,.87)),group(4,steam(300,1000,1.1)+steam(705,1070,1.1))]
v.DESIGNS=DESIGNS;v.art=art
schedule=v.schedule;pose=v.pose
def storyboard(lines,ts,animated):
    doc=f'''---
format: 1080x1920
duration: {ts[-1]['end']:.8f}s
message: Attend to one specific remembered moment of connection and its personal meaning, without treating it as a verdict on the relationship.
arc: ordinary kitchen → memory and attention → details → subjective meaning → limit → optional reflection and sharing → return
audience: Indonesian adults
mode: autonomous
---

# Momen kecil, dinikmati lagi — storyboard v1

Exactly sixteen meaningful compositions, charcoal 08/10. Editorial v1.3 / visual v1.2; canonical fixed chrome, local Newsreader and DM Sans. Content x88–936 / y230–1480, full spoken captions y1550–1740. Original tea-making and remembered-context illustrations, no B-roll. Registry word search returned generic caption effects and light leaks, none fitting the canonical restrained caption and faceless kitchen-memory treatment. Reuse the accepted board caption implementation and draw the episode-specific scene. Four semantic states per frame. Numbers indicate illustration order only. Memory shapes represent a thought, not proof of relationship outcomes. Static poses are verified before synthesis; later timing uses measured native speech. No BGM, sparse material cues, deliberate quiet on both dark moments and the final hold.

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
- reads: initial context (0–{d*.14:.2f}s); action ({d*.14:.2f}–{d*.43:.2f}s); response/detail ({d*.43:.2f}–{d*.73:.2f}s); consequence ({d*.73:.2f}–{d:.2f}s)
- sound: {'narration and intentional material-cue silence' if n in (8,10,14,16) else 'narration; selected cues resolved in sound_design.json'}

Purpose/layout: {idea}
Starting state: {beats[0]}. Internal beats: {beats[1]} at {d*.14:.2f}s → {beats[2]} at {d*.43:.2f}s → {beats[3]} at {d*.73:.2f}s. Final state is the complete illustration; title and chrome remain stationary. Continuity uses the same cups, distinct faceless pair and thought bubble across detail cuts. Cut to the next scene's changed viewpoint; two full-palette switches punctuate specific lines rather than promotional transitions.
'''
        if x['dramatic']:doc+=f'\nDramatic line: "{x["text"]}". Reason: '+('the speaker recognizes the personally felt meaning of company' if n==8 else 'one warm memory does not settle a wider relationship question')+'. Ground, copy, captions and chrome invert together, with actor shapes retained.\n'
        doc+='\n'
    return doc
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--assemble',action='store_true');a=ap.parse_args();lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));ts=schedule(lines)
    (V/'compositions/frames').mkdir(parents=True,exist_ok=True)
    if not a.assemble:
        for x,t in zip(lines,ts):(V/f'compositions/frames/f{x["id"]:02d}.html').write_text(pose(x,t),encoding='utf-8')
    (V/'index.html').write_text(v.index(lines,ts,a.assemble),encoding='utf-8');(V/'STORYBOARD.md').write_text(storyboard(lines,ts,a.assemble),encoding='utf-8');(V/'scene_schedule.json').write_text(json.dumps(ts,indent=2)+'\n',encoding='utf-8')
    (V/'SPEC.md').write_text('''GOAL: Explain relational savoring through an ordinary remembered tea-making moment; invite personal attention without a treatment/outcome claim.
OUTPUT: HyperFrames 1080x1920/30fps, sixteen meaningful scenes, approximately 90 seconds.
LOOK: cream #F3EDE3, charcoal #302B28, brick #A34F3F, sand #D8C8B5. Fourteen cream, exactly two charcoal (08/10). Newsreader 76–82px, DM Sans captions 46px; inherited fixed chrome. No supporting paragraphs.
OBJECTS: Faceless organic pair with distinct contours; mugs with handles and rims, kettle with spout/handle/lid, table with legs, chairs, door with knob, window with mullions and night moon; thought outline with two trailing circles; speech space with a tail. Ground every memory in a remembering participant.
MOTION: Four semantic states; three context/action/response developments at roughly 14/43/73% with varied draw/settle/move mechanisms, measured against native speech. Traces 0.6–0.9s power2.inOut; actor arrival 0.6–0.9s power3.out. Stable emphasis/chrome. No idle loops or drifting titles. Final deliberate hold.
SHOTS: Wide kitchen; thought close-up; attention to memory; arrival at door; cups and kettle; linger on a cup; pair on chairs; dark personal meaning; specific memory; dark limit; choose one memory; place/action/context; optional speech; separate subjective meanings; return to kitchen; cups and quiet ending.
BANNED: Generic card grids, particles, gradients, neon, B-roll, diagnosis, gender/blame coding, manufactured neuroscience, guaranteed effect, identical slide-ups, continuous zoom and title drift. Board serif/cream/numbering are identity. Connecting traces represent attention and subjective experience, never causal efficacy.
QA: Full visual board before audio; caption coverage; motion/reverse seeks; acoustic anchors; all fifteen visual seams; full MP4 decode; final actual SFX placement, loudness and true peak. Record listening limits.
''',encoding='utf-8')
    print(json.dumps(dict(scenes=len(ts),duration=ts[-1]['end'],animated=a.assemble)))
if __name__=='__main__':main()
