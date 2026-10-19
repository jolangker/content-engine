"""Synchronize the approved storyboard to the one continuous voiceover.

This step assigns timing and scene direction; frame workers preserve the exact
approved static layouts. It never rewrites narration or generates more speech.
"""
from pathlib import Path
import json
import math
import re
import shutil

prod=Path(__file__).resolve().parent
video=prod/'video'
meta=json.loads((video/'audio_meta.json').read_text(encoding='utf-8'))
voice=meta['voices'][0]
words=voice['words']
copy=(prod/'SCRIPT.md').read_text(encoding='utf-8').split('## Reading copy\n\n',1)[1].split('\n## Timing and delivery',1)[0].strip()
paras=copy.split('\n\n')
norm=lambda s:re.sub(r'[^\w]','',s).casefold()
expected=copy.split()
assert len(words)==len(expected)==180
assert [norm(w['text']) for w in words]==[norm(w) for w in expected], 'Native alignment words differ from the approved script'
assert all('[' not in w['text'] and ']' not in w['text'] for w in words)
frames=json.loads((video/'storyboard-data.json').read_text(encoding='utf-8'))
voice_offset=0.4
total=math.ceil((voice_offset+voice['duration_s']+1.2)*30)/30
counts=[len(p.split()) for p in paras]
indices=[0]
for c in counts:indices.append(indices[-1]+c)
starts=[0.0]
for i in indices[1:-1]:
    boundary=voice_offset+(words[i-1]['end']+words[i]['start'])/2
    starts.append(round(boundary*30)/30)
ends=starts[1:]+[total]

# Concrete reveal directions are paced to paragraph-local native word timings.
directions=[
 ['Establish both solid actors and the short observation segment with the main headline.','On “udah kebayang”, reveal the italic imagined-future phrase, then trace the dashed arch without changing its final geometry.','Land the two labels and let the contrast between the short solid segment and large imagined arch read.'],
 ['Bring in the coffee headline and solid connection as the remembered preference is spoken.','At “Di kepala lo”, reveal the dashed thought container; on “Dia pasti”, reveal the italic thought phrase.','Land the interpretation label at the end of the thought, preserving the approved diagram scale.'],
 ['Hold the solid person and the headline, then open the first unknown as the speaker says “perbedaan”.','Reveal the second connector and label on “menepati janji”.','Reveal the final connector and label on “menghormati batas”; unknowns remain open, not negative.'],
 ['Introduce the main reflection and the already-experienced short solid segment.','On “belum kalian alami”, reveal the dashed extension progressively in its approved location.','At “lo isi sendiri”, land the imagined-connection label and hold the incomplete relationship.'],
 ['Introduce the concept title without diagnosing a person.','Reveal “Terpaku pada seseorang” with the first attention path on its spoken phrase; add “Sangat ingin dibalas” on the reciprocation cue.','On “kepikiran” and “mengalihkan”, add the last attention path and label; preserve the still endpoint positions.'],
 ['Deliberate restrained frame: both solid actors enter with the open interval and question.','The question remains unanswered as “perasaan dia” is spoken.','Land the small uncertainty label; settle into a readable hold, with no idle floating.'],
 ['Reveal the headline and compact conversation fragment.','On “baca ulang”, draw the return path; show the “dibaca lagi” label on that cue.','On “respons hangat” and “harapan”, reveal the outlined possibility and its label; do not move the bubble.'],
 ['Keep the approved charcoal ground and establish the two solid actors plus the title.','On “mencari penjelasan”, trace the imagined routes sequentially, preserving dashed appearance.','On “kemungkinan”, reveal “Mungkin…” and the small explanation label; land with visible tension, no perpetual motion.'],
 ['Introduce the headline and the short solid shared experience.','As “versi hubungan” is spoken, draw the much larger imagined outline around the actors.','On “belum pernah kalian jalani”, land the experience label inside the outline and hold the distinction.'],
 ['Deliberate qualification frame: introduce the headline and the imagined-future outline.','On “belum cukup”, reveal the open gap/question rather than a diagnostic equivalence.','Land the concept label and supporting copy, then hold still for the viewer to read the qualification.'],
 ['Introduce the headline and simple day line, with the attention path only beginning to form.','On “sulit pikiran itu dialihkan”, draw the attention interruption and reveal the first reflective question.','On “dampaknya ke keseharian”, reveal the second question; never add scores, thresholds, or diagnostic gauges.'],
 ['Introduce “Coba pisahkan” and the common trunk.','On “apa yang dia lakukan”, draw the solid observation branch and reveal its matching label.','On “apa yang lo harapkan”, reveal the dashed expectation branch and its label; the final layout stays exactly the approved split.'],
 ['Introduce the coffee-versus-compatibility headline, then reveal the actual-event band with “Dia inget kopi gue”.','On “Dia pasti cocok”, reveal the conclusion band and its italic quotation.','On “perlu diuji lewat saling mengenal”, land both actors and the modest solid segment; preserve all quote line breaks.'],
 ['Deliberate reflective close: reveal the question in its approved line groups, paced to the actual spoken question.','Reveal both actual actors and the modest shared segment on “bangun berdua”.','Allow the quiet ending pad; do not invent a complete reciprocal relationship or fade out essential copy early.'],
]

