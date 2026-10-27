"""Freeze the researched attribution episode and its inherited assets."""
from pathlib import Path
import hashlib, importlib.util, json, shutil

P=Path(__file__).resolve().parent; ROOT=P.parents[1]; V=P/'video'; B=ROOT/'boards/ruang-di-antara'
LINES=[
('The unanswered message','Pesan lo belum dibalas. Dari mana kesimpulan, dia udah nggak peduli, itu datang?','Belum dibalas','intimate, conversational, curious'),
('Name the concept','Ada konsep attribution, atau atribusi: penjelasan yang kita buat tentang penyebab perilaku seseorang.','Attribution','clear, gently explanatory'),
('Event and explanation','Kejadiannya: balasan belum masuk. Penjelasannya bisa, dia sibuk, atau dia sengaja menghindar.','Kejadian → penjelasan',''),
('The screen has limits','Layar yang sama belum memberi tahu alasan di belakangnya.','','observant, unhurried'),
('Adding intention','Waktu lo menyimpulkan dia sengaja, lo sedang menambahkan dugaan tentang niatnya.','Sengaja?',''),
('Making it enduring','Kalau lanjut jadi, dia selalu begitu, satu kejadian mulai lo baca sebagai pola menetap.','Selalu begitu?','measured, precise'),
('Two research distinctions','Dalam penelitian pasangan, penjelasan tentang penyebab dan penilaian tentang kesengajaan memang dibedakan.','Penyebab · kesengajaan','clear, explanatory'),
('A thought is not disproven','Mengenali atribusi nggak otomatis berarti dugaan lo salah.','Belum tentu salah','quietly firm'),
('What supports the account','Periksa: informasi apa yang mendukungnya, dan apa yang masih belum lo tahu?','Apa yang diketahui?','curious, unhurried'),
('The benign account is also an account','Membayangkan dia sibuk juga masih dugaan, sebelum ada informasi.','Masih dugaan',''),
('Separate before asking','Coba pisahkan kejadian, tafsiran, lalu pertanyaan yang ingin lo ajukan.','Lihat · tafsir · tanya','open, practical'),
('An adaptable line','Gua belum dapat balasan sejak tadi. Gua jadi khawatir. Lo bisa ngobrol kapan?','','sincere, speaking to a partner'),
('Listen and observe follow-through','Setelah dia menjawab, lihat juga tindakannya dan kesepakatan kalian soal kabar.','Jawaban dan tindakan','warm, precise'),
('Repeated behavior matters','Kalau pengabaian terus berulang, dampaknya tetap layak dibahas.','Dampaknya tetap ada','quietly firm'),
('Keep responsibility and boundaries','Memahami kemungkinan alasan nggak menghapus tanggung jawab atau batas yang lo butuhkan.','Batas tetap berlaku','gentle, direct'),
('Return to the opening','Sebelum memutuskan dia nggak peduli, cek: apa yang lo lihat, dan apa yang lo simpulkan?','Lihat dulu, cek lagi','intimate, reflective, leave space'),
]
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    lines=[dict(id=i,title=a,text=b,emphasis=c,delivery=d,dramatic=i in (8,14)) for i,(a,b,c,d) in enumerate(LINES,1)]
    count=sum(len(x['text'].split()) for x in lines);print('spoken_words',count)
    assert 170<=count<=205
    dump(V/'script_data.json',lines)
    spec=importlib.util.spec_from_file_location('voice_policy',ROOT/'.agents/skills/shortform-production/scripts/narration.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    voice,resolution=m.resolve_voice(ROOT)
    dump(V/'audio_request.json',dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=resolution,tts_model='eleven_v4',lines=[dict(id='narration',text='\n\n'.join((f"[{x['delivery']}] " if x['delivery'] else '')+x['text'] for x in lines))]))
    script=f'# Jeda balasan dan dugaan — script v1\n\n{count} spoken words. Hook 1 selected by agent before drafting under immediate automation. Fictional message scenario. Attribution is a construct, not a diagnosis. Concept explanation and discussion occupy Lines 2–10; no clinical or causal outcome claim.\n\n'
    for x in lines: script+=f"## Line {x['id']}: {x['title']}\n\n{x['text']}\n\nOn-screen: {x['emphasis'] or '(none)'}. Timing: estimated until measured alignment.\n\n"
    for f in (P/'SCRIPT.md',V/'SCRIPT.md'):f.write_text(script,encoding='utf-8')
    (V/'assets/fonts').mkdir(parents=True,exist_ok=True)
    for f in (B/'assets').iterdir():
        if f.is_file() and f.suffix in ('.ttf','.txt'):shutil.copy2(f,V/'assets/fonts'/f.name)
    shutil.copy2(B/'frame.md',V/'frame.md');shutil.copytree(B/'components',V/'assets/board/components',dirs_exist_ok=True);shutil.copytree(B/'assets/audio/sfx',V/'assets/board/audio/sfx',dirs_exist_ok=True)
    (V/'vendor').mkdir(exist_ok=True);shutil.copy2(ROOT/'productions/terima-kasih-yang-melihat/video/vendor/gsap.min.js',V/'vendor/gsap.min.js')
    snapshot=dict(source='board',board_accounts_file='boards/ruang-di-antara/ACCOUNTS.json',board_accounts_sha256=hashlib.sha256((B/'ACCOUNTS.json').read_bytes()).hexdigest(),accounts=json.loads((B/'ACCOUNTS.json').read_text(encoding='utf-8'))['accounts']);dump(P/'target_snapshot.json',snapshot)
    episode=f'''# Jeda balasan dan dugaan

## Brief and authorization

- topic: Attribution in interpreting an unanswered partner message; distinguish observation, inferred cause/intention and evidence.
- topic_selection: auto, delegated by --topic=auto; candidate 1 selected after presenting ten options.
- board: ruang-di-antara; [editorial v1.3](../../boards/ruang-di-antara/EDITORIAL.md), [visual/audio v1.2](../../boards/ruang-di-antara/frame.md), implementation 2026-10-21.
- audience/language: Indonesian adults, conversational lo–gua, complete spoken captions.
- output: 1080x1920, 30fps, approximately 90s, 16 meaningful scenes, 14 cream and 2 charcoal.
- execution_policy: automation
- automation_after: none
- automation_state: active
- human_review: none
- human_approved: false
- pre_render_authorization: delegated by the user's --automation instruction
- requested_endpoint: publishing
- delivery: queue, next configured slot; no custom time.
- commit: explicitly requested after pipeline completion; commit this production and tracker row.

## Topic selection and overlap

Candidates presented: unanswered-message attributions (selected); autonomy support; apology responsibility; unspoken expectations; privacy boundaries; social comparison; asking for support; small bids for connection; supporting a partner's ideals; differing conflict memories. These were editorial directions, not ten verified claims. Selected attribution offers an identifiable screen/clock scene and a primary-source distinction that can be explained within 90s. Existing episodes cover capitalization, active listening, agreed pauses, illusion of transparency, shared novel activities and gratitude. The nearest episode, gua-kira-udah-kelihatan, concerns overestimating the visibility of one's own feelings; this episode concerns explanations added to another's observed behavior. Different question, process and takeaway. Inspected tracker and all production folders, including unregistered roda-beda-putaran; no duplicate slug/topic.

## Hook selection before script

1. “Pesan lo belum dibalas. Dari mana kesimpulan ‘dia udah nggak peduli’ itu datang?” Direct event/inference contrast. Recommended and selected.
2. “‘Dia sengaja ngediemin gua.’ Bagian mana yang lo lihat, dan bagian mana yang lo simpulkan?” Inner speech and evidence.
3. “Dua jam tanpa balasan. Kenapa satu layar kosong bisa terasa punya banyak arti?” Visual detail and multiple explanations.

Agent selected Hook 1 after source-body research, before SCRIPT.md. The full script preserves the opening in spoken form. {count} words; explanation/discussion Lines 2–10. Editorial verification delegated, no human approval claimed.

## Publishing targets

```json
{json.dumps(snapshot,ensure_ascii=False,indent=2)}
```

Preflight: Admin's Workspace (exact ID above), @eliansatya connected, requires_approval=false, publishes_directly=true. Account timezone Asia/Jakarta; daily configured queue 14:00. Current MCP instagram_reel: one video, max 900s/314572800 bytes, caption max 2200 characters/five hashtags. Actual account file takes precedence over stale DIRECTION.md prose saying empty accounts. Actual future schedule will be saved in PUBLISHING.json.

## Creative and audio decisions

One fictional delayed-message situation. Phone only because it carries the observed event. Organic faceless pair, unfinished message space, clock, separate inference branches, evidence/detail windows, reply and agreement. Vary close phone, wide pair, inspection detail, branching comparison and boundary views. Actor color implies no gender or blame. Exactly two dark frames: 08 (recognition is not disproof) and 14 (repeated behavior still has an impact). Fixed canonical board chrome and fonts. No B-roll.

Narration: ElevenLabs / {voice} / eleven_v4; root .env voice, full tagged script, natural speed. No BGM: speech, unresolved time and sparse material cues leave the reasoning open without manufacturing reassurance. SFX: bundled media-use library inspected; UI chimes/glitches do not fit. Reuse frozen board contact/air/connection variants with source hashes and episode-specific triggers. Quiet dark turns and final hold. No new generated SFX.

## State

Research/script verified under delegation. Next: pose, capture and inspect complete 16-scene storyboard before synthesis and animation. No preview server started. CLI initialized at 0.8.209. Context7 tools are unavailable in this session; installed project skill references and current CLI help are the fallback for CLI syntax.
'''
    (P/'EPISODE.md').write_text(episode,encoding='utf-8');(V/'BRIEF.md').write_text(episode,encoding='utf-8')
    (P/'SOURCES.md').write_text('''# Research and claim boundaries

Research date: 2026-10-28. Jina search discovered S1; focused and full read_url retrieved the source body, measures, results and limitations. A PubMed candidate returned a CAPTCHA and was not used. No trend claim.

S1. Ellison et al. (2016), Interplay between Marital Attributions and Conflict Behavior in Predicting Depressive Symptoms. Original study, author manuscript: https://pmc.ncbi.nlm.nih.gov/articles/PMC4767684/ . 284 couples; attribution questionnaires, observed conflict and one-year follow-up. The construct describes explanations for a spouse's behavior. Its measures distinguish causal accounts from responsibility judgments including intentionality. Results varied by outcome and spouse; they do not justify a universal instruction to give benign explanations. Sample primarily European American, heterosexual, generally well-functioning couples with children; no trial of Indonesian texting advice.

| Claim | Support | Limits |
| --- | --- | --- |
| Attribution means an explanation about the cause of behavior, Lines 2–3 | S1 abstract/construct and RAM measures | Indonesian gloss is explanatory translation; no diagnosis. |
| Cause and intentionality judgments are distinguished, Lines 5–7 | S1 measures separately operationalize causal/responsibility attributions | No claim that these exhaust all dimensions; stable-pattern illustration is editorial, not a finding from one text. |
| Recognizing an account does not prove it false; benign accounts also need information, Lines 8–10 | Epistemic boundary of the construct and S1's mixed/context-dependent results | Not an experimentally validated script or guaranteed de-escalation technique. |
| Unanswered message, busy/avoiding possibilities, worry and suggested question | Fictional author-created illustration | No evidence about an actual person's motive. No claim that delayed replies diagnose anything. |
| Observe follow-through and discuss repeated impact/boundaries, Lines 11–16 | Editorial application of uncertainty and responsibility distinction | Does not excuse harm, guarantee trust, require staying, or treat distress. |

No quantitative or mental-health outcome is narrated. Diagrams illustrate alternative explanations, not brain pathways or measured effects. Public caption credits and links S1. Creative reference is the approved board, separate from evidence.
''',encoding='utf-8')
    tracker=json.loads((ROOT/'TRACKER.json').read_text(encoding='utf-8'));assert not any(x['slug']==P.name for x in tracker['productions']);tracker['productions'].append(dict(slug=P.name,topic='Attribution: distinguishing an unanswered partner message from inferred cause and intention',board='ruang-di-antara',stage='storyboard',status='in_progress',path='productions/'+P.name));dump(ROOT/'TRACKER.json',tracker)
    for name in ('visuals.py','capture_board.py','animate.py'):
        text=(ROOT/'productions/terima-kasih-yang-melihat'/name).read_text(encoding='utf-8').replace('Terima kasih yang melihat','Jeda balasan dan dugaan')
        if name=='capture_board.py':text=text.replace('08 and 10','08 and 14')
        (P/name).write_text(text,encoding='utf-8')

if __name__=='__main__':main()
