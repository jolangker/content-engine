from pathlib import Path
import json, math, re
P=Path(__file__).resolve().parent; V=P/'video';ROOT=P.parents[1]
data=json.loads((P/'scene-plan.json').read_text(encoding='utf-8'))
a=json.loads((V/'audio_meta.json').read_text()); voice=a['voices'][0];words=voice['words'];pr=.3;tail=1.32
assert len(words)==sum(len(d['vo'].split()) for d in data)
def clean(s):return re.sub(r'[^\w]','',s).lower()
idx=0
layouts=[
('Intimate quote above an asymmetric pair; brick speaker carries one small sand event mark toward a distant listener.','Quote dominates; the shared event emerges later.'),
('Small acknowledgement high left; listener moves toward a drawn screen at the right while the speaker remains low left.','Attention changes direction, not a repeated quote layout.'),
('Charcoal pressure field; one large empty listening space contracts around a smaller speaker, with a withheld connection.','Dark field and negative space replace the two-actor interaction.'),
('Observation above a dividing line; a single response is separated from the open question of motive.','Return to cream; horizontal separation with no actor pair.'),
('Oversized concept name, then a low three-stage path from positive event to sharing and response.','Typography is the focal object; explanatory nodes unfold later.'),
('Large diagonal actors connected by an extended curve, with the event travelling into the shared space.','Diagram fills the canvas with unequal scale and diagonal distance.'),
('Three short response qualities stack down the left beside a small listening actor at the right.','Sequential textual ladder replaces the two-actor diagram.'),
('A large quiet word sits above two close, small actors with a short connection and generous space.','Major scale contrast; stillness is intentional after the concept ladder.'),
('A restrained association diagram joins response, closeness and satisfaction; a detached caveat remains below.','Evidence relationship, not a causal arrow or invented numerical chart.'),
('Large invitation quote broken into a readable editorial stack; a small open relational curve below.','Quoted speech leads without additional explanatory paragraph.'),
('Effort appears as a horizontal trace with several past marks and a present actor; recognition text sits above.','Time trace gives the acknowledgement a concrete referent.'),
('Two unequal vertical zones: enjoy the news, then make room to discuss worries; a curved route connects them.','Order diagram changes the axis and hierarchy of the preceding timeline.'),
('A first-person sharing quote sits low beside an outward gesture from one brick actor.','Asymmetric personal statement; one actor rather than a pair.'),
('Spare reflective question over a low, calm connected pair. No effects or unnecessary exit.','Question leads and deliberate stillness lets it land.')]
for i,d in enumerate(data):
    count=len(d['vo'].split());d['words']=words[idx:idx+count]
    assert [clean(x) for x in d['vo'].split()]==[clean(x['text']) for x in d['words']],d['id']
    d['word_start']=idx;d['word_end']=idx+count;idx+=count
    d['start']=0 if i==0 else pr+(words[d['word_start']-1]['end']+d['words'][0]['start'])/2
    d['composition'],d['visual_change']=layouts[i]
duration=math.ceil((pr+voice['duration_s']+tail)*30)/30
for i,d in enumerate(data):
    d['end']=data[i+1]['start'] if i+1<len(data) else duration;d['duration']=d['end']-d['start']
    def cue(index):return max(.2,min(d['duration']-.8,pr+d['words'][min(index,len(d['words'])-1)]['start']-d['start']))
    d['cue1']=cue(max(2,len(d['words'])//3));d['cue2']=cue(max(3,int(len(d['words'])*.68)))
    d['proof_at']=min(d['end']-.18,d['start']+max(d['cue2']+.65,d['duration']*.75))
timing=dict(duration=duration,pre_roll=pr,tail=tail,scenes=data)
(V/'timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf-8')
story='''---
format: 1080x1920
duration: 90s
message: "Kabar baik juga butuh disambut"
arc: good news → missed response → concept → engaged attention → concrete invitation → reflection
audience: Indonesian adults reflecting on everyday relationships
mode: autonomous
music: none
captions: enabled
---

# Storyboard — Kabar baik

Internal scene plan, agent-verified under delegated automation. No human sketch checkpoint requested. The board's canonical frame.md and shared chrome are inherited verbatim. Captions stay in y1550–1740; scene content stays in x88–936 / y230–1480.

## Video direction

Cream editorial field, charcoal pressure beat in frame 3, brick/sand organic faceless actors without gender coding. Newsreader leads reflection; DM Sans supports explanation. Fourteen distinct compositions vary actor presence, scale, alignment, density and diagram axis. Motion changes the meaning of distance/attention/connection. No B-roll, ornamental grain or generic floating decor. Hold intentionally after cues; no looping breathing or camera drift. Cuts preserve fixed chrome.

Catalog searched before custom graphics; titlecard-calm and line-by-line-slide primitives installed. Their restrained reveal mechanics are adapted to board typography and measured word cues. The organic relationship actors are board-native custom forms; catalog results did not provide that semantic treatment and a gap was reported. Motion recipes: svg-path-draw and spring-pop-entrance (smooth, no overshoot). Native delegation is not authorized; frame construction uses the documented inline serial fallback.

Audio: one continuous ElevenLabs eleven_v4 recording, project-env voice, native speed; no BGM. Sparse frozen board SFX will mark only concrete attention/connection events. Final reflection and uncued scenes stay quiet. No fabricated listening or human approval. Measured narration 84.48 s; preroll 0.30 s and tail 1.32 s; total 86.10 s.

'''
for d in data:
    c1=d['cue1'];c2=d['cue2'];du=d['duration']
    story+=f'''## Frame {d['number']} — {d['title']}

- status: outline
- src: compositions/frames/{d['id']}.html
- duration: {du:.6f}s
- poster: {d['proof_at']-d['start']:.3f}s
- transition_in: cut
- scene: {d['composition']}
- voiceover: "{d['vo']}"
- type: {'hook' if d['number']==1 else 'outro' if d['number']==14 else 'feature_showcase'}
- persuasion: concrete scenario and bounded explanation
- beat: {d['layout']}
- blueprint: compose
- focal: {d['text']}
- roles: main typography = foreground subject; relational form/path = supporting explanation; flat field = intentional background
- asset_candidates: []
- layout: {d['layout']}
- visual_change: {d['visual_change']}
- word_range: {d['word_start']}–{d['word_end']-1}
- absolute_time: {d['start']:.3f}–{d['end']:.3f}s
- screen_copy: {d['text']}
- support_copy: {d['support'] or 'none'}

Scene 1 (0.0–{c1:.3f}s): Establish the first named subject in the composition described above. Restrained titlecard-calm arrival; only the opening thought is present.
Scene 2 ({c1:.3f}–{c2:.3f}s): Develop the relational action as the spoken example or definition reaches it. Smooth transform movement and SVG path draw, with no diagnostic color meaning.
Scene 3 ({c2:.3f}–{du:.3f}s): Reveal the support/qualifier or final line on its measured word cue; hold the resolved pose still. The next scene owns the cut. {'The final question holds with no SFX.' if d['number']==14 else ''}

'''
(V/'STORYBOARD.md').write_text(story,encoding='utf-8')
print(json.dumps(dict(narration=voice['duration_s'],duration=duration,word_count=len(words),scenes=[dict(id=d['id'],start=round(d['start'],3),duration=round(d['duration'],3)) for d in data])))
