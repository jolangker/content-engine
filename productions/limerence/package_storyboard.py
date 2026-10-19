"""Package inspected HyperFrames stills as a reviewable static storyboard."""
from pathlib import Path
import html
import json
import struct

PROD = Path(__file__).resolve().parent
VIDEO = PROD / "video"
frames = json.loads((VIDEO / "storyboard-data.json").read_text(encoding="utf-8"))
source = (PROD / "SCRIPT.md").read_text(encoding="utf-8")
paras = source.split("## Reading copy\n\n",1)[1].split("\n## Timing and delivery",1)[0].strip().split("\n\n")

descriptions = [
    "Pengalaman yang masih sedikit berdampingan dengan masa depan yang sudah dibayangkan.",
    "Perhatian kecil adalah kejadian. Kesimpulan tentang kecocokan masih perlu diuji.",
    "Perbedaan, janji, dan batas: ada sisi dirinya yang belum lo alami langsung.",
    "Garis solid menandai pengalaman; perpanjangan putus-putus menandai bayangan.",
    "Konsep dikenalkan setelah situasinya terasa dekat, tanpa memberi diagnosis.",
    "Pertanyaan dibiarkan terbuka; perasaan orang lain belum kita ketahui.",
    "Membaca ulang percakapan menjadi contoh pencarian tanda.",
    "Satu frame arang memberi tekanan saat berbagai tafsir menjaga kemungkinan.",
    "Yang dibayangkan tampak lebih besar daripada pengalaman yang sudah dibagikan.",
    "Berfantasi tentang masa depan saja belum cukup untuk menyimpulkan limerence.",
    "Dua pertanyaan refleksi tentang perhatian dan dampaknya pada keseharian.",
    "Pisahkan kejadian dari harapan yang dilekatkan padanya.",
    "Contoh kopi kembali untuk memperjelas perbedaan kejadian dan kesimpulan.",
    "Pertanyaan penutup memberi ruang bagi pengalaman yang benar-benar dibangun berdua.",
]

cards=[]
for f,p,desc in zip(frames,paras,descriptions):
    stills=list((VIDEO/'boards'/'stills').glob(f'frame-{f["i"]-1:02d}-at-*.png'))
    if len(stills)!=1:
        raise RuntimeError(f'Expected exactly one still for frame {f["i"]}, found {stills}')
    png=stills[0]
    w,h=struct.unpack('>II',png.read_bytes()[16:24])
    assert (w,h)==(1080,1920),(png,w,h)
    f['still']=f'stills/{png.name}'
    cards.append(f'''<article class="frame" id="frame-{f['i']:02d}">
<a class="still" href="{f['still']}" target="_blank" aria-label="Lihat frame {f['i']:02d} ukuran penuh"><img src="{f['still']}" alt="{html.escape(desc,quote=True)}" width="1080" height="1920"></a>
<div class="card-body"><div class="time">{f['start']:.0f}–{f['end']:.0f} detik <span>· {f['duration']} detik</span></div>
<h2 class="title">{f['i']:02d}: {html.escape(f['title'])}</h2>
<p class="words">{html.escape(desc)}</p>
<details><summary>Narasi</summary><p>{html.escape(p)}</p></details></div></article>''')

page='''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Limerence — Storyboard v1 · Ruang di Antara</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f5f4f1;color:#302b28;font-family:Inter,system-ui,sans-serif;font-size:16px;line-height:1.55}
main{max-width:1540px;margin:auto;padding:52px 40px 64px}.eyebrow{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#6c5e54;margin:0 0 12px}
header{max-width:1000px;margin-bottom:34px}h1{font-size:clamp(28px,3.2vw,46px);letter-spacing:-.04em;line-height:1.12;font-weight:550;margin:0 0 20px}
.intro{max-width:850px;color:#625850;margin:0 0 20px}.tags{display:flex;gap:10px;flex-wrap:wrap}.tags span{border:1px solid #d8c8b5;border-radius:100px;padding:5px 12px;font-size:12px;background:#fcfbf8}
.legend{display:flex;gap:28px;flex-wrap:wrap;font-size:13px;color:#625850;margin-top:20px}.sample{display:inline-block;width:30px;border-top:2px solid #302b28;vertical-align:middle;margin-right:8px}.sample.dashed{border-top:2px dashed #a34f3f}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px;align-items:start}.frame{background:#fff;border:1px solid #e0dcd5;border-radius:16px;overflow:hidden}
.still{display:block;background:#f3ede3}.still:focus-visible{outline:4px solid #a34f3f;outline-offset:-4px}.still img{display:block;width:100%;height:auto;aspect-ratio:9/16}
.card-body{padding:18px 20px 20px}.time{font-size:12px;color:#8c5949;letter-spacing:.02em}.time span{color:#786c63}.title{font-size:19px;line-height:1.25;letter-spacing:-.025em;margin:7px 0 11px;font-weight:600}
.words{font-size:14px;line-height:1.5;color:#625850;margin:0}details{border-top:1px solid #e9e5df;margin-top:16px;padding-top:12px}summary{cursor:pointer;font-size:13px;color:#6e4739}details p{font-size:14px;line-height:1.6;margin:12px 0 0}
footer{margin-top:36px;font-size:13px;color:#6b6058;border-top:1px solid #d8c8b5;padding-top:20px}a{color:inherit}.status{color:#8c5949;font-weight:550}
@media(max-width:1000px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}main{padding:32px 20px}}@media(max-width:620px){.grid{grid-template-columns:1fr;gap:20px}main{padding:28px 16px}.card-body{padding:16px}.legend{gap:10px}}
</style></head><body><main><header><p class="eyebrow">Ruang di Antara · Limerence · Storyboard v1</p>
<h1>Kenal dia, atau mengisi<br>yang belum lo tahu?</h1>
<p class="intro">14 komposisi statis untuk meninjau alur, teks, dan hubungan antar-bentuk. Klik gambar untuk melihat ukuran penuh; buka “Narasi” untuk membaca bagian naskahnya.</p>
<div class="tags"><span>9:16 · 1080 × 1920</span><span>±90 detik · estimasi</span><span class="status">Menunggu review visual</span></div>
<div class="legend"><span><i class="sample"></i>Kejadian / pengalaman</span><span><i class="sample dashed"></i>Bayangan / tafsir</span></div></header>
<section class="grid" aria-label="14 frame storyboard">'''+"\n".join(cards)+'''</section>
<footer>Storyboard statis · Naskah v1 disetujui · Durasi akan disesuaikan dengan hasil narasi. Ruang bawah tiap frame disediakan untuk subtitle. Untuk revisi, sebut nomor frame dan bagian yang ingin diubah.</footer>
</main></body></html>'''
(VIDEO/'boards'/'storyboard.html').write_text(page,encoding='utf-8')
(VIDEO/'storyboard-data.json').write_text(json.dumps(frames,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'frames':len(frames),'fullSizeStills':'1080x1920','board':str(VIDEO/'boards'/'storyboard.html')},ensure_ascii=False))
