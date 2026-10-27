"""Decode the suspect cut frames directly from the delivered MP4."""
from pathlib import Path
import json,subprocess
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;V=P/'video';Q=V/'verification';D=Q/'encoded-cut-frames';D.mkdir(exist_ok=True);F=P/'exports'/f'{P.name}-v1.mp4'
scenes=json.loads((V/'timing.json').read_text(encoding='utf-8'))['scenes'];rows=[]
for n in (6,12,16):
    frame=scenes[n-1]['start_frame']
    for offset in (-1,0,1):
        i=frame+offset;dest=D/f'f{n:02d}-{offset+1}.png'
        # Frame selection, not a rounded millisecond seek.
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(F),'-vf',f'select=eq(n\\,{i}),scale=344:612','-frames:v','1',str(dest)],check=True,capture_output=True)
        rows.append(dict(incoming=n,offset=offset,frame=i,time=i/30,file=dest.relative_to(V).as_posix()))
sheet=Image.new('RGB',(1080,3*670),'#e7e1d8');draw=ImageDraw.Draw(sheet)
for k,r in enumerate(rows):
    im=Image.open(V/r['file']).convert('RGB');x=k%3*360+8;y=k//3*670+24;sheet.paste(im,(x,y));draw.text((x,y+618),f"F{r['incoming']:02d} {r['offset']:+d} | encoded frame {r['frame']}",fill='#302B28')
sheet.save(Q/'encoded-cuts.png');(Q/'encoded-cuts.json').write_text(json.dumps(dict(source=F.relative_to(P).as_posix(),samples=rows,visual_inspection='pending'),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(frames=len(rows),sheet='verification/encoded-cuts.png')))
