from pathlib import Path
import sys, json, shutil, importlib.util

ROOT=Path(__file__).resolve().parents[2]
P=Path(__file__).resolve().parent
V=P/'video'
rows=[
('Kabar yang dibawa pulang','Lo akhirnya dapat promosi. Hal pertama yang lo pengen: cerita ke dia, orang yang tahu perjuangan lo.','“Gue dapat promosi.”','Kabar yang ingin dibagi.','quote','[intimate, quietly excited, conversational]'),
('Sambutan yang lewat','Dia jawab, oh, bagus. Lalu lanjut melihat layar. Lo ikut diam, padahal tadi pengen cerita panjang.','“Oh, bagus.”','Lalu perhatian beralih.','distraction',''),
('Ruang yang mengecil','Kabar baiknya tetap ada. Tapi rasa senangnya bisa mengecil ketika ceritanya seperti nggak mendapat tempat.','Senangnya belum selesai.','Ceritanya keburu berhenti.','shrink','[soft, observant, reflective]'),
('Menahan kesimpulan','Ini belum cukup buat menyimpulkan dia nggak peduli. Mungkin dia terdistraksi; kita belum tahu.','Satu respons.','Belum seluruh ceritanya.','boundary',''),
('Capitalization','Dalam riset hubungan, berbagi kejadian positif ke orang dekat dibahas sebagai capitalization.','Capitalization','Berbagi kejadian positif dengan orang dekat.','concept','[clear, grounded, gently explanatory]'),
('Menikmati bersama','Kesempatan buat menikmati lagi kabar itu, sambil merasakan bagaimana orang dekat menyambutnya.','Kabar baik → cerita bersama','Ada ruang untuk menikmatinya lagi.','share',''),
('Respons aktif konstruktif','Respons aktif-konstruktif menunjukkan keterlibatan dan antusiasme: ikut senang, bertanya, memberi ruang buat cerita.','Aktif-konstruktif','Terlibat. Tertarik. Membuka cerita.','response',''),
('Perhatian yang terasa','Fokusnya perhatian yang terasa, bukan harus heboh. Suara tenang pun bisa menunjukkan minat yang tulus.','Perhatian yang terasa.','Nggak harus heboh.','quiet','[warm, reassuring, unhurried]'),
('Kaitan dengan kedekatan','Penelitian mengaitkan respons seperti ini dengan kedekatan dan kepuasan hubungan. Ada kaitan, bukan jaminan.','Berkaitan dengan kedekatan.','Kaitan, bukan jaminan.','evidence','[measured, clear]'),
('Pertanyaan yang membuka','Misalnya: wah, akhirnya! Bagian mana yang paling bikin lo senang? Gue pengen denger ceritanya.','“Bagian mana yang paling bikin lo senang?”','Pertanyaan yang membuka cerita.','question','[sincerely pleased, inviting, conversational]'),
('Mengakui usaha','Lalu tanggapi usahanya: gue inget lo nyiapin ini berbulan-bulan. Pasti berarti banget buat lo.','“Gue inget usaha lo.”','Akui apa yang berarti buat dia.','effort',''),
('Kekhawatiran punya tempat','Kalau ada kekhawatiran, itu bisa dibahas juga. Beri kesempatan buat menikmati kabarnya sebelum masuk ke risikonya.','Senang dulu. Bahas juga risikonya.','Kekhawatiran tetap punya tempat.','sequence','[practical, gentle]'),
('Menyatakan keinginan','Kalau lo yang cerita, lo bisa bilang: gue lagi senang, mau bagi momen ini sebentar.','“Gue mau bagi momen ini.”','Sampaikan apa yang ingin lo bagi.','offer','[open, personal, calm]'),
('Refleksi','Saat pasangan membawa kabar baik, apa respons lo memberi ruang buat ikut menikmatinya?','Ada ruang untuk ikut senang?','','reflection','[intimate, reflective, leave a quiet pause]')
]
data=[]
for i,(title,vo,text,support,layout,tag) in enumerate(rows,1):
    data.append(dict(number=i,id=f'{i:02d}-{layout}',title=title,vo=vo,text=text,support=support,layout=layout,tag=tag))
