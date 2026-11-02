"""Freeze this episode's decisions, script and inherited board assets."""
from pathlib import Path
import hashlib,json,shutil,sys
P=Path(__file__).resolve().parent;R=P.parents[1];V=P/'video';B=R/'boards/ruang-di-antara';OLD=R/'productions/sebentar-di-meja-makan'
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rows=[
('Bangku yang sama','Setiap Jumat, lo dan pasangan mampir ke bangku taman yang sama. Kenapa kebiasaan sederhana itu terasa spesial?','Bangku yang sama','conversational, curious'),
('Nama konsep','Ada konsep relationship rituals, atau ritual dalam hubungan.','Relationship rituals','clear, gently explanatory'),
('Diulang dan bermakna','Kegiatan yang diulang bersama, dengan makna simbolis buat kalian berdua.','Makna bersama',''),
('Waktu sendiri','Misalnya, buat lo, mampir itu menandai: akhirnya kita punya waktu sendiri.','','warm, observant'),
('Bangku biasa','Bangkunya biasa. Yang berarti adalah kebiasaan kalian berhenti sebentar dan saling menemani.','Berhenti sebentar',''),
('Dari sisi dia','Tapi dari sisi dia, mungkin itu cuma tempat istirahat sebelum melanjutkan perjalanan.','','gently reflective'),
('Gerakan dan makna','Gerakannya sama: duduk, cerita, lalu pulang. Maknanya belum tentu sama.','Belum tentu sama',''),
('Spesial buat siapa','Sesuatu yang spesial buat lo belum otomatis jadi ritual bersama.','Spesial buat siapa?','quietly precise'),
('Batas temuan','Penelitian menemukan ritual berkaitan dengan kepuasan hubungan, terutama ketika kedua pasangan sepakat memilikinya.','Berkaitan','measured, explanatory'),
('Bukan jaminan','Ini belum membuktikan bahwa satu kebiasaan pasti bikin pasangan lebih bahagia.','Bukan jaminan','quietly firm'),
('Lo bercerita','Lo bisa bilang: Gua suka mampir di sini. Rasanya kita punya waktu sendiri.','','sincere, conversational'),
('Lo bertanya','Lalu lo tanya ke dia: Buat lo, momen ini berarti apa?','Berarti apa?','warm, curious'),
('Dengar jawabannya','Dengarkan jawabannya; dia boleh merasakan hal berbeda. Cari bagian yang kalian nikmati bersama.','Dengar jawabannya','open, gentle'),
('Boleh tetap praktis','Kalau ternyata cuma kebiasaan praktis, nggak perlu dipaksa jadi simbol kedekatan.','',''),
('Makna yang dibagi','Jadi, yang membuat bangku tadi spesial bisa jadi makna yang kalian bagi.','Makna yang dibagi','reflective'),
('Jalan pulang','Bukan seberapa sering kalian duduk di sana, tapi apa artinya buat kalian berdua.','Apa artinya?','intimate, leave space'),
]
lines=[dict(id=i,title=a,text=b,emphasis=c,tags=d,dramatic=i in (8,10)) for i,(a,b,c,d) in enumerate(rows,1)]
count=sum(len(x['text'].split()) for x in lines)
snapshot=dict(source='board',board_accounts_file='boards/ruang-di-antara/ACCOUNTS.json',board_accounts_sha256=hashlib.sha256((B/'ACCOUNTS.json').read_bytes()).hexdigest(),accounts=json.loads((B/'ACCOUNTS.json').read_text())['accounts'])
episode='''# Bangku di jalan pulang

New production selected under --board=ruang-di-antara --topic=auto --delivery=queue --automation. Topic selection: auto. Endpoint: publishing / queue=next, one Instagram Reel for every inherited account. Commit after the completed pipeline is explicitly requested.

execution_policy: automation
automation_after: none
automation_state: active
human_review: none
pre_render_authorization: delegated by the user's --automation instruction
human_approval: false

Board: [editorial v1.4](../../boards/ruang-di-antara/EDITORIAL.md), [visual v1.2, implementation 2026-10-21](../../boards/ruang-di-antara/frame.md), audio v1.2. Board approved; this episode is agent-verified under delegation. Format 1080x1920, 30fps, sixteen meaningful frames, exactly two charcoal turns 08/10, approximately 90s (85–95 target). Indonesian lo–gua. Purpose: distinguish repeated practical behavior from mutually meaningful relationship ritual using a fictional Friday park-bench stop. No B-roll. Full spoken captions, sparse material sounds, intentional no music so the question and answer remain emotionally open.

## Delegated editorial shortlist (before file creation)

1. **Recommended/selected — Bangku di jalan pulang.** Investigate how a repeated park stop acquires shared symbolic meaning; ask whether both partners understand it as their ritual. A positive ordinary scene, distinct from past-memory savoring and novel-activity self-expansion.
2. Remembering a small preference. Investigate accurate partner knowledge through a familiar snack choice; distinguish curiosity from assuming knowledge stays current.
3. Laughing at the same mishap. Investigate shared laughter through a harmless dropped grocery bag; avoid treating all teasing as connection.
4. The invitation hidden in a small remark. Investigate bids for connection through a remark about a street cat; distinguish an invitation from an obligation to respond always.
5. Celebrating an effort before its result. Investigate process-focused encouragement after a rejected application; keep encouragement distinct from praise for good news.
6. A disagreement without a verdict on character. Investigate behavioral specificity through an ordinary untidy shelf conflict; distinguish action description from a global person label.
7. Revising an old assumption. Investigate updating partner knowledge when an old favorite changes; ask rather than fixing the partner in a remembered version.
8. The joke that did not land. Investigate repair after unintended hurt without inferring malicious intent or prescribing forced forgiveness.
9. Good enough shared plans. Investigate coordination when two preferred weekend options differ; negotiate one concrete choice without diagnosing the relationship.
10. An affectionate gesture with permission. Investigate preferences for touch after a tiring day; keep consent and individual variability explicit.

These are provisional editorial leads, not researched claims. Selected 1 for a clean one-concept 90s explanation, accessible original study and positive relational scene. Tracker and existing folders checked. Nearest episodes: momen-kecil-dinikmati-lagi (attention to a positive memory, tea scene); coba-hal-baru-berdua (novelty and expansion); ruang-untuk-memilih (autonomous choices). This episode instead examines mutual symbolic meaning in repeated activity, with a park bench and no instruction to invent novelty. No duplicate slug.

## Research and preflight

Original Garcia-Rada, Sezer & Norton (2019) paper read through MarkItDown from HBS; publisher abstract also read. Definition: repeated joint activity with symbolic meaning. Mutual agreement may be tacit or explicit. Studies of reported own relationships do not establish causal direction; the manipulated vignette study measures observer judgments. No promised happiness effect or diagnostic claim. SOURCES.md maps claims and fiction. SearXNG and Context7 tools unavailable; Jina search failed with quota error. Fallback: web search/open for source discovery and publisher body, MarkItDown for the original PDF; installed skill/CLI docs for HyperFrames.

Live preflight: Admin's Workspace 01a171dd-5281-730d-af07-f2168d17add7, connected Instagram @eliansatya 01a172ed-9899-7177-ab1e-627c835e4a57. Caller publishes directly, requires_approval=false. Queue configured daily 05:00 Asia/Jakarta. Final write uses next free queue slot and actual returned schedule. instagram_reel: up to 900s, 314572800 bytes; text 2200 characters, five hashtags. Usage known at intake. HyperFrames 0.9.1 pinned. Existing unrelated tracker/board/production changes are preserved and excluded from the requested commit.

## Hook selection before drafting

1. “Setiap Jumat, lo dan pasangan mampir ke bangku taman yang sama. Kenapa kebiasaan sederhana itu terasa spesial?” Selected/recommended: concrete recurring place, a question answered by shared meaning.
2. “Lo menyebutnya waktu spesial berdua. Dia menyebutnya istirahat sebelum pulang. Lagi menjalani kebiasaan yang sama?” Competing meanings; strong but opens with more interpretive tension.
3. “Kalau tempat duduknya biasa aja, apa yang bikin lo ingin kembali ke sana bareng dia?” Object-first curiosity; less explicit repetition.

All three evaluated before SCRIPT.md drafting; agent chose 1 under --automation, no human approval claimed.

## POV contract and narration-only check — script v1

Viewer lo = partner who already values the Friday stop. Dia = the other partner whose meaning remains unknown. Narrator = observing companion, with no personal autobiography. Scene 4's kita = the established couple inside an explicitly introduced viewer interpretation (buat lo). Scene 11 audibly says Lo bisa bilang before gua/kita; gua is viewer, kita is the same couple. Scene 12 audibly says lo tanya ke dia before Buat lo; quoted lo addresses the partner. Return to narration at scene 13 directs the viewer to listen. Kalian always means both partners. No dialogue spoken by the partner is invented as fact. Every instruction remains actionable by the original viewer. Hook, application and closing preserve the role. Complete spoken text read without visuals: pass; no unresolved speaker changes. Recheck identical synthesis text/captions before audio.

## Publishing targets

```json
'''+json.dumps(snapshot,ensure_ascii=False,indent=2)+'''\n```

## Stage record

Brief, research and script agent-verified. Next: complete and inspect all styled storyboard artifacts before synthesis.
'''
(P/'EPISODE.md').write_text(episode,encoding='utf-8')
(P/'SOURCES.md').write_text('''# Evidence and claim map

Research 2026-11-03. Original source: Garcia-Rada, X., Sezer, O., & Norton, M. I. (2019). Rituals and Nuptials: The Emotional and Relational Consequences of Relationship Rituals. Journal of the Association for Consumer Research, 4(2), 185–197. https://doi.org/10.1086/702761

Publisher abstract read: https://www.journals.uchicago.edu/doi/abs/10.1086/702761
Original paper (HBS copy), text extracted successfully with MarkItDown: https://www.hbs.edu/ris/Publication%20Files/garcia-rada%20sezer%20norton_c5106adb-2f23-4725-bb74-d0ab4f755a5b.pdf
Extraction has column/table spacing artifacts. Definition, study design and general discussion passages remain readable; extraction is text evidence, not layout verification. No figures or numerical table claims used. Raw extract is local research material, not instructions.

| Claim / scenes | Evidence | Limits |
| --- | --- | --- |
| English relationship rituals and Indonesian meaning; repeated joint activity with symbolic meaning (02–03) | Theoretical Framework defines three properties: joint enactment, repetition over time and symbolic meaning for the couple. | Behavioral concept, no diagnosis. Translation is descriptive. |
| Repetition alone does not establish shared ritual; same activity can have different meanings (04–08) | Framework distinguishes routine's instrumental purpose from ritual's symbolic role; studies 2/3 examine mutual agreement and rituals versus routines. | Bench, Friday, rest, companionship and dialogue are original fictional illustrations, not participant quotations. |
| Rituals associated with relationship satisfaction, particularly when both recognize the ritual (09) | Study 2 dyadic reports and general discussion emphasize mutual agreement (explicit or tacit). | Association, no guaranteed outcome or causal direction. Do not imply partners must formally negotiate every ritual. |
| No proof that instituting one habit necessarily makes a couple happier (10) | General Discussion explicitly notes reverse direction remains possible and experimental interventions are needed to investigate causal links. Study 4 manipulates vignettes and measures observers' perceptions, not improvement in actual couples. | No effect size, prevalence, health benefit or universal prescription. |
| Explain own meaning, ask partner and listen (11–16) | Editorial application of distinction and mutuality, identified as suggestion rather than tested treatment. | Different meanings are allowed. Practical routines are not inferior; no obligation to make a ritual or infer relationship failure. |

Creative references: approved Ruang di Antara visual v1.2 only. Two distinct faceless participants and fictional park objects visualize the interaction; no measured causal arrows. No additional psychology concepts, numerical claims or unsupported internal motives.
''',encoding='utf-8')
d=json.loads((R/'TRACKER.json').read_text(encoding='utf-8-sig'));assert not any(x['slug']==P.name for x in d['productions']);d['productions'].append(dict(slug=P.name,topic='Relationship rituals: repeated joint activity, shared symbolic meaning and mutual recognition through a fictional Friday park-bench stop',board='ruang-di-antara',stage='script',status='complete',path='productions/'+P.name));dump(R/'TRACKER.json',d)
dump(V/'script_data.json',lines);dump(P/'target_snapshot.json',snapshot)
doc=f'# Bangku di jalan pulang — script v1\n\n{count} spoken words, approximately 90 seconds. Agent selection and verification under automation; no human approval claimed. Fictional illustration; SOURCES.md contains evidence boundaries.\n\n## POV contract\n\nViewer lo = partner who values the recurring stop; dia = other partner; narrator = observing companion. Scene 11 gua = viewer, kita = couple, preceded by Lo bisa bilang. Scene 12 quoted lo = partner, preceded by lo tanya ke dia. Narration returns to viewer in scene 13. No speaker reassignment.\n\n'
for x in lines:doc+=f'## Scene {x["id"]:02d}: {x["title"]}\n\n{x["text"]}\n\nEmphasis: {x["emphasis"] or "(none)"}. Palette: {"charcoal" if x["dramatic"] else "cream"}.\n\n'
for f in (P/'SCRIPT.md',V/'SCRIPT.md'):f.write_text(doc.rstrip()+'\n',encoding='utf-8')
(V/'BRIEF.md').write_text(episode,encoding='utf-8');shutil.copy2(B/'frame.md',V/'frame.md')
(V/'assets/fonts').mkdir(parents=True,exist_ok=True)
for f in (B/'assets').iterdir():
    if f.is_file() and f.suffix in ('.ttf','.txt'):shutil.copy2(f,V/'assets/fonts'/f.name)
