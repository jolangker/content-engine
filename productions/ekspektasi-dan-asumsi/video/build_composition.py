import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
timing = json.load(open(ROOT / 'timing.json', encoding='utf-8'))
audio_meta = json.load(open(ROOT / 'audio_meta.json', encoding='utf-8'))
caption_groups = json.load(open(ROOT / 'caption_groups.json', encoding='utf-8'))
total_duration = audio_meta['total_duration_s']

frames_dir = ROOT / 'compositions/frames'
frames_dir.mkdir(parents=True, exist_ok=True)

# 1. Generate Frame 01: Ekspektasi di Jalan Pulang
f1 = timing[0]
(frames_dir / '01-ekspektasi-pulang.html').write_text(f"""<template>
<div data-composition-id="scene-01" data-duration="{f1['duration']}" data-height="1920" data-width="1080" id="scene-01-root">
<section class="shot">
  <div class="ground clip" data-duration="{f1['duration']}" data-start="0" data-track-index="0" id="scene-01-ground"></div>
  <div class="eyebrow">Ruang di Antara</div>
  <div class="page-number">01</div>
  
  <h1 class="display" id="s01-title" style="top:320px; font-size:120px;">
    Sepanjang jalan pulang.
  </h1>

  <div id="s01-bubble" style="position:absolute; left:96px; top:580px; width:880px; padding:48px; background:#EAE2D5; border-radius:24px; border:2px solid #D8C8B5;">
    <div style="font-size:28px; text-transform:uppercase; letter-spacing:2px; color:#A34F3F; margin-bottom:16px; font-weight:600;">Skenario di kepala lo</div>
    <p style="font-family:Newsreader,serif; font-size:68px; line-height:1.2; color:#302B28;">
      “Pengen disambut hangat, atau ditanya: <em>hari ini gimana?</em>”
    </p>
  </div>

  <svg class="figure" id="s01-icon" style="left:460px; top:1040px; width:160px; height:160px;" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="42" fill="none" stroke="#A34F3F" stroke-width="3" stroke-dasharray="6 6"/>
    <path d="M50 25 V50 L65 65" fill="none" stroke="#A34F3F" stroke-width="4" stroke-linecap="round"/>
  </svg>

  <p class="foot" id="s01-foot">Hari rasanya berat. Ekspektasi sudah terbentuk sebelum sampai pintu.</p>
</section>
</div>
<script>
const tl = gsap.timeline({{paused:true}});
tl.fromTo("#s01-title", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 0.1);
tl.fromTo("#s01-bubble", {{opacity:0, scale:0.95}}, {{opacity:1, scale:1, duration:0.7, ease:"power3.out"}}, 2.5);
tl.fromTo("#s01-icon", {{opacity:0, rotation:-20}}, {{opacity:1, rotation:0, duration:0.6, ease:"power3.out"}}, 5.0);
tl.fromTo("#s01-foot", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 6.5);
window.__timelines["scene-01"] = tl;
</script>
</template>""", encoding='utf-8')

