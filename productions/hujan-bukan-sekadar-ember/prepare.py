from pathlib import Path
import json, shutil, importlib.util

P=Path(__file__).resolve().parent
V=P/'video'
ROOT=P.parents[1]
scenes=[
dict(id='01-kumpulkan',title='Ember saja cukup?',label='Atap → talang → tangki',duration=15,vo='Kalau kamu mau menyimpan air hujan, taruh ember saja. Beres? Belum. Mulutnya kecil, sementara air dari atap lewat begitu saja. Jadi, kumpulkan lewat talang, lalu arahkan ke tangki.',purpose='Establish the goal, the tiny collection area and the roof-fed solution.'),
dict(id='02-saring',title='Daunnya ikut masuk',label='Saringan sampah besar',duration=14,vo='Tapi atap juga mengumpulkan daun dan kotoran. Kita pasang saringan untuk menahan sampah besar. Masalahnya, debu yang terbawa air masih bisa lewat. Saringan ini belum membuat air aman diminum.',purpose='Distinguish debris screening from water treatment.'),
dict(id='03-pisahkan',title='Belokkan aliran awal',label='Tabung terisi → aliran ke tangki',duration=19,vo='Jadi, aliran awal kita belokkan ke tabung terpisah. Tabung ini terisi lebih dulu, lalu air berikutnya mengalir ke tangki. Namanya pemisah aliran awal. Setelah hujan, tabung perlu dikuras dan dibersihkan supaya siap dipakai lagi.',purpose='Open a sectional view and trace first-flush filling, bypass and reset.'),
dict(id='04-tutup',title='Ada yang mau pindahan',label='Tutup + jala pada bukaan',duration=18,vo='Kelihatannya sudah beres. Eh, ada yang mau pindahan. Tangki dibiarkan terbuka, nyamuk bisa masuk. Jadi, tutup tangkinya, dan beri jala pada bukaan, termasuk ventilasi. Dinding yang tidak tembus cahaya juga membantu membatasi pertumbuhan alga.',purpose='Use a brief theatrical visitor gag to motivate lid and screened openings.'),
dict(id='05-limpahkan',title='Penuh, lalu ke mana?',label='Pelimpah → area penerima',duration=13,vo='Sekarang hujannya terus turun. Kalau tangki penuh, air butuh jalan keluar. Kita tambahkan pipa pelimpah, lalu arahkan menjauhi fondasi rumah. Jalur keluar ini juga diberi jala.',purpose='Trace excess water away from the house to a receiving planted depression.'),
dict(id='06-pakai',title='Setiap bagian ada alasannya',label='Untuk menyiram tanaman hias',duration=15,vo='Saat dibutuhkan, air bisa diambil untuk menyiram tanaman hias. Bersihkan talang, saringan, dan penampung secara berkala. Ini sistem penampungan, bukan pengolahan air minum. Nah, sekarang kamu boleh duduk. Tanamannya dulu yang minum.',purpose='Resolve the collection chain, maintenance, end use and chair callback.')]
(V/'scene-plan.json').write_text(json.dumps(scenes,ensure_ascii=False,indent=2),encoding='utf-8')
script='# Narration v1\n\nAgent-verified against SOURCES.md before synthesis. Indonesian, native speed; approximately 94 seconds including comic/read holds.\n\n'
for s in scenes: script+=f"## {s['id']} — {s['title']}\n\n{s['vo']}\n\n"
(P/'SCRIPT.md').write_text(script,encoding='utf-8');(V/'SCRIPT.md').write_text(script,encoding='utf-8')
start=0; storyboard='''---
format: 1080x1920
duration: 90s
message: Every rainwater collection component solves a different problem.
arc: how-to-process
audience: Curious Indonesian general viewers
mode: autonomous
---

## Video direction

Inherit Bongkar Sistem v1 exactly: warm daylight, sky #8CCFE8, earth #B77C51/#875B43, roof #D66B44, teal #178A91, yellow #F4C44B, cream #FFF5DE and ink #173B42. Barlow captions 58px/700 with cream backing; labels 34px/700. Yellow-cap builder with cream sleeves and teal overalls is invariant. Original procedural true 3D scene; world coordinates and added components persist across views. Roof/tank/destination remain spatially continuous. Exposed front wall is a labeled SECTION, not transparent material in the real tank.

Three composition families: environment-wide collection, screen/first-flush diagnostic close-ups, tank/character comedy and wide final-use return. No title panels replace the world. Water paths develop on spoken cues. Captions occupy x72–930 y300–500; critical action lies y570–1530. Upper series mark at y170. Labels lie near the relevant object, clear of caption rail.

Motion grammar: compose multi-phase-camera, dynamic-content-sequencing and anticipation/settle using deterministic Three.js time and paused GSAP annotation timelines. Each scene has a time-coded evolving action; no front-loaded slideshow or idle screensaver motion. Water moves only along installed routes. No orbit for its own sake. Beat 4 includes a 3–5s arrival/reaction; the final chair payoff has a readable hold. No music; restrained action SFX and water, with room around the joke.

Execution: flow automation, storyboard no, mode autonomous. Pipeline override requires static poses, all six stills, HTML board and PNG before audio/animation. Agent verification replaces human approval. Export is authorized under the user's --automation. No package or publishing.

'''
shots=[
'0–4s: centered bucket/character, broad roof context; builder points confidently. 4–8s: view opens to demonstrate roof runoff missing bucket. 8–end: gutter/downspout/tank assemble in causal order, camera lands on their connected route.',
'0–4s: asymmetric close view of gutter and leaves. 4–9s: mesh arrives, leaves stop while blue flow continues. 9–end: fine brown dots pass the mesh; hold the distinction without a purity checkmark.',
'0–5s: sectional standpipe dominates, dirty first portion runs downward. 5–10s: chamber fills to tee and subsequent blue flow turns toward tank. 10–14s: name appears after function. 14–end: after-rain state, inlet stops and bottom drain empties slowly; cleaning/reset cue.',
'0–4s: builder unfolds chair, mosquito visitor arrives with suitcase, reaction hold. 4–8s: open tank vulnerability is visible. 8–13s: lid and ventilation mesh assemble. 13–end: section closes into opaque tank and visitor waits outside; no airtight cap claim.',
'0–4s: tank section reaches overflow elevation. 4–9s: overflow pipe installs and water traverses it toward the receiving bed away from the house. 9–end: close view confirms outlet mesh; wide receiving destination makes the drainage route unambiguous.',
'0–5s: wide completed system; builder fills watering can from low tap, pours onto ornamental plant. 5–10s: component cleaning cue appears on the named parts, no removal of essential screens. 10–end: non-potable boundary and final seated character hold; the plant, not the person, receives water.'
]
for i,s in enumerate(scenes):
    storyboard+=f"## Frame {i+1} — {s['title']}\n\n- status: built\n- src: compositions/frames/{s['id']}.html\n- duration: {s['duration']}s\n- start: {start}s\n- poster: {s['duration']*.65:.2f}s\n- transition_in: cut\n- scene: {s['purpose']}\n- voiceover: {s['vo']}\n- asset_candidates: []\n- narrativeRole: {'Hook' if i==0 else 'Key_Feature' if i<5 else 'Brand_Outro'}\n- focal: Original shared 3D rainwater diorama, view {i+1}\n- caption_keepout: x72–930 y300–500\n- rules: multi-phase-camera, dynamic-content-sequencing\n\nPurpose: {s['purpose']}\n\nLayout: {['layered-depth','asymmetric 60/40','centered','rule-of-thirds','layered-depth','centered'][i]}. {shots[i]}\n\nExact label: `{s['label']}`. Diagram claims map to SOURCES.md S1/S2.\n\n"
    start+=s['duration']
