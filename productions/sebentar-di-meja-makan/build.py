"""Episode-owned dinner/phone drawings with the inherited board renderer."""
from pathlib import Path
import argparse,json
import visuals as v
from visuals import path,line,circle,rect,group,actor,bubble,ribbon,C,I,A,S
P=Path(__file__).resolve().parent;V=P/'video'
def phone(x,y,k=1,c=I,screen=False):
    return f'<g transform="translate({x} {y}) scale({k})">'+rect(-67,-125,134,250,c,'none',18)+line(-24,-97,24,-97,c,4)+line(-18,100,18,100,c,4)+(rect(-44,-50,88,65,c,S,8)+line(-28,-27,25,-27,c,4)+line(-28,-7,10,-7,c,4) if screen else '')+'</g>'
def plate(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+circle(0,0,78,c,w=5)+circle(0,0,58,c,w=3)+path('M-113 -70V75M-130 -70V-30Q-113 0 -96 -30V-70M-113 -70V-20M113 -70V75M113 -70Q90 -15 113 0',c,5)+'</g>'
def glass(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-35 -50H35L25 55H-25ZM-29 -5H29',c,5)+'</g>'
def table(x=515,y=1130,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-340 -95Q-365 -95 -365 -65V140Q-365 165 -340 165H340Q365 165 365 140V-65Q365 -95 340 -95Z',c,5)+line(-310,165,-310,225,c)+line(310,165,310,225,c)+'</g>'
def meal(c=I): return table(c=c)+plate(310,1160,.85,c)+plate(720,1160,.85,c)+glass(510,1095,.65,c)
def dots(x,y,c=I):return ''.join(circle(x+i*26,y,4,c,c,w=1) for i in range(3))
def fragment(x,y,w=245,c=I):return path(f'M{x} {y}H{x+w*.37}M{x+w*.52} {y}H{x+w}',c,6)
def turn(x,y,w=250,c=A):return path(f'M{x} {y}Q{x+w*.55} {y-90} {x+w} {y-10}M{x+w-25} {y-42}L{x+w} {y-10}L{x+w-35} {y+4}',c,6)
DESIGNS=[
('Dinner interrupted','Wide dinner view establishes two distinct faceless partners, plates, glass, phone and the opening conversation.', ['pair and dinner table','speaker’s speech space','phone demanding attention','conversation trace stops before receiver']),
('Phone takes attention','Large phone occupies the space between two partners while a conversation route bends toward its screen.', ['two separate partners','large central phone','short speech space','attention route directed to screen']),
('An interaction is interrupted','Horizontal conversation is visibly interrupted where a phone enters its route.', ['speaker and listener','conversation route','phone inserted into route','remaining route broken into two pieces']),
('An ordinary work story','Speaker opens a story over dinner; the receiving partner has a phone notification.', ['speaker and meal','work-story speech space','receiver and phone','notification outline on screen']),
('Repeat the missed point','Receiver’s short response sits apart from the speaker’s interrupted story.', ['speaker and receiver','receiver’s short response space','interrupted story trace','speaker reopens the earlier trace']),
('Describe visible actions','Object close-up separates two observable details: a broken conversational route and a phone.', ['large phone','continuous speech trace','trace now split','receiver-side trace leads toward phone']),
('Room for a story','Speaker remains large; the space for the story narrows near the still-present phone.', ['speaker','large speech outline','phone near receiving side','story trace confined to speaker side']),
('Feeling is heard, intention asked','Charcoal dialog pair gives the speaker a full space and leaves the other partner’s intention as an open question.', ['speaker and receiver','speaker’s speech space','receiver’s distinct response space','open inquiry route without motive label']),
('One scene has limits','Close phone/meal detail remains concrete; the pair stays in view with an open gap for inquiry.', ['phone beside two plates','speaker','receiver','open inquiry route between the pair']),
('Name a pressing reply','Receiver names a need to answer; a phone remains inside that partner’s own speech space.', ['receiver','receiver’s speech space','phone inside that space','speaker retains a separate uncompleted story']),
('Ask for attention','Speaker makes a dinner-specific request with a phone set beside the table instead of across the story.', ['speaker and receiver','speaker’s request space','table and two plates','phone moved to table edge']),
('Announce the pause','Receiver’s message reply is visible within an announced pause; the other partner’s unfinished story remains present.', ['receiver and phone','receiver’s speech space','small message detail','speaker’s retained story trace']),
('Return through action','Charcoal return: phone is set aside, attention route comes back and the earlier story reconnects.', ['dinner and distinct pair','phone resting away from route','returning attention trace','speaker’s story route reconnects']),
('Both needs have a place','Two distinct speech spaces connect across dinner; the phone rests outside their shared route.', ['two partners and meal','first speech space','second speech space','phone aside with an open shared route']),
('Reopen the conversation','The opening dinner composition returns; speech now reaches the partner while the phone stays aside.', ['pair and dinner table','speaker reopens the story','phone aside','conversation trace reaches receiver']),
('Discuss availability','Close dinner ending holds the pair and their joined conversation while the phone stays visibly outside the route.', ['two partners and plates','phone resting at edge','speaker’s story trace','receiver’s return route before quiet hold']),
]
def art(n,dark):
    c=C if dark else I
    if n==1:return [group(1,actor(260,820,.95,c)+actor(765,820,.95,A,True)+meal(c)),group(2,bubble(155,590,370,175,c)),group(3,phone(750,1025,.63,c,True)),group(4,fragment(390,920,230,c))]
    if n==2:return [group(1,actor(230,1180,.95,c)+actor(815,1180,.95,A,True)),group(2,phone(520,920,1.5,c,True)),group(3,bubble(145,625,290,155,c)),group(4,path('M315 1080Q350 945 435 920',A,7))]
    if n==3:return [group(1,actor(225,1020,1,c)+actor(805,1020,1,A,True)),group(2,ribbon(315,890,410,c)),group(3,phone(550,970,.95,c)),group(4,path('M315 890C365 872 415 870 465 880M635 900C665 902 695 900 725 890',c,5))]
    if n==4:return [group(1,actor(245,1160,1.1,c)+plate(260,1390,.65,c)),group(2,bubble(155,650,525,260,c)+line(205,725,530,725,c)+line(205,770,450,770,c)),group(3,actor(785,1060,.92,A,True)+phone(755,1290,.7,c)),group(4,rect(725,1260,60,35,c,S,6))]
    if n==5:return [group(1,actor(255,1200,1,c)+actor(785,1110,1,A,True)),group(2,bubble(625,635,230,165,c)+dots(700,710,c)),group(3,fragment(185,910,390,c)),group(4,turn(265,1370,385,A))]
    if n==6:return [group(1,phone(710,1050,1.38,c,True)),group(2,bubble(155,650,450,235,c)),group(3,fragment(175,1015,340,c)),group(4,path('M250 1250Q380 1360 620 1185',A,7))]
    if n==7:return [group(1,actor(250,1190,1.35,c)),group(2,bubble(165,630,650,335,c)),group(3,phone(780,1150,.85,c)),group(4,line(225,745,445,745,c,6)+line(225,805,385,805,c,6))]
    if n==8:return [group(1,actor(245,1220,1,c)+actor(790,1220,1,A,True)),group(2,bubble(145,650,350,260,c)),group(3,bubble(585,760,285,220,c)),group(4,path('M390 1110Q515 1020 670 1110',c,6))]
    if n==9:return [group(1,plate(275,850,.9,c)+plate(760,850,.9,c)+phone(520,865,1.1,c,True)),group(2,actor(245,1260,.9,c)),group(3,actor(790,1260,.9,A,True)),group(4,path('M355 1170Q510 1095 675 1170',c,6))]
    if n==10:return [group(1,actor(785,1280,1.1,A,True)),group(2,bubble(240,640,625,360,c)),group(3,phone(600,825,.95,c,True)),group(4,actor(235,1300,.92,c)+fragment(155,1070,300,c))]
    if n==11:return [group(1,actor(240,1155,.9,c)+actor(790,1155,.9,A,True)),group(2,bubble(150,630,630,260,c)),group(3,table(515,1260,.92,c)+plate(330,1280,.66,c)+plate(705,1280,.66,c)),group(4,phone(835,1300,.5,c))]
    if n==12:return [group(1,actor(765,1120,1.03,A,True)+phone(730,1330,.65,c,True)),group(2,bubble(280,630,585,320,c)),group(3,rect(545,745,225,105,c,'none',12)+dots(625,797,c)),group(4,actor(235,1260,.85,c)+fragment(145,1070,305,c))]
    if n==13:return [group(1,actor(245,815,.95,c)+actor(780,815,.95,A,True)+table(515,1200,1,c)+plate(310,1215,.85,c)+plate(720,1215,.85,c)),group(2,phone(850,1390,.48,c)),group(3,turn(685,970,-340,c)),group(4,bubble(160,605,385,160,c)+ribbon(345,1010,340,c))]
    if n==14:return [group(1,actor(245,1190,.95,c)+actor(790,1190,.95,A,True)+plate(310,1390,.7,c)+plate(715,1390,.7,c)),group(2,bubble(150,650,330,235,c)),group(3,bubble(550,770,330,235,c)),group(4,phone(850,1410,.40,c)+ribbon(365,1090,295,A))]
    if n==15:return [group(1,actor(260,820,.95,c)+actor(765,820,.95,A,True)+meal(c)),group(2,bubble(155,590,370,175,c)),group(3,phone(850,1390,.48,c)),group(4,ribbon(355,925,335,A))]
    return [group(1,actor(250,800,1.1,c)+actor(785,800,1.1,A,True)+plate(310,1260,1,c)+plate(720,1260,1,c)),group(2,phone(840,1430,.4,c)),group(3,bubble(155,1000,350,145,c)),group(4,path('M680 1030Q595 920 470 935',A,6))]
v.DESIGNS=DESIGNS;v.art=art
schedule=v.schedule;pose=v.pose
def storyboard(lines,ts,animated):
    doc=f'''---
format: 1080x1920
duration: {ts[-1]['end']:.8f}s
message: Notice a phone-interrupted interaction and ask explicitly for conversational attention.
arc: dinner interruption → concept → observable actions and limits → request and named pause → return through action
audience: Indonesian adults
mode: autonomous
---

# Sebentar di meja makan — storyboard v1

Exactly sixteen original meaningful compositions: fourteen cream, two charcoal (08/13). Board editorial v1.3 / visual v1.2, fixed chrome, Newsreader and DM Sans. Same irregular ink participant and differently contoured brick participant throughout; colors indicate identity only. Key content x88–936 / y230–1480; full speech captions y1550–1740 under the accepted board geometry. No B-roll or supporting paragraphs. Four semantic stages per scene. Phone is a rounded handset with speaker, screen and lower mark; plates have rims and cutlery; table and drinking glass ground the meal. A broken route represents the fictional interruption, not a psychological measurement. Static poses precede paid narration and animation.

Registry searched for minimal captions/dialogue/line drawing: generic weight-shift captions and notification UI would replace the accepted typography and illustration vocabulary, so the inherited board renderer remains. BGM intentionally absent: exposed conversational pauses support inquiry without prescribing an emotion. Sparse frozen board contact/air/connection cues follow measured action timing. Dark turns and final reflection withhold SFX.

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
- sound: {'narration with intentional SFX silence' if n in (8,13,16) else 'narration, with selected material cues in sound_design.json'}

Purpose/layout: {idea}
Starting state: {beats[0]}. Internal beats: {beats[1]} at {d*.14:.2f}s → {beats[2]} at {d*.43:.2f}s → {beats[3]} at {d*.73:.2f}s. Final state: full episode illustration, heading and fixed chrome. Continuity: same pair, phone, plates, story route and returning attention; view changes distinguish observable action, possible experience and inquiry. Caption replacements are not semantic beats.
'''
        if x['dramatic']:doc+=f'\nDramatic line: "{x["text"]}". Reason: '+('a feeling receives room while motive remains an inquiry' if n==8 else 'attention returns through concrete action rather than only a promise')+'. Entire background, captions, emphasis and chrome invert together.\n'
        doc+='\n'
    return doc
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--assemble',action='store_true');args=ap.parse_args();lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));ts=schedule(lines)
    (V/'compositions/frames').mkdir(parents=True,exist_ok=True)
    if not args.assemble:
        for x,t in zip(lines,ts):
            source=pose(x,t)
            if x['id']==3:source=source.replace('<g id="beat2">','<g id="beat2" opacity="0">')
            (V/f'compositions/frames/f{x["id"]:02d}.html').write_text(source,encoding='utf-8')
    (V/'index.html').write_text(v.index(lines,ts,args.assemble),encoding='utf-8');(V/'STORYBOARD.md').write_text(storyboard(lines,ts,args.assemble),encoding='utf-8');(V/'scene_schedule.json').write_text(json.dumps(ts,indent=2)+'\n',encoding='utf-8')
    (V/'SPEC.md').write_text('''GOAL: Explain partner phubbing through one interrupted dinner conversation and a concrete request to return attention.
OUTPUT: HyperFrames 0.9.1, 1080x1920, 30fps, sixteen shots, approximately 90s, Instagram Reel.
LOOK: inherited board cream #F3EDE3, ink #302B28, brick #A34F3F, sand #D8C8B5. Newsreader 76–82px; full captions DM Sans 46px. Fixed chrome. Exactly charcoal 08/13; fourteen cream. The board explicitly authorizes cream/serif and series chrome.
OBJECTS: Two irregular faceless participants with distinct contours; rounded handset with earpiece/screen; two plates with rims and cutlery; rounded dinner table and water glass; speech spaces and attention traces. Fictional illustration, no scientific measurements.
MOTION: Context is visible at cut; meaningful changes at 14/43/73% of each measured scene. Line draws 0.6–0.9s power2.inOut; phone arrives or moves aside 0.6–0.9s power3.out. No infinite motion or moving reading text. Final quiet hold.
SHOTS: dinner wide; concept phone close-up; conversation interrupted; story and notification; repeat missed point; observable interruption; speaker experience; dark inquiry; inference limits; pressing reply; concrete request; announced pause; dark return through action; needs discussed; opening reprise; availability question.
SOUND: One continuous ElevenLabs native-speed voice; measured acoustic pauses and integer 30fps cuts; sparse contact/air/connection cues. No BGM: conversational pauses remain open. Dark turns/final hold withhold SFX.
BANNED: stock footage, supporting paragraphs, generic UI cards, diagnostic labels, gender/blame coding, causal satisfaction claims, mandatory permanent availability, identical entrances, decorative drift, particles, gradients, notification pings, invented numbers.
QA: Complete styled storyboard before audio; all captions; exactly 16 scenes/2 dark; actual semantic phases, forward/reverse seeks, fifteen quiet scene anchors, encoded seam frames/audio, source hashes, cue matching, full decode and proof sheet. Listening limitations stated separately.
''',encoding='utf-8')
    (V/'STORYLINES.md').write_text('''# Storyline selection

Five devices considered: dinner interruption; phone-user replay; overhead meal objects; one conversation trace; a silent phone-setting action followed by explanation.

1. Selected: a moment at dinner, wide/object/dialogue cuts with opening reprise. First two seconds show a pair, two plates and a story about to be interrupted. Arc: interruption → definition → distinction → request → announced pause → visible return. Board ink/cream material and selective contact sounds. Strongest because the ordinary event carries the whole explanation.
2. Phone-user replay: follow the handset from screen close-up to the missed story, then retrace its path in reverse. First two seconds focus on the phone. More subjective but risks confusing a single illustrative event with hidden intention.
3. Overhead continuous meal: one table composition changes only through plates, phone and speech routes. First two seconds show two settings and one handset. Bold single-stage approach; rejected because sixteen meaningful frames benefit from visible changes in viewpoint and focal scale.

Agent selection under immediate automation; no additional human storyline gate. Chosen hook and accepted board already resolve the same story/look decision.
''',encoding='utf-8')
    print(json.dumps(dict(scenes=16,duration=ts[-1]['end'],animated=args.assemble)))
if __name__=='__main__':main()
