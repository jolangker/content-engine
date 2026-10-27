from pathlib import Path
import json, re, shutil, sys, importlib.util

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent.parent
V=BASE/'video'
def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8')
def dump(path,obj): write(path,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

lines=[
('Cuma mau cerita?', 'Lo cuma pengen cerita soal hari yang berat. Kok obrolannya malah jadi daftar solusi?'),
('Ruang dulu.', 'Kadang, yang lo butuhin saat itu cuma ruang buat didengar dulu.'),
('Pulang membawa cerita', 'Misalnya, lo pulang bilang: gua capek, tadi kerjaan gua dikritik lagi.'),
('Cerita terhenti.', 'Dia jawab: ya udah, cari kerja lain aja. Lalu cerita lo berhenti.'),
('Belum selesai.', 'Sarannya mungkin masuk akal. Tapi lo belum sempat menjelaskan bagian yang berat.'),
('Belum tahu.', 'Satu respons belum cukup buat menyimpulkan dia nggak peduli. Mungkin dia ingin membantu.'),
('Belum ketemu.', 'Niat membantu dan merasa dipahami belum tentu ketemu dalam respons yang sama.'),
('Dengar. Cek.', 'Mendengarkan aktif berarti berusaha memahami cerita, lalu mengecek apakah tangkapan kita sudah tepat.'),
('Beri ruang.', 'Coba tahan saran sebentar. Kasih ruang sampai dia selesai menjelaskan bagian yang berat.'),
('Usaha lo…', 'Lo bisa bilang: jadi, lo kecewa karena usaha lo tadi kayak nggak kelihatan?'),
('Boleh dikoreksi.', 'Kalau dia mengoreksi, ikuti koreksinya. Jangan buru-buru mempertahankan tebakan lo.'),
('Dengerin dulu?', 'Gua dengerin dulu, atau lo pengen kita cari jalan keluar bareng?'),
('Bisa berubah.', 'Pertanyaan ini memberi pilihan. Jawabannya juga bisa berubah selama obrolan.'),
('Gua mau didengerin dulu.', 'Kalau lo yang cerita, bilang: gua mau didengerin dulu. Nanti kita pikirin langkahnya.'),
('Saran punya tempat.', 'Saran tetap punya tempat, ketika itu yang dibutuhkan. Mendengar dulu membantu lo menyesuaikannya.'),
('Tanya kebutuhannya.', 'Sebelum menyusun jawaban, coba cari tahu: sekarang, bantuan seperti apa yang dia butuhkan?')]
titles=['The interrupted story','Room to be heard','After work','The story stops','An unfinished account','Suspend the verdict','Intention and experience','Listening and checking','Let the story unfold','Check the meaning','Accept correction','Offer a choice','Needs may change','State a need','Advice in shared space','Return to the opening']
purposes=[
'Show story colliding with unsolicited solution cards.',
'Offer the value early: open room for the speaker.',
'Ground the fictional account in a doorway, bag and marked work sheet.',
'Let the outgoing ribbon meet a blocking response, then stop.',
'Keep unfinished speech visible beside a plausible solution.',
'Make the listener and an uncertain question the focus; avoid motive diagnosis.',
'Separate the offered solution from the receiving speech space.',
'Show a return path checking a story against the speaker.',
'Move advice aside as three parts of the story unfold.',
'Turn an inferred feeling into a question returned to the speaker.',
'Replace the tentative listening path with the corrected route.',
'Open two support options on a fork, leaving the speaker agency.',
'Move a shared marker between options without ranking either.',
'Give the original speaker a clear request in their own space.',
'Bring the solution note back onto a shared table after listening.',
'End with a large shared conversation space and deliberate quiet hold.']
frames=[]
durations=[6,5,6,6,5,6,5,6,6,6,5,6,5,6,6,5]
t=0
for i,((emphasis,vo),title,purpose,d) in enumerate(zip(lines,titles,purposes,durations),1):
    frames.append(dict(n=i,title=title,emphasis=emphasis,vo=vo,purpose=purpose,start=t,duration=d,dark=i in [4,12]))
    t+=d
dump(V/'scenes.json',frames)
board=ROOT/'boards/ruang-di-antara'
shutil.copy2(board/'frame.md',V/'frame.md')
shutil.copytree(board/'components',V/'components',dirs_exist_ok=True)
shutil.copytree(board/'assets',V/'assets/board',dirs_exist_ok=True)
spec=importlib.util.spec_from_file_location('narration',ROOT/'.agents/skills/shortform-production/scripts/narration.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
voice,resolution=mod.resolve_voice(ROOT)
tags={0:'[conversational]',3:'[softly]',7:'[explaining]',11:'[gently]',15:'[reflective]'}
full='\n\n'.join((tags.get(i,'')+' '+vo).strip() for i,(_,vo) in enumerate(lines))
dump(V/'audio_request.json',dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=resolution,tts_model='eleven_v4',speed=1.0,lines=[dict(id='narration',text=full)],bgm=dict(mode='none')))
script=f'''# SCRIPT — Cerita belum selesai\n\nVersion 1. Agent-verified under delegated automation. {len(' '.join(x[1] for x in lines).split())} spoken words. All situations and dialogue are fictional illustrations.\n\n**Voice:** ElevenLabs / {voice} / eleven_v4. Resolved from root .env.\n**Voice settings:** Native speed, one continuous full-script request.\n**Voice direction:** Intimate conversational Indonesian lo–gua; curiosity on the opening, restrained pauses on frames 4 and 12, warm practical delivery on the examples.\n\n'''
for f in frames:
    script+=f'''## Line {f['n']} — {f['title']} (Frame {f['n']})\n\n**Time:** Estimated {f['start']:.1f}–{f['start']+f['duration']:.1f}s; measured alignment follows.\n**Delivery:** {tags.get(f['n']-1,'Continue naturally, without presenter emphasis.')}\n\n    {f['vo']}\n\n**On-screen:** {f['emphasis']}\n\n'''
write(BASE/'SCRIPT.md',script); write(V/'SCRIPT.md',script)
write(BASE/'SOURCES.md','''# Sources and claim boundaries

Research date: 2026-10-25. Discovery and extraction used Tavily CLI. Tavily search succeeded; publisher and Semantic Scholar extraction failed, including an advanced publisher retry. The publisher full paper was not read. No claim about romantic relationship outcomes or universal superiority of listening is used.

## Evidence

1. Weger, H., Castle Bell, G., Minei, E. M., & Robinson, M. C. (2014). The Relative Effectiveness of Active Listening in Initial Interactions. International Journal of Listening, 28(1), 13–31. https://doi.org/10.1080/10904018.2013.813234
   Accessible university summary: https://reachfamilies.umn.edu/sites/default/files/prtw/2021-09/Weger_2014__2021091010606.pdf
   In 115 undergraduates' initial interactions, active listening, advice and simple acknowledgement were compared. Perceived understanding favored active listening; satisfaction was not significantly different between active listening and advice. The summary's broad opening statement is less precise than its detailed findings: retain that distinction. These are brief initial interactions, not evidence of long-term couple improvement. This is feasibility/context evidence only; no numerical or comparative outcome claim is narrated.
2. HelpGuide, Active Listening Tips for Improved Communication. https://www.helpguide.org/relationships/communication/active-listening
   Extracted successfully. Reflective listening includes paraphrasing, checking understanding, allowing corrections and avoiding mechanical repetition. The guide recommends asking whether advice is wanted. This is expert/public guidance, not a trial of the episode's exact wording. Do not adopt its unsourced body-language percentages.

## Script mapping

| Frames | Proposition | Basis and limitation |
| --- | --- | --- |
| 1–5 | Someone may want to finish a difficult story before receiving advice. | Fictional after-work scene; practical possibility consistent with source 2, not a statement about all people. |
| 6–7 | One response does not establish a partner's care or intention; intention and felt understanding may differ. | Epistemic limitation and illustrative distinction; no diagnosis or empirical motive claim. |
| 8 | Active listening seeks understanding and checks what was understood. | Source 2 reflective listening guidance; source 1 provides contextual research lead. |
| 9–11 | Let a person finish, paraphrase tentatively and accept corrections. | Source 2; quoted question is an authored adaptable example. |
| 12–14 | Ask what support is wanted and let the speaker express a preference. | Source 2 advice-permission recommendation, adapted editorially. A changing answer is presented as a possibility. |
| 15–16 | Advice has a place when wanted; listening can inform how it is offered. | Source 2 and a bounded editorial synthesis. No guaranteed benefit. |

## Creative reference and exclusions

Board v1.2 visual studies are creative references only. The earlier kabar-baik episode concerns capitalization around positive events; this episode concerns difficult-event disclosure, checking understanding and support preference. Other workspace productions explain objects/infrastructure and do not overlap. No diagnostic labels, attachment types, gender-coded motives, statistics or claims that advice is inherently harmful are included.
''')
accounts=json.loads((board/'ACCOUNTS.json').read_text(encoding='utf-8-sig'))['accounts']
write(BASE/'EPISODE.md',f'''# Cerita belum selesai

## Resolved brief

- topic_selection: auto, delegated by --topic=auto on 2026-10-25
- topic: Offering advice before a difficult story has been heard; a fictional after-work interaction.
- board: ruang-di-antara, approved v1.2, implementation 2026-10-21
- direction: [DIRECTION.md](../../boards/ruang-di-antara/DIRECTION.md), [EDITORIAL.md](../../boards/ruang-di-antara/EDITORIAL.md), [frame.md](../../boards/ruang-di-antara/frame.md)
- language: Indonesian lo–gua; vertical 1080x1920, 30 fps; target 85–95s.
- execution_policy: automation
- automation_after: none
- automation_state: active
- human_review: none
- pre_render_authorization: delegated by the user's --automation instruction
- until: export
- delivery: package default, capped before packaging by --until=export
- external_delivery: none requested; no upload, draft, queue or publication in scope.
- storyboard: all 16 static styled stills, HTML and PNG required; agent verification replaces human review.
- narration: ElevenLabs / {voice} / eleven_v4, voice from project root .env. Tags supplied; native speed and one full-script request.
- BGM: none. Let the intimate spoken exchange and pauses carry the emotional turns.
- SFX: reuse board contact, air and connection sounds for selective events; resolve exact measured triggers after narration.

## Topic selection

Ten candidates were presented before files were created: early advice; vague later promise; short reply and interpretation; asking for space; apology follow-through; shifting to one's own story; reluctant agreement; unclear support need; postponed small conversations; understanding without agreement. Early advice was selected for concrete recognition, usable guidance and accessible evidence. No trend claim. Candidate 8 is reserved as a related alternative, not a second production. Existing kabar-baik is about positive-event sharing, a materially different question and takeaway. The unregistered roda-beda-putaran folder was checked by topic and is unrelated.

## Hook selection before script drafting

1. “Lo cuma pengen cerita soal hari yang berat. Kok obrolannya malah jadi daftar solusi?” — speaker's recognizable scene, promise: explain mismatched support.
2. “Pas dia cerita capek, lo langsung bilang, ‘Ya udah, resign aja.’ Pernah?” — listener's perspective, promise: show a more responsive opening.
3. “Kenapa saran yang masuk akal kadang tetap bikin lo merasa belum didengar?” — experiential distinction, promise: separate solving from understanding.

Selected: 1, agent-selected under delegated automation. Specific situation, modest claim and direct return at the ending. Script v1 is agent-verified, not human-approved.

## Publishing target snapshot

Source: boards/ruang-di-antara/ACCOUNTS.json at intake. The actual file supersedes stale narrative documentation saying the list is empty. Inherited full list:

```json
{json.dumps(accounts,ensure_ascii=False,indent=2)}
```

## Workflow and state

HyperFrames CLI 0.8.197, faceless-explainer route. The workflow freshness command reported this route retired in the newest skill family; installed local workflow instructions remain available and are used with the project's explicit shortform-production overrides. Native delegation is not used because the dispatch adapter requires explicit user permission; inline execution is its authorized fallback. No new permission pause is needed.

Current stage: script, agent-verified. Next: static scene poses and complete visual storyboard, before any paid synthesis. No preview server has been started by this run.
''')
write(V/'capture/extracted/visible-text.txt','$shortform-production --board=ruang-di-antara --topic=auto --until=export --automation\n\nSelected topic: '+frames[0]['purpose'])
dump(V/'capture/extracted/tokens.json',dict(title='Cerita belum selesai',description='Understand before offering advice',colors=['#F3EDE3','#302B28','#A34F3F','#D8C8B5'],fonts=['Newsreader','DM Sans']))
tracker=json.loads((ROOT/'TRACKER.json').read_text(encoding='utf-8-sig'))
if not any(x['slug']==BASE.name for x in tracker['productions']):
    tracker['productions'].append(dict(slug=BASE.name,topic='Listening and checking understanding before offering advice during difficult-event disclosure',board='ruang-di-antara',stage='script',status='in_progress',path='productions/'+BASE.name))
dump(ROOT/'TRACKER.json',tracker)
print('Prepared',len(frames),'frames;',len(' '.join(x[1] for x in lines).split()),'words; estimated duration',t)
