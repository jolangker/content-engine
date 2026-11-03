"""Stage only this completed production and its tracker entry, leaving unrelated work intact."""
from pathlib import Path
import json,subprocess
P=Path(__file__).resolve().parent;R=P.parents[1];prefix=P.relative_to(R).as_posix()+'/'
def git(*args,**kwargs):return subprocess.run(['git',*args],cwd=R,check=True,capture_output=True,**kwargs)
staged=git('diff','--cached','--name-only').stdout.decode().splitlines()
assert all(p=='TRACKER.json' or p.startswith(prefix) for p in staged),'Unrelated staged changes exist; preserve them'
original=(R/'TRACKER.json').read_bytes();working=json.loads(original.decode('utf-8-sig'));entry=next(x for x in working['productions'] if x['slug']==P.name)
assert entry['stage']=='publishing' and entry['status']=='complete'
head=json.loads(git('show','HEAD:TRACKER.json').stdout.decode('utf-8-sig'))
assert not any(x['slug']==P.name for x in head['productions']),'Production already committed; do not stage another tracker insertion'
head['productions'].append(entry)
blob=(json.dumps(head,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
oid=git('hash-object','-w','--stdin',input=blob).stdout.decode().strip()
git('add','--',prefix.rstrip('/'))
git('update-index','--cacheinfo','100644',oid,'TRACKER.json')
names=git('diff','--cached','--name-only').stdout.decode().splitlines();assert names and all(n=='TRACKER.json' or n.startswith(prefix) for n in names)
assert (R/'TRACKER.json').read_bytes()==original,'Working tracker changed during staging'
git('diff','--cached','--check','--','.',f':(exclude){prefix}video/vendor/gsap.min.js',f':(exclude){prefix}video/assets/fonts/*-OFL.txt')
print(json.dumps(dict(staged_files=len(names),scope=prefix,tracker='HEAD plus this production entry only',unrelated_working_tree='preserved')))