(V/'STORYBOARD.md').write_text(storyboard,encoding='utf-8')
(V/'capture/extracted').mkdir(parents=True,exist_ok=True)
(V/'capture/extracted/visible-text.txt').write_text((V/'BRIEF.md').read_text(encoding='utf-8')+'\n\n'+(P/'SOURCES.md').read_text(encoding='utf-8'),encoding='utf-8')
(V/'capture/extracted/tokens.json').write_text(json.dumps(dict(title='Hujan bukan sekadar ember',description='Progressive rainwater-harvesting explanation',colors=['#8CCFE8','#173B42','#FFF5DE','#178A91','#F4C44B'],fonts=['Barlow','IBM Plex Mono'])),encoding='utf-8')
(V/'vendor').mkdir(exist_ok=True)
for source,dest in [('three/build/three.module.js','three.module.js'),('three/build/three.core.js','three.core.js'),('gsap/dist/gsap.min.js','gsap.min.js')]:shutil.copy(V/'node_modules'/source,V/'vendor'/dest)
shutil.copy(V/'node_modules/three/LICENSE',V/'vendor/THREE-LICENSE.txt')
(V/'vendor/GSAP-LICENSE.txt').write_text('GSAP 3.14.2. License information: https://gsap.com/standard-license/\nFrozen from the published gsap npm package.\n',encoding='utf-8')
print('Prepared script, six-scene storyboard, source package and frozen libraries. Static poses next; no audio request made.')
