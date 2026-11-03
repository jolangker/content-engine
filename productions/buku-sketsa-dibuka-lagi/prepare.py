"""Freeze the delegated episode decisions and inherited assets."""
from pathlib import Path
import hashlib, json, shutil, sys
P=Path(__file__).resolve().parent; R=P.parents[1]; V=P/'video'; B=R/'boards/ruang-di-antara'; OLD=R/'productions/bangku-di-jalan-pulang'
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rows=[
('Buku dibuka lagi','Dia ingin menggambar lagi. Lo langsung menyarankan jualan. Kenapa dia malah terdiam?','Mau menggambar lagi','conversational, curious'),
('Tujuan yang berbeda','Dukungan bisa meleset kalau tujuan yang dibantu berbeda dari yang dia inginkan.','Arah siapa?','gentle, observant'),
('Nama konsep','Ini berkaitan dengan Michelangelo phenomenon, atau fenomena Michelangelo.','Michelangelo phenomenon','clear, explanatory'),
('Diri yang dituju','Pasangan dapat membantu mendekati sosok yang ingin kita jadi, lewat cara melihat dan merespons.','Diri yang dituju',''),
('Cita-cita dia','Patokannya cita-cita dia sendiri, termasuk keterampilan atau sifat yang ingin dia kembangkan.','Cita-cita dia',''),
('Berani berkarya','Dalam contoh ini, dia ingin berani berkarya setelah lama menyimpan buku sketsanya.','','warm, observant'),
('Harga dan pembeli','Saat lo langsung membahas harga dan pembeli, percakapan bergeser ke target penghasilan.','Target penghasilan',''),
('Belum ingin menjual','Padahal, dia belum bilang ingin menjual gambarnya.','Belum tentu tujuannya','quietly precise'),
('Sesuai tujuan','Saran lo mungkin masuk akal, tapi belum tentu menguatkan tujuan yang dia bangun.','',''),
('Bantuan yang relevan','Dukungan yang sesuai bisa berupa kesempatan latihan, dorongan, atau bantuan yang dia butuhkan.','Ruang buat latihan','clear, gently explanatory'),
('Tidak menjamin','Itu nggak menjamin satu respons langsung membuat cita-citanya tercapai.','Langkah, bukan jaminan','quietly firm'),
('Tanya dulu','Lo bisa tanya: Gua pengin ngerti, bagian mana yang pengin lo coba lagi?','Tanya dulu','warm, curious'),
('Dia menjawab','Misalnya dia menjawab: Gua mau rutin menggambar dulu, tanpa mikirin hasilnya harus dijual.','','sincere, conversational'),
('Tawarkan waktu','Setelah dengar jawabannya, lo bisa menawarkan waktu latihan yang cocok dengan rencana kalian.','Waktu buat mencoba',''),
('Dia melangkah','Bantuannya mengikuti tujuan dia, sambil memberi ruang buat dia mengerjakan langkahnya sendiri.','','reflective'),
('Arah siapa','Jadi, sebelum kasih arah, cek dulu: arah siapa yang sedang lo dukung?','Arah siapa?','intimate, leave space')]
lines=[dict(id=i,title=a,text=b,emphasis=c,tags=d,dramatic=i in (8,11)) for i,(a,b,c,d) in enumerate(rows,1)]
count=sum(len(x['text'].split()) for x in lines); assert 170<=count<=200,count
snapshot=dict(source='board',board_accounts_file='boards/ruang-di-antara/ACCOUNTS.json',board_accounts_sha256=hashlib.sha256((B/'ACCOUNTS.json').read_bytes()).hexdigest(),accounts=json.loads((B/'ACCOUNTS.json').read_text())['accounts'])
episode='''# Buku sketsa dibuka lagi

New production requested 2026-11-04: --board=ruang-di-antara --topic=auto --delivery=queue --automation. Commit after the finished pipeline. Topic selection: auto. Endpoint: publishing, queue=next, all inherited targets.

execution_policy: automation
automation_after: none
automation_state: active
human_review: none
pre_render_authorization: delegated by the user's --automation instruction
human_approval: false

Board: [editorial v1.4](../../boards/ruang-di-antara/EDITORIAL.md), [visual v1.2 / implementation 2026-10-21](../../boards/ruang-di-antara/frame.md), audio v1.2. Indonesian lo–gua; 1080x1920, 30fps, sixteen meaningful compositions, exactly two dramatic frames 08/11, approximately 90s (85–95). Original faceless participants and sketchbook/pencil/table illustrations, no B-roll. Full spoken captions. No BGM: the partner's aspirations stay open rather than emotionally prescribed; sparse material SFX mark relevant actions, with quiet dramatic turns and closing hold.

## Delegated shortlist — prepared before creation

1. **Recommended/selected: Buku sketsa dibuka lagi.** Investigate the Michelangelo phenomenon through support for a partner's own desired creative self. Ask whether an offer to sell drawings supports the aspiration the partner actually named.
2. Remembering a changed preference. Investigate updating partner knowledge when an old favorite is no longer wanted; ask instead of fixing a person in the past.
3. A laugh shared after a harmless mishap. Investigate shared laughter while keeping affectionate enjoyment distinct from ridicule.
4. An invitation in a small remark. Investigate bids for connection through a remark about a street cat; avoid an obligation to respond at all times.
5. What stays private. Investigate privacy-boundary coordination when a partner shares a personal story; negotiate what may be retold.
6. A disappointment named without agreement. Investigate emotional validation while retaining disagreement about an event; distinguish feeling from verdict.
7. A shelf, not a character judgment. Investigate describing an ordinary behavior instead of assigning a global personal label.
8. Familiarity with separate skills. Investigate distributed partner knowledge through a recipe and grocery scene; avoid equating memory roles with fairness.
9. Receiving a compliment. Investigate accepting a specific positive observation without dismissing it; avoid a promise about self-esteem.
10. A gesture of affection with permission. Investigate different preferences for touch after a tiring day, with consent and variability explicit.

Candidates are provisional editorial angles. Selected 1 for positive everyday growth, an intelligible concrete object, one established concept and accessible author research. Tracker and production folders checked. Nearest overlap: ruang-untuk-memilih concerns autonomous personally endorsed choices; coba-hal-baru-berdua concerns joint novelty; deadline-dan-cucian concerns stress and negotiated assistance. Here the audience is the supporter, the central question is alignment with the partner's ideal self, and the application is to ask about the partner's growth goal before offering goal-specific help. No duplicate slug or repeated scene/takeaway.

## Research and delivery preflight

Read Rusbult, Finkel & Kumashiro (2009), an author-hosted research review, using MarkItDown. Text extraction has column spacing artifacts but the definitions and distinction from Pygmalion are identifiable. PsycNet original-study record returned HTTP403; no unseen findings attributed to it. Source map in SOURCES.md; no effect size, health claim, outcome guarantee or inferred motive. SearXNG discovery available with some engines unavailable. Context7 integration absent in this session; technical execution uses the pinned installed HyperFrames docs and current CLI schemas.

Trypost live preflight: Admin's Workspace 01a171dd-5281-730d-af07-f2168d17add7; connected Instagram @eliansatya 01a172ed-9899-7177-ab1e-627c835e4a57. publishes_directly=true, requires_approval=false. instagram_reel supports 900s / 314572800 bytes, caption 2200 characters, at most five hashtags. Queue daily 05:00 Asia/Jakarta; use next configured free slot, record actual returned UTC and local schedule. Local MP4 upload selected. HyperFrames 0.9.1 pinned; usage known at intake. Existing unrelated TRACKER.json change and untracked video-nearby-copy production are preserved and excluded from this episode's commit.

## Three hooks, selected before script drafting

1. **Selected/recommended:** “Dia ingin menggambar lagi. Lo langsung menyarankan jualan. Kenapa dia malah terdiam?” An observable mismatch opens the question without assigning a motive to the silence. The episode supplies a possible distinction, not a diagnosis.
2. “Buku sketsanya baru dibuka, lo udah ngomongin pembeli. Kalian lagi mendukung tujuan yang sama?” Object-first and two agendas; less conversational than option 1.
3. “Waktu lo bilang pengin dia berkembang, versi siapa yang sedang lo bayangkan?” Reflective tension, but too abstract for the opening compared with the sketchbook.

Agent selected 1 under immediate automation. All three evaluated after research, before SCRIPT.md. No human approval claimed.

## POV contract and narration-only continuity — script v1

Viewer lo = supporter who suggested selling the partner's drawings. Dia = partner wanting to draw again. Narrator = observing companion; no narrator autobiography. Scene 4 kita is generic inclusive selfhood in the explanation and does not give the partner a new viewer role; scenes 5 onward explicitly return to dia's goals. Scene 12 audibly identifies Lo bisa tanya before gua (viewer) and quoted lo (partner). Scene 13 audibly identifies Misalnya dia menjawab: gua is now the partner. Scene 14 audibly returns to the viewer with Setelah dengar jawabannya, lo bisa. Kalian = the established couple. Every instruction is directed to the same supporter. The silence is observable; aspirations and dialogue are explicitly fictional examples, not a claim about the real viewer's partner. Closing answers the supporter's initial question. Full spoken sequence read without visuals: pass, no unresolved referents. Exact tagged synthesis text and full captions must retain these cues.

## Publishing targets

```json
'''+json.dumps(snapshot,ensure_ascii=False,indent=2)+'''\n```

## Stage record

Brief, research and script agent-verified under delegation. Next: complete and visually inspect the entire static storyboard before synthesis.
'''
(P/'EPISODE.md').write_text(episode,encoding='utf-8')
(P/'SOURCES.md').write_text('''# Evidence and claim map

Research date 2026-11-04. Author research review: Rusbult, C. E., Finkel, E. J., & Kumashiro, M. (2009). The Michelangelo Phenomenon. Current Directions in Psychological Science, 18(6), 305–309. https://doi.org/10.1111/j.1467-8721.2009.01657.x

Author-hosted full paper read through MarkItDown: https://faculty.wcas.northwestern.edu/eli-finkel/documents/47_RusbultFinkelKumashiro2009_CDir.pdf

Extraction succeeds with multi-column spacing/table artifacts; wording checked in the relevant sections. No numerical findings or figure geometry used. The 1999 original-study PsycNet record https://psycnet.apa.org/record/1999-03699-005 returned 403, so original study details are not represented as independently read.

| Spoken/visual claim | Evidence | Boundary |
| --- | --- | --- |
| Michelangelo phenomenon / fenomena Michelangelo, partners can support movement toward an ideal self (03–04) | Review abstract and The Ideal Self and Partner Affirmation: ideal self includes desired skills, traits and resources; partners' perceptions and behavior may affirm these goals. | Descriptive interpersonal research model, not a diagnosis or a claim that all partners create growth. Indonesian is a direct translation. |
| The relevant goals are the target person's own aspirations (05,09,15–16) | Partner affirmation defined by compatibility with the target's ideal self; Pygmalion Phenomenon section distinguishes sculpting toward the sculptor's own ideals. | Do not depict coercive reshaping or presume to know another person's true self. Asking is an editorial application. |
| Goal-relevant support can include opportunities, encouragement or direct assistance (10) | Review p306: communicating confidence, reacting positively to ideal-congruent action, providing direct assistance; examples of eliciting behaviors consistent with the target ideal. | Examples, no universal best technique. Selling art is not intrinsically unsupportive; it is mismatched only in this fictional scene where the partner names a different immediate goal. |
| One response does not guarantee achievement (11) | Review summarizes multiple interpersonal processes over time and longitudinal/associational evidence, with future research directions. | We make no numerical, causal effect-size, immediate achievement, relationship-satisfaction or clinical claim. |
| Sketchbook opening, silence, selling suggestion, explicit response and practice-time offer (01–02,06–08,12–16) | Original fictional illustration and editorial application of goal alignment. | Silence has no diagnosed cause. Wording says can/maybe and explicitly introduces the example. Dialogue is invented, not a research participant quotation. No suggestion to abandon work or shared commitments. |

Creative reference: approved Ruang di Antara visual v1.2 and original sketchbook/table/pencil drawings. Actor identity and palettes do not encode gender, blame or psychological value. No data chart or causal outcome gauge. Author/year and the source URL accompany upload copy.
''',encoding='utf-8')
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8-sig')); assert not any(x['slug']==P.name for x in tracker['productions'])
tracker['productions'].append(dict(slug=P.name,topic='Michelangelo phenomenon: support aligned with a partner’s ideal-self aspirations through a fictional return-to-drawing scene',board='ruang-di-antara',stage='script',status='complete',path='productions/'+P.name)); dump(R/'TRACKER.json',tracker)
dump(V/'script_data.json',lines);dump(P/'target_snapshot.json',snapshot)
doc=f'# Buku sketsa dibuka lagi — script v1\n\n{count} spoken words; approximately 90 seconds. Fictional example. Agent-verified under automation; no human approval.\n\n## POV contract\n\nViewer lo = supporter suggesting selling; dia = partner returning to drawing; narrator = observing companion. Scene 12 Lo bisa tanya introduces viewer gua / partner lo. Scene 13 Misalnya dia menjawab introduces partner gua. Scene 14 returns audibly to the viewer. Kalian = couple; general kita in scene 4 does not change the viewer role.\n\n'
for x in lines:doc+=f'## Scene {x["id"]:02d}: {x["title"]}\n\n{x["text"]}\n\nEmphasis: {x["emphasis"] or "(none)"}. Palette: {"charcoal" if x["dramatic"] else "cream"}.\n\n'
for f in (P/'SCRIPT.md',V/'SCRIPT.md'):f.write_text(doc,encoding='utf-8')
(V/'BRIEF.md').write_text(episode,encoding='utf-8');shutil.copy2(B/'frame.md',V/'frame.md')
(V/'assets/fonts').mkdir(parents=True,exist_ok=True)
for f in (B/'assets').iterdir():
    if f.is_file() and f.suffix in ('.ttf','.txt'):shutil.copy2(f,V/'assets/fonts'/f.name)
shutil.copytree(B/'components',V/'assets/board/components',dirs_exist_ok=True);shutil.copytree(B/'assets/audio/sfx',V/'assets/board/audio/sfx',dirs_exist_ok=True)
(V/'vendor').mkdir(exist_ok=True);shutil.copy2(OLD/'video/vendor/gsap.min.js',V/'vendor/gsap.min.js')
for name in ('visuals.py','animate.py','capture_stills.py','capture_board.py','qa.py','prepare_audio.py','finish_audio.py','verify_export.py','capture_motion.py','verify_cut_frames.py','preview_qa.py'):
    shutil.copy2(OLD/name,P/name)
sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'))
from narration import resolve_voice
voice,res=resolve_voice(R,board='ruang-di-antara')
dump(V/'audio_request.json',dict(provider='elevenlabs',board='ruang-di-antara',lang='id',voice=voice,voice_resolution=res,tts_model='eleven_v4',lines=[dict(id='narration',text='\n\n'.join((f'[{x["tags"]}] ' if x['tags'] else '')+x['text'] for x in lines))]))
print(json.dumps(dict(words=count,scenes=len(lines),targets=len(snapshot['accounts']))))
