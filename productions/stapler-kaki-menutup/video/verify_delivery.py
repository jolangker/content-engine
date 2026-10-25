from pathlib import Path
import json,hashlib,requests,datetime
V=Path(__file__).resolve().parent;P=V.parent;R=P.parents[1]
p=P/'PUBLISHING.json';d=json.loads(p.read_text());post=d['posts'][0];observed=json.loads((V/'verification/trypost-readback.json').read_text())
assert observed['id']==post['trypost_post_id'] and observed['status']=='scheduled' and observed['schedule_mode']=='queue'
assert observed['social_account']['id']==post['social_account_id'] and observed['social_account']['username']=='dibalikbenda.id'
assert len(observed['media'])==1 and observed['media'][0]['size']==d['assets'][0]['bytes'] and observed['media'][0]['meta']['duration']==90
schedule=datetime.datetime.fromisoformat(observed['scheduled_at']).replace(tzinfo=datetime.timezone.utc);assert schedule>datetime.datetime.now(datetime.timezone.utc)
media=observed['media'][0];response=requests.get(media['url'],stream=True,timeout=90);response.raise_for_status();digest=hashlib.sha256();size=0
for part in response.iter_content(1024*1024):digest.update(part);size+=len(part)
assert digest.hexdigest()==post['export_sha256'] and size==d['assets'][0]['bytes']
timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat();d['assets'][0].update(public_url=media['url'],public_http_status=response.status_code,public_sha256=digest.hexdigest(),verified_at=timestamp)
post.update(readback_verified_at=timestamp,scheduled_at_utc=schedule.isoformat(),scheduled_at_local=schedule.astimezone(datetime.timezone(datetime.timedelta(hours=7))).isoformat(),timezone='Asia/Jakarta')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
ep=P/'EPISODE.md'
with ep.open('a',encoding='utf-8') as f:f.write(f'\n## Queue delivery complete\n\nTrypost post `{post["trypost_post_id"]}` read back as scheduled, queue mode, exact Instagram @dibalikbenda.id account, one 90-second video. Actual schedule: {post["scheduled_at_local"]} (Asia/Jakarta), {schedule.isoformat()} UTC. Public served copy HTTP {response.status_code}, SHA-256 and {size} bytes match final export. Caption differs only in LF→CRLF transport endings; both payload hashes retained. [Receipt](PUBLISHING.json). This is scheduled, not a claim of publication. No preview remains. Next: scoped commit requested by the user.\n')
with (P/'CONTENT_PACKAGE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Delivery receipt\n\nScheduled through Trypost Local for **27 October 2026, 10:00 Asia/Jakarta** ({schedule.isoformat()}). Post ID `{post["trypost_post_id"]}`. [Receipt](PUBLISHING.json). Public media bytes/hash match the final export. No live publication claimed; future monitoring not requested.\n')
tp=R/'TRACKER.json';t=json.loads(tp.read_text());next(x for x in t['productions'] if x['slug']==P.name).update(stage='publishing',status='complete');tp.write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'scheduled','post_id':post['trypost_post_id'],'scheduled_at':post['scheduled_at_local'],'public_media_verified':True,'sha256':digest.hexdigest()}))
