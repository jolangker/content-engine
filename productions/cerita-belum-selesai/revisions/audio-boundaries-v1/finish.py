from pathlib import Path
import json,subprocess,hashlib
BASE=Path(__file__).resolve().parent;ROOT=BASE.parent.parent;V=BASE/'video'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def cli(*args):
    p=subprocess.run(['npx.cmd','hyperframes@0.8.197',*args],cwd=V,capture_output=True,text=True,encoding='utf-8',errors='replace',check=True)
    return json.loads(p.stdout)
export=read(V/'verification/export.json');sound=read(V/'verification/sound-design-export.json')
assert export['status']==sound['status']=='passed'
stop=cli('preview','--stop','--json');status=cli('preview','--status','--json')
assert status['result']['state']=='not-running',status
p=subprocess.run(['powershell','-NoProfile','-Command','Get-NetTCPConnection -LocalPort 3002 -State Listen -ErrorAction SilentlyContinue | Select-Object LocalAddress,LocalPort,OwningProcess | ConvertTo-Json -Compress'],capture_output=True,text=True)
owners=json.loads(p.stdout) if p.stdout.strip() else []
if isinstance(owners,dict):owners=[owners]
assert all(x['OwningProcess']!=21360 for x in owners)
process=subprocess.run(['powershell','-NoProfile','-Command','Get-CimInstance Win32_Process -Filter "ProcessId = 21360" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress'],capture_output=True,text=True)
cleanup=dict(status='passed',project=str(V),recorded_pid=21360,recorded_port=3002,stop=stop,managed_status=status,port_owners_after_stop=owners,recorded_pid_process_after_stop=json.loads(process.stdout) if process.stdout.strip() else None)
(V/'verification/preview-cleanup.json').write_text(json.dumps(cleanup,indent=2)+'\n',encoding='utf-8')
doc=f'''# Verification — Cerita belum selesai v1

Status: complete at the requested **export** endpoint. Agent-verified under the user's `--automation` instruction. No human editorial or perceptual audio approval is claimed.

## Delivered files

- [MP4](exports/cerita-belum-selesai-v1.mp4): {export['duration_s']:.3f}s, 1080 × 1920, 30 fps, H.264/AAC, {export['bytes']/1e6:.2f} MB.
- [Spoken captions](exports/cerita-belum-selesai.srt): 38 phrases, all 194 spoken words, no delivery tags.
- [Decoded export proof sheet](exports/proof-sheet.jpg).
- [Visual storyboard](video/boards/storyboard.html) and [full PNG](video/boards/storyboard.png): all 16 styled planning poses, 1640 × 3531px review image. Later timing labels use measured narration.

## Evidence

Render uses pinned HyperFrames 0.8.197, local GSAP/fonts and seekable scene timelines. The CLI full check passed runtime, layout and contrast without errors. Reviewed exceptions: approved canonical 26px chrome versus generic 28px craft threshold; 38 caption segments intentionally share one dedicated caption track. Studio also scans the required storyboard HTML and inherited chrome fragment as standalone compositions; its two missing-root-ID findings concern those documents, not renderable video scenes.

Creative review covered exactly 16 meaningful compositions, 14 cream and two charcoal frames (04 and 12), silhouette continuity, restrained selective copy and complete caption coverage. Four illustrated states per scene were inspected, and pixel-change checks excluded caption/chrome areas. The full Studio player reached 86s with no page errors; the narration reached 84.8s at native speed. The final quiet visual tail is 1.2s. No B-roll or music bed.

The final MP4 fully decodes. Sixteen decoded frames agree with matching seeked preview states (mean absolute RGB errors recorded in [export.json](video/verification/export.json)). Five planned material cues passed independent waveform matching in the AAC export, including timing/gain checks; see [sound-design-export.json](video/verification/sound-design-export.json). Measured final integrated loudness: {export['loudness']['input_i']} LUFS, true peak {export['loudness']['input_tp']} dBTP. The original TTS cache is preserved; the mix uses a duration-preserving loudness derivative.

Perceptual listening was unavailable. Native alignment, playback progression, full decode, levels and cue waveform matches provide technical evidence, not a claim about human-perceived naturalness or mix balance. Research and authored-example limits are in [SOURCES.md](SOURCES.md).

## Resource lifecycle and scope

Pipeline preview PID 21360 / port 3002 stopped through the project CLI after export verification. Managed status is not-running and the recorded PID no longer owns the listening port. [Cleanup evidence](video/verification/preview-cleanup.json).

No content package, upload or external delivery was requested under the export cap. Further work requires a new continuation request. Board and generation metadata remain frozen with this production.

MP4 SHA-256: `{export['sha256']}`.
'''
(BASE/'VERIFICATION.md').write_text(doc,encoding='utf-8')
with (BASE/'EPISODE.md').open('a',encoding='utf-8') as f:
    f.write(f'\n## Final outcome\nCurrent stage: export. Status: complete. MP4 {export["duration_s"]:.3f}s, 1080x1920/30fps, {export["bytes"]} bytes. Full decode, sixteen preview/export frame comparisons and all five exported cue waveform checks passed. See VERIFICATION.md and video/verification/. Render used drawelement capture with hardware Intel D3D11 GPU on Windows (2m36.8s render). Preview PID 21360/port 3002 released and verified after export; no pipeline preview hold remains. Listening limits recorded honestly. Stop at export; no content package or external delivery.\n')
tracker=read(ROOT/'TRACKER.json')
for row in tracker['productions']:
    if row['slug']==BASE.name:row.update(stage='export',status='complete')
(ROOT/'TRACKER.json').write_text(json.dumps(tracker,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert (ROOT/next(x for x in tracker['productions'] if x['slug']==BASE.name)['path']).is_dir()
print(json.dumps(dict(stage='export',status='complete',cleanup=cleanup['status'],export=export['export'],duration=export['duration_s'])))
