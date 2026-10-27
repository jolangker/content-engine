"""Episode-specific dinner, contribution and gratitude compositions."""
import argparse, json
from pathlib import Path
import visuals as v
from visuals import path,line,circle,rect,group,actor,plate,bubble,ribbon,C,I,A,S
P=Path(__file__).resolve().parent; V=P/'video'

def clock(x,y,r=70,c=I):return circle(x,y,r,c)+line(x,y,x,y-r*.6,c,4)+line(x,y,x+r*.5,y+r*.2,c,4)
def pot(x,y,k=1,c=I):return f'<g transform="translate({x} {y}) scale({k})">'+path('M-135 -45H135V75Q135 110 95 110H-95Q-135 110 -135 75Z',c,6,S)+path('M-170 -35H-135M135 -35H170M-150 -60Q0 -125 150 -60',c,6)+path('M-35 -118H35M-55 -150Q-90 -185 -50 -220M45 -150Q10 -185 50 -220',c,5)+'</g>'
def bag(x,y,k=1):return f'<g transform="translate({x} {y}) scale({k})">'+path('M-95 -60H95L115 130H-115Z',I,5,S)+path('M-45 -60V-100Q0 -155 45 -100V-60',I,5)+circle(-30,-70,35,A,S)+path('M30 -50L60 -135L80 -120L60 -30',I,5)+'</g>'
def vegetables(x,y,k=1):return f'<g transform="translate({x} {y}) scale({k})">'+rect(-130,-85,260,170,I,C,25)+circle(-50,0,40,A,S)+circle(45,20,35,A,S)+path('M-120 -25L95 65M-35 -100L10 -150L35 -135L-10 -80',I,6)+'</g>'

DESIGNS=[
('Dinner and a small thank you','Two organic participants face a prepared plate; a short speech space arrives, then a path returns to the cook.',['pair at dinner','plate set','thanks space','attention returns to cook']),
('Gratitude travels between people','A large speaker opens a voice ribbon toward the benefactor; a shared dinner marker enters and the route meets the recipient.',['speaker','voice ribbon','kindness marker','recipient']),
('Two focuses in the same expression','The pair shares one speaking space; one branch reaches the meal, another reaches the cook, and a common ribbon keeps both in one expression.',['pair and speech','benefit branch','contribution branch','common expression']),
('Tired arrival and ready food','A doorway locates the arrival; a plate is set at the table, the participant sits, and a quiet pause surrounds the meal.',['arrival at doorway','ready dinner','seat at table','resting interval']),
('The benefit received','One participant rests beside an emptied plate; a benefit ribbon arrives and the cooking task is left on a separate side.',['resting participant','plate','relief ribbon','separate cooking task']),
('The actual preparation','A grocery bag, chopped ingredients and pot develop from left to right; a small clock completes the sequence of time spent.',['grocery bag','prepared ingredients','pot cooking','time spent']),
('Give the contribution space','The cook stands beside the pot; a large recognition arc opens from the speaker, follows the work and arrives near the cook.',['cook and pot','recognition space','work trace','recognition reaches cook']),
('The benefactor inside the thanks','On charcoal, a speech outline encloses the still-identifiable benefactor, a cream effort trace connects the pot, and the speaker remains outside listening.',['benefactor in words','cooking contribution','effort trace','speaker present']),
('A bounded observation','Two people have a recorded conversation; short brackets locate that interaction and an unfilled expression mark remains illustrative, without a percentage or projection.',['conversing pair','speech exchange','bounded observation','warmth trace']),
('Other issues remain separate','On charcoal, a thank-you ribbon reaches one person while another unresolved conversation stays separate; the path ends without joining the two.',['pair and appreciation','other conversation','unresolved line','bounded path']),
('One real action','Close on a hand-like contribution trace, one pot and one clock; an observation arc chooses the concrete action rather than a pile of praise.',['one pot','time marker','observed contribution','single recognition trace']),
('A specific spoken thank you','A large open speech space joins the pair, holds a meal/time detail and lands one appreciation route at the partner.',['speaker and listener','specific words space','time and meal','appreciation reaches partner']),
('Ask before inventing','A question space leaves room above the cook; a short answer space appears beside the actual pot and time is left unfilled.',['cook','open question','answer space','unfilled detail']),
('A reply has room','Two participants keep their space; the partner opens a reply, the speaker remains still and a reciprocal trace meets between them.',['pair','partner reply','speaker holds space','reciprocal trace']),
('Back to the meal','Overhead return to the opening meal, with a separate trace toward the preparation and the person who did it.',['dinner plate','shared table','preparation trace','cook identified']),
('A concrete final recognition','The original pair remains at dinner; a speech path carries one contribution from the pot to the cook and settles in a quiet open ending.',['pair and meal','cooking trace','recognition route','quiet shared space']),
]

