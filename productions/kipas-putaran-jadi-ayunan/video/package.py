"""Package the verified export and freeze the exact queue intent."""
from pathlib import Path
import json,hashlib,re
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2]
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
e=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));assert e['status']=='passed'
assert hashlib.sha256((P/e['local_file']).read_bytes()).hexdigest()==e['sha256']
caption='''Baling-balingnya terus searah. Kenapa kepala kipas bisa bolak-balik?

Pada kipas mekanis tipe ini, putaran motor diteruskan lewat roda gigi ke pin engkol. Batang penghubung mengikat pin itu pada jangkar di penyangga. Panjang batang yang tetap membuat kepala berayun saat pin terus mengorbit.

Kenop mengendalikan kopling pada jalur ayunan, sementara baling-baling tetap digerakkan motor.

Ilustrasi dan kecepatan gerak disederhanakan; bentuk kopling ditampilkan secara konsep. Desain kipas lain bisa berbeda. Bunyi mekanisme bersifat ilustratif.

Rujukan teknis:
https://patents.google.com/patent/US7811059B2/en

#DiBalikBenda #CaraKerja #KipasAngin #Mekanisme #Teknik'''
assert len(caption)<=2200 and len(re.findall(r'#\w+',caption))<=5
files=[e['local_file']]+[f'exports/{P.name}-v1{suffix}' for suffix in ['.srt','.vtt','-cover.png']]
assert all((P/f).is_file() and (P/f).stat().st_size for f in files)
package=f'''# Content package — Kipas: Putaran Jadi Ayunan

## Titles
Recommended: **Baling-Baling Searah, Kepala Bolak-Balik. Kok Bisa?**

Alternatives:
- Satu Motor, Dua Gerakan Kipas
- Kenop Ditarik, Kenapa Baling-Baling Tetap Jalan?

## Ready-to-post Instagram caption

{caption}

## Hashtags
#DiBalikBenda #CaraKerja #KipasAngin #Mekanisme #Teknik

## Editorial keywords
cara kerja kipas angin, osilasi kipas, batang penghubung, pin engkol, roda gigi ulir, kopling kipas, gerak melingkar menjadi ayunan

These are editorial discovery terms, not a dedicated Instagram upload field.

## Cover
Implemented local cover uses opening-frame title **Kenapa bisa bolak-balik?**, decoded from finalMP4 at2.0s. Optional remote cover settings are unset; no claim the local PNG is applied remotely.

## Verified delivery metadata
| Field | Value |
| --- | --- |
| Production | {P.name} |
| Board | Di Balik Benda v6 |
| Language | Indonesian |
| Destination | Instagram Reel @dibalikbenda.id |
| Workspace | Admin's Workspace /01a171dd-5281-730d-af07-f2168d17add7 |
| Account | 01a172c9-3761-700a-9798-00febaa9fa90 |
| Version | v1 |
| Duration | {e['duration_s']:.3f}s |
| Dimensions / aspect | 1080x1920 /9:16 |
| Frame rate / count | 30fps /2700 |
| Format | MP4,H.264/AAC |
| Bytes | {e['bytes']} |
| SHA-256 | {e['sha256']} |
| Captions | Burned-in plus SRT/VTT |
| Delivery | Next configured queue slot; actual schedule in PUBLISHING.json |
| Optional settings | Cover, sponsorship and other unrequested declarations unset |

## Files
- [Final video]({files[0]})
- [SRT]({files[1]})
- [VTT]({files[2]})
- [Local cover]({files[3]})
- [Storyboard HTML](video/boards/storyboard.html)
- [Storyboard PNG](video/boards/storyboard.png)
- [Technical sources](SOURCES.md)
- [Export evidence](video/verification/export.json)
- [Review and limits](video/REVIEW.md)

Original illustrated schematic, no product-dimension or calibrated-speed claim. Fonts retain OFL licenses. Reused SFX provenance in video/assets/audio/sfx/assets.json; no new SFX generated. Continuous ElevenLabs source retained; derivative tempo/acoustic placement in audio_boundaries.json. Audio measured but not subjectively heard in this environment.
'''
(P/'CONTENT_PACKAGE.md').write_text(package,encoding='utf-8');(V/'post-caption.txt').write_text(caption,encoding='utf-8')
identity=dict(provider='trypost',workspace_id='01a171dd-5281-730d-af07-f2168d17add7',workspace_name="Admin's Workspace",social_account_id='01a172c9-3761-700a-9798-00febaa9fa90',service='instagram',handle='dibalikbenda.id')
payload=dict(**identity,content=caption,content_type='instagram_reel',media=dict(export_sha256=e['sha256']),meta={},requested_delivery='queue',queue='next',requested_due_at=None)
dump(V/'posting-intent.json',dict(payload=payload,payload_sha256=hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()))
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Verified export and package\nFinal90s/2700frames/1080x1920/30fps,H.264/AAC, full decode and16 decoded proof frames. SHA256{e["sha256"]}; bytes{e["bytes"]}. Package contains3 titles, exact Instagram copy,5 hashtags, keywords, local cover and SRT/VTT. Encoded cues and acoustic seams checked separately. No subjective listening claim. Next: upload, queue verification, commit.\n')
t=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));next(x for x in t['productions'] if x['slug']==P.name).update(stage='content_package',status='complete');dump(R/'TRACKER.json',t)
print(json.dumps(dict(title='Kipas: Putaran Jadi Ayunan',caption_characters=len(caption),sha256=e['sha256'])))
