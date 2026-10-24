from pathlib import Path
import json,subprocess,hashlib,re,io
import numpy as np
from PIL import Image,ImageDraw
V=Path(__file__).resolve().parent
export=V.parent/'exports/satu-jahitan-mesin-jahit.mp4'
def run(args):return subprocess.run(args,capture_output=True,check=True)
probe=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(export)]).stdout)
video=next(s for s in probe['streams'] if s['codec_type']=='video');audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (video['width'],video['height'])==(1080,1920)
assert video['r_frame_rate']=='30/1' and int(video['nb_frames'])==2700
assert abs(float(probe['format']['duration'])-90)<=1/30
decode=run(['ffmpeg','-v','error','-i',str(export),'-f','null','-']);assert not decode.stderr.strip()
pcm=run(['ffmpeg','-v','error','-i',str(export),'-vn','-ar','48000','-f','f32le','pipe:1']).stdout
samples=np.frombuffer(pcm,dtype='<f4');assert np.isfinite(samples).all() and np.max(np.abs(samples))<1
meter=run(['ffmpeg','-hide_banner','-i',str(export),'-af','loudnorm=print_format=json','-f','null','-']).stderr.decode(errors='replace')
metrics=json.loads(meter[meter.rfind('{'):meter.rfind('}')+1]);assert -18<float(metrics['input_i'])<-14 and float(metrics['input_tp'])<=-1
comparisons=[]
for ref in sorted((V/'verification/final-look').glob('frame-*.png')):
    at=float(re.search(r'-at-(.+)s\.png$',ref.name).group(1))
    png=run(['ffmpeg','-v','error','-ss',str(at),'-i',str(export),'-frames:v','1','-f','image2pipe','-vcodec','png','pipe:1']).stdout
    actual=np.asarray(Image.open(io.BytesIO(png)).convert('RGB').resize((360,640)),dtype=np.float32)
    expected=np.asarray(Image.open(ref).convert('RGB').resize((360,640)),dtype=np.float32)
    mae=float(np.mean(np.abs(actual-expected)));comparisons.append(dict(time=at,mean_absolute_pixel_error=mae))
assert comparisons and max(c['mean_absolute_pixel_error'] for c in comparisons)<5,comparisons
proof=V/'verification/export-frames';proof.mkdir(exist_ok=True)
plan=json.loads((V/'timing.json').read_text(encoding='utf-8'))
times=[0]+[round(s['start']+s['duration']/2,3) for s in plan['scenes']]+[28.5,29.8,31.6,38.7,43.4,71.3,72.3,74.2,75.8,89.966]
times=sorted(set(times));thumbs=[]
for i,t in enumerate(times):
    dest=proof/f'{i:02}-at-{t}s.png';run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(export),'-frames:v','1',str(dest)])
    im=Image.open(dest).convert('RGB');im.thumbnail((270,480));tile=Image.new('RGB',(290,514),'#ECEEE9');tile.paste(im,(10,30));ImageDraw.Draw(tile).text((12,8),f'{t:.3f} s',fill='#172B3B');thumbs.append(tile)
cols=6;rows=(len(thumbs)+cols-1)//cols;sheet=Image.new('RGB',(290*cols,514*rows),'#ECEEE9')
for i,im in enumerate(thumbs):sheet.paste(im,((i%cols)*290,(i//cols)*514))
sheet.save(V.parent/'exports/proof-sheet.jpg',quality=92)
result=dict(status='passed',export=export.name,sha256=hashlib.sha256(export.read_bytes()).hexdigest(),bytes=export.stat().st_size,duration_s=float(probe['format']['duration']),width=1080,height=1920,fps=30,frames=int(video['nb_frames']),video_codec=video['codec_name'],audio_codec=audio['codec_name'],full_decode_errors=0,sample_peak=float(np.max(np.abs(samples))),integrated_lufs=float(metrics['input_i']),true_peak_dbtp=float(metrics['input_tp']),proof_times=times,reviewed_frame_comparisons=comparisons,creative_listening='Unavailable; objective measurements are not perceptual listening.',motion_review='Diagnostic seeked sequences and decoded export frames inspected; no claim of uninterrupted full-speed audiovisual watching.')
(V/'verification/export.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
