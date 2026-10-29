"""Package only the verified final export, retaining scope and source limits."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;V=P/'video'
CAPTION='''“Maaf, gua sibuk.” Penjelasannya ada. Tindakan yang lo akui sudah jelas?

Acknowledgment of responsibility, atau pengakuan tanggung jawab, adalah salah satu komponen permintaan maaf. Dalam contoh di video: menyebut bahwa gua berangkat terlalu mepet dan bikin lo menunggu, lalu menawarkan perbaikan yang bisa gua jalankan.

Alasan tetap boleh dijelaskan. Coba perhatikan apakah tindakan, dampak, dan langkah berikutnya juga dibicarakan. Penerimanya boleh butuh waktu; permintaan maaf tidak mewajibkan dia langsung merasa lega.

Adegan ini ilustrasi fiktif. Riset Lewicki, Polin, & Lount (2016) menilai permintaan maaf tertulis dalam skenario kerja, bukan membuktikan kalimat tertentu pasti berhasil pada pasangan.

Sumber: An Exploration of the Structure of Effective Apologies, Negotiation and Conflict Management Research.
https://ncmr.lps.library.cmu.edu/article/id/264
Ulasan peneliti: https://news.osu.edu/the-6-elements-of-an-effective-apology-according-to-science/

#RuangDiAntara #KomunikasiPasangan #PermintaanMaaf'''
def main():
    r=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));f=P/r['file'];assert f.exists() and hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256']
    assert (P/'exports'/f'{P.name}.srt').exists()
    assert json.loads((V/'verification/sound-design-export-v2.json').read_text())['status']=='passed'
    assert json.loads((V/'verification/encoded-cuts.json').read_text())['visual_inspection']=='passed'
    assert len(CAPTION)<=2200 and CAPTION.count('#')<=5
    target=json.loads((P/'target_snapshot.json').read_text(encoding='utf-8'))
    data=dict(title='Maaf yang menyebut tindakan',alternatives=['Setelah bilang maaf, apa yang lo akui?','Alasan sudah ada. Perbaikannya apa?'],caption=CAPTION,hashtags=['#RuangDiAntara','#KomunikasiPasangan','#PermintaanMaaf'],keywords='permintaan maaf, pengakuan tanggung jawab, acknowledgment of responsibility, komunikasi pasangan, tawaran perbaikan',cover_text='Maaf, gua sibuk',cover_status='Use opening frame; no separate cover artwork requested or generated',publishing_targets=target,verified_export=r)
    (P/'delivery-copy.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(P/'publish-caption.txt').write_text(CAPTION+'\n',encoding='utf-8')
    document=f'''# Content package — Maaf yang menyebut tindakan

## Title

Recommended: **{data['title']}**

Alternatives:

- {data['alternatives'][0]}
- {data['alternatives'][1]}

## Instagram @eliansatya caption — ready to paste

{CAPTION}

## Discovery and cover

Hashtags: {' '.join(data['hashtags'])}

Editorial keywords (Instagram has no dedicated tag field in this handoff): {data['keywords']}.

Cover recommendation: **Maaf, gua sibuk** — matches actual opening frame. Separate cover artwork is not implemented; optional cover offset/feed-sharing remain unset.

## Verified delivery metadata

- production: {P.name}; board ruang-di-antara, editorial v1.3 / visual-audio v1.2.
- language: Indonesian, lo–gua. Destination: Instagram reel @eliansatya in Trypost Admin's Workspace; complete inherited target snapshot in target_snapshot.json.
- version: v1, agent-verified under delegated --automation; human_approved=false.
- [MP4]({r['file']}): {r['duration_s']:.6f}s, {r['width']}x{r['height']}, 9:16, {r['fps']}fps, {r['frames']} frames, {r['video_codec']}/{r['audio_codec']}, {r['bytes']:,} bytes.
- SHA-256: `{r['sha256']}`.
- captions: all183 spoken words burned in, plus [SRT](exports/{P.name}.srt),48 groups.
- [Decoded proof](exports/export-proof.png), [Storyboard HTML](video/boards/storyboard.html), [Storyboard PNG](video/boards/storyboard.png).
- Research/limits: [SOURCES.md](SOURCES.md); a fictional ordinary lateness scene, no guarantee of forgiveness. BGM intentionally absent. Frozen SFX provenance/licenses remain in video/assets/board/audio/sfx/.
- Full decode, all15 encoded visual/audio seams and six actual cue matches passed. Audio measured, not perceptually heard; levels {r['loudness']['input_i']} LUFS / {r['loudness']['input_tp']} dBTP.
- Authorized delivery: next configured account queue, Asia/Jakarta. Actual provider allocation and media/post identities belong to PUBLISHING.json after scheduling; no future publication monitor requested.

## Package verification

Caption compared with final script and claim boundaries; {len(CAPTION)} characters, three hashtags, within current connected MCP limits. Export hash and all linked artifacts checked. Optional sponsorship, custom date, separate cover and feed-sharing are unset because none was requested. Local source files and metadata enter the requested commit; generated media/exports follow existing Git ignores and remain locally available.
'''
    (P/'CONTENT_PACKAGE.md').write_text(document,encoding='utf-8')
    for path in [r['file'],f'exports/{P.name}.srt','exports/export-proof.png','video/boards/storyboard.html','video/boards/storyboard.png']:assert (P/path).exists(),path
    print(json.dumps(dict(package='CONTENT_PACKAGE.md',caption_characters=len(CAPTION),hashtags=3,export_sha256=r['sha256'])))
if __name__=='__main__':main()
