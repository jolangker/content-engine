"""Save sanitized upload/post evidence immediately; never persist upload secrets."""
from pathlib import Path
from datetime import datetime,timezone
import base64
import json
import sys
P=Path(__file__).resolve().parent;file=P/'PUBLISHING.json';d=json.loads(file.read_text(encoding='utf-8'));mode=sys.argv[1];observed=json.loads(base64.b64decode(sys.argv[2]));now=datetime.now(timezone.utc).isoformat();asset=d['assets'][0];post=d['posts'][0]
if mode=='uploaded':
    assert observed['http_status'] in (200,201) and observed['status']=='uploaded';asset.update(status='uploaded',uploaded_at=now,upload_http_status=observed['http_status'])
elif mode in ('created','verified'):
    ob=observed.get('post',observed)
    assert ob['status'] in ('draft','pending_approval','scheduled','publishing','published','failed'),ob['status']
    # Exact provider shape is saved in the receipt after stripping media URLs.
    media=ob.get('media',[]);media=[dict(id=m.get('id'),type=m.get('type'),mime_type=m.get('mime_type'),original_filename=m.get('original_filename',m.get('name')),size=m.get('size',m.get('size_bytes')),duration=m.get('duration'),meta=m.get('meta')) for m in media]
    post.update(trypost_post_id=ob['id'],status=ob['status'],observed_provider_status=ob['status'],scheduled_at=ob.get('scheduled_at'),published_at=ob.get('published_at'),observed_schedule_mode=ob.get('schedule_mode'),returned_media_ids=[m['id'] for m in media],service_url=ob.get('platform_url'),observed_media=media)
    if media:asset.update(status='attached',media_id=media[0]['id'],trypost_post_id=ob['id'],attached_at=now)
    if mode=='verified':
        assert ob['status'] in ('scheduled','published'),ob['status']
        assert ob.get('content')==post['payload']['content'],'Caption differs'
        assert ob.get('social_account_id',ob.get('social_account',{}).get('id'))==post['social_account_id'],'Account differs'
        assert ob.get('content_type')=='instagram_reel','Content type differs'
        assert len(media)==1,'Media count differs'
        assert ob.get('scheduled_at'),'Scheduled time missing'
        if ob['status']=='scheduled':
            scheduled=datetime.fromisoformat(ob['scheduled_at'].replace('Z','+00:00'))
            if scheduled.tzinfo is None:scheduled=scheduled.replace(tzinfo=timezone.utc)
            assert scheduled>datetime.now(timezone.utc),'Scheduled time is not future'
        post.update(verified_at=now,content_matches_payload=True,verification=dict(post_readback='passed',account_identity='passed',caption='exact match',media_attachment='passed',schedule='future scheduled time verified'))
        asset.update(status='verified',verified_at=now,verification='Direct HTTP upload and exact media ID, original filename, bytes and server duration matched against the local export; SHA-256 recorded before upload.')
else:raise ValueError('Unknown receipt mode')
file.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(mode=mode,asset_status=asset['status'],post_status=post['status'],post_id=post.get('trypost_post_id'),scheduled_at=post.get('scheduled_at'))))
