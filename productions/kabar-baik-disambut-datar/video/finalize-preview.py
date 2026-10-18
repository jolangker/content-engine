"""Record the reviewed artifacts and technical evidence for the preview gate."""
from pathlib import Path
import json
import re
import subprocess
import wave
import struct
from PIL import Image, ImageChops

ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[2]
FROZEN=ROOT/'boards/approved-storyboard-v1'

def read_json(path):
    b=path.read_bytes()
    s=b.decode('utf16' if b[:2] in (b'\xff\xfe',b'\xfe\xff') else 'utf-8-sig')
    return json.loads(s[s.index('{'):] if s.lstrip().startswith('>') else s)

def dump(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

check=read_json(ROOT/'boards/check-preview-v1.json')
assert check['ok'] and not check['browserSkipped'], 'Finish the full HyperFrames check first.'
assert check['motion']['enabled'] and check['motion']['ok']
dump(ROOT/'boards/check-preview-v1.json',check)
frames=read_json(ROOT/'boards/preview-frames.json')
captions=read_json(ROOT/'captions.json')
audio=read_json(ROOT/'audio_meta.json')
words=audio['voices'][0]['words']
approved=' '.join((ROOT/'assets/approved-narration.txt').read_text(encoding='utf8').split())
assert approved==' '.join(w['text'] for w in words)
assert approved==' '.join(' '.join(c['lines']) for c in captions)
assert all(len(c['lines'])<=2 for c in captions)
assert all(a['end']<=b['start'] for a,b in zip(captions,captions[1:]))
assert all(w['start']<w['end'] for w in words)
assert all(a['end']<=b['start'] for a,b in zip(words,words[1:]))
assert all(a['end']==b['start'] for a,b in zip(frames,frames[1:]))

# Prove pixel movement inside each illustration, excluding headlines and captions.
proof=[]
for p in (ROOT/'boards/motion-proof-v1').glob('frame-*-at-*s.png'):
    t=float(re.search(r'-at-([0-9.]+)s',p.name)[1])
    proof.append((t,p))
proof.sort()
pose_checks=[]
for f in frames:
    samples=[(t,p) for t,p in proof if f['start']<=t<f['end']]
    assert len(samples)>=2, f"Missing pose samples for {f['id']}"
    changes=[]
    for (t1,p1),(t2,p2) in zip(samples,samples[1:]):
        a=Image.open(p1).convert('RGB').crop((50,430,1030,1460))
        b=Image.open(p2).convert('RGB').crop((50,430,1030,1460))
        diff=ImageChops.difference(a,b)
        changed=sum(max(px)>12 for px in diff.get_flattened_data())
        changes.append({'from':t1,'to':t2,'changed_pixels':changed})
    assert any(c['changed_pixels']>100 for c in changes), f"No illustration movement in {f['id']}"
    pose_checks.append({'frame':f['id'],'ok':True,'comparisons':changes})

voice=ROOT/audio['voices'][0]['path']
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(voice),'-f','null','-'],check=True)
with wave.open(str(voice),'rb') as w:
    assert w.getsampwidth()==2 and w.getnchannels()==1
    samples=struct.unpack('<'+'h'*w.getnframes(),w.readframes(w.getnframes()))
    peak=max(abs(s) for s in samples)
    clipped=sum(abs(s)>=32767 for s in samples)
assert clipped==0 and peak>0

script=(FROZEN/'SCRIPT.md').read_text(encoding='utf8')
script=re.sub(r'\*\*Status:\*\*.*','**Status:** narasi v1 approved; storyboard v1 approved; preview v1 awaiting_review.',script,count=1)
script=re.sub(r'\*\*Voice:\*\*.*','**Voice:** George — ElevenLabs, JBFqnCBsd6RMkjVDRZzb, eleven_multilingual_v2. Default workspace.',script,count=1)
script=re.sub(r'\*\*Voice settings:\*\*.*','**Voice settings:** satu full-script request speed 1.0, MP3 44100/128. Preview WAV atempo=0.85, native word alignment diskalakan 1/0.85. Voice 88.385283s + hold akhir 1.5s = 89.885s.',script,count=1)
for f in frames:
    pat=rf'(## Line {f["number"]} .*?\n\n)\*\*Time:\*\*[^\n]+'
    script=re.sub(pat,lambda m:m[1]+f'**Time:** {f["start"]:.4f}–{f["end"]:.4f}s; words {f["word_ids"][0]}–{f["word_ids"][-1]}',script,count=1,flags=re.S)
