"""Refresh only the corrected speaker ownership pose and its storyboard still."""
from pathlib import Path
import json,shutil,subprocess
import build
P=Path(__file__).resolve().parent;V=P/'video';B=V/'boards';F=V/'compositions/frames/f06.html'
lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));ts=build.schedule(lines);saved=F.read_bytes();backup=V/'verification/before-f06';backup.mkdir(parents=True,exist_ok=True);(backup/'f06.html').write_bytes(saved)
oldstill=sorted((B/'stills').glob('frame-*.png'))[5];shutil.copy2(oldstill,backup/'storyboard-f06.png')
try:
    F.write_text(build.pose(lines[5],ts[5]),encoding='utf-8')
    at=ts[5]['start']+ts[5]['duration']*.94
    r=subprocess.run([shutil.which('npx.cmd'),'--yes','hyperframes@0.9.1','snapshot','--at',str(at),'--no-end','--describe','false','-o','boards/stills/redo-f06'],cwd=V,capture_output=True,text=True,encoding='utf-8');(backup/'repair-capture.log').write_text(r.stdout+r.stderr,encoding='utf-8');r.check_returncode()
    fresh=list((B/'stills/redo-f06').glob('frame-*.png'));assert len(fresh)==1;shutil.copy2(fresh[0],oldstill)
finally:F.write_bytes(saved)
print('Corrected F06 pose captured; restore animation with --frame 6')
