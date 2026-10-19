"""Inspect the encoded delivery file and decode proof frames from that file."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, subprocess, re

prod=Path(__file__).resolve().parent
video=prod/'video'
movie=prod/'exports/limerence.mp4'
proof=video/'verification/encoded'
proof.mkdir(parents=True,exist_ok=True)
assert movie.is_file() and movie.stat().st_size>0
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(movie)],text=True))
vs=next(s for s in probe['streams'] if s['codec_type']=='video')
aus=next(s for s in probe['streams'] if s['codec_type']=='audio')
duration=float(probe['format']['duration'])
target=json.loads((video/'timing.json').read_text(encoding='utf-8'))['duration']
assert (vs['width'],vs['height'])==(1080,1920)
assert vs['avg_frame_rate']=='30/1'
assert abs(duration-target)<=.04,(duration,target)
assert aus['codec_name']=='aac' and float(aus['duration'])>83

reference=sorted((video/'verification/animated-stills').glob('frame-*.png'))
assert len(reference)==14
times=[float(re.search(r'-at-([\d.]+)s',p.name).group(1)) for p in reference]
indices=[round(t*30) for t in times]
select='select='+ '+'.join(f'eq(n\\,{n})' for n in indices)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-y',
    '-i',str(movie),'-vf',select,'-fps_mode','vfr',str(proof/'frame-%02d.png')],check=True)
decoded=sorted(proof.glob('frame-*.png'))
assert len(decoded)==14

comparisons=[]
for i,(before,after,t) in enumerate(zip(reference,decoded,times),1):
    r=subprocess.run(['ffmpeg','-hide_banner','-i',str(before),'-i',str(after),
        '-lavfi','ssim','-f','null','NUL'],capture_output=True,text=True,check=True)
    match=re.search(r'All:([\d.]+)',r.stderr)
    comparisons.append({'frame':i,'reference':before.name,'decoded':after.name,
        'reference_time':t,'encoded_frame_time':indices[i-1]/30,'ssim':float(match.group(1))})

sheet=Image.new('RGB',(7*248,2*478),(33,30,28))
draw=ImageDraw.Draw(sheet)
for i,(p,t) in enumerate(zip(decoded,times)):
    shot=Image.open(p).convert('RGB');assert shot.size==(1080,1920)
    shot.thumbnail((240,427),Image.Resampling.LANCZOS)
    x=(i%7)*248+4;y=(i//7)*478+28
    sheet.paste(shot,(x,y));draw.text((x,y-19),f'{i+1:02d} | {t:.3f}s',fill=(245,238,228))
sheet.save(proof/'contact-sheet.jpg',quality=94)
result={'path':str(movie),'bytes':movie.stat().st_size,'duration_s':duration,
    'target_duration_s':target,'width':vs['width'],'height':vs['height'],
    'fps':vs['avg_frame_rate'],'video_codec':vs['codec_name'],'pixel_format':vs['pix_fmt'],
    'audio_codec':aus['codec_name'],'audio_duration_s':float(aus['duration']),
    'audio_sample_rate':aus['sample_rate'],'decoded_proof_frames':14,
    'preview_comparisons':comparisons,'minimum_ssim':min(c['ssim'] for c in comparisons)}
audio_measurement=subprocess.run(['ffmpeg','-hide_banner','-i',str(movie),
    '-vn','-af','loudnorm=I=-18:TP=-2:LRA=7:print_format=json','-f','null','NUL'],
    capture_output=True,text=True,check=True)
measurement=json.loads(re.search(r'\{\s*"input_i"[\s\S]*?\}',audio_measurement.stderr).group(0))
result['encoded_audio_lufs']=float(measurement['input_i'])
result['encoded_audio_true_peak_dbtp']=float(measurement['input_tp'])
# The renderer delivers stereo, while the approved source/mix measurement was
# mono. Compare a unity-preserving mono downmix to that mono reference; simply
# comparing integrated stereo LUFS would count the duplicated channel twice.
mono_measurement=subprocess.run(['ffmpeg','-hide_banner','-i',str(movie),
    '-vn','-af','pan=mono|c0=0.5*c0+0.5*c1,loudnorm=I=-18:TP=-2:LRA=7:print_format=json',
    '-f','null','NUL'],capture_output=True,text=True,check=True)
mono=json.loads(re.search(r'\{\s*"input_i"[\s\S]*?\}',mono_measurement.stderr).group(0))
result['encoded_mono_downmix_lufs']=float(mono['input_i'])
assert abs(result['encoded_mono_downmix_lufs']-(-18.49))<1
assert result['encoded_audio_true_peak_dbtp']<0
(prod/'exports/verification.json').write_text(json.dumps({'summary':result,'ffprobe':probe},indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