def art(n,dark):
    ink=C if dark else I
    if n==1:return [group(1,actor(260,1080,1)+actor(790,1080,1,A,True)+rect(345,1050,350,170,S,S,45)),group(2,plate(520,1100,86)),group(3,bubble(160,590,390,185)+ribbon(205,670,245)),group(4,path('M575 860Q720 830 765 950',A,6))]
    if n==2:return [group(1,actor(260,1050,1.3)),group(2,path('M370 950Q530 710 725 860',A,7)),group(3,plate(520,720,80)),group(4,actor(795,1030,1,A,True))]
    if n==3:return [group(1,actor(250,1180,.8)+actor(805,1180,.8,A,True)+bubble(175,570,650,230)),group(2,path('M400 850Q300 930 345 1050',I,5)+plate(345,1050,60)),group(3,path('M650 850Q780 870 805 1050',A,5)),group(4,ribbon(265,680,460))]
    if n==4:return [group(1,path('M140 1280V580H400V1280',S,8)+'<g id="arrival">'+actor(680,1280,.7)+'</g>'),group(2,rect(500,980,360,230,S,S,40)+plate(680,1020,90)),group(3,actor(840,790,.70,A,True)),group(4,path('M460 670Q650 570 850 690',I,5))]
    if n==5:return [group(1,actor(315,1015,1.35)),group(2,plate(640,1240,100)),group(3,ribbon(485,805,325)),group(4,pot(795,650,.55)+path('M670 735Q650 790 680 840',S,4))]
    if n==6:return [group(1,bag(270,735,.75)),group(2,vegetables(530,970,.88)),group(3,pot(755,1275,.8)+path('M590 1390H910',I,7)),group(4,clock(780,670,70)+path('M335 830Q390 865 425 915M635 1070Q700 1100 725 1140',A,5))]
    if n==7:return [group(1,actor(780,800,1,A,True)+pot(740,1190,.8)),group(2,bubble(135,590,410,250)),group(3,path('M250 920Q290 1210 605 1240',I,6)),group(4,path('M610 1230Q890 1130 840 930',A,6))]
    if n==8:return [group(1,bubble(380,580,500,580,ink)+actor(625,875,1.25,A,True)),group(2,pot(245,1200,.65,ink)),group(3,path('M365 1170Q490 1240 565 1080',S,6)),group(4,actor(220,800,.8,ink))]
    if n==9:return [group(1,actor(275,1120,.9)+actor(795,1120,.9,A,True)),group(2,bubble(185,650,310,170)+bubble(580,830,300,160,A)),group(3,path('M140 580H190M140 580V1300H190M865 580H915V1300H865',S,5)),group(4,ribbon(390,1210,260))]
    if n==10:return [group(1,actor(250,1180,.7,ink)+actor(800,1180,.7,A,True)+ribbon(345,1120,355,S)),group(2,bubble(245,590,560,270,ink)),group(3,path('M320 730C390 615 535 850 625 730C680 660 710 700 730 740',S,6)),group(4,path('M530 1080V950',ink,5)+circle(530,950,10,ink,ink))]
    if n==11:return [group(1,pot(485,1080,1.4)),group(2,clock(785,720,85)),group(3,path('M185 1190Q105 830 405 655',A,7)),group(4,path('M410 650Q550 550 665 650',I,5))]
    if n==12:return [group(1,actor(230,1240,.8)+actor(820,1240,.8,A,True)),group(2,bubble(140,565,720,340)),group(3,clock(680,730,65)+plate(370,730,70)),group(4,path('M340 1080Q535 970 745 1100',A,6))]
    if n==13:return [group(1,actor(760,1150,1,A,True)+pot(720,1330,.55)),group(2,bubble(130,590,420,255)+path('M310 665Q390 620 385 690Q380 725 340 740V765',I,5)+circle(340,800,5,I,I)),group(3,bubble(570,900,315,155,A)),group(4,circle(740,990,34,I)+path('M160 1090Q310 1210 470 1080',S,5))]
    if n==14:return [group(1,actor(230,1210,.85)+actor(820,1210,.85,A,True)),group(2,bubble(515,600,370,230,A)+ribbon(555,700,250,I)),group(3,path('M175 1000Q200 930 290 940',I,5)),group(4,path('M350 1180Q530 1350 715 1180',A,6))]
    if n==15:return [group(1,plate(465,1020,155)),group(2,rect(200,790,550,440,S,'none',70)),group(3,path('M620 1190Q850 1260 820 930',A,6)+pot(800,790,.48)),group(4,actor(805,580,.55,A,True))]
    return [group(1,actor(250,1130,.9)+actor(800,1130,.9,A,True)+plate(530,1200,90)),group(2,pot(530,710,.65)),group(3,path('M530 820Q380 930 410 1060',I,5)),group(4,path('M420 1060Q620 910 745 1035',A,6))]

