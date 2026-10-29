"""Package the verified export and its actual measured metadata."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;V=P/'video'
CAPTION='''Dua cangkir. Satu malam. Bagian mana yang masih terasa hangat waktu lo ingat lagi?

Relational savoring, atau menikmati kembali momen kedekatan dalam hubungan, memberi perhatian pada satu pengalaman positif ketika lo merasa terhubung dengan seseorang. Dalam contoh fiktif di video, momen itu sesederhana ditemani bikin teh setelah pulang capek.

Kalau ingin mencoba, ingat satu kejadian yang terasa dekat: tempatnya, apa yang terjadi, dan bagian yang berarti buat lo. Kalau mau dibagikan, ceritakan sebagai pengalaman lo sendiri, tanpa menuntut perasaan yang sama.

Satu kenangan hangat tidak menyimpulkan kualitas seluruh hubungan atau menyelesaikan masalah yang masih ada. Video ini penjelasan singkat dengan ilustrasi, bukan pelaksanaan protokol terapi atau janji hasil tertentu.

Sumber konsep dan proses refleksi: Borelli dan kolega (2024), Culturally adapting relational savoring: A therapeutic approach to improve relationship quality.
https://pmc.ncbi.nlm.nih.gov/articles/PMC11245364/

#RuangDiAntara #RelationalSavoring #RelasiSehariHari'''
def main():
    r=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));f=P/r['file'];assert f.exists() and hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256']
    assert json.loads((V/'verification/sound-design-export-v2.json').read_text())['status']=='passed'
    assert json.loads((V/'verification/encoded-cuts.json').read_text())['visual_inspection']=='passed'
    groups=json.loads((V/'caption_groups.json').read_text(encoding='utf-8'));words=sum(len(g['words']) for g in groups)
    assert words==204 and len(CAPTION)<2200 and CAPTION.count('#')<=5
    target=json.loads((P/'target_snapshot.json').read_text(encoding='utf-8'))
    data=dict(title='Momen kecil, dinikmati lagi',alternatives=['Dua cangkir, satu kenangan dekat','Apa yang masih terasa hangat?'],caption=CAPTION,hashtags=['#RuangDiAntara','#RelationalSavoring','#RelasiSehariHari'],keywords='relational savoring, menikmati kenangan, momen kedekatan, hubungan pasangan, pengalaman positif',cover_text='Momen kecil',cover_status='Actual opening frame; no separate cover generated',publishing_targets=target,verified_export=r)
    (P/'delivery-copy.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(P/'publish-caption.txt').write_text(CAPTION+'\n',encoding='utf-8')
    text=f'''# Content package — Momen kecil, dinikmati lagi

## Titles

Recommended: **{data['title']}**

- Alternative 1: {data['alternatives'][0]}
- Alternative 2: {data['alternatives'][1]}

## Instagram @eliansatya caption — ready to paste

{CAPTION}

## Discovery and cover

Hashtags: {' '.join(data['hashtags'])}

Editorial keywords (no dedicated Instagram tag field in this handoff): {data['keywords']}.

Cover text: **Momen kecil**, present on the actual opening frame. A separate cover is not implemented. Optional cover offset, feed-sharing and other unsupported/unrequested settings remain unset.

## Verified delivery metadata

- Production: {P.name}; board ruang-di-antara editorial v1.3 / visual-audio v1.2, implementation 2026-10-21.
- Language: Indonesian, lo–gua; destination Instagram Reel @eliansatya, Trypost Admin's Workspace. Full inherited account snapshot: target_snapshot.json.
- Version v1; agent-verified under --automation; human_approved=false.
- [MP4]({r['file']}): {r['duration_s']:.6f}s, {r['width']}x{r['height']}, 9:16, {r['fps']}fps, {r['frames']} frames, {r['video_codec']}/{r['audio_codec']}, {r['bytes']:,} bytes.
- SHA-256: `{r['sha256']}`.
- Captions: all {words} spoken words burned in; [SRT](exports/{P.name}.srt), {len(groups)} groups.
- [Decoded export proof](exports/export-proof.png), [Storyboard HTML](video/boards/storyboard.html), [Storyboard PNG](video/boards/storyboard.png).
- Sources and limits: [SOURCES.md](SOURCES.md). Fictional tea scene and subjective experience; no treatment/effectiveness claim. BGM intentionally absent; frozen material SFX credits and license records are local under video/assets/board/audio/sfx/.
- Full decode, all fifteen encoded visual/audio seams and six actual cue matches passed. Audio measured at {r['loudness']['input_i']} LUFS / {r['loudness']['input_tp']} dBTP; perceptual listening unavailable.
- Authorized endpoint: next account queue slot, Asia/Jakarta. Actual provider schedule and media/post IDs: PUBLISHING.json after scheduling. No later publication monitoring requested.

## Package verification

Caption checked against the final script and claim boundaries: {len(CAPTION)} characters and three hashtags, within the live MCP account limits. Export hash and all linked files checked. Sponsorship, custom date and separate cover are unset. Generated media/exports follow existing Git ignores and remain locally available; source and metadata belong in the requested commit.
'''
    (P/'CONTENT_PACKAGE.md').write_text(text,encoding='utf-8')
    for path in [r['file'],f'exports/{P.name}.srt','exports/export-proof.png','video/boards/storyboard.html','video/boards/storyboard.png']:assert (P/path).exists(),path
    print(json.dumps(dict(package='CONTENT_PACKAGE.md',caption_characters=len(CAPTION),words=words,export_sha256=r['sha256'])))
if __name__=='__main__':main()
