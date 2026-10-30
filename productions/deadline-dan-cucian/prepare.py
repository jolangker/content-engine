"""Freeze this episode and copy reusable verified implementation utilities."""
from pathlib import Path
import hashlib,json,shutil,sys
P=Path(__file__).resolve().parent;R=P.parents[1];V=P/'video';B=R/'boards/ruang-di-antara';OLD=P.parent/'momen-kecil-dinikmati-lagi'
LINES=[
('Deadline dan cucian','Deadline dia besok. Kenapa yang kalian ributin justru cucian malam ini?','Deadline. Cucian.','intimate, conversational, curious'),
('Nama konsep','Di sini ada konsep dyadic coping, atau mengatasi stres bersama pasangan.','Dyadic coping','clear, gently explanatory'),
('Proses berdua','Artinya, stres yang dialami satu orang ditanggapi lewat komunikasi dan respons pasangannya.','',''),
('Dua pekerjaan','Misalnya, dia dikejar revisi kantor, sementara cucian yang dijanjikan belum dibereskan.','','observant, grounded'),
('Yang terlihat','Lo cuma melihat keranjang penuh. Dia belum cerita seberapa kewalahan dirinya.','Belum diceritakan',''),
('Sinyal dan respons','Dalam proses ini, tanda stres disampaikan, ditangkap, lalu direspons. Bantuan bisa berbentuk dukungan emosional.','','clear, explanatory'),
('Membantu satu tugas','Bisa juga mengambil sebagian tugas, supaya pasangan punya ruang menghadapi tekanannya.','Sebagian tugas',''),
('Batas bantuan','Tapi membantu nggak harus berarti mengambil semua tanggung jawabnya.','Ada batas','quietly firm'),
('Kapasitas berdua','Bentuk bantuan perlu dibicarakan. Kalian juga punya tenaga dan batas yang berbeda.','','warm, grounded'),
('Menyebut stres','Coba mulai: gua lagi kewalahan sama revisi. Cucian gua belum kepegang.','Gua lagi kewalahan','honest, intimate'),
('Permintaan konkret','Terus minta yang spesifik: malam ini bisa bantu jemur? Gua yang lipat besok.','Bisa bantu jemur?','speaking gently to a partner'),
('Jawaban terbatas','Pasangannya boleh jawab: gua bisa jemur separuh. Sisanya kita atur lagi.','Gua bisa separuh','open, conversational'),
('Bagian yang disepakati','Di situ, stresnya disebut, kebutuhannya jelas, dan kemampuan membantu ikut mendapat tempat.','','clear, explanatory'),
('Beban yang terbagi','Deadline kerjanya tetap ada. Kesepakatan ini membagi satu beban rumah yang konkret.','Satu beban konkret',''),
('Kembali ke awal','Jadi, pertengkaran soal cucian tadi bisa dibuka lewat pertanyaan yang lebih terarah.','','reflective'),
('Pertanyaan bersama','Gua lagi berat di bagian ini. Bagian mana yang bisa kita tangani bareng?','Bagian mana?','soft, intimate, reflective'),
]
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 assert not (V/'script_data.json').exists(),'Resume existing frozen intake'
 lines=[dict(id=i,title=t,text=s,emphasis=e,tags=tag,dramatic=i in (8,10)) for i,(t,s,e,tag) in enumerate(LINES,1)]
 count=sum(len(x['text'].split()) for x in lines);assert 170<=count<=215,count
 snapshot=dict(source='board',board_accounts_file='boards/ruang-di-antara/ACCOUNTS.json',board_accounts_sha256=hashlib.sha256((B/'ACCOUNTS.json').read_bytes()).hexdigest(),accounts=json.loads((B/'ACCOUNTS.json').read_text(encoding='utf-8'))['accounts']);dump(P/'target_snapshot.json',snapshot)
 episode='''# Deadline dan cucian

## Resolved intake

- topic_selection: auto; candidate 1 of ten presented in conversation, selected under --topic=auto.
- Topic: dyadic coping with an ordinary external work stressor; explicitly communicating stress and negotiating limited practical assistance.
- Board: [editorial v1.3](../../boards/ruang-di-antara/EDITORIAL.md), [visual v1.2 / implementation 2026-10-21](../../boards/ruang-di-antara/frame.md), audio v1.2. Canonical chrome and local fonts inherited byte-for-byte.
- Indonesian adults; natural lo–gua narration; 1080x1920 at 30fps, approximately 90 seconds, exactly sixteen scenes, charcoal scenes 08 and 10.
- execution_policy: automation
- automation_after: none
- automation_state: active
- human_review: none
- human_approval: false
- pre_render_authorization: delegated by the user's --automation instruction
- requested_endpoint: publishing
- delivery: queue; next configured available slot for every inherited account, without an invented time.
- Commit requested after pipeline completion. Existing working-tree changes belong to other work; commit only this production and its tracker insertion.
- Narration: one continuous tagged ElevenLabs eleven_v4 take, root .env voice at native speed.
- BGM: none, to leave the ordinary household negotiation and its pauses unscored.
- SFX: sparse board-library contact/air/connection material sounds for laundry, work pressure and agreement; no automatic transition sounds. Bundled media-use assets inspected first; bright UI sounds and cinematic impacts do not suit this illustration. Dark frames and final hold use deliberate silence.
- CLI: pinned HyperFrames 0.8.209, as in the latest verified same-board implementation. Context7 MCP is unavailable in this session; local installed skill/CLI docs are the fallback for its syntax. No skills upgrades.

## Selection and overlap

Ten candidates: dyadic coping; partner phubbing; stress spillover; co-rumination; perceived fairness; relationship rituals; invisible support; social comparison; partner knowledge; relational uncertainty. Candidate 1 offers an observable work/laundry scene, clear conceptual support and a limited practical takeaway. No trending claim. Discovery leads were searched through Jina; full source bodies for the selected explanation were read.

Tracker and all production directories inspected. Distinct from cerita-belum-selesai (listening before advice), ruang-untuk-memilih (autonomy), maaf-yang-menyebut-tindakan (responsibility after lateness), and gua-kira-udah-kelihatan (illusion of transparency). The central question here is how to share a concrete task while facing external stress, with both partners' capacity retained. The unregistered roda-beda-putaran is mechanical and has no overlap. Exactly one new episode is created.

## Hook checkpoint before script

1. “Deadline dia besok. Kenapa yang kalian ributin justru cucian malam ini?” A concrete collision of work and household tasks; promise: trace stress communication and negotiate assistance.
2. “‘Gua lagi penuh.’ Bantuan apa yang sebenarnya lo minta dari kalimat itu?” A vague request; promise: make the needed help specific.
3. “Kerjaannya punya dia. Bagian mana yang bisa lo bantu malam ini?” The responding partner's view; promise: identify a bounded contribution.

Agent recommended/selected hook 1 under immediate automation after reading sources and before drafting. It establishes the task that returns in the final question. No human acceptance claimed.

## Preflight

Trypost Admin's Workspace, 01a171dd-5281-730d-af07-f2168d17add7. Caller admin, requires_approval=false, publishes_directly=true. Exact selected account 01a172ed-9899-7177-ab1e-627c835e4a57 is connected Instagram @eliansatya. Configured queue exists; use its next slot. instagram_reel supports 900 seconds / 314572800 bytes; caption 2200 characters and at most five hashtags. Actual returned future schedule must be verified. Board DIRECTION.md's empty-account prose is stale; actual ACCOUNTS.json is authoritative and is not edited by this run.

## Publishing targets

```json
'''+json.dumps(snapshot,ensure_ascii=False,indent=2)+'''\n```

## Current evidence

Research complete: reviewed conceptual integration plus original diary study. Correlational results are not narrated as causes. The scene, dialogue, capacity boundary and practical negotiation are educational illustrations, with no treatment or universal outcome claim. Proceed through complete visual storyboard before synthesis, then verified animation/export/package/queue.
'''
 (P/'EPISODE.md').write_text(episode,encoding='utf-8')
 d=json.loads((R/'TRACKER.json').read_text(encoding='utf-8-sig'));assert not any(x['slug']==P.name for x in d['productions']);d['productions'].append(dict(slug=P.name,topic='Dyadic coping: explicit work-stress communication and negotiated, bounded practical assistance through a fictional laundry scene',board='ruang-di-antara',stage='script',status='in_progress',path='productions/'+P.name));dump(R/'TRACKER.json',d)
 dump(V/'script_data.json',lines)
 doc=f'# Deadline dan cucian — script v1\n\n{count} spoken words; Indonesian lo–gua; estimated 90 seconds. All work/laundry dialogue is fictional. Hook 1 selected before drafting under automation. Scenes 02–09 explain the process and bounds; 10–14 illustrate a specific negotiation. No causal outcome claim.\n\n'
 for x in lines:doc+=f'## Scene {x["id"]:02d}: {x["title"]}\n\n{x["text"]}\n\nEmphasis: {x["emphasis"] or "(none)"}. Palette: {"charcoal" if x["dramatic"] else "cream"}.\n\n'
 for f in (P/'SCRIPT.md',V/'SCRIPT.md'):f.write_text(doc,encoding='utf-8')
 (V/'BRIEF.md').write_text(episode+f'\nScript v1 agent-verified: {count} words, opening/question resolved, concept spoken in English and Indonesian, discussion beyond definition. Human approval false.\n',encoding='utf-8')
 (V/'assets/fonts').mkdir(parents=True,exist_ok=True)
 for f in (B/'assets').iterdir():
  if f.is_file() and f.suffix in ('.ttf','.txt'):shutil.copy2(f,V/'assets/fonts'/f.name)
 shutil.copy2(B/'frame.md',V/'frame.md');shutil.copytree(B/'components',V/'assets/board/components',dirs_exist_ok=True);shutil.copytree(B/'assets/audio/sfx',V/'assets/board/audio/sfx',dirs_exist_ok=True)
 (V/'vendor').mkdir(exist_ok=True);shutil.copy2(OLD/'video/vendor/gsap.min.js',V/'vendor/gsap.min.js')
 for name in ('visuals.py','animate.py','capture_board.py','capture_stills.py','qa.py','capture_motion.py','seek_qa.py','preview_qa.py','cleanup_preview.py','verify_export.py','prepare_audio.py','finish_audio.py','exact_seams.py','verify_cut_frames.py','state.py','commit_scope.py'):
  s=(OLD/name).read_text(encoding='utf-8').replace(OLD.name,P.name).replace('Momen kecil, dinikmati lagi','Deadline dan cucian')
  s=s.replace('==204',f'=={count}').replace('204 aligned',f'{count} aligned').replace('caption_words=204',f'caption_words={count}')
  (P/name).write_text(s,encoding='utf-8')
 sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'));import narration
 voice,_=narration.resolve_voice(R)
 dump(V/'audio_request.json',dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=dict(source='project_env',key='ELEVENLABS_VOICE_ID'),tts_model='eleven_v4',lines=[dict(id='narration',text='\n\n'.join(('['+x['tags']+'] ' if x['tags'] else '')+x['text'] for x in lines))]))
 print(json.dumps(dict(words=count,scenes=16,stage='script')))
if __name__=='__main__':main()
