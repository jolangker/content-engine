from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parent;r=P/'PUBLISHING.json';d=json.loads(r.read_text())
a=d['assets'][-1];assert a['status']=='verified'
assert hashlib.sha256((P/a['local_file']).read_bytes()).hexdigest()==a['sha256']
payload={'channelId':'6ad6400e778b240e2f5a8060','text':(P/'caption.txt').read_text(encoding='utf-8').strip(),'assets':[{'video':{'url':a['secure_url'],'metadata':{'thumbnailOffset':1500}}}],'metadata':{'instagram':{'type':'reel','shouldShareToFeed':True,'isAiGenerated':True}},'mode':'addToQueue','saveToDraft':True,'schedulingType':'automatic'}
fingerprint=hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
if d['posts']:raise SystemExit('A post attempt already exists; reconcile before preparing another')
d['posts'].append({'organization_id':'691274923530437a1a02ed9f','organization_name':'My Organization','channel_id':payload['channelId'],'service':'instagram','handle':'eliansatya','export_sha256':a['sha256'],'payload_sha256':fingerprint,'requested_delivery':'draft','requested_due_at':None,'attempt_started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'planned','payload':payload,'preflight':{'matching_existing_posts':0,'other_episode_drafts':1,'pagination_complete':True}})
r.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(P/'buffer_payload.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'planned','payload_sha256':fingerprint,'caption_characters':len(payload['text']),'media':a['secure_url']}))
