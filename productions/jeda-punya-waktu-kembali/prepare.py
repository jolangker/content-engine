from pathlib import Path
import hashlib, importlib.util, json, shutil

B=Path(__file__).resolve().parent; R=B.parent.parent; V=B/'video'
def w(p,s): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding='utf-8')
def dump(p,x): w(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

brief='''---
workflow: faceless-explainer
flow: automation
storyboard: no
mode: autonomous
message: A requested pause needs a shared plan to return and actual follow-through.
destination: Instagram Reels
aspect: 1080x1920
language: Indonesian
audience: Indonesian adults in close relationships
length: 90s
angle: story-explainer with how-to
narration: yes
board: ruang-di-antara
board_revision: v1.2 / 2026-10-21
delivery: draft
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
pre_render_authorization: delegated by the user's --automation instruction
---

## Intent
User: `$shortform-production --board=ruang-di-antara --topic=auto --delivery=draft --automation`; `commit setelah pipeline selesai`.
Topic delegated and selected: Jeda punya waktu kembali. Explain the fictional moment of an argument paused with an indefinite “nanti,” then offer a shared return agreement and observable follow-through. Do not diagnose withdrawal, infer motives, prescribe a universal break length, or promise conflict resolution.

## Assets
Inherit ../../../boards/ruang-di-antara/frame.md and components/, Newsreader/DM Sans fonts and licensed material SFX. No B-roll. Resolve root .env voice using the maintained narration entry point; ElevenLabs eleven_v4, one continuous native-speed request.

## Customizations
Exactly 16 compositions; 14 cream, 2 charcoal (04: unfinished conversation; 12: returning in action). Full spoken captions, selective emphasis, organic faceless participants. Static storyboard artifacts including boards/storyboard.png are required before audio synthesis, overriding the autonomous sketch skip. Agent verification replaces the human layout checkpoint.

## Notes
Explicit: board, auto topic, automation, draft endpoint, commit after completion.
Inferred from board: ~90s, 1080x1920/30fps, Indonesian lo–gua, illustrated interactions. Selected under delegation: topic/angle, hook 1, narrative props. No music bed: let the pause and re-entry remain audible; sparse material SFX mark only actual actions. No temporary preview retained after export verification.
Integration check: short on-screen emphasis and independent captions leave room for the 16 illustrated actions at phone scale. Clock 20:00 is fictional scheduling dialogue, never an empirically prescribed interval.
'''
w(V/'BRIEF.md',brief)
lines=[
('Nanti itu kapan?', 'Dia bilang, nanti kita bahas. Lo jadi lebih tenang, atau malah bingung: nanti itu kapan?'),
('Ada waktu kembali.', 'Jeda bisa memberi ruang buat menenangkan diri. Obrolannya tetap perlu punya waktu kembali.'),
('Mulai memanas.', 'Misalnya, kalian membahas rencana yang berubah. Nada mulai naik, dan jawaban makin pendek.'),
('Masih tertunda.', 'Satu orang pergi. Yang lain masih duduk dengan pertanyaan yang belum selesai.'),
('Belum tahu.', 'Lo mungkin butuh tenang. Dia mungkin belum tahu apakah percakapan ini bakal dilanjutkan.'),
('Tahan kesimpulan.', 'Satu jeda belum menjelaskan niat seseorang. Lihat juga cara jedanya dibicarakan.'),
('Sepakati dulu.', 'Saat suasana tenang, sepakati bagaimana kalian meminta jeda dan kembali ngobrol.'),
('Bilang kondisi lo.', 'Ketika mulai kewalahan, bilang kondisi lo dan minta waktu, tanpa menyerang.'),
('Lanjut jam delapan?', 'Gua mulai susah dengar. Gua mau tenang dulu. Kita lanjut jam delapan, ya?'),
('Waktu yang realistis.', 'Jam delapan cuma contoh kesepakatan. Pilih waktu yang realistis buat kalian.'),
('Tenangkan diri.', 'Selama jeda, lakukan hal yang menenangkan. Jangan sibuk menyusun balasan buat menyerang.'),
('Benar-benar kembali.', 'Lalu, benar-benar kembali. Kesepakatan tadi perlu kelihatan dalam tindakan.'),
('Kabari. Sepakati ulang.', 'Kalau belum siap, kabari dan sepakati ulang. Jangan membiarkan orang lain menebak.'),
('Kembali ke persoalan.', 'Pas balik, mulai dari persoalan yang tadi tertunda. Nggak harus langsung beres semuanya.'),
('Lihat tindak lanjut.', 'Kalau berulang kali nggak dilanjutkan, bicarakan pola penundaannya saat suasana lebih tenang.'),
('Kapan? Siapa mulai?', 'Jadi, kalau bilang nanti, coba lengkapi: kapan kita kembali, dan siapa yang mulai?')]
titles=['An indefinite later','The return belongs in the plan','The changed plan','The conversation remains','Two possible experiences','Suspend the verdict','Agree while calm','State the need','A concrete return request','A workable appointment','A calming interval','Return in action','Renegotiate explicitly','Resume the original issue','Notice repeated postponement','Complete the word later']
purposes=[
'Show an indefinite speech space between two people and a clock without an agreed marker.',
'Give the value early: a pause and an agreed return are part of one plan.',
'Establish a changed shared plan on a table as the illustrated argument begins.',
'One participant moves away while the unfinished shared topic stays with the other.',
'Show separate possible experiences without pretending to read motives.',
'Keep an open question beside the departing trace instead of attaching a verdict.',
'In a calm two-shot, both participants place a marker on a shared agreement.',
'Focus on the requester naming their own state and opening room for a pause.',
'Let a proposed time travel from the requester toward a shared clock.',
'Give both participants room to choose a realistic appointment rather than a universal interval.',
'Use a window, plant and seated silhouette to make the cooling interval concrete.',
'Bring the established participant back to the same unfinished topic.',
'An update travels before the appointment marker is moved by agreement.',
'Bring the original changed-plan card back to the shared table for discussion.',
'Make repeated pending cards visible as a pattern that can itself be discussed.',
'Complete the shared return path with time and initiation markers, then hold quietly.']
beats=[
['Two participants face the speech space','A later ribbon starts across the gap','The route stops at an empty clock','An unresolved marker remains'],
['The existing route is visible','A pause opens space between actors','A shared time marker arrives','The return route completes'],
['A table carries the original plan','A replacement card overlaps it','A speech ribbon rises','A short answer interrupts its length'],
['Both actors remain recognizable','One moves toward the edge of the conversation','The topic card stays on the table','The other actor and unresolved route hold'],
['Both actors occupy separate spaces','One space opens for calming','The other retains the question','Both possibilities stay visible without a verdict'],
['A familiar departing trace is visible','An unanswered question opens','A verdict card stops short','Attention moves to the shared speech space'],
['Two actors share a calm table','The pause signal enters','A time marker is offered','Both routes meet the agreement'],
['Requester fills the focal field','A body-state ribbon contracts','A speech space opens outward','The other participant receives the request'],
['A large shared clock anchors the frame','A request ribbon reaches it','The 20:00 proposal becomes visible','The other actor adds a reply marker'],
['A shared appointment page opens','One proposed slot is visible','Another person moves a token toward it','The two routes meet without claiming any fixed interval'],
['A participant sits beside a window','The conflict note is set aside','Space opens around the silhouette','A plant and cup settle into a quiet interval'],
['The original topic waits at the table','The returning actor moves toward it','The other actor turns toward the route','The shared route reconnects; quiet hold'],
['The original appointment remains visible','An update ribbon reaches the waiting participant','A new appointment marker is proposed','Both paths meet the revised marker'],
['The same topic card returns','Two actors sit at the shared table','A listening route opens','The card turns toward both; resolution stays open'],
['One pending card is visible','Two further pending cards accumulate','The pair turns attention to the stack','A shared speech space opens about the pattern'],
['Two participants and their shared topic remain','A time marker joins the route','An initiation marker completes the path','Both actors settle with the plan; quiet final hold']]
durations=[5,5,6,5,6,6,6,6,5,6,6,6,5,6,5,6]
scenes=[]; start=0
for i,((em,vo),title,purpose,bs,dur) in enumerate(zip(lines,titles,purposes,beats,durations),1):
    scenes.append(dict(n=i,title=title,emphasis=em,vo=vo,purpose=purpose,beats=bs,start=start,duration=dur,dark=i in [4,12]));start+=dur
dump(V/'scenes.json',scenes)
count=sum(len(x[1].split()) for x in lines)
assert 170<=count<=200,count
spec=importlib.util.spec_from_file_location('narration',R/'.agents/skills/shortform-production/scripts/narration.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
voice,resolution=m.resolve_voice(R)
tags={1:'[intimate, curious, conversational]',3:'[observant, slightly tense]',6:'[gentle, measured]',9:'[sincere, speaking directly to a partner]',11:'[calm, unhurried]',12:'[quietly firm]',16:'[warm, reflective]'}
script=f'# SCRIPT — Jeda punya waktu kembali\n\nVersion 1; agent-verified under delegated automation. {count} spoken words.\n\n**Voice:** ElevenLabs / {voice} / eleven_v4, resolved from root .env.\n**Voice settings:** Native speed 1; one continuous synthesis request.\n**Voice direction:** Intimate, observant Indonesian lo–gua. No clinical authority cadence.\n\n'
for s in scenes:
    script+=f'## Line {s["n"]} — {s["title"]} (Frame {s["n"]})\n\n**Time:** Estimated {s["start"]}–{s["start"]+s["duration"]}s; replace with measured alignment.\n**Delivery:** {tags.get(s["n"],"Continue naturally.")}\n\n    {s["vo"]}\n\n**On-screen:** {s["emphasis"]}\n\n'
w(B/'SCRIPT.md',script);w(V/'SCRIPT.md',script)
dump(V/'audio_request.json',dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=resolution,tts_model='eleven_v4',speed=1,lines=[dict(id='narration',text='\n\n'.join((tags.get(s['n'],'')+' '+s['vo']).strip() for s in scenes))],bgm=dict(mode='none')))
board=R/'boards/ruang-di-antara'
shutil.copy2(board/'frame.md',V/'frame.md');shutil.copytree(board/'components',V/'components',dirs_exist_ok=True)
shutil.copytree(board/'assets',V/'assets/board',dirs_exist_ok=True)
w(V/'capture/extracted/visible-text.txt','User invocation: $shortform-production --board=ruang-di-antara --topic=auto --delivery=draft --automation\ncommit setelah pipeline selesai\n\nSelected topic: Jeda punya waktu kembali.\n\n'+(B/'SCRIPT.md').read_text(encoding='utf-8'))
dump(V/'capture/extracted/tokens.json',dict(title='Jeda punya waktu kembali',description=brief,colors=['#F3EDE3','#302B28','#A34F3F','#D8C8B5'],fonts=['Newsreader','DM Sans']))
accounts=json.loads((board/'ACCOUNTS.json').read_text())['accounts']
episode=f'''# Jeda punya waktu kembali

## Resolved brief
Board: ruang-di-antara, approved v1.2 implementation 2026-10-21. Editorial: ../../boards/ruang-di-antara/EDITORIAL.md; visual: ../../boards/ruang-di-antara/frame.md. 1080×1920, 30fps, about 90s, sixteen illustrated scenes, two charcoal frames (04 and 12), no B-roll. Indonesian lo–gua; adults in close relationships.
Topic: An agreed pause during an ordinary disagreement, with an explicit return arrangement and actual follow-through. Fictional changed-plan scenario. Purpose: make the next conversation concrete without diagnosing the participants or promising resolution.
topic_selection: auto
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
pre_render_authorization: delegated by the user's --automation instruction
requested_endpoint: publishing
delivery: draft
schedule: none
commit: requested after pipeline completion
human_approval: none recorded

## Topic selection evidence
Ten candidates were presented before creating this production: (1) a pause with a return time, (2) specific gratitude, (3) apologies followed by “but,” (4) short replies and inferred meaning, (5) communicating time alone, (6) attention to screens, (7) reconnection rituals, (8) promises and follow-through, (9) updating knowledge of a partner, (10) new shared activities. Candidate 1 selected under explicit --topic=auto: clear ordinary scenario, concrete takeaway, source availability, and feasible sixteen-frame visual development. Other candidates remain ideas requiring their own research; no trend claim.
Overlap check: productions/kabar-baik covers receiving good news; productions/cerita-belum-selesai covers listening before advice. This episode concerns a paused disagreement and agreed return/follow-through, with a materially different audience question and action. No conflicting slug found.
Creative telling options considered internally: unresolved clock (selected), dual point of view, a return-route diagram, an exchange of appointment cards, an empty chair that is revisited. Selected story with how-to retains a recognizable interaction and varied close details.

## Publishing targets
source: board
board_accounts_file: boards/ruang-di-antara/ACCOUNTS.json
board_accounts_sha256: {sha(board/'ACCOUNTS.json')}
accounts: {json.dumps(accounts,ensure_ascii=False)}
Preflight verified exact workspace and connected Instagram account before synthesis: Admin's Workspace / {accounts[0]['workspace_id']}; @eliansatya / {accounts[0]['social_account_id']}. Content type instagram_reel; 900s, 314572800 bytes, 2200 caption characters, 5 hashtags, one video. Optional feed-sharing setting not requested. Use local upload, draft only.

## Research and hook decision
Research complete under SOURCES.md. Three hooks were presented before drafting:
1. “Dia bilang, nanti kita bahas. Lo jadi lebih tenang, atau malah bingung: nanti itu kapan?” — uncertainty about return; selected/recommended under automation.
2. “Gimana caranya minta jeda, kalau pasangan lo masih pengen menyelesaikan obrolannya?” — requester viewpoint.
3. “Obrolannya berhenti. Tapi kapan kalian benar-benar kembali membahasnya?” — follow-through viewpoint.
Selection rationale: the concrete word “nanti” establishes the question and pays off in the final request. Script v1: {count} spoken words, supported advisory scope, no diagnostic claim. Agent verification only; no fabricated human approval.

## Audio decisions
Narration: use, explicit ElevenLabs / {voice} / eleven_v4, root .env resolver provenance. One continuous native-speed request after the static board passes verification.
BGM: none; absence makes the pause, uncompleted conversation, and return audible without emotional scoring.
SFX: use selected licensed board material sounds for the shared agreement, movement away, and return. No automatic effect on every cut. Exact measured triggers and gains will be recorded in video/sound_design.json.

## Storyboard and runtime
Full static storyboard required before synthesis: video/STORYBOARD.md, video/boards/stills, video/boards/storyboard.html and PNG. Agent verifies under active automation.
HyperFrames 0.8.198 init; installed project workflow retained. CLI reports faceless-explainer retired upstream and installed skills current; local workflow remains available and governs this run. Board's canonical frame overrides a shipped design preset. Native frame delegation not authorized; execute the documented inline serial fallback for each frame.
Preview: none started; query status before starting, record ownership, release after export verification and verify process/port cleanup before packaging.
'''
w(B/'EPISODE.md',episode)
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8-sig'))
assert not any(p['slug']==B.name for p in tracker['productions'])
tracker['productions'].append(dict(slug=B.name,topic='Agreed pauses during ordinary couple conflict: explicit return arrangements and follow-through',board='ruang-di-antara',stage='script',status='complete',path='productions/'+B.name))
dump(R/'TRACKER.json',tracker)
print(json.dumps(dict(words=count,voice=voice,scenes=len(scenes))))
