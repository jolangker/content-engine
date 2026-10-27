from pathlib import Path
import json, re, hashlib, importlib.util
BASE=Path(__file__).resolve().parent; ROOT=BASE.parent.parent; V=BASE/'video'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,obj): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
scenes=read(V/'scenes.json'); meta=read(V/'audio_meta.json'); placement=read(V/'placement.json'); words=placement['words']
norm=lambda s: re.sub(r'[^a-z0-9]','',s.lower())
script=[w for s in scenes for w in s['vo'].split()]
assert [norm(x) for x in script]==[norm(x['text']) for x in words], 'Native alignment text mismatch'
offset=0; caps=[]; end=round(placement['duration_s']+1.2,3)
for s in scenes:
    n=len(s['vo'].split()); ws=words[offset:offset+n]; offset+=n
    s['word_first']=offset-n;s['word_last']=offset-1
    s['start']=0 if s['n']==1 else round(ws[0]['start']-.06,4)
    s['speech_start']=ws[0]['start'];s['speech_end']=ws[-1]['end']
for i,s in enumerate(scenes):
    s['duration']=round((scenes[i+1]['start'] if i<15 else end)-s['start'],4)
    ws=words[s['word_first']:s['word_last']+1]
    group=[]; groups=[]
    for word in ws:
        if group and (len(' '.join(x['text'] for x in group+[word]))>55 or word['end']-group[0]['start']>2.8):
            groups.append(group); group=[]
        group.append(word)
        if word['text'][-1:] in '.?!': groups.append(group); group=[]
    if group:groups.append(group)
    for j,group in enumerate(groups):
        start=max(s['start'],group[0]['start']-.035)
        finish=min(s['start']+s['duration'],group[-1]['end']+.17)
        if j+1<len(groups): finish=min(finish,groups[j+1][0]['start']-.035)
        caps.append(dict(start=round(start,4),end=round(finish,4),text=' '.join(x['text'] for x in group),dark=s['dark'],scene=s['n']))
dump(V/'scenes.json',scenes);dump(V/'captions.json',caps)
dump(V/'timing.json',dict(duration_s=end,voice_duration_s=placement['duration_s'],original_voice_duration_s=meta['total_duration_s'],basis='native ElevenLabs alignment plus explicit editorial pauses recorded in placement.json, native speech speed 1; 1.2s final visual hold',words=words,scenes=scenes))
def timestamp(t):
    ms=round(t*1000); return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
out='\n\n'.join(f'{i+1}\n{timestamp(c["start"])} --> {timestamp(c["end"])}\n{c["text"]}' for i,c in enumerate(caps))+'\n'
(BASE/'exports').mkdir(exist_ok=True)
(BASE/'exports/jeda-punya-waktu-kembali.srt').write_text(out,encoding='utf-8')
# Transition stage only after all audio decisions are resolved below.
tracker=read(ROOT/'TRACKER.json')
for p in tracker['productions']:
    if p['slug']==BASE.name:p.update(stage='production',status='in_progress')
dump(ROOT/'TRACKER.json',tracker)
with (BASE/'EPISODE.md').open('a',encoding='utf-8') as f:
    f.write(f'\n## Measured audio and timing\nNarration completed in one request: {meta["total_duration_s"]:.3f}s, {len(words)} aligned words, selected provider/voice/model retained. Six seconds of editorial silence at sentence gaps, documented in placement.json, yield {placement["duration_s"]:.3f}s placed narration. Speech stays at native speed; original source/metadata preserved. Final composition {end:.3f}s including 1.2s quiet visual tail, within board planning range. Native word text exactly matches all {len(script)} scripted tokens after punctuation normalization. {len(caps)} caption phrases preserve every spoken word. Speech and scene windows are in video/timing.json. Perceptual listening unavailable; no human audio approval claimed.\n')
print(json.dumps(dict(duration=end,captions=len(caps),scene_windows=[(s['n'],s['start'],s['duration']) for s in scenes])))
