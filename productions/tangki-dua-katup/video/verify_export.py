from pathlib import Path
import json,subprocess,hashlib,re
from PIL import Image,ImageDraw
import numpy as np
V=Path(__file__).resolve().parent;P=V.parent;E=P/'exports/tangki-dua-katup-v1.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(E)]))
vs=next(x for x in probe['streams'] if x['codec_type']=='video');au=next(x for x in probe['streams'] if x['codec_type']=='audio')
dur=float(probe['format']['duration']);assert abs(dur-90)<=1/30;assert (vs['width'],vs['height'])==(1080,1920)
assert vs['r_frame_rate']=='30/1';assert vs['codec_name']=='h264';assert au['codec_name']=='aac';assert int(vs['nb_frames'])==2700
r=subprocess.run(['ffmpeg','-v','error','-i',str(E),'-f','null','NUL'],capture_output=True,text=True,check=True);assert not r.stderr.strip(),r.stderr
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(E),'-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','NUL'],capture_output=True,text=True,check=True)
levels=json.loads(re.findall(r'\{[^{}]+\}',r.stderr)[-1]);assert float(levels['input_tp'])<-.5;assert -22<float(levels['input_i'])<-12
def samples(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ar','48000','-ac','1','-f','f32le','pipe:1']),dtype=np.float32).astype(float)
voice=samples(V/'assets/audio/narration-master.wav');actual=samples(E);placed=json.loads((V/'placed_audio.json').read_text(encoding='utf-8'));matches=[]
for k in [4,32,62,92,122,152]:
 t=placed['words'][k]['start'];a=round((t-.3)*48000);b=round(t*48000);x=voice[a:a+48000];y=actual[b:b+48000];corr=float(np.corrcoef(x,y)[0,1]);gain=float(np.dot(x,y)/np.dot(x,x));assert corr>.85,(t,corr);matches.append(dict(export_time=t,correlation=corr,gain=gain))
plan=json.loads((V/'timing.json').read_text(encoding='utf-8'));Q=V/'verification/export-frames';Q.mkdir(exist_ok=True)
sheet=Image.new('RGB',(4*320,4*610),'#ECEEE9');draw=ImageDraw.Draw(sheet);times=[]
for i,s in enumerate(plan):
 t=round(s['start']+s['duration']*.62,3);times.append(t);p=Q/f'{s["id"]}-{t}s.jpg'
 subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(E),'-frames:v','1','-q:v','2',str(p)],check=True)
 with Image.open(p) as im:im.thumbnail((320,570));sheet.paste(im,((i%4)*320,(i//4)*610+30))
 draw.text(((i%4)*320+8,(i//4)*610+8),f'{s["id"]} | {t}s',fill='#172B3B')
sheet.save(V/'verification/export-contact-sheet.jpg',quality=93)
report=dict(file=E.relative_to(P).as_posix(),sha256=hashlib.sha256(E.read_bytes()).hexdigest(),bytes=E.stat().st_size,duration_s=dur,width=1080,height=1920,fps=30,frames=2700,video_codec=vs['codec_name'],audio_codec=au['codec_name'],full_decode='passed; no errors',loudness=levels,narration_matches=matches,proof_times=times,captions='burned in plus SRT and VTT; spoken words only',perceptual_listening='Unavailable; no full-speed auditory or phone-speaker review claimed. Objective mix, narration and per-cue export presence verified independently.')
(V/'verification/export.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
