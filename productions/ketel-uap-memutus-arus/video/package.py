"""Package only the verified export and persist a token-free queue intent."""
from pathlib import Path
import json,hashlib,datetime
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2]
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
v=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));dest=P/v['local_file']
assert hashlib.sha256(dest.read_bytes()).hexdigest()==v['sha256']
for name in ['audio-boundaries-export-v2.json','sound-design-export-v2.json','motion.json','captions.json']:
 report=json.loads((V/'verification'/name).read_text(encoding='utf-8'))
 assert report['status']=='passed',f'Unverified dependency: {name}'
accounts=json.loads((R/'boards/di-balik-benda/ACCOUNTS.json').read_text(encoding='utf-8'))['accounts'];assert len(accounts)==1
a=accounts[0]
caption='''Airnya mendidih, lalu ketel mati sendiri. Pada contoh mekanisme ini, uap melewati saluran khusus dan memanaskan cakram bimetal. Cakram menyentak, tuas serta batang penghubung bergerak, lalu kontak listrik terpisah.

Yang memicu pemutusnya adalah panas uap yang mencapai sensor di luar ruang air. Saat listrik terputus, panas yang sudah tersimpan tetap perlu waktu untuk mereda.

Ini contoh ketel dengan pemutus mekanis berbasis uap; desain lain bisa berbeda. Ilustrasi dan jarak gerak diperbesar, waktu pemanasan diringkas, serta interaksi diperlambat agar terbaca.

Rujukan: Ingenia/Royal Academy of Engineering — https://www.ingenia.org.uk/articles/how-do-kettles-know-when-to-switch-off
Mekanisme acuan: https://patents.google.com/patent/US4357520A/en

#DiBalikBenda #KetelListrik #CaraKerja #Mekanisme #SainsSehariHari'''
assert len(caption)<=2200 and caption.count('#')==5
(V/'post-caption.txt').write_text(caption,encoding='utf-8')
package=f'''# Kenapa Ketel Bisa Mati Sendiri?

## Title options
Recommended: Kenapa Ketel Bisa Mati Sendiri?

Alternatives: Uap yang Memicu Sakelar Ketel; Dari Air Mendidih ke Kontak Terputus.

## Instagram caption — ready to post
{caption}

## Editorial keywords
ketel listrik, pemutus uap, bimetal, sakelar otomatis, termostat mekanis, kontak listrik, cara kerja ketel

## Cover
Opening frame at0ms; actual text: “Kok tahu harus mati?” No separate illustration or text has been invented for the cover.

## Verified delivery metadata
- Production: {P.name}; board di-balik-benda v6; language Indonesian.
- Target: Instagram @{a['handle']}; Trypost Local / {a['workspace_name']}.
- Requested action: queue in next configured slot, daily10:00Asia/Jakarta. Actual assigned instant belongs in PUBLISHING.json after scheduling.
- Version: v1; MP4 H.264/AAC, {v['width']}x{v['height']},9:16,30fps,{v['frames']}frames,{v['duration_s']:.3f}s,{v['bytes']}bytes.
- SHA-256: {v['sha256']}.
- [Video]({v['local_file']})
- [SRT](exports/{P.name}-v1.srt), [WebVTT](exports/{P.name}-v1.vtt); captions burned in and included as sidecars.
- [Cover](exports/{P.name}-v1-cover.png), extracted from the verified first frame.
- [Source map](SOURCES.md), [script](SCRIPT.md), [review](video/REVIEW.md), [export verification](video/verification/export.json).
- Subjective audio listening was unavailable. Waveform seams, cue presence and level evidence are separate from perceptual review. No human approval claimed.
- Optional upload settings other than0mscover selection remain unset. No sponsorship, visibility or rights declaration inferred.
'''
for file in [dest,P/'exports'/f'{P.name}-v1.srt',P/'exports'/f'{P.name}-v1.vtt',P/'exports'/f'{P.name}-v1-cover.png']:assert file.is_file()
(P/'CONTENT_PACKAGE.md').write_text(package,encoding='utf-8')
payload=dict(provider='trypost',workspace_id=a['workspace_id'],workspace_name=a['workspace_name'],social_account_id=a['social_account_id'],service=a['service'],handle=a['handle'],content_type='instagram_reel',content=caption,media_source=dict(export_sha256=v['sha256'],route='local_upload'),meta=dict(cover_offset_ms=0),requested_delivery='queue',requested_due_at=None,queue='next')
intent=dict(payload=payload,payload_sha256=hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest())
dump(V/'posting-intent.json',intent)
t=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));next(x for x in t['productions'] if x['slug']==P.name).update(stage='content_package',status='complete');dump(R/'TRACKER.json',t)
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('\n## Verified package\nCONTENT_PACKAGE.md matches export v1 and actual metadata. All delivery links exist; Instagram caption length='+str(len(caption))+', five relevant hashtags. Next: reconcile duplicate search, upload exact verified bytes, schedule queue next and save observed receipt. No second draft-review gate under active automation.\n')
print(json.dumps(dict(status='complete',caption_characters=len(caption),export_sha256=v['sha256'])))
