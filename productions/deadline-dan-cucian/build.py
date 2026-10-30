"""Episode-specific laundry/work illustrations; inherited board mount and chrome."""
from pathlib import Path
import argparse,json
import visuals as v
from visuals import path,line,circle,rect,group,actor,bubble,ribbon,C,I,A,S
P=Path(__file__).resolve().parent;V=P/'video'
def laptop(x,y,k=1,c=I):
 return f'<g transform="translate({x} {y}) scale({k})">'+rect(-140,-105,280,180,c,'none',10)+path('M-140 75L-190 125H190L140 75M-65 100H65',c,6)+line(-95,-55,70,-55,S,5)+line(-95,-15,35,-15,S,5)+line(-95,25,75,25,A,5)+'</g>'
def shirt(x,y,k=1,c=I,fill='none'):
 return f'<g transform="translate({x} {y}) scale({k})">'+path('M-40 -85L-110 -40L-78 15L-53 0V105H53V0L78 15L110 -40L40 -85Q0 -30 -40 -85Z',c,5,fill)+'</g>'
def basket(x,y,k=1,c=I):
 return f'<g transform="translate({x} {y}) scale({k})">'+path('M-155 -70L-125 110Q0 150 125 110L155 -70ZM-155 -70Q0 -110 155 -70M-90 -50L-75 95M-30 -50L-25 110M30 -50L25 110M90 -50L75 95M-130 5H130M-120 55H120',c,5)+'</g>'
def laundry(x,y,k=1,c=I):return shirt(x-55*k,y-90*k,k*.65,c,S)+shirt(x+65*k,y-65*k,k*.55,c)+basket(x,y,k,c)
def hanger(x,y,k=1,c=I):
 return f'<g transform="translate({x} {y}) scale({k})">'+path('M-22 -62Q-28 -112 10 -112Q55 -110 25 -65L0 -42M0 -42L-130 42Q-150 60 -120 62H120Q150 60 130 42Z',c,5)+'</g>'
def calendar(x,y,k=1,c=I):
 return f'<g transform="translate({x} {y}) scale({k})">'+rect(-95,-110,190,220,c,'none',12)+line(-95,-50,95,-50,c)+line(-52,-132,-52,-87,c)+line(52,-132,52,-87,c)+circle(0,33,45,A,w=5)+'</g>'
def folded(x,y,k=1,c=I):
 return f'<g transform="translate({x} {y}) scale({k})">'+path('M-115 -35H115V30H-115ZM-105 30H125V90H-105M-95 -35V-95H105V-35',c,5)+line(-70,-65,65,-65,S,4)+'</g>'
