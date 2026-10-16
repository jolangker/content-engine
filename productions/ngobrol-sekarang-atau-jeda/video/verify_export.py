"""Inspect the approved delivery encode and decode proof frames from the MP4."""
from pathlib import Path
from fractions import Fraction
import json, subprocess, hashlib
from PIL import Image, ImageDraw, ImageChops, ImageStat

root=Path(__file__).resolve().parent
output=root.parent/'exports/ngobrol-sekarang-atau-jeda-v1.mp4'
assert output.exists() and output.stat().st_size>100000,'Delivery file absent or empty'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(output)],text=True))
video=next(s for s in probe['streams'] if s['codec_type']=='video')
audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (video['width'],video['height'])==(1080,1920),video
assert float(Fraction(video['avg_frame_rate']))==30,video
actual_duration=float(probe['format']['duration'])
assert abs(actual_duration-65.352)<.12,actual_duration
decoded=subprocess.run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'],capture_output=True,text=True)
assert decoded.returncode==0 and not decoded.stderr.strip(),decoded.stderr
levels=subprocess.run(['ffmpeg','-hide_banner','-i',str(output),'-vn','-af','volumedetect','-f','null','-'],capture_output=True,text=True)
assert 'mean_volume: -inf' not in levels.stderr,'Silent delivery audio'
qc=output.parent/'verification-v1';qc.mkdir(exist_ok=True)
times=[4,20.748,30.404,38.38,53.82,64.652]
proof=[];thumbs=[]
for i,t in enumerate(times):
    target=qc/f'decoded-{i+1:02d}-at-{t}s.png'
    subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(output),'-frames:v','1','-y',str(target)],check=True)
    with Image.open(target) as img:
        img=img.convert('RGB')
        reference=list((root/'boards/preview-v1').glob(f'frame-*-at-{t}s.png'))
        assert len(reference)==1,(t,reference)
        with Image.open(reference[0]) as ref:
            mae=sum(ImageStat.Stat(ImageChops.difference(img,ref.convert('RGB'))).mean)/3
        assert mae<12,(t,mae,'Encode differs materially from approved preview')
        tile=Image.new('RGB',(360,670),'#F3EDE3')
        tile.paste(img.resize((360,640)),(0,30))
        ImageDraw.Draw(tile).text((12,8),f'{i+1:02d} / {t:.3f}s',fill='#302B28')
        thumbs.append(tile)
        proof.append({'time':t,'file':target.name,'mean_absolute_pixel_error_vs_preview':round(mae,4)})
sheet=Image.new('RGB',(1080,1340),'#D8C8B5')
for i,tile in enumerate(thumbs):sheet.paste(tile,((i%3)*360,(i//3)*670))
sheet.save(qc/'decoded-contact-sheet.jpg',quality=94)
import re
result={
    'file':output.name,'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
    'duration_s':actual_duration,'authored_duration_s':65.352,
    'video':{'codec':video['codec_name'],'width':video['width'],'height':video['height'],'fps':video['avg_frame_rate'],'frames':video.get('nb_frames'),'pixel_format':video.get('pix_fmt')},
    'audio':{'codec':audio['codec_name'],'sample_rate':audio.get('sample_rate'),'channels':audio.get('channels'),'duration':audio.get('duration'),'levels':dict(re.findall(r'(mean_volume|max_volume): ([^\n]+)',levels.stderr))},
    'decode_errors':decoded.stderr.strip(),'proof_frames':proof,
    'approval':'User requested ekspor for final preview v1 on 2026-10-17',
    'status':'encoded and mechanically verified; decoded contact sheet awaits visual inspection'
}
(qc/'export-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
