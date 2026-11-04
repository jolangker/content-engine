"""Original household scene designs on the frozen board renderer."""
from pathlib import Path
import argparse,json
import visuals as v
from visuals import actor,path,line,circle,rect,group,bubble,ribbon
P=Path(__file__).resolve().parent;V=P/'video';C=v.C;I=v.I;A=v.A;S=v.S
def bag(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-15 -90L-40 -120L-5 -108L15 -130L32 -105L10 -90M-15 -90C-47 -64 -82 -12 -76 58Q-70 92 0 95Q75 94 78 55C80 0 52 -62 10 -90Z',c,6)+path('M-15 -90Q0 -83 10 -90M-40 0Q-55 35 -35 68M35 -40Q54 0 50 40',c,4)+'</g>'
def door(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-105 220V-210H105V220M-135 220H140',c,6)+circle(65,10,8,c,c,3)+'</g>'
def bin_(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-105 -100H105L82 135H-82ZM-120 -100V-125H120V-100ZM-35 -125V-151H35V-125M-42 -55V85M0 -55V85M42 -55V85',c,6)+'</g>'
def dishes(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-130 30Q0 67 130 30M-130 50Q0 88 130 50M-130 70Q0 110 130 70',c,6)+f'<ellipse cx="0" cy="10" rx="130" ry="43" fill="none" stroke="{c}" stroke-width="6"/>'+f'<ellipse cx="0" cy="10" rx="90" ry="26" fill="none" stroke="{c}" stroke-width="4"/>'+'</g>'
def sink(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-190 40H190V75Q190 155 110 155H-105Q-190 155 -190 75ZM-80 40V-140Q-80 -200 -20 -200H35Q75 -200 75 -160V-120M52 -120H98M-102 -40H-155',c,7)+'</g>'
def clock(x,y,k=1,c=I):return f'<g transform="translate({x} {y}) scale({k})">'+circle(0,0,100,c)+path('M0 -65V0L45 30M0 -85V-75M85 0H75M0 85V75M-85 0H-75',c,6)+'</g>'
def arrow(x,y,w=160,c=A):return path(f'M{x} {y}H{x+w}M{x+w-22} {y-16}L{x+w} {y}L{x+w-22} {y+16}',c,6)
DESIGNS=[
('Unmoved bag','A tied refuse bag sits beside a door while the task owner and partner notice the still unresolved task.',['door and floor','tied bag by door','task owner arrives from left','partner pauses on the right']),
('Find a cue','Close-up of the bag and a clock, then dishes introduce a concrete event to consider.',['large bag','clock appears separately','path opens toward the dishes','dishes become the candidate event']),
('Link situation to action','Dishes and bag occupy a large clear visual relationship without an outcome meter.',['dish stack','connecting path grows','bag joins the link','outside bin establishes the specific destination']),
('From wish to plan','Task owner has a speech space, then clock and door make time and place concrete.',['task owner','speech outline','clock anchors timing','door anchors location']),
('Owner says later','The owner speaks while the partner remains separate and the bag is still in place.',['pair and bag','owner speech space','short later ribbon','partner receives without a task transfer']),
('Unanchored later','Two clocks remain separated from the stationary refuse bag.',['door and bag','first clock','second clock','a short path stops before the bag']),
('Attention elsewhere','The owner moves among ordinary dishes and a book-shaped task sheet while the bag remains by the door.',['door and bag','owner at dishes','additional task sheet','clock advances the scene context']),
('Intention needs action','A large owner-owned bag is held in focus with an open path to the exit.',['large bag','task owner beside it','door ahead','clear path toward the exit']),
('One recognizable cue','Large dishes lead through a directional link to the specific bag.',['dish stack','cue outline','link between objects','bag as the selected response']),
('Predecided next step','Dishwashing and bag pickup share a wide scene with a visible route.',['sink and dishes','owner at sink','bag near route','route toward outside bin']),
('Agreement still matters','Equal visual weight for two actors, shared speech space and household task.',['two actors','shared speech outline','task bag remains shared context','two separate reply marks']),
('Owner names the plan','The task owner speaks; dishes and bag enter that same speaker-owned space in sequence.',['owner and partner','owner speech space','dish cue inside speech','bag and directional connector inside speech']),
('Check feasibility','Clock, door and bin show time, route and destination, alongside both participants.',['clock and door','outside bin','task owner','partner joins the feasibility check']),
('Act after the cue','Last dish is set down; owner grips the knot, lifts the bag and carries it toward the outside bin.',['sink and dish','last dish lands','owner grips tied bag','owner and bag arrive beside outside bin']),
('Discuss what happened','The pair face one another with distinct reply spaces and the disposal location visible behind.',['pair and outside bin','owner report space','partner response space','short connection stays between speakers']),
('Return to the doorway','Opening doorway returns with a dish cue, owner-owned bag and a concrete outward route.',['opening doorway','dish cue','owner with bag','route connects to outside bin'])]
def art(n,dark):
    c=C if dark else I;pair=actor(245,1230,.86,c)+actor(790,1230,.9,A,True)
    if n==1:return [group(1,door(615,970,1.25,c)+line(125,1280,900,1280,c)),group(2,bag(580,1180,.65,c)),group(3,actor(230,1240,.83,c)),group(4,actor(810,1260,.7,A,True))]
    if n==2:return [group(1,bag(385,1100,1.65,c)),group(2,clock(760,790,.8,c)),group(3,path('M600 1050Q770 1000 770 1150',A,6)),group(4,dishes(770,1250,.68,c))]
    if n==3:return [group(1,dishes(280,900,.95,c)),group(2,arrow(430,950,150,A)),group(3,bag(725,955,1.1,c)),group(4,bin_(725,1275,.55,c))]
    if n==4:return [group(1,actor(245,1230,1.15,c)),group(2,bubble(125,650,420,255,c)),group(3,clock(710,850,.78,c)),group(4,door(760,1180,.56,c))]
    if n==5:return [group(1,pair+bag(520,1320,.57,c)),group(2,bubble(130,650,440,260,c)),group(3,ribbon(205,775,260,c)),group(4,path('M720 790Q805 870 790 1040',A,5))]
    if n==6:return [group(1,door(745,1030,.85,c)+bag(715,1210,.57,c)),group(2,clock(295,810,.77,c)),group(3,clock(390,1140,.69,c)),group(4,path('M440 940Q560 940 560 1080',A,6))]
    if n==7:return [group(1,door(795,1110,.58,c)+bag(775,1240,.45,c)),group(2,actor(250,1230,.8,c)+dishes(350,985,.65,c)),group(3,rect(490,740,155,200,c)+path('M520 790H610M520 825H600M520 860H605',c,4)),group(4,clock(265,715,.52,c))]
    if n==8:return [group(1,bag(445,1090,1.38,c)),group(2,actor(205,1300,.8,c)),group(3,door(795,1020,.8,c)),group(4,arrow(575,1310,260,c))]
    if n==9:return [group(1,dishes(315,880,1.05,c)),group(2,circle(315,880,195,c)),group(3,arrow(520,1010,160,A)),group(4,bag(760,1145,1.27,c))]
    if n==10:return [group(1,sink(300,1000,.64,c)+dishes(295,1135,.5,c)),group(2,actor(200,1330,.76,c)),group(3,bag(555,1260,.7,c)),group(4,path('M610 1240Q700 1190 790 1155',A,6)+bin_(800,1020,.60,c))]
    if n==11:return [group(1,actor(240,1240,.95,c)+actor(790,1240,.95,A,True)),group(2,bubble(160,650,680,300,c)),group(3,bag(520,1270,.65,c)),group(4,ribbon(230,760,200,c)+ribbon(565,835,200,c))]
    if n==12:return [group(1,actor(230,1300,1,c)+actor(830,1340,.60,A,True)),group(2,bubble(125,650,690,370,c)),group(3,dishes(330,800,.68,c)),group(4,arrow(455,835,100,A)+bag(665,845,.70,c))]
    if n==13:return [group(1,clock(270,760,.65,c)+door(570,1020,.8,c)),group(2,bin_(815,1180,.56,c)),group(3,actor(200,1290,.78,c)),group(4,actor(700,1340,.72,A,True))]
    if n==14:return [group(1,sink(285,880,.70,c)),group(2,dishes(285,1070,.65,c)),group(3,actor(640,1170,.75,c)+bag(745,1120,.65,c)+path('M684 1125Q715 1110 735 1060',c,7)),group(4,bin_(810,1040,.65,c)+path('M680 1300Q790 1280 810 1205',A,6))]
    if n==15:return [group(1,pair+bin_(520,1350,.37,c)),group(2,bubble(125,665,340,240,c)),group(3,bubble(560,830,340,240,c)),group(4,ribbon(385,1160,265,A))]
    return [group(1,door(610,970,1.15,c)),group(2,dishes(280,790,.7,c)),group(3,actor(235,1260,.8,c)+bag(345,1230,.6,c)),group(4,arrow(420,1290,290,A)+bin_(810,1240,.5,c))]
v.DESIGNS=DESIGNS;v.art=art;schedule=v.schedule;pose=v.pose
def storyboard(lines,ts,animated):
    doc=f'''---
format: 1080x1920
duration: {ts[-1]['end']:.8f}s
message: Link an agreed action to a recognizable situational cue, while retaining responsibility and feasibility.
arc: unmoved refuse bag → situation/action plan → initiation gap → specific cue → limits → owner plan → action → accountability
audience: Indonesian adults
mode: autonomous
---

# Nanti itu kapan? — storyboard v1

Editorial v1.4 / visual v1.2. Sixteen original household compositions; charcoal 08/11, fourteen cream. Irregular ink actor remains viewer/task owner, rounded brick actor remains partner. Tied bag has gathered neck/knot, door has frame/handle, dishes have elliptical rims, sink has faucet/basin, outside bin has lid/ribs. Color does not encode gender or blame. Exactly two dark inversions retain actor silhouette and fixed chrome geometry. Full captions y1550–1740; key content x88–936/y230–1480. Original context-bearing objects, selective 0–5 word emphasis, no supporting paragraphs/B-roll.

Registry searched minimal captions and line drawing; existing board caption renderer and deterministic stroke reveals preserve identity. No synthetic data chart. Four semantic states, developments at 14/43/73 percent. Static storyboard completed before synthesis/animation. No music: expose ordinary responsibility without a prescribed emotional response; sparse local board material cues, silence on dramatic turns and final hold.

'''
    for x,t in zip(lines,ts):
        n=x['id'];title,idea,beats=DESIGNS[n-1];d=t['duration'];doc+=f'''## Frame {n}: {x['title']} ({t['start']:.3f}-{t['end']:.3f}s)

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
- reads: context at cut; action {d*.14:.2f}s; response {d*.43:.2f}s; consequence {d*.73:.2f}s; final hold
- sound: {'narration, intentional SFX silence' if n in (8,11,16) else 'narration; selected cues in sound_design.json'}

Purpose/layout: {idea}
Starting state: {beats[0]}. Semantic developments: {beats[1]} at {d*.14:.2f}s → {beats[2]} at {d*.43:.2f}s → {beats[3]} at {d*.73:.2f}s. Final state retains visible consequence. Continuity: same owner, partner, tied bag and household. Wide doorway, close objects, speaker framing and action route vary composition. Captions do not count as semantic animation beats.

'''
        if x['dramatic']:doc+=f'Dramatic line: "{x["text"]}". Reason: '+('the intention must become action' if n==8 else 'planning does not settle willingness or fairness')+'. Invert ground, text, captions and chrome together; return to cream next scene.\n\n'
    return doc
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--assemble',action='store_true');a=ap.parse_args();lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));ts=schedule(lines);(V/'compositions/frames').mkdir(parents=True,exist_ok=True)
    if not a.assemble:
        for x,t in zip(lines,ts):(V/f'compositions/frames/f{x["id"]:02d}.html').write_text(pose(x,t),encoding='utf-8')
    (V/'index.html').write_text(v.index(lines,ts,a.assemble),encoding='utf-8');(V/'STORYBOARD.md').write_text(storyboard(lines,ts,a.assemble),encoding='utf-8');(V/'scene_schedule.json').write_text(json.dumps(ts,indent=2)+'\n',encoding='utf-8')
    (V/'SPEC.md').write_text('''GOAL: Help the agreed task owner connect a recognizable cue to a specific action; no mind-reading or guaranteed relationship outcome.
OUTPUT: HyperFrames 1080x1920/30fps, sixteen scenes, 85–95 seconds. Automation through Trypost queue, no human approval claimed.
LOOK: Frozen cream #F3EDE3, ink #302B28, brick #A34F3F, sand #D8C8B5. Local Newsreader 76–82px, DM Sans captions 46px. Fixed series chrome from board. Content x88–936/y230–1480 and captions y1550–1740 override generic layout defaults. Exactly two charcoal scenes 08/11.
OBJECTS: Original knot-neck refuse bag, framed door with handle, rimmed dish stack, faucet and basin, outside bin with lid/ribs. Same irregular owner on left and rounded partner on right. Arrows show proposed action sequence, no measured causal outcome.
MOTION: Four semantic states/scene; developments at 14/43/73%, stroke reveals 0.6–0.9s power2.inOut; arrivals/settles power3.out. Stationary headings and chrome. Continuous native-speed narration, acoustic pauses and integer 30fps cuts. Full spoken captions up to five words/group.
SHOTS: doorway unresolved bag; cue question close-up; dishes/action link; time/place; owner speech; unanchored later; competing activity; dark action; clear cue link; predecided route; dark agreement limit; explicit owner plan; feasibility; last dish then bag; report; doorway reprise.
SOUND: One ElevenLabs eleven_v4 narration, sparse licensed board material cues, quiet dark turns and final reflection; no BGM for open-ended ordinary responsibility.
BANNED: B-roll, presumed partner motives, diagnosis, gender/blame colors, outcome gauges, guaranteed success, supporting paragraphs, gradients, neon, particles, continual drift, repeated title entrance, automatic SFX at every cut.
QA: Static board PNG before synthesis, POV check, sixteen/two palette count, internal states and phone sheets, seek consistency, exact seams, H264/AAC full decode, acoustic boundary and SFX matching, export SHA-256, public remote-byte check and actual schedule readback. Sound measured, not heard.
''',encoding='utf-8')
    (V/'STORYLINES.md').write_text('''# Delegated storyline choice

Five seeds: household doorway/action route; one continuous kitchen counter; metaphorical railway; future completed chore in reverse; abstract intention/action typography.

1. Selected: a visible refuse bag at the door, dish cue and owner taking responsibility, with object close-ups and speaker-owned speech spaces. Recognizable, fair and follows one task through sixteen compositions.
2. A single continuous counter with all actions in one wide view. Spatial continuity is strong but lacks enough meaningful focal variation for this board.
3. A metaphorical railway changing tracks between intention and action. Bold visual structure, but loses the everyday household context and could imply guaranteed automatic success.

Agent chose 1 under immediate automation; selected hook/board resolve storyline/look without another pitch gate.
''',encoding='utf-8');print(json.dumps(dict(scenes=16,duration=ts[-1]['end'],animated=a.assemble)))
if __name__=='__main__':main()
