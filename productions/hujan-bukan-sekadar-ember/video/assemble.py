from pathlib import Path
import json,re,html,subprocess,hashlib,shutil
V=Path(__file__).resolve().parent;P=V.parent;R=P.parents[1]
plan=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'));meta=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'))
voice=meta['voices'][0];words=voice['words'];offset=.35
clean=lambda s:re.sub(r'[^\w]','',s.lower())
expected=[clean(w) for s in plan for w in s['vo'].split()]
assert expected==[clean(w['text']) for w in words],'Native alignment differs from the locked script'
total=voice['duration_s']+offset+1.7
starts=[];ends=[];count=0
for i,s in enumerate(plan):
    s['word_start']=count;s['word_end']=count+len(s['vo'].split())-1
    s['start']=0 if i==0 else words[count]['start']+offset
    count+=len(s['vo'].split());starts.append(s['start'])
for i,s in enumerate(plan):
    s['end']=starts[i+1] if i+1<len(plan) else total;s['duration']=s['end']-s['start'];ends.append(s['end'])
def cue(phrase,scene_index=0):
    seek=[clean(w) for w in phrase.split()];s=plan[scene_index]
    for i in range(s['word_start'],s['word_end']-len(seek)+2):
        if expected[i:i+len(seek)]==seek:return round(words[i]['start']+offset,4)
    raise ValueError(f'Missing cue {phrase}')
cues={'gutter':cue('Jadi kumpulkan'),'tank':cue('lalu arahkan'),'screen':cue('Kita pasang',1),'dust':cue('Masalahnya',1),'firstflush':cue('Jadi aliran awal',2),'fill':cue('terisi lebih dulu',2),'bypass':cue('air berikutnya',2),'drain':cue('Setelah hujan',2),'bug':cue('Eh ada',3),'lid':cue('Jadi tutup',3),'opaque':cue('Dinding yang',3),'full':cue('Kalau tangki penuh',4),'overflow':cue('Kita tambahkan',4),'overflowmesh':cue('Jalur keluar',4),'pour':cue('menyiram',5),'maintain':cue('Bersihkan talang',5),'nonpotable':cue('Ini sistem',5),'sit':cue('Nah sekarang',5)}
(V/'scene-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
(V/'cues.json').write_text(json.dumps(cues,indent=2),encoding='utf-8')
meta['export_duration']=total;meta['narration_offset']=offset;meta['measured_scene_ranges']=plan
(V/'audio_meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
# Native source remains immutable. Normalization changes gain, not speed, words or timing.
dest=V/'assets/audio/narration-master.wav'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(V/voice['path']),'-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-ac','1',str(dest)],check=True)
groups=[];g=[]
for i,w in enumerate(words):
    if g and (len(' '.join(x['text'] for x in g))+1+len(w['text'])>26 or len(g)>=5):groups.append(g);g=[]
    g.append(w)
    if re.search(r'[.!?]$',w['text']) or i in [s['word_end'] for s in plan]:groups.append(g);g=[]
if g:groups.append(g)
def stamp(t):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
caption_html=[];srt=[];manifest=[]
for i,g in enumerate(groups):
    start=g[0]['start']+offset;end=min(voice['duration_s']+offset,g[-1]['end']+offset+.04);text=' '.join(w['text'] for w in g)
    caption_html.append(f'<div id="cap-{i:03}" class="clip" data-start="{start:.4f}" data-duration="{end-start:.4f}" data-track-index="0"><div class="spoken">{html.escape(text)}</div></div>')
    srt.append(f'{i+1}\n{stamp(start)} --> {stamp(end)}\n{text}\n')
    manifest.append(dict(id=i,start=start,end=end,text=text))