(P/'scene-plan.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
spec=importlib.util.spec_from_file_location('narration',ROOT/'.agents/skills/shortform-production/scripts/narration.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
voice,provenance=mod.resolve_voice(ROOT)
spoken='\n\n'.join(d['vo'] for d in data)
tagged='\n\n'.join((d['tag']+' ' if d['tag'] else '')+d['vo'] for d in data)
request=dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=provenance,tts_model='eleven_v4',speed=1.0,lines=[dict(id='narration',text=tagged)],bgm=dict(mode='none'))
(V/'audio_request.json').write_text(json.dumps(request,ensure_ascii=False,indent=2),encoding='utf-8')
script=f'# SCRIPT — Kabar baik juga butuh disambut\n\nVersion v1; agent-verified under delegated automation. {len(spoken.split())} spoken words.\n\n**Voice:** ElevenLabs / {voice} / eleven_v4, resolved from project root .env.\n**Voice direction:** Intimate Indonesian lo–gua. Warm interest without a theatrical celebration.\n**Voice settings:** Native speed, single full-script request; no provider fallback.\n\n'
for d in data:
    script+=f'## Line {d["number"]} — {d["title"]} (Frame {d["number"]})\n\n**Time:** Estimated 5–8 seconds; measured alignment follows.\n**Delivery:** {d["tag"] or "Continue naturally in the previous register."}\n\n    {d["vo"]}\n\n**On-screen:** {d["text"]}\n**Support:** {d["support"] or "None"}\n\n'
script+='## Verification\n\nSOURCES.md maps the concept, response definition and association claim. Promotion and dialogue are fictional illustrations. The script distinguishes association from guarantee and avoids assessing care from one response. Quiet interest is an editorial application, not a claim that all understated responses were equivalent in the cited studies.\n'
(P/'SCRIPT.md').write_text(script,encoding='utf-8');(V/'SCRIPT.md').write_text(script,encoding='utf-8')
for sub in ['assets/fonts','components','capture/extracted','.media/audio/sfx','verification','compositions/frames']:(V/sub).mkdir(parents=True,exist_ok=True)
board=ROOT/'boards/ruang-di-antara'
shutil.copy2(board/'frame.md',V/'frame.md')
for f in (board/'components').iterdir():
    if f.is_file():shutil.copy2(f,V/'components'/f.name)
for f in (board/'assets').iterdir():
    if f.suffix in ['.ttf','.txt']:shutil.copy2(f,V/'assets/fonts'/f.name)
for f in (board/'assets/audio/sfx').iterdir():
    if f.suffix in ['.wav','.md']:shutil.copy2(f,V/'.media/audio/sfx'/f.name)
(V/'capture/extracted/visible-text.txt').write_text('$shortform-production —board=ruang-di-antara —topic=auto —delivery=draft —automation\n\nSelected topic: Capitalization and responses to a partner\'s good news.\n\n'+spoken,encoding='utf-8')
(V/'capture/extracted/tokens.json').write_text(json.dumps(dict(title='Kabar baik juga butuh disambut',description='Capitalization in everyday relationships',colors=['#F3EDE3','#302B28','#A34F3F','#D8C8B5'],fonts=['Newsreader','DM Sans']),indent=2),encoding='utf-8')
tracker=json.loads((ROOT/'TRACKER.json').read_text(encoding='utf-8-sig'))
entry=next(x for x in tracker['productions'] if x['slug']=='kabar-baik');entry.update(stage='script',status='complete')
(ROOT/'TRACKER.json').write_text(json.dumps(tracker,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(words=len(spoken.split()),voice=voice,scenes=len(data))))
