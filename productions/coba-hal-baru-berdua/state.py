"""Narrow production state updates and durable verification notes."""
from pathlib import Path
import argparse
import json
P=Path(__file__).resolve().parent;ROOT=P.parents[1];V=P/'video'
ap=argparse.ArgumentParser();ap.add_argument('stage');ap.add_argument('status');ap.add_argument('--note',default='');args=ap.parse_args()
tracker=json.loads((ROOT/'TRACKER.json').read_text(encoding='utf-8'));row=next(x for x in tracker['productions'] if x['slug']==P.name);row.update(stage=args.stage,status=args.status);(ROOT/'TRACKER.json').write_text(json.dumps(tracker,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
assert all((ROOT/x['path']).is_dir() for x in tracker['boards']+tracker['productions'])
if args.note:
    with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('\n'+args.note+'\n')
print(json.dumps(row))
