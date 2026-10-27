"""Freeze this episode's researched script, authorization, and reusable assets."""
from pathlib import Path
import hashlib, importlib.util, json, shutil

P=Path(__file__).resolve().parent; ROOT=P.parents[1]; V=P/'video'; B=ROOT/'boards/ruang-di-antara'; O=P.parent/'jeda-balasan-dan-dugaan'
LINES=[
('A choice that feels closed','Terserah lo, katanya. Tapi kenapa pilihan yang beda masih terasa salah?','Terserah lo?','intimate, conversational, curious'),
('Name the concept','Di sini relevan konsep autonomy support, atau dukungan terhadap otonomi.','Autonomy support','clear, gently explanatory'),
('Room for a perspective','Artinya, pasangan memberi ruang buat lo menyampaikan keinginan dan memilih sesuai nilai lo.','Ruang memilih',''),
('A concrete wish','Misalnya, lo ingin ikut kelas keramik setiap Sabtu. Dia lebih suka kalian di rumah.','','observant, conversational'),
('A different preference','Dia boleh punya pendapat berbeda dan menjelaskan kekhawatirannya.','Boleh berbeda',''),
('Understanding a reason','Yang dilihat: apakah alasan lo didengar, dan pilihan lo bisa dibicarakan tanpa tekanan?','Alasannya didengar?','measured, precise'),
('A shared consideration','Kalau dia bilang, gua bakal kangen waktu bareng, ada kebutuhan yang bisa kalian bahas.','Waktu bersama',''),
('Conditional approval','Kalau jadi, kalau sayang gua lo batalin, persetujuan mulai terasa seperti syarat kedekatan.','Syarat kedekatan','quietly firm'),
('No diagnosis from one line','Satu kalimat belum cukup buat menilai seluruh hubungan. Perhatikan pola responsnya.','Lihat polanya','gentle, precise'),
('Clarify the wish','Coba tanya, apa yang bikin kelas itu penting buat lo?','','curious, open'),
('Give the answer space','Lalu beri ruang buat jawabannya, sebelum menawarkan pilihan lain.','Dengar alasannya',''),
('Explain your own concern','Lo juga bisa bilang, gua ingin tetap punya waktu berdua.','Kebutuhan lo juga','sincere, speaking to a partner'),
('Negotiate the impact','Kita atur waktunya gimana? Dampaknya ke waktu bersama tetap perlu disepakati.','Atur bersama','warm, practical'),
('Agreement without pressure','Kesepakatan perlu ruang untuk bilang belum cocok, tanpa ancaman kehilangan kasih sayang.','Bisa bilang belum','quietly firm'),
('Participation remains','Mendukung otonomi tetap melibatkan perhatian, pertanyaan, dan batas yang jelas.','Tetap terlibat','gentle, direct'),
('Answer the opening','Jadi, terserah lo terasa memberi pilihan kalau respons setelahnya juga menyisakan ruang memilih.','Ruang itu terasa','intimate, reflective, leave space'),
]
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    existing=json.loads((ROOT/'TRACKER.json').read_text(encoding='utf-8'))
    assert not any(x['slug']==P.name for x in existing['productions']), 'Intake is already frozen; resume the existing production instead of overwriting it.'
    lines=[dict(id=i,title=a,text=b,emphasis=c,delivery=d,dramatic=i in (8,14)) for i,(a,b,c,d) in enumerate(LINES,1)]
    count=sum(len(x['text'].split()) for x in lines); print('spoken_words',count); assert 170<=count<=205
    dump(V/'script_data.json',lines)
    spec=importlib.util.spec_from_file_location('voice_policy',ROOT/'.agents/skills/shortform-production/scripts/narration.py'); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    voice,resolution=m.resolve_voice(ROOT)
    dump(V/'audio_request.json',dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=resolution,tts_model='eleven_v4',lines=[dict(id='narration',text='\n\n'.join((f"[{x['delivery']}] " if x['delivery'] else '')+x['text'] for x in lines))]))
    script=f'# Ruang untuk memilih — script v1\n\n{count} spoken words. Hook 1 selected under delegated automation after source-body research and before drafting. One fictional weekend ceramics-class conversation; no diagnosis or guaranteed relationship outcome. Explanation/discussion: Lines 2–9, elaborated by application 10–15.\n\n'
    for x in lines:script+=f"## Line {x['id']}: {x['title']}\n\n{x['text']}\n\nOn-screen: {x['emphasis'] or '(none)'}. Estimated timing until native alignment.\n\n"
    for f in (P/'SCRIPT.md',V/'SCRIPT.md'):f.write_text(script.rstrip()+'\n',encoding='utf-8')
    (V/'assets/fonts').mkdir(parents=True,exist_ok=True)
    for f in (B/'assets').iterdir():
        if f.is_file() and f.suffix in ('.ttf','.txt'):shutil.copy2(f,V/'assets/fonts'/f.name)
    shutil.copy2(B/'frame.md',V/'frame.md');shutil.copytree(B/'components',V/'assets/board/components',dirs_exist_ok=True);shutil.copytree(B/'assets/audio/sfx',V/'assets/board/audio/sfx',dirs_exist_ok=True)
    (V/'vendor').mkdir(exist_ok=True);shutil.copy2(O/'video/vendor/gsap.min.js',V/'vendor/gsap.min.js')
    snapshot=dict(source='board',board_accounts_file='boards/ruang-di-antara/ACCOUNTS.json',board_accounts_sha256=hashlib.sha256((B/'ACCOUNTS.json').read_bytes()).hexdigest(),accounts=json.loads((B/'ACCOUNTS.json').read_text(encoding='utf-8'))['accounts']);dump(P/'target_snapshot.json',snapshot)
    for name in ('visuals.py','animate.py','capture_board.py','qa.py','capture_motion.py','seek_qa.py','preview_qa.py','cleanup_preview.py','verify_export.py','prepare_audio.py','finish_audio.py'):
        s=(O/name).read_text(encoding='utf-8').replace('jeda-balasan-dan-dugaan',P.name).replace('Jeda balasan dan dugaan','Ruang untuk memilih')
        s=s.replace('==182',f'=={count}').replace('182 aligned',f'{count} aligned').replace('caption_words=182',f'caption_words={count}')
        (P/name).write_text(s,encoding='utf-8')
    episode=f'''# Ruang untuk memilih

## Brief and authorization

- topic: Autonomy support in an everyday couple decision; room for personally endorsed choice alongside shared consequences.
- topic_selection: auto, delegated by --topic=auto; candidate 1 selected after presenting ten topics.
- board: ruang-di-antara; [editorial v1.3](../../boards/ruang-di-antara/EDITORIAL.md), [visual/audio v1.2](../../boards/ruang-di-antara/frame.md), implementation 2026-10-21.
- audience/language: Indonesian adults; natural lo–gua; complete spoken captions.
- output: 1080x1920, 30fps; 85–95s target; exactly 16 scenes, 14 cream and two charcoal.
- execution_policy: automation
- automation_after: none
- automation_state: active
- human_review: none
- human_approved: false
- pre_render_authorization: delegated by the user's --automation instruction
- requested_endpoint: publishing
- delivery: queue, next configured account slot; no custom time.
- commit: explicitly requested after pipeline completion; narrow production/tracker commit.

## Topic selection and overlap

Candidates presented: supporting choices (selected), specific apology, unspoken expectations, privacy, relationship comparison, explicit support requests, small connection invitations, supporting ideals, differing conflict memories, wanted touch. Selected autonomy support offers a concrete choice and contrasting response within 90s, supported by original relationship research. Other candidates remain unresearched editorial proposals. Tracker and production folders checked, including unregistered roda-beda-putaran. Nearest prior active-listening episode concerns understanding a difficult-event account before advice; this episode concerns personal choice and pressure in negotiating a weekend class. Shared-new-activities episode concerns mutually wanted novelty; this one preserves different interests. No duplicated central question/takeaway.

## Hook selection before script

1. “Terserah lo, katanya. Tapi kenapa pilihan yang beda masih terasa salah?” Recommended and selected: specific conditional-choice friction, answered by the response that follows.
2. “Lo minta pendapat, tapi pulang-pulang rasanya harus mengikuti pilihannya. Apa yang bergeser?” Advice becoming obligation.
3. “Bisa nggak sih dukung pasangan, walau pilihan kalian beda?” Direct question about disagreement.

Agent selected Hook 1 under immediate automation after source-body research, before SCRIPT.md. {count} spoken words. Editorial check: English term and immediate Indonesian meaning early, explanation/discussion through one scene, one connected application and closing answer. No human approval claimed.

## Publishing targets

```json
{json.dumps(snapshot,ensure_ascii=False,indent=2)}
```

Live preflight: Admin's Workspace, exact identity tuple above, @eliansatya connected, requires_approval=false / publishes_directly=true. Asia/Jakarta queue daily 14:00. Current MCP instagram_reel: one video, maximum 900s and 314572800 bytes; caption 2200 characters/five hashtags. Actual ACCOUNTS.json supersedes stale DIRECTION.md prose saying empty accounts. Actual future schedule goes in PUBLISHING.json.

## Creative and audio decisions

One fictional ceramics-class decision. Two consistent faceless organic participants, a handmade bowl/clay, Saturday calendar and shared time; open paths, constriction, response spaces and a negotiated schedule. No phone or B-roll. Exactly two dramatic scenes: 08 (closeness made conditional) and 14 (room to disagree). Large details alternate with wide conversation, response-space close-ups and time negotiation. Fixed canonical chrome/fonts; color encodes no blame or gender.

Narration: ElevenLabs / {voice} / eleven_v4, root .env voice with delivery tags. No BGM: unhurried speech, material gestures and quiet moments carry the choice without prescribing a feeling. Bundled media-use SFX inspected; retain frozen board contact/air/connection variants with hashes/credits; sparse cues only. No generated SFX. Perceptual listening unavailable; measure acoustic seams, cues and final levels honestly.

## State

Research/script agent-verified. Next: pose and inspect complete visual storyboard before synthesis/animation. HyperFrames initialized in initially empty video/. Context7 MCP unavailable; local maintained skill references and installed CLI help provide the syntax fallback. No preview started.
'''
    (P/'EPISODE.md').write_text(episode,encoding='utf-8');(V/'BRIEF.md').write_text(episode,encoding='utf-8')
    (P/'SOURCES.md').write_text('''# Research and claim boundaries

Research date: 2026-10-28. Jina searches plus selected source-body read_url passages; no trend claim. Board creative references are separate from factual evidence.

S1. Weinstein et al., Autonomy support and diastolic blood pressure: Long term effects and conflict navigation in romantic relationships. Original research / author manuscript: https://pmc.ncbi.nlm.nih.gov/articles/PMC4764637/ . Introduction defines autonomy support as supporting authentic expression, choices and values with relatively low coercion/pressure. Romantic partners respect values/interests and allow self-expression without fear of judgment or retribution; conditional affection is distinguished from autonomy support. Study 1 began with 187 couples (86% Caucasian, mostly heterosexual) and substantial follow-up attrition. This episode uses its conceptual definition, not physiological results. Observational associations do not establish that the suggested dialogue causes benefits; no blood pressure or clinical outcome claim appears in the episode.

S2. University of Rochester Center for Community Health & Prevention, Self-Determination Theory of Motivation: https://www.urmc.rochester.edu/community-health/patient-care/self-determination-theory . Institutional explanation: autonomy is willingly endorsing one's behavior; support involves acknowledging perspective/preferences, giving rationale and choice, refraining from pressure. This health-care framing corroborates the definition and broad support practices; it is not a trial of couple advice.

| Claim / scene | Evidence | Boundary |
| --- | --- | --- |
| English autonomy support and Indonesian gloss, Lines 2–3 | S1 introduction; S2 autonomy definition | Translation/explanation, no diagnosis. |
| Different preference can be voiced, reasons heard, pressure considered, Lines 5–7 | S1 self-expression and low pressure; S2 acknowledging perspective and giving rationale | Different opinion alone does not establish coercion or support. |
| Affection contingent on compliance, Line 8 | S1 unconditional versus conditional felt love | Fictional wording illustrates the distinction; one sentence cannot diagnose a person/relationship. Line 9 explicitly preserves that limit. |
| Ask importance, hear the answer and discuss own concern, Lines 10–13 | Editorial application of S1/S2, not a tested script | No guarantee of harmony. Mutual time impacts remain negotiable. |
| Room to disagree without threatened affection, Line 14 | S1 free expression without retribution and conditional affection distinction | Normative illustration, not a claim of equal responsibility in every situation. |
| Attention and clear boundaries, closing response after “terserah”, Lines 15–16 | Editorial synthesis/application | No instruction to accept harmful behavior or abandon boundaries. |

Ceramics class, Saturday preference, missing time together and dialogue are author-created fictional examples. Diagrams represent choices/interaction, not brain mechanisms, causal outcome data or measurements. No statistics are narrated. Public delivery copy links S1/S2 with concise credit.
''',encoding='utf-8')
    tracker=json.loads((ROOT/'TRACKER.json').read_text(encoding='utf-8'));assert not any(x['slug']==P.name for x in tracker['productions']);tracker['productions'].append(dict(slug=P.name,topic='Autonomy support: room for personally endorsed choices while negotiating shared time',board='ruang-di-antara',stage='storyboard',status='in_progress',path='productions/'+P.name));dump(ROOT/'TRACKER.json',tracker)
if __name__=='__main__':main()
