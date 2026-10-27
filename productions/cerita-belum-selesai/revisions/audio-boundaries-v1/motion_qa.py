from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
V=Path(__file__).resolve().parent/'video';files=sorted((V/'verification/motion-stills').glob('frame-*.png'))
assert len(files)==64,len(files)
rows=[]
for i in range(16):
    fs=files[i*4:i*4+4]; arrays=[np.asarray(Image.open(f).convert('RGB'))[500:1480,88:936].astype(float) for f in fs]
    delta=[float(np.mean(np.max(np.abs(a-b),axis=2)>15)) for a,b in zip(arrays,arrays[1:])]
    assert min(delta)>.001, (i+1,delta)
    rows.append(dict(scene=i+1,content_change_fraction=delta,stills=[f.name for f in fs]))
for sheet in range(4):
    im=Image.new('RGB',(1080,4*515),'#F3EDE3');d=ImageDraw.Draw(im)
    for row in range(4):
        n=sheet*4+row
        for col in range(4):
            thumb=Image.open(files[n*4+col]).resize((260,462))
            im.paste(thumb,(col*270,row*515+28));d.text((col*270+8,row*515+8),f'{n+1:02} / beat {col+1}',fill='#302B28')
    im.save(V/f'verification/motion-sheet-{sheet+1}.jpg',quality=92)
(V/'verification/motion-report.json').write_text(json.dumps(dict(status='passed',scene_count=16,samples=64,excludes='Caption, emphasis and chrome pixels excluded from content-change measurement',scenes=rows),indent=2),encoding='utf-8')
print('All 16 scenes change in the illustrated content field across 4 sampled states.')
