from pathlib import Path
import json,re,subprocess,hashlib
V=Path(__file__).resolve().parent
plan=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'))
meta=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'))
voice=meta['voices'][0]; words=voice['words'];rate=1.05;offset=.35
source=V/voice['path'];master=V/'assets/audio/narration-master.wav'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-af',f'atempo={rate},loudnorm=I=-16:TP=-1.5:LRA=7','-ar','48000','-ac','1',str(master)],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(master)]))
duration=float(probe['format']['duration']);assert duration+offset<89
norm=lambda t:re.sub(r'[^a-z0-9]','',t.lower())
cursor=0
for s in plan['scenes']:
    tokens=s['vo'].split(); n=len(tokens);got=words[cursor:cursor+n]
    assert [norm(t) for t in tokens]==[norm(w['text']) for w in got],s['id']
    s['word_first']=cursor;s['word_last']=cursor+n-1
    s['speech_start']=round(got[0]['start']/rate+offset,3)
    s['speech_end']=round(min(got[-1]['end']/rate,duration)+offset,3)
    cursor+=n
assert cursor==len(words)
for i,s in enumerate(plan['scenes']):s['start']=0 if i==0 else round(s['speech_start']-.10,3)
for i,s in enumerate(plan['scenes']):s['duration']=round((plan['scenes'][i+1]['start'] if i+1<len(plan['scenes']) else 90)-s['start'],3)
caps=[];pending=[]
for w in words:
    pending.append(w);text=' '.join(x['text'] for x in pending)
    if len(pending)>=5 or (len(pending)>=2 and (w['text'].endswith(('.',',','?')) or len(text)>36)):
        caps.append(pending);pending=[]
if pending:caps.append(pending)
groups=[]
for i,c in enumerate(caps):
    start=max(0,c[0]['start']/rate+offset-.025)
    end=min(c[-1]['end']/rate+offset+.12,duration+offset)
    if i+1<len(caps):end=min(end,caps[i+1][0]['start']/rate+offset-.02)
    assert end>start
    groups.append(dict(text=' '.join(w['text'] for w in c),start=start,end=end))
plan.update(captions=groups,narration_offset=offset,source_voice_duration=voice['duration_s'],voice_duration=duration,narration_rate=rate,timing_basis='Native word timestamps divided by the recorded 1.05 pitch-preserving tempo factor; no words removed. Each new shot leads its opening word by 100ms. Last shot holds its resolved seam through 90s.')
(V/'timing.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Preserve raw source metadata and source alignment. The placed master has its own measured record.
meta['placed_narration']=dict(path=master.relative_to(V).as_posix(),duration_s=duration,source=voice['path'],tempo=rate,pitch_preserved=True,sha256=hashlib.sha256(master.read_bytes()).hexdigest())
(V/'audio_meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def tc(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
exports=V.parent/'exports';exports.mkdir(exist_ok=True)
(exports/'satu-jahitan-mesin-jahit.srt').write_text('\n\n'.join(f"{i}\n{tc(c['start'])} --> {tc(c['end'])}\n{c['text']}" for i,c in enumerate(groups,1))+'\n',encoding='utf-8')
story=(V/'STORYBOARD.md').read_text(encoding='utf-8')
for s in plan['scenes']:
    pattern=rf"(## Frame {int(s['id'][1:])}: .*?\n)(.*?)(?=\n## Frame|\n## Sound|\Z)"
    def replace(m):
        b=m[2];b=re.sub(r'- duration: .*',f"- duration: {s['duration']}s",b);b=re.sub(r'- start: .*',f"- start: {s['start']}s",b)
        b=b.replace('- status: built','- status: animated')
        return m[1]+b+f"\nMeasured narration: words {s['word_first']}–{s['word_last']}; {s['speech_start']}–{s['speech_end']}s.\n"
    story=re.sub(pattern,replace,story,flags=re.S)
story+='\n## Measured audio\n\nOne ElevenLabs eleven_v4 full-script request, project-env voice. Native audio 91.60s; a 1.05 pitch-preserving tempo adjustment produces the placed master at '+str(duration)+'s without a second synthesis call. Source recording and source alignment are preserved; every caption and shot timestamp uses the same inverse tempo mapping. Narration starts at +0.35s. The final seam holds for observation through the exact 90-second endpoint. Static boards retain their original estimated timings as pre-audio planning evidence.\n'
(V/'STORYBOARD.md').write_text(story,encoding='utf-8')
plan_sound=dict(version=1,decisions=dict(narration=dict(mode='use',volume=.8,reason='One complete Indonesian narration; native source retained, pitch-preserving tempo 1.05 fits the fixed 90-second board; master normalized to -16 LUFS mono before gain.'),bgm=dict(mode='none',reason='Intentional unscored mechanical inspection, permitted by Di Balik Benda v3.'),sfx=dict(mode='none',reason='No supplied real sewing-machine acoustics; available UI effects do not fit the mechanism. Slowed thread paths should not invent machine impacts.')),assets=[],cues=[],timing_sha256=hashlib.sha256((V/'timing.json').read_bytes()).hexdigest(),narration_sha256=hashlib.sha256(master.read_bytes()).hexdigest(),narration_processing=dict(source=voice['path'],source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),output='assets/audio/narration-master.wav',output_sha256=hashlib.sha256(master.read_bytes()).hexdigest(),tempo=rate,pitch_preserved=True,paid_resynthesis=False))
(V/'sound_design.json').write_text(json.dumps(plan_sound,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
episode=V.parent/'EPISODE.md';episode.write_text(episode.read_text(encoding='utf-8')+f"\n## Audio v1\n\nProvider elevenlabs; voice {meta['voice_id']} resolved from root .env; model eleven_v4. One request produced 91.60s and 211 aligned spoken words, with tags excluded. A pitch-preserving 1.05 tempo adjustment fits the exact board duration without paid resynthesis; placed master {duration}s. All words and source audio preserved, word timestamps scaled consistently. Voice-only is intentional; no BGM/SFX cues planned. Audio has not been perceptually listened to.\n",encoding='utf-8')
tracker=V.parents[2]/'TRACKER.json';data=json.loads(tracker.read_text(encoding='utf-8-sig'));next(x for x in data['productions'] if x['slug']==V.parent.name).update(stage='production',status='in_progress');tracker.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'source_duration':voice['duration_s'],'master_duration':duration,'rate':rate,'captions':len(groups),'scenes':[(s['id'],s['start'],s['duration']) for s in plan['scenes']]}))
