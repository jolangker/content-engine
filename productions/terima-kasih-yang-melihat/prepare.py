"""Freeze the new episode, preserving all existing workspace work."""
from pathlib import Path
import hashlib, importlib.util, json, shutil, subprocess

P=Path(__file__).resolve().parent; ROOT=P.parents[1]; V=P/'video'; B=ROOT/'boards/ruang-di-antara'
LINES=[
('An ordinary thank you','Makasih ya, udah masak. Apa yang sebenarnya lo hargai dari dia malam itu?','Makasih untuk apa?','intimate, conversational, curious'),
('Name the concept','Ini berkaitan dengan expressed gratitude, atau ungkapan rasa syukur: menyampaikan penghargaan atas kebaikan orang lain.','Expressed gratitude','clear, gently explanatory'),
('Two possible focuses','Dalam ucapan itu, lo bisa menceritakan manfaat buat diri lo, sekaligus menghargai tindakan dia.','Yang lo lihat',''),
('Receiving the meal','Misalnya, lo pulang capek. Makanan udah siap, jadi lo bisa langsung istirahat.','','observant, unhurried'),
('The benefit','Gua jadi nggak perlu masak. Kalimat ini menceritakan manfaat yang lo terima.','Gua terbantu',''),
('Look at the effort','Sekarang lihat tindakannya: dia meluangkan waktu, menyiapkan bahan, lalu memasak setelah kegiatannya sendiri.','','warm, attentive'),
('Name what was done','Saat lo menyebut usaha itu, ucapan terima kasih memberi tempat buat kontribusinya.','Usahanya terlihat',''),
('A person in the thank you','Orang yang membantu ikut hadir dalam ucapan lo.','Ada dia di situ','soft, reflective'),
('What research observed','Dalam penelitian percakapan pasangan, penghargaan yang berfokus pada pasangan berkaitan dengan perasaan lebih disayangi sesudahnya.','Dalam percakapan','measured, precise'),
('Preserve the limit','Temuan ini nggak menjamin satu kalimat bikin hubungan membaik, atau menghapus masalah yang perlu dibahas.','Tetap ada batas','quietly firm'),
('One genuine observation','Coba sebut satu tindakan yang benar-benar lo perhatikan. Nggak perlu pujian berlebihan.','Satu hal nyata','open, practical'),
('A concrete thank you','Makasih udah nyiapin makan walau hari lo juga padat. Gua menghargai waktu yang lo luangin.','Waktu yang lo luangin','sincere, speaking to a partner'),
('No assumption about motive','Kalau belum tahu ceritanya, tanya. Jangan mengarang pengorbanan yang dia nggak ceritakan.','Beri ruang cerita','gentle, precise'),
('Let the answer exist','Lalu beri ruang buat jawabannya, tanpa menagih balasan.','','warm, unhurried'),
('Return to the opening','Jadi, apa yang lo hargai dari makan malam tadi?','Apa yang lo hargai?',''),
('A specific ending','Coba ucapkan satu usaha nyata yang lo lihat darinya.','Sebut usahanya','intimate, reflective, leave space'),
]

