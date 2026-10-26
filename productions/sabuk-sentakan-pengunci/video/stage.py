from pathlib import Path
import json,sys
V=Path(__file__).resolve().parent;R=V.parents[2];P=V.parent
stage,status=sys.argv[1:3]
t=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));next(x for x in t['productions'] if x['slug']==P.name).update(stage=stage,status=status)
(R/'TRACKER.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if len(sys.argv)>3:
    with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('\n'+sys.argv[3]+'\n')
print(stage+': '+status)
