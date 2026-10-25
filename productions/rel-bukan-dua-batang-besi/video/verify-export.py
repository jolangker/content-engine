from pathlib import Path
import json,subprocess,hashlib,re,importlib.util,sys
from PIL import Image,ImageDraw
import numpy as np
V=Path(__file__).resolve().parent;ROOT=V.parents[2];export=V.parent/'exports/rel-bukan-dua-batang-besi.mp4'
out=V/'verification/export';out.mkdir(exist_ok=True)
def run(args,**kw):return subprocess.run(args,capture_output=True,check=True,**kw)
probe=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(export)],text=True).stdout)
video=next(s for s in probe['streams'] if s['codec_type']=='video');audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
timing=json.loads((V/'timing.json').read_text(encoding='utf-8'));duration=float(probe['format']['duration'])
assert (video['width'],video['height'],video['r_frame_rate'])==(1080,1920,'30/1')
assert abs(duration-timing['duration'])<.1
audio_only='--audio-only' in sys.argv
if audio_only:
    prior=json.loads((out/'report.json').read_text());assert prior['sha256']==hashlib.sha256(export.read_bytes()).hexdigest();blacksegments=prior['black_segments'];loud=prior['loudness']
else:
    decode=run(['ffmpeg','-v','error','-i',str(export),'-f','null','-'],text=True)
    black=run(['ffmpeg','-hide_banner','-i',str(export),'-vf','blackdetect=d=0.15:pix_th=0.08','-an','-f','null','-'],text=True)
    blacksegments=[s for s in black.stderr.splitlines() if 'black_start:' in s]
    assert not blacksegments
    levels=run(['ffmpeg','-hide_banner','-i',str(export),'-vn','-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-f','null','-'],text=True)
    loud=json.loads(re.findall(r'\{\s*"input_i".*?\}',levels.stderr,re.S)[-1]);(out/'loudness.json').write_text(json.dumps(loud,indent=2)+'\n')
plan=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'));files=[]
times=[s['start']+.72*s['duration'] for s in plan]+[duration-.1]
for i,t in enumerate(times):
    p=out/f'frame-{i+1:02}-at-{t:.3f}s.png'
    if not audio_only:run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(export),'-frames:v','1',str(p)])
    files.append(p)
sheet=Image.new('RGB',(1440,4*690),(248,244,232));draw=ImageDraw.Draw(sheet)
for i,f in enumerate(files):
    im=Image.open(f).convert('RGB');im.thumbnail((345,630));x=(i%4)*360;y=(i//4)*690;draw.text((x+8,y+8),f'{i+1:02} / {times[i]:.2f}s',fill='#173B42');sheet.paste(im,(x+5,y+33))
sheet.save(out/'contact-sheet.jpg',quality=92)
groups=json.loads((V/'caption_groups.json').read_text(encoding='utf-8'));norm=lambda t:re.sub(r'[^\w]','',t.lower())
assert [norm(w) for g in groups for w in g['text'].split()]==[norm(w['text']) for w in timing['words']]
assert all(0<=g['start']<g['end']<=duration for g in groups)
# Fit expected complete mix at authored times. This detects missing/misaligned narration independently of metadata.
def pcm(p):
    channels=int(json.loads(run(['ffprobe','-v','error','-select_streams','a:0','-show_entries','stream=channels','-of','json',str(p)],text=True).stdout)['streams'][0]['channels'])
    # Equal-amplitude channel average: FFmpeg's default stereo->mono coefficients
    # add +3.01 dB for coherent dual mono, which is not source gain or clipping.
    raw=np.frombuffer(run(['ffmpeg','-v','error','-i',str(p),'-vn','-ar','48000','-f','f32le','pipe:1']).stdout,dtype='<f4').astype(float)
    return raw.reshape(-1,channels).mean(axis=1)
sig=pcm(export);voice=pcm(V/'assets/audio/narration-master.wav');expected=np.zeros(len(sig));a=round(timing['voice_offset']*48000);n=min(len(voice),len(sig)-a);expected[a:a+n]+=voice[:n]
sd=json.loads((V/'sound_design.json').read_text());assets={a['id']:a for a in sd['assets']}
for c in sd['cues']:
    cue=pcm(V/assets[c['asset']]['path']);a=round(c['start']*48000);n=min(len(cue),round(c['duration']*48000),len(sig)-a);expected[a:a+n]+=cue[:n]*c['volume']
corr=float(np.corrcoef(sig,expected)[0,1]);gain=float(np.dot(sig,expected)/np.dot(expected,expected));peak=float(np.max(np.abs(sig)))
report=dict(file=str(export),sha256=hashlib.sha256(export.read_bytes()).hexdigest(),bytes=export.stat().st_size,duration=duration,composition_duration=timing['duration'],width=video['width'],height=video['height'],fps=video['r_frame_rate'],video_codec=video['codec_name'],audio_codec=audio['codec_name'],full_decode=True,black_segments=blacksegments,loudness=loud,caption_groups=len(groups),caption_words=len(timing['words']),caption_exact_script_equality=True,mix_correlation=corr,mix_gain=gain,decoded_peak=peak,listening='Measured, not heard; subjective listening unavailable.')
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
if corr<.98 or not(.9<gain<1.1):raise ValueError('Export audio differs from authored mix; retain video and repair audio from verified source tracks')
if peak>=.999:raise ValueError('Export clipping requires mix repair')
report['status']='passed'
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
