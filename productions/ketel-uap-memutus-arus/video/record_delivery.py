"""Persist each observed post immediately; verify schedule and served bytes."""
from pathlib import Path
import json,sys,datetime,hashlib,requests,urllib.parse,socket,ipaddress
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2]
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
mode=sys.argv[1];remote=json.loads((V/('remote-post-created.json' if mode=='created' else 'remote-post-verified.json')).read_text(encoding='utf-8'))
receipt=json.loads((P/'PUBLISHING.json').read_text(encoding='utf-8'));post=receipt['posts'][0];asset=receipt['assets'][0];payload=post['payload']
assert remote['content']==payload['content'] and remote['content_type']==payload['content_type']
assert remote['social_account']['id']==post['social_account_id'] and remote['social_account']['username']==post['handle']
assert len(remote['media'])==1
media=remote['media'][0];assert media['type']=='video' and media['size']==asset['bytes']
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
post.update(trypost_post_id=remote['id'],status=remote['status'],provider_status=remote['status'],schedule_mode=remote.get('schedule_mode'),scheduled_at=remote.get('scheduled_at'),published_at=remote.get('published_at'),service_url=remote.get('platform_url'),media_ids=[media['id']],error=remote.get('error_message'),last_observed_at=now)
asset.update(status='attached',media_id=media['id'],trypost_post_id=remote['id'],attached_at=now)
dump(P/'PUBLISHING.json',receipt)
if mode=='created':
 print(json.dumps(dict(post_id=remote['id'],status=remote['status'],scheduled_at=remote.get('scheduled_at'),media_id=media['id'])));sys.exit(0)
assert remote['status']=='scheduled' and remote['schedule_mode']=='queue'
scheduled=datetime.datetime.fromisoformat(remote['scheduled_at']).replace(tzinfo=datetime.timezone.utc)
assert scheduled>datetime.datetime.now(datetime.timezone.utc)
url=media['url'];parts=urllib.parse.urlparse(url);assert parts.scheme=='https' and not parts.query and not parts.username
addresses={a[4][0] for a in socket.getaddrinfo(parts.hostname,443,type=socket.SOCK_STREAM)};assert all(ipaddress.ip_address(a).is_global for a in addresses)
r=requests.get(url,timeout=120,allow_redirects=False);assert r.status_code==200 and r.headers.get('content-type','').split(';')[0]=='video/mp4'
served_hash=hashlib.sha256(r.content).hexdigest();assert served_hash==asset['sha256'] and len(r.content)==asset['bytes']
asset.update(status='verified',served_url=url,served_http_status=r.status_code,served_sha256=served_hash,served_bytes=len(r.content),verified_at=now,anonymous_public_hostname_verified=True)
post.update(verified_at=now,scheduled_at_utc=scheduled.isoformat(),scheduled_at_local=scheduled.astimezone(datetime.timezone(datetime.timedelta(hours=7))).isoformat())
dump(P/'PUBLISHING.json',receipt)
t=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));next(x for x in t['productions'] if x['slug']==P.name).update(stage='publishing',status='complete');dump(R/'TRACKER.json',t)
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('\n## Queue endpoint complete\nTrypost Local re-read confirmed scheduled/queue for @'+post['handle']+', post ID='+remote['id']+', media ID='+media['id']+'. Assigned UTC='+scheduled.isoformat()+'; local='+post['scheduled_at_local']+'. Anonymous HTTPS media download returned200 with exact export SHA256 and bytes. [Receipt](PUBLISHING.json). Scheduled endpoint complete; publication is future and not claimed live. No future polling authorized/needed. Next: commit this production and its tracker entry; preserve unrelated workspace changes.\n')
with (P/'CONTENT_PACKAGE.md').open('a',encoding='utf-8') as f:f.write('\n## Observed queue result\nScheduled for '+post['scheduled_at_local']+' (Asia/Jakarta). Post ID: '+remote['id']+'. Exact attached media verified against export SHA256. See [receipt](PUBLISHING.json). This is a scheduled post, not a claim of publication.\n')
print(json.dumps(dict(status='scheduled',post_id=remote['id'],scheduled_at_local=post['scheduled_at_local'],served_sha256=served_hash,bytes=len(r.content))))
