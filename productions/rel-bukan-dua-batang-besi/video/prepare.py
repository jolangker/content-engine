from pathlib import Path
import json, shutil, re, importlib.util

V=Path(__file__).resolve().parent
ROOT=V.parents[2]

rows=[
('01-dua-rel','Dua rel, selesai?', 'Kalau kamu mau bikin jalur kereta, taruh dua batang besi. Beres? Belum.', 'Rails lower onto bare soil; builder celebrates beside a folded chair.', ['Lower the rails until steel contacts soil.','Builder points at the incomplete track and lifts a thumb.']),
('02-beban','Bebannya ke mana?', 'Kereta memberi beban besar. Kalau penopangnya lemah, jalurnya bisa turun. Jadi, kita lihat apa yang bekerja di bawahnya.', 'A wheelset contacts rail; a local cutaway exposes the support chain.', ['Wheel settles onto the rail head.','A schematic load path exposes concentrated support and illustrative settlement.']),
('03-bantalan','Perlu tumpuan', 'Bantalan menopang rel dan membantu menyebarkan beban ke lapisan di bawahnya. Tapi rel juga harus terikat ke bantalan.', 'Sleepers approach in a lifted explanatory panel and broaden the support footprint.', ['Sleepers move beneath the lifted rails and meet their rail seats.','Load markers spread across sleeper width; the unsecured rail is isolated.']),
('04-penambat','Ikat ke bantalan', 'Penambat menjepit kaki rel. Sekarang rel dan bantalan bekerja bersama, bukan sekadar ditumpuk.', 'Macro rail seat with resilient pad and generic paired spring clips.', ['Pad and rail foot meet the sleeper seat.','Paired clips slide over the rail foot and hold it.']),
('05-balas','Batu yang bekerja', 'Di bawahnya, kita butuh balas: batu pecah bersudut. Batu-batunya saling mengunci dan meneruskan beban ke tanah dasar.', 'Panel is lifted for explanatory access; angular ballast is poured and contacts under the sleepers.', ['Angular stones pour into the support bed.','Macro stones meet their neighbors; schematic load continues down.']),
('06-bahu','Jangan mudah bergeser', 'Balas juga mengisi sela dan sisi bantalan, membantu menahan pergeseran. Nah, kelihatannya sudah bisa santai.', 'Stone shoulder fills beside sleeper ends; builder brings chair to a pad away from the track.', ['Shoulder stones approach and pack beside sleeper ends.','Lateral restraint is shown; builder unfolds chair on the verge.']),
('07-air','Eh, kok basah?', 'Eh, kok basah? Celah batu memang bisa melewatkan air, tapi airnya tetap perlu jalan keluar.', 'Rain reaches the ballast; a puddle interrupts the builder before he sits.', ['Water enters voids and collects where there is no outfall.','Chair foot meets puddle; builder recoils and lifts the chair.']),
('08-drainase','Beri jalan keluar', 'Jadi, dasar jalur dan saluran drainase perlu mengarahkan air ke tempat pembuangan. Bukan membiarkannya terjebak.', 'Section reveals shaped formation and the side drain with an outlet.', ['Local cutaway reveals the formation and continuous drainage route.','Blue schematic water travels from the support zone into the side drain and outlet.']),
('09-tanah','Jaga penopangnya', 'Tanah yang jenuh air bisa kehilangan kekakuan. Lapisan penyangga dan drainase harus bekerja bersama, supaya tumpuannya tetap baik.', 'Follow water to a lower outlet; return to the supported section.', ['Trapped water leaves through the lower outlet.','Schematic load reaches the formation while the support state remains continuous.']),
('10-bersihkan','Batu juga dirawat', 'Lama-lama, balas bisa kotor. Butiran halus mengisi celahnya. Karena itu, balas perlu diperiksa, dibersihkan, atau diganti.', 'Fines enter a diagnostic stone window; a cleaning screen separates debris.', ['Fine material settles into the void window.','A screen separates fines; clean angular stones return.']),
('11-tamping','Rapikan tumpuannya', 'Kalau tumpuan berubah, mesin tamping memadatkan balas di bawah bantalan untuk membantu mengembalikan geometri jalur.', 'A simplified maintenance head lifts the panel; tines insert and squeeze beneath sleeper.', ['Maintenance head raises the rail/sleeper panel for correction.','Tines insert and squeeze ballast beneath the sleeper, then withdraw.']),
('12-utuh','Setiap bagian ada alasannya', 'Pada jalur berbalas, rel, bantalan, batu, tanah dasar, dan drainase adalah satu sistem. Sekarang, kursinya boleh dipakai.', 'Pull back to completed route; train passes while builder sits behind the fence on a dry paved pad.', ['A wheel load passes through the completed supported track.','Builder lowers onto the dry chair away from the railway; the opening confidence pays off.']),
]
plan=[]
total_words=sum(len(r[2].split()) for r in rows)
cursor=0
for i,(id,title,vo,purpose,steps) in enumerate(rows):
    duration=90*len(vo.split())/total_words
    plan.append(dict(id=id,title=title,vo=vo,purpose=purpose,steps=steps,start=cursor,duration=duration,end=cursor+duration))
    cursor+=duration
