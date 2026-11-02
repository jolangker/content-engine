"""Prepare destination copy tied to the verified local export."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;V=P/'video'
CAPTION='''“Sebentar,” katanya sambil lihat HP. Kenapa cerita lo jadi berhenti di meja makan?

Partner phubbing membahas perhatian ke ponsel yang menyela interaksi bersama pasangan. Dalam adegan fiktif ini, yang bisa diamati adalah cerita terputus dan satu bagian harus diulang. Perasaan kurang mendapat ruang bisa dibicarakan, sementara niat pasangan tetap perlu ditanyakan.

Salah satu kalimat yang bisa dicoba: “Gua pengin selesai cerita. Bisa taruh HP dulu selama kita makan?” Kalau ada pesan mendesak, sebutkan kebutuhannya dan bicarakan kapan perhatian bisa kembali. Lalu lanjutkan cerita dari bagian yang tertinggal.

Contoh percakapan ini merupakan ilustrasi, tanpa diagnosis atau jaminan hasil. Kalian bisa menyepakati waktu berbicara dan kebutuhan jeda masing-masing.

Saat makan berdua, kapan kalian tersedia buat saling mendengar?

Sumber konsep: Roberts & David, ringkasan penelitian oleh penulis asli, Baylor University (2017), merujuk penelitian 2016.
https://kellercenter.hankamer.baylor.edu/news/story/2017/partner-phubbing-how-cell-phones-impact-romantic-partnerships

#RuangDiAntara #PartnerPhubbing #KomunikasiPasangan'''
def main():
    r=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
    assert json.loads((V/'verification/sound-design-export-v2.json').read_text())['status']=='passed'
    assert json.loads((V/'verification/encoded-cuts.json').read_text())['visual_inspection']=='passed'
    assert json.loads((V/'verification/preview-cleanup.json').read_text())['status']=='passed'
    groups=json.loads((V/'caption_groups.json').read_text(encoding='utf-8'));assert sum(len(g['words']) for g in groups)==190
    assert len(CAPTION)<2200 and CAPTION.count('#')<=5
    target=json.loads((P/'target_snapshot.json').read_text(encoding='utf-8'))
    data=dict(title='Sebentar di meja makan',alternatives=['Cerita lo berhenti di notifikasi mana?','Kapan kita tersedia buat mendengar?'],caption=CAPTION,hashtags=['#RuangDiAntara','#PartnerPhubbing','#KomunikasiPasangan'],keywords='partner phubbing, perhatian pasangan, ponsel saat makan, komunikasi pasangan, cerita terputus',cover_text='Sebentar?',cover_status='Present on actual opening frame; no separate artwork',publishing_targets=target,verified_export=r)
    (P/'delivery-copy.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(P/'publish-caption.txt').write_text(CAPTION+'\n',encoding='utf-8')
    doc=f'''# Content package — Sebentar di meja makan

## Titles

Recommended: **{data['title']}**

- Alternative 1: {data['alternatives'][0]}
- Alternative 2: {data['alternatives'][1]}

## Instagram @eliansatya caption — ready to paste

{CAPTION}

## Discovery and cover

Hashtags: {' '.join(data['hashtags'])}

Editorial keywords (no separate Instagram tag field in this handoff): {data['keywords']}.

Cover text: **Sebentar?**, present in the actual opening. No separate cover generated. Unrequested cover offset, feed-sharing, sponsorship and rights declarations remain unset.

## Verified delivery metadata

- Production: {P.name}; board ruang-di-antara editorial v1.3 / visual-audio v1.2; implementation 2026-10-21.
- Indonesian lo–gua; Instagram Reel @eliansatya in Trypost Admin's Workspace. Full inherited target snapshot: target_snapshot.json.
- Version v1; agent-verified under --automation; human_approved=false.
- [MP4]({r['file']}): {r['duration_s']:.6f}s, {r['width']}x{r['height']} (9:16), {r['fps']}fps, {r['frames']} frames, {r['video_codec']}/{r['audio_codec']}, {r['bytes']:,} bytes.
- SHA-256: `{r['sha256']}`.
- Full burned-in captions: all 190 spoken words in {len(groups)} groups. [SRT](exports/{P.name}.srt).
- [Decoded proof](exports/export-proof.png), [Storyboard HTML](video/boards/storyboard.html), [Storyboard PNG](video/boards/storyboard.png).
- Evidence and limitations: [SOURCES.md](SOURCES.md). Fictional dinner dialogue; established behavioral term, no diagnosis, causal relationship result or guaranteed outcome. Narration and sparse frozen material sounds; no BGM. Provenance/licenses: video/assets/board/audio/sfx/.
- Full decode, fifteen encoded acoustic seams, forty-five visual seam frames and six actual SFX matches passed. Audio: {r['loudness']['input_i']} LUFS, {r['loudness']['input_tp']} dBTP. Perceptual listening unavailable; measured evidence does not establish perceptual quality.
- Delivery authorized: next configured queue slot, Asia/Jakarta. Actual scheduled time and IDs belong in PUBLISHING.json after readback. No future publication monitoring requested.

## Package verification

Copy matches final script and claim boundaries; {len(CAPTION)} characters / three hashtags meet live account limits. All linked artifacts exist and MP4 hash matches. Pipeline preview released after export verification. Existing Git ignores retain generated media locally; the commit includes sources, alignment, provenance and receipts.
'''
    (P/'CONTENT_PACKAGE.md').write_text(doc,encoding='utf-8')
    for name in (r['file'],f'exports/{P.name}.srt','exports/export-proof.png','video/boards/storyboard.html','video/boards/storyboard.png'):assert (P/name).exists(),name
    print(json.dumps(dict(package='CONTENT_PACKAGE.md',caption_characters=len(CAPTION),words=190,export_sha256=r['sha256'])))
if __name__=='__main__':main()
