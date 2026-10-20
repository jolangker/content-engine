from pathlib import Path
import json, subprocess, hashlib, re, shutil
from PIL import Image, ImageDraw, ImageFont
P=Path(__file__).resolve().parent;V=P/'video';F=P/'exports/kabar-baik-v1.mp4';Q=V/'verification';Q.mkdir(exist_ok=True)
t=json.loads((V/'timing.json').read_text(encoding='utf-8'))
def run(args):return subprocess.run(args,capture_output=True,text=True,encoding='utf-8',errors='replace',check=True)
probe=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(F)]).stdout)
(Q/'ffprobe-v1.json').write_text(json.dumps(probe,indent=2),encoding='utf-8')
video=next(s for s in probe['streams'] if s['codec_type']=='video');audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
dur=float(probe['format']['duration']);assert abs(dur-t['duration'])<.06
assert (video['width'],video['height'],video['r_frame_rate'])==(1080,1920,'30/1')
assert video['codec_name']=='h264' and audio['codec_name']=='aac'
dec=run(['ffmpeg','-v','error','-i',str(F),'-f','null','-']);assert not dec.stderr.strip(),dec.stderr
mix=run(['ffmpeg','-hide_banner','-i',str(F),'-vn','-af','ebur128=peak=true:framelog=quiet','-f','null','-']).stderr
(Q/'loudness-v1.txt').write_text(mix,encoding='utf-8')
summary=mix[mix.rfind('Summary:'):]
integrated=float(re.search(r'I:\s+(-?[\d.]+) LUFS',summary)[1]);peak=float(re.search(r'Peak:\s+(-?[\d.]+) dBFS',summary)[1]);assert peak<0
sha=hashlib.sha256(F.read_bytes()).hexdigest()
frames=Q/'encoded-v1';frames.mkdir(exist_ok=True)
samples=[]
for d in t['scenes']:
    frame=frames/f'{d["number"]:02}-{d["id"]}.png'
    run(['ffmpeg','-v','error','-ss',str(d['proof_at']),'-i',str(F),'-frames:v','1','-update','1','-y',str(frame)])
    samples.append(dict(scene=d['id'],time=d['proof_at'],file=str(frame.relative_to(P))))
tiles=[]
for sample in samples:
    im=Image.open(P/sample['file']).convert('RGB');im.thumbnail((270,480))
    tile=Image.new('RGB',(290,520),'#D8C8B5');tile.paste(im,(10,30));ImageDraw.Draw(tile).text((10,8),sample['scene'],fill='#302B28');tiles.append(tile)
sheet=Image.new('RGB',(290*7,520*2),'#D8C8B5')
for i,tile in enumerate(tiles):sheet.paste(tile,((i%7)*290,(i//7)*520))
sheet.save(P/'exports/contact-sheet-v1.jpg',quality=94)
run(['ffmpeg','-v','error','-ss','5.357','-i',str(F),'-frames:v','1','-update','1','-y',str(P/'exports/cover-v1.png')])
result=dict(status='passed',export='exports/kabar-baik-v1.mp4',sha256=sha,bytes=F.stat().st_size,duration=dur,width=1080,height=1920,fps=30,video_codec=video['codec_name'],audio_codec=audio['codec_name'],channels=audio['channels'],sample_rate=audio['sample_rate'],full_av_decode='passed',integrated_lufs=integrated,true_peak_dbfs=peak,samples=samples,creative_listening='not established; objective checks only',human_approval=False)
(P/'exports/verification-v1.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='samples'}))
