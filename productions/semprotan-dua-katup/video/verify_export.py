from pathlib import Path
import json,subprocess,hashlib,re
from PIL import Image,ImageDraw
import numpy as np
V=Path(__file__).resolve().parent;P=V.parent; E=P/'exports/semprotan-dua-katup-v1.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(E)]))
vs=next(x for x in probe['streams'] if x['codec_type']=='video');au=next(x for x in probe['streams'] if x['codec_type']=='audio')
dur=float(probe['format']['duration']);assert abs(dur-90)<=1/30;assert (vs['width'],vs['height'])==(1080,1920)
assert vs['r_frame_rate']=='30/1';assert vs['codec_name']=='h264';assert au['codec_name']=='aac';assert int(vs['nb_frames'])==2700
decode=subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(E),'-f','null','NUL'],capture_output=True,text=True,check=True)
assert not decode.stderr.strip(),decode.stderr
audio=subprocess.run(['ffmpeg','-hide_banner','-i',str(E),'-af','loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json','-f','null','NUL'],capture_output=True,text=True,check=True)
levels=json.loads(re.findall(r'\{[^{}]+\}',audio.stderr)[-1]);assert float(levels['input_tp'])<-.5;assert -21<float(levels['input_i'])<-13
def samples(path):
    b=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),'-vn','-ar','44100','-ac','1','-f','f32le','pipe:1'])
    return np.frombuffer(b,dtype=np.float32)
expected=samples(V/'assets/audio/narration-master.wav');actual=samples(E);matches=[]
for t in [5,20,35,50,65,80]:
    i=round(t*44100);j=round((t+.3)*44100);a=expected[i:i+88200].astype(float);b=actual[j:j+88200].astype(float)
    corr=float(np.corrcoef(a,b)[0,1]);gain=float(np.dot(a,b)/np.dot(a,a));matches.append(dict(source_time=t,export_time=t+.3,correlation=corr,fitted_gain=gain));assert corr>.95,(t,corr)
times=[3.94,10.384,16.251,26.687,31.345,36.479,50.212,55.507,67.05,72.824,86.811]
Q=V/'verification/export-frames';Q.mkdir(exist_ok=True)
sheet=Image.new('RGB',(4*320,3*620),'#ECEEE9');draw=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
    name=Q/f'{i+1:02}-{t}s.jpg'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(E),'-frames:v','1','-q:v','2',str(name)],check=True)
    with Image.open(name) as im:im.thumbnail((320,570));sheet.paste(im,((i%4)*320,(i//4)*620+30))
    draw.text(((i%4)*320+8,(i//4)*620+8),f'{i+1:02} | {t}s',fill='#172B3B')
sheet.save(V/'verification/export-contact-sheet.jpg',quality=92)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','3.7','-i',str(E),'-frames:v','1','-q:v','2',str(P/'exports/cover.jpg')],check=True)
report=dict(file=E.relative_to(P).as_posix(),sha256=hashlib.sha256(E.read_bytes()).hexdigest(),bytes=E.stat().st_size,duration_s=dur,width=1080,height=1920,fps=30,frames=2700,video_codec=vs['codec_name'],audio_codec=au['codec_name'],full_decode='passed; no errors',loudness=levels,narration_waveform_matches=matches,proof_times=times,subtitle_mode='burned in and SRT',listening='Full-speed audiovisual listening unavailable; no perceptual approval claimed.')
(V/'verification/export.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
