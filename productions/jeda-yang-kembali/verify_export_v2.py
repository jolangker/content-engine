"""Decode and inspect the corrective local export, retaining the v1 delivery evidence."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib
import json
import re
import subprocess

P = Path(__file__).resolve().parent
V = P / 'video'
movie = P / 'exports/jeda-yang-kembali-v2.mp4'
proof = V / 'verification/encoded-v2'
proof.mkdir(parents=True, exist_ok=True)
probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(movie)],text=True))
video = next(s for s in probe['streams'] if s['codec_type']=='video')
audio = next(s for s in probe['streams'] if s['codec_type']=='audio')
timing = json.loads((V / 'timing.json').read_text(encoding='utf-8'))
duration = float(probe['format']['duration'])
assert (video['width'],video['height'],video['avg_frame_rate']) == (1080,1920,'30/1')
assert abs(duration-timing['duration']) < 1/30+.001
assert audio['codec_name']=='aac' and abs(float(audio['duration'])-duration)<.1
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(movie),'-map','0:v:0','-map','0:a:0','-f','null','NUL'],check=True)
times = [scene['proof_at'] for scene in timing['scenes']]
indices = [round(t*30) for t in times]
select = 'select=' + '+'.join(f'eq(n\\,{n})' for n in indices)
subprocess.run(['ffmpeg','-v','error','-xerror','-y','-i',str(movie),'-vf',select,'-fps_mode','vfr',str(proof / 'frame-%02d.png')],check=True)
frames = sorted(proof.glob('frame-*.png'))
assert len(frames)==14
sheet = Image.new('RGB',(4*276,4*525),(38,34,31))
draw = ImageDraw.Draw(sheet)
comparisons = []
for i,(path,seconds) in enumerate(zip(frames,times)):
    image = Image.open(path).convert('RGB')
    assert image.size==(1080,1920)
    image.thumbnail((268,477),Image.Resampling.LANCZOS)
    x,y=i%4*276+4,i//4*525+28
    sheet.paste(image,(x,y))
    draw.text((x,y-20),f'{i+1:02d} | {seconds:.3f}s',fill=(245,237,227))
    folder = 'v2-opening' if i<5 else 'v2-all'
    reference = next((V / 'verification' / folder).glob(f'frame-{i:02d}-*.png'))
    result = subprocess.run(['ffmpeg','-hide_banner','-i',str(reference),'-i',str(path),'-lavfi','ssim','-f','null','NUL'],capture_output=True,text=True,check=True)
    score = float(re.search(r'All:([\d.]+)',result.stderr).group(1))
    assert score > .985,(i,score)
    comparisons.append({'frame':i+1,'time':seconds,'ssim':score})
sheet.save(P / 'exports/jeda-yang-kembali-v2-contact-sheet.jpg',quality=94)

def measure(prefix=''):
    chain = (prefix+',' if prefix else '') + 'loudnorm=I=-19.5:TP=-3:LRA=7:print_format=json'
    result = subprocess.run(['ffmpeg','-hide_banner','-i',str(movie),'-vn','-af',chain,'-f','null','NUL'],capture_output=True,text=True,check=True)
    return json.loads(re.search(r'\{\s*"input_i"[\s\S]*?\}',result.stderr).group(0))

stereo = measure()
mono = measure('pan=mono|c0=0.5*c0+0.5*c1')
assert float(stereo['input_tp']) < -.5
assert -22 < float(mono['input_i']) < -17
sha = hashlib.sha256(movie.read_bytes()).hexdigest()
summary = {'revision':'v2','local_file':'exports/jeda-yang-kembali-v2.mp4','sha256':sha,'bytes':movie.stat().st_size,
           'duration_s':duration,'width':1080,'height':1920,'fps':30,'frames':int(video['nb_frames']),
           'video_codec':video['codec_name'],'pixel_format':video['pix_fmt'],'audio_codec':audio['codec_name'],
           'audio_channels':audio['channels'],'audio_sample_rate':audio['sample_rate'],
           'encoded_audio_lufs':float(stereo['input_i']),'encoded_mono_downmix_lufs':float(mono['input_i']),
           'encoded_true_peak_dbtp':float(stereo['input_tp']),'full_av_decode':True,'decoded_scene_frames':14,
           'comparisons':comparisons,'minimum_ssim':min(item['ssim'] for item in comparisons)}
(P / 'exports/verification-v2.json').write_text(json.dumps({'summary':summary,'ffprobe':probe},indent=2)+'\n',encoding='utf-8')
(P / 'exports/jeda-yang-kembali-v2.mp4.sha256').write_text(sha+'  jeda-yang-kembali-v2.mp4\n',encoding='utf-8')
print(json.dumps({key:value for key,value in summary.items() if key!='comparisons'}))
