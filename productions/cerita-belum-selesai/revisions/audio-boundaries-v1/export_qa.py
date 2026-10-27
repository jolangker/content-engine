from pathlib import Path
import json,subprocess,hashlib,re
import numpy as np
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parent;V=BASE/'video'; E=BASE/'exports/cerita-belum-selesai-v1.mp4'
Q=V/'verification/export-frames';Q.mkdir(parents=True,exist_ok=True)
def run(args):return subprocess.run(args,capture_output=True,text=True,encoding='utf-8',errors='replace',check=True)
meta=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(E)]).stdout)
video=next(s for s in meta['streams'] if s['codec_type']=='video');aud=next(s for s in meta['streams'] if s['codec_type']=='audio')
assert (video['width'],video['height'],video['r_frame_rate'])==(1080,1920,'30/1')
assert abs(float(meta['format']['duration'])-86)<.05
run(['ffmpeg','-v','error','-i',str(E),'-f','null','-'])
scenes=json.loads((V/'scenes.json').read_text(encoding='utf-8'));refs=sorted((V/'verification/motion-stills').glob('frame-*.png'))
proof=Image.new('RGB',(1320,4*630),'#F3EDE3');draw=ImageDraw.Draw(proof);comparisons=[]
for i,s in enumerate(scenes):
    time=round(s['start']+s['duration']*.86,3);out=Q/f'f{i+1:02}.png'
    run(['ffmpeg','-v','error','-y','-ss',str(time),'-i',str(E),'-frames:v','1',str(out)])
    img=Image.open(out).convert('RGB'); a=np.asarray(img).astype(float);b=np.asarray(Image.open(refs[i*4+3]).convert('RGB')).astype(float)
    mae=float(np.mean(np.abs(a-b))); comparisons.append(dict(scene=i+1,time=time,mean_absolute_rgb_error=mae,reference=refs[i*4+3].name))
    assert mae<8,(i+1,mae)
    x=(i%4)*330;y=(i//4)*630
    proof.paste(img.resize((324,576)),(x,y+28));draw.text((x+8,y+8),f'{i+1:02} / {time:.2f}s',fill='#302B28')
proof.save(BASE/'exports/proof-sheet.jpg',quality=93)
loud=run(['ffmpeg','-hide_banner','-i',str(E),'-af','loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json','-f','null','-']).stderr
(V/'verification/export-loudness.log').write_text(loud,encoding='utf-8')
loudjson=json.loads(loud[loud.rfind('{'):loud.rfind('}')+1]);assert float(loudjson['input_tp'])<0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report=dict(status='passed',export=E.name,sha256=sha(E),bytes=E.stat().st_size,duration_s=float(meta['format']['duration']),width=video['width'],height=video['height'],fps=video['r_frame_rate'],video_codec=video['codec_name'],audio_codec=aud['codec_name'],full_decode='passed',loudness=loudjson,render_vs_preview=comparisons,composition_sha256=sha(V/'index.html'),sound_design_sha256=sha(V/'sound_design.json'),caption_sha256=sha(BASE/'exports/cerita-belum-selesai.srt'),listening='Perceptual listening unavailable. Player/media progression, full decode, levels, alignment and exported SFX waveform presence are separate technical evidence; no human audio approval is claimed.')
(V/'verification/export.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['render_vs_preview','loudness']}));print('Preview/export MAE range',min(x['mean_absolute_rgb_error'] for x in comparisons),max(x['mean_absolute_rgb_error'] for x in comparisons));print('LUFS',loudjson['input_i'],'true peak',loudjson['input_tp'])
