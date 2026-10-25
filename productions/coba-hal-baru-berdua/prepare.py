"""Freeze this episode's script, brief and self-contained board assets."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import shutil

P=Path(__file__).resolve().parent; ROOT=P.parents[1]; V=P/'video'; BOARD=ROOT/'boards/ruang-di-antara'
LINES=[
('The familiar evening','Makan di tempat yang sama, pulang lewat jalan yang sama. Kok waktu berdua terasa itu-itu lagi?','Itu-itu lagi?','intimate, conversational, curious'),
('The concept','Ada konsep self-expansion, atau perluasan diri: bertambahnya pengalaman, kemampuan, atau cara pandang kita.','Self-expansion','clear, gently explanatory'),
('A shared route','Dalam hubungan, salah satu jalannya: mencoba hal baru dan menarik bersama.','Pengalaman baru',''),
('The repeated weekend','Misalnya, tiap akhir pekan kalian makan, lalu pulang. Nyaman, tapi kali ini terasa datar.','','observant, unhurried'),
('What might be missing','Kebersamaannya ada. Yang terasa kurang bisa jadi kesempatan mengalami sesuatu yang belum biasa.','Ada ruang?',''),
('The recipe','Saat belajar resep baru, kalian sama-sama belum tahu hasilnya.','Belum tahu','warm, quietly curious'),
('Taking turns','Lo mencoba menguleni, dia membaca langkahnya. Lalu bergantian saat adonannya susah dibentuk.','',''),
('Another side','Ada sisi pasangan yang baru kelihatan ketika kalian menghadapi hal yang belum dikuasai.','Sisi yang baru','soft, reflective'),
('The research boundary','Penelitian menemukan kegiatan baru dan menggugah bersama dapat meningkatkan penilaian kualitas hubungan sesaat setelahnya.','Sesaat setelahnya','measured, precise'),
('An important limit','Ini nggak menjamin hubungan membaik terus, atau menyelesaikan masalah yang dibiarkan.','Bukan jaminan','quietly firm'),
('A small experiment','Mulai dari satu percobaan kecil yang kalian berdua ingin coba.','Sama-sama ingin','open, inviting'),
('An invitation','Gua pengen bikin sesuatu bareng. Sabtu kita coba resep ini, mau?','Coba bareng?','sincere, speaking to a partner'),
('Room to choose','Kalau dia nggak tertarik, cari pilihan lain bersama. Nggak perlu memaksa.','Boleh pilih lain','gentle, practical'),
('After trying','Selesai mencoba, tanyakan: bagian mana yang paling lo nikmati tadi?','Bagian mana?','curious, warmly interested'),
('The shared experience','Yang dicari: pengalaman baru yang dibagi, tanpa harus sempurna atau mahal.','Pengalaman bersama',''),
('Return to the evening','Kalau waktu berdua terasa itu-itu lagi, hal kecil apa yang ingin kalian pelajari bareng?','Belajar apa bareng?','intimate, reflective, leave space'),
]

def write_json(path,data): path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    tracker=json.loads((ROOT/'TRACKER.json').read_text(encoding='utf-8'))
    assert not any(x['slug']==P.name for x in tracker['productions']), 'Production exists; resume its recorded stage instead of rerunning intake'
    spec=importlib.util.spec_from_file_location('narration_policy',ROOT/'.agents/skills/shortform-production/scripts/narration.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    voice,resolution=mod.resolve_voice(ROOT)
    lines=[dict(id=i+1,title=a,text=b,emphasis=c,delivery=d,dramatic=i+1 in (8,10)) for i,(a,b,c,d) in enumerate(LINES)]
    count=sum(len(x['text'].split()) for x in lines)
    assert 170<=count<=200,count
    write_json(V/'script_data.json',lines)
    script=f'''# SCRIPT — Coba hal baru berdua

Version 1; {count} spoken words. Agent-verified under immediate automation; no human approval claimed.
One fictional couple and shared cooking scene illustrate the concept. No diagnostic inference.

Voice: ElevenLabs / {voice} / eleven_v4; root .env default, native speed 1, one continuous request.
The English concept and Indonesian meaning are spoken in Line 2. Lines 2–10 develop the concept and its limits; Lines 11–16 derive one shared experiment and answer the opening.

'''
    for x in lines:
        script+=f"## Line {x['id']} — {x['title']} (Frame {x['id']})\n\n**Time:** Estimated; replace with measured alignment.\n**Delivery:** {x['delivery'] or 'Continue naturally.'}\n\n    {x['text']}\n\n**On-screen:** {x['emphasis'] or 'No emphasis copy.'}\n\n"
    script+='''## Claim verification

SOURCES.md C1–C4 map the definition, shared activity route, short-term finding and limits. The cooking example, mutual choice, budget and reflection questions are editorial applications, not tested recipes or guaranteed interventions. Routine and comfort are not pathologized. Dramatic frames 8 and 10 emphasize discovery and the limit of the finding respectively.
'''
    (P/'SCRIPT.md').write_text(script,encoding='utf-8');(V/'SCRIPT.md').write_text(script,encoding='utf-8')
    request=dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=resolution,tts_model='eleven_v4',speed=1,lines=[dict(id='narration',text='\n\n'.join((f"[{x['delivery']}] " if x['delivery'] else '')+x['text'] for x in lines))],bgm=dict(mode='none'))
    write_json(V/'audio_request.json',request)
    (V/'assets/fonts').mkdir(parents=True,exist_ok=True)
    for f in (BOARD/'assets').iterdir():
        if f.is_file() and f.suffix in ('.ttf','.txt'):shutil.copy2(f,V/'assets/fonts'/f.name)
    shutil.copy2(BOARD/'frame.md',V/'frame.md');shutil.copytree(BOARD/'components',V/'assets/board/components',dirs_exist_ok=True);shutil.copytree(BOARD/'assets/audio/sfx',V/'assets/board/audio/sfx',dirs_exist_ok=True)
    (V/'vendor').mkdir(exist_ok=True);shutil.copy2(ROOT/'productions/jeda-punya-waktu-kembali/video/vendor/gsap.min.js',V/'vendor/gsap.min.js')
    accounts=json.loads((BOARD/'ACCOUNTS.json').read_text(encoding='utf-8'))['accounts'];ah=hashlib.sha256((BOARD/'ACCOUNTS.json').read_bytes()).hexdigest()
    snapshot=dict(source='board',board_accounts_file='boards/ruang-di-antara/ACCOUNTS.json',board_accounts_sha256=ah,accounts=accounts)
    write_json(P/'target_snapshot.json',snapshot)
    (P/'EPISODE.md').write_text(f'''# Coba hal baru berdua

## Brief and authority

- topic: Shared self-expansion through a mutually wanted novel activity in an ordinary couple relationship.
- topic_selection: auto, delegated by the user's --topic=auto.
- board: ruang-di-antara; [editorial v1.3](../../boards/ruang-di-antara/EDITORIAL.md), [visual/audio v1.2](../../boards/ruang-di-antara/frame.md), implementation 2026-10-21. Board files remain unchanged.
- audience: Indonesian adults; intimate lo–gua, id narration and captions.
- format: 1080×1920, 30 fps, approximately 90 seconds, exactly 16 scenes and two charcoal inversions.
- execution_policy: automation
- automation_after: none
- automation_state: active
- human_review: none
- pre_render_authorization: delegated by the user's --automation instruction
- requested_endpoint: publishing
- delivery: queue; next configured slot, no --at supplied.
- commit: explicitly requested after pipeline completion.
- human_approved: false

## Topic selection and overlap check

Ten candidates were presented before production: shared self-expansion (selected), specific gratitude, divided phone attention, attribution of short replies, autonomy-supportive goal support, stress spillover, renewed curiosity, difference within closeness, gradual reciprocal self-disclosure, and positive reminiscence. Self-expansion best adds a positive shared-activity episode with a credible original experimental evidence path and strong visual action. Alternatives remain unproduced candidates, not verified claims.

Compared tracker topics and the scripts for kabar-baik, cerita-belum-selesai, jeda-punya-waktu-kembali and gua-kira-udah-kelihatan. This episode concerns new experiences during time together, rather than responding to good news, listening before advice, agreed returns from conflict pauses, or visibility of feelings. No existing folder uses this slug. One new episode only.

## Hooks — selected before script drafting

1. “Makan di tempat yang sama, pulang lewat jalan yang sama. Kok waktu berdua terasa itu-itu lagi?” Recognizable routine; promises an explanation and one small shared experiment. Recommended and agent-selected under delegated automation.
2. “Kapan terakhir lo melihat pasangan mencoba sesuatu yang belum dia kuasai?” Curiosity about an unfamiliar side; promises a shared-learning angle.
3. “Kalender kalian penuh waktu berdua. Pengalaman barunya masih kebagian tempat?” Activity versus novelty; promises a closer look at the content of time together.

Hook 1 is selected because its concrete opening and return question support one continuous cooking story without assuming a relationship defect. SCRIPT.md was written after this choice. Script v1 has {count} spoken words; agent editorial verification passed, no human script approval claimed.

## Publishing targets

publishing_targets:
```json
{json.dumps(snapshot,ensure_ascii=False,indent=2)}
```

Preflight: Admin's Workspace; exact @eliansatya connected; me.requires_approval=false, me.publishes_directly=true. Instagram reel accepts one video, up to 900s and 314572800 bytes, maximum five hashtags, caption limit 2200 characters. Configured slots 14:00 and 19:00 Asia/Jakarta every day; use queue next, retain actual returned time. No custom schedule invented. The stale prose in board DIRECTION.md says accounts are empty, but the actual ACCOUNTS.json and live MCP account agree; that actual list is the inherited source of truth.

## Creative and audio decisions

Faceless organic pair with distinct silhouettes (charcoal and brick, no gender/blame coding), illustrated table, plates, route, mixing bowl, dough and recipe. Preserve canonical fixed chrome and full spoken captions. Exactly two charcoal turns: Frame 8 reveals a new view of the partner; Frame 10 holds the limits of the finding. No B-roll. Required static storyboard artifacts will be agent-verified before audio/animation despite storyboard:no.

Narration: ElevenLabs / {voice} / eleven_v4, source root .env, one continuous full-script request; no provider/model substitution. BGM intentionally absent: quiet kitchen details and pauses leave the outcome open rather than promising celebration. SFX: reuse frozen licensed board material sounds for real action and connection; no transition quota, silence at the limitation and closing hold. Final cues must follow measured speech and motion.

## Current state

Script and research verified. Next: complete static styled storyboard and inspect all sixteen scenes, then synthesize and measure narration. No preview server created yet. Preserve pre-existing uncommitted gua-kira-udah-kelihatan and its tracker changes separately from this episode's commit.
''',encoding='utf-8')
    (P/'SOURCES.md').write_text('''# Sources and claim boundaries

Research date: 2026-10-26. Jina search was used for discovery; selected source bodies were read. PubMed and ResearchGate returned bot challenges, so the original study abstract was read through Europe PMC. No claim relies on a search snippet.

## Read sources

S1. Aron, A., Norman, C. C., Aron, E. N., McKenna, C., & Heyman, R. E. (2000). Couples' shared participation in novel and arousing activities and experienced relationship quality. Journal of Personality and Social Psychology, 78(2), 273–284. Original study abstract: https://europepmc.org/article/MED/10707334 ; DOI https://doi.org/10.1037/0022-3514.78.2.273 . Read abstract: newspaper questionnaire, door-to-door survey and three laboratory experiments. The experiments compared a seven-minute novel/arousing joint task with a mundane task, with a no-activity comparison supporting a task effect. Relationship quality was assessed before/after; observational discussion ratings also showed the effect. Abstract only, not a full-methods audit. No numerical effect size or universal success rate is used.

S2. Self-Expansion Activities with a Partner as One Path to Well-Being. Open research review: https://pmc.ncbi.nlm.nih.gov/articles/PMC13203665/ . Read definition, shared activity discussion, and conclusions. The model describes expanding resources, knowledge, capabilities and perspectives, including through relationships; shared novel/challenging activities are one route. Review notes more cross-cultural and long-term research is needed. Used for terminology and context, not a promise of health or therapeutic effects. No well-being claim appears in the narration.

## Claim map

| ID | Script/visual implication | Evidence and limit |
| --- | --- | --- |
| C1 | Self-expansion means adding experiences, capabilities or perspectives. Line 2. | S2's theoretical definition; accessible Indonesian gloss, not a diagnostic category. |
| C2 | Shared new and interesting activities are one route in a relationship. Lines 3, 5–8. | S1 experimental activity context and S2 model. A possible avenue, not the sole cause or cure for routine. |
| C3 | Novel, arousing shared activities can improve experienced relationship-quality ratings immediately afterward. Line 9. | S1's pre/post experimental abstract. Narration explicitly says sesaat setelahnya. No guarantee of durable change, no claim cooking was the tested task. |
| C4 | No guarantee of continuing improvement or resolution of neglected problems. Line 10. | Boundary of S1's short pre/post result and S2's long-term research qualification; the study does not test curing unresolved problems. |
| C5 | The couple's weekend feels flat, they knead/read/swap roles and notice a new side. Lines 1, 4–8. | Fictional illustrative scene. No assertion of another person's hidden motive, no measured causal mechanism. Visual paths and experience marks are metaphors, not data. |
| C6 | Choose an affordable mutually wanted experiment, allow alternatives and ask what was enjoyable. Lines 11–16. | Editorial application derived from the shared activity idea; not a tested protocol, price threshold or promised outcome. Mutual willingness is explicit; comfort and routine remain legitimate. |

No mental-health diagnosis, crisis advice, neuroscience mechanism, demographic generalization, or claim of a trend. Source attribution belongs in the public caption. Separate firsthand listening from objective verification in the eventual verification record.
''',encoding='utf-8')
    (V/'capture/extracted').mkdir(parents=True,exist_ok=True)
    (V/'capture/extracted/visible-text.txt').write_text('User invocation: $shortform-production --board=ruang-di-antara --topic=auto --delivery=queue --automation\nCommit after pipeline finished.\n\nSelected topic: shared self-expansion through one mutually wanted novel experience.\n\n'+script,encoding='utf-8')
    write_json(V/'capture/extracted/tokens.json',dict(title='Coba hal baru berdua',description='Shared self-expansion, bounded to a small mutually wanted experiment.',colors=['#F3EDE3','#302B28','#A34F3F','#D8C8B5'],fonts=['Newsreader','DM Sans']))
    tracker=json.loads((ROOT/'TRACKER.json').read_text(encoding='utf-8'))
    assert not any(x['slug']==P.name for x in tracker['productions'])
    tracker['productions'].append(dict(slug=P.name,topic='Shared self-expansion through mutually wanted novel activities in an ordinary couple relationship',board='ruang-di-antara',stage='storyboard',status='in_progress',path='productions/'+P.name));write_json(ROOT/'TRACKER.json',tracker)
    print(json.dumps(dict(words=count,voice=voice,model='eleven_v4',scenes=len(lines),synthesis_started=False)))
if __name__=='__main__':main()
