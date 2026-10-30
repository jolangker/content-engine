"""Decode all fifteen cut boundaries and adjacent frames in one FFmpeg pass."""
from pathlib import Path
import json,subprocess
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;V=P/'video';Q=V/'verification';D=Q/'encoded-cut-frames';D.mkdir(exist_ok=True);F=P/'exports'/f'{P.name}-v1.mp4'
scenes=json.loads((V/'timing.json').read_text(encoding='utf-8'))['scenes'];rows=[]
for n in range(2,17):
    frame=scenes[n-1]['start_frame']
    for offset in (-1,0,1):
        i=frame+offset;dest=D/f'frame-{len(rows)+1:03d}.png'
        rows.append(dict(incoming=n,offset=offset,frame=i,time=i/30,file=dest.relative_to(V).as_posix()))
expression='+'.join(f'eq(n\\,{r["frame"]})' for r in rows)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(F),'-vf',f'select={expression},scale=344:612','-vsync','0',str(D/'frame-%03d.png')],check=True,capture_output=True)
assert all((V/r['file']).exists() for r in rows)
for page in range(3):
    sheet=Image.new('RGB',(1080,5*670),'#e7e1d8');draw=ImageDraw.Draw(sheet)
    for k,r in enumerate(rows[page*15:(page+1)*15]):
        im=Image.open(V/r['file']).convert('RGB');x=k%3*360+8;y=k//3*670+24;sheet.paste(im,(x,y));draw.text((x,y+618),f"F{r['incoming']:02d} {r['offset']:+d} | encoded frame {r['frame']}",fill='#302B28')
    sheet.save(Q/f'encoded-cuts-{page+1}.png')
(Q/'encoded-cuts.json').write_text(json.dumps(dict(source=F.relative_to(P).as_posix(),samples=rows,visual_inspection='pending'),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(frames=len(rows),sheets=[f'verification/encoded-cuts-{i}.png' for i in (1,2,3)])))
