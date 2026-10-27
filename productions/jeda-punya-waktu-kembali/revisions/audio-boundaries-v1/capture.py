from pathlib import Path
import json,subprocess,shutil
V=Path(__file__).resolve().parent/'video';s=json.loads((V/'scenes.json').read_text())
times=','.join(str(round(x['start']+x['duration']*f,3)) for x in s for f in [.10,.36,.62,.86])
args=[shutil.which('npx.cmd'),'--yes','hyperframes@0.8.198','snapshot','--at',times,'--no-end','--describe','false','-o','verification/motion-stills']
p=subprocess.run(args,cwd=V,capture_output=True,text=True,encoding='utf-8',errors='replace');(V/'verification/capture.log').write_text(p.stdout+'\n'+p.stderr,encoding='utf-8');p.check_returncode()
print('Captured',len(list((V/'verification/motion-stills').glob('frame-*.png'))),'motion states')