(ROOT/'SCRIPT.md').write_text(script,encoding='utf8')

story=(FROZEN/'STORYBOARD.md').read_text(encoding='utf8')
story=story.replace('duration: 90s','duration: 89.885s',1)
story=story.replace('layout_review: awaiting_review','layout_review: approved')
a=story.index('Naskah v1,');b=story.index('## Video direction')
story=story[:a]+'''Naskah v1 (175 kata) dan storyboard visual v1 (14 shot) diterima pengguna pada 18 Oktober 2026 melalui “cocok” di masing-masing checkpoint. Layout yang diterima dibekukan di boards/approved-storyboard-v1/. Preview v1 menambahkan animasi, satu track narasi kontinu, dan subtitle lengkap. Durasi terukur 89.885 detik, termasuk hold penutup 1.5 detik. **Final preview awaiting_review**; belum disetujui untuk export.

'''+story[b:]
story=story.replace('subtitle contoh pada satu track tersendiri','subtitle lengkap pada satu track tersendiri')
a=story.index('Rencana gerak berikut');b=story.index('## Frame 1')
story=story[:a]+'''Gerak v1 mempertahankan pose dan palet: masuk/menoleh, tangan yang tertahan, HP yang diletakkan, dan gestur untuk mendengar. Semua perpindahan antarscene berupa cut. Satu narasi utuh menjadi acuan. Alignment native diskalakan terhadap tempo preview; time-stretch dapat menimbulkan selisih lokal kecil. Rincian: [MOTION.md](MOTION.md), audio_meta.json, dan captions.json.

'''+story[b:]
for f in frames:
    n=f['number']
    story=re.sub(rf'## Frame {n} — [^\n]+',f'## Frame {n} — {f["title"]} ({f["start"]:.3f}–{f["end"]:.3f}s)',story,count=1)
    pat=rf'(## Frame {n} — [\s\S]*?)(?=\n## Frame |\Z)'
    def fix(m):
        part=m[1]
        part=re.sub(r'- duration: [^\n]+',f'- duration: {f["duration"]}s',part,count=1)
        part=re.sub(r'- poster: [^\n]+',f'- poster: {f["duration"]/2:.4f}s local; {f["poster"]}s root',part,count=1)
        part=part.replace('- status: built','- status: animated')
        part=part.replace('- layout_review: approved',f'- layout_review: approved\n- words: {f["word_ids"][0]}–{f["word_ids"][-1]}\n- motion: '+' → '.join(f['motion_phases']))
        return part
    story=re.sub(pat,fix,story,count=1)
(ROOT/'STORYBOARD.md').write_text(story,encoding='utf8')

