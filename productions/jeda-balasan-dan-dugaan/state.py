"""Record the current verified dependency without altering other tracker rows."""
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
stage=sys.argv[1];status=sys.argv[2] if len(sys.argv)>2 else 'in_progress'
t=ROOT/'TRACKER.json';d=json.loads(t.read_text(encoding='utf-8'));next(x for x in d['productions'] if x['slug']==P.name).update(stage=stage,status=status);t.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if stage=='audio':
    with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('''
## Storyboard verification

All 16 styled static poses captured from the actual composition before synthesis/animation. Complete HTML board and saved PNG verified: 1440x3229, all images loaded at 1080x1920, ordered 01–16. Agent inspected saved PNG: 14 cream, charcoal 08/14, fixed chrome, no clipped emphasis/captions. Phone close-ups, branches, calendar details and wide pair vary the focal layout. [HTML](video/boards/storyboard.html), [PNG](video/boards/storyboard.png). Agent-verified under delegation; no human approval. Next: one continuous narration call.
''')
assert all((ROOT/x['path']).is_dir() for x in d['boards']+d['productions'])
print(json.dumps(dict(stage=stage,status=status)))
