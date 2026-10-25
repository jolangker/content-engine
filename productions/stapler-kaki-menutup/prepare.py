from pathlib import Path
import json, shutil, hashlib, importlib.util

P=Path(__file__).resolve().parent; R=P.parents[1]; V=P/'video'
def write(p,s):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(s.rstrip()+'\n',encoding='utf-8')
def js(p,x): write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

brief='''---
workflow: hyperframes
legacy_route: faceless-explainer
flow: automation
storyboard: no
mode: autonomous
message: "Bilah mendorong; alur landasan menekuk kaki staples."
destination: instagram-reels
aspect: 1080x1920
language: id
length: 90s
angle: how-it-works
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
pre_render_authorization: delegated by the user's --automation instruction
delivery: queue
endpoint: publishing
---

## Intent
Follow one staple through a direct-action manual desktop stapler with stationary inward-clinching anvil. Explain feed, cover actuation, guided blade, penetration, constrained plastic bending, and spring return. General Indonesian audience; curious precise guide, no repair advice.

## Assets
Inherited Di Balik Benda v4 frame.md and bundled fonts, original shaded layered SVG mechanisms, project-root default ElevenLabs voice with eleven_v4. Reuse suitable tactile and editorial SFX; intentional no music so small contact cues remain distinct.

## Customizations
90 seconds at 30 fps, 16 explanatory shots. 2.5D illustration throughout; two useful detail views (feed channel and transverse clinching section). Original geometry is schematic, not to scale; removed shell and slowed/replayed action are labelled. All causal interactions get visible approach/contact/response and event sound. Preserve active blue blade and front guide landmark.

## Notes
Full pre-audio static storyboard stills, HTML, and PNG are required despite storyboard:no, under shortform-production's project override. Agent verification replaces human checkpoints; no human approval is claimed. Queue every inherited account: only Instagram dibalikbenda.id in Admin's Workspace. Use its next configured slot, no explicit due time. New CLI 0.8.199 retires faceless-explainer into consolidated HyperFrames; use current explainer/story/spec/format/review references. Commit only this production and its tracker row; preserve unrelated starting changes.
'''
write(V/'BRIEF.md',brief)
shutil.copy2(R/'boards/di-balik-benda/frame.md',V/'frame.md')
for name in ['manrope.ttf','Manrope-OFL.txt','ibm-plex-mono.ttf','IBM-Plex-Mono-OFL.txt']:
    (V/'assets/fonts').mkdir(parents=True,exist_ok=True)
    shutil.copy2(R/'boards/di-balik-benda/assets'/name,V/'assets/fonts'/name)

sentences=[
('Siapa yang menekuk?','Kita menekan dari atas. Tapi siapa yang menekuk kaki staples di bawah kertas?','whole'),
('Ikuti satu staples','Kita ikuti stapler manual biasa, dengan kaki staples yang dilipat ke dalam.','whole'),
('Cangkang dibuka','Di dalamnya ada magazen, pengumpan berpegas, dan bilah penekan di ujung depan.','explode'),
('Selalu ke depan','Pengumpan menekan deretan staples ke depan, sampai staples pertama berada di jalur bilah.','feed'),
('Satu jalur keluar','Jalur sempit ini menuntun staples pertama saat didorong turun. Sisanya tetap di magazen.','feed'),
('Tekanan diteruskan','Saat kepala ditekan, lengan berputar pada engsel belakang dan magazen mendekati kertas.','side'),
('Bilah menyentuh','Bilah logam kemudian menekan punggung staples pertama, meneruskan gaya tangan ke kawat.','side'),
('Dua kaki menembus','Kedua kaki yang masih lurus menembus lembaran kertas. Belum terlipat menjadi pengunci.','front'),
('Bertemu landasan','Di bawah kertas, ujung kakinya mencapai alur pada pelat logam, yang disebut landasan.','front'),
('Alur mengubah arah','Tekanan berlanjut. Permukaan alur mengarahkan ujung kaki ke dalam sambil kawat menekuk.','clinch'),
('Bukan ditarik dari bawah','Landasannya tidak perlu bergerak. Bilah tetap mendorong dari atas, alur membelokkan kaki.','clinch'),
('Kertas kini terikat','Punggung staples tertahan di atas. Kaki yang terlipat menahan lembaran dari bawah.','result'),
('Bilah naik kembali','Saat tangan dilepas, pegas mengembalikan mekanisme penekan. Bilah naik dan jalur depan terbuka.','side'),
('Staples berikutnya maju','Pengumpan berpegas memajukan deretan staples lagi, menempatkan staples berikutnya di bawah bilah.','feed'),
('Ulangi satu siklus','Sekarang lihat utuh: tekan, tembus, tekuk, lalu kembali siap. Gerak cepatnya kita perlambat.','cycle'),
('Dorong, lalu bentuk','Jadi, bilah mendorong staples. Bentuk alur landasanlah yang menentukan tekukan kakinya.','result')]
duration=[6,4.5,6,5.5,5,5,5,6,5,7,6,5,6,5,7,6]
assert sum(duration)==90
sc=[];t=0
for i,((title,text,view),d) in enumerate(zip(sentences,duration)):
    sc.append(dict(id=f's{i+1:02}',title=title,text=text,view=view,start=t,end=t+d,duration=d))
    t+=d