brief=(ROOT/'BRIEF.md').read_text(encoding='utf8').replace('?cocok?','“cocok”')
(ROOT/'BRIEF.md').write_text(brief,encoding='utf8')
report={
    'version':'preview-v1','stage':'preview','status':'awaiting_review',
    'duration_s':audio['composition_duration_s'],'voice_duration_s':audio['total_duration_s'],
    'shots':14,'words':len(words),'caption_groups':len(captions),
    'source_text_unchanged':True,'caption_text_complete':True,'caption_max_lines':2,
    'word_times_monotonic':True,'scene_cuts_contiguous':True,
    'voice_full_decode_passed':True,'clipped_samples':clipped,'pcm_peak':peak,
    'motion_pose_checks':pose_checks,'hyperframes_check':check['saved'],
    'browser':'HyperFrames Chromium, hardware Intel Iris Xe / ANGLE D3D11',
    'limitations':['CUA browser inventory was empty; Studio UI playback not inspected through CUA.',
        'Audio decode, duration, native source alignment and clipping checked; subjective listening is part of user preview review.',
        'Native word times scaled for atempo=0.85; small local time-stretch differences are possible.',
        'Motion liveness applies to the active root; per-shot movement additionally proved by illustration pixel comparisons.'],
    'rendered_mp4':False
}
dump(ROOT/'boards/verification-preview-v1.json',report)
(ROOT/'VERIFICATION.md').write_text('''# Verifikasi preview v1 — 18 Oktober 2026

## Hasil

- 14 shot animasi, 1080×1920, 89.885 detik; suara kontinu 88.385283 detik dan hold akhir 1.5 detik.
- Naskah 175 kata dan seluruh subtitle cocok persis dengan narasi yang diterima. 45 frasa, maksimal dua baris; waktu naik berurutan, tidak ada dua frasa terlihat bersamaan atau gap antarshot.
- Full `npm run check` lolos: browser benar-benar berjalan, lint/runtime/layout/motion/contrast tanpa error atau warning. Lihat [check-preview-v1.json](boards/check-preview-v1.json).
- Penanda motion: root harus terus mengalami perubahan; semua host tampil pada waktunya dan tetap dalam frame. Audit ini memakai selector host karena ID dalam sub-komposisi mendapat namespace saat bundling. Assertion liveness per host sepanjang 90 detik sengaja tidak dipakai: host sebelum/sesudah durasinya memang tidak aktif.
- Gerak tiap ilustrasi dibuktikan terpisah dengan pasangan snapshot di wilayah y=430–1460, tanpa headline/subtitle. Semua 14 shot menunjukkan perubahan piksel. Bukti rinci di [verification-preview-v1.json](boards/verification-preview-v1.json), gambar di boards/motion-proof-v1/.
- Keyframes berhasil diekstrak dari 14 komposisi dan caption. Bukti HP juga dicapture sebagai strip; strip yang mengikuti crop objek tidak cukup menunjukkan jarak gerak, sehingga frame penuh sebelum/selama/setelah penempatan ikut diperiksa.
- Seluruh shot diperiksa sebagai PNG ukuran penuh, termasuk pembuka, tiga penekanan, aksi melepas HP, dan pertanyaan penutup. Koreksi: tangan tetap di canvas, subtitle memakai frasa yang utuh, pertanyaan terakhir ditahan sampai akhir.
- WAV lolos decode penuh FFmpeg, tidak kosong, tidak ada sampel clipping. Sumber asli MP3 dan alignment disimpan; tidak ada sintesis ulang setelah request berhasil.

## Batas pemeriksaan

CUA tidak menyediakan browser yang dapat dikontrol. Pemeriksaan UI Studio dan penilaian audio lewat pendengaran tidak diklaim sudah dilakukan. Chromium HyperFrames menjalankan audit/snapshot dengan GPU hardware Intel Iris Xe / ANGLE D3D11. Durasi file, decode, batas peak, dan kesesuaian teks/alignment diperiksa; intonasi dan tempo perlu didengar di preview. Alignment native diskalakan terhadap atempo=0.85, sehingga selisih lokal kecil dari time-stretch tetap mungkin.

## Gate

Status: **preview / awaiting_review**. Naskah v1 dan storyboard visual v1 sudah disetujui. Preview ini belum mendapat persetujuan; belum ada render/export MP4. Sesuai HyperFrames CLI, render dilakukan setelah pengguna meninjau dan menerima preview.
''',encoding='utf8')

