"""Record the complete stable queue intent before any remote write."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
P=Path(__file__).resolve().parent;V=P/'video';now=datetime.now(timezone.utc).isoformat()
r=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));copy=json.loads((P/'delivery-copy.json').read_text(encoding='utf-8'));target=json.loads((P/'target_snapshot.json').read_text(encoding='utf-8'))['accounts'][0]
assert not (P/'PUBLISHING.json').exists(),'Reconcile existing receipt before another attempt'
assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
payload=dict(provider='trypost',workspace_id=target['workspace_id'],social_account_id=target['social_account_id'],content=copy['caption'],content_type='instagram_reel',media=dict(export_sha256=r['sha256']),meta={},status='scheduled',queue='next',scheduled_at=None)
fingerprint=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
asset=dict(provider='trypost',workspace_id=target['workspace_id'],source='local_upload',local_file=r['file'],sha256=r['sha256'],bytes=r['bytes'],status='planned',attempt_started_at=now)
post=dict(provider='trypost',workspace_id=target['workspace_id'],workspace_name=target['workspace_name'],social_account_id=target['social_account_id'],service='instagram',handle=target['handle'],content_type='instagram_reel',export_sha256=r['sha256'],payload_sha256=fingerprint,payload=payload,requested_delivery='queue',requested_due_at=None,attempt_started_at=now,status='planned',duplicate_check=dict(search='maaf',account=target['social_account_id'],all_statuses=True,matches=0,pagination='page 1 of 1, complete',checked_before_attempt=True))
(P/'PUBLISHING.json').write_text(json.dumps(dict(schema_version=2,assets=[asset],posts=[post]),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status='planned',export_sha256=r['sha256'],payload_sha256=fingerprint)))
