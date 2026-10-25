from pathlib import Path
import json,datetime
from zoneinfo import ZoneInfo
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;rpath=P/'PUBLISHING.json'
r=json.loads(rpath.read_text(encoding='utf-8'));p=r['posts'][-1];a=r['assets'][-1]
assert p['status']=='published' and p['provider_status']=='published' and p['content_matches_package']
assert a['status']=='verified' and a['public_media_check']['sha256']==p['export_sha256']
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
dt=datetime.datetime.strptime(p['published_at'],'%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc)
p.update(verified_at=now,published_at_timezone='UTC',published_at_local=dt.astimezone(ZoneInfo('Asia/Jakarta')).isoformat(),verification=dict(status='passed',scope='Provider-observed published status, exact target account, full package caption, one verified attached export and returned platform URL'))
rpath.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
entry=f'''\n## Publication complete\nCurrent stage: publishing. Status: complete. Trypost observed published / publish_status published for Instagram @eliansatya. Post ID: {p['trypost_post_id']}. Published at {p['published_at']} UTC ({p['published_at_local']}, Asia/Jakarta). Returned URL: {p['service_url']}. The first status check reported a temporary platform outage and retrying; the same post then published automatically. No replacement post or second upload was created. Exact caption and attached verified export retained. [Receipt](PUBLISHING.json); [content package](CONTENT_PACKAGE.md). No further action pending for this publish-now request.\n'''
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(entry)
with (P/'CONTENT_PACKAGE.md').open('a',encoding='utf-8') as f:
    f.write(f'\n## Delivery receipt\nPublished via Trypost to Instagram @eliansatya at {p["published_at_local"]} (Asia/Jakarta). [Live Reel]({p["service_url"]}). Trypost post {p["trypost_post_id"]}. Status verified published; see PUBLISHING.json.\n')
with (P/'VERIFICATION.md').open('a',encoding='utf-8') as f:
    f.write(f'\n## Subsequent publishing continuation\nThe user explicitly extended the earlier export-only scope with “publish sekarang via trypost”. The existing video was reused without regeneration. Public served media matched the full export SHA-256 and byte range; exact package caption was checked before publication. Trypost confirmed published at {p["published_at_local"]}; [live Reel]({p["service_url"]}). See PUBLISHING.json for the preserved receipt and transient retry observation.\n')
t=json.loads((ROOT/'TRACKER.json').read_text(encoding='utf-8'))
next(x for x in t['productions'] if x['slug']==P.name).update(stage='publishing',status='complete')
(ROOT/'TRACKER.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(stage='publishing',status='complete',url=p['service_url'],published_at_local=p['published_at_local'])))
