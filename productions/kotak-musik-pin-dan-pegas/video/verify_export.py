"""Verify the actual encoded delivery and retain decoded proof frames."""
from pathlib import Path
import json,subprocess,hashlib,re
from PIL import Image,ImageDraw
V=Path(__file__).resolve().parent;P=V.parent;E=P/'exports';video=E/(P.name+'-v1.mp4');D=V/'verification/export';D.mkdir(parents=True,exist_ok=True)
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
levels_run=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-af','loudnorm=I=-16:TP=-1:LRA=9:print_format=json','-f','null','NUL'],capture_output=True,text=True,check=True)
levels=json.loads(re.findall(r'\{[^{}]+\}',levels_run.stderr)[-1]);dump(D/'loudness.json',levels)
times=[0,.8,12.8,22.6,33.1,38.1,40.5,41.7,60.9,64.8,79.3,89.5]
thumbs=[]
for n,t in enumerate(times):
    p=D/f'frame-{n:02}-at-{t:g}s.png'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(p)],check=True)
    im=Image.open(p).convert('RGB');im.thumbnail((270,480));tile=Image.new('RGB',(290,520),'#ECEEE9');tile.paste(im,(10,28));ImageDraw.Draw(tile).text((10,8),f'{t:g}s decoded MP4',fill='#172B3B');thumbs.append(tile)
sheet=Image.new('RGB',(290*4,520*3),'#ECEEE9')
for n,tile in enumerate(thumbs):sheet.paste(tile,((n%4)*290,(n//4)*520))
sheet.save(D/'proof-sheet.jpg')
report=dict(status='passed',file=video.relative_to(P).as_posix(),sha256=sha(video),bytes=video.stat().st_size,duration_s=float(probe['format']['duration']),width=vs['width'],height=vs['height'],fps=30,frames=2700,video_codec=vs['codec_name'],pixel_format=vs['pix_fmt'],audio_codec=a['codec_name'],audio_sample_rate=a['sample_rate'],full_decode=True,lufs=float(levels['input_i']),true_peak_dbtp=float(levels['input_tp']),proof_times=times,composition_sha256=sha(V/'index.html'),sound_plan_sha256=sha(V/'sound_design.json'),caption_mode='burned_in_and_srt_vtt',listening='not available; no perceptual listening claimed')
dump(V/'verification/export.json',report)
print(json.dumps(report))
