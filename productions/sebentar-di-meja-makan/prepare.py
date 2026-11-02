"""Freeze the delegated episode brief and inherit reusable board implementation."""
from pathlib import Path
import hashlib, importlib.util, json, shutil, sys

P=Path(__file__).resolve().parent; R=P.parents[1]; V=P/'video'; B=R/'boards/ruang-di-antara'; OLD=P.parent/'deadline-dan-cucian'
LINES=[
('Sebentar di meja makan',"Sebentar, katanya sambil lihat HP. Kenapa cerita lo jadi berhenti di meja makan?",'Sebentar?','intimate, conversational, curious'),
('Nama konsep','Ada konsep partner phubbing, atau mengabaikan pasangan karena perhatian beralih ke ponsel.','Partner phubbing','clear, gently explanatory'),
('Interaksi yang tersela','Ini membahas saat HP menyela interaksi yang sedang kalian jalani bersama.','',''),
('Cerita dan notifikasi','Misalnya, lo lagi cerita soal kejadian di kantor. Dia membuka notifikasi.','','observant, grounded'),
('Bagian yang terlewat','Terus, katanya. Tapi lo harus mengulang bagian yang barusan lewat.','Barusan sampai mana?',''),
('Apa yang terlihat','Di sini, yang terlihat adalah cerita terputus dan perhatian yang berpindah.','','clear, explanatory'),
('Pengalaman pembicara','Dari situ, lo mungkin merasa obrolan ini kurang mendapat ruang.','Kurang mendapat ruang',''),
('Perasaan dan niat','Perasaan itu perlu didengar. Niat dia tetap perlu ditanyakan.','Tanya niatnya','quietly firm'),
('Batas kesimpulan','Satu adegan belum menjelaskan kenapa dia membuka HP, apalagi kadar sayangnya.','','warm, grounded'),
('Pesan yang mendesak','Kalau ada pesan mendesak, kebutuhan itu bisa disampaikan, supaya kalian tahu percakapannya sedang dijeda.','Perlu membalas?',''),
('Permintaan perhatian','Coba bilang: gua pengin selesai cerita. Bisa taruh HP dulu selama kita makan?','Bisa taruh dulu?','speaking gently to a partner'),
('Jeda yang disebut','Kalau dia perlu membalas: gua jawab pesan ini sebentar, habis itu gua dengerin lagi.','Habis ini, lanjut','open, conversational'),
('Perhatian kembali','Lalu lakukan: ponsel ditaruh, perhatian kembali, dan ceritanya dilanjutkan dari bagian yang tertinggal.','Lalu, lakukan','warm, deliberate'),
('Ruang kebutuhan berdua','Kesepakatan ini memberi tempat buat kebutuhan komunikasi kalian. Kalian juga boleh menyepakati kapan perlu jeda.','','clear, explanatory'),
('Cerita dibuka lagi','Jadi, cerita yang berhenti tadi bisa dibuka lagi lewat permintaan perhatian yang jelas.','','reflective'),
('Kapan kita tersedia','Saat makan berdua, kapan kita benar-benar tersedia buat saling mendengar?','Kapan kita tersedia?','soft, intimate, reflective'),
]
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    assert (V/'hyperframes.json').exists(), 'Initialize the empty video directory first.'
    assert not (V/'script_data.json').exists(), 'Resume frozen intake instead of replacing it.'
    lines=[dict(id=i,title=t,text=s,emphasis=e,tags=tag,dramatic=i in (8,13)) for i,(t,s,e,tag) in enumerate(LINES,1)]
    count=sum(len(x['text'].split()) for x in lines); assert 170<=count<=210,count
    snapshot=dict(source='board',board_accounts_file='boards/ruang-di-antara/ACCOUNTS.json',board_accounts_sha256=hashlib.sha256((B/'ACCOUNTS.json').read_bytes()).hexdigest(),accounts=json.loads((B/'ACCOUNTS.json').read_text(encoding='utf-8'))['accounts']);dump(P/'target_snapshot.json',snapshot)
    episode='''# Sebentar di meja makan

New production requested on 2026-11-02 with `$shortform-production --board=ruang-di-antara --topic=auto --delivery=queue --automation`. User also requested a Git commit after the pipeline finishes.

## Resolved brief and execution

board: ruang-di-antara; editorial v1.3 / visual and audio v1.2; implementation 2026-10-21.
Direction: [DIRECTION.md](../../boards/ruang-di-antara/DIRECTION.md), [EDITORIAL.md](../../boards/ruang-di-antara/EDITORIAL.md), [frame.md](../../boards/ruang-di-antara/frame.md).
topic_selection: auto
topic: Partner phubbing in a fictional dinner conversation: phone distraction, observable interruption and an explicit request for attention.
purpose: Explain one established concept through an ordinary interaction, then offer one adaptable response.
audience: Indonesian adults reflecting on ordinary couple communication.
language: Indonesian, consistent lo–gua; English concept and Indonesian meaning spoken early.
format: Instagram Reel; 1080x1920; 30fps; sixteen meaningful illustrated scenes; target 90s, accepted board range 85–95s.
audio: continuous ElevenLabs eleven_v4 narration; root voice inherited through board-aware resolver; sparse frozen board material SFX; no BGM so conversational pauses remain exposed.
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
human_approval: false
pre_render_authorization: delegated by the user's --automation instruction, after agent checks and creative verification
requested_endpoint: publishing
delivery: queue
schedule: next configured account queue slot; resolve and verify returned future instant at delivery
commit: after verified pipeline endpoint, scoped to this episode and its tracker insertion

## Topic discovery and overlap

Ten candidates presented in conversation before file creation: dinner/partner phubbing (selected); relationship rituals; repetitive problem talk; humor boundaries; wanted assistance; concealed meal preferences; differing recollections; small follow-through; relationship comparison; changed weekend expectations. Selection favors an observable phone/meal scene, original-author definition, and a distinct phone-attention question. Alternatives remain candidates, not verified scientific explanations or additional productions.

Tracker and production directory names inspected. Distinct from cerita-belum-selesai (checking understanding before advice), jeda-balasan-dan-dugaan (attributing an unanswered message), and jeda-punya-waktu-kembali (agreed pause during conflict). Here the central question is a phone interrupting a conversation already taking place. No trending claim. Exactly one new episode.

## Research boundaries

Original researchers' Baylor article read through Jina. It defines phubbing as attending to a phone during another person's interaction and explains their partner-phubbing research. ScienceDirect original-paper page returned a CAPTCHA; no extracted challenge text is evidence. The script uses the definition, no numeric prevalence or causal relationship claims. Fictional feeling is explicitly possible; phone use alone does not establish motive or relationship diagnosis. Practical dinner agreement is an illustrative editorial suggestion, not a tested intervention. See SOURCES.md.

## Hook selection before script

1. “Sebentar, katanya sambil lihat HP. Kenapa cerita lo jadi berhenti di meja makan?” Concrete interaction; promises an account of interrupted attention. Recommended and selected.
2. “Kalian makan berdua. Perhatian kalian lagi ada di tempat yang sama?” Presence versus attention; promises to explain the distinction.
3. “Lo cuma cek satu notifikasi. Bagian cerita mana yang barusan kelewat?” Phone-user viewpoint; promises a concrete way to return attention.

All three presented before SCRIPT.md drafting. Agent selected hook 1 under the explicit immediate automation policy. It carries the dinner scene into the closing question. This is delegated selection, not human approval.

## Preflight

Trypost Admin's Workspace 01a171dd-5281-730d-af07-f2168d17add7 matches the saved board account. Live connected Instagram @eliansatya: 01a172ed-9899-7177-ab1e-627c835e4a57. Caller publishes directly, requires_approval=false. Configured queue exists. instagram_reel permits 900s / 314572800 bytes; caption at most 2200 characters / five hashtags. Queue read at intake begins 2026-11-03T07:00:00Z; final creation uses queue=next and verifies actual receipt. DIRECTION.md's empty-account prose is stale; actual ACCOUNTS.json supplies the authoritative mapping.

Context7 MCP tools are unavailable in this session. Installed project skill documentation and the resolved HyperFrames CLI help provide the CLI fallback. HyperFrames 0.9.1 is pinned for this new project. Usage status known at intake; no plan-limit inference from a rendering success.

## Publishing targets

```json
'''+json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n```\n\n## Current stage\n\nScript agent verification complete; continue to the complete visual storyboard before synthesis.\n'
    (P/'EPISODE.md').write_text(episode,encoding='utf-8')
    sources='''# Sources and claim boundaries

Research date: 2026-11-02. Research tool: Jina search_web and read_url. Creative fictional illustrations are kept separate from evidence.

## Read primary author source

James A. Roberts and Meredith E. David (2017), “Partner Phubbing: How Cell Phones Impact Romantic Partnerships,” Baylor University Keller Center.
https://kellercenter.hankamer.baylor.edu/news/story/2017/partner-phubbing-how-cell-phones-impact-romantic-partnerships

Full article body read. The original researchers define phubbing as attending to a cellphone so that an interaction is interrupted, or using it instead of communicating with another present person. Partner phubbing applies this behavior to significant others. They describe scale development and a US adult study relating reported phubbing, phone conflict and relationship satisfaction. The article also makes stronger causal-sounding interpretations; this episode does not reproduce those interpretations as established causation.

Underlying paper: Roberts & David (2016), Computers in Human Behavior 54, 134–141, doi:10.1016/j.chb.2015.07.058.
https://www.sciencedirect.com/science/article/pii/S0747563215300704
Publisher fetch was blocked by a CAPTCHA. It is a bibliographic lead, not a successfully read full paper. The accessible original-author university article supports the definition used here.

## Claim map

| Scene | Content | Support and scope |
| --- | --- | --- |
| 02–03 | English term partner phubbing, immediate Indonesian meaning; phone attention interrupts an ongoing couple interaction | Original-author definition in the read Baylor article. A behavioral concept, not diagnosis. |
| 01, 04–06 | Dinner, office story, checking a notification, asking to repeat | Explicit fictional scenario. Shows observable actions covered by the definition; no claim about all couples. |
| 07–09 | Speaker may feel the conversation has little room; feeling warrants attention while motive needs inquiry | “Mungkin” marks hypothetical experience. Motive and love are not inferred from the behavior. No causal or diagnostic claim. |
| 10–14 | Announce a pressing reply, request phone-free conversation, return to the missed point | Illustrative negotiated dialogue and visible follow-through, not an empirically validated treatment or universal rule. |
| 15–16 | Ask for attention and discuss availability | Episode-specific practical reflection resolving the opening. No guaranteed relationship outcome. |

## Exclusions and creative references

No prevalence figures, attachment labels, depression claims, addiction claims or phone-ban prescriptions. No inference that every phone interaction is phubbing: the illustrated interruption is the relevant boundary. Emergency needs and agreed pauses remain discussable. The board's static studies guide palette, actors and motion only, not scientific assertions.
'''
    (P/'SOURCES.md').write_text(sources,encoding='utf-8')
    d=json.loads((R/'TRACKER.json').read_text(encoding='utf-8-sig'));assert not any(x['slug']==P.name for x in d['productions']);d['productions'].append(dict(slug=P.name,topic='Partner phubbing: phone-interrupted dinner conversation, observable attention shifts and an explicit request to reconnect',board='ruang-di-antara',stage='script',status='in_progress',path='productions/'+P.name));dump(R/'TRACKER.json',d)
    dump(V/'script_data.json',lines)
    doc=f'# Sebentar di meja makan — script v1\n\n{count} spoken words; estimated 90 seconds. Dinner and dialogue are fictional illustrations. Hook 1 selected before drafting under automation. Definition and limits in SOURCES.md.\n\n'
    for x in lines:doc+=f'## Scene {x["id"]:02d}: {x["title"]}\n\n{x["text"]}\n\nEmphasis: {x["emphasis"] or "(none)"}. Palette: {"charcoal" if x["dramatic"] else "cream"}.\n\n'
    for f in (P/'SCRIPT.md',V/'SCRIPT.md'):f.write_text(doc.rstrip()+'\n',encoding='utf-8')
    (V/'BRIEF.md').write_text(episode+f'\nScript v1: {count} words, English term and Indonesian meaning spoken in scene 02; definition, example and interpretive limits in 03–10; application and return in 11–16.\n',encoding='utf-8')
    (V/'assets/fonts').mkdir(parents=True,exist_ok=True)
    for f in (B/'assets').iterdir():
        if f.is_file() and f.suffix in ('.ttf','.txt'):shutil.copy2(f,V/'assets/fonts'/f.name)
    shutil.copy2(B/'frame.md',V/'frame.md');shutil.copytree(B/'components',V/'assets/board/components',dirs_exist_ok=True);shutil.copytree(B/'assets/audio/sfx',V/'assets/board/audio/sfx',dirs_exist_ok=True)
    (V/'vendor').mkdir(exist_ok=True);shutil.copy2(OLD/'video/vendor/gsap.min.js',V/'vendor/gsap.min.js')
    for name in ('visuals.py','animate.py','capture_board.py','capture_stills.py','qa.py','capture_motion.py','seek_qa.py','preview_qa.py','cleanup_preview.py','verify_export.py','prepare_audio.py','finish_audio.py','exact_seams.py','verify_cut_frames.py','state.py','commit_scope.py'):
        s=(OLD/name).read_text(encoding='utf-8').replace(OLD.name,P.name).replace('Deadline dan cucian','Sebentar di meja makan').replace('hyperframes@0.8.209','hyperframes@0.9.1')
        s=s.replace('==186',f'=={count}').replace('186 aligned',f'{count} aligned').replace('caption_words=186',f'caption_words={count}').replace('in (8,10)','in (8,13)')
        (P/name).write_text(s,encoding='utf-8')
    sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'));import narration
    voice,provenance=narration.resolve_voice(R,board='ruang-di-antara')
    dump(V/'audio_request.json',dict(provider='elevenlabs',board='ruang-di-antara',lang='id',voice=voice,voice_resolution=provenance,tts_model='eleven_v4',lines=[dict(id='narration',text='\n\n'.join(('['+x['tags']+'] ' if x['tags'] else '')+x['text'] for x in lines))]))
    pkg=json.loads((V/'package.json').read_text(encoding='utf-8'));pkg['scripts']={k:v.replace('npx hyperframes','npx --yes hyperframes@0.9.1') for k,v in pkg['scripts'].items()};dump(V/'package.json',pkg)
    print(json.dumps(dict(words=count,scenes=16,stage='script',human_approval=False)))
if __name__=='__main__':main()
