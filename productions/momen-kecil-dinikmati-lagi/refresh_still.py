"""Update the revised memory pose without replacing the other planning stills."""
from pathlib import Path
import json,shutil,subprocess
P=Path(__file__).resolve().parent;V=P/'video';B=V/'boards'
s=json.loads((V/'scene_schedule.json').read_text(encoding='utf-8'))[14]
at=s['start']+s['duration']*.94
r=subprocess.run([shutil.which('npx.cmd'),'--yes','hyperframes@0.8.209','snapshot','--at',str(at),'--no-end','--describe','false','-o','boards/stills/redo'],cwd=V,capture_output=True,text=True,encoding='utf-8');r.check_returncode()
generated=list((B/'stills/redo').glob('frame-*.png'));assert len(generated)==1
original=list((B/'stills').glob('frame-14-*.png'));assert len(original)==1
shutil.copy2(generated[0],original[0])
subprocess.run(['python',str(P/'capture_board.py')],check=True)
print(json.dumps(dict(scene=15,at=at,still=original[0].name,reason='Clarify recalled pair versus outside observer; no narration change')))
