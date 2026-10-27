"""Capture CLI evidence without console-sized reports or shell redirection encoding."""
from pathlib import Path
import json,subprocess,sys
sys.stdout.reconfigure(encoding='utf-8')
V=Path(__file__).resolve().parent
name=sys.argv[1];args=sys.argv[2:]
r=subprocess.run(['npx.cmd','--yes','hyperframes@0.8.206',*args],cwd=V,capture_output=True,text=True,encoding='utf-8',errors='replace')
(V/f'{name}.log').write_text(r.stdout+'\nSTDERR\n'+r.stderr,encoding='utf-8')
parsed=None
for i,c in enumerate(r.stdout if '--json' in args else ''):
 if c=='{':
  try:parsed=json.JSONDecoder().raw_decode(r.stdout[i:])[0];break
  except json.JSONDecodeError:pass
if parsed is not None:
 (V/f'{name}.json').write_text(json.dumps(parsed,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 summary={k:parsed[k] for k in ['ok','url','pid','port','status','error','browserSkipped'] if k in parsed}
 for k in ['lint','runtime','layout','motion','contrast','craft']:
  if k in parsed:summary[k]={q:parsed[k].get(q) for q in ['ok','errorCount','warningCount','samples','sampleCount'] if q in parsed[k]}
 print(json.dumps(dict(exit_code=r.returncode,report=name+'.json',summary=summary)))
else:print(r.stdout[-2500:]);print(r.stderr[-500:])
sys.exit(r.returncode)
