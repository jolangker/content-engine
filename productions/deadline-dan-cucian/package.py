"""Create destination copy only after actual export verification."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;V=P/'video'
CAPTION='''Deadline dia besok. Kenapa yang kalian ributin justru cucian malam ini?

Dyadic coping, atau mengatasi stres bersama pasangan, membahas komunikasi dan respons saat menghadapi tekanan. Salah satu bentuk bantuannya adalah mengambil sebagian tugas, dengan tetap membicarakan kebutuhan dan kapasitas masing-masing.

Dalam adegan fiktif ini, permintaannya konkret: “Malam ini bisa bantu jemur? Gua yang lipat besok.” Pasangannya juga bisa menyebut batas: “Gua bisa jemur separuh. Sisanya kita atur lagi.”

Deadline tetap ada. Yang disepakati adalah pembagian satu tugas rumah. Contoh ini bukan jaminan konflik selesai atau semua tanggung jawab harus diambil alih.

Kalau sedang berat, bagian mana yang ingin lo bicarakan dan tangani bareng?

Sumber: Falconier & Kuhn (2019), tinjauan konsep dyadic coping; Pagani dkk. (2019), studi diary komunikasi stres. Studi diary bersifat korelasional, bukan bukti sebab-akibat.
https://pmc.ncbi.nlm.nih.gov/articles/PMC6443825/
https://pmc.ncbi.nlm.nih.gov/articles/PMC6400868/

#RuangDiAntara #DyadicCoping #KomunikasiPasangan'''
def main():
 r=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));f=P/r['file'];assert hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256']
 assert json.loads((V/'verification/sound-design-export-v2.json').read_text())['status']=='passed'
 assert json.loads((V/'verification/encoded-cuts.json').read_text())['visual_inspection']=='passed'
 assert json.loads((V/'verification/preview-cleanup.json').read_text())['status']=='passed'
 groups=json.loads((V/'caption_groups.json').read_text(encoding='utf-8'));assert sum(len(g['words']) for g in groups)==186
 assert len(CAPTION)<2200 and CAPTION.count('#')<=5
 target=json.loads((P/'target_snapshot.json').read_text(encoding='utf-8'))
 data=dict(title='Deadline dan cucian',alternatives=['Deadline lo, bantuan gua apa?','Bagian mana yang bisa kita tangani bareng?'],caption=CAPTION,hashtags=['#RuangDiAntara','#DyadicCoping','#KomunikasiPasangan'],keywords='dyadic coping, mengatasi stres bersama pasangan, komunikasi stres, bantuan pasangan, pembagian tugas rumah',cover_text='Deadline. Cucian.',cover_status='Present on actual opening frame; no separate artwork',publishing_targets=target,verified_export=r)
 (P/'delivery-copy.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(P/'publish-caption.txt').write_text(CAPTION+'\n',encoding='utf-8')
 doc=f'''# Content package — Deadline dan cucian

## Titles

Recommended: **{data['title']}**

- Alternative 1: {data['alternatives'][0]}
- Alternative 2: {data['alternatives'][1]}

## Instagram @eliansatya caption — ready to paste

{CAPTION}

## Discovery and cover

Hashtags: {' '.join(data['hashtags'])}

Editorial keywords (Instagram has no dedicated tag field in this handoff): {data['keywords']}.

Cover text: **Deadline. Cucian.**, present in the actual opening. No separate cover generated. Optional cover offset, feed sharing, sponsorship, custom date and unrequested declarations remain unset.

## Verified delivery metadata

- Production: {P.name}; board ruang-di-antara editorial v1.3 / visual-audio v1.2, implementation 2026-10-21.
- Indonesian lo–gua; Instagram Reel @eliansatya, Trypost Admin's Workspace. Full board-inherited target snapshot: target_snapshot.json.
- Version v1; agent-verified under --automation; human_approved=false.
- [MP4]({r['file']}): {r['duration_s']:.6f}s, {r['width']}x{r['height']} (9:16), {r['fps']}fps, {r['frames']} frames, {r['video_codec']}/{r['audio_codec']}, {r['bytes']:,} bytes.
- SHA-256: `{r['sha256']}`.
- All 186 spoken words burned in, {len(groups)} groups; [SRT](exports/{P.name}.srt).
- [Decoded export proof](exports/export-proof.png), [Storyboard HTML](video/boards/storyboard.html), [Storyboard PNG](video/boards/storyboard.png).
- Research and boundaries: [SOURCES.md](SOURCES.md). Fictional work/laundry dialogue; no diagnosis, treatment or guaranteed outcome. BGM intentionally absent. Frozen material sound provenance/licenses in video/assets/board/audio/sfx/.
- Full decode, fifteen encoded acoustic seams, forty-five visual seam frames and six actual SFX matches passed. Audio: {r['loudness']['input_i']} LUFS, {r['loudness']['input_tp']} dBTP. Perceptual listening unavailable.
- Endpoint authorized: each inherited account's next configured queue slot, Asia/Jakarta. Actual scheduled time and provider IDs are retained in PUBLISHING.json after successful readback. Future publication monitoring is outside this request.

## Verification

Caption checked against script and sources: {len(CAPTION)} characters and three hashtags, within live MCP account limits. All linked artifacts exist and export hash matches. Preview released after export verification. Generated media and exports remain local under existing Git ignores; the requested commit contains source, alignment, provenance and receipts.
'''
 (P/'CONTENT_PACKAGE.md').write_text(doc,encoding='utf-8')
 for name in (r['file'],f'exports/{P.name}.srt','exports/export-proof.png','video/boards/storyboard.html','video/boards/storyboard.png'):assert (P/name).exists(),name
 print(json.dumps(dict(package='CONTENT_PACKAGE.md',caption_characters=len(CAPTION),words=186,export_sha256=r['sha256'])))
if __name__=='__main__':main()
