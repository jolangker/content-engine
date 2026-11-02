"""Inspect actual encoded delivery metadata and decoded proof frames."""
from pathlib import Path
import json,subprocess,hashlib
from PIL import Image,ImageOps,ImageDraw
V=Path(__file__).resolve().parent;P=V.parent;E=P/'exports';dest=E/f'{P.name}-v1.mp4';Q=V/'verification/export';Q.mkdir(parents=True,exist_ok=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(dest)]))
video=next(s for s in probe['streams'] if s['codec_type']=='video');audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert video['width']==1080 and video['height']==1920 and video['r_frame_rate']=='30/1'
assert int(video['nb_read_frames'])==2700 and abs(float(probe['format']['duration'])-90)<=1/30
assert video['codec_name']=='h264' and audio['codec_name']=='aac'
subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],capture_output=True,check=True)
timing=json.loads((V/'timing.json').read_text(encoding='utf-8'))
times=[s['start']+.58*s['duration'] for s in timing['scenes']]
for n,t in enumerate(times):subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(dest),'-frames:v','1',str(Q/f'{n+1:02}.png')],capture_output=True,check=True)
sheet=Image.new('RGB',(1440,4*710),'#ECEEE9');draw=ImageDraw.Draw(sheet)
for n,t in enumerate(times):
 im=Image.open(Q/f'{n+1:02}.png').convert('RGB');im.thumbnail((340,650));x=(n%4)*360+10;y=(n//4)*710+10;sheet.paste(im,(x,y));draw.text((x,y+655),f'{n+1:02} @ {t:.3f}s',fill='#172B3B')
sheet.save(Q/'contact-sheet.jpg',quality=94)
cover_time=0.0
subprocess.run(['ffmpeg','-v','error','-y','-ss',str(cover_time),'-i',str(dest),'-frames:v','1',str(E/f'{P.name}-v1-cover.png')],capture_output=True,check=True)
report=dict(status='passed',local_file=dest.relative_to(P).as_posix(),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),bytes=dest.stat().st_size,duration_s=float(probe['format']['duration']),width=1080,height=1920,fps=30,frames=int(video['nb_read_frames']),video_codec=video['codec_name'],pixel_format=video.get('pix_fmt'),audio_codec=audio['codec_name'],audio_sample_rate=audio['sample_rate'],full_decode='passed',proof_times=times,cover_offset_ms=round(cover_time*1000),listening='Not performed; audio presence/levels/correlation measured separately.')
(V/'verification/export.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