# 2. Generate Frame 02: Respons Kontras & Sinyal Tubuh
f2 = timing[1]
(frames_dir / '02-respons-kontras.html').write_text(f"""<template>
<div data-composition-id="scene-02" data-duration="{f2['duration']}" data-height="1920" data-width="1080" id="scene-02-root">
<section class="shot">
  <div class="ground clip" data-duration="{f2['duration']}" data-start="0" data-track-index="0" id="scene-02-ground"></div>
  <div class="eyebrow">Ruang di Antara</div>
  <div class="page-number">02</div>

  <h1 class="display" id="s02-title" style="top:320px; font-size:110px;">
    Situasi bergeser.
  </h1>

  <div id="s02-split" style="position:absolute; left:96px; top:540px; width:888px; display:flex; gap:32px;">
    <div style="flex:1; padding:36px; background:#F8F6F2; border:2px solid #D8C8B5; border-radius:20px;">
      <div style="font-size:24px; color:#A34F3F; text-transform:uppercase; letter-spacing:2px; font-weight:600;">Ekspektasi</div>
      <div style="font-size:44px; margin-top:12px; font-weight:500;">Disambut & ditemenin</div>
    </div>
    <div style="flex:1; padding:36px; background:#EDE6DC; border:2px solid #D8C8B5; border-radius:20px;">
      <div style="font-size:24px; color:#8E929A; text-transform:uppercase; letter-spacing:2px; font-weight:600;">Realitas</div>
      <div style="font-size:44px; margin-top:12px; font-weight:500;">Sapa sekilas, sibuk sendiri</div>
    </div>
  </div>

  <div id="s02-signals" style="position:absolute; left:96px; top:860px; width:888px; padding:40px; background:#302B28; color:#F3EDE3; border-radius:24px;">
    <div style="font-size:24px; color:#D8C8B5; letter-spacing:3px; text-transform:uppercase;">Bahasa Tubuh Menarik Diri</div>
    <div style="font-size:42px; line-height:1.4; margin-top:16px;">
      • Duduk agak jauh<br>
      • Helaan nafas diberatkan<br>
      • Nada bicara pendek-pendek
    </div>
  </div>

  <p class="foot" id="s02-foot">Sinyal dipancarkan tanpa sepatah kata pun penjelasan.</p>
</section>
</div>
<script>
const tl = gsap.timeline({{paused:true}});
tl.fromTo("#s02-title", {{opacity:0, y:25}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 0.1);
tl.fromTo("#s02-split", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 2.0);
tl.fromTo("#s02-signals", {{opacity:0, scale:0.96}}, {{opacity:1, scale:1, duration:0.7, ease:"power3.out"}}, 5.5);
tl.fromTo("#s02-foot", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 9.0);
window.__timelines["scene-02"] = tl;
</script>
</template>""", encoding='utf-8')

# 3. Generate Frame 03: Jurang Persepsi
f3 = timing[2]
(frames_dir / '03-jurang-persepsi.html').write_text(f"""<template>
<div data-composition-id="scene-03" data-duration="{f3['duration']}" data-height="1920" data-width="1080" id="scene-03-root">
<section class="shot">
  <div class="ground clip" data-duration="{f3['duration']}" data-start="0" data-track-index="0" id="scene-03-ground"></div>
  <div class="eyebrow">Ruang di Antara</div>
  <div class="page-number">03</div>

  <div id="s03-inner" style="position:absolute; left:96px; top:300px; width:888px; padding:44px; background:#FAF8F5; border-left:8px solid #A34F3F; border-radius:12px; box-shadow:0 8px 24px rgba(0,0,0,0.04);">
    <div style="font-size:24px; color:#A34F3F; text-transform:uppercase; letter-spacing:2px; font-weight:600;">Monolog Batin Lo</div>
    <div style="font-family:Newsreader,serif; font-size:62px; line-height:1.2; margin-top:14px; color:#302B28;">
      “Masa kayak gini aja nggak peka? Gestur gue udah sejelas ini.”
    </div>
  </div>

  <div id="s03-comparison" style="position:absolute; left:96px; top:680px; width:888px;">
    <div style="background:#FAF0EB; border:2px solid #E4C0B4; padding:36px; border-radius:20px; margin-bottom:24px;">
      <div style="font-size:26px; color:#A34F3F; font-weight:600; text-transform:uppercase;">Di persepsi lo:</div>
      <div style="font-size:48px; font-weight:600; color:#302B28; margin-top:6px;">Lampu Sorot Benderang 💡</div>
    </div>
    <div style="background:#ECE7DF; border:2px solid #D8C8B5; padding:36px; border-radius:20px;">
      <div style="font-size:26px; color:#706862; font-weight:600; text-transform:uppercase;">Di mata dia:</div>
      <div style="font-size:48px; font-weight:600; color:#302B28; margin-top:6px;">Lagi capek biasa / pengen tenang ☁️</div>
    </div>
  </div>

  <p class="foot" id="s03-foot">Dua orang di ruangan yang sama dengan dua realitas yang berbeda.</p>
</section>
</div>
<script>
const tl = gsap.timeline({{paused:true}});
tl.fromTo("#s03-inner", {{opacity:0, x:-30}}, {{opacity:1, x:0, duration:0.6, ease:"power3.out"}}, 0.1);
tl.fromTo("#s03-comparison", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.7, ease:"power3.out"}}, 4.0);
tl.fromTo("#s03-foot", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 8.5);
window.__timelines["scene-03"] = tl;
</script>
</template>""", encoding='utf-8')

