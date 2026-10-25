from pathlib import Path
import datetime,hashlib,json,requests
B=Path(__file__).resolve().parent;R=B.parent.parent;path=B/'PUBLISHING.json';r=json.loads(path.read_text(encoding='utf-8'));a=r['assets'][-1];p=r['posts'][-1];now=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert p['provider_status']=='draft' and p['content_matches_package'] and p['trypost_post_id'] and a['media_id']
url=a['observed_media']['url'];response=requests.get(url,timeout=(20,120));response.raise_for_status()
assert response.headers.get('Content-Type','').startswith('video/')
assert len(response.content)==a['bytes'] and hashlib.sha256(response.content).hexdigest()==a['sha256']
a.update(status='verified',verified_at=now,served_media_check=dict(status='verified',url=url,http_status=response.status_code,bytes=len(response.content),sha256=a['sha256']))
p.update(verified_at=now,verification=dict(status='passed',scope='Read-back draft status, exact account, exact caption, one attached video, served-file bytes/SHA-256, no schedule or publication'))
path.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (B/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Draft delivery complete\nCurrent stage: publishing. Status: complete. Requested Trypost draft verified for Instagram @eliansatya in Admin\'s Workspace. Post ID {p["trypost_post_id"]}; media {a["media_id"]}. Exact package caption, content type, account and attached verified export checked by read-back. Served media SHA-256/bytes match export. No schedule/publication requested or observed. Receipt PUBLISHING.json. Preview cleanup verified. User-requested Git commit is next.\n')
with (B/'CONTENT_PACKAGE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Delivery receipt\nTrypost draft verified: post `{p["trypost_post_id"]}`, Instagram @eliansatya, media `{a["media_id"]}`. Exact caption and export verified. No schedule or publication. See [PUBLISHING.json](PUBLISHING.json).\n')
with (B/'VERIFICATION.md').open('a',encoding='utf-8') as f:f.write(f'\n## External draft verification\nTrypost read-back returned draft for exact Instagram account and one attached video, matching caption and media metadata. Publicly served copy returned HTTP 200 and full SHA-256/byte match. Post {p["trypost_post_id"]}. No schedule or publication observed. PUBLISHING.json retains evidence.\n')
t=json.loads((R/'TRACKER.json').read_text());next(x for x in t['productions'] if x['slug']==B.name).update(stage='publishing',status='complete');(R/'TRACKER.json').write_text(json.dumps(t,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(stage='publishing',status='complete',post_id=p['trypost_post_id'],draft_verified=True)))