js(V/'scene-plan.json',sc)
hooks=[{'line':sentences[0][1],'angle':'Hidden actor under a familiar action; chosen: direct payoff at the anvil.'},{'line':'Satu staples masuk. Staples berikutnya langsung siap. Apa yang mengaturnya?','angle':'Automatic feed, less direct to the strongest macro.'},{'line':'Kawat lurus ini berubah jadi pengunci kertas. Ikuti perjalanannya.','angle':'Material journey, clear but less curiosity.'}]
accounts=json.loads((R/'boards/di-balik-benda/ACCOUNTS.json').read_text())
episode='''# Stapler: siapa yang menekuk kakinya?

- Board: [Di Balik Benda v4](../../boards/di-balik-benda/DIRECTION.md), [editorial](../../boards/di-balik-benda/EDITORIAL.md), [visual specification](../../boards/di-balik-benda/frame.md).
- topic_selection: auto, explicitly delegated by --topic=auto.
- execution_policy: automation; automation_after: none; automation_state: active; human_review: none.
- pre_render_authorization: delegated by the user's --automation instruction.
- Requested endpoint: publishing; delivery: queue; schedule: next configured account slot, Asia/Jakarta (daily 10:00); no custom --at.
- Audience/language/output: curious general audience, Indonesian, 1080x1920, 30 fps, 90 seconds.
- Scope: one direct-action manual desk-stapler cycle, stationary inward-clinching anvil. Not a spring-powered release stapler, flat-clinch moving anvil, or staple gun.
- Audio: ElevenLabs eleven_v4, default voice resolved only from root .env; tagged full-script request. Event SFX required, no BGM to separate fine contact cues from speech.
- Medium: board-v4 2.5D only; original editable SVG with side faces, metal shading, consistent light, layer order; stationary base and anvil. Labels and force arrows are flat support.
- Storyboard override: pre-audio styled stills + HTML + full PNG required; agent verification, no human approval.
- Mechanical source limitations: schematic geometry, enlarged wire/clearance, compressed depth; not a measured product replica. Same variant throughout. Anvil groove angles and sheet capacities are not claimed.

## Topic decision
Candidates: stapler cycle; bicycle pawl freehub; reversible socket ratchet; automatic umbrella; mechanical kitchen timer; manual can opener; hydraulic door closer; inertial seatbelt reel; soap dispenser; crank pencil sharpener.
Chosen stapler balances feed/rotation/translation/penetration/plastic bending/return, primary patent support and a legible 90-second cycle. Freehub/ratchet concentrate on tooth contact; umbrella/timer need more variant geometry; door closer/seatbelt need tighter variant and domain boundaries; soap pump overlaps sprayer. Other candidates remain evidence leads, not verified scripts.
Overlap: tracker read, all production folders inspected including orphan roda-beda-putaran (no EPISODE.md). Prior board episodes cover lockstitch, cylinder lock, trigger sprayer and toilet cistern; none covers stapler. Historical v1 pen/zipper/clothespin/cable tie also differ. No related production overwritten.

## Hook selection
'''
for i,h in enumerate(hooks,1):episode+=f'{i}. {h["line"]} — {h["angle"]}\n'
episode+='\nSelected 1 under delegated automation, after source verification and before drafting SCRIPT.md.\n\n## Publishing targets\n```json\n'+json.dumps({'source':'board','board_accounts_file':'boards/di-balik-benda/ACCOUNTS.json','board_accounts_sha256':sha(R/'boards/di-balik-benda/ACCOUNTS.json'),'accounts':accounts['accounts']},indent=2)+'\n```\n\nPreflight: exact workspace/account connected; caller publishes directly; instagram_reel permits 900 s / 300 MiB, max 5 hashtags, 2200 characters. Queue schedule configured daily 10:00 Asia/Jakarta. Live tools read before synthesis.\n\n## State\nBrief/research/script agent-verified. Storyboard in progress. No preview server started. Starting unrelated changes: TRACKER.json includes gua-kira-udah-kelihatan and that production directory is untracked; exclude from requested commit.\n'
write(P/'EPISODE.md',episode)
write(P/'SOURCES.md','''# Evidence and claim boundaries

Sources read with Jina on 2026-10-26. These are operation evidence, not creative geometry references. Original illustrations only.

| ID | Claim / visual relation | Evidence and limitations |
| --- | --- | --- |
| C1 | Pivoted cover, magazine, base; spring-biased pusher advances staple stick; driver blade drives and returns | [US4666075A, Swingline, Stapler mechanism](https://patents.google.com/patent/US4666075A/en): description of parts 11–18, 21–32, 40–52, figures 1,4–7. Specific cover/pusher arrangement is not universal. Episode shows functional schematic, not exact assembly. |
| C2 | Front staple sits below blade in a guiding passage; pusher bias feeds front; pressing driver expels foremost staple | [US2702384A, Stapling machine](https://patents.google.com/patent/US2702384A/en): magazine M, follower SP, spring ES, guide gaps 15, blade DB; figs 7–12 and assembled operation. Its extendible follower spring is not represented as a generic compression coil; episode uses a labelled spring-bias symbol. |
| C3 | Anvil grooves receive legs after penetration; continued downward driver force bends legs inward | [US6244491B1, Hand held stapler](https://patents.google.com/patent/US6244491B1/en): description of stationary grooved anvil and initial inward deflection. Patent includes a particular later groove geometry and leverage construction; no dimensions, capacities, angles, or exact groove cross-section are transferred. |
| C4 | Common inward-clinching configuration; some reversible plates support outward pinning, outside episode | [Salco / Staple Headquarters: Why Do Staplers Have Two Settings?](https://www.stapleheadquarters.com/why-do-staplers-have-two-settings): describes grooves and inward versus outward result, independent cross-check for C3. Not all staplers have reversible anvils. |

## Mapping
Shots 1–3: C1–C4; 4–7: C1,C2; 8–12: C3,C4; 13–14: C1,C2; 15–16: combined bounded cycle. The voice gives no sheet-count, force or speed figures. The two legs in a frontal schematic are offset slightly in depth in the oblique result view, avoiding a false claim that their tips must collide or overlap. The leg bending is continuous material deformation, not rigid hinge rotation.

## Simplifications
Metal thickness, clearances and wire diameter enlarged for phone readability. Removed shell, exploded spacing, schematic front section and slow replay are visibly identified. Paper, anvil and driver keep consistent spatial roles. The wire's above-paper segment remains straight while the emerging length bends along the anvil; the anvil does not rise to meet it. The pusher advances only after blade clearance. Sounds are reused illustrative/editorial cues, not recorded acoustic evidence of this mechanism.
''')
script='# Locked narration and screen copy\n\nAgent-selected hook 1; source-bounded under automation. Estimated duration 90 s; measured timing will replace estimates. Captions are spoken words only.\n\n'
for s in sc:script+=f'## {s["id"]}: {s["start"]:g}–{s["end"]:g}s\n\n**Narration:** {s["text"]}\n\n**On screen:** {s["title"]}\n\n'
write(P/'SCRIPT.md',script);write(V/'SCRIPT.md',script)
write(V/'STORYLINES.md','''# Storyline selection
Five seeds: follow one staple through a cycle; begin underneath the paper; reverse from finished binding; compare with/without anvil; let the pusher guide the tour.

1. Selected: follow one staple. Familiar stack of papers on a mineral workbench; whole object → shell reveal → channel → transverse clinch macro → reset. First two seconds: whole shaded stapler with paper and downward force cue, question visible. Hook → feed → drive → form → reset → whole answer. Manrope, mineral/ink and satin metal. Narration plus quiet material cues, no score.
2. Reverse investigation: begin on finished folded legs and trace backward through the paper to the head, then return to the result. Reverse camera form, same bounded mechanics; rejected because sequence risks reversing causality.
3. Anvil counterfactual: one stroke with base removed for inspection, stop before bending, then restore landasan to explain the missing constraint. Matched comparison form; rejected because no-base operation can suggest a different fastening mode and costs observation time.
''')
write(V/'SPEC.md','''GOAL: Viewer can distinguish downward driving by the blade from bending by stationary anvil grooves.
OUTPUT: HyperFrames 1080x1920, 30 fps, 90x30 = 2700 frames.
LOOK: canvas #ECEEE9, paper #F8F9F5, ink #172B3B, input #C94422, active #2459C4, result #167580; metal #A6B4BE. Manrope 800 at 78px titles, Manrope 600 at 43px captions, IBM Plex Mono 32px annotations. Minimum horizontal key-text inset 108px; captions at y=1480–1660, no platform-edge text.
OBJECTS: manual stapler with rear hinge, bowed cover, channel magazine, front driver, U-wire strip, follower, fixed metal anvil and layered paper. Original SVG side faces offset 18–30px, upper-left highlight, 2.5D only; no WebGL or true 3D.
MOTION: physical approach power2.inOut 0.8–1.7s; contact linear/power1.in 0.3–0.8s; return power2.out 0.7–1.2s. SVG state proxy derived only from local paused timeline. Camera static during decisive contact; all handoffs preserve blade/front-mouth landmark. Changed-state holds 0.5–1.5s; no ambient loops.
SHOTS: scene-plan.json and STORYBOARD.md own exact shot ranges. 16 shots with whole, layer reveal, feed macro, side actuation, transverse wire deformation, underside result and coordinated cycle.
BANNED: floating cards, gear icons standing in for parts, generic UI clicks as recorded mechanism foley, 3D orbit, flat standalone diagram scene, whole-scene shakes, elastic steel, moving stationary anvil, resetting the same loop under new labels, subtitles in platform chrome.
QA: all storyboard stills; multiple poses at penetration/first anvil contact/bending/return/feed; reverse seeking; phone-width caption proof; 2700-frame decode and sound cue export matching. Auditory listening unavailable: report as measured, not heard.
''')
spec=importlib.util.spec_from_file_location('narration',R/'.agents/skills/shortform-production/scripts/narration.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
voice,res=mod.resolve_voice(R)
text='[curious, clear] '+sentences[0][1]+' [explaining calmly] '+' '.join(s[1] for s in sentences[1:8])+' [slightly slower, precise] '+' '.join(s[1] for s in sentences[8:12])+' [clear, conclusive] '+' '.join(s[1] for s in sentences[12:])
js(V/'audio_request.json',{'provider':'elevenlabs','lang':'id','voice':voice,'voice_resolution':res,'tts_model':'eleven_v4','speed':1.0,'lines':[{'id':'narration','text':text}],'bgm':{'mode':'none'}})
track=json.loads((R/'TRACKER.json').read_text());assert not any(x['slug']==P.name for x in track['productions'])
track['productions'].append({'slug':P.name,'topic':'Manual desktop stapler: spring-biased staple feed, guided driver, paper penetration, stationary inward-clinching anvil and return','board':'di-balik-benda','stage':'storyboard','status':'in_progress','path':'productions/'+P.name});js(R/'TRACKER.json',track)
print(json.dumps({'scenes':len(sc),'words':sum(len(s['text'].split()) for s in sc),'duration':t,'voice':voice}))
