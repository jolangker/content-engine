from pathlib import Path
import json,re,html,subprocess,hashlib
V=Path(__file__).resolve().parent
def read(p):return json.loads((V/p).read_text(encoding='utf-8'))
def write(p,v):(V/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
plan=read('scene-plan.json');audio=read('audio_meta.json');voice=audio['voices'][0];words=voice['words'];offset=.25
normalize=lambda w:re.sub(r'[^\w]','',w.lower())
expected=[normalize(w) for s in plan for w in s['vo'].split()]
actual=[normalize(w['text']) for w in words]
if expected!=actual:raise ValueError('Narration alignment does not exactly match spoken script')
source=V/voice['path'];master=V/'assets/audio/narration-master.wav'
if not master.exists():
    # One measured constant gain preserves native speech, no compression or retiming.
    p=subprocess.run(['ffmpeg','-hide_banner','-i',str(source),'-af','volumedetect','-f','null','-'],capture_output=True,text=True)
    peak=float(re.search(r'max_volume: ([\-\d.]+) dB',p.stderr)[1]);mean=float(re.search(r'mean_volume: ([\-\d.]+) dB',p.stderr)[1]);gain=min(-17-mean,-2.5-peak)
    subprocess.run(['ffmpeg','-v','error','-i',str(source),'-af',f'volume={gain}dB,apad=pad_dur=0.2','-ar','48000','-ac','1',str(master)],check=True)
    write('verification/voice-gain.json',dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),source_peak=peak,source_mean=mean,gain_db=gain,source_duration=voice['duration_s'],padding_s=.2,retimed=False))
voice_duration=float(json.loads(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(master)],capture_output=True,text=True,check=True).stdout)['format']['duration'])
cursor=0;boundaries=[0]
for i,s in enumerate(plan):
    count=len(s['vo'].split());s['word_start']=cursor;s['word_end']=cursor+count-1;cursor+=count
    if cursor<len(words):boundaries.append(offset+(words[cursor-1]['end']+words[cursor]['start'])/2)
boundaries.append(max(offset+voice_duration+1.2,offset+words[-1]['end']+1.1))
for i,s in enumerate(plan):s.update(start=boundaries[i],end=boundaries[i+1],duration=boundaries[i+1]-boundaries[i])
write('scene-plan.json',plan)
write('timing.json',dict(duration=boundaries[-1],voice_offset=offset,voice_duration=voice_duration,words=words,scenes=plan))
# Phrase groups preserve every spoken word, never delivery tags.
groups=[]
for s in plan:
    chunk=[]
    for j in range(s['word_start'],s['word_end']+1):
        w=words[j];chunk.append(w)
        if len(chunk)>=5 or re.search(r'[.!?]$',w['text']) or j==s['word_end']:
            groups.append(dict(text=' '.join(w['text'] for w in chunk),start=offset+chunk[0]['start'],end=offset+chunk[-1]['end']+.07,words=chunk));chunk=[]
for i,g in enumerate(groups):
    if i+1<len(groups):g['end']=min(g['end'],groups[i+1]['start'])
write('caption_groups.json',groups)
def stamp(t):
    n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
exp=V.parent/'exports';exp.mkdir(exist_ok=True)
(exp/'rel-bukan-dua-batang-besi.srt').write_text(''.join(f'{i+1}\n{stamp(g["start"])} --> {stamp(g["end"])}\n{g["text"]}\n\n' for i,g in enumerate(groups)),encoding='utf-8')
caps=''.join(f'<div id="caption-group-{i}" class="clip" data-start="{g["start"]:.6f}" data-duration="{g["end"]-g["start"]:.6f}" data-track-index="3"><div class="spoken">{html.escape(g["text"])}</div></div>' for i,g in enumerate(groups))
(V/'compositions/captions.html').write_text(f'''<template><style>#root{{position:absolute;inset:0;color:#173B42}}.spoken{{position:absolute;left:72px;top:1185px;width:max-content;max-width:825px;padding:17px 26px;border-radius:16px;background:#FFF5DE;font:700 58px/1.1 Barlow,sans-serif;letter-spacing:-.87px;white-space:normal}}</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{boundaries[-1]}">{caps}</div><script>const tl=gsap.timeline({{paused:true}});window.__timelines['captions']=tl;</script></template>''',encoding='utf-8')
sb=(V/'STORYBOARD.md').read_text(encoding='utf-8');sb=re.sub(r'duration: 90s',f'duration: {boundaries[-1]:.3f}s',sb,1)
for s in plan:
    pattern=r'(- src: compositions/frames/'+re.escape(s['id'])+r'\.html\n- duration: )[\d.]+s'
    sb=re.sub(pattern,lambda m:m[1]+f'{s["duration"]:.3f}s',sb)
sb=sb.replace('- status: outline','- status: animated')
sb+='\n## Measured narration alignment\n\nNative one-request voice; no speed change. Times refer to main composition.\n\n| Scene | Start | End | Word range |\n| --- | --- | --- | --- |\n'
for s in plan:sb+=f'| {s["id"]} | {s["start"]:.3f} | {s["end"]:.3f} | {s["word_start"]}–{s["word_end"]} |\n'
(V/'STORYBOARD.md').write_text(sb,encoding='utf-8')
print(json.dumps(dict(duration=boundaries[-1],voice_duration=voice_duration,words=len(words),caption_groups=len(groups),exact_script_equality=True)))
