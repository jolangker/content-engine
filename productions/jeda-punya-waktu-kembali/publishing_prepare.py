from pathlib import Path
import json,hashlib,datetime
B=Path(__file__).resolve().parent;R=B.parent.parent;V=B/'video';receipt=B/'PUBLISHING.json'
assert not receipt.exists(),'Reconcile an existing attempt before another write'
e=json.loads((V/'verification/export.json').read_text());assert e['status']=='passed'
content=(B/'publish-caption.txt').read_text(encoding='utf-8');path=B/'exports'/e['export'];assert hashlib.sha256(path.read_bytes()).hexdigest()==e['sha256']
assert path.stat().st_size==e['bytes'] and e['bytes']<=314572800 and e['duration_s']<=900 and len(content)<=2200 and content.count('#')<=5
now=datetime.datetime.now(datetime.timezone.utc).isoformat();workspace='01a171dd-5281-730d-af07-f2168d17add7';account='01a172ed-9899-7177-ab1e-627c835e4a57'
payload=dict(provider='trypost',workspace_id=workspace,social_account_id=account,content=content,content_type='instagram_reel',media_source=dict(export_sha256=e['sha256']),meta={},requested_delivery='draft',requested_due_at=None)
identity=hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
asset=dict(provider='trypost',local_file='exports/'+e['export'],sha256=e['sha256'],bytes=e['bytes'],duration_s=e['duration_s'],width=e['width'],height=e['height'],status='planned',attempt_started_at=now,workspace_id=workspace,source='local_upload')
post=dict(provider='trypost',workspace_id=workspace,workspace_name="Admin's Workspace",social_account_id=account,service='instagram',handle='eliansatya',content_type='instagram_reel',export_sha256=e['sha256'],payload_sha256=identity,payload_serialization='JSON UTF-8; ensure_ascii=false; sorted keys; comma/colon separators without whitespace',payload=payload,requested_delivery='draft',requested_due_at=None,attempt_started_at=now,status='planned',duplicate_check=dict(search='Nanti itu kapan',account_id=account,status='draft',matches=0))
receipt.write_text(json.dumps(dict(schema_version=2,assets=[asset],posts=[post]),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
t=json.loads((R/'TRACKER.json').read_text());next(x for x in t['productions'] if x['slug']==B.name).update(stage='publishing',status='in_progress');(R/'TRACKER.json').write_text(json.dumps(t,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(payload_sha256=identity,export_sha256=e['sha256'],status='planned')))
