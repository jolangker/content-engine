"""Update only this production's actual stage and preserve other registry rows."""
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent;R=P.parents[1];p=R/'TRACKER.json';d=json.loads(p.read_text(encoding='utf-8'))
stage=sys.argv[1];status=sys.argv[2] if len(sys.argv)>2 else 'in_progress'
next(x for x in d['productions'] if x['slug']==P.name).update(stage=stage,status=status)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all((R/x['path']).is_dir() for x in d['boards']+d['productions'])
print(json.dumps(dict(stage=stage,status=status)))