# 4. Generate Frame 04: Illusion of Transparency
f4 = timing[3]
(frames_dir / '04-illusion-transparency.html').write_text(f"""<template>
<div data-composition-id="scene-04" data-duration="{f4['duration']}" data-height="1920" data-width="1080" id="scene-04-root" class="dark">
<section class="shot">
  <div class="ground clip" data-duration="{f4['duration']}" data-start="0" data-track-index="0" id="scene-04-ground" style="background:#262220;"></div>
  <div class="eyebrow" style="color:#D8C8B5;">Konsep Psikologi</div>
  <div class="page-number" style="color:#D8C8B5;">04</div>

  <div id="s04-badge" style="position:absolute; left:96px; top:310px; padding:12px 28px; background:rgba(216,200,181,0.15); border:1px solid #D8C8B5; border-radius:100px; font-size:24px; color:#D8C8B5; letter-spacing:2px; text-transform:uppercase;">
    Gilovich, Savitsky, & Medvec (1998)
  </div>

  <h1 class="display" id="s04-title" style="top:400px; font-size:122px; color:#F3EDE3;">
    Illusion of Transparency.
  </h1>

  <div id="s04-desc" style="position:absolute; left:96px; top:720px; width:888px; font-size:44px; line-height:1.45; color:#DDD5CA;">
    Kecenderungan kognitif melebih-lebihkan sejauh mana isi pikiran dan perasaan kita bisa dibaca orang lain.
  </div>

  <div id="s04-reason" style="position:absolute; left:96px; top:1040px; width:888px; padding:40px; background:rgba(255,255,255,0.05); border-radius:24px; border-left:6px solid #D8C8B5;">
    <div style="font-size:24px; color:#D8C8B5; letter-spacing:2px; text-transform:uppercase;">Mengapa Terjadi?</div>
    <div style="font-family:Newsreader,serif; font-size:56px; line-height:1.25; color:#FAF9F6; margin-top:12px;">
      “Karena rasa itu begitu bising di dalam diri, kita mengira dunia luar mendengar bunyinya.”
    </div>
  </div>

  <p class="foot" id="s04-foot" style="color:#A8A29E;">Perasaan intens di dalam tidak otomatis menjadi sinyal yang jelas di luar.</p>
</section>
</div>
<script>
const tl = gsap.timeline({{paused:true}});
tl.fromTo("#s04-badge", {{opacity:0, y:15}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, 0.1);
tl.fromTo("#s04-title", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 0.5);
tl.fromTo("#s04-desc", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 4.5);
tl.fromTo("#s04-reason", {{opacity:0, scale:0.96}}, {{opacity:1, scale:1, duration:0.7, ease:"power3.out"}}, 9.0);
tl.fromTo("#s04-foot", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, 13.0);
window.__timelines["scene-04"] = tl;
</script>
</template>""", encoding='utf-8')

