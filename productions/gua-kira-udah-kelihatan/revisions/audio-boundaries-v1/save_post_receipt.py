from pathlib import Path
import json,sys
from datetime import datetime,timezone
observed=json.loads(sys.stdin.readline())
p=Path('productions/gua-kira-udah-kelihatan/PUBLISHING.json');d=json.loads(p.read_text(encoding='utf-8'));post=d['posts'][0];post.update(trypost_post_id=observed['id'],status=observed['status'],observed_provider_status=observed['status'],scheduled_at=observed['scheduled_at'],published_at=observed['published_at'],returned_media_ids=observed['media_ids'],service_url=observed['platform_url'],created_at=observed['created_at']);a=d['assets'][0];a.update(status='attached',media_id=observed['media_ids'][0],trypost_post_id=observed['id'],attached_at=datetime.now(timezone.utc).isoformat());p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
