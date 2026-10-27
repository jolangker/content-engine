from pathlib import Path
import json,subprocess,shutil,datetime
B=Path(__file__).resolve().parent;V=B/'video';npx=shutil.which('npx.cmd')
def cli(*args):
    p=subprocess.run([npx,'--yes','hyperframes@0.8.198','preview',*args,'--json'],cwd=V,capture_output=True,text=True,encoding='utf-8');p.check_returncode();return json.loads(p.stdout)
before=cli('--status');r=before['result'];assert r['state']=='running' and r['pid']==26224 and Path(r['projectDir']).resolve()==V
stopped=cli('--stop');after=cli('--status')
assert after['result']['state']=='not-running'
p=subprocess.run(['powershell','-NoProfile','-Command','Get-NetTCPConnection -LocalPort 3002 -State Listen -ErrorAction SilentlyContinue | Select-Object LocalAddress,LocalPort,OwningProcess | ConvertTo-Json -Compress'],capture_output=True,text=True)
owners=json.loads(p.stdout) if p.stdout.strip() else []
if isinstance(owners,dict):owners=[owners]
assert all(x['OwningProcess']!=26224 for x in owners)
record=dict(status='passed',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),project=str(V),owned_pid=26224,owned_port=3002,created_by_this_run=True,before=before,stop=stopped,after=after,listeners_after=owners,recorded_process_still_owns_port=False)
(V/'verification/preview-cleanup.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
with (B/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('\n## Preview released\nPipeline-owned PID 26224 / port 3002 stopped with resolved CLI after export verification. Follow-up status not-running and TCP listener query confirm the recorded process no longer owns the port. No unrelated server terminated. Evidence: video/verification/preview-cleanup.json.\n')
print(json.dumps(dict(status='passed',pid=26224,port=3002,listeners_after=owners)))