(ROOT.parent/'EPISODE.md').write_text('''# Kabar baik disambut datar

## Brief dan pilihan

- Pengguna memilih ide 4: “Lo bawa kabar baik. Dia cuma jawab, ‘Oh, bagus.’”
- Board **ruang-di-antara v2**, approved 17 Oktober 2026: [EDITORIAL.md](../../boards/ruang-di-antara/EDITORIAL.md) dan [DIRECTION.md](../../boards/ruang-di-antara/DIRECTION.md).
- Pilar Di antara kita. Satu adegan berbagi kabar presentasi yang dipuji, konsep capitalization dan respons aktif-konstruktif, satu kemungkinan percakapan, satu pertanyaan pengamatan.
- Register Indonesia lo–gua, dekat dan observatif; ilustrasi/grafis, tanpa foto/footage. Krem #F3EDE3, arang #302B28, bata #A34F3F, pasir #D8C8B5; Newsreader dan DM Sans lokal.
- Format 9:16, 1080×1920, 30 fps; target board 85–95 detik dan lebih dari 10 shot. Hasil preview: **89.885 detik, 14 shot**. Platform unggah belum dipilih; tidak menghambat preview.
- Route HyperFrames faceless-explainer, flow automation dengan checkpoint proyek tetap berlaku. Tidak ada native delegation; animasi dikerjakan inline dari layout yang diterima.

## Riset dan narasi

[SOURCES.md](SOURCES.md) menghubungkan C1–C4 ke Gable dkk. (2004, teks lengkap) dan Gable, Gonzaga, & Strachman (2006, abstrak). Klaim disampaikan sebagai asosiasi; satu jawaban pendek belum cukup menilai niat/kepedulian. Dialog dan skenario adalah ilustrasi. Narasi [SCRIPT.md](SCRIPT.md) tetap 175 kata tanpa perubahan sejak disetujui.

## Riwayat review

1. **Naskah v1 approved**, 18 Oktober 2026: pengguna menjawab “cocok” atas narasi lengkap. Ini menerima teks dan enam beat editorial.
2. **Storyboard visual v1 approved**, 18 Oktober 2026: pengguna menjawab “cocok” atas papan 14 shot. [Papan HTML](video/boards/storyboard.html) dan [PNG](video/boards/storyboard.png) dipertahankan; sumber layout dibekukan di video/boards/approved-storyboard-v1/.
3. **Preview v1 awaiting_review**: penerimaan storyboard melanjutkan audio/animasi, tidak menghapus review final preview. Audio dan motion versi ini belum disetujui pengguna. Belum ada export MP4.

## Audio dan assembly

- Default workspace: ElevenLabs George, JBFqnCBsd6RMkjVDRZzb, model eleven_multilingual_v2. Voice ini bukan pilihan eksplisit pengguna; dapat direvisi pada review.
- Satu full-script request yang berhasil dengan convert_with_timestamps, MP3 44100/128 dan normalized_alignment native. Shared engine sebelumnya gagal menghasilkan suara; format PCM44100 pada helper kemungkinan tidak sesuai tier akun. Direct SDK menghasilkan file valid; tidak ada retry sintesis otomatis. Detail di video/synthesize-narration.py dan assets/voice/narration-v1/.
- Audio asli 75.139773 detik. Preview memakai turunan WAV FFmpeg atempo=0.85, 88.385283 detik; hold penutup 1.5 detik. Pitch dipertahankan, kata tidak ditambah/dipotong/disintesis ulang. Timestamp diskalakan 1/0.85; time-stretch dapat menimbulkan selisih lokal kecil.
- Satu track suara kontinu, tanpa BGM/SFX. Subtitle lengkap 45 frasa pada satu track terpisah, maksimal dua baris; tiga teks penekanan dipertahankan.
- Cut dan gerak memakai rentang kata yang tercatat di [video/STORYBOARD.md](video/STORYBOARD.md), [video/SCRIPT.md](video/SCRIPT.md), audio_meta.json, dan captions.json. Gerak sendi menggunakan SVG original dan GSAP lokal 3.14.2; tidak mengubah layout yang disetujui.

## Status dan langkah berikutnya

**Stage: preview / awaiting_review.** Preview lokal aktif akan dicatat di video/boards/preview-server.json. Full check browser dan pemeriksaan PNG selesai; [VERIFICATION.md](video/VERIFICATION.md) menjelaskan bukti dan batas pemeriksaan. Browser UI CUA tidak tersedia; audio tidak diklaim telah dinilai lewat pendengaran.

Pengguna meninjau alur gerak, keterbacaan, tempo, dan intonasi di Studio. Jika ada revisi, simpan pada versi produksi ini dan ulangi pemeriksaan yang relevan. Jika preview diterima, lanjutkan render/export sesuai HyperFrames final-look gate, periksa hasil encode dan AV-nya, lalu perbarui tracker ke export/complete. Approval preview tidak dianggap sudah ada.
''',encoding='utf8')

tracker=WORKSPACE/'TRACKER.json'
t=read_json(tracker)
for row in t['productions']:
    if row['slug']=='kabar-baik-disambut-datar':
        row.update(stage='preview',status='awaiting_review')
assert all((WORKSPACE/row['path']).is_dir() for row in t['productions'])
dump(tracker,t)
print(json.dumps({'stage':'preview','status':'awaiting_review','shots':14,'words':len(words),'caption_groups':len(captions),'per_shot_pixel_motion_passed':len(pose_checks)},ensure_ascii=False))
