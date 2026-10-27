"""Sample four phases of every actual assembled shot for visual review."""
from pathlib import Path
import json
import shutil
import subprocess
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;V=P/'video';Q=V/'verification';ts=json.loads((V/'timing.json').read_text(encoding='utf-8'))['scenes']
times=[s['start']+s['duration']*f for s in ts for f in (.08,.34,.63,.94)]
cmd=[shutil.which('npx.cmd'),'--yes','hyperframes@0.8.206','snapshot','--at',','.join(f'{t:.5f}' for t in times),'--no-end','--describe','false','-o','verification/motion-phases']
result=subprocess.run(cmd,cwd=V,capture_output=True,text=True,encoding='utf-8');(Q/'motion-capture.log').write_text(result.stdout+'\n'+result.stderr,encoding='utf-8');result.check_returncode()
files=sorted((Q/'motion-phases').glob('frame-*.png'));assert len(files)==64,len(files)
for page in range(4):
    sheet=Image.new('RGB',(1120,4*530),'#e7e1d8');draw=ImageDraw.Draw(sheet)
    for row in range(4):
        for col in range(4):
            k=page*16+row*4+col;im=Image.open(files[k]).convert('RGB');im.thumbnail((268,477));x=col*280+6;y=row*530+20;sheet.paste(im,(x,y));draw.text((x,y+482),f'F{k//4+1:02d} | {times[k]:.2f}s',fill='#302B28')
    sheet.save(Q/f'motion-sheet-{page+1}.png')
report=dict(frames=16,samples=64,fractions=[.08,.34,.63,.94],sheets=[f'verification/motion-sheet-{n}.png' for n in range(1,5)])
(Q/'motion-sampling.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
