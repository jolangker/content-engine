"""Reconcile the completed queue endpoint and final local handoff."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
P=Path(__file__).resolve().parent;ROOT=P.parents[1];V=P/'video';receipt=json.loads((P/'PUBLISHING.json').read_text(encoding='utf-8'));post=receipt['posts'][0];asset=receipt['assets'][0]
assert post['status']=='scheduled' and asset['status']=='verified'
due=datetime.strptime(post['scheduled_at'],'%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc);assert due>datetime.now(timezone.utc)
assert hashlib.sha256((P/asset['local_file']).read_bytes()).hexdigest()==asset['sha256']==post['export_sha256']
assert not any(key in json.dumps(receipt) for key in ('upload_token','upload_url','signature='))
assert json.loads((V/'verification/preview-cleanup.json').read_text(encoding='utf-8'))['status']=='passed'
post['scheduled_at_utc']=due.isoformat();post['scheduled_at_local']='2026-10-27T14:00:00+07:00';post['timezone']='Asia/Jakarta';post['verification']['schedule']='future queued time confirmed against fresh current time; 2026-10-27 07:00:00 UTC = 14:00 WIB'
post['verification']['media_bytes']=4580998;post['verification']['media_duration_s']=90;post['verification']['media_filename']='coba-hal-baru-berdua-v1.mp4'
(P/'PUBLISHING.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
text=(P/'EPISODE.md').read_text(encoding='utf-8').replace('## Current state\n\nScript and research verified.','## Initial handoff (historical)\n\nScript and research verified.')
text+='''
## Final outcome

All dependencies through the requested queue endpoint are complete for v1. Trypost post 01a17526-698f-718d-9c04-3edf42bad872 was created exactly once after a zero-match account/content duplicate check. Direct local upload returned HTTP201; attached media 01a17526-42c9-70a5-b45f-7fccc65ca078 matched original filename, 4580998 bytes and server-measured 90s. Readback confirmed exact caption, instagram_reel, exact connected @eliansatya identity, schedule_mode=queue and status=scheduled.

Actual schedule: 2026-10-27 07:00:00 UTC = 27 October 2026, 14:00 WIB (Asia/Jakarta), a future instant verified against the current clock. published_at remains null; no live publication is claimed. Receipt: PUBLISHING.json. This is the next configured queue slot selected by the service, not an invented custom time.

Delivery: exports/coba-hal-baru-berdua-v1.mp4, exports/coba-hal-baru-berdua.srt, CONTENT_PACKAGE.md and exports/export-proof.png. Export and all six SFX-presence checks passed; direct listening unavailable as disclosed. Agent-verified under delegated automation, no human approval fabricated. Pipeline preview PID4560/port3002 released and verified. No remaining production blocker or required review. Future publication monitoring is outside this completed queue request.

Next action: create the explicitly requested local Git commit for this episode and its narrow tracker addition. Preserve the unrelated pre-existing gua-kira-udah-kelihatan files and tracker change. Rendered video/audio and generated proof PNGs follow existing Git ignore rules and remain locally available.
'''
(P/'EPISODE.md').write_text(text,encoding='utf-8')
with (P/'CONTENT_PACKAGE.md').open('a',encoding='utf-8') as f:f.write('\n## Queue receipt\n\nScheduled in Trypost for **27 October 2026, 14:00 WIB**, returned 2026-10-27 07:00:00 UTC. Post ID: 01a17526-698f-718d-9c04-3edf42bad872. Status scheduled; published_at null. Account, exact copy, attached file identity and schedule verified by post readback. See PUBLISHING.json.\n')
with (V/'BRIEF.md').open('a',encoding='utf-8') as f:f.write('\n# Completed handoff\n\nV1 verified export and queue delivery completed. Actual schedule 2026-10-27T14:00:00+07:00, exact receipt in ../PUBLISHING.json. Pipeline-owned Studio preview was stopped and port ownership verified. No human approvals or live publication claimed.\n')
tracker=json.loads((ROOT/'TRACKER.json').read_text(encoding='utf-8'));next(x for x in tracker['productions'] if x['slug']==P.name).update(stage='publishing',status='complete');(ROOT/'TRACKER.json').write_text(json.dumps(tracker,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all((ROOT/x['path']).is_dir() for x in tracker['boards']+tracker['productions'])
print(json.dumps(dict(status='complete',post_id=post['trypost_post_id'],scheduled_at_local=post['scheduled_at_local'])))
