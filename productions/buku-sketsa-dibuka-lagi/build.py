"""Sixteen original sketchbook compositions in the approved board language."""
from pathlib import Path
import argparse,json
import visuals as v
from visuals import path,line,circle,rect,group,actor,bubble,ribbon,C,I,A,S
P=Path(__file__).resolve().parent;V=P/'video'
def book(x=520,y=1050,k=1,c=I,ink=True):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M0 -140Q-140 -185 -265 -140V150Q-140 105 0 150Q140 105 265 150V-140Q140 -185 0 -140ZM0 -140V150',c,6)+''.join(line(-245,yy,-230,yy,c,3) for yy in range(-110,120,40))+(sketch(125,0,.85,c) if ink else '')+'</g>'
def sketch(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-65 75H70M-45 68L-25 -20H35L50 68ZM0 -22C-70 -35 -65 -105 -14 -90C-10 -140 65 -125 55 -75C105 -50 45 -15 0 -22Z',c,4)+'</g>'
def pencil(x,y,k=1,c=A):
    return f'<g transform="translate({x} {y}) scale({k}) rotate(30)">'+path('M-16 -120H16V90L0 125L-16 90ZM-16 -90H16M-16 90H16M0 125V112',c,5)+line(0,-87,0,86,c,2)+'</g>'
def table(x=520,y=1220,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-360 0H360V35H-360ZM-305 35V180M305 35V180',c,6)+'</g>'
def price(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+path('M-90 -65H35L100 0L35 65H-90Z',c,5)+circle(51,0,9,c)+path('M-58 -22H-10M-58 0H8M-58 22H-10',c,4)+'</g>'
def clock(x,y,k=1,c=I):
    return f'<g transform="translate({x} {y}) scale({k})">'+circle(0,0,85,c)+path('M0 -50V0L42 25',c,5)+''.join(line(xx,yy,xx*.86,yy*.86,c,3) for xx,yy in [(0,-78),(78,0),(0,78),(-78,0)])+'</g>'
def reply(x,y,w=360,h=230,c=I):
    return path(f'M{x+25} {y}H{x+w-25}Q{x+w} {y} {x+w} {y+25}V{y+h-25}Q{x+w} {y+h} {x+w-25} {y+h}H{x+w-80}L{x+w-45} {y+h+60}L{x+w-50} {y+h}H{x+25}Q{x} {y+h} {x} {y+h-25}V{y+25}Q{x} {y} {x+25} {y}Z',c,5)
DESIGNS=[
('Open sketchbook','An open sketchbook at a table; partner returns to drawing while viewer introduces a price tag.',['sketchbook and tabletop','partner takes position by the book','viewer arrives at the table','price tag enters the viewer side']),
('Two agendas','One shared table, two separate speech spaces: selling versus drawing.',['two distinct actors','viewer speech outline','partner reply outline','price and drawing symbols reveal different goals']),
('A growth model','Large open sketchbook links a current unfinished drawing to a clearer drawing; partner remains its author.',['large open book','partial plant sketch','pencil by the page','partner beside the open practice space']),
('Support in action','Pair at the same table; the viewer makes room beside the partner rather than moving the partner.',['table and partner','viewer settles beside table','open sketchbook','short support ribbon reaches the work surface']),
('Whose aspiration','Partner foreground with a large reply space containing the desired practice, with no imposed outcome.',['partner foreground','partner reply outline','small drawing in reply space','pencil links partner to their own page']),
('Back to drawing','Close-up book leaves one page empty; familiar plant drawing and pencil return without a business symbol.',['open book on tabletop','first plant contour','pencil near empty page','partner enters the open practice space']),
('Sales agenda','The viewer speech space contains a price tag and buyer silhouettes; partner and book remain below.',['viewer and table','viewer speech space','price tag inside viewer speech','two small buyer silhouettes in same speech space']),
('Unstated goal','Dark close-up: the partner has a drawing in a distinct reply space while the sales tag remains separate.',['partner and book','partner reply outline','plant drawing in reply space','price tag stays outside that reply space']),
('Relevant to whom','Wide view with two separate possible routes; no arrow equates selling with the partner goal.',['table and pair','viewer price space','partner drawing space','short lines meet their own symbols, not each other']),
('Practice opportunity','Large shared tabletop provides a book, a pencil and a clock as bounded practice support.',['tabletop','book opens','pencil becomes available','clock makes a possible practice interval visible']),
('No instant outcome','Dark book detail holds an unfinished drawing and an open practice path, without a success stamp.',['book and partner','unfinished contour','pencil stays beside page','open path continues beyond this one drawing']),
('Viewer asks','Viewer foreground opens a speech space but leaves the partner answer empty.',['viewer and partner','viewer question space','small book marks the topic','open reply space on partner side']),
('Partner answers','Partner reply space contains a book and pencil; the viewer listens from a smaller position.',['partner foreground and viewer','partner reply outline','book inside the reply','pencil confirms the named practice goal']),
('Offer time','Clock and sketchbook share a table while the two actors approach from separate sides.',['clock and tabletop','open book','viewer arrives','partner settles by the book']),
('Their own step','Partner with pencil occupies the practice space; viewer remains adjacent outside the working page.',['table and viewer','partner at the book','pencil moves into the practice area','small drawn plant develops on the page']),
('Return to the book','Reprise of the opening table now centers the partner drawing; the viewer support stays beside the page.',['open book and table','partner by book','viewer beside the table','pencil joins the sketch then holds']),
]
def art(n,dark):
    c=C if dark else I
    pair=actor(285,1230,.85,c)+actor(790,1220,.90,A,True)
    if n==1:return [group(1,book(520,1000,.9,c)+table(520,1170,.95,c)),group(2,actor(790,1220,.85,A,True)+path('M747 1170Q712 1115 690 1080',A,8)),group(3,actor(205,1270,.80,c)),group(4,price(280,800,.9,c))]
    if n==2:return [group(1,pair),group(2,bubble(135,660,335,240,c)),group(3,reply(560,770,335,240,c)),group(4,price(300,780,.7,c)+book(725,880,.43,c))]
    if n==3:return [group(1,book(515,1030,1.35,c,False)),group(2,sketch(335,1050,.8,c)),group(3,pencil(700,1050,.9)),group(4,actor(805,1330,.58,A,True))]
    if n==4:return [group(1,table(520,1160,.95,c)+actor(780,1230,.85,A,True)),group(2,actor(205,1280,.80,c)),group(3,book(520,1000,.8,c)),group(4,path('M745 1170Q710 1105 675 1080',A,8)+ribbon(325,1080,130,A))]
    if n==5:return [group(1,actor(750,1270,1.3,A,True)),group(2,reply(180,650,650,350,c)),group(3,book(510,825,.65,c)),group(4,pencil(645,1110,.8,c))]
    if n==6:return [group(1,book(520,980,1.32,c,False)+table(520,1210,1,c)),group(2,sketch(345,990,.9,c)),group(3,pencil(670,1030,1.1)),group(4,actor(800,1350,.66,A,True)+path('M770 1305Q690 1220 670 1080',A,8))]
    if n==7:return [group(1,actor(235,1280,1.08,c)+book(610,1260,.68,c)),group(2,bubble(140,650,685,355,c)),group(3,price(370,815,.95,c)),group(4,actor(610,810,.4,c)+actor(720,810,.4,c,True))]
    if n==8:return [group(1,actor(770,1250,1.15,A,True)+book(355,1250,.6,c)),group(2,reply(410,650,475,340,c)),group(3,sketch(650,830,1.05,c)),group(4,price(240,865,.95,c))]
    if n==9:return [group(1,pair+table(520,1360,.92,c)),group(2,bubble(135,650,335,235,c)+price(300,765,.68,c)),group(3,reply(560,750,335,235,c)+book(725,860,.43,c)),group(4,path('M270 1070V955M780 1060V1040',c,5))]
    if n==10:return [group(1,table(520,1200,1.03,c)),group(2,book(480,1030,.94,c)),group(3,pencil(810,1070,.7)),group(4,clock(760,750,.8,c))]
    if n==11:return [group(1,book(450,1070,1.05,c,False)+actor(820,1290,.62,A,True)),group(2,path('M290 1135H385M313 1128L333 1040H365M337 1035Q290 985 325 960',c,5)),group(3,pencil(650,1120,.8,c)),group(4,path('M190 1370Q350 1305 500 1370Q650 1430 850 1370',c,5))]
    if n==12:return [group(1,actor(250,1250,1.05,c)+actor(815,1270,.7,A,True)),group(2,bubble(130,650,370,250,c)),group(3,book(315,785,.43,c)),group(4,reply(560,880,335,220,c))]
    if n==13:return [group(1,actor(780,1250,1.2,A,True)+actor(230,1270,.72,c)),group(2,reply(200,650,660,370,c)),group(3,book(500,830,.7,c)),group(4,pencil(695,830,.62,c))]
    if n==14:return [group(1,clock(760,720,.8,c)+table(520,1190,.96,c)),group(2,book(520,1030,.8,c)),group(3,actor(200,1300,.78,c)),group(4,actor(790,1270,.9,A,True)+path('M745 1215Q710 1150 680 1120',A,8))]
    if n==15:return [group(1,table(520,1210,.96,c)+actor(200,1340,.72,c)),group(2,actor(790,1280,.94,A,True)+book(535,1040,.85,c,False)),group(3,pencil(655,1030,.8)+path('M748 1220Q700 1170 655 1070',A,8)),group(4,sketch(640,1040,.5,c))]
    return [group(1,book(520,1000,.9,c)+table(520,1170,.95,c)),group(2,actor(790,1220,.85,A,True)),group(3,actor(205,1270,.80,c)),group(4,pencil(655,1000,.65)+path('M745 1165Q700 1110 655 1040',A,8))]
v.DESIGNS=DESIGNS;v.art=art
schedule=v.schedule;pose=v.pose
def storyboard(lines,ts,animated):
    doc=f'''---
format: 1080x1920
duration: {ts[-1]['end']:.8f}s
message: Support the partner's own desired growth rather than substituting a different goal.
arc: sketchbook reopened → growth model → mismatched sales advice → relevant help → ask and hear → drawing again
audience: Indonesian adults
mode: autonomous
---

# Buku sketsa dibuka lagi — storyboard v1

Editorial v1.4 / visual v1.2. Sixteen original meaningful compositions, fourteen cream and two charcoal (08/11). Irregular ink viewer remains supporter; rounded brick partner remains aspiring artist. Open book has paired curved pages and spine; plant sketch, pencil tip/eraser, four-legged tabletop, price tag with hole and clock establish recognizable context. No measured progress or diagnostic symbols. In dark frames ink becomes cream while actor shapes/positions persist. Stationary board chrome. Caption band y1550–1740, key content x88–936/y230–1480. Full captions, 0–5 emphasis words, no supporting paragraph or B-roll.

Catalog searched minimal captions line drawing dialogue; generic captions and whiteboard ink are available. Reuse existing board caption renderer and deterministic stroke principles to preserve its approved forms; episode objects drawn as original SVG. Each shot develops context, action, response and consequence at 0/14/43/73 percent, with actual semantic changes below. Narration begins only after complete styled static board verification. BGM intentionally none; sparse board SFX, quiet 08/11/final hold.

'''
    for x,t in zip(lines,ts):
        n=x['id']; title,idea,beats=DESIGNS[n-1];d=t['duration']
        doc+=f'''## Frame {n}: {x['title']} ({t['start']:.3f}-{t['end']:.3f}s)

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
- reads: context at cut; action {d*.14:.2f}s; response {d*.43:.2f}s; consequence {d*.73:.2f}s; final readable hold
- sound: {'narration, intentional SFX silence' if n in (8,11,16) else 'narration; selected cues in sound_design.json'}

Purpose/layout: {idea}
Starting state: {beats[0]}. Internal semantic developments: {beats[1]} at {d*.14:.2f}s → {beats[2]} at {d*.43:.2f}s → {beats[3]} at {d*.73:.2f}s. Final state retains the context and visible consequence. Continuity: same supporter and artist shapes, same sketchbook, paired pages and repeated plant drawing. Vary wide, close object, speaker, goal-space and tabletop framing; subtitle changes are not action beats.

'''
        if x['dramatic']:doc+=f'Dramatic line: "{x["text"]}". Reason: '+('recognize that selling has not been stated as the partner goal' if n==8 else 'limit the claim: relevant support cannot guarantee instant achievement')+'. Background, labels, captions and fixed chrome invert together; next frame returns to cream.\n\n'
    return doc
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--assemble',action='store_true');args=ap.parse_args()
    lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));ts=schedule(lines);(V/'compositions/frames').mkdir(parents=True,exist_ok=True)
    if not args.assemble:
        for x,t in zip(lines,ts):(V/f'compositions/frames/f{x["id"]:02d}.html').write_text(pose(x,t),encoding='utf-8')
    (V/'index.html').write_text(v.index(lines,ts,args.assemble),encoding='utf-8');(V/'STORYBOARD.md').write_text(storyboard(lines,ts,args.assemble),encoding='utf-8');(V/'scene_schedule.json').write_text(json.dumps(ts,indent=2)+'\n',encoding='utf-8')
    (V/'SPEC.md').write_text('''GOAL: Help the supporter notice whether their advice fits the partner's ideal-self aspiration; ask, hear, then offer relevant help.
OUTPUT: HyperFrames 1080x1920, 30fps, 16 compositions, approximately 90 seconds (85–95). Automation through Trypost queue; agent verification, no human approval claimed.
LOOK: Approved board cream #F3EDE3 / ink #302B28 / brick #A34F3F / sand #D8C8B5. Local Newsreader regular display 76–82px, DM Sans captions 46px, no shadows or gradients. Board identity geometry overrides generic platform defaults. Two dark turns 08/11. Content x88–936/y230–1480; captions y1550–1740; stationary header/frame number/footer.
OBJECTS: Same distinct irregular supporter left and rounded aspiring artist right. Curved paired sketchbook pages/spine, familiar potted plant sketch, pencil with tip/eraser, tabletop/legs, price tag with hole, clock and actor-owned speech outlines. Sales symbols remain outside artist's desired practice space. No outcome gauge.
MOTION: Four semantic states per shot, developments at 14/43/73%; 0.6–0.9s power2.inOut stroke reveals and power3.out arrivals/settles. One reading priority; no indefinite loops. Native-speed continuous narration, measured acoustic cuts on integer 30fps clock. Full spoken captions in groups up to five words.
SHOTS: opening book/table; separate agendas; large book; pair support; artist's aspiration; drawing close-up; sales speech; dark unspoken goal; separate target routes; practice objects; dark outcome limit; viewer asks; partner answers; time offer; partner works; opening reprise.
SOUND: ElevenLabs eleven_v4 one recording, sparse traceable board material cues. No BGM: leave aspiration and answer emotionally open. Quiet dark turns and final hold.
BANNED: B-roll, gender/blame/diagnosis coding, presumed causes of silence, success stamps or guaranteed growth, extra psychological concepts, supporting paragraphs, neon, particles, gradients, perpetual drift, same text entrance everywhere, automatic whoosh on every cut.
QA: Complete static board before synthesis, narration-only POV, sixteen/two palette count, all intermediate semantic states and phone sheet, seek consistency and seams, full H264/AAC decode, acoustic boundary checks, SFX waveform matching, export hash and remote schedule receipts. Record sound not heard.
''',encoding='utf-8')
    (V/'STORYLINES.md').write_text('''# Delegated storyline choice

1. Selected: sketchbook return with supporter suggesting sales, separate goal-spaces, explicit question/answer and practice-time offer. Recognizable context and stable audience role.
2. A single overhead page split between two sets of marks. Elegant but insufficient scene/actor variety for sixteen meaningful compositions.
3. A future gallery opening then reverse to practice. Strong outcome hook but implies success not supported by the model or this fictional advice.

Agent chose 1 under immediate automation. Hook and board resolve storyline/look; no additional human pitch gate.
''',encoding='utf-8')
    print(json.dumps(dict(scenes=16,duration=ts[-1]['end'],animated=args.assemble)))
if __name__=='__main__':main()