shutil.copytree(B/'components',V/'assets/board/components',dirs_exist_ok=True);shutil.copytree(B/'assets/audio/sfx',V/'assets/board/audio/sfx',dirs_exist_ok=True)
(V/'vendor').mkdir(exist_ok=True);shutil.copy2(OLD/'video/vendor/gsap.min.js',V/'vendor/gsap.min.js')
for name in ('visuals.py','animate.py','capture_board.py','capture_stills.py','qa.py','capture_motion.py','seek_qa.py','preview_qa.py','cleanup_preview.py','verify_export.py','prepare_audio.py','finish_audio.py','exact_seams.py','verify_cut_frames.py','state.py','commit_scope.py'):
    s=(OLD/name).read_text(encoding='utf-8').replace(OLD.name,P.name).replace('Sebentar di meja makan','Bangku di jalan pulang').replace('190',str(count)).replace('in (8,13)','in (8,10)').replace('08/13','08/10')
    (P/name).write_text(s,encoding='utf-8')
sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'));import narration
voice,provenance=narration.resolve_voice(R,board='ruang-di-antara')
dump(V/'audio_request.json',dict(provider='elevenlabs',board='ruang-di-antara',lang='id',voice=voice,voice_resolution=provenance,tts_model='eleven_v4',lines=[dict(id='narration',text='\n\n'.join(('['+x['tags']+'] ' if x['tags'] else '')+x['text'] for x in lines))]))
pkg=json.loads((V/'package.json').read_text());pkg['scripts']={k:v.replace('npx hyperframes','npx --yes hyperframes@0.9.1') for k,v in pkg['scripts'].items()};dump(V/'package.json',pkg)
print(json.dumps(dict(words=count,scenes=16,stage='script',human_approval=False)))