# 5. Generate Frame 05: Jebakan Kedekatan
f5 = timing[4]
(frames_dir / '05-jebakan-kedekatan.html').write_text(f"""<template>
<div data-composition-id="scene-05" data-duration="{f5['duration']}" data-height="1920" data-width="1080" id="scene-05-root">
<section class="shot">
  <div class="ground clip" data-duration="{f5['duration']}" data-start="0" data-track-index="0" id="scene-05-ground"></div>
  <div class="eyebrow">Ruang di Antara</div>
  <div class="page-number">05</div>

  <h1 class="display" id="s05-title" style="top:320px; font-size:115px;">
    Jebakan kedekatan.
  </h1>

  <div id="s05-card" style="position:absolute; left:96px; top:540px; width:888px; padding:44px; background:#FAF8F5; border-radius:24px; border:2px solid #D8C8B5;">
    <div style="font-size:24px; color:#A34F3F; letter-spacing:2px; text-transform:uppercase; font-weight:600;">Asumsi Hubungan</div>
    <div style="font-family:Newsreader,serif; font-size:56px; line-height:1.25; color:#302B28; margin-top:14px;">
      “Kalau dia beneran sayang, harusnya dia otomatis tahu.”
    </div>
  </div>

  <div id="s05-truth" style="position:absolute; left:96px; top:900px; width:888px; padding:44px; background:#302B28; color:#F3EDE3; border-radius:24px;">
    <div style="font-size:24px; color:#D8C8B5; letter-spacing:2px; text-transform:uppercase;">Kenyataan Relasi</div>
    <div style="font-size:50px; font-weight:600; line-height:1.25; margin-top:16px;">
      Sayang bukan berarti telepati.<br>
      <span style="color:#D8C8B5; font-weight:400; font-size:40px;">Pasangan lo bukan cenayang.</span>
    </div>
  </div>

  <p class="foot" id="s05-foot">Kedekatan cinta tidak menggantikan kebutuhan berkomunikasi secara verbal.</p>
</section>
</div>
<script>
const tl = gsap.timeline({{paused:true}});
tl.fromTo("#s05-title", {{opacity:0, y:25}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 0.1);
tl.fromTo("#s05-card", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 1.5);
tl.fromTo("#s05-truth", {{opacity:0, scale:0.96}}, {{opacity:1, scale:1, duration:0.7, ease:"power3.out"}}, 5.8);
tl.fromTo("#s05-foot", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 9.0);
window.__timelines["scene-05"] = tl;
</script>
</template>""", encoding='utf-8')

# 6. Generate Frame 06: Alternatif Komunikasi Lugas
f6 = timing[5]
(frames_dir / '06-komunikasi-lugas.html').write_text(f"""<template>
<div data-composition-id="scene-06" data-duration="{f6['duration']}" data-height="1920" data-width="1080" id="scene-06-root">
<section class="shot">
  <div class="ground clip" data-duration="{f6['duration']}" data-start="0" data-track-index="0" id="scene-06-ground"></div>
  <div class="eyebrow">Alternatif Respons</div>
  <div class="page-number">06</div>

  <h1 class="display" id="s06-title" style="top:300px; font-size:105px;">
    Ubah kode jadi kalimat.
  </h1>

  <div id="s06-intro" style="position:absolute; left:96px; top:480px; width:888px; padding:36px; background:#EDE7DF; border-radius:20px; border-left:6px solid #A34F3F;">
    <div style="font-size:24px; color:#A34F3F; text-transform:uppercase; font-weight:600; letter-spacing:2px;">Risiko Menunggu Ditebak</div>
    <div style="font-family:Newsreader,serif; font-size:46px; line-height:1.3; color:#302B28; margin-top:8px;">
      Kita sedang menyiapkan diri untuk kecewa pada ekspektasi yang kita bangun sendiri.
    </div>
  </div>

  <div id="s06-box" style="position:absolute; left:96px; top:740px; width:888px; padding:40px; background:#FAF8F5; border:3px solid #302B28; border-radius:24px; box-shadow:0 12px 32px rgba(0,0,0,0.06);">
    <div style="font-size:24px; color:#A34F3F; letter-spacing:2px; text-transform:uppercase; font-weight:600;">Contoh Kalimat Lugas</div>
    <div style="font-family:Newsreader,serif; font-size:52px; line-height:1.28; color:#302B28; margin-top:14px;">
      “Hari ini gue capek banget dan rasanya lagi sensitif. Gue nggak butuh solusi, tapi boleh nggak kita duduk bareng dulu setengah jam?”
    </div>
  </div>

  <div id="s06-steps" style="position:absolute; left:96px; top:1160px; width:888px; display:flex; gap:20px;">
    <div style="flex:1; padding:24px; background:#EAE2D5; border-radius:16px;">
      <div style="font-size:20px; color:#A34F3F; font-weight:600;">1. Keadaan</div>
      <div style="font-size:28px; font-weight:500; margin-top:4px;">Capek & sensitif</div>
    </div>
    <div style="flex:1; padding:24px; background:#EAE2D5; border-radius:16px;">
      <div style="font-size:20px; color:#A34F3F; font-weight:600;">2. Batasan</div>
      <div style="font-size:28px; font-weight:500; margin-top:4px;">Bukan solusi</div>
    </div>
    <div style="flex:1; padding:24px; background:#EAE2D5; border-radius:16px;">
      <div style="font-size:20px; color:#A34F3F; font-weight:600;">3. Permintaan</div>
      <div style="font-size:28px; font-weight:500; margin-top:4px;">Duduk 30 menit</div>
    </div>
  </div>

  <p class="foot" id="s06-foot">Memberi arah yang jelas jauh lebih adil daripada menguji kepekaan.</p>
</section>
</div>
<script>
const tl = gsap.timeline({{paused:true}});
tl.fromTo("#s06-title", {{opacity:0, y:25}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 0.1);
tl.fromTo("#s06-intro", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 0.5);
tl.fromTo("#s06-box", {{opacity:0, y:25}}, {{opacity:1, y:0, duration:0.7, ease:"power3.out"}}, 10.5);
tl.fromTo("#s06-steps", {{opacity:0, y:25}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 17.5);
tl.fromTo("#s06-foot", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 20.0);
window.__timelines["scene-06"] = tl;
</script>
</template>""", encoding='utf-8')

