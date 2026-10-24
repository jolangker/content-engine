from pathlib import Path
import json, shutil, importlib.util, re
V=Path(__file__).resolve().parent
P=V.parent; R=P.parent.parent
spec=importlib.util.spec_from_file_location('narration',R/'.agents/skills/shortform-production/scripts/narration.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
voice,resolution=mod.resolve_voice(R)
rows=[
('Masuk, belum tentu berputar','Kunci yang salah tetap bisa masuk.', 'front',5,'Kunci bisa masuk, tapi kenapa belum tentu bisa diputar? Jawabannya ada pada pin-pin kecil di dalamnya.'),
('Gerigi mengatur tinggi','Lima pasangan pin, satu syarat.', 'side',5,'Kita lihat silinder kunci pin konvensional. Gerigi anak kunci harus menyelaraskan semua pasangan pin, bukan sekadar masuk.'),
('Rumah tetap. Inti berputar.','Dua bagian dengan tugas berbeda.', 'shell',5,'Bagian luarnya disebut rumah kunci. Di dalamnya ada inti yang bisa berputar, dengan lubang tempat anak kunci masuk.'),
('Satu ruang, tiga bagian','Pin bawah · pin atas · pegas', 'stack',6,'Setiap ruang berisi pin bawah, pin atas, dan pegas. Panjang pin bawah mengikuti kedalaman gerigi pasangannya.'),
('Tanpa kunci: terhalang','Pin atas melintasi batas putar.', 'blocked',6,'Tanpa anak kunci, pegas mendorong susunan pin turun. Pin atas menyeberangi batas inti dan rumah, sehingga putaran terhalang.'),
('Masuk → naik turun','Gerigi mengangkat; pegas menekan.', 'insert',6,'Saat anak kunci masuk, permukaan geriginya mendorong pin bawah. Pin atas ikut naik, dan pegas di atasnya tertekan.'),
('Setiap tinggi punya pasangan','Gerigi tinggi bertemu pin lebih pendek.', 'profile',6,'Gerigi yang lebih tinggi dipasangkan dengan pin bawah lebih pendek. Gerigi lebih rendah memakai pin bawah lebih panjang.'),
('Pertemuannya sejajar','Batas putar disebut shear line.', 'aligned',6,'Pada kunci yang cocok, pertemuan pin bawah dan pin atas semuanya tepat berada di batas putar, atau shear line.'),
('Satu pin terlalu rendah','Pin atas masih menghalangi.', 'low',6,'Satu gerigi terlalu rendah? Pin atas masih melintasi batas itu. Inti tetap tidak bisa berputar.'),
('Terlalu tinggi juga terhalang','Kini pin bawah melintasi batas.', 'high',6,'Kalau terlalu tinggi, justru pin bawah yang menyeberang ke rumah kunci. Mengangkat lebih tinggi bukan berarti lebih cocok.'),
('Kini inti bisa berputar','Pin bawah ikut; pin atas tinggal.', 'turn',6,'Saat semuanya sejajar, inti dan pin bawah dapat berputar bersama anak kunci. Pin atas tetap di dalam rumah.'),
('Pegas tetap di rumah','Bagian yang berputar sudah terpisah.', 'rotated',5,'Pegas juga tetap di atas. Pemisahan pada batas tadi membuat rumah tidak ikut terseret saat inti berputar.'),
('Putaran diteruskan','Inti terhubung ke penggerak belakang.', 'cam',5,'Di belakang inti, penggerak meneruskan putaran ke mekanisme pengunci pintu. Bentuk sambungannya bisa berbeda antarproduk.'),
('Kembali ke posisi awal','Ruang pin kembali bertemu.', 'return',6,'Untuk mencabut anak kunci, inti dikembalikan ke posisi pelepasan. Pada contoh ini, ruang pin kembali sejajar.'),
('Kunci keluar, pin turun','Pegas mengembalikan penghalang.', 'withdraw',5,'Ketika anak kunci ditarik, pegas menurunkan pin lagi. Batas putar kembali terhalang.'),
('Bentuk kecil, syarat serentak','Semua pasangan harus tepat bersama.', 'summary',6,'Jadi, gerigi bukan cuma pola. Bentuknya menyetel beberapa pin sekaligus, agar satu inti bisa berputar.')]
short=[
'Kunci bisa masuk, tapi kenapa belum tentu bisa diputar? Jawabannya ada pada pin-pin di dalamnya.',
'Pada silinder kunci pin konvensional, gerigi anak kunci harus menyelaraskan semua pasangan pin, bukan sekadar masuk.',
'Bagian luar adalah rumah kunci. Di dalamnya ada inti yang bisa berputar, dengan lubang anak kunci.',
'Setiap ruang berisi pin bawah, pin atas, dan pegas. Panjang pin bawah mengikuti kedalaman gerigi pasangannya.',
'Tanpa anak kunci, pegas mendorong pin turun. Pin atas melintasi batas inti dan rumah, sehingga putaran terhalang.',
'Saat kunci masuk, geriginya mendorong pin bawah. Pin atas ikut naik, dan pegas di atasnya tertekan.',
'Gerigi lebih tinggi dipasangkan dengan pin bawah lebih pendek. Gerigi lebih rendah memakai pin lebih panjang.',
'Pada kunci yang cocok, semua pertemuan pin bawah dan pin atas tepat di batas putar, atau shear line.',
'Satu gerigi terlalu rendah? Pin atas masih melintasi batas itu. Inti tetap tidak bisa berputar.',
'Terlalu tinggi? Justru pin bawah menyeberang ke rumah. Lebih tinggi bukan berarti lebih cocok.',
'Saat semuanya sejajar, inti dan pin bawah berputar bersama anak kunci. Pin atas tetap di rumah.',
'Pegas juga tetap di atas. Pemisahan tadi membuat rumah tidak ikut berputar.',
'Penggerak belakang meneruskan putaran ke mekanisme pengunci pintu. Bentuk sambungannya berbeda antarproduk.',
'Untuk mencabut kunci, inti dikembalikan ke posisi pelepasan. Pada contoh ini, ruang pin kembali sejajar.',
'Saat kunci ditarik, pegas menurunkan pin lagi. Batas putar kembali terhalang.',
'Gerigi bukan cuma pola. Bentuknya menyetel beberapa pin sekaligus, agar satu inti bisa berputar.'
]
rows=[(*r[:4],short[i]) for i,r in enumerate(rows)]
scenes=[];t=0
for i,(title,sub,view,dur,vo) in enumerate(rows):
    scenes.append(dict(id=f'lock-{i+1:02}',number=i+1,title=title,subtitle=sub,view=view,start=t,duration=dur,vo=vo));t+=dur
assert t==90
(V/'scene-plan.json').write_text(json.dumps(dict(duration=90,scenes=scenes),ensure_ascii=False,indent=2),encoding='utf-8')
(V/'assets/fonts').mkdir(parents=True,exist_ok=True)
for f in ['manrope.ttf','ibm-plex-mono.ttf','Manrope-OFL.txt','IBM-Plex-Mono-OFL.txt']:
    shutil.copy2(R/'boards/di-balik-benda/assets'/f,V/'assets/fonts'/f)
shutil.copy2(R/'boards/di-balik-benda/frame.md',V/'frame.md')
(V/'capture/extracted').mkdir(parents=True,exist_ok=True)
(V/'capture/extracted/visible-text.txt').write_text((V/'BRIEF.md').read_text(encoding='utf-8'),encoding='utf-8')
(V/'capture/extracted/tokens.json').write_text(json.dumps(dict(title='Di Balik Benda: silinder kunci',description='A conventional pin-tumbler operating cycle',colors=['#ECEEE9','#172B3B','#C94422','#2459C4','#167580'],fonts=['Manrope','IBM Plex Mono'])),encoding='utf-8')
script=f'# SCRIPT — Why the key can turn\n\n**Voice:** ElevenLabs {voice}, eleven_v4\n\n**Voice direction:** Curious, plain Indonesian, careful at the shear-line explanation. Agent-verified under delegated automation; no human approval claimed.\n'
for s in scenes:script+=f'\n## Line {s["number"]} — {s["title"]} (Frame {s["number"]})\n\n**Time:** {s["start"]}–{s["start"]+s["duration"]}s (estimated)\n\n    {s["vo"]}\n'
(P/'SCRIPT.md').write_text(script,encoding='utf-8');(V/'SCRIPT.md').write_text(script,encoding='utf-8')
text='\n\n'.join(('[curious, conversational] ' if i==0 else '[slow down, explain precisely] ' if i==7 else '[clear, concluding] ' if i==15 else '')+s['vo'] for i,s in enumerate(scenes))
(V/'audio_request.json').write_text(json.dumps(dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=resolution,tts_model='eleven_v4',speed=1,lines=[dict(id='narration',text=text)],bgm=dict(mode='none')),ensure_ascii=False,indent=2),encoding='utf-8')
board='''---
format: 1080x1920
duration: 90s
message: "A correct key aligns every pin-pair split with the plug boundary."
arc: question → anatomy → constraint → alignment → rotation → output → reset
audience: curious Indonesian viewers
mode: autonomous
music: none
---

## Video direction

Original non-scale shaded SVG sections, Manrope and IBM Plex Mono, inherited Di Balik Benda v3. Stable landmark: blue third pin chamber. Input orange, inspected contact blue, output teal. Caption keep-out: 1500–1740px; all essential graphics above 1430px. No decorative grid or camera orbit. Side section, single-stack macro, profile comparison and end-on cut give different information. Cut transitions preserve state; low/high cases are explicitly separate examples. Mechanical motion uses svg-icon-enrichment and control-target-sync; deliberate observation holds replace ambient loops. Blueprint: compose throughout.

Execution: static storyboard artifacts are mandatory under the production pipeline; agent verifies them before audio and motion. Native delegation is not granted; execute frame-worker fallback serially. No fabricated human approvals.
'''
purposes=['Pose the familiar question with exterior keyway','State the exact conventional variant and alignment thesis','Distinguish stationary shell and rotating core','Expose contact and spring relationship within one chamber','Show physical obstruction at the plug boundary','Follow the entering key surface and coupled pins','Explain complementary lengths rather than arbitrary shapes','Show all splits aligned on the same constraint','Show an upper pin blocking a low-key case','Show a lower pin blocking a high-key case','Turn the rigid plug, key and lower pins together','Isolate fixed upper pins and springs while plug stays rotated','Trace output rotation to the rear cam','Return to the withdrawal position without moving the shell','Show spring-driven reset during withdrawal','Reconnect the shape to the whole operating principle']
for s,why in zip(scenes,purposes):
    board+=f'\n## Frame {s["number"]} — {s["title"]}\n\n- status: built\n- src: compositions/frames/{s["id"]}.html\n- duration: {s["duration"]}s\n- start: {s["start"]}s\n- transition_in: cut\n- scene: {why}\n- voiceover: "{s["vo"]}"\n- poster: {s["duration"]*.6:.2f}s\n- blueprint: compose\n- motion: svg-icon-enrichment, control-target-sync\n- focal: original {s["view"]} cylinder illustration\n- roles: mechanism foreground; annotation supporting; pale bench background\n- evidence: SOURCES.md C1–C7\n\nNarrative role: {why}. On-screen copy: {s["title"]}; {s["subtitle"]}.\n\nState continuity: {s["view"]}; same blue third chamber and orange key persist across side views. Anatomical or low/high comparison cuts are marked as an explanatory view.\n\nScene 1 (0–0.6s): establish the composed {s["view"]} view; title legible at entry.\nScene 2 (0.6–{s["duration"]*.78:.2f}s): expose the named relationship and animate its causal action to the narration; do not replay an unrelated operating loop. Diagnostic poses: before input → intermediate contact/constraint → resulting state.\nScene 3 ({s["duration"]*.78:.2f}–{s["duration"]}s): hold the resulting state for inspection; preserve it into the next causal view. Rhythm: {"longer contact inspection" if s["view"] in ["blocked","insert","aligned","low","high","turn"] else "orientation or causal handoff"}.\n'
