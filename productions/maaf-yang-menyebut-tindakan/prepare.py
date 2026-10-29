"""Freeze this episode's script and reuse the board's rendering utilities/assets."""
from pathlib import Path
import hashlib, importlib.util, json, shutil

P=Path(__file__).resolve().parent; ROOT=P.parents[1]; V=P/'video'; B=ROOT/'boards/ruang-di-antara'; OLD=P.parent/'ruang-untuk-memilih'
LINES=[
('An unfinished apology','Maaf, gua sibuk. Kalau berhenti di situ, bagian mana yang belum terjawab?','Maaf, gua sibuk','intimate, conversational, curious'),
('Name the component','Ada komponen acknowledgment of responsibility, atau pengakuan tanggung jawab, dalam permintaan maaf.','Pengakuan tanggung jawab','clear, gently explanatory'),
('Name your action','Artinya, lo mengakui tindakan lo yang keliru, sekaligus menjelaskan keadaannya.','Tindakan gua',''),
('The person who waited','Misalnya, lo datang telat. Pasangan udah menunggu, dan waktu makannya ikut mundur.','','observant, conversational'),
('Context without ownership','Gua sibuk menjelaskan situasinya. Tapi belum menyebut tindakan lo yang bikin dia menunggu.','Alasannya ada','measured, precise'),
('An action becomes specific','Kalau lo bilang, gua berangkat terlalu mepet, tindakan yang lo akui jadi jelas.','Berangkat terlalu mepet',''),
('What the research studied','Dalam riset permintaan maaf, pengakuan tanggung jawab dan tawaran perbaikan dinilai penting.','Tanggung jawab · perbaikan','clear, precise'),
('Keep the evidence boundary','Risetnya pakai skenario kerja, jadi ini bukan rumus agar pasangan pasti memaafkan.','Bukan jaminan','gently firm'),
('The missing acknowledgment','Alasan boleh dijelaskan. Apakah tanggung jawab lo ikut disebut?','Bagian gua?','quietly reflective'),
('Speak to the action','Coba bilang, maaf gua bikin lo nunggu. Gua tadi berangkat terlalu mepet.','','sincere, speaking to a partner'),
('Ask about the consequence','Ada yang perlu kita atur ulang karena keterlambatan gua?','Perlu diatur ulang?','open, curious'),
('A concrete next step','Berikutnya, gua akan berangkat lebih awal, dan kabari kalau jadwalnya berubah.','Langkah berikutnya','warm, practical'),
('A plan needs follow-through','Pilih perbaikan yang bisa lo jalankan. Setelah itu, tindak lanjuti.','Jalankan','gently direct'),
('Room for a response','Dia boleh butuh waktu. Permintaan maaf nggak mewajibkan dia langsung merasa lega.','Beri waktu','quietly firm'),
('Answer the opening question','Yang belum terjawab tadi: tindakan apa yang lo akui, dan apa langkah berikutnya?','Apa yang diakui?','reflective'),
('An apology with substance','Biar maafnya punya isi, sebut tindakan lo, lalu ikuti dengan perbaikan.','Maaf yang punya isi','intimate, reflective, leave space'),
]
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    assert not (V/'script_data.json').exists(), 'Intake already frozen; resume instead.'
    lines=[dict(id=i,title=a,text=b,emphasis=c,delivery=d,dramatic=i in (9,14)) for i,(a,b,c,d) in enumerate(LINES,1)]
    count=sum(len(x['text'].split()) for x in lines);print('spoken_words',count);assert 170<=count<=200
    dump(V/'script_data.json',lines)
    spec=importlib.util.spec_from_file_location('voice_policy',ROOT/'.agents/skills/shortform-production/scripts/narration.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    voice,resolution=m.resolve_voice(ROOT)
    dump(V/'audio_request.json',dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=resolution,tts_model='eleven_v4',lines=[dict(id='narration',text='\n\n'.join((f"[{x['delivery']}] " if x['delivery'] else '')+x['text'] for x in lines))]))
    script=f'# Maaf yang menyebut tindakan — script v1\n\n{count} spoken words. Hook 1 selected under delegated automation after source-body research and before drafting. Fictional ordinary lateness; the researched component does not guarantee forgiveness. Lines 2–9 explain/discuss the concept and evidence boundary before one connected application. Timings are estimates until native recording placement.\n\n'
    for x in lines:script+=f"## Line {x['id']}: {x['title']}\n\n{x['text']}\n\nOn-screen: {x['emphasis'] or '(none)'}.\n\n"
    for f in (P/'SCRIPT.md',V/'SCRIPT.md'):f.write_text(script.rstrip()+'\n',encoding='utf-8')
    (V/'assets/fonts').mkdir(parents=True,exist_ok=True)
    for f in (B/'assets').iterdir():
        if f.is_file() and f.suffix in ('.ttf','.txt'):shutil.copy2(f,V/'assets/fonts'/f.name)
    shutil.copy2(B/'frame.md',V/'frame.md');shutil.copytree(B/'components',V/'assets/board/components',dirs_exist_ok=True);shutil.copytree(B/'assets/audio/sfx',V/'assets/board/audio/sfx',dirs_exist_ok=True)
    (V/'vendor').mkdir(exist_ok=True);shutil.copy2(OLD/'video/vendor/gsap.min.js',V/'vendor/gsap.min.js')
    snapshot=dict(source='board',board_accounts_file='boards/ruang-di-antara/ACCOUNTS.json',board_accounts_sha256=hashlib.sha256((B/'ACCOUNTS.json').read_bytes()).hexdigest(),accounts=json.loads((B/'ACCOUNTS.json').read_text(encoding='utf-8'))['accounts']);dump(P/'target_snapshot.json',snapshot)
    # Rendering/measurement utilities are adapted from the same board's last episode.
    for name in ('visuals.py','animate.py','capture_board.py','capture_stills.py','qa.py','capture_motion.py','seek_qa.py','preview_qa.py','cleanup_preview.py','verify_export.py','prepare_audio.py','finish_audio.py','exact_seams.py','verify_cut_frames.py'):
        s=(OLD/name).read_text(encoding='utf-8').replace('ruang-untuk-memilih',P.name).replace('Ruang untuk memilih','Maaf yang menyebut tindakan')
        s=s.replace('==182',f'=={count}').replace('182 aligned',f'{count} aligned').replace('caption_words=182',f'caption_words={count}').replace('in (8,14)','in (9,14)').replace('08/14','09/14').replace('08 and 14','09 and 14')
        (P/name).write_text(s,encoding='utf-8')
    with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('\n## Frozen intake\n\nScript v1 agent-verified: '+str(count)+' spoken words; concept name and immediate Indonesian meaning in line 2, substantive explanation and scene discussion in lines 2–9, concrete application 10–13, receiver autonomy 14, opening answered 15–16. No human approval.\n\nPublishing target snapshot:\n\n```json\n'+json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n```\n\nNarration selected from project .env: ElevenLabs / '+voice+' / eleven_v4. Assets and licenses copied from approved board.\n')
    (V/'BRIEF.md').write_text((P/'EPISODE.md').read_text(encoding='utf-8'),encoding='utf-8')
    t=json.loads((ROOT/'TRACKER.json').read_text(encoding='utf-8-sig'))
    for x in t['productions']:
        if x['slug']==P.name:x.update(stage='storyboard',status='in_progress')
    dump(ROOT/'TRACKER.json',t)
if __name__=='__main__':main()
