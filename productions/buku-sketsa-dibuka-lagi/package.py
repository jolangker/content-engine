"""Create copy and metadata only from a verified delivery export."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;V=P/'video'
r=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));f=P/r['file'];assert f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256']
caption='''Dia ingin menggambar lagi. Lo langsung kepikiran cara jualannya. Tujuan yang sedang kalian bicarakan sama nggak?

Michelangelo phenomenon membahas bagaimana pasangan dapat mendukung seseorang mendekati diri yang ingin dia kembangkan. Patokannya cita-cita orang itu sendiri.

Di contoh fiktif ini, dia ingin rutin menggambar dulu. Menawarkan waktu latihan bisa lebih sesuai daripada langsung menyusun target penjualan. Menjual karya tetap bisa jadi pilihan, kalau itu memang tujuannya.

Sebelum kasih arah, lo bisa tanya: “Bagian mana yang pengin lo coba lagi?” Lalu dengarkan jawabannya.

Dukungan yang relevan tetap tidak menjamin satu respons langsung membuat cita-cita tercapai.

Rujukan: Rusbult, Finkel & Kumashiro (2009), The Michelangelo Phenomenon. https://doi.org/10.1111/j.1467-8721.2009.01657.x

#RuangDiAntara #Relasi #DukunganPasangan #PsikologiHubungan'''
assert len(caption)<=2200 and caption.count('#')<=5
copy=dict(title='Buku sketsa dibuka lagi',caption=caption,content_type='instagram_reel',meta={},hashtags=['RuangDiAntara','Relasi','DukunganPasangan','PsikologiHubungan'])
(P/'delivery-copy.json').write_text(json.dumps(copy,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
target=json.loads((P/'target_snapshot.json').read_text(encoding='utf-8'))['accounts'][0]
doc=f'''# Content package — Buku sketsa dibuka lagi

## Title

Recommended: **Buku sketsa dibuka lagi**

Alternatives: “Lo lagi mendukung arah siapa?” / “Dia mau latihan, lo sudah mikirin jualan”

## Instagram caption — ready to use

{caption}

## Hashtags

#RuangDiAntara #Relasi #DukunganPasangan #PsikologiHubungan

## Editorial keywords

Michelangelo phenomenon, fenomena Michelangelo, dukungan pasangan, ideal self, cita-cita, latihan menggambar, komunikasi pasangan, tujuan pribadi

Instagram has no dedicated keyword field here; these are editorial discovery phrases.

## Cover

Opening emphasis already implemented: “Mau menggambar lagi”. Use the video opening by default; no separate cover artwork or offset override requested. Optional settings remain unset.

## Verified delivery metadata

- Slug: {P.name}; board ruang-di-antara, editorial v1.4 / visual and audio v1.2.
- Language: Indonesian, lo–gua. Fictional illustrative interaction, no diagnosis or outcome guarantee.
- Destination: Instagram @{target['handle']}, {target['workspace_name']}, workspace {target['workspace_id']}, account {target['social_account_id']}.
- Endpoint: Trypost queue=next; actual future scheduling result belongs in [PUBLISHING.json](PUBLISHING.json).
- Version v1: [MP4]({r['file']}), {r['duration_s']:.5f}s, 1080x1920 (9:16), 30fps, H264/{r['pixel_format']}, AAC. Bytes {r['bytes']}.
- SHA-256: {r['sha256']}
- Captions: full 187 spoken words burned in; [SRT](exports/{P.name}.srt), 49 measured groups. Word timings are estimates, scene anchors acoustic.
- [Decoded proof](exports/export-proof.png), [verification](video/verification/export.json), [research](SOURCES.md).
- Narration: ElevenLabs eleven_v4, source voice provenance in video/audio_request.json and audio_meta.json. One native-speed recording, quiet-region pauses and final normalization. Six local board material cues, no BGM. SFX credits/licenses in video/assets/board/audio/sfx/CREDITS.md; fonts/licenses local.
- Full decode, picture inspection, quiet-cut and SFX waveform checks passed. Sound measured; perceptual listening unavailable. Agent verification under delegated automation, no human approval claimed.
- No sponsorship, audience designation, account tags, feed-sharing override or separate cover chosen; not invented to fill optional fields.
'''
for path in [f,P/f'exports/{P.name}.srt',P/'exports/export-proof.png']:assert path.exists(),path
(P/'CONTENT_PACKAGE.md').write_text(doc,encoding='utf-8')
print(json.dumps(dict(caption_characters=len(caption),hashtags=caption.count('#'),export_sha256=r['sha256'])))
