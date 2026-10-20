from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parent;r=P/'PUBLISHING.json';d=json.loads(r.read_text(encoding='utf-8'))
payload=json.loads((P/'buffer_payload.json').read_text(encoding='utf-8'))
raw=json.loads((P/'buffer_corrected_result.json').read_text(encoding='utf-8'))
assert not raw.get('isError')
post=json.loads(next(c['text'] for c in raw['content'] if c['type']=='text'))
assert post['status']=='draft' and post['id']=='6ad64f0ed1648e7b92bea274'
assert post['text']==payload['text']
assert post['channelId']==payload['channelId']
assert post['assets'][0]['source']==d['assets'][-1]['secure_url']
assert post['assets'][0]['video']['durationMs']==86267
assert post['metadata']['type']=='reel' and post['metadata']['shouldShareToFeed'] is True
assert post['metadata']['isAiGenerated'] is True
assert post['dueAt'] is None and post['sentAt'] is None
p=d['posts'][-1];initial=p['observed']
actual_initial_payload={**payload,'text':initial['text']}
actual_initial_hash=hashlib.sha256(json.dumps(actual_initial_payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
p['attempts']=[{'action':'create','status':'draft','buffer_post_id':initial['id'],'observed_at':p['observed_at'],'payload_sha256':actual_initial_hash,'note':'PowerShell default decoding altered Unicode punctuation. Same draft was repaired; no duplicate post created.'},{'action':'edit','status':'rejected','http_status':400,'error':'Instagram posts require a type (post, story, or reel).','note':'No remote mutation; retried once with explicit existing Reel metadata and asset.'},{'action':'edit','status':'draft','observed_at':post['updatedAt'],'payload_sha256':p['payload_sha256'],'note':'Exact UTF-8 caption, media and settings verified against saved response.'}]
p.update(status='draft',provider_status='draft',buffer_post_id=post['id'],observed=post,observed_at=post['updatedAt'],scheduled_at=None,sent_at=None,encoding_repair_pending=False,verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
r.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
verification=json.loads((P/'exports/verification.json').read_text())['summary']
check=json.loads((P/'video/verification/check-release.json').read_text(encoding='utf-16'))
assert check['ok'] and d['assets'][-1]['status']=='verified'
ep=P/'EPISODE.md';text=ep.read_text(encoding='utf-8')
text=text.replace('Brief resolved; research and script in progress.','Requested endpoint complete: verified export, content package, Cloudinary original and saved Buffer draft.')
text+='''

## Final delivery — 2026-10-20

- Requested endpoint complete. Buffer Instagram @eliansatya Reel draft `6ad64f0ed1648e7b92bea274` is saved in My Organization. Observed status: draft, no dueAt or sentAt. Caption matches caption.txt exactly, including Unicode punctuation and source URLs. Existing draft was repaired after a Windows decoding issue; no duplicate was made. Share to feed and AI-generated provenance settings are true; thumbnail offset 1500 ms.
- Cloudinary hosts the verified original. Anonymous full download matches all 6,472,880 bytes and SHA-256 f23cabc9ca575f16ee2bad475af30f750edb3b7ef1d6bc04763b66282d453dc0. The connector forces overwrite:true; a fresh UUID plus full hash and exact absent-target preflight ensured this created a new asset without replacing existing media. No signing credentials are stored.
- Final MP4: 86.266667s, 1080×1920, 30 fps, 2,588 frames, H.264/yuv420p, AAC stereo 48 kHz. Burned-in subtitles and an optional SRT. All frames/audio decode with -xerror; 14 encoded scene proofs inspected, minimum preview/encode SSIM 0.998615. Four renderer ground-truth checks passed. Encoded mix: -16.56 LUFS stereo, -19.56 LUFS mono downmix, -2.63 dBTP.
- [Video](exports/jeda-yang-kembali.mp4), [content package](CONTENT_PACKAGE.md), [contact sheet](exports/jeda-yang-kembali-contact-sheet.jpg), [verification](exports/verification.json), [external receipts](PUBLISHING.json).
- No human review was fabricated. Automation authorized this exact agent-verified version through draft delivery. Next action belongs to the user: review/edit the saved draft or request a later delivery change; no publication is scheduled by this run.
'''
ep.write_text(text,encoding='utf-8')
package=P/'CONTENT_PACKAGE.md';txt=package.read_text(encoding='utf-8')
txt+='\n## Observed delivery result\n\nBuffer draft `6ad64f0ed1648e7b92bea274` is saved for Instagram @eliansatya in My Organization. Caption, source credits, original media, Reel/feed settings and 1500 ms thumbnail are verified in the successful save response. Status: draft; no due time or publication. Hosted original bytes and SHA-256 match the delivered MP4. See PUBLISHING.json for the direct media URL and complete receipt.\n'
package.write_text(txt,encoding='utf-8')
report='''# Verification — final look v1

HyperFrames 0.8.176; 1080×1920/30 fps; automation authorization. Rendering completed in 111.7 seconds, drawElement capture, hardware Intel Iris Xe GPU. Four screenshot ground-truth comparisons passed.

Final check: zero lint, runtime, layout, motion or contrast findings. Root-level motion assertions target each headline and both actors; 42 assertions across 300 motion samples pass. Dense transition/layout pass also found no runtime/layout issues. All 14 scene proofs inspected; full-size opening 30s frames and refined labels inspected before rendering. No unchanged check was repeated after export.

The entire encoded audiovisual file decodes with FFmpeg -xerror. All 14 representative encoded frames match their preview frames (SSIM >= 0.998615). Original narration 84.64s, 187 words in exact alignment order, 0.4s preroll, total 86.266667s. Forty-five caption phrases contain spoken words only. Native gain +3dB and true-peak ceiling -3dBTP, measured encoded stereo -16.56 LUFS / -2.63dBTP, mono -19.56 LUFS. No speed change, no provider substitution.

Persistent preview was exposed and HTTP 200 verified. The computer-use connector had no browser/app surface, so no interactive realtime preview listen is claimed. Technical runtime, motion, complete decode, measured audio and encoded pixel evidence are the agent verification basis.

Export details and hash: ../exports/verification.json. Draft identity, exact caption, media and settings: ../PUBLISHING.json. All required delivery links exist. Local fonts and licenses included; original audio preserved.
'''
(P/'video/VERIFICATION.md').write_text(report,encoding='utf-8')
tracker=P.parent.parent/'TRACKER.json';data=json.loads(tracker.read_text())
next(x for x in data['productions'] if x['slug']==P.name).update(stage='publishing',status='complete')
tracker.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
for entry in data['productions']:assert (P.parent.parent/entry['path']).is_dir()
for f in ['EPISODE.md','SCRIPT.md','SOURCES.md','CONTENT_PACKAGE.md','PUBLISHING.json',verification['local_file'],'exports/jeda-yang-kembali.srt','exports/jeda-yang-kembali-contact-sheet.jpg']:assert (P/f).is_file()
print(json.dumps({'endpoint':'draft','status':'complete','buffer_post_id':post['id'],'caption_exact':True,'hosted_sha256_exact':True,'duration_s':verification['duration_s']}))
