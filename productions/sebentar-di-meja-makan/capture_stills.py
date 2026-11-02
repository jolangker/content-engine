"""Capture the posed scene plan through the actual HyperFrames composition."""
from pathlib import Path
import json,shutil,subprocess
P=Path(__file__).resolve().parent;V=P/'video';B=V/'boards';B.mkdir(exist_ok=True)
ts=json.loads((V/'scene_schedule.json').read_text(encoding='utf-8'))
times=','.join(f'{x["start"]+x["duration"]*.94:.8f}' for x in ts)
shutil.copy2(V/'index.html',B/'.posed.html')
r=subprocess.run([shutil.which('npx.cmd'),'--yes','hyperframes@0.9.1','snapshot','--at',times,'--no-end','--describe','false','-o','boards/stills'],cwd=V,capture_output=True,text=True,encoding='utf-8')
(B/'capture.log').write_text(r.stdout+'\n'+r.stderr,encoding='utf-8');print(r.stdout[-1300:]);r.check_returncode()
