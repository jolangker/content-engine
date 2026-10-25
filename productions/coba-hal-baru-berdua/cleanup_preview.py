"""Release only the recorded pipeline-owned preview and verify its listening port."""
from pathlib import Path
import json
import shutil
import subprocess
from datetime import datetime,timezone
P=Path(__file__).resolve().parent;V=P/'video';Q=V/'verification';owned=json.loads((Q/'preview-owner.json').read_text(encoding='utf-8'));npx=shutil.which('npx.cmd')
def cli(*args):
    p=subprocess.run([npx,'--yes','hyperframes@0.8.200','preview',*args,'--json'],cwd=V,capture_output=True,text=True,encoding='utf-8');p.check_returncode();return json.loads(p.stdout)
before=cli('--status');r=before['result'];assert r['state']=='running' and r['pid']==owned['pid'] and Path(r['projectDir']).resolve()==V
stopped=cli('--stop');after=cli('--status');assert after['result']['state']=='not-running'
p=subprocess.run(['powershell','-NoProfile','-Command',f"Get-NetTCPConnection -LocalPort {owned['port']} -State Listen -ErrorAction SilentlyContinue | Select-Object LocalAddress,LocalPort,OwningProcess | ConvertTo-Json -Compress"],capture_output=True,text=True)
owners=json.loads(p.stdout) if p.stdout.strip() else [];owners=[owners] if isinstance(owners,dict) else owners
assert all(x['OwningProcess']!=owned['pid'] for x in owners)
record=dict(status='passed',checked_at=datetime.now(timezone.utc).isoformat(),project=str(V),owned_pid=owned['pid'],owned_port=owned['port'],created_by_this_run=True,before=before,stop=stopped,after=after,listeners_after=owners,recorded_process_still_owns_port=False)
(Q/'preview-cleanup.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f"\n## Preview released\nPipeline-owned PID {owned['pid']} / port {owned['port']} stopped after export verification. Follow-up status is not-running and the TCP listener check confirms that PID no longer owns the port. No unrelated server terminated. Evidence: video/verification/preview-cleanup.json.\n")
print(json.dumps(dict(status='passed',pid=owned['pid'],port=owned['port'],listeners_after=owners)))
