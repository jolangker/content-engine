"""Retain the observed caption correction without creating another post."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
file=P/'PUBLISHING.json';receipt=json.loads(file.read_text(encoding='utf-8'));fix=json.loads((P/'video/verification/caption-reconciliation.json').read_text(encoding='utf-8'));post=receipt['posts'][0]
assert fix['verified_exact_match'] and post['trypost_post_id']==fix['post_id']
assert fix['corrected_content']==post['payload']['content'];assert fix['original_scheduled_at']==fix['retained_scheduled_at']==post['scheduled_at']
prior={**post['payload'],'content':fix['previous_observed_content']}
fix['previous_observed_payload_sha256']=hashlib.sha256(json.dumps(prior,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
fix['corrected_payload_sha256']=post['payload_sha256']
post['reconciliations']=[fix]
file.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('\n## Delivery caption reconciliation\n\nReadback caught curly-quote mojibake caused by a Windows-default Get-Content read during handoff. Updated the same scheduled post from an explicit UTF-8 source, retaining its media and schedule. Second readback matches the package exactly. Previous observed copy and payload fingerprint retained in PUBLISHING.json; no duplicate created. A packaging helper initially expected the pre-boundary sound receipt filename; corrected it to sound-design-export-v2.json and verified the package before upload.\n')
print('Caption correction retained; exact package copy, same post/media/schedule verified.')
