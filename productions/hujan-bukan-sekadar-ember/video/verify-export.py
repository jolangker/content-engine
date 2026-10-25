from pathlib import Path
import json,subprocess,re,hashlib
import numpy as np
from scipy.signal import correlate,correlation_lags
from PIL import Image,ImageDraw,ImageFont
V=Path(__file__).resolve().parent;out=V.parent/'exports/hujan-bukan-sekadar-ember.mp4';D=V/'verification/export';D.mkdir(parents=True,exist_ok=True)
def run(args):return subprocess.run(args,capture_output=True,check=True)
probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]).stdout)
video=next(x for x in probe['streams'] if x['codec_type']=='video');audio=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert(video['width'],video['height'])==(1080,1920)
assert video['r_frame_rate']=='30/1'
assert abs(float(probe['format']['duration'])-84.7)<.1
decode=run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'])
black=run(['ffmpeg','-hide_banner','-i',str(out),'-vf','blackdetect=d=0.1:pix_th=0.10:pic_th=0.98','-an','-f','null','-']).stderr.decode(errors='replace')
assert 'black_start:' not in black,'Unexpected black section in export'
loud=run(['ffmpeg','-hide_banner','-i',str(out),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-vn','-f','null','-']).stderr.decode(errors='replace')
measurement=json.loads(re.findall(r'\{[^{}]+\}',loud,re.S)[-1])
def pcm(path):return np.frombuffer(run(['ffmpeg','-v','error','-i',str(path),'-ar','16000','-ac','1','-f','f32le','-']).stdout,dtype='<f4').astype(float)
actual=pcm(out);source=pcm(V/'assets/audio/narration-master.wav');rain=pcm(V/'assets/audio/rain-bed.wav')
voice=np.zeros_like(actual);off=round(.35*16000);voice[off:off+len(source)]=source[:max(0,min(len(source),len(actual)-off))]
sound=json.loads((V/'sound_design.json').read_text(encoding='utf-8'));points=sound['cues'][0]['envelope'];ambience=np.zeros_like(actual);n=min(len(rain),len(actual));ambience[:n]=rain[:n]*np.interp(np.arange(n)/16000,[p['t'] for p in points],[p['v'] for p in points])
# AAC decoding should preserve alignment; search a bounded codec-delay window.
a=actual[:320000];b=voice[:320000];c=correlate(a,b,mode='full',method='fft');lags=correlation_lags(len(a),len(b));mask=np.abs(lags)<=2048;lag=int(lags[mask][np.argmax(c[mask])])
if lag>=0: target=actual[lag:];sv=voice[:len(target)];sr=ambience[:len(target)]
else: target=actual[:lag];sv=voice[-lag:];sr=ambience[-lag:]
coeff=np.linalg.lstsq(np.column_stack([sv,sr]),target,rcond=None)[0]
prediction=coeff[0]*sv+coeff[1]*sr;corr=float(np.corrcoef(prediction,target)[0,1]);error=float(np.sqrt(np.mean((target-prediction)**2)))
print(json.dumps(dict(mix_diagnostic=dict(lag=lag,coefficients=coeff.tolist(),ratio=float(coeff[1]/coeff[0]),correlation=corr,residual=error))),flush=True)
assert corr>.98,'Export mix differs from authored tracks'
assert .5<coeff[1]/coeff[0]<1.5,'Rain cue is missing or its mix relation is wrong'
times=[2,12.8,18.5,28.5,33,38,44,51,63,70,71.4,80.5]
stills=[]
for i,t in enumerate(times):
    dest=D/f'frame-{i:02}-at-{t}s.png';run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(out),'-frames:v','1',str(dest)]);stills.append(dest)
cellw,cellh=360,680;sheet=Image.new('RGB',(4*cellw,3*cellh),'#F8F4E8');draw=ImageDraw.Draw(sheet)
font=ImageFont.truetype(str(V/'assets/fonts/barlow-bold.ttf'),24)
for i,p in enumerate(stills):
    im=Image.open(p).convert('RGB');im.thumbnail((354,630));x=(i%4)*cellw+3;y=(i//4)*cellh+40;sheet.paste(im,(x,y));draw.text((x+8,y-31),f'{i+1:02} · {times[i]}s',font=font,fill='#173B42')
sheet.save(D/'contact-sheet.jpg',quality=93)
report=dict(path=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),bytes=out.stat().st_size,duration=float(probe['format']['duration']),video=dict(codec=video['codec_name'],width=video['width'],height=video['height'],fps=video['r_frame_rate'],frames=video.get('nb_frames'),pixel_format=video['pix_fmt']),audio=dict(codec=audio['codec_name'],sample_rate=audio['sample_rate'],channels=audio['channels'],loudness=measurement),full_decode='passed',black_segments=0,mix=dict(codec_delay_samples=lag,voice_gain=float(coeff[0]),rain_gain=float(coeff[1]),rain_to_voice_gain_ratio=float(coeff[1]/coeff[0]),expected_mix_correlation=corr,residual_rms=error,cue_presence='Rain source and authored envelope recovered from the exported audio; narration recovered at its authored offset.'),proof_frames=[str(p.relative_to(V)) for p in stills],creative_listening='Unavailable: automated ASR, decoding and mix comparison do not certify human listening, pronunciation or comic prosody.')
(D/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
