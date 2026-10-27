"""Stage only this episode and its tracker row, preserving unrelated board work."""
from pathlib import Path
import json,subprocess
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
run=lambda args,**kw:subprocess.run(args,cwd=ROOT,check=True,capture_output=True,**kw)
receipt=json.loads((P/'PUBLISHING.json').read_text(encoding='utf-8'));assert all(x['status']=='scheduled' for x in receipt['posts']);assert all(x['status']=='verified' for x in receipt['assets'])
tracker_path=ROOT/'TRACKER.json';working_bytes=tracker_path.read_bytes();working=json.loads(working_bytes)
row=next(x for x in working['productions'] if x['slug']==P.name);assert row['stage']=='publishing' and row['status']=='complete'
head=json.loads(run(['git','show','HEAD:TRACKER.json']).stdout)
assert not any(x['slug']==P.name for x in head['productions'])
head['productions'].append(row)
staged=(json.dumps(head,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
blob=run(['git','hash-object','-w','--stdin'],input=staged).stdout.decode().strip()
run(['git','add','--',P.relative_to(ROOT).as_posix()])
run(['git','update-index','--add','--cacheinfo',f'100644,{blob},TRACKER.json'])
paths=run(['git','diff','--cached','--name-only']).stdout.decode().splitlines()
assert all(x=='TRACKER.json' or x.startswith(P.relative_to(ROOT).as_posix()+'/') for x in paths),paths
# Preserve exact third-party GSAP bytes and upstream OFL license text, including
# their existing whitespace. Check every authored file without rewriting vendors.
run(['git','diff','--cached','--check','--','.',':(exclude)productions/terima-kasih-yang-melihat/video/vendor/gsap.min.js',':(exclude)productions/terima-kasih-yang-melihat/video/assets/fonts/*-OFL.txt'])
assert tracker_path.read_bytes()==working_bytes,'Working tracker changed during staging'
print(run(['git','diff','--cached','--stat']).stdout.decode())
print(run(['git','commit','-m','Produce and queue Terima kasih yang melihat']).stdout.decode())
assert tracker_path.read_bytes()==working_bytes,'Working tracker was unexpectedly modified'
print(run(['git','status','--short']).stdout.decode())
print(run(['git','rev-parse','--short','HEAD']).stdout.decode())
