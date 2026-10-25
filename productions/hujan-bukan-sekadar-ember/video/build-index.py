from pathlib import Path
import json
V=Path(__file__).resolve().parent
scenes=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'))
starts=[];ends=[];t=0
for s in scenes: starts.append(t);t+=s['duration'];ends.append(t)
timing=dict(starts=starts,ends=ends)
(V/'timing.json').write_text(json.dumps(timing,indent=2),encoding='utf-8')
audio='';captions='';meta=V/'audio_meta.json'
if meta.exists():
    m=json.loads(meta.read_text(encoding='utf-8'));t=float(m.get('export_duration',t));audio=(V/'audio-tags.html').read_text(encoding='utf-8') if (V/'audio-tags.html').exists() else ''
    captions=(V/'captions.mount.txt').read_text(encoding='utf-8') if (V/'captions.mount.txt').exists() else ''
html='''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><title>Hujan bukan sekadar ember · Bongkar Sistem</title>
<script src="vendor/gsap.min.js"></script>
<style>
@font-face{font-family:Barlow;src:url('assets/fonts/barlow-bold.ttf');font-weight:700}
@font-face{font-family:Barlow;src:url('assets/fonts/barlow-black.ttf');font-weight:900}
@font-face{font-family:Barlow;src:url('assets/fonts/barlow-regular.ttf');font-weight:400}
@font-face{font-family:'IBM Plex Mono';src:url('assets/fonts/ibm-plex-mono.ttf');font-weight:400}
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;background:#8CCFE8;color:#173B42;font-family:Barlow,sans-serif}
#root{width:100%;height:100%;position:relative;overflow:hidden}.clip{position:absolute;inset:0}
#world{width:100%;height:100%;display:block}.identity{position:absolute;left:72px;top:164px;display:flex;align-items:center;gap:18px;font-size:29px;font-weight:900;letter-spacing:1px}.identity:before{content:'';width:12px;height:33px;background:#F4C44B;border-radius:3px}
#scene-title{position:absolute;left:72px;top:224px;font-size:64px;font-weight:900;line-height:1.02;max-width:840px;margin:0}
#scene-label{position:absolute;left:72px;bottom:335px;max-width:800px;background:#FFF5DE;padding:14px 21px;border-radius:12px;font-size:34px;font-weight:700;line-height:1.14;border-left:7px solid #178A91}
#section-label{position:absolute;right:160px;top:565px;font-family:'IBM Plex Mono',monospace;font-size:26px;letter-spacing:1px;padding:12px;background:#FFF5DE;border-radius:6px}
.spoken{position:absolute;left:72px;top:342px;max-width:858px;width:max-content;padding:17px 26px;background:#FFF5DE;border-radius:16px;font-size:58px;line-height:1.1;font-weight:700;letter-spacing:-.87px;box-shadow:0 5px 0 #173B4215}
.footer{position:absolute;left:72px;bottom:275px;font-size:28px;font-weight:700;letter-spacing:.3px}
</style></head><body>
<div id="root" data-composition-id="rainwater" data-width="1080" data-height="1920" data-duration="DURATION">
<canvas id="world" class="clip" data-start="0" data-duration="DURATION" data-track-index="0"></canvas>
<div class="identity">BONGKAR SISTEM</div>
FRAMES
<div class="footer">Skema edukasi · bukan gambar instalasi</div>
CAPTIONS
AUDIO
</div>
<script>window.EPISODE_PLAN=PLAN;window.EPISODE_TIMING=TIMING;window.EPISODE_CUES=CUES;window.STATIC_STORYBOARD=STATIC;
const tl=gsap.timeline({paused:true});tl.to({}, {duration:DURATION});window.__timelines=window.__timelines||{};window.__timelines.rainwater=tl;</script>
<script type="module" src="world.js"></script>
</body></html>'''
# Literal placeholder substitution avoids replacing the variable names themselves.
cues=json.loads((V/'cues.json').read_text()) if (V/'cues.json').exists() else {}
frames=''.join(f'<div id="scene-{s["id"]}" data-composition-id="{s["id"]}" data-composition-src="compositions/frames/{s["id"]}.html" data-start="{starts[i]:.4f}" data-duration="{s["duration"]:.4f}" data-width="1080" data-height="1920" data-track-index="1"></div>' for i,s in enumerate(scenes))
html=html.replace('=PLAN;','='+json.dumps(scenes,ensure_ascii=False)+';').replace('=TIMING;','='+json.dumps(timing)+';').replace('=CUES;','='+json.dumps(cues)+';').replace('=STATIC;','=false;' if meta.exists() else '=true;').replace('DURATION',f'{t:.4f}').replace('CAPTIONS',captions).replace('AUDIO',audio).replace('FRAMES',frames)
(V/'index.html').write_text(html,encoding='utf-8')
print(f'Index: {t:.3f}s; {len(scenes)} scenes; static storyboard={not meta.exists()}')
