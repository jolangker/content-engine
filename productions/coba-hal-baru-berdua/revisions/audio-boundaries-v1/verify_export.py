"""Verify the actual encoded video, audio and representative decoded frames."""
from pathlib import Path
import hashlib
import json
import subprocess
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parent;V=P/'video';E=P/'exports';FILE=E/'coba-hal-baru-berdua-v1.mp4'

def main():
    raw=subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(FILE)],capture_output=True,text=True,check=True)
    info=json.loads(raw.stdout);video=next(s for s in info['streams'] if s['codec_type']=='video');audio=next(s for s in info['streams'] if s['codec_type']=='audio')
    assert video['width']==1080 and video['height']==1920
    assert video['codec_name']=='h264' and audio['codec_name']=='aac'
    assert video['r_frame_rate']=='30/1'
    target=json.loads((V/'timing.json').read_text(encoding='utf-8'))['duration_s']
    assert abs(float(video['duration'])-target)<.05
    assert int(video['nb_frames'])==round(target*30)
    subprocess.run(['ffmpeg','-v','error','-i',str(FILE),'-f','null','-'],capture_output=True,check=True)
    measure=subprocess.run(['ffmpeg','-hide_banner','-i',str(FILE),'-af','loudnorm=I=-16:TP=-1:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    loudness=json.JSONDecoder().raw_decode(measure.stderr[measure.stderr.rfind('{'):])[0]
    assert -18<float(loudness['input_i'])<-13
    assert float(loudness['input_tp'])<=-.5
    frames=V/'verification/export-frames';frames.mkdir(parents=True,exist_ok=True)
    schedule=json.loads((V/'timing.json').read_text(encoding='utf-8'))['scenes']
    sheet=Image.new('RGB',(1440,4*680),'#e7e1d8');draw=ImageDraw.Draw(sheet)
    for i,s in enumerate(schedule):
        at=s['start']+s['duration']*.77
        dest=frames/f'frame-{i+1:02d}.png'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{at:.5f}','-i',str(FILE),'-frames:v','1','-vf','scale=344:612',str(dest)],capture_output=True,check=True)
        im=Image.open(dest).convert('RGB');x=(i%4)*360+8;y=(i//4)*680+24
        sheet.paste(im,(x,y));draw.text((x,y+620),f'{i+1:02d} / 16  |  {at:.2f}s',fill='#302B28')
    sheet.save(E/'export-proof.png')
    receipt={'version':'v1','file':FILE.relative_to(P).as_posix(),'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'bytes':FILE.stat().st_size,'duration_s':float(video['duration']),'container_duration_s':float(info['format']['duration']),'width':1080,'height':1920,'fps':30,'frames':int(video['nb_frames']),'video_codec':video['codec_name'],'pixel_format':video.get('pix_fmt'),'audio_codec':audio['codec_name'],'audio_channels':audio.get('channels'),'full_decode':'passed','loudness':loudness,'sound_listening':'not performed; measurements do not establish perceptual quality','proof':'exports/export-proof.png'}
    (V/'verification/export.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt))
if __name__=='__main__':main()