def write_json(name,obj): (V/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write_json('scene-plan.json',plan)
(V/'scene-data.js').write_text('window.RAIL_PLAN='+json.dumps(plan,ensure_ascii=False)+';\nwindow.RAIL_DURATION=90;\n',encoding='utf-8')
for f in ['assets/fonts','assets/audio','vendor','compositions/frames','boards/stills','verification','capture/extracted']:(V/f).mkdir(parents=True,exist_ok=True)
for name in ['barlow-bold.ttf','barlow-black.ttf','barlow-regular.ttf','ibm-plex-mono.ttf','Barlow-OFL.txt','IBM-Plex-Mono-OFL.txt']:
    shutil.copy2(ROOT/'boards/bongkar-sistem/assets'/name,V/'assets/fonts'/name)
shutil.copy2(ROOT/'boards/bongkar-sistem/frame.md',V/'frame.md')
for name in ['three.module.js','three.core.js','gsap.min.js']:
    shutil.copy2(ROOT/'productions/hujan-bukan-sekadar-ember/video/vendor'/name,V/'vendor'/name)
(V/'capture/extracted/visible-text.txt').write_text('$shortform-production --board=bongkar-sistem --topic=auto --until=export --automation\nSelected: conventional ballasted railway support and drainage.\n',encoding='utf-8')
write_json('capture/extracted/tokens.json',dict(title='Rel bukan dua batang besi',description='Setiap lapisan di bawah rel punya tugas.',colors=['#173B42','#CCA84F','#3C6261'],fonts=['Barlow','IBM Plex Mono']))
script='# Narration v1\n\nAgent-selected under delegated automation; human approval false. Native speed, estimated 90 seconds.\n\n'
for s in plan:script+=f"## {s['id']}\n\n{s['vo']}\n\n"
(V.parent/'SCRIPT.md').write_text(script,encoding='utf-8');(V/'SCRIPT.md').write_text(script,encoding='utf-8')
sb='''---
format: 1080x1920
duration: 90s
message: "Setiap lapisan di bawah rel punya tugas."
arc: incomplete attempt -> support -> restraint -> drainage -> maintenance -> whole
audience: curious Indonesian viewers
mode: autonomous
music: none
---

## Video direction

Board Bongkar Sistem v2. Twelve shots contain 24 meaningful steps. One persistent original 3D rural worksite with material variation, a worker of adult proportions, yellow cap and teal work shirt. Maintain the same track axis and completed component states. A majority of shots travel inside the shot: dolly inward, track the transfer, crane to a section, withdraw to the working whole. Settle around contact. Captions stay at y=1180–1320; labels above the hero with leader lines where needed. No blank pedestal, no infographic slide, no recurring ambient zoom. Camera and objects are pure functions of seek time. Orange force and blue flow notation are schematic, never measured simulation.

Static poses are required before audio/animation by project override, verified by the agent. Narration uses one continuous full-script ElevenLabs eleven_v4 request; no workflow provider fallback. Foley marks material actions; no BGM to preserve the narrative's contacts. Listening status must remain honest.

'''
for i,s in enumerate(plan):
    sb+=f"## Frame {i+1} — {s['title']}\n\n- status: outline\n- src: compositions/frames/{s['id']}.html\n- duration: {s['duration']:.3f}s\n- poster: {s['duration']*.68:.3f}s\n- transition_in: cut\n- scene: {s['purpose']}\n- voiceover: {s['vo']}\n- narrativeRole: Develop the supported reason for the next part.\n- type: problem-solution\n- asset_candidates: []\n- motion: anticipation, purposeful camera travel, physical contact, readable hold\n\n"
    sb+=f"Scene 1 (0–{s['duration']*.48:.2f}s): {s['steps'][0]} Camera moves from contextual approach to action detail; settles before contact.\n\nScene 2 ({s['duration']*.48:.2f}–{s['duration']:.2f}s): {s['steps'][1]} Follow consequence then hold 0.6s. Focal: the actual component or character action; full-screen setting continues.\n\n"
(V/'STORYBOARD.md').write_text(sb,encoding='utf-8')
(V/'SPEC.md').write_text('''# Director specification

GOAL: The viewer can follow a wheel load into the ground and explain why ballast and drainage both matter.
OUTPUT: HyperFrames 1080x1920, 30 fps, H.264/AAC. Estimated 90s; measured narration replaces estimates.
LOOK: Continuous daylight rural railway worksite beyond every frame edge. Soil #75604A, grass #52684A, steel #8E9997, teal #3C6261, yellow #CCA84F. MeshStandardMaterial roughness 0.45–1.0; metalness 0–0.7. Key + hemisphere fill + cool rim. Modest construction bevels, concrete/ground procedural texture. No floating earth slab. Adult worker height 1.76 world units, shoulder width 0.48, head height 0.24.
TYPE: Local Barlow 900 titles 72px, 700 captions 58px with 1.1 leading; label 34px. Safe x 72–930; identity at y190; titles y240; captions y1180–1320. Board cream caption material and yellow/teal identity are inherited exceptions to generic style bans.
OBJECTS: I-profile steel rails, tapered concrete sleepers, dark rail pads, paired generic steel spring clips, angular stone aggregate, soil formation, open side drain and lower outlet, rain, cleaning screen, tamping head/tines, wheelset and completed train, worker, folding chair, paved pad, fence, houses, road, trees, poles.
MOTION: Smoothstep camera dolly/track/crane over first 60–80% of shot, settle at critical contact. Part approach 0.6–1.1s and contact hold 0.4–0.8s. Secondary body parts follow primary pose by 0.12s. No continuous bouncing or zoom across every shot. World and camera computed from scene-local time; seeded object placement.
SHOTS: scene-plan.json and STORYBOARD.md are the 12-shot / 24-step authority. Every shot supplies two useful developments, and narrative order is an explanatory reconstruction, not a building procedure.
BANNED: isolated pedestal, empty color moat, cartoon infant proportions, tiny invisible contacts, component pop-in already installed, fabricated failure, measurement-looking force arrows without schematic label, wall-clock animation, HUD decoration, decorative glow, floating particles, cut-only camera language, ambience-only sound coverage, claim of perceptual listening from numerical checks.
QA: All 12 static scene poses before audio; all 24 action result frames; inside-shot camera start/middle/end; phone-width proof; cut adjacency; final decoded export; SFX event-to-cue and audio checks. Record sound measured not heard and limitations of temporal visual inspection.
''',encoding='utf-8')
ep=V.parent/'EPISODE.md'
ep.write_text(ep.read_text(encoding='utf-8')+'''\n## Hook and script selection

1. Selected: “Kalau kamu mau bikin jalur kereta, taruh dua batang besi. Beres? Belum.” Incomplete attempt directly motivates the support chain.
2. “Kereta yang berat itu sebenarnya ditahan oleh apa?” Load-journey question.
3. “Batu di bawah rel bukan sekadar pengisi.” Stones-only myth.

Presented before drafting. Hook 1 selected by agent under --automation, with claim boundaries in SOURCES.md. SCRIPT.md v1 is agent-verified for 12 shots and 24 developments, not human-approved. Updated HyperFrames CLI 0.8.196 reports that faceless-explainer is retired into the main HyperFrames references; current explainer/3D/character/vertical/story/spec/review instructions govern execution. No native delegation used; implementation is sequential. HeyGen signed out; workspace ElevenLabs policy takes precedence over workflow offline fallback.\n''',encoding='utf-8')
print(json.dumps(dict(scenes=len(plan),steps=24,spoken_words=total_words)))
