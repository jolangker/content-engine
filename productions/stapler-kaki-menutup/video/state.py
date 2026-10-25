from pathlib import Path
import json,sys
V=Path(__file__).resolve().parent;P=V.parent;R=P.parents[1]
path=R/'TRACKER.json';t=json.loads(path.read_text(encoding='utf-8-sig'))
row=next(s for s in t['productions'] if s['slug']==P.name)
row.update(stage=sys.argv[1],status=sys.argv[2]);assert (R/row['path']).is_dir()
path.write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(row))