v.DESIGNS=DESIGNS;v.art=art
schedule=v.schedule;pose=v.pose
def storyboard(lines,ts,animated):
    doc=f'''---
format: 1080x1920
duration: {ts[-1]['end']:.5f}s
message: Recognize the partner's concrete contribution within a sincere thank-you.
arc: dinner question → expressed gratitude → benefit and effort → evidence and limit → specific appreciation → reply
audience: Indonesian adults
mode: autonomous
---

# Terima kasih yang melihat — visual storyboard v1

Editorial v1.3 / visual-audio v1.2. Exactly 16 frames; charcoal 8 (the benefactor in the thanks) and 10 (limit of the finding), 14 cream. Stable organic silhouettes, fixed canonical chrome, full captions y1550–1740; key content x88–936/y230–1480. Contribution paths are metaphors, not measurements. Varied pair/overhead/close-work/observer/exchange compositions. Registry queried organic conversation gratitude; light leak and phone chat templates do not fit this flat dinner illustration. No named effect is recreated. Agent verifies the full static board before synthesis and animation; no human approval claimed. Voice uses root .env ElevenLabs eleven_v4. No BGM; sparse licensed material cues after measured timing; silence on the caveat and final hold.

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
- reads: opening action (0–{d*.14:.2f}s); contribution develops ({d*.14:.2f}–{d*.43:.2f}s); response ({d*.43:.2f}–{d*.73:.2f}s); consequence ({d*.73:.2f}–{d:.2f}s)
- sound: {'intentional silence' if n in (8,10,16) else 'narration; selected material cue only where listed in sound_design.json'}

Purpose/layout: {idea}
States: {beats[0]} already locatable → {beats[1]} at {d*.14:.2f}s → {beats[2]} at {d*.43:.2f}s → {beats[3]} at {d*.73:.2f}s. Preserve landed static geometry, caption clearance and actor identity. The next frame develops the narrated reasoning; cuts preserve the illustrated vocabulary without claiming a causal mechanism.
'''
        if x['dramatic']:doc+=f'\nDramatic line: "{x["text"]}". Reason: {"the person receives space inside the appreciation" if n==8 else "interrupt any guarantee or substitute for unresolved conversation"}. Invert ground, copy, captions and chrome together.\n'
        doc+='\n'
    return doc
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--assemble',action='store_true');a=ap.parse_args();lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));ts=schedule(lines)
    (V/'compositions/frames').mkdir(parents=True,exist_ok=True)
    if not a.assemble:
        for x,t in zip(lines,ts):(V/f'compositions/frames/f{x["id"]:02d}.html').write_text(pose(x,t),encoding='utf-8')
    (V/'index.html').write_text(v.index(lines,ts,a.assemble),encoding='utf-8');(V/'STORYBOARD.md').write_text(storyboard(lines,ts,a.assemble),encoding='utf-8');(V/'scene_schedule.json').write_text(json.dumps(ts,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(frames=16,duration=ts[-1]['end'],snapshot_at=','.join(f'{t["start"]+t["duration"]*.94:.5f}' for t in ts))))
if __name__=='__main__':main()