def rail(x,y,w=650,c=I):return line(x,y,x+w,y,c,5)+line(x+18,y,x+18,y+340,c,5)+line(x+w-18,y,x+w-18,y+340,c,5)
DESIGNS=[
('Work and laundry collide','Wide household view locates a work laptop, a full basket, and two distinct participants.', ['stressed participant and laptop','full laundry basket','responding participant','deadline calendar']),
('One concept, two participants','Two faceless participants connected by a communicative route; work stress remains anchored to its owner.', ['stressed participant and laptop','work-pressure trace','listening participant','response route']),
('Stress communicates across a relationship','Diagonal actor-to-actor composition develops signal, reception and response with the laptop as context.', ['stressed participant','speech space','receiving participant','response trace']),
('Promised task remains beside work','Object close-up contrasts an open work revision with a still-full laundry basket.', ['large laptop','deadline calendar','full basket','one shirt still in the basket']),
('Visible task, missing account','Helper foreground looks toward a large basket; the stressed partner remains at the edge without a speech space.', ['helper and basket','second unfinished shirt','stressed participant behind','open gap between them']),
('A signal is received and answered','Three-stage large interaction: spoken pressure, attending partner and a return ribbon.', ['stressed speaker','speech space with work detail','receiving partner','supportive return ribbon']),
('One task is taken on','Helper approaches one hanger while work remains with the stressed participant.', ['stressed participant and laptop','basket','helper with hanger','one shirt on the hanger']),
('Help has a boundary','Charcoal close-up preserves one bounded contribution alongside the remaining workload.', ['helper and one hanger','one shirt','remaining basket and laptop','visible boundary between contribution and remainder']),
('Both capacities stay in view','Asymmetric pair with separate task spaces and an open communication route.', ['stressed participant and laptop','helper and small basket','separate task boundaries','negotiation trace']),
('Stress is finally named','Charcoal speech close-up gives the stressed participant a large speech space containing the work detail.', ['stressed speaker','large speech space','laptop revision inside speech','responding participant']),
('Request one concrete action','Large hanger and shirt become the request; folded laundry tomorrow stays in a separate space.', ['speaker and receiver','speech space','hanger and one shirt','folded laundry beside calendar']),
('Offer only half tonight','Clothes rail holds two garment positions; one fills while the other stays pending in the basket.', ['rail and helper','first hanger','one hanging shirt','remaining basket below empty position']),
('Stress, need, available help','Three concrete objects form one negotiated interaction: laptop, requested hanger and bounded contribution.', ['pair across the content field','work detail in speaker space','hanger between them','receiving response route']),
('The work deadline remains','Laptop and deadline persist above; below, laundry is explicitly split between hanging and remaining work.', ['laptop and deadline','one shirt on hanger','remaining basket','task boundary']),
('Return to the opening scene','Opening wide household composition returns with a speech route and one completed contribution.', ['stressed participant and laptop','helper','laundry basket','hanger and agreed route']),
('Which part can we share','Close shared task scene with two locatable participants and one hanger; no magically empty workload.', ['two distinct participants','one hanger','shirt joining hanger','remaining basket before final quiet hold']),
]
def art(n,dark):
 c=C if dark else I
 if n==1:return [group(1,actor(270,970,.9,c)+laptop(280,1210,.62,c)),group(2,laundry(690,1190,.94,c)),group(3,actor(770,845,.77,A,True)),group(4,calendar(475,700,.55,c))]
 if n==2:return [group(1,actor(250,1000,1,c)+laptop(260,1260,.56,c)),group(2,path('M270 850Q270 750 390 755',A,6)),group(3,actor(775,1040,.95,A,True)),group(4,path('M415 810Q650 740 730 900',c,6)+path('M700 1200Q520 1320 375 1190',S,6))]
 if n==3:return [group(1,actor(260,1190,1.15,c)+laptop(245,1390,.42,c)),group(2,bubble(170,650,510,220,c)),group(3,actor(780,1010,1.1,A,True)),group(4,ribbon(435,1090,260,A))]
 if n==4:return [group(1,laptop(360,850,1.2,c)),group(2,calendar(760,695,.65,c)),group(3,basket(650,1220,1.2,c)),group(4,shirt(620,1070,.87,c,S))]
 if n==5:return [group(1,actor(265,1060,1.2,A,True)+laundry(680,1230,1,c)),group(2,shirt(790,1060,.55,c)),group(3,actor(755,710,.63,c)),group(4,path('M365 1025Q475 960 530 930',S,6))]
 if n==6:return [group(1,actor(240,1270,.95,c)),group(2,bubble(155,630,555,285,c)+laptop(425,775,.56,c)),group(3,actor(790,1030,.98,A,True)),group(4,path('M720 1200Q490 1400 355 1290',A,7))]
 if n==7:return [group(1,actor(250,820,.8,c)+laptop(245,1025,.57,c)),group(2,laundry(295,1295,.7,c)),group(3,actor(765,1120,1,A,True)+hanger(720,810,.8,c)),group(4,shirt(720,910,.73,c,S))]
 if n==8:return [group(1,actor(750,1200,.85,A,True)+hanger(685,760,1,c)),group(2,shirt(685,900,.9,c)),group(3,laundry(270,1210,.8,c)+laptop(280,815,.65,c)),group(4,path('M505 650V1390',S,5))]
 if n==9:return [group(1,actor(260,840,.85,c)+laptop(260,1055,.55,c)),group(2,actor(755,1100,.85,A,True)+basket(760,1330,.56,c)),group(3,path('M110 1135H410M610 1420H900',S,5)),group(4,path('M380 815Q585 675 690 960',A,6))]
 if n==10:return [group(1,actor(255,1295,1,c)),group(2,bubble(150,625,690,385,c)),group(3,laptop(485,805,1,c)),group(4,actor(785,1225,.9,A,True))]
 if n==11:return [group(1,actor(250,1310,.9,c)+actor(780,1310,.9,A,True)),group(2,bubble(155,615,705,405,c)),group(3,hanger(410,760,.75,c)+shirt(410,865,.78,c,S)),group(4,folded(730,1110,.6,c)+calendar(745,940,.4,c))]
 if n==12:return [group(1,rail(170,720,690,c)+actor(255,1275,.8,A,True)),group(2,hanger(405,820,.75,c)),group(3,shirt(405,950,1,c,S)),group(4,laundry(755,1250,.8,c))]
 if n==13:return [group(1,actor(235,1240,.95,c)+actor(795,1240,.95,A,True)),group(2,bubble(150,625,385,280,c)+laptop(340,760,.55,c)),group(3,hanger(700,710,.78,c)+shirt(700,850,.72,c,S)),group(4,ribbon(340,1110,350,A))]
 if n==14:return [group(1,laptop(375,760,.95,c)+calendar(770,690,.55,c)),group(2,hanger(300,1110,.8,c)+shirt(300,1230,.8,c,S)),group(3,laundry(750,1260,.75,c)),group(4,path('M500 1010V1430',S,5))]
 if n==15:return [group(1,actor(270,970,.9,c)+laptop(280,1210,.62,c)),group(2,actor(770,845,.77,A,True)),group(3,laundry(690,1260,.75,c)),group(4,hanger(585,1060,.65,c)+path('M355 950Q520 825 665 865',A,6))]
 return [group(1,actor(250,820,1,c)+actor(770,820,1,A,True)),group(2,hanger(515,1060,1.2,c)),group(3,shirt(515,1230,1.13,c,S)),group(4,basket(800,1360,.5,c))]
