"""Package the exact verified export and freeze its queue intent."""
from pathlib import Path
import hashlib,json,re
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2]
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
e=json.loads((V/'verification/export.json').read_text(encoding='utf-8'))
assert e['status']=='passed' and hashlib.sha256((P/e['local_file']).read_bytes()).hexdigest()==e['sha256']
caption='''Sekali klik, isi pensil maju. Kenapa saat tombol kembali, isinya tidak ikut mundur?

Pada mekanisme rahang dan cincin ini, penjepit membawa isi ke depan. Saat cincin mencapai pembatas, penjepit maju sedikit lagi hingga terbuka. Penahan ringan di dekat ujung menjaga posisi isi selama penjepit kembali, lalu cincin merapatkan rahangnya lagi.

Ilustrasi potongan dan jarak gerak diperbesar agar perpindahan genggaman terlihat. Desain pensil lain bisa berbeda. Bunyi mekanisme bersifat ilustratif.

Rujukan teknis:
https://patents.google.com/patent/US4106874A/en
https://data.epo.org/publication-server/rest/v1.1/patents/EP0168122NWA1/document.html

#DiBalikBenda #PensilMekanik #CaraKerja #Mekanisme'''
assert len(caption)<=2200 and len(re.findall(r'#\w+',caption))<=5
files=[e['local_file']]+[f'exports/{P.name}-v1{x}' for x in ['.srt','.vtt','-cover.png']]
assert all((P/f).is_file() and (P/f).stat().st_size for f in files)
package=f'''# Content package — Pensil: Jepit dan Maju

## Titles
Recommended: **Tombol Kembali, Kenapa Isi Pensil Tidak Ikut Mundur?**

Alternatives:
- Penjepit Kecil di Balik Satu Klik Pensil
- Bagaimana Isi Pensil Maju Sedikit demi Sedikit?

## Ready-to-post Instagram caption

{caption}

## Hashtags
#DiBalikBenda #PensilMekanik #CaraKerja #Mekanisme

## Editorial keywords
cara kerja pensil mekanik, penjepit isi pensil, chuck, cincin penjepit, penahan isi pensil, pegas, mekanisme klik

These are editorial discovery terms, not a dedicated Instagram upload field.

## Cover
Implemented local cover uses the opening-frame title **Maju, kok tidak mundur?**, decoded from finalMP4 at2.0s. Optional remote cover settings remain unset; local PNG is supplied separately.

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
| Delivery | Next configured queue slot; observed schedule in PUBLISHING.json |
| Optional settings | Cover, sponsorship and unrequested declarations unset |

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

Original illustrated schematic, no product-dimension or calibrated-speed claim. Sources describe specific embodiments and the feed subsystem is bounded in SOURCES.md. Fonts retain OFL licenses. Existing SFX provenance in video/assets/audio/sfx/assets.json; no new SFX generation. One continuous ElevenLabs source retained; derivative pace/acoustic placement in audio_boundaries.json. Audio measured but not subjectively heard in this environment.
'''
(P/'CONTENT_PACKAGE.md').write_text(package,encoding='utf-8');(V/'post-caption.txt').write_text(caption,encoding='utf-8')
identity=dict(provider='trypost',workspace_id='01a171dd-5281-730d-af07-f2168d17add7',workspace_name="Admin's Workspace",social_account_id='01a172c9-3761-700a-9798-00febaa9fa90',service='instagram',handle='dibalikbenda.id')
payload=dict(**identity,content=caption,content_type='instagram_reel',media=dict(export_sha256=e['sha256']),meta={},requested_delivery='queue',queue='next',requested_due_at=None)
dump(V/'posting-intent.json',dict(payload=payload,payload_sha256=hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()))
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Verified export and package\nFinal90s/2700frames/1080x1920/30fps,H.264/AAC, full decode and16decoded proof frames. SHA256{e["sha256"]}; bytes{e["bytes"]}. Package contains3titles, exact Instagram copy,4hashtags, keywords, local cover and SRT/VTT. Encoded cues and acoustic seams checked separately. No subjective listening claim. Next: upload, queue verification, commit.\n')
t=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));next(x for x in t['productions'] if x['slug']==P.name).update(stage='content_package',status='complete');dump(R/'TRACKER.json',t)
print(json.dumps(dict(title='Pensil: Jepit dan Maju',caption_characters=len(caption),sha256=e['sha256'])))
