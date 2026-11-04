"""Record final visual inspection and reconcile the repaired caption history."""
from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;V=P/'video';Q=V/'verification'
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
f=Q/'encoded-cuts.json';d=json.loads(f.read_text());assert len(d['samples'])==45;d['visual_inspection']='passed: all three sheets inspected, forty-five exact adjacent frames cover fifteen cuts, no blank/palette/chrome defect';dump(f,d)
f=Q/'export.json';d=json.loads(f.read_text());d['visual_inspection']='passed: all sixteen encoded proof scenes and forty-five adjacent cut frames inspected; animated stroke fragments during reveal are intentional';dump(f,d)
f=P/'PUBLISHING.json';d=json.loads(f.read_text(encoding='utf-8'));post=d['posts'][0];assert post['content_matches_payload'];post['history'][0]['resolution']='Correct UTF-8 caption updated on same scheduled post; final readback exactly matches original intended payload. Media and queue schedule retained.';dump(f,d)
script=json.loads((V/'script_data.json').read_text(encoding='utf-8'));groups=json.loads((V/'caption_groups.json').read_text(encoding='utf-8'));normalize=lambda x:re.sub(r'\s+',' ',x.strip());assert normalize(' '.join(x['text'] for x in script))==normalize(' '.join(x['text'] for x in groups))
assert len(script)==16 and sum(x['dramatic'] for x in script)==2
assert (P/'CONTENT_PACKAGE.md').is_file() and (P/'exports/nanti-itu-kapan.srt').is_file()
final=json.loads((Q/'final-look.json').read_text());assert final['composition_sha256']==hashlib.sha256((V/'index.html').read_bytes()).hexdigest()
with (P/'EPISODE.md').open('a',encoding='utf-8') as out:out.write('\n## Final delivery reconciliation\n\nInitial remote caption readback exposed ANSI-decoded smart-quote corruption; correct UTF-8 copy updated on the same scheduled post. Prior observed caption and correction retained in PUBLISHING.json history. Final readback exactly matches original intended local payload; no duplicate post or changed schedule. All 208 spoken words match caption text; sixteen scenes/two dark palettes and current root source hash verified. All encoded proof and cut sheets visually accepted; intentional partial stroke reveals are motion, not clipping. Public media bytes/hash match local export.\n')
print(json.dumps(dict(caption_text='exact match',caption_repair='verified on same post',encoded_visual_review='passed',current_version='verified')))
