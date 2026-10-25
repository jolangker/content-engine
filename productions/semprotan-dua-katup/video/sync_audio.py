from pathlib import Path
import json,re,hashlib,subprocess,difflib
V=Path(__file__).resolve().parent;R=V.parent.parent.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'));v=m['voices'][0]
out=V/'assets/audio/narration-master.wav';out.parent.mkdir(exist_ok=True)
tempo=1.20;offset=.3
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(V/v['path']),'-af',f'atempo={tempo},loudnorm=I=-16:TP=-1.5:LRA=7','-ar','44100','-ac','1',str(out)],check=True)
duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(out)]))
assert offset+duration<90
m['placed_narration']=dict(path=out.relative_to(V).as_posix(),sha256=sha(out),duration_s=duration,source_path=v['path'],source_sha256=sha(V/v['path']),tempo=tempo,offset=offset,pitch_preserved=True,paid_resynthesis=False)
(V/'audio_meta.json').write_text(json.dumps(m,indent=2,ensure_ascii=False),encoding='utf-8')
p=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'));words=v['words']
norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower())
expected=[norm(w) for s in p['scenes'] for w in s['vo'].split()]
observed=[norm(w['text']) for w in words]
assert expected==observed, list(difflib.unified_diff(expected,observed))[:12]
count=0;boundaries=[]
for s in p['scenes']:
    n=len(s['vo'].split());s['word_start']=count;s['word_end_exclusive']=count+n
    boundaries.append(0 if not count else round((words[count-1]['end']+words[count]['start'])/2/tempo+offset,3))
    count+=n
boundaries.append(90)
caps=[]
for i,s in enumerate(p['scenes']):
    s['start']=boundaries[i];s['duration']=round(boundaries[i+1]-boundaries[i],3)
    ws=words[s['word_start']:s['word_end_exclusive']];group=[]
    def flush():
        if group:
            caps.append(dict(text=' '.join(w['text'] for w in group),start=group[0]['start']/tempo+offset,end=min(89.8,group[-1]['end']/tempo+offset+.09)))
            group.clear()
    for w in ws:
        if group and (len(' '.join(x['text'] for x in group))+len(w['text'])>40 or len(group)>=6):flush()
        group.append(w)
        if w['text'].endswith(('.', '?', '!')):flush()
    flush()
for a,b in zip(caps,caps[1:]):a['end']=min(a['end'],b['start']-.012)
p.update(captions=caps,tempo=tempo,narration_offset=offset,source_audio_sha256=sha(V/v['path']))
(V/'timing.json').write_text(json.dumps(p,indent=2,ensure_ascii=False),encoding='utf-8')
sb=(V/'STORYBOARD.md').read_text(encoding='utf-8')
for s in p['scenes']:
    pattern=r'(## Frame '+str(s['number'])+r' — .*?)(?=\n## Frame |\Z)'
    def update(mt):
        block=mt[0];block=re.sub(r'- duration: .*',f'- duration: {s["duration"]}s',block);block=re.sub(r'- start: .*',f'- start: {s["start"]}s',block)
        block=re.sub(r'- poster: .*',f'- poster: {s["duration"]*.6:.3f}s',block)
        return block+f'\nMeasured narration words: [{s["word_start"]}, {s["word_end_exclusive"]}); source native alignment divided by {tempo}, placed at {offset}s.\n'
    sb=re.sub(pattern,update,sb,flags=re.S)
(V/'STORYBOARD.md').write_text(sb,encoding='utf-8')
# Captions stay verbatim; delivery tags never enter them.
def stamp(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
ex=V.parent/'exports';ex.mkdir(exist_ok=True)
(ex/'semprotan-dua-katup.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(caps))+'\n',encoding='utf-8')
sound=dict(version=1,decisions=dict(narration=dict(mode='use',volume=.85,reason='Continuous Indonesian ElevenLabs eleven_v4; source 105.68s retained, pitch-preserving tempo 1.20 and normalization to -16 LUFS before placement.'),bgm=dict(mode='none',reason='Intentional unscored inspection bench; preserve speech and observation pauses.'),sfx=dict(mode='none',reason='Reuse scan found no project/global sprayer foley; bundled assets are UI, typing, whoosh and impacts. Generic UI clicks, whooshes and impacts do not fit liquid pumping; no calibrated sprayer recording found. Synthetic contact sounds would imply unsupported acoustics at slowed illustrative timing. Intentional silence between narration.')),assets=[],cues=[],timing_sha256=sha(V/'timing.json'),narration_sha256=sha(out),narration_processing=m['placed_narration'],creative_listening='Not available in this tool session; no perceptual approval claimed. Native alignment, decode, loudness and captions are verified objectively.')
(V/'sound_design.json').write_text(json.dumps(sound,indent=2),encoding='utf-8')
print(json.dumps(dict(native_duration=v['duration_s'],placed_duration=duration,tempo=tempo,scenes=len(p['scenes']),captions=len(caps),scene_durations=[s['duration'] for s in p['scenes']])) )
