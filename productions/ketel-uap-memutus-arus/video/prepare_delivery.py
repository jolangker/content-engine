"""Persist token-free posting intent before the one authorized external write."""
from pathlib import Path
import json,datetime,hashlib
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2]
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
intent=json.loads((V/'posting-intent.json').read_text(encoding='utf-8'));verified=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));payload=intent['payload']
assert hashlib.sha256((P/verified['local_file']).read_bytes()).hexdigest()==verified['sha256']
assert json.loads((V/'duplicate-check.json').read_text(encoding='utf-8'))['total']==0
receipt=P/'PUBLISHING.json'
if receipt.exists():raise SystemExit('Reconcile existing receipt before another attempt')
asset=dict(provider='trypost',workspace_id=payload['workspace_id'],local_file=verified['local_file'],sha256=verified['sha256'],bytes=verified['bytes'],source='local_upload',status='planned',attempt_started_at=now)
post={k:payload[k] for k in ['provider','workspace_id','workspace_name','social_account_id','service','handle','content_type','requested_delivery','requested_due_at']}
post.update(export_sha256=verified['sha256'],payload=payload,payload_sha256=intent['payload_sha256'],attempt_started_at=now,status='planned',duplicate_check=dict(search='ketel',account=payload['social_account_id'],all_statuses=True,matches=0,pagination='page1of1',evidence='video/duplicate-check.json'))
dump(receipt,dict(schema_version=2,assets=[asset],posts=[post]))
t=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));next(x for x in t['productions'] if x['slug']==P.name).update(stage='publishing',status='in_progress');dump(R/'TRACKER.json',t)
print('Persisted one local-upload and queue intent; no remote post created yet')
