from pathlib import Path
from PIL import Image, ImageDraw
import json, subprocess, re, hashlib, shutil
P=Path(__file__).resolve().parent;V=P/'video';movie=P/'exports/jeda-yang-kembali.mp4'
proof=V/'verification/encoded';proof.mkdir(parents=True,exist_ok=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(movie)],text=True))
vs=next(s for s in probe['streams'] if s['codec_type']=='video');au=next(s for s in probe['streams'] if s['codec_type']=='audio')
t=json.loads((V/'timing.json').read_text(encoding='utf-8'));duration=float(probe['format']['duration'])
assert (vs['width'],vs['height'],vs['avg_frame_rate'])==(1080,1920,'30/1')
assert abs(duration-t['duration'])<=1/30+.001
assert au['codec_name']=='aac' and abs(float(au['duration'])-duration)<.1
times=[round(s['start']+min(s['duration']-.4,s['cue2']+.5),3) for s in t['scenes']]
indices=[round(x*30) for x in times]
select='select='+ '+'.join(f'eq(n\\,{n})' for n in indices)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-y','-i',str(movie),'-vf',select,'-fps_mode','vfr',str(proof/'frame-%02d.png')],check=True)
decoded=sorted(proof.glob('frame-*.png'));assert len(decoded)==14
sheet=Image.new('RGB',(4*276,4*525),(38,34,31));draw=ImageDraw.Draw(sheet)
comp=[]
refined={1:'frame-00-at-11.766s.png',2:'frame-01-at-17.66s.png',4:'frame-02-at-28.896s.png',8:'frame-03-at-53.05s.png',12:'frame-04-at-78.066s.png'}
for i,(p,sec) in enumerate(zip(decoded,times)):
    img=Image.open(p).convert('RGB');assert img.size==(1080,1920)
    img.thumbnail((268,477),Image.Resampling.LANCZOS);x=i%4*276+4;y=i//4*525+28
    sheet.paste(img,(x,y));draw.text((x,y-20),f'{i+1:02d} | {sec:.3f}s',fill=(245,237,227))
    before=V/'verification/refined'/refined[i] if i in refined else next((V/'verification/all-scenes').glob(f'frame-{i:02d}-*.png'))
    r=subprocess.run(['ffmpeg','-hide_banner','-i',str(before),'-i',str(p),'-lavfi','ssim','-f','null','NUL'],capture_output=True,text=True,check=True)
    score=float(re.search(r'All:([\d.]+)',r.stderr).group(1));assert score>.985,(i,score)
    comp.append({'frame':i+1,'time':sec,'ssim':score})
sheet.save(P/'exports/jeda-yang-kembali-contact-sheet.jpg',quality=94)
def measure(filters=''):
    chain=(filters+',' if filters else '')+'loudnorm=I=-18:TP=-2:LRA=7:print_format=json'
    r=subprocess.run(['ffmpeg','-hide_banner','-i',str(movie),'-vn','-af',chain,'-f','null','NUL'],capture_output=True,text=True,check=True)
    return json.loads(re.search(r'\{\s*"input_i"[\s\S]*?\}',r.stderr).group(0))
m=measure();mono=measure('pan=mono|c0=0.5*c0+0.5*c1')
assert float(m['input_tp'])<-.5
assert -21<float(mono['input_i'])<-17
sha=hashlib.sha256(movie.read_bytes()).hexdigest()
summary={'local_file':'exports/jeda-yang-kembali.mp4','sha256':sha,'bytes':movie.stat().st_size,'duration_s':duration,'width':1080,'height':1920,'fps':30,'frames':int(vs['nb_frames']),'video_codec':vs['codec_name'],'pixel_format':vs['pix_fmt'],'audio_codec':au['codec_name'],'audio_channels':au['channels'],'audio_sample_rate':au['sample_rate'],'encoded_audio_lufs':float(m['input_i']),'encoded_mono_downmix_lufs':float(mono['input_i']),'encoded_true_peak_dbtp':float(m['input_tp']),'decoded_scene_frames':14,'comparisons':comp,'minimum_ssim':min(x['ssim'] for x in comp)}
(P/'exports/verification.json').write_text(json.dumps({'summary':summary,'ffprobe':probe},indent=2)+'\n',encoding='utf-8')
(P/'exports/jeda-yang-kembali.mp4.sha256').write_text(sha+'  jeda-yang-kembali.mp4\n',encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='comparisons'}))
