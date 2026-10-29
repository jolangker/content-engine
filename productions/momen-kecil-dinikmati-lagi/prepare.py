"""Freeze the episode and adapt verified board utilities without modifying earlier work."""
from pathlib import Path
import hashlib, json, shutil, sys
P=Path(__file__).resolve().parent; R=P.parents[1]; V=P/'video'; B=R/'boards/ruang-di-antara'; OLD=P.parent/'maaf-yang-menyebut-tindakan'
LINES=[
('Duduk di dapur','Cuma duduk berdua di dapur. Kenapa momen sekecil itu masih terasa hangat waktu lo ingat lagi?','Momen kecil','intimate, conversational, curious'),
('Nama konsep','Ada konsep relational savoring, atau menikmati kembali momen kedekatan dalam hubungan.','Relational savoring','clear, gently explanatory'),
('Memberi perhatian','Artinya, lo sengaja memberi perhatian pada pengalaman positif ketika merasa terhubung dengan seseorang.','Nikmati kembali',''),
('Satu kejadian','Misalnya, malam itu lo pulang capek. Dia menemani lo bikin teh.','','warm, observant'),
('Detail yang tinggal','Yang lo ingat bisa sesederhana dua cangkir, suara air, dan dia duduk di sebelah.','',''),
('Tinggal sebentar','Saat mengingatnya, lo tinggal sebentar pada detail itu, sambil memperhatikan perasaan yang muncul.','Tinggal sebentar','unhurried, reflective'),
('Makna kedekatan','Bagian pentingnya: apa yang bikin lo merasa dekat dalam kejadian itu?','Apa yang terasa dekat?','curious, gentle'),
('Pengalaman pribadi','Buat gua, mungkin karena malam itu gua merasa ditemani, tanpa harus banyak ngomong.','Gua merasa ditemani','quietly warm'),
('Satu momen','Fokusnya satu pengalaman yang nyata buat lo, dengan makna yang lo rasakan sendiri.','','clear, grounded'),
('Bukan kesimpulan','Satu kenangan hangat nggak berarti seluruh hubungan selalu baik, atau masalahnya sudah selesai.','Satu momen','quietly firm'),
('Pilih kenangan','Kalau mau mencoba, pilih satu momen kecil ketika lo merasa dekat.','Ingat satu momen','warm, inviting'),
('Buka detailnya','Ingat tempatnya, apa yang terjadi, lalu perhatikan bagian yang terasa berarti buat lo.','',''),
('Boleh dibagikan','Kalau ingin cerita ke dia, bisa bilang: gua suka waktu kita bikin teh kemarin.','','speaking gently to a partner'),
('Sebut maknanya','Gua ngerasa ditemani. Itu contoh berbagi pengalaman lo, tanpa menuntut perasaan yang sama.','Tanpa menuntut','open, gentle'),
('Kembali ke dapur','Jadi, momen sederhana tadi bisa lo datangi lagi lewat ingatan yang diberi perhatian.','Datangi lagi','reflective'),
('Detail penutup','Dua cangkir. Satu malam. Bagian mana yang masih terasa hangat buat lo?','Bagian mana?','soft, intimate, reflective'),
]
def dump(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    assert not (V/'script_data.json').exists(), 'Intake already frozen; resume the existing episode.'
    lines=[dict(id=i,title=t,text=text,emphasis=e,tags=tag,dramatic=i in (8,10)) for i,(t,text,e,tag) in enumerate(LINES,1)]
    count=sum(len(x['text'].split()) for x in lines)
    assert 170<=count<=215,count
    snapshot=dict(source='board',board_accounts_file='boards/ruang-di-antara/ACCOUNTS.json',board_accounts_sha256=hashlib.sha256((B/'ACCOUNTS.json').read_bytes()).hexdigest(),accounts=json.loads((B/'ACCOUNTS.json').read_text(encoding='utf-8'))['accounts'])
    dump(P/'target_snapshot.json',snapshot)
    episode='''# Momen kecil, dinikmati lagi

## Resolved intake

- topic_selection: auto; selected candidate 1 of 10 presented in conversation, delegated by --topic=auto.
- Topic: relational savoring, attending to a specific positive memory of connectedness.
- Angle: a fictional ordinary evening making tea; attention to sensory details and personally experienced meaning. No clinical or guaranteed relationship outcome.
- Board: [Ruang di Antara editorial v1.3](../../boards/ruang-di-antara/EDITORIAL.md), [visual v1.2 / implementation 2026-10-21](../../boards/ruang-di-antara/frame.md), audio v1.2.
- Audience: Indonesian adults; natural lo–gua Indonesian; 1080x1920/30fps Instagram Reel, approximately 90 seconds; exactly sixteen scenes and two charcoal scenes (08, 10).
- execution_policy: automation
- automation_after: none
- automation_state: active
- human_review: none
- human_approval: false
- pre_render_authorization: delegated by the user's --automation instruction
- requested_endpoint: publishing
- delivery: queue; each account's next configured free slot; no invented custom time.
- Commit requested after the pipeline finishes. Preserve pre-existing working-tree changes and commit only this production plus its tracker entry.
- Narration: ElevenLabs / eleven_v4, root .env voice; one full tagged continuous take. Native speed.
- BGM: none; sensory memory and reflective pauses benefit from open space rather than an emotional music bed.
- SFX: use sparse frozen board contact/air/connection cues after inspecting the bundled media-use library. Bright UI sounds and impacts do not fit this kitchen-memory treatment. No automatic cut sounds; final reflection quiet.

## Topic selection and overlap

Ten candidates presented: relational savoring; partner phubbing; stress spillover; dyadic coping; co-rumination; shared rituals; perceived fairness in tasks; social comparison; invisible support; updating knowledge of a partner. Candidate 1 best combines positive connection, a concrete visual scene, clear definition from its developers, and no efficacy promise.

Tracker and production folders checked. Distinct from kabar-baik (response to new good news), terima-kasih-yang-melihat (recognizing another's contribution), coba-hal-baru-berdua (new shared activity), and cerita-belum-selesai (listening before advice). This episode attends to one's own existing memory. The unregistered roda-beda-putaran folder is a mechanical production and has no editorial overlap. No second episode is started.

## Preflight

Trypost MCP workspace Admin's Workspace, ID 01a171dd-5281-730d-af07-f2168d17add7; actor is admin, requires_approval=false, publishes_directly=true. Board account 01a172ed-9899-7177-ab1e-627c835e4a57 is connected Instagram @eliansatya. Queue configured daily 14:00 Asia/Jakarta. Content type instagram_reel, 900s / 314572800-byte ceilings, max five hashtags, 2200 caption characters. Reverify current returned scheduling result before completion. DIRECTION.md account prose is stale; actual ACCOUNTS.json contains the authoritative selected identity.

## Hook checkpoint, before script drafting

1. “Cuma duduk berdua di dapur. Kenapa momen sekecil itu masih terasa hangat waktu lo ingat lagi?” Concrete recalled scene; promise: explain attention to a moment of connection.
2. “Kalau diminta mengingat satu momen dekat minggu ini, kenapa yang muncul justru obrolan sambil bikin teh?” Memory selection; promise: explore personally meaningful details.
3. “Momen baiknya udah lewat. Masih bisa lo nikmati lagi?” Direct question; promise: define savoring a remembered moment.

Recommendation and choice: Hook 1, selected by the agent under immediate automation after source reading, before SCRIPT.md. It provides a specific scene without an efficacy claim. No human approval claimed.

## Publishing target snapshot

```json
'''+json.dumps(snapshot,ensure_ascii=False,indent=2)+'''\n```

## Verification and next action

Research resolved; definition and illustrative adaptation boundaries mapped in SOURCES.md. Proceed through script, complete visual storyboard, measured narration, animation, verification, preview, verified export, package and actual queue scheduling. Technical and creative checks remain required under automation.
'''
    (P/'EPISODE.md').write_text(episode,encoding='utf-8')
    tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8-sig'))
    assert not any(x['slug']==P.name for x in tracker['productions'])
    tracker['productions'].append(dict(slug=P.name,topic='Relational savoring: attending to a specific positive memory of connectedness through an ordinary shared tea-making scene',board='ruang-di-antara',stage='script',status='in_progress',path='productions/'+P.name));dump(R/'TRACKER.json',tracker)
    sources='''# Research and evidence boundaries

Research accessed 2026-10-30 via Jina search_web and read_url, including the selected article body. No claim that this is trending.

## Core source

[Borelli and colleagues (2024), Culturally adapting relational savoring: A therapeutic approach to improve relationship quality](https://pmc.ncbi.nlm.nih.gov/articles/PMC11245364/). A developer-authored protocol and cultural-adaptation article. Read the definition, memory selection, memory reflection, cultural context and clinical cautions. It describes attention to specific positive experiences of connection, often giving or receiving sensitive care. Reflection includes concrete sensory and emotional details and personal meaning. Its structured intervention includes additional preparation and facilitated work; this short episode is an educational illustration, not that intervention.

## Claim map

| Claim / script spans | Support and qualification |
| --- | --- |
| Relational savoring refers to attending to a positive experience of connection (02–03). | Article definition and protocol. “Menikmati kembali momen kedekatan” is a descriptive Indonesian rendering, not a standardized clinical translation. |
| Recall a specific positive memory, its details, emotions and meaning (06–07, 09, 11–12, 15). | Memory-selection/reflection sections. Our tea scene is fictional and does not claim proven benefit from this brief adaptation. |
| Scene: tired arrival, tea, company, felt warmth (01, 04–05, 08). | Fictional illustration of subjective experience. Warmth is this speaker's possible experience, not an inevitable effect or evidence of the partner's intent. |
| A positive memory does not establish the whole relationship's quality or resolve ongoing problems (10). | Editorial evidence limit. The source does not validate that inference. No treatment, safety, repair or forgiveness promise is made. |
| Optional line to share a memory without requiring a matching feeling (13–14). | Creative communication example, not a tested component or outcome claim. |
| Closing question (16). | Invitation to personal observation; no required response or diagnosis. |

## Limits

Evidence about outcomes is not narrated. Findings in clinical, parenting, long-distance or culturally specific samples are not generalized to Indonesian viewers. No neurobiological mechanism, duration/dose prescription, fixed habit or universal nostalgia claim. These figures and connecting traces indicate attention, remembered context and subjective meaning; they do not depict changes in relationship quality.

## Discovery leads, not script evidence

Searches also returned partner responsiveness (PMC5922804), sleep/conflict (PMC9249692), and partner phubbing (Frontiers DOI 10.3389/fpsyg.2025.1561159). Those were feasibility leads for alternatives; no claim from them enters this episode. The chosen article is sufficient for the narrow definition and memory-reflection process used here.
'''
    (P/'SOURCES.md').write_text(sources,encoding='utf-8')
    dump(V/'script_data.json',lines)
    script=f'# Momen kecil, dinikmati lagi — script v1\n\nLanguage: Indonesian (lo–gua). {count} spoken whitespace-delimited words. Hook 1 agent-selected before drafting. One concept; scenes 02–09 explain/discuss it. All dialogue and tea details are fictional illustrations. Estimated 90 seconds; replace estimates with native audio timing.\n\n'
    for x in lines:script+=f"## Scene {x['id']:02d}: {x['title']}\n\n{x['text']}\n\nEmphasis: {x['emphasis'] or '(none)'}. Palette: {'charcoal' if x['dramatic'] else 'cream'}.\n\n"
    for dest in (P/'SCRIPT.md',V/'SCRIPT.md'):dest.write_text(script.rstrip()+'\n',encoding='utf-8')
    (V/'assets/fonts').mkdir(parents=True,exist_ok=True)
    for f in (B/'assets').iterdir():
        if f.is_file() and f.suffix in ('.ttf','.txt'):shutil.copy2(f,V/'assets/fonts'/f.name)
    shutil.copy2(B/'frame.md',V/'frame.md');shutil.copytree(B/'components',V/'assets/board/components',dirs_exist_ok=True);shutil.copytree(B/'assets/audio/sfx',V/'assets/board/audio/sfx',dirs_exist_ok=True)
    (V/'vendor').mkdir(exist_ok=True);shutil.copy2(OLD/'video/vendor/gsap.min.js',V/'vendor/gsap.min.js')
    for name in ('visuals.py','animate.py','capture_board.py','capture_stills.py','qa.py','capture_motion.py','seek_qa.py','preview_qa.py','cleanup_preview.py','verify_export.py','prepare_audio.py','finish_audio.py','exact_seams.py','verify_cut_frames.py','state.py'):
        s=(OLD/name).read_text(encoding='utf-8').replace(OLD.name,P.name).replace('Maaf yang menyebut tindakan','Momen kecil, dinikmati lagi')
        s=s.replace('==183',f'=={count}').replace('183 aligned',f'{count} aligned').replace('caption_words=183',f'caption_words={count}').replace('in (9,14)','in (8,10)').replace('in (9, 14)','in (8, 10)').replace('09 and 14','08 and 10').replace('09/14','08/10')
        (P/name).write_text(s,encoding='utf-8')
    # Build the request only from the root .env voice resolver, never print credentials.
    sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'));import narration
    voice,resolution=narration.resolve_voice(R)
    dump(V/'audio_request.json',dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=dict(source='project_env',key='ELEVENLABS_VOICE_ID'),tts_model='eleven_v4',lines=[dict(id='narration',text='\n\n'.join(('['+x['tags']+'] ' if x['tags'] else '')+x['text'] for x in lines))]))
    (V/'BRIEF.md').write_text(episode+f'\nScript v1 agent-verified before static storyboard: {count} words. Exact pipeline endpoint is publishing/queue.\n',encoding='utf-8')
    print(json.dumps(dict(words=count,scenes=len(lines),board='ruang-di-antara',stage='script')))
if __name__=='__main__':main()