v.DESIGNS=DESIGNS;v.art=art
schedule=v.schedule;pose=v.pose
def storyboard(lines,ts,animated):
 doc=f'''---
format: 1080x1920
duration: {ts[-1]['end']:.8f}s
message: Name external stress and negotiate one concrete contribution within both partners' capacity.
arc: work and laundry collide → coping process → help and limits → explicit request → bounded agreement → return
audience: Indonesian adults
mode: autonomous
---

# Deadline dan cucian — storyboard v1

Sixteen original meaningful compositions; fourteen cream and exactly two charcoal (08/10). Board editorial v1.3, visual v1.2; fixed inherited chrome, Newsreader and DM Sans. Key content x88–936 / y230–1480; all speech captions y1550–1740. Stressed participant retains an irregular charcoal/cream silhouette; responding participant retains a different brick silhouette. No gender or blame code. SVG objects are fictional contextual illustrations. A work deadline remains after the agreement: help is a bounded task, not a proven psychological cure. Registry queried for minimal captions/dialogue/line drawing; generic caption weight/pill and whiteboard effects do not replace the board's canonical captions and object interactions. Four semantic states per frame. Static poses reviewed before synthesis. No BGM; sparse frozen material cues after measured placement. Both dark turns and final hold intentionally quiet.

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
- reads: context (0–{d*.14:.2f}s); action ({d*.14:.2f}–{d*.43:.2f}s); response/detail ({d*.43:.2f}–{d*.73:.2f}s); consequence ({d*.73:.2f}–{d:.2f}s)
- sound: {'narration with intentional SFX silence' if n in (8,10,16) else 'narration; selected material cues in sound_design.json'}

Purpose/layout: {idea}
Starting state: {beats[0]}. Internal beats: {beats[1]} at {d*.14:.2f}s → {beats[2]} at {d*.43:.2f}s → {beats[3]} at {d*.73:.2f}s. Final state: complete illustration with fixed heading/chrome. Continuity follows the same laptop, basket, shirt and distinct pair. The cut changes viewpoint or consequence; speech captions are not counted as semantic actions.
'''
  if x['dramatic']:doc+=f'\nDramatic line: "{x["text"]}". Reason: '+('assistance has a visible boundary and leaves responsibilities present' if n==8 else 'the previously unspoken pressure becomes an explicit first-person statement')+'. Ground, captions, emphasis and chrome invert together for the entire scene.\n'
  doc+='\n'
 return doc
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--assemble',action='store_true');a=ap.parse_args();lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));ts=schedule(lines)
 (V/'compositions/frames').mkdir(parents=True,exist_ok=True)
 if not a.assemble:
  for x,t in zip(lines,ts):(V/f'compositions/frames/f{x["id"]:02d}.html').write_text(pose(x,t),encoding='utf-8')
 (V/'index.html').write_text(v.index(lines,ts,a.assemble),encoding='utf-8');(V/'STORYBOARD.md').write_text(storyboard(lines,ts,a.assemble),encoding='utf-8');(V/'scene_schedule.json').write_text(json.dumps(ts,indent=2)+'\n',encoding='utf-8')
 (V/'SPEC.md').write_text('''GOAL: Explain dyadic coping through naming work pressure and negotiating one limited laundry task.
OUTPUT: 1080x1920, 30fps, sixteen scenes, approximately 90 seconds, Instagram Reel.
LOOK: board #F3EDE3 cream / #302B28 ink / #A34F3F brick / #D8C8B5 sand; exactly dark 08/10. Newsreader 76–82px, DM Sans captions 46px. Fixed board chrome unchanged. No supporting paragraphs.
OBJECTS: Irregular faceless stressed participant; differently contoured brick partner; revision laptop with keyboard, laundry basket with mesh, shirts with sleeves and neck, hangers with hooks, calendar with binding rings. Trace means communication; boundary means limited contribution, not diagnosis.
MOTION: Four semantic stages per shot. Context remains at cut, then relevant action/reception/consequence at 14/43/73% of measured duration. SVG draws 0.6–0.9s power2.inOut; arrivals 0.6–0.9s power3.out. No decorative drifting. Late scene 16 resolves into quiet hold.
SHOTS: household wide; concept pair; communication diagonal; object detail; helper viewpoint; response route; taking one task; dark boundary; both capacities; dark stress statement; specific request; half offered; agreement; deadline remains; opening reprise; shared question.
SOUND: one continuous native-speed voice, measured quiet-region pause placement; no BGM; sparse board contact/air/connection cues on actual object events. Dark moments and final hold quiet.
BANNED: stock footage, B-roll, gradients, particles, UI cards, generic icons, neurobiology, gender/blame coding, global cure, equal-capacity assumption, identical entrances, floating titles, looped motion, invented data.
QA: Complete styled static board before audio; all captions; within-scene semantic progress; reverse seeks; fixed chrome; fifteen acoustic scene anchors; exact seams; actual encoded audio, SFX placement, decode and proof frames.
''',encoding='utf-8')
 print(json.dumps(dict(scenes=16,duration=ts[-1]['end'],animated=a.assemble)))
if __name__=='__main__':main()
