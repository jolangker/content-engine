from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent;R=B.parent.parent;V=B/'video'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
e=read(V/'verification/export.json');assert e['status']=='passed'
assert read(V/'verification/sound-design-export.json')['status']=='passed'
assert read(V/'verification/preview-cleanup.json')['status']=='passed'
for name in ['jeda-punya-waktu-kembali-v1.mp4','jeda-punya-waktu-kembali.srt','proof-sheet.jpg']:assert (B/'exports'/name).is_file()
caption='''“Nanti kita bahas.” Nanti itu kapan?

Saat perlu jeda, coba sampaikan kondisi lo dan sepakati waktu untuk kembali.

“Gua mulai susah dengar. Gua mau tenang dulu. Kita lanjut jam delapan, ya?”

Jamnya cuma contoh. Yang perlu dibicarakan bersama: kapan kembali, siapa yang mulai, dan bagaimana mengabari kalau belum siap. Lalu lihat tindak lanjutnya.

Adegan dan dialog merupakan ilustrasi percakapan sehari-hari.

Rujukan: The Family Institute, bagian 4 — https://www.family-institute.org/behavioral-health-resources/trouble-communicating-your-partner-top-five-tips-couples-therapist
Gottman Institute — https://www.gottman.com/blog/the-four-horsemen-stonewalling/

#RuangDiAntara #Komunikasi #Relasi #Jeda'''
assert len(caption)<=2200 and caption.count('#')<=5
(B/'publish-caption.txt').write_text(caption,encoding='utf-8')
text=f'''# Content package — Jeda punya waktu kembali

## Title
Recommended: **Jeda punya waktu kembali**

Alternatives:
- Kalau bilang nanti, kapan lanjut?
- Minta jeda, sepakati kembali

## Instagram @eliansatya — ready-to-paste caption

{caption}

## Hashtags
`#RuangDiAntara #Komunikasi #Relasi #Jeda`

## Editorial keywords
jeda saat konflik, waktu kembali, komunikasi pasangan, kesepakatan, tindak lanjut, obrolan tertunda

## Cover text
“Nanti itu kapan?” — matches opening emphasis. Unimplemented cover-art suggestion; no custom cover upload requested. Default service selection remains unset.

## Delivery metadata
- Production: jeda-punya-waktu-kembali / board ruang-di-antara v1.2, 2026-10-21 implementation.
- Account: Instagram @eliansatya; Trypost Admin's Workspace / 01a171dd-5281-730d-af07-f2168d17add7; account 01a172ed-9899-7177-ab1e-627c835e4a57.
- Requested delivery: draft, no schedule or publication time.
- Language: Indonesian, lo–gua.
- Version: v1, agent-verified under delegated automation; no human approval claimed.
- Actual duration: {e['duration_s']:.3f}s; {e['width']}×{e['height']}, 9:16, 30fps; MP4 / {e['video_codec']} / {e['audio_codec']}.
- Captions: full spoken words, burned in and [SRT sidecar](exports/jeda-punya-waktu-kembali.srt), 41 phrases / 194 words. Native speech speed, six seconds of editorial pauses; 1.2s quiet visual tail.
- [Video](exports/jeda-punya-waktu-kembali-v1.mp4) — {e['bytes']} bytes; SHA-256 `{e['sha256']}`.
- [Final proof sheet](exports/proof-sheet.jpg), [storyboard PNG](video/boards/storyboard.png), [storyboard HTML](video/boards/storyboard.html).
- Optional feed-sharing, service cover offset, mentions and other platform settings unset; no sponsorship or rights declaration inferred.

## Editorial and rights notes
The clock's 20:00 is a fictional appointment, not a prescribed break length. Return-plan advice is attributed to institutional practice guidance; no clinical diagnosis or guaranteed resolution. Claim map: [SOURCES.md](SOURCES.md). The observational study is research background, not causal evidence for this exact script.

Illustration and animation authored locally. Newsreader and DM Sans font licenses retained under video/assets/board/. Six reused material SFX derive from the board's licensed Pixabay library; provenance and treatment hashes in video/sound_design.json and video/assets/board/audio/sfx/CREDITS.md. BGM intentionally absent.

## Verification and limits
Full decode, frame/duration/codec checks, matching preview/export proof frames, caption coverage, loudness and exported cue presence verified; evidence in [VERIFICATION.md](VERIFICATION.md) and video/verification/. Full Studio progression verified to the end. Perceptual listening unavailable; no assertion of listened mix quality or human audio approval. Temporary preview must be verified stopped before delivery work.

## External delivery
Pending creation and read-back verification of the requested Trypost draft. The receipt will be PUBLISHING.json. This package does not claim a live Instagram post.
'''
(B/'CONTENT_PACKAGE.md').write_text(text,encoding='utf-8')
t=read(R/'TRACKER.json');next(x for x in t['productions'] if x['slug']==B.name).update(stage='content_package',status='complete');(R/'TRACKER.json').write_text(json.dumps(t,indent=2)+'\n',encoding='utf-8')
with (B/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Content package complete\nVerified export v1: {e["duration_s"]:.3f}s, 1080×1920/30fps, {e["bytes"]} bytes, SHA-256 {e["sha256"]}. Package and exact caption prepared for inherited Instagram @eliansatya. Delivery remains draft; continue through external upload and read-back verification.\n')
print(json.dumps(dict(caption_characters=len(caption),hashtags=caption.count('#'),duration=e['duration_s'],sha256=e['sha256'])))
