"""Refresh only corrected static storyboard poses, restoring the film in finally."""
from pathlib import Path
import json, shutil, subprocess
import build
P=Path(__file__).resolve().parent;V=P/'video';B=V/'boards'
lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));ts=build.schedule(lines);ids=(4,12,13)
saved={p:p.read_bytes() for p in [V/'index.html',*[V/f'compositions/frames/f{n:02d}.html' for n in ids]]}
old=sorted((B/'stills').glob('frame-*.png'));assert len(old)==16
try:
    shutil.copy2(V/'index.html',B/'.film.html')
    (V/'index.html').write_text(build.v.index(lines,ts,False),encoding='utf-8')
    for n in ids:(V/f'compositions/frames/f{n:02d}.html').write_text(build.pose(lines[n-1],ts[n-1]),encoding='utf-8')
    at=','.join(f'{ts[n-1]["start"]+ts[n-1]["duration"]*.94:.8f}' for n in ids)
    r=subprocess.run([shutil.which('npx.cmd'),'--yes','hyperframes@0.8.209','snapshot','--at',at,'--no-end','--describe','false','-o','boards/stills/redo'],cwd=V,capture_output=True,text=True,encoding='utf-8')
    (B/'refresh.log').write_text(r.stdout+'\n'+r.stderr,encoding='utf-8');r.check_returncode()
    new=sorted((B/'stills/redo').glob('frame-*.png'));assert len(new)==len(ids)
    for n,f in zip(ids,new):shutil.copy2(f,old[n-1])
finally:
    for p,data in saved.items():p.write_bytes(data)
print(json.dumps(dict(corrected_static_frames=ids,film_restored=True,narration_regenerated=False)))
