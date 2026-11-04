"""Freeze the selected episode and reuse only isolated technical helpers."""
from pathlib import Path
import hashlib,json,shutil,sys
P=Path(__file__).resolve().parent;R=P.parents[1];V=P/'video';B=R/'boards/ruang-di-antara';OLD=R/'productions/buku-sketsa-dibuka-lagi'
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rows=[
('Kantong di pintu','Lo udah bilang bakal buang sampah. Malamnya, kantong itu masih di depan pintu. Niatnya berhenti di mana?','Nanti itu kapan?'),
('Cari pemicu','Salah satu hal yang bisa dicek: rencana lo udah punya pemicu tindakan belum?','Pemicu tindakan'),
('Konsep','Ada konsep implementation intentions, atau niat implementasi: mengaitkan situasi tertentu dengan tindakan yang akan dilakukan.','Implementation intentions'),
('Niat dan rencana','Bedakan keinginan melakukan sesuatu dengan rencana kapan, di mana, dan bagaimana lo mulai.','Niat → rencana'),
('Sepakat bertugas','Misalnya lo sepakat bertugas membuang sampah, tapi cuma bilang: Gua buang nanti.','Gua buang nanti'),
('Nanti menggantung','Kata nanti belum menunjuk kejadian yang akan jadi tanda buat lo bergerak.','Setelah apa?'),
('Kesempatan lewat','Saat kegiatan lain berjalan, kesempatan memulai bisa kelewat. Ada celah antara niat dan tindakan.',''),
('Perlu tindakan','Niat yang tulus tetap perlu diwujudkan.','Perlu diwujudkan'),
('Hubungkan pemicu','Rencana ini menghubungkan pemicu yang mudah dikenali dengan respons yang spesifik.','Pemicu → tindakan'),
('Langkah ditentukan','Saat pemicunya muncul, lo udah menentukan langkah berikutnya, tanpa memutuskan semuanya dari awal.',''),
('Batas rencana','Tapi rencana ini nggak menggantikan pembagian tugas yang adil atau kesediaan lo menjalankannya.','Tetap perlu sepakat'),
('Janji spesifik','Lo bisa bilang ke dia: Gua yang buang sampah. Setelah cuci piring malam ini, gua bawa kantongnya ke tempat sampah luar.','Setelah cuci piring'),
('Cek hambatan','Cek apakah waktu dan tempatnya memungkinkan. Kalau ada hambatan, ubah rencananya bersama.','Bisa dijalankan?'),
('Mulai bergerak','Begitu piring terakhir selesai dicuci, lo ambil kantongnya, lalu bawa keluar.',''),
('Bicarakan hasil','Selesai atau belum, bicarakan hasilnya. Pasangan lo nggak otomatis menjadi pengingat pribadi.','Tanggung jawab lo'),
('Jawaban penutup','Jadi, waktu lo bilang nanti, lanjutkan: setelah kejadian apa, lo mulai melakukan apa?','Setelah apa, lakukan apa?')]
lines=[dict(id=i,title=a,text=b,emphasis=c,tags=('conversational, curious' if i==1 else 'quietly firm' if i in (8,11) else 'warm, clear, reflective' if i==16 else 'gentle, explanatory'),dramatic=i in (8,11)) for i,(a,b,c) in enumerate(rows,1)]
count=sum(len(x['text'].split()) for x in lines)
snapshot=dict(source='board',board_accounts_file='boards/ruang-di-antara/ACCOUNTS.json',board_accounts_sha256=hashlib.sha256((B/'ACCOUNTS.json').read_bytes()).hexdigest(),accounts=json.loads((B/'ACCOUNTS.json').read_text())['accounts'])
episode='''# Nanti itu kapan?

Requested 2026-11-05: --board=ruang-di-antara --topic=auto --delivery=queue --automation. Commit after pipeline completion. New production; endpoint publishing, queue next configured slot, full inherited account set.

execution_policy: automation
automation_after: none
automation_state: active
human_review: none
pre_render_authorization: delegated by the user's --automation instruction
human_approval: false

Board: [editorial v1.4](../../boards/ruang-di-antara/EDITORIAL.md), [visual v1.2 / implementation 2026-10-21](../../boards/ruang-di-antara/frame.md), audio v1.2. Indonesian lo–gua; 1080x1920/30fps, sixteen meaningful compositions, exactly two charcoal turns 08/11, 85–95 seconds. Original faceless actors, tied refuse bag, door, dishes and outside bin; no B-roll. Full spoken captions. Narration plus sparse material sounds; intentional no music so an ordinary responsibility remains emotionally open, with quiet dramatic turns and final hold.

## Delegated shortlist prepared before folder creation

1. **Recommended and selected: Nanti itu kapan?** Investigate implementation intentions through an agreed refuse-disposal task. Ask how a recognizable situation can become a cue for a specific action.
2. Laughing together after a harmless mishap. Investigate shared laughter, while separating mutual amusement from ridicule.
3. Updating a familiar preference. Investigate checking what a partner currently enjoys rather than relying on an old favorite.
4. A personal story retold to friends. Investigate coordinated privacy boundaries and explicit permission.
5. Disappointment without agreement. Investigate validation of feelings while retaining disagreement about an event.
6. One shelf, one complaint. Investigate describing specific behavior rather than assigning global character judgments.
7. Who remembers the travel details? Investigate transactive memory and explicit coordination, without justifying unequal mental labor.
8. Receiving a compliment. Investigate a specific positive observation without dismissing it or promising self-esteem benefits.
9. A remark about a street cat. Investigate an ordinary invitation to connect without requiring constant availability.
10. Different preferences for touch. Investigate consent and changing preferences after a tiring day.

These are provisional editorial angles, not ten researched claims. Pick 1 is concrete, feasible in sixteen frames, and gives the person responsible for a task an actionable self-regulation tool. Tracker plus all production folders checked. Nearest overlap: deadline-dan-cucian covers negotiated practical support under work stress; jeda-punya-waktu-kembali covers returning to conflict; gua-kira-udah-kelihatan covers a sender overestimating emotional transparency. Here the viewer is the task owner, the question is initiating an agreed action, and the takeaway is linking a situation to a response. No repeated central claim or slug.

## Research and technical preflight

Read Gollwitzer (1999), Implementation intentions: Strong effects of simple plans, full research article via MarkItDown at the Prospective Psychology mirror. Extraction contains column/OCR artifacts but the definition and action-initiation discussion are clear. Author publication page returned HTTP403. No unseen findings, numerical effect sizes, clinical advice or relationship-outcome guarantee. SearXNG default engines returned irrelevant Bing material; yahoo-only search recovered relevant scholarly records. Claims and limits in SOURCES.md.

Context7 tools are unavailable in this session; pinned installed HyperFrames references and actual CLI help/schema serve as the technical fallback. HyperFrames 0.9.1. Trypost preflight verified Admin's Workspace 01a171dd-5281-730d-af07-f2168d17add7, connected Instagram @eliansatya 01a172ed-9899-7177-ab1e-627c835e4a57, publishes_directly=true, requires_approval=false. instagram_reel: 900s, 314572800 bytes, caption 2200 chars, at most five hashtags. Daily queue 05:00 Asia/Jakarta; actual free schedule resolved at write time. Local MP4 upload selected.

## Hooks selected after research, before script drafting

1. **Selected/recommended:** “Lo udah bilang bakal buang sampah. Malamnya, kantong itu masih di depan pintu. Niatnya berhenti di mana?” Observable unresolved action, no inferred motive, stable viewer as task owner.
2. “Kata nanti udah keluar. Tapi kapan badan lo mulai bergerak?” Direct self-reflection; less concrete than the visible bag.
3. “Lo punya niat baik. Udah ada kejadian yang jadi tanda buat mulai?” Concept-first question; weaker immediate recognition than option 1.

Agent selected 1 under immediate automation. It asks about a possible planning gap; the script does not diagnose every unfulfilled promise as this mechanism.

## POV contract and narration-only continuity — script v1

Viewer lo = the person who agreed to dispose of the refuse; dia/pasangan lo = partner in that household; narrator = observing companion. Scene 5 audibly introduces the viewer's quoted gua with lo... bilang. Scene 12 lo bisa bilang ke dia introduces viewer gua / partner addressee; after the quote, scene 13's imperative returns to the same task owner. Together/both means the established pair negotiating feasibility. All later actions and the closing remain addressed to the task owner. Partner never becomes a default reminder. No narrator autobiography or invented partner motive. The continuous spoken sequence read without labels/images: pass; every pronoun, instruction and quote transition resolves. Preserve exact cues in synthesis and captions.

## Publishing targets

```json
'''+json.dumps(snapshot,ensure_ascii=False,indent=2)+'''\n```

## Stage record

Brief, research, hook and script agent-verified. Next: complete static storyboard and inspect every scene before synthesis. Unrelated existing board changes, kaleng-roda-dan-pisau production and tracker differences must stay outside the requested commit.
'''
(P/'EPISODE.md').write_text(episode,encoding='utf-8')
(P/'SOURCES.md').write_text('''# Evidence and claim map

Research date: 2026-11-05. Gollwitzer, P. M. (1999). Implementation intentions: Strong effects of simple plans. American Psychologist, 54(7), 493–503. DOI https://doi.org/10.1037/0003-066X.54.7.493

Full article read via MarkItDown: https://www.prospectivepsych.org/sites/default/files/pictures/Gollwitzer_Implementation-intentions-1999.pdf . Original author's research, hosted by a psychology initiative; extraction has column spacing/OCR artifacts. Author publication page http://www.socmot.uni-konstanz.de/publications/implementation-intentions-strong-effects-simple-plans returned HTTP403. No findings attributed to unseen material.

| Claim | Evidence and interpretation | Limits |
| --- | --- | --- |
| Implementation intentions / niat implementasi link an anticipated situation to a specific response (03,09) | Abstract; Goal Intentions Versus Implementation Intentions, pp494–495. Indonesian term is a direct explanatory translation. | General self-regulation concept, not a diagnosis or relationship-specific treatment. |
| Goal intention differs from predeciding when/where/how to initiate an action (02,04–06) | p494 explicitly contrasts goal commitment and situational response planning. | A promise can fail for many reasons. The opening asks about one checkable planning gap, not inferred unwillingness. |
| Other activity can cause an opportunity to be missed (07) | Action Initiation section p495 discusses absorption in ongoing activity and missed opportunities. | Possibility, no assertion that this is the actual viewer's reason. |
| Predeciding the response reduces the need to decide anew when the situation occurs (10) | Preparing Goal Pursuit and action-initiation discussion pp494–495. | Does not guarantee remembering or completion; no universal automaticity claim. |
| Plan still requires willingness and does not settle fair task allocation (11,13,15) | Article distinguishes goal commitment from implementation, with implementation subordinate to the goal. Fairness and shared feasibility are editorial scope limits. | No claim that a plan repairs relationship dissatisfaction or unequal labor. Partner is not assigned the reminder role. |
| Bag by the door, agreed responsibility, washing dishes as cue, taking refuse outside (01,05–06,12–16) | Original fictional example and proposed application. | Illustrative sequence; no research participant quote or causal success proof. Cue and location must be feasible and mutually agreed. Visual disposal is an example, not guaranteed efficacy. |

No effect size, health outcome, diagnostic label or guaranteed relationship benefit. No gender/blame coloring. Creative source: approved board visual v1.2 and original SVG household objects. Caption includes research attribution and fictional-example context.
''',encoding='utf-8')
doc=f'# Nanti itu kapan? — script v1\n\n{count} spoken words. Approximately 90 seconds. Fictional household example; agent verified, no human approval.\n\n## POV contract\n\nViewer lo = task owner; dia = partner; narrator = observing companion. Scene 5 and 12 audibly assign quoted gua to viewer. All instructions and closing retain that role.\n\n'
for x in lines:doc+=f'## Scene {x["id"]:02d}: {x["title"]}\n\n{x["text"]}\n\nEmphasis: {x["emphasis"] or "(none)"}. Palette: {"charcoal" if x["dramatic"] else "cream"}.\n\n'
for f in (P/'SCRIPT.md',V/'SCRIPT.md'):f.write_text(doc,encoding='utf-8')
(V/'BRIEF.md').write_text(episode,encoding='utf-8');dump(V/'script_data.json',lines);dump(P/'target_snapshot.json',snapshot)
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8-sig'));assert not any(x['slug']==P.name for x in tracker['productions']);tracker['productions'].append(dict(slug=P.name,topic='Implementation intentions: linking a recognizable situational cue to an agreed household action through a fictional refuse-disposal scene',board='ruang-di-antara',stage='script',status='complete',path='productions/'+P.name));dump(R/'TRACKER.json',tracker)
shutil.copy2(B/'frame.md',V/'frame.md');(V/'assets/fonts').mkdir(parents=True,exist_ok=True)
for f in (B/'assets').iterdir():
    if f.is_file() and f.suffix in ('.ttf','.txt'):shutil.copy2(f,V/'assets/fonts'/f.name)
