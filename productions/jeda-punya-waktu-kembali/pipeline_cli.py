from pathlib import Path
import subprocess,shutil,sys
B=Path(__file__).resolve().parent;R=B.parent.parent;V=B/'video'
mode=sys.argv[1]
assert mode in ['check','render']
subprocess.run([sys.executable,str(R/'.agents/skills/shortform-production/scripts/sound_design.py'),'--video',str(V),'--check'],cwd=V,check=True)
args=[shutil.which('npx.cmd'),'--yes','hyperframes@0.8.198',mode]
if mode=='render' and len(sys.argv)==2:args+=['--quality','delivery','--output','../exports/jeda-punya-waktu-kembali-v1.mp4']
else:args+=sys.argv[2:]
if mode=='render':
    with (V/'render.log').open('w',encoding='utf-8') as log:
        result=subprocess.run(args,cwd=V,stdout=log,stderr=subprocess.STDOUT)
    print((V/'render.log').read_text(encoding='utf-8')[-5500:]);sys.exit(result.returncode)
sys.exit(subprocess.run(args,cwd=V).returncode)
