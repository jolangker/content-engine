"""Verify the local SFX revision against the preserved visual export and frozen cues."""
from pathlib import Path
import json
import re
import subprocess
import sys
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parent
V=P/'video'
sys.path.insert(0,str(P.parents[1]/'.agents/skills/shortform-production/scripts'))
from sound_design import digest, verify_export
OLD='limerence.mp4'
NEW='limerence-sfx-v2.mp4'
movie=P/'exports'/NEW
reference=P/'exports'/OLD
timing=json.loads((V/'timing.json').read_text(encoding='utf-8'))
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(movie)],text=True))
video=next(s for s in probe['streams'] if s['codec_type']=='video')
audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
duration=float(probe['format']['duration'])
assert (video['width'],video['height'],video['avg_frame_rate'])==(1080,1920,'30/1')
assert abs(duration-timing['duration'])<.04
assert audio['codec_name']=='aac' and abs(float(audio['duration'])-duration)<.1
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(movie),'-map','0:v:0','-map','0:a:0','-f','null','NUL'],check=True)
scenes=timing.get('scenes',timing.get('frames'))
times=[s['start']+s['duration']*.65 for s in scenes]
select='select='+'+'.join('eq(n\\,'+str(round(t*30))+')' for t in times)
proof=V/'verification/sfx-encoded'
before=V/'verification/sfx-before'
for source,folder in [(movie,proof),(reference,before)]:
    folder.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-vf',select,'-fps_mode','vfr',str(folder/'frame-%02d.png')],check=True)
frames=sorted(proof.glob('frame-*.png'))
assert len(frames)==14
comparisons=[]
sheet=Image.new('RGB',(4*276,4*525),(38,34,31)); draw=ImageDraw.Draw(sheet)
for i,(path,t) in enumerate(zip(frames,times)):
    result=subprocess.run(['ffmpeg','-hide_banner','-i',str(before/path.name),'-i',str(path),'-lavfi','ssim','-f','null','NUL'],capture_output=True,text=True,check=True)
    score=float(re.search(r'All:([\d.]+)',result.stderr).group(1))
    assert score>.985,(i,score)
    comparisons.append({'scene':i+1,'time':t,'ssim_vs_prior_export':score})
    image=Image.open(path).convert('RGB'); image.thumbnail((268,477),Image.Resampling.LANCZOS)
    x,y=i%4*276+4,i//4*525+28; sheet.paste(image,(x,y)); draw.text((x,y-20),f'{i+1:02d} | {t:.3f}s',fill=(245,237,227))
sheet_path=P/'exports'/(Path(NEW).stem+'-contact-sheet.jpg')
sheet.save(sheet_path,quality=94)
levels=subprocess.run(['ffmpeg','-hide_banner','-i',str(movie),'-vn','-af','loudnorm=I=-18:TP=-2:LRA=7:print_format=json','-f','null','NUL'],capture_output=True,text=True,check=True)
measure=json.loads(re.search(r'\{\s*"input_i"[\s\S]*?\}',levels.stderr).group(0))
assert float(measure['input_tp'])<-.5
cue_report=verify_export(V,movie)
# Preserve speech media, word alignment, captions and timing across this revision.
backup=P/'revisions/before-sound-design-2026-10-20/video/audio_meta.json'
a=json.loads(backup.read_text(encoding='utf-8')); b=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'))
assert a['voices']==b['voices']
summary={'revision':'sfx-2026-10-20','file':'exports/'+NEW,'bytes':movie.stat().st_size,'sha256':digest(movie),
    'prior_export_sha256':digest(reference),'duration':duration,'width':1080,'height':1920,'fps':30,
    'video_codec':video['codec_name'],'audio_codec':audio['codec_name'],'audio_channels':audio['channels'],
    'audio_sample_rate':audio['sample_rate'],'full_av_decode':True,'narration_metadata_unchanged':True,
    'loudness_lufs':float(measure['input_i']),'true_peak_dbtp':float(measure['input_tp']),
    'decoded_scene_frames':14,'minimum_ssim':min(c['ssim_vs_prior_export'] for c in comparisons),
    'cue_verification':cue_report,'visual_comparisons':comparisons,
    'listening':'No human or agent realtime listening claimed; cue waveform presence, timing, encoded loudness and decode verified.'}
(P/'exports/verification-sfx.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
(P/'exports'/(NEW+'.sha256')).write_text(summary['sha256']+'  '+NEW+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k not in ['cue_verification','visual_comparisons']}))