shutil.copytree(B/'components',V/'assets/board/components',dirs_exist_ok=True);shutil.copytree(B/'assets/audio/sfx',V/'assets/board/audio/sfx',dirs_exist_ok=True)
shutil.copytree(OLD/'video/vendor',V/'vendor',dirs_exist_ok=True)
helpers=['visuals.py','animate.py','capture_stills.py','capture_board.py','prepare_audio.py','finish_audio.py','qa.py','verify_export.py','capture_motion.py','verify_cut_frames.py','cleanup_preview.py','state.py','upload_media.py','verify_remote_media.py','commit_scope.py']
for name in helpers:shutil.copy2(OLD/name,P/name)
for name in ('prepare_audio.py','finish_audio.py'):
    f=P/name;s=f.read_text(encoding='utf-8').replace('==187',f'=={count}').replace('187 aligned words',f'{count} aligned words').replace('caption_words=187',f'caption_words={count}');f.write_text(s,encoding='utf-8')
f=P/'visuals.py';f.write_text(f.read_text(encoding='utf-8').replace('Buku sketsa dibuka lagi','Nanti itu kapan?'),encoding='utf-8')
f=P/'capture_board.py';s=f.read_text(encoding='utf-8').replace('Buku sketsa dibuka lagi','Nanti itu kapan?').replace('Support the partner’s own creative aspiration; ask before offering a different goal.','Connect a recognizable cue to an agreed household action; retain responsibility and feasibility.');f.write_text(s,encoding='utf-8')
print(json.dumps(dict(words=count,scenes=len(lines),stage='script')))
