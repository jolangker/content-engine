from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;ROOT=P.parents[1];V=P/'video'
r=json.loads((P/'PUBLISHING.json').read_text(encoding='utf-8-sig'));a=r['assets'][-1];post=r['posts'][0]
assert a['status']=='verified' and post['status']=='draft'
assert a['sha256']==post['export_sha256']==hashlib.sha256((P/a['local_file']).read_bytes()).hexdigest()
assert post['payload_sha256']==hashlib.sha256(json.dumps(post['payload'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert post['provider_result']['text']==post['payload']['text']
assert post['provider_result']['assets'][0]['source']==a['secure_url']
for f in ['exports/kabar-baik-v1.mp4','exports/kabar-baik.srt','exports/kabar-baik.vtt','exports/cover-v1.png','exports/contact-sheet-v1.jpg','exports/verification-v1.json','SOURCES.md','SCRIPT.md']:
    assert (P/f).is_file() and (P/f).stat().st_size>0,f
package=P/'CONTENT_PACKAGE.md';text=package.read_text(encoding='utf-8')
text=text.replace('Local content package complete. Continue the already authorized Cloudinary hosting and Buffer draft action, saving actual provider IDs/status in PUBLISHING.json. This package does not claim the post is live.',f'''**Complete through the requested draft endpoint.** Original MP4 is publicly hosted and its downloaded SHA-256/bytes match this package. Buffer post `{post['buffer_post_id']}` has observed status `draft`, with the exact caption, media URL, 5357 ms thumbnail, Reel type, feed-sharing and AI declaration saved. No schedule or publication occurred.

Receipt: [PUBLISHING.json](PUBLISHING.json). [Hosted verified video]({a['secure_url']}). The provider did not return a direct Buffer post URL; the saved draft is under @eliansatya in My Organization.''')
package.write_text(text,encoding='utf-8')
ep=P/'EPISODE.md';text=ep.read_text(encoding='utf-8')
text=text.replace('Brief resolved. Research/script preparation in progress. No human approval claimed. Next: finalize bounded claims and narration, then measure audio and build the 14 compositions.','Complete through publishing/draft for version v1. The final receipt and next action are recorded below. No human approval is claimed.')
text+=f'''\n## Requested endpoint completed\n\nCloudinary asset `{a['asset_id']}` is verified against the exact local MP4, SHA-256 `{a['sha256']}`, {a['bytes']} bytes. A UUID suffix isolates the new asset because the connected signing preset returned overwrite:true despite the explicit false request. Exact target absence was verified before upload; no existing asset was replaced. Signed credentials were removed from temporary storage.\n\nBuffer **My Organization** / Instagram **@eliansatya**: post `{post['buffer_post_id']}`, observed status **draft**, created {post['created_at']}. Saved media, exact caption, Reel type, feed sharing, AI declaration and thumbnail offset were confirmed by the creation response. Due/sent times are null. Receipt: [PUBLISHING.json](PUBLISHING.json). The selected endpoint is complete; no scheduling/publication or future monitoring is requested.\n\nCurrent next action: none within this run. The user may review the saved draft or request a separate later action. Human approval remains unset; realtime creative listening was not available.\n'''
ep.write_text(text,encoding='utf-8')
with (V/'VERIFICATION.md').open('a',encoding='utf-8') as f:
    f.write(f'\n## External delivery evidence\n\nHosted original was downloaded without authentication; content-type video/mp4, byte size and SHA-256 exactly match the local export. Buffer creation returned saved draft {post["buffer_post_id"]} with the requested caption/media/settings and null due/sent times. PUBLISHING.json retains the observed response and payload fingerprint. Draft endpoint complete; no live-post claim.\n')
trackerpath=ROOT/'TRACKER.json';tracker=json.loads(trackerpath.read_text(encoding='utf-8-sig'));entry=next(x for x in tracker['productions'] if x['slug']=='kabar-baik');entry.update(stage='publishing',status='complete');trackerpath.write_text(json.dumps(tracker,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert set(tracker)=={'boards','productions'}
for e in tracker['boards']+tracker['productions']:assert (ROOT/e['path']).is_dir()
for target in re.findall(r'\]\(([^)]+)\)',package.read_text(encoding='utf-8')):
    if not target.startswith(('https://','http://')):assert (P/target).exists(),target
assert not Path('C:/Users/muhth/AppData/Local/Temp/codex-kabar-baik-upload-sign.json').exists()
print(json.dumps(dict(stage='publishing',status='complete',delivery='draft',buffer_post_id=post['buffer_post_id'],duration=86.1,export=a['local_file'])))
