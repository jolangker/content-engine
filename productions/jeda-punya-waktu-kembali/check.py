from pathlib import Path
import json,subprocess,shutil,sys
V=Path(__file__).resolve().parent/'video'
args=[shutil.which('npx.cmd'),'--yes','hyperframes@0.8.198','check','--json','--snapshots','--samples','32']
p=subprocess.run(args,cwd=V,capture_output=True,text=True,encoding='utf-8',errors='replace')
(V/'check-final.log').write_text(p.stderr,encoding='utf-8')
(V/'verification-final.json').write_text(p.stdout,encoding='utf-8')
try:
    d=json.loads(p.stdout);print(json.dumps({k:{a:b for a,b in v.items() if a in ['ok','errorCount','warningCount','assertionsChecked']} if isinstance(v,dict) else v for k,v in d.items() if k in ['ok','browserSkipped','lint','layout','runtime','contrast','motion','craft']}))
    for k in ['lint','runtime','layout','motion','contrast','craft']:
        for x in d.get(k,{}).get('findings',[]):
            if x.get('severity')=='error':print(k,json.dumps(x))
        warnings=[x for x in d.get(k,{}).get('findings',[]) if x.get('severity')=='warning']
        if warnings:print(k,'reviewed warning codes:',sorted(set(x['code'] for x in warnings)))
except Exception:print(p.stdout[-3000:]);print(p.stderr[-1500:])
sys.exit(p.returncode)