approved=video/'approved-static'
approved.mkdir(exist_ok=True)
for f in frames:
    target=approved/Path(f['src']).name
    if not target.exists():shutil.copy2(video/f['src'],target)

sbpath=video/'STORYBOARD.md'
sb=sbpath.read_text(encoding='utf-8')
blocks=re.split(r'(?m)(?=^## Frame \d+:)',sb)
intro=blocks[0]
intro=re.sub(r'(?m)^duration: .*',f'duration: {total:.3f}s',intro)
intro=intro.split('# Limerence — storyboard v1',1)[0]+'''# Limerence — approved layouts, narrated motion plan

The user approved all 14 styled static layouts on 2026-10-19. Preserve their placement, hierarchy, type, palette, and copy. Real timing comes from one continuous ElevenLabs/Brian/eleven_v4 recording (83.76 seconds), with 0.4 seconds of preroll and 1.2 seconds of ending room. Do not resynthesize or time-stretch to fit the earlier 90-second estimate.

## Video direction

Palette and fonts are fixed in frame.md. These are confirmed sketches: animate the existing elements, not a redesigned layout. Observations and real actors stay solid; imagined connections remain visibly dashed/open throughout the reveal. Keep the one charcoal frame 08.

Reveal model: per-cue layer reveals → dynamic-content-sequencing; SVG self-draw → svg-path-draw. The selected registry component svg-stroke-trace supplies the measured-length mechanism (installed in compositions/components/svg-stroke-trace.html). Apply that mechanism to the existing paths, not its demo shape or default colors. For dashed paths, preserve the approved dash pattern with a measured white-stroke mask, or use a simple opacity reveal; never replace imagined dashes with a solid stroke. Measure geometry once at setup. No moving text along a path, no camera moves, no layout shifts, no generic glow/bounce/noise.

Narration timing is the cue clock; each frame below carries its actual local words. Hero text must become visible by 0.5 seconds; supporting elements reveal as their phrase arrives, across the full frame. Use restrained long-tail entrances with settled endpoints. Every landed state must match its approved still. Deliberate quiet holds: 06, 10, and 14. No independent floating or repetitive breathing. Do not author between-frame transitions or non-final exits; current transition_in: cut is preserved.

Captions are enabled on a separate root track at y=1570–1760. Preserve the approved decorative series footer below the caption region; its placement is part of the user's approved board and it does not compete with narration. Do not add captions or audio in frame files.

'''
newblocks=[]
for i,(f,p,start,end,block) in enumerate(zip(frames,paras,starts,ends,blocks[1:])):
    dur=end-start
    local=[]
    for w in words[indices[i]:indices[i+1]]:
        local.append({'text':w['text'],'start':round(w['start']+voice_offset-start,3),'end':round(w['end']+voice_offset-start,3)})
    f.update(start=round(start,6),end=round(end,6),duration=round(dur,6),poster=round(start+dur*.82,6),words=local)
    block=re.sub(r'^## Frame .*',f'## Frame {i+1}: {f["title"]} ({start:.3f}-{end:.3f}s)',block,count=1)
    block=re.sub(r'(?m)^- duration: .*',f'- duration: {dur:.6f}s',block)
    block=re.sub(r'(?m)^- poster: .*',f'- poster: {f["poster"]:.6f}',block)
    block=block.split('Static pose:',1)[0].rstrip()+'\n\n'
    block+=f'- blueprint: compose\n- focal: the existing approved headline and relational diagram\n- roles: headline = foreground subject; actors and connectors = foreground subject; labels = supporting; cream/charcoal = full-bleed background\n- motion_rules: svg-path-draw, dynamic-content-sequencing\n- source_observation: approved-static/{Path(f["src"]).name}\n\n'
    cuts=[0,dur*.29,dur*.66,dur]
    for j,d in enumerate(directions[i]):
        block+=f'Scene {j+1} ({cuts[j]:.3f}–{cuts[j+1]:.3f}s): {d} Keep the approved editorial framing and hierarchy; use per-cue layer reveals → dynamic-content-sequencing and selective SVG self-draw → svg-path-draw. The windows guide rhythm; the actual word cues below take precedence.\n\n'
    block+='Native word cues (frame-local seconds):\n\n'+json.dumps(local,ensure_ascii=False)+'\n\n'
    newblocks.append(block)
sbpath.write_text(intro+''.join(newblocks),encoding='utf-8')
(video/'storyboard-data.json').write_text(json.dumps(frames,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(video/'timing.json').write_text(json.dumps({'voice_offset':voice_offset,'voice_duration':voice['duration_s'],'duration':total,'fps':30,'frames':[{k:f[k] for k in ['i','src','start','end','duration','poster','words']} for f in frames]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'word_match':True,'words':len(words),'frames':len(frames),'voice_duration':voice['duration_s'],'total_duration':total,'durations':[round(f['duration'],3) for f in frames]}))
