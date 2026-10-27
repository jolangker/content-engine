"""Episode-specific ceramics, choices, response spaces, and shared-time scenes."""
from pathlib import Path
import argparse, json
import visuals as v
from visuals import path,line,circle,rect,group,actor,bubble,ribbon,bowl,C,I,A,S
P=Path(__file__).resolve().parent;V=P/'video'

def pot(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-115 -55Q0 -95 115 -55L100 85Q0 145 -100 85Z',c,5,S)+path('M-115 -55Q0 -15 115 -55M-80 -48Q0 -65 80 -48',c,5)+path('M-160 155H160',c,4)+'</g>'
def calendar(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+rect(-160,-180,320,360,c,'none',18)+line(-160,-90,160,-90,c)+line(-85,-215,-85,-145,c)+line(85,-215,85,-145,c)+f'<text x="0" y="-122" text-anchor="middle" fill="{c}" font-family="DM Sans" font-size="36">SABTU</text>'+line(-98,-20,98,-20,S,4)+line(-98,45,98,45,S,4)+line(-98,110,98,110,S,4)+'</g>'
def clock(x,y,r=75,c=I):return circle(x,y,r,c)+line(x,y,x,y-r*.6,c,4)+line(x,y,x+r*.5,y+r*.2,c,4)
def question(x,y,c=I):return path(f'M{x-25} {y-22}Q{x+35} {y-66} {x+35} {y-18}Q{x+35} {y+5} {x} {y+18}V{y+38}',c,6)+circle(x,y+65,5,c,c)
def dash(d,c=I):return path(d,c,5,extra='stroke-dasharray="14 16"')
def sofa(x,y,k=1,c=I):return f'<g transform="translate({x} {y}) scale({k})">'+rect(-200,-65,400,170,c,S)+rect(-175,-155,350,155,c,'none')+line(-150,110,-150,155,c)+line(150,110,150,155,c)+'</g>'
DESIGNS=[
('An apparently open choice','Two distinct participants; a broad speech space says permission while the route toward a ceramic pot narrows.',['two participants','open speech space','pot as desired activity','narrowed route']),
('Room around a choice','Close ceramic pot held in a broad open boundary; two separate voices leave space around its route.',['large pot','first voice','different voice','open choice boundary']),
('An endorsed direction','The participant and pot share a route; a surrounding open space leaves the direction with the chooser.',['chooser','pot','chosen route','space around the route']),
('One Saturday, two wishes','A large Saturday calendar bridges a pot and home sofa, with the pair locatable on opposite sides.',['Saturday calendar','ceramics wish','home wish','pair and shared time']),
('Different views can coexist','Wide pair with two speech spaces; distinct curved responses remain separate around the shared calendar.',['pair','first perspective','different perspective','common Saturday']),
('Make the reason audible','Close speaker with pot; their voice reaches an open receiving space, with no imposed path drawn over it.',['speaker','ceramics reason','voice route','receiving space']),
('Shared time is a need','A clock and two seats make shared time concrete; each person has a response route into it.',['clock','two seats','first response','second response']),
('Closeness as a condition','Charcoal: a route between pair and pot is squeezed by two boundary strokes; the response space remains visibly constricted.',['pair continuity','desired pot','constricting boundary','tight response space']),
('Look across responses','Three distinct conversation spaces are inspected as a sequence rather than one sentence deciding a relationship.',['first exchange','next exchange','third exchange','open observation bracket']),
('Ask why the class matters','One question crosses between pair toward the pot; a broad speech space waits for the answer.',['questioner','ceramics participant','question path','answer space']),
('Leave room for the answer','A close response space opens fully; its voice reaches the listener before an alternate activity is proposed.',['response space','own reason','voice ribbon','listener']),
('Name your own wish','Return to the pair with home seats; a different voice names desired time without blocking the pot.',['pair','shared seats','own voice','unblocked activity']),
('Negotiate the calendar','Large calendar receives a ceramic marker and a distinct shared-time circle on different portions; two routes meet it.',['calendar','class marker','together-time marker','two agreement routes']),
('A disagreement has space','Charcoal: pair retain distance and connection; one response remains open while a clear boundary leaves a gap to answer.',['pair continuity','open response','clear boundary','reply gap']),
('Care remains involved','Two participants lean their attention toward a common time space while the ceramic choice remains separate.',['pair','attention routes','clear shared space','separate personal activity']),
('An open choice stays open','Return to opening: pair, pot and speech space; the path now remains open around a personally chosen direction.',['opening pair','desired pot','open speech space','unconstricted route']),
]
def art(n,dark):
    ink=C if dark else I
    if n==1:return [group(1,actor(245,1130,1.05)+actor(800,1130,.95,A,True)),group(2,bubble(155,600,460,190)+ribbon(205,690,330)),group(3,pot(690,875,.65)),group(4,path('M360 1110Q510 890 620 1060',A,6)+line(510,945,510,1030,I)+line(555,1025,555,1120,I))]
    if n==2:return [group(1,pot(505,1010,1.7)),group(2,ribbon(160,700,260)),group(3,ribbon(640,1220,230,I)),group(4,path('M180 620H110V1380H900V620H750',I,5))]
    if n==3:return [group(1,actor(245,1160,1.15)),group(2,pot(790,820,.85)),group(3,path('M360 1120Q535 1080 690 880',A,7)),group(4,path('M130 650Q500 470 900 650M110 1330Q520 1480 920 1270',S,5))]
    if n==4:return [group(1,calendar(505,830,1.05)),group(2,pot(240,1210,.65)),group(3,sofa(795,1220,.5)),group(4,actor(190,910,.6)+actor(830,910,.6,A,True)+path('M325 1240Q515 1390 665 1240',A,5))]
    if n==5:return [group(1,actor(245,1180,.95)+actor(815,1180,.95,A,True)),group(2,bubble(120,600,340,190)+ribbon(155,690,235)),group(3,bubble(600,815,310,175,A)+ribbon(640,900,210,I)),group(4,calendar(490,1255,.47))]
    if n==6:return [group(1,actor(240,1110,1.15)),group(2,pot(355,785,.7)),group(3,path('M345 1030Q500 755 680 875',A,6)),group(4,bubble(615,905,285,235)+ribbon(650,1010,205))]
    if n==7:return [group(1,clock(510,735,125)),group(2,sofa(510,1160,1.15)),group(3,actor(180,875,.65)+path('M230 945Q225 1060 360 1120',A,6)),group(4,actor(845,875,.65,A,True)+path('M800 945Q790 1060 665 1120',I,6))]
    if n==8:return [group(1,actor(240,1200,1,ink)+actor(825,1200,.9,A,True)),group(2,pot(520,770,1,ink)),group(3,line(465,1020,465,1295,ink,7)+line(575,1020,575,1295,ink,7)),group(4,path('M350 1190H455M585 1190H710',S,6)+bubble(465,1025,105,125,ink))]
    if n==9:return [group(1,bubble(130,650,360,170)+ribbon(175,720,235)),group(2,bubble(490,925,365,170,A)+ribbon(535,1005,235,I)),group(3,bubble(140,1190,350,160)+ribbon(180,1270,230)),group(4,path('M850 620H925V1415H560',S,6))]
    if n==10:return [group(1,actor(240,1165,1)),group(2,actor(810,1165,1,A,True)+pot(770,860,.55)),group(3,path('M345 1050Q490 860 680 1030',A,6)+question(500,820)),group(4,bubble(530,590,370,160,A))]
    if n==11:return [group(1,bubble(140,630,655,330)),group(2,pot(400,820,.75)),group(3,ribbon(310,1100,330)),group(4,actor(790,1240,1,A,True)+path('M650 1110Q765 1050 800 1120',I,5))]
    if n==12:return [group(1,actor(240,1200,.95)+actor(815,1200,.95,A,True)),group(2,sofa(500,800,.75)),group(3,bubble(130,985,340,135)+ribbon(165,1050,230)),group(4,pot(795,680,.5)+path('M610 965Q745 970 800 850',A,6))]
    if n==13:return [group(1,calendar(510,990,1.7)),group(2,pot(420,1030,.5)),group(3,clock(655,1165,58,A)),group(4,path('M110 850Q190 720 270 770M900 1330Q825 1450 750 1395',A,6))]
    if n==14:return [group(1,actor(230,1170,1,ink)+actor(825,1170,1,A,True)),group(2,bubble(135,610,355,205,ink)+ribbon(170,700,240,S)),group(3,path('M535 865V1045M535 1210V1410',ink,7)),group(4,path('M345 1160Q430 1090 515 1130M560 1130Q640 1090 715 1160',S,6))]
    if n==15:return [group(1,actor(240,1160,1)+actor(810,1160,1,A,True)),group(2,path('M350 1120Q520 980 705 1120',A,6)),group(3,clock(525,1040,70)+path('M455 1190H590',I,5)),group(4,pot(525,710,.8)+line(380,865,675,865,S,4))]
    return [group(1,actor(245,1160,1.05)+actor(800,1160,.95,A,True)),group(2,pot(700,850,.75)),group(3,bubble(130,600,420,185)+ribbon(175,690,290)),group(4,path('M355 1140Q540 990 650 900',A,7)+path('M415 1270Q625 1295 855 1050',S,5))]
v.DESIGNS=DESIGNS;v.art=art
schedule=v.schedule;pose=v.pose
def storyboard(lines,ts,animated):
    doc=f'''---
format: 1080x1920
duration: {ts[-1]['end']:.8f}s
message: Support personally endorsed choices while negotiating consequences for shared time.
arc: apparently open choice → autonomy support → Saturday preferences → pressure → reasons → shared agreement → open response
audience: Indonesian adults
mode: autonomous
---

# Ruang untuk memilih — visual storyboard v1

Exactly sixteen meaningful compositions; charcoal 08/14, fourteen cream. Canonical frozen chrome, Newsreader/DM Sans and flat four-color illustrations. Content x88–936/y230–1480; captions y1550–1740. Pot and Saturday calendar make the activity/time concrete. No gender, blame or diagnostic color encoding. Registry query organic conversation autonomy choice caption returned chat mockups and decorative captions; original board-consistent relational illustrations and unadorned full captions fit this film. No BGM; sparse frozen material cues. Static storyboard verification precedes synthesis/animation under automation, not human approval.

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
- sound: {'intentional SFX silence' if n in (8,14,16) else 'narration; selected cues in sound_design.json'}

Purpose/layout: {idea}
States: {beats[0]} locatable at cut → {beats[1]} at {d*.14:.2f}s → {beats[2]} at {d*.43:.2f}s → {beats[3]} at {d*.73:.2f}s. Each state develops the illustrated action; captions do not count as semantic motion. Next cut changes detail/scale or returns to the same pair. Keep title/chrome stationary and actor silhouettes consistent.
'''
        if x['dramatic']:doc+=f'\nDramatic line: "{x["text"]}". Reason: {"conditional closeness constricts a choice" if n==8 else "agreement requires room for an honest disagreement"}. Invert ground, captions, main copy and chrome together for this entire frame.\n'
        doc+='\n'
    return doc
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--assemble',action='store_true');a=ap.parse_args();lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));ts=schedule(lines)
    (V/'compositions/frames').mkdir(parents=True,exist_ok=True)
    if not a.assemble:
        for x,t in zip(lines,ts):(V/f'compositions/frames/f{x["id"]:02d}.html').write_text(pose(x,t),encoding='utf-8')
    (V/'index.html').write_text(v.index(lines,ts,a.assemble),encoding='utf-8');(V/'STORYBOARD.md').write_text(storyboard(lines,ts,a.assemble),encoding='utf-8');(V/'scene_schedule.json').write_text(json.dumps(ts,indent=2)+'\n',encoding='utf-8')
    (V/'SPEC.md').write_text('''GOAL: Recognize whether a choice remains open after a partner responds, and discuss both personal wishes and shared time.
OUTPUT: HyperFrames 1080x1920, 30fps, 16 meaningful scenes.
TIME: 90s estimate; measured native-speed narration and integer-frame acoustic anchors replace estimates.
LOOK: Ground #F3EDE3, ink #302B28, brick #A34F3F, sand #D8C8B5. Two charcoal inversions 08/14. Newsreader 400 76–82px; DM Sans 500 captions 46px, object labels 36px. No shadow/grain/blur. Fixed canonical chrome.
OBJECTS: Distinct organic faceless pair, clay ceramic pot with open rim/base, Saturday calendar with binders and rule lines, shared sofa and clock, speech spaces, boundaries and routes. No phone.
MOTION: First semantic state at cut. Three meaningful developments near 14%, 43%, 73%; trace 0.6–0.9s power2.inOut, responsive placement 0.6–0.9s power3.out, varied left/down versus line revelation. No idle loops. Titles remain fixed. Quiet final hold.
SHOTS: STORYBOARD.md carries shot-specific scale, actions, reading windows and sounds. Alternate wide pair, large pot, calendar close-up, shared seating and response spaces. Two intentional palette cuts.
BANNED: B-roll, neon, gradients, particles, decorative cards, diagnostic labels, conditional-love imagery as a diagnosis, gender/blame colors, identical entrances, drifting text, unseeded randomness. Cream/serif/number chrome are inherited approved identity exceptions. Hard detail cuts preserve the board's illustrated conversation grammar.
QA: All sixteen static poses before synthesis; all actual intermediate beats; two inversions; 360px legibility; stationary chrome; seek determinism; preview; encoded proof; full decode; fifteen acoustic seams; actual placed cue presence, duration and levels. Sound measured, not perceptually heard.
''',encoding='utf-8')
    print(json.dumps(dict(frames=16,duration=ts[-1]['end'],snapshot_at=','.join(f'{t["start"]+t["duration"]*.94:.8f}' for t in ts))))
if __name__=='__main__':main()
