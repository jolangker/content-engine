"""Build full captions and reconcile sparse local cues with the measured scene map."""
from pathlib import Path
import hashlib,html,json,re,sys
P=Path(__file__).resolve().parent;V=P/'video';ROOT=P.parents[1]
sys.path.insert(0,str(ROOT/'.agents/skills/shortform-production/scripts'))
import sound_design
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    timing=json.loads((V/'timing.json').read_text(encoding='utf-8'));scenes=timing['scenes'];words=timing['words'];duration=timing['duration_s'];groups=[]
    for scene in scenes:
        current=[]
        for w in words[scene['word_start']:scene['word_end']]:
            if current and (len(current)>=5 or len(' '.join(x['text'] for x in current+[w]))>34 or w['start']-current[-1]['end']>.22):
                groups.append(dict(scene=scene['id'],words=current));current=[]
            current.append(w)
            if re.search(r'[.?!:]$',w['text']):groups.append(dict(scene=scene['id'],words=current));current=[]
        if current:groups.append(dict(scene=scene['id'],words=current))
    nodes=[]
    for i,g in enumerate(groups):
        ws=g['words'];start=ws[0]['start'];end=min(ws[-1]['end']+.1,scenes[g['scene']-1]['end'])
        if i+1<len(groups):end=min(end,groups[i+1]['words'][0]['start'])
        assert end>start
        text=' '.join(w['text'] for w in ws);color='#F3EDE3' if g['scene'] in (8,13) else '#302B28'
        nodes.append(f'<div id="caption-{i:03d}" class="clip caption-group" data-start="{start:.17g}" data-duration="{end-start:.17g}" data-track-index="0" data-layout-allow-caption-zone="true" style="color:{color}">{html.escape(text)}</div>');g.update(start=start,end=end,text=text)
    (V/'compositions/captions.html').write_text('''<template><style>@font-face{font-family:'DM Sans';src:url('assets/fonts/dm-sans.ttf')}#root{position:absolute;inset:0;width:1080px;height:1920px;pointer-events:none;font-family:'DM Sans',sans-serif}.caption-group{position:absolute;left:88px;top:1550px;width:848px;min-height:115px;text-align:center;font:500 46px/1.25 'DM Sans',sans-serif;overflow:visible}</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="'''+str(duration)+'">'+''.join(nodes)+'''</div><script>const tl=gsap.timeline({paused:true});tl.to({},{duration:'''+str(duration)+'''},0);window.__timelines.captions=tl;</script></template>''',encoding='utf-8');dump(V/'caption_groups.json',groups)
    manifest=json.loads((V/'assets/board/audio/sfx/manifest.json').read_text(encoding='utf-8'))
    assets=[dict(id=a['id'],path=f"assets/board/audio/sfx/{a['file']}",sha256=a['sha256'],duration=a['duration'],source=dict(board='ruang-di-antara visual v1.2',provenance=a['source'],credits='assets/board/audio/sfx/CREDITS.md')) for a in manifest['assets']]
    requests=[(1,'contact',.43,'the handset enters attention during the dinner story'),(3,'air',.43,'the handset interrupts the conversation route'),(5,'air',.73,'the speaker returns toward the missed part of the story'),(10,'contact',.43,'the pressing phone reply is explicitly brought into the conversation'),(11,'contact',.73,'the handset settles beside the dinner setting'),(15,'connection',.73,'the reopened story route reaches the receiver')]
    cues=[]
    for i,(n,aid,f,purpose) in enumerate(requests,1):
        s=scenes[n-1];asset=next(a for a in assets if a['id']==aid)
        cues.append(dict(id=f'sfx-{i:02d}-{aid}',asset=aid,scene=f'f{n:02d}',purpose=purpose,trigger=f'Visual beat at {f:.2f} of measured scene {n:02d}',start=round(s['start']+s['duration']*f+.03333,8),duration=asset['duration'],volume=.50 if aid!='air' else .48,track=4))
    plan=dict(version=1,decisions=dict(narration=dict(mode='use',reason='Continuous ElevenLabs native-speed recording, measured quiet splices and one final normalization.'),bgm=dict(mode='none',reason='The dinner conversation and pauses remain exposed so the score does not prescribe a feeling or imply a magical repair.'),sfx=dict(mode='use',reason='Six restrained frozen material cues mark phone attention, interrupted direction, inquiry, setting the phone aside and the reopened story; no notification ping or transition quota.')),timing_sha256=digest(V/'timing.json'),narration_sha256=digest(V/'assets/audio/narration.wav'),motion_sources={f'compositions/frames/f{i:02d}.html':sound_design.motion_digest(V/f'compositions/frames/f{i:02d}.html') for i in range(1,17)},assets=assets,cues=cues,silence='No SFX in dark 08/13, needs discussion 14 or final hold 16; no BGM throughout.')
    dump(V/'sound_design.json',plan)
    for s in scenes:dump(V/f'compositions/frames/f{s["id"]:02d}.motion.json',dict(duration=s['duration'],assertions=[dict(kind='before',a=f'#f{s["id"]:02d}-beat2',b=f'#f{s["id"]:02d}-beat3')]))
    dump(V/'index.motion.json',dict(duration=duration,assertions=[dict(kind='before',a=f'#f{n:02d} #f{n:02d}-beat2',b=f'#f{n:02d} #f{n:02d}-beat3') for n in (1,3,6,11,12,13)]+[dict(kind='keepsMoving',withinSelector='#root',maxStaticSec=3.5)]))
    E=P/'exports';E.mkdir(exist_ok=True)
    def stamp(t):
        ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
    (E/f'{P.name}.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(g["start"])} --> {stamp(g["end"])}\n{g["text"]}' for i,g in enumerate(groups))+'\n',encoding='utf-8')
    assert sum(len(g['words']) for g in groups)==190
    print(json.dumps(dict(caption_groups=len(groups),caption_words=190,sfx_cues=len(cues),duration=duration)))
if __name__=='__main__':main()
