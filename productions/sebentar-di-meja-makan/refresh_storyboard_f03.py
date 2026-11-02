"""Refresh only the static final-state pose without altering the delivered film."""
from pathlib import Path
import hashlib,json,shutil,subprocess
import build
P=Path(__file__).resolve().parent;V=P/'video';Q=V/'verification'
root=V/'index.html';scene=V/'compositions/frames/f03.html';saved={root:root.read_bytes(),scene:scene.read_bytes()}
lines=json.loads((V/'script_data.json').read_text());times=build.schedule(lines);t=times[2];at=t['start']+t['duration']*.94
try:
    root.write_text(build.v.index(lines,times,False),encoding='utf-8')
    scene.write_text(build.pose(lines[2],t).replace('<g id="beat2">','<g id="beat2" opacity="0">'),encoding='utf-8')
    r=subprocess.run([shutil.which('npx.cmd'),'--yes','hyperframes@0.9.1','snapshot','--at',str(at),'--no-end','--describe','false','-o','boards/stills/redo-f03-final'],cwd=V,capture_output=True,text=True,encoding='utf-8');r.check_returncode()
    fresh=next((V/'boards/stills/redo-f03-final').glob('frame-*.png'));dest=next((V/'boards/stills').glob('frame-02-*.png'));shutil.copy2(fresh,dest)
finally:
    for file,data in saved.items():file.write_bytes(data)
assert all(file.read_bytes()==data for file,data in saved.items())
subprocess.run(['python',str(P/'capture_board.py')],check=True)
print('Static final-state route corrected; delivered film files restored byte-for-byte.')
