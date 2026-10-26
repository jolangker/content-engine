"""Verify the encoded delivery and decode representative output frames."""
from pathlib import Path
import json,subprocess,hashlib,re
from PIL import Image,ImageDraw
V=Path(__file__).resolve().parent;P=V.parent;video=P/'exports'/(P.name+'-v1.mp4');D=V/'verification/export';D.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
vs=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (vs['width'],vs['height'])==(1080,1920)
assert vs['codec_name']=='h264' and a['codec_name']=='aac'
assert vs['r_frame_rate']=='30/1' and int(vs['nb_frames'])==2700
assert abs(float(probe['format']['duration'])-90)<=1/30
assert video.stat().st_size<314572800
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','NUL'],check=True)
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-af','loudnorm=I=-16:TP=-1:LRA=9:print_format=json','-f','null','NUL'],capture_output=True,text=True,check=True)
levels=json.loads(re.findall(r'\{[^{}]+\}',r.stderr)[-1]);dump(D/'loudness.json',levels)
assert float(levels['input_tp'])<0,'Encoded audio clips'
times=[0,3.4,9,13.2,23.4,39.9,49.15,51.7,54.4,59.95,62.4,64.7,68.3,79.9,82.7,89.5];tiles=[]
for n,t in enumerate(times):
    p=D/f'frame-{n:02}-at-{t:g}s.png';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(p)],check=True)
    im=Image.open(p).convert('RGB');im.thumbnail((270,480));tile=Image.new('RGB',(290,520),'#ECEEE9');tile.paste(im,(10,28));ImageDraw.Draw(tile).text((10,8),f'{t:g}s decoded MP4',fill='#172B3B');tiles.append(tile)
sheet=Image.new('RGB',(290*4,520*4),'#ECEEE9')
for n,tile in enumerate(tiles):sheet.paste(tile,((n%4)*290,(n//4)*520))
sheet.save(D/'proof-sheet.jpg')
report=dict(status='passed',file=video.relative_to(P).as_posix(),sha256=sha(video),bytes=video.stat().st_size,duration_s=float(probe['format']['duration']),width=vs['width'],height=vs['height'],fps=30,frames=2700,video_codec=vs['codec_name'],pixel_format=vs['pix_fmt'],audio_codec=a['codec_name'],audio_sample_rate=a['sample_rate'],full_decode=True,lufs=float(levels['input_i']),true_peak_dbtp=float(levels['input_tp']),proof_times=times,composition_sha256=sha(V/'index.html'),sound_plan_sha256=sha(V/'sound_design.json'),caption_mode='burned_in_and_srt_vtt',listening='Unavailable; no auditory or phone-speaker listening claimed')
dump(V/'verification/export.json',report);print(json.dumps(report))
