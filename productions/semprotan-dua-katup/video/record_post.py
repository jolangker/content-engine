from pathlib import Path
import json,sys,datetime
V=Path(__file__).resolve().parent;P=V.parent;R=P.parent.parent
observed=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8-sig'))
receipt=P/'PUBLISHING.json';d=json.loads(receipt.read_text(encoding='utf-8'));post=d['posts'][0]
assert observed['channelId']==post['channel_id']
assert observed['text']==post['payload']['text']
assert observed['assets'][0]['source']==post['payload']['assets'][0]['video']['url']
if post.get('buffer_post_id'):assert post['buffer_post_id']==observed['id']
post.update(buffer_post_id=observed['id'],status=observed['status'],provider_status=observed['status'],scheduled_at=observed.get('dueAt'),sent_at=observed.get('sentAt'),service_url=observed.get('externalLink'),error=observed.get('error'),observed=observed,last_checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks_performed=post.get('checks_performed',0)+1)
receipt.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
complete=observed['status']=='sent'
status='complete' if complete else 'blocked' if observed['status']=='error' else 'in_progress'
tpath=R/'TRACKER.json';t=json.loads(tpath.read_text(encoding='utf-8'));next(x for x in t['productions'] if x['slug']==P.name).update(stage='publishing',status=status);tpath.write_text(json.dumps(t,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(dict(post_id=observed['id'],status=observed['status'],service_url=observed.get('externalLink'),sent_at=observed.get('sentAt'))))
