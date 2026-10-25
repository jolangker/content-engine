from pathlib import Path
import json,subprocess,hashlib,re
from PIL import Image,ImageDraw
import numpy as np
V=Path(__file__).resolve().parent;P=V.parent;E=P/'exports/stapler-kaki-menutup-v1.mp4';Q=V/'verification';Q.mkdir(exist_ok=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(E)]))
vs=next(x for x in probe['streams'] if x['codec_type']=='video');au=next(x for x in probe['streams'] if x['codec_type']=='audio')
duration=float(probe['format']['duration']);assert abs(duration-90)<=1/30
assert (vs['width'],vs['height'])==(1080,1920) and vs['r_frame_rate']=='30/1' and int(vs['nb_frames'])==2700
assert vs['codec_name']=='h264' and au['codec_name']=='aac'
subprocess.run(['ffmpeg','-v','error','-i',str(E),'-f','null','NUL'],capture_output=True,text=True,check=True)
result=subprocess.run(['ffmpeg','-hide_banner','-i',str(E),'-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','NUL'],capture_output=True,text=True,check=True)
levels=json.loads(re.findall(r'\{[^{}]+\}',result.stderr)[-1]);assert -22<float(levels['input_i'])<-12 and float(levels['input_tp'])<-.5
def samples(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ar','48000','-ac','1','-f','f32le','pipe:1']),dtype=np.float32).astype(float)
voice=samples(V/'assets/audio/narration-master.wav');actual=samples(E);placed=json.loads((V/'placed_audio.json').read_text());matches=[]
for k in [5,40,75,110,145,180]:
    t=placed['words'][k]['start'];a=round(t*48000);x=voice[a:a+24000];y=actual[a:a+24000];corr=float(np.corrcoef(x,y)[0,1]);assert corr>.85,(t,corr);matches.append({'time':t,'correlation':corr})
native=json.loads((V/'audio_meta.json').read_text())['voices'][0];source=samples(V/native['path']);source_matches=[]
for t in [1,20,40,60,80]:
    x=source[round(t*48000):round(t*48000)+24000];y=voice[round((t+.45)*48000):round((t+.45)*48000)+24000];corr=float(np.corrcoef(x,y)[0,1]);assert corr>.9,(t,corr);source_matches.append({'source_time':t,'placed_time':t+.45,'correlation':corr})
plan=json.loads((V/'timing.json').read_text());frames=Q/'export-frames';frames.mkdir(exist_ok=True);sheet=Image.new('RGB',(1280,2440),'#ECEEE9');draw=ImageDraw.Draw(sheet);times=[]
for i,s in enumerate(plan):
    t=round(s['start']+.62*s['duration'],3);times.append(t);dest=frames/f'{s["id"]}-{t}s.jpg'
    subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(E),'-frames:v','1','-q:v','2',str(dest)],check=True)
    with Image.open(dest) as im:im.thumbnail((320,570));sheet.paste(im,((i%4)*320,(i//4)*610+30))
    draw.text(((i%4)*320+8,(i//4)*610+8),f'{s["id"]} | {t}s',fill='#172B3B')
sheet.save(Q/'export-contact-sheet.jpg',quality=93)
subprocess.run(['ffmpeg','-y','-v','error','-ss','2','-i',str(E),'-frames:v','1','-q:v','2',str(P/'exports/cover.jpg')],check=True)
report={'file':E.relative_to(P).as_posix(),'sha256':hashlib.sha256(E.read_bytes()).hexdigest(),'bytes':E.stat().st_size,'duration_s':duration,'width':1080,'height':1920,'fps':30,'frames':2700,'video_codec':'h264','audio_codec':'aac','full_decode':'passed','loudness':levels,'narration_export_matches':matches,'native_to_placed_matches':source_matches,'proof_times':times,'captions':'burned-in plus SRT and VTT, 197 spoken words only','listening':'Measured, not heard. No subjective full-speed audiovisual or phone-speaker listening claimed.'}
(Q/'export.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
