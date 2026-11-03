"""Update only this production's stage and append durable evidence."""
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent;R=P.parents[1]
stage=sys.argv[1];status=sys.argv[2]
f=R/'TRACKER.json';d=json.loads(f.read_text(encoding='utf-8-sig'));row=next(x for x in d['productions'] if x['slug']==P.name);row.update(stage=stage,status=status);f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert (R/row['path']).is_dir()
if len(sys.argv)>3:
    with (P/'EPISODE.md').open('a',encoding='utf-8') as out:out.write('\n'+sys.argv[3]+'\n')
print(json.dumps(dict(stage=stage,status=status)))