def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    baseline=ROOT/'.git/terima-kasih-tracker-before.json'
    if not baseline.exists():shutil.copy2(ROOT/'TRACKER.json',baseline)
    lines=[dict(id=i,title=a,text=b,emphasis=c,delivery=d,dramatic=i in (8,10)) for i,(a,b,c,d) in enumerate(LINES,1)]
    count=sum(len(x['text'].split()) for x in lines)
    assert 170<=count<=220,count
    dump(V/'script_data.json',lines)
    spec=importlib.util.spec_from_file_location('voice_policy',ROOT/'.agents/skills/shortform-production/scripts/narration.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    voice,resolution=m.resolve_voice(ROOT)
    dump(V/'audio_request.json',dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=resolution,tts_model='eleven_v4',lines=[dict(id='narration',text='\n\n'.join((f"[{x['delivery']}] " if x['delivery'] else '')+x['text'] for x in lines))]))
    script=f'# Terima kasih yang melihat — script v1\n\n{count} spoken words. Agent-selected Hook 1 before drafting, under immediate --automation. No human approval claimed. One fictional dinner scene; no diagnostic label. English concept and Indonesian meaning are spoken in Line 2; Lines 2–10 develop its explanation and limits.\n\n'
    for x in lines:script+=f"## Line {x['id']}: {x['title']}\n\n{x['text']}\n\nOn-screen: {x['emphasis'] or '(none)'}. Timing: estimated until native alignment. Delivery: {x['delivery'] or 'continue naturally'}.\n\n"
    (P/'SCRIPT.md').write_text(script,encoding='utf-8');(V/'SCRIPT.md').write_text(script,encoding='utf-8')
    (V/'assets/fonts').mkdir(parents=True,exist_ok=True)
    for f in (B/'assets').iterdir():
        if f.is_file() and f.suffix in ('.ttf','.txt'):shutil.copy2(f,V/'assets/fonts'/f.name)
    shutil.copy2(B/'frame.md',V/'frame.md');shutil.copytree(B/'components',V/'assets/board/components',dirs_exist_ok=True);shutil.copytree(B/'assets/audio/sfx',V/'assets/board/audio/sfx',dirs_exist_ok=True)
    (V/'vendor').mkdir(exist_ok=True);shutil.copy2(ROOT/'productions/coba-hal-baru-berdua/video/vendor/gsap.min.js',V/'vendor/gsap.min.js')
    snapshot=dict(source='board',board_accounts_file='boards/ruang-di-antara/ACCOUNTS.json',board_accounts_sha256=hashlib.sha256((B/'ACCOUNTS.json').read_bytes()).hexdigest(),accounts=json.loads((B/'ACCOUNTS.json').read_text(encoding='utf-8'))['accounts']);dump(P/'target_snapshot.json',snapshot)
    episode=f'''# Terima kasih yang melihat

## Brief and execution

- topic: Expressed gratitude that recognizes a partner's praiseworthy action, alongside benefits received.
- topic_selection: delegated by --topic=auto; selected candidate 1 from the ten presented before file creation.
- board: ruang-di-antara, [editorial v1.3](../../boards/ruang-di-antara/EDITORIAL.md), [visual/audio v1.2](../../boards/ruang-di-antara/frame.md), implementation 2026-10-21.
- audience/language: Indonesian adults; intimate lo–gua narration and complete spoken captions.
- output: 1080x1920, 30 fps, approximately 90 seconds, 16 scenes, 14 cream / 2 charcoal.
- execution_policy: automation
- automation_after: none
- automation_state: active
- human_review: none
- human_approved: false
- pre_render_authorization: delegated by the user's --automation instruction
- requested_endpoint: publishing
- delivery: queue, next configured slot; no custom time requested.
- commit: requested after pipeline completion; isolate this production and its tracker row from pre-existing jangan-sahut board work.

## Topic and overlap

Ten candidates: specific gratitude (selected), relationship attributions, empathic accuracy, autonomy support, stress spillover, implementation intentions, gradual self-disclosure, sacrifice motivation, apology responsibility/repair, and overgeneralization. These were topic directions, not verified factual claims. Specific gratitude adds an affirmative relational episode with a strong primary observational source and a legible dinner scene. Compared existing tracker/folders and recent scripts: kabar-baik concerns responding to another's good news; this concerns thanking a benefactor for their action. Other episodes cover listening, conflict pauses, transparency and shared novel experiences. Different audience question, scenario and takeaway. Slug was absent before initialization.

## Hook selection before script

1. “Makasih ya, udah masak.” Apa yang sebenarnya lo hargai dari dia malam itu? Everyday dialogue; promises an examination of the focus of thanks. Recommended and selected.
2. Lo lega karena dibantu. Dia tahu nggak bagian mana dari usahanya yang lo lihat? Recipient viewpoint; promises attention to the contribution.
3. Dua ucapan terima kasih bisa menyebut hal yang berbeda. Yang satu hasilnya; yang satu usahanya. Bedanya apa? Comparison; promises a distinction.

Agent selected Hook 1 under delegated automation after source-body research, before SCRIPT.md. It offers a concrete situation and returns to the same question without declaring anyone ungrateful. Script v1: {count} spoken words, agent editorial check; no human approval.

## Publishing targets

publishing_targets:
```json
{json.dumps(snapshot,ensure_ascii=False,indent=2)}
```

Preflight 2026-10-27: Admin's Workspace, exact account @eliansatya connected; requires_approval=false, publishes_directly=true. Current MCP Instagram reel: one video, maximum 900 seconds / 314572800 bytes; caption 2200 characters, five hashtags. Queue uses configured Asia/Jakarta times; actual returned schedule will be recorded in PUBLISHING.json. Actual ACCOUNTS.json supersedes stale board prose about an empty list.

## Creative and audio

One fictional dinner: organic pair, prepared meal, stove/pot, ingredients, clock, speech spaces and contribution traces. Vary wide pair, overhead meal, close effort sequence, person/words, bounded study illustration and reciprocal exchange. Fixed canonical chrome and typography; full captions. Dark Frame 8 puts the benefactor in the thanks; dark Frame 10 limits the finding. Exactly two inversions, no B-roll or diagnostic/gender color coding.

Narration: ElevenLabs / {voice} / eleven_v4, root .env voice, one tagged full-script request, native speed. No BGM: material cooking details, speech and pauses serve the intimate exchange without a sentimental promise. SFX: use sparse frozen board contact/air/connection assets after inspecting the bundled UI-oriented library; no automatic transition effects. Silence at the caveat and final hold. Provenance and actual cue alignment required.

## Current state

Research and script agent-verified. Next: pose and verify all 16 static scenes and the complete storyboard PNG before synthesis or animation. No preview server started.
'''
    (P/'EPISODE.md').write_text(episode,encoding='utf-8')
    (P/'SOURCES.md').write_text('''# Research and claim boundaries

Research date: 2026-10-27. Jina search discovered the primary paper; focused Jina read_url retrieved its actual body, methods, definitions, results and discussion. No factual claim relies on search snippets. No trend claim.

S1. Algoe, S. B., Kurtz, L. E., & Hilaire, N. M. (2016). Putting the “You” in “Thank You”: Examining Other-Praising Behavior as the Active Relational Ingredient in Expressed Gratitude. Social Psychological and Personality Science, 7(7), 658–666. https://pmc.ncbi.nlm.nih.gov/articles/PMC4988174/ . Original study and conceptual replication across three samples, 370 naturalistic couple conversations. Observers coded other-praising (recognition of praiseworthy actions/qualities) separately from self-benefit statements. More other-praising was associated with recipients perceiving greater expresser responsiveness, positive feelings and felt loving after the conversation. This specific behavioral association is observational; do not claim randomly assigning a phrase caused enduring improvement. Sample context includes heterosexual US couples; not evidence of universality or an Indonesian validated intervention. No numerical effect size is narrated.

## Claim map

| Claim | Wording and support | Limits |
| --- | --- | --- |
| C1 | Expressed gratitude, Indonesian gloss ungkapan rasa syukur, conveys appreciation for another's kindness. Lines 2–3. | S1 theoretical and operational discussion. Established construct, not a diagnosis. |
| C2 | Gratitude expressions can describe both benefit received and the benefactor's action. Lines 3–8. | S1 separates other-praising and self-benefit; they are not mutually exclusive and the script says sekaligus. No claim that self-benefit is bad or invalid. |
| C3 | Partner-focused appreciation in couple conversations was associated with more felt loving afterward. Line 9. | S1 results; berkaitan preserves association. No guaranteed emotional response, causal mechanism or long-term outcome. |
| C4 | One sentence does not guarantee improved relationship or erase other issues. Line 10. | Boundary of S1: this is not a treatment or conflict-resolution trial. |
| C5 | Dinner, tired arrival, shopping/preparation/clock and time spent. Lines 1,4–8,12. | Fictional illustrative scene; author-created objects and dialogue are not observations of a real person or a tested task. |
| C6 | Mention one real action; ask rather than invent effort; allow a response without demanding reciprocity. Lines 11–16. | Editorial application, not a validated script/protocol or promise of gratitude. |

Visual contribution paths and speech spaces are illustrative metaphors, not measured psychological states. No percentages, diagnostic advice, hidden-motive assertions or therapeutic promises. Public copy credits S1 and links the original source. Creative reference: approved board, kept separate from research evidence.
''',encoding='utf-8')
    brief=episode.split('## Current state')[0];(V/'BRIEF.md').write_text(brief,encoding='utf-8')
    tracker=json.loads((ROOT/'TRACKER.json').read_text(encoding='utf-8'));assert not any(x['slug']==P.name for x in tracker['productions']);tracker['productions'].append(dict(slug=P.name,topic='Expressed gratitude: recognizing a partner’s contribution alongside benefits received',board='ruang-di-antara',stage='storyboard',status='in_progress',path='productions/'+P.name));dump(ROOT/'TRACKER.json',tracker)
    print(json.dumps(dict(words=count,scenes=16,provider='elevenlabs',model='eleven_v4',audio_generated=False)))

if __name__=='__main__':main()
