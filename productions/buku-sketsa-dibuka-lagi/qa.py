"""Run the pinned CLI and keep structured receipts without terminal progress noise."""
from pathlib import Path
import json,shutil,subprocess,sys
P=Path(__file__).resolve().parent;V=P/'video';Q=V/'verification';Q.mkdir(exist_ok=True)
sys.stdout.reconfigure(encoding='utf-8')
job=sys.argv[1]
args={'check':['check','--json'],'review':['snapshot','--review','--json'],'render':['render','--quality','delivery','--output',f'../exports/{P.name}-v1.mp4']}[job]
if job in ('check','render'):subprocess.run([sys.executable,str(P.parents[1]/'.agents/skills/shortform-production/scripts/sound_design.py'),'--video',str(V),'--check'],check=True)
r=subprocess.run([shutil.which('npx.cmd'),'--yes','hyperframes@0.9.1',*args],cwd=V,capture_output=True,text=True,encoding='utf-8')
(Q/f'{job}-output.log').write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
if job=='check':
    files=list((V/'.hyperframes/artifacts/checks').glob('*.json'));d=json.loads(max(files,key=lambda x:x.stat().st_mtime).read_text(encoding='utf-8'));(Q/'hyperframes-check.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:{kk:vv for kk,vv in v.items() if kk in ('ok','errorCount','warningCount','infoCount','samples')} if isinstance(v,dict) else v for k,v in d.items() if k in ('ok','errorCount','warningCount','lint','runtime','layout','motion','contrast','craft','audio')}))
elif job=='review':
    found=None
    for i,ch in enumerate(r.stdout):
        if ch=='{':
            try:
                d,_=json.JSONDecoder().raw_decode(r.stdout[i:])
                if isinstance(d,dict) and 'contactSheets' in d:found=d;break
            except ValueError:pass
    if found:(Q/'review-manifest.json').write_text(json.dumps(found,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(ok=found.get('ok'),contactSheets=found.get('contactSheets'),review=found.get('review',{}).get('sheets'))))
    else:print(r.stdout[-2500:])
else:print(r.stdout[-3500:]);print(r.stderr[-1000:])
r.check_returncode()