assert ' '.join(x['text'] for x in manifest)==' '.join(w['text'] for w in words)
(V/'caption_groups.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'exports').mkdir(exist_ok=True);(P/'exports/hujan-bukan-sekadar-ember.srt').write_text('\n'.join(srt),encoding='utf-8')
(V/'compositions/frames').mkdir(parents=True,exist_ok=True)
caption_doc='<template><div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="'+str(total)+'" style="width:100%;height:100%;position:relative">'+''.join(caption_html)+'<script>const tl=gsap.timeline({paused:true});tl.to({}, {duration:'+str(total)+'});window.__timelines.captions=tl;</script></div></template>'
(V/'compositions/captions.html').write_text(caption_doc,encoding='utf-8')
(V/'captions.mount.txt').write_text(f'<div id="caption-track" data-track-kind="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{total}" data-width="1080" data-height="1920" data-track-index="3"></div>',encoding='utf-8')
# Six bounded frame packets are implemented inline in sequence: native dispatch permission was not separately granted.
for i,s in enumerate(plan):
    sec='<div class="section-tag">POTONGAN</div>' if i in (2,4) else ''
    doc=f'''<template><div id="root" data-composition-id="{s['id']}" data-width="1080" data-height="1920" data-duration="{s['duration']:.4f}">
<style>#root{{width:100%;height:100%;position:relative}}.scene-heading{{position:absolute;left:72px;top:224px;font-family:Barlow,sans-serif;font-weight:900;font-size:64px;line-height:1.02;max-width:840px;margin:0;color:#173B42}}.scene-note{{position:absolute;left:72px;bottom:335px;max-width:800px;background:#FFF5DE;padding:14px 21px;border-radius:12px;font-family:Barlow,sans-serif;font-size:34px;font-weight:700;line-height:1.14;border-left:7px solid #178A91;color:#173B42}}.section-tag{{position:absolute;right:160px;top:565px;font-family:'IBM Plex Mono',monospace;font-size:28px;letter-spacing:1px;padding:12px;background:#FFF5DE;border-radius:6px;color:#173B42}}</style>
<div class="clip" data-start="0" data-duration="{s['duration']:.4f}"><h1 id="{s['id']}-heading" class="scene-heading">{html.escape(s['title'])}</h1><div id="{s['id']}-note" class="scene-note">{html.escape(s['label'])}</div>{sec}</div>
<script>const tl=gsap.timeline({{paused:true}});tl.fromTo('#{s['id']}-heading',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.35,ease:'power3.out'}},.03);tl.fromTo('#{s['id']}-note',{{opacity:0,y:12}},{{opacity:1,y:0,duration:.4,ease:'power3.out'}},.15);window.__timelines['{s['id']}']=tl;</script></div></template>'''
    faces="@font-face{font-family:Barlow;src:url('../../assets/fonts/barlow-bold.ttf');font-weight:700}@font-face{font-family:Barlow;src:url('../../assets/fonts/barlow-black.ttf');font-weight:900}@font-face{font-family:'IBM Plex Mono';src:url('../../assets/fonts/ibm-plex-mono.ttf');font-weight:400}"
    doc=doc.replace('<style>','<style>'+faces).replace(f'id="{s["id"]}-',f'id="el-{s["id"]}-').replace(f"'#{s['id']}-",f"'#el-{s['id']}-").replace('<div class="clip"',f'<div id="el-{s["id"]}-content" class="clip"')
    (V/'compositions/frames'/f"{s['id']}.html").write_text(doc,encoding='utf-8')
rain=V/'assets/audio/rain-loop.mp3';duration=12
sound=dict(version=1,decisions=dict(narration=dict(mode='use',provider=meta['tts_provider'],voice=meta['voice_id'],model=meta['tts_model'],speed=1,offset=offset),bgm=dict(mode='none',reason='Leave the teaching chain and comic interruption unscored.'),sfx=dict(mode='use',reason='Restrained rain supports the changing environment; dip at the visitor reaction and stop after rain. No unverified mechanical or wing recording is implied. Additional planned placement/trickle accents intentionally omitted to keep speech clear.')),assets=[],cues=[],creative_listening='No perceptual audio input available. Full-file decode, native word alignment, independent local ASR, waveform and final mix measurements are used; these do not certify prosody or subjective balance.')
sound['assets'].append(dict(path='assets/audio/rain-loop.mp3',sha256=hashlib.sha256(rain.read_bytes()).hexdigest(),source='ElevenLabs eleven_text_to_sound_v2',request='assets/audio/rain-loop.json'))
# Freeze repeated bytes into a single finite ambience bed; gaps are native track envelopes.
rainEnd=starts[5]
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-stream_loop','-1','-i',str(rain),'-t',str(rainEnd),'-af',f'loudnorm=I=-25:TP=-4:LRA=11,apad,atrim=0:{rainEnd}','-ar','48000',str(V/'assets/audio/rain-bed.wav')],check=True)
points=[dict(t=0,v=0),dict(t=.8,v=.09),dict(t=cues['drain']-.3,v=.09),dict(t=cues['drain']+.2,v=0),dict(t=starts[3],v=0),dict(t=cues['bug']+2.5,v=0),dict(t=cues['bug']+3,v=.07),dict(t=starts[5]-.5,v=.07),dict(t=starts[5],v=0)]
points=sorted(points,key=lambda x:x['t'])
probe=json.loads(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(V/'assets/audio/rain-bed.wav')],capture_output=True,text=True,check=True).stdout)
rainSlot=float(probe['format']['duration'])
points[-1]['t']=rainSlot
auto=html.escape(json.dumps(dict(version=1,lanes=[dict(target='volume',points=points)])),quote=True)
tags=f'<audio id="narration" src="assets/audio/narration-master.wav" data-start="{offset}" data-duration="{voice["duration_s"]}" data-track-index="10" data-volume="1"></audio>\n<audio id="rain-ambience" src="assets/audio/rain-bed.wav" data-start="0" data-duration="{rainSlot}" data-track-index="12" data-volume="1" data-automation="{auto}"></audio>'
(V/'audio-tags.html').write_text(tags,encoding='utf-8')
sound['cues']=[dict(id='rain-ambience',start=0,end=rainSlot,envelope=points,path='assets/audio/rain-bed.wav')];sound['narration_sha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
(V/'sound_design.json').write_text(json.dumps(sound,ensure_ascii=False,indent=2),encoding='utf-8')
story=(V/'STORYBOARD.md').read_text(encoding='utf-8')
for i,s in enumerate(plan):
    pattern=rf'(## Frame {i+1} — .*?)(?=\n## Frame |\Z)'
    match=re.search(pattern,story,re.S);block=match.group(1)
    block=re.sub(r'- duration: [^\n]+',f"- duration: {s['duration']:.4f}s",block);block=re.sub(r'- start: [^\n]+',f"- start: {s['start']:.4f}s",block);block=block.replace('- status: built','- status: animated')
    block+=f"\nMeasured timing: {s['start']:.4f}–{s['end']:.4f}s, native words {s['word_start']}–{s['word_end']}. Native speech offset {offset}s. Cues in cues.json override estimated timing fractions.\n"
    story=story[:match.start()]+block+story[match.end():]
(V/'STORYBOARD.md').write_text(story,encoding='utf-8')
print(json.dumps(dict(duration=total,starts=starts,ends=ends,cues=cues,caption_groups=len(groups),aligned_words=len(words)),indent=2))