(V/'STORYBOARD.md').write_text(board,encoding='utf-8')
sources='''# Sources and claim boundaries

Research date: 2026-10-24. Discovery and extraction used Tavily CLI; query-focused extraction flags failed validation, then plain extraction succeeded. Source excerpts support the claims below; the script is original Indonesian paraphrase. No source image is reproduced.

## Evidence

1. Schlage, Rekeying Quick Start Guide, manufacturer reference: https://www.schlage.com/content/dam/sch-us/documents/pdf/installation-manuals/P513-325.pdf . Glossary defines cylinder, plug, bottom pin, pin-tumbler mechanism and simultaneous alignment by correctly cut key; rotating plug drives tailpiece/drive mechanism.
2. Schlage, Key Systems, Cylinders and Keys catalog, manufacturer glossary: https://commercial.schlage.com/content/dam/allegion-us-2/web-files/schlage/information-documents/Schlage_Key_Systems_Cylinders_and_Keys_Catalog_109487.pdf . Defines bottom pin in direct contact with the key, top pin contacting its spring, body surrounding plug, and cam transferring rotation to bolt mechanism. Technical alternative models and master pins are outside this episode.
3. Lockwiki, Pin tumbler, specialist cross-check and four operating-state diagrams: https://www.lockwiki.com/index.php/Pin_tumbler . Sections Principles of operation and Components establish rest, correct key, rotated plug and incorrect-key states; fixed driver pins/springs in housing, different lower-pin lengths, cam and reset. Raw extraction retained in research-extract.json. No bypass instructions used or included.

## Claim map

| ID | Script / visual assertion | Support and limit |
| --- | --- | --- |
| C1 | Compatible keyway entry alone does not satisfy all pin heights | 1 pin-tumbler definition; 3 incorrect-key state. Says can enter, not that any key fits. |
| C2 | Stationary housing encloses rotating plug and chambers | 1 cylinder/plug; 2 body/plug; 3 operating diagrams. |
| C3 | Conventional chamber has bottom pin, upper pin and spring | 1 mechanism definition; 2 top/bottom pin definitions. Single split per chamber; no master pins. |
| C4 | Key profile lifts paired pins and compresses springs | 1 pin tumbler/key-cut alignment; 2 direct key/spring contacts; 3 component and correct-key sections. Continuous contact path is an original schematic interpretation. |
| C5 | Correct key aligns all pair splits with the shear line; too low and too high both obstruct rotation | 1 simultaneous alignment; 3 principles, historical positive-locking explanation and bad-key diagram. Relative geometry is schematic; no tolerances claimed. |
| C6 | Key, plug and lower pins rotate; upper pins and springs stay housed | 3 components, correct-key rotated state; 1 rotating plug. No longitudinal side view is falsely rotated. |
| C7 | Rear cam transfers rotation; return and withdrawal allow spring reset | 2 cam definition; 3 plug/cam/springs and no-key state. Exact downstream bolt linkage omitted; position of removal identified as this example. |

## Visual provenance and qualifications

All illustrations are original SVG. Five chambers are an illustrative conventional configuration, not a claim about every manufacturer. Geometry is not to scale. Shell removed, vertical section and end-on view are labeled. Time is slowed. Oversized clearances aid visibility; rigid parts remain rigid. Upper and lower pins remain in contact during insertion. Low and high key examples change the matching key profile with the pin height together. No branded product, strength, security guarantee, tolerance or universality claim.

Creative source: board v3 and its canonical frame.md. Manrope / IBM Plex Mono copied with their OFL licenses. Catalog search found generic exploded layers and mechanical shutter transitions, no faithful pin-tumbler mechanism; original mechanical geometry is necessary. BGM and SFX to be resolved for this operating explanation.
'''
(P/'SOURCES.md').write_text(sources,encoding='utf-8')
tracker=json.loads((R/'TRACKER.json').read_text())
next(x for x in tracker['productions'] if x['slug']==P.name).update(stage='storyboard',status='in_progress')
(R/'TRACKER.json').write_text(json.dumps(tracker,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(dict(scenes=len(scenes),duration=t,spoken_words=sum(len(s['vo'].split()) for s in scenes),voice=voice)))
