"""Create upload copy tied to this exact verified export."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;V=P/'video'
CAPTION='''Setiap Jumat mampir ke bangku yang sama. Apa yang bikin kebiasaan sederhana itu terasa spesial?

Relationship rituals, atau ritual dalam hubungan, adalah kegiatan yang diulang bersama dan punya makna simbolis buat pasangan. Dua orang bisa melakukan hal yang sama, tetapi memberi arti yang berbeda: buat satu orang itu waktu khusus berdua, buat yang lain mungkin sekadar istirahat sebelum pulang.

Dalam penelitian, ritual berkaitan dengan kepuasan hubungan, terutama ketika kedua pasangan sama-sama mengakui ritualnya. Temuan ini belum membuktikan bahwa membuat satu kebiasaan pasti bikin hubungan lebih bahagia.

Lo bisa mulai dengan cerita: “Gua suka mampir di sini. Rasanya kita punya waktu sendiri.” Lalu tanya ke dia: “Buat lo, momen ini berarti apa?” Dengarkan jawabannya, termasuk kalau maknanya berbeda. Kebiasaan praktis juga boleh tetap praktis.

Bangku dan percakapan dalam video adalah ilustrasi fiktif. Pertanyaan kecil buat kalian: kebiasaan mana yang sama-sama terasa berarti?

Sumber: Garcia-Rada, Sezer & Norton (2019), Rituals and Nuptials, Journal of the Association for Consumer Research.
https://doi.org/10.1086/702761

#RuangDiAntara #RitualHubungan #KomunikasiPasangan'''
def main():
    r=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
    for name in ('sound-design-export-v2.json','preview-cleanup.json'):
        assert json.loads((V/'verification'/name).read_text())['status']=='passed'
    assert json.loads((V/'verification/encoded-cuts.json').read_text())['visual_inspection']=='passed'
    groups=json.loads((V/'caption_groups.json').read_text(encoding='utf-8'));assert sum(len(g['words']) for g in groups)==187
    assert len(CAPTION)<2200 and CAPTION.count('#')<=5
    target=json.loads((P/'target_snapshot.json').read_text(encoding='utf-8'))
    data=dict(title='Bangku di jalan pulang',alternatives=['Kebiasaan sama, maknanya sama?','Apa yang bikin momen ini spesial?'],caption=CAPTION,hashtags=['#RuangDiAntara','#RitualHubungan','#KomunikasiPasangan'],keywords='relationship rituals, ritual hubungan, makna bersama, kebiasaan pasangan, komunikasi pasangan',cover_text='Bangku yang sama',cover_status='Actual opening frame; no separate cover artwork',publishing_targets=target,verified_export=r)
    (P/'delivery-copy.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(P/'publish-caption.txt').write_text(CAPTION+'\n',encoding='utf-8')
    doc=f'''# Content package — Bangku di jalan pulang

## Titles

Recommended: **{data['title']}**

- Alternative 1: {data['alternatives'][0]}
- Alternative 2: {data['alternatives'][1]}

## Instagram @eliansatya — ready to paste

{CAPTION}

## Discovery and cover

Hashtags: {' '.join(data['hashtags'])}

Editorial keywords: {data['keywords']}. No dedicated Instagram keyword field is claimed.

Cover text: **Bangku yang sama**, present on the opening frame. No separate artwork. Unrequested cover offset, feed-sharing, sponsorship and rights declarations remain unset.

## Verified delivery metadata

- Production {P.name}; ruang-di-antara editorial v1.4 / visual-audio v1.2, implementation 2026-10-21. Indonesian lo–gua.
- Instagram Reel @eliansatya, Trypost Admin's Workspace. Full inherited target set: [target snapshot](target_snapshot.json).
- Version v1, agent-verified under --automation; human_approved=false.
- [MP4]({r['file']}): {r['duration_s']:.6f}s, 1080x1920 (9:16), 30fps, {r['frames']} frames, H264/AAC, {r['bytes']:,} bytes.
- SHA-256 `{r['sha256']}`.
- All 187 spoken words burned in across {len(groups)} groups. [Sidecar SRT](exports/{P.name}.srt).
- [Decoded proof](exports/export-proof.png), [Storyboard HTML](video/boards/storyboard.html), [Storyboard PNG](video/boards/storyboard.png).
- Evidence: [SOURCES.md](SOURCES.md). Repetition and mutually recognized symbolic meaning; association is not causation. Fictional park scene and suggested dialogue, no diagnosis or tested treatment claim.
- One native-speed ElevenLabs eleven_v4 recording; sparse frozen board sounds, no music. Licenses/provenance: video/assets/board/audio/sfx/. All fifteen encoded acoustic seams and six SFX waveform matches passed; forty-five encoded cut frames inspected. Full decode passed. Audio {r['loudness']['input_i']} LUFS / {r['loudness']['input_tp']} dBTP. Perceptual listening unavailable; measured evidence does not establish perceptual quality.
- Queue=next authorized; actual returned schedule/identities in [receipt](PUBLISHING.json) once created. No future publication monitoring.

## Verification

Copy matches the delivered script and claim boundaries; {len(CAPTION)} characters / three hashtags meet live limits. All delivery paths exist and export hash matches. Pipeline preview released after export verification. Generated media remain locally available under existing Git ignores; sources, captions, alignment, provenance and receipts are versioned.
'''
    (P/'CONTENT_PACKAGE.md').write_text(doc,encoding='utf-8')
    for name in (r['file'],f'exports/{P.name}.srt','exports/export-proof.png','video/boards/storyboard.html','video/boards/storyboard.png'):assert (P/name).exists()
    print(json.dumps(dict(package='CONTENT_PACKAGE.md',caption_characters=len(CAPTION),export_sha256=r['sha256'])))
if __name__=='__main__':main()
