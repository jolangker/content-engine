"""Create measured captions and the independently verified local SFX plan."""
from pathlib import Path
import hashlib
import html
import importlib.util
import json
import re

P=Path(__file__).resolve().parent;V=P/'video';ROOT=P.parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    timing=json.loads((V/'timing.json').read_text(encoding='utf-8'))
    scenes=timing['scenes'];words=timing['words'];duration=timing['duration_s'];groups=[]
    for scene in scenes:
        current=[]
        for w in words[scene['word_start']:scene['word_end']]:
            if current and (len(current)>=5 or len(' '.join(x['text'] for x in current+[w]))>34 or w['start']-current[-1]['end']>.18):
                groups.append({'scene':scene['id'],'words':current});current=[]
            current.append(w)
            if re.search(r'[.?!:]$',w['text']):groups.append({'scene':scene['id'],'words':current});current=[]
        if current:groups.append({'scene':scene['id'],'words':current})
    elements=[]
    for i,g in enumerate(groups):
        ws=g['words'];start=max(.1,ws[0]['start']);end=ws[-1]['end']+.10
        if i+1<len(groups):end=min(end,groups[i+1]['words'][0]['start'])
        end=min(end,scenes[g['scene']-1]['end']);end=max(end,start+.03)
        text=' '.join(w['text'] for w in ws);color='#F3EDE3' if g['scene'] in (8,10) else '#302B28'
        elements.append(f'<div id="caption-{i:03d}" class="clip caption-group" data-start="{start:.5f}" data-duration="{end-start:.5f}" data-track-index="0" data-layout-allow-caption-zone="true" style="color:{color}">{html.escape(text)}</div>')
        g.update(start=start,end=end,text=text)
    body='''<!doctype html><html lang="id"><head><meta charset="UTF-8"></head><body><template><style>
    @font-face{font-family:'DM Sans';src:url('assets/fonts/dm-sans.ttf')}
    #root{position:absolute;inset:0;width:1080px;height:1920px;pointer-events:none;font-family:'DM Sans',sans-serif}
    .caption-group{position:absolute;left:88px;top:1550px;width:848px;min-height:115px;text-align:center;font:500 46px/1.25 'DM Sans',sans-serif;overflow:visible;}
    </style><div id="root" data-composition-id="captions" data-start="0" data-duration="'''+str(duration)+'''" data-width="1080" data-height="1920">'''+''.join(elements)+'''</div><script>const tl=gsap.timeline({paused:true});tl.to({},{duration:'''+str(duration)+'''},0);window.__timelines=window.__timelines||{};window.__timelines.captions=tl;</script></template></body></html>'''
    (V/'compositions/captions.html').write_text(body,encoding='utf-8')
    (V/'caption_groups.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    manifest=json.loads((V/'assets/board/audio/sfx/manifest.json').read_text(encoding='utf-8'))
    assets=[{'id':a['id'],'path':f"assets/board/audio/sfx/{a['file']}",'sha256':a['sha256'],'duration':a['duration'],'source':{'board':'ruang-di-antara visual v1.2','provenance':a['source'],'credits':'assets/board/audio/sfx/CREDITS.md'}} for a in manifest['assets']]
    requests=[(1,'contact',.12,'the cancellation stroke lands on the calendar'),(3,'air',.45,'the boundary opens between internal experience and external view'),(7,'air',.38,'the reverse view reveals the short visible answer'),(12,'contact',.12,'the explicit feeling gains a speaking space'),(13,'contact',.40,'the second cup returns as the shared-time context is named'),(14,'connection',.70,'a return speaking space appears for the other participant')]
    cues=[]
    for i,(n,a,f,purpose) in enumerate(requests,1):
        s=scenes[n-1];asset=next(x for x in assets if x['id']==a)
        cues.append({'id':f'sfx-{i:02d}-{a}','asset':a,'scene':f'f{n:02d}','purpose':purpose,'trigger':f'Frame {n:02d} visual beat at {f:.2f} of measured scene duration','start':round(s['start']+s['duration']*f+.03333,5),'duration':asset['duration'],'volume':.50 if a!='air' else .48,'track':4})
    helper=ROOT/'.agents/skills/shortform-production/scripts/sound_design.py'
    spec=importlib.util.spec_from_file_location('sound_plan',helper);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    plan={'version':1,'decisions':{'narration':{'mode':'use','reason':'Continuous native-speed ElevenLabs narration with explicit measured editorial pauses, including a longer question and two turns; no time stretching.'},'bgm':{'mode':'none','reason':'Unfilled pauses make room to distinguish internal feeling from external information; a music bed could prescribe an interpretation of the partner.'},'sfx':{'mode':'use','reason':'Six frozen licensed material cues follow actual cancellation, viewpoint shifts, speaking and response actions; no automatic transition sounds.'}},'timing_sha256':digest(V/'timing.json'),'narration_sha256':digest(V/'assets/audio/narration.wav'),'motion_sources':{f'compositions/frames/f{i:02d}.html':mod.motion_digest(V/f'compositions/frames/f{i:02d}.html') for i in range(1,17)},'assets':assets,'cues':cues,'silence':'No SFX under the uncertain-meaning charcoal frame 08 or the distinction frame 10. The final reflective hold stays quiet. No BGM throughout.'}
    (V/'sound_design.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for scene in scenes:
        n=scene['id']; assertions=[{'kind':'appearsBy','selector':'#drawing','bySec':.1}]
        if n!=8:assertions.append({'kind':'before','a':'#beat2','b':'#beat3'})
        (V/f'compositions/frames/f{n:02d}.motion.json').write_text(json.dumps({'duration':scene['duration'],'assertions':assertions},indent=2)+'\n',encoding='utf-8')
    root_assertions=[{'kind':'before','a':f'#scene-{n:02d} #beat2','b':f'#scene-{n:02d} #beat3'} for n in (1,2,4,7,12,14)]
    root_assertions.append({'kind':'keepsMoving','withinSelector':'#root','maxStaticSec':3.2})
    (V/'index.motion.json').write_text(json.dumps({'duration':duration,'assertions':root_assertions},indent=2)+'\n',encoding='utf-8')
    e=P/'exports';e.mkdir(exist_ok=True)
    def stamp(t):
        ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
    srt='\n\n'.join(f"{i+1}\n{stamp(g['start'])} --> {stamp(g['end'])}\n{g['text']}" for i,g in enumerate(groups))+'\n'
    (e/'gua-kira-udah-kelihatan.srt').write_text(srt,encoding='utf-8')
    print(json.dumps({'caption_groups':len(groups),'caption_words':sum(len(g['words']) for g in groups),'sfx_cues':len(cues),'duration':duration}))

if __name__=='__main__':main()