# 7. Generate Frame 07: Refleksi Penutup
f7 = timing[6]
(frames_dir / '07-refleksi-penutup.html').write_text(f"""<template>
<div data-composition-id="scene-07" data-duration="{f7['duration']}" data-height="1920" data-width="1080" id="scene-07-root" class="dark">
<section class="shot">
  <div class="ground clip" data-duration="{f7['duration']}" data-start="0" data-track-index="0" id="scene-07-ground" style="background:#262220;"></div>
  <div class="eyebrow" style="color:#D8C8B5;">Refleksi Akhir</div>
  <div class="page-number" style="color:#D8C8B5;">07</div>

  <div id="s07-question" style="position:absolute; left:96px; top:520px; width:888px;">
    <div style="font-size:32px; color:#D8C8B5; letter-spacing:3px; text-transform:uppercase;">Sebelum lo menyimpulkan dia nggak peduli...</div>
    <h1 style="font-family:Newsreader,serif; font-size:92px; line-height:1.2; color:#FAF9F6; margin-top:32px; font-weight:400;">
      Kebutuhan itu udah beneran keluar lewat kata-kata, atau baru sebatas skenario di kepala lo sendiri?
    </h1>
  </div>

  <div id="s07-brand" style="position:absolute; left:96px; top:1340px; border-top:1px solid rgba(216,200,181,0.3); padding-top:40px; width:888px;">
    <div style="font-size:28px; letter-spacing:4px; text-transform:uppercase; color:#D8C8B5;">Ruang di Antara</div>
    <div style="font-size:34px; color:#A8A29E; margin-top:8px;">Melihat pola hubungan dengan lebih jernih.</div>
  </div>
</section>
</div>
<script>
const tl = gsap.timeline({{paused:true}});
tl.fromTo("#s07-question", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.7, ease:"power3.out"}}, 0.1);
tl.fromTo("#s07-brand", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, 5.0);
window.__timelines["scene-07"] = tl;
</script>
</template>""", encoding='utf-8')

print("Generated all 7 composition frames.")

# 8. Generate Captions Pill Component
captions_html = f"""<template>
<div data-composition-id="captions" data-duration="{total_duration}" data-height="1920" data-width="1080" id="captions-root">
  <div id="caption-box" style="position:absolute; left:96px; right:96px; bottom:180px; display:flex; justify-content:center; pointer-events:none; z-index:999;">
    <div id="caption-pill" style="background:rgba(26,24,23,0.85); border:1px solid rgba(255,255,255,0.12); padding:16px 36px; border-radius:100px; font-family:'DM Sans',sans-serif; font-size:38px; font-weight:600; color:#FAF9F6; text-align:center; box-shadow:0 12px 32px rgba(0,0,0,0.35);">
      <span id="caption-text"></span>
    </div>
  </div>
</div>
<script>
const groups = {json.dumps(caption_groups)};
const textEl = document.getElementById('caption-text');
const pillEl = document.getElementById('caption-pill');

const tl = gsap.timeline({{paused:true}});

groups.forEach(g => {{
  tl.call(() => {{
    pillEl.style.opacity = '1';
    textEl.textContent = g.text;
  }}, null, g.start);
}});

// Hide when inactive
tl.call(() => {{
  pillEl.style.opacity = '0';
}}, null, {audio_meta['audio_duration_s']});

window.__timelines["captions"] = tl;
</script>
</template>"""

(ROOT / 'compositions/captions.html').write_text(captions_html, encoding='utf-8')
print("Generated compositions/captions.html")

# 9. Generate Master index.html
mounts = []
for i, f in enumerate(timing):
    mounts.append(
        f'<div class="clip shot" id="mount-0{f["n"]}" data-label="{f["title"]}" '
        f'data-composition-id="scene-0{f["n"]}" data-composition-src="compositions/frames/{f["id"]}.html" '
        f'data-start="{f["start"]}" data-duration="{f["duration"]}" data-track-index="{i+1}" '
        f'data-track-kind="graphics" data-width="1080" data-height="1920"></div>'
    )

index_html = f"""<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=1080,height=1920">
  <title>Jelas di Kepala Lo, Tapi Belum Pernah Diomongin — Ruang di Antara</title>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <style>
    @font-face {{
      font-family: Newsreader;
      src: url('assets/fonts/newsreader.ttf') format('truetype');
      font-weight: 200 800;
      font-display: block;
    }}
    @font-face {{
      font-family: Newsreader;
      src: url('assets/fonts/newsreader-italic.ttf') format('truetype');
      font-weight: 200 800;
      font-style: italic;
      font-display: block;
    }}
    @font-face {{
      font-family: 'DM Sans';
      src: url('assets/fonts/dm-sans.ttf') format('truetype');
      font-weight: 100 1000;
      font-display: block;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{
      margin: 0;
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #F3EDE3;
      color: #302B28;
      font-family: 'DM Sans', sans-serif;
      -webkit-font-smoothing: antialiased;
    }}
    #root {{
      width: 100%;
      height: 100%;
      position: relative;
      overflow: hidden;
    }}
    .shot {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
    }}
    .ground {{
      position: absolute;
      inset: 0;
      background: #F3EDE3;
    }}
    .dark .ground {{
      background: #262220;
    }}
    .dark {{
      color: #F3EDE3;
    }}
    .eyebrow {{
      position: absolute;
      left: 96px;
      top: 148px;
      font-size: 25px;
      letter-spacing: 3px;
      text-transform: uppercase;
      font-weight: 500;
    }}
    .page-number {{
      position: absolute;
      right: 150px;
      top: 148px;
      font-size: 25px;
      letter-spacing: 3px;
    }}
    h1, h2, p {{ margin: 0; }}
    .display {{
      position: absolute;
      left: 96px;
      width: 888px;
      font-family: Newsreader, serif;
      font-weight: 400;
      line-height: 1.05;
      letter-spacing: -3px;
    }}
    .foot {{
      position: absolute;
      left: 96px;
      bottom: 260px;
      right: 120px;
      font-size: 32px;
      line-height: 1.4;
      color: #55504A;
    }}
    .foot:before {{
      content: '';
      display: block;
      width: 80px;
      height: 3px;
      background: currentColor;
      margin-bottom: 24px;
    }}
    .figure {{
      position: absolute;
      display: block;
    }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{total_duration}">
    {''.join(mounts)}
    <div id="caption-mount" class="clip shot" style="z-index:100" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{total_duration}" data-track-index="10" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
    <audio id="master-voice" src="{audio_meta['audio_path']}" data-start="0" data-duration="{audio_meta['audio_duration_s']}" data-track-index="99" data-track-kind="audio"></audio>
  </div>
  <script>
    window.__timelines = window.__timelines || {{}};
    window.__timelines["main"] = gsap.timeline({{paused:true}});
  </script>
</body>
</html>"""

(ROOT / 'index.html').write_text(index_html, encoding='utf-8')
print("Generated index.html with master audio track.")
