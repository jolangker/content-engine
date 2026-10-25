from pathlib import Path
import json, shutil, sys, re
V=Path(__file__).resolve().parent
ROOT=V.parents[2]
rows=[
('Siapa yang menghentikan air?',6,'whole','Sekali tekan, air keluar. Tapi siapa yang tahu kapan tangkinya sudah penuh?','Satu siklus otomatis','tank','whole'),
('Buka tangkinya',5,'tank','Kita buka tangki tipe tuas dan flapper. Ada dua katup dengan tugas berbeda.','Tipe tuas + flapper','reveal','tank'),
('Dua tugas terpisah',5,'tank','Yang di bawah membuang air. Yang di samping mengatur air masuk.','Buang / isi','identify','tank'),
('Putaran menjadi tarikan',5,'lever','Tekan gagang. Tuas berputar, menarik rantai ke atas.','Putar → tarik','lever','lever'),
('Jalur buang terbuka',6,'flapper','Rantai mengangkat flapper dari dudukannya. Jalur menuju mangkuk terbuka.','Flapper terangkat','open','flapper'),
('Gravitasi bekerja',5,'tank','Air tangki turun karena gravitasi. Gagangnya tidak memompa air.','Air mengalir turun','drain','tank'),
('Tetap terbuka sesaat',6,'flapper','Gagang dilepas. Daya apung membantu flapper tetap terbuka sesaat.','Dibantu daya apung','buoyancy','flapper'),
('Pelampung ikut turun',6,'float','Air turun, pelampung ikut merosot. Katup pengisi mulai membuka.','Turun → mulai isi','floatdown','float'),
('Buang dan isi bertumpang tindih',5,'tank','Jadi, pengisian bisa dimulai saat air lama masih keluar.','Dua aliran bersamaan','overlap','tank'),
('Karet kembali menutup',6,'flapper','Saat tangki terkuras, flapper turun. Karet bertemu dudukan, menutup jalur buang.','Kembali ke dudukan','close','flapper'),
('Tangki mulai penuh lagi',5,'fill','Kini air masuk tertampung. Permukaannya naik, membawa pelampung.','Air naik → pelampung naik','rise','fill'),
('Batas tercapai, aliran berhenti',6,'float','Pelampung mengendalikan katup pengisi. Saat batasnya tercapai, air masuk berhenti.','Naik → berhenti isi','stop','float'),
('Selang kecil punya jalur sendiri',6,'refill','Sebagian air pengisi melewati selang kecil menuju pipa limpasan, mengisi kembali mangkuk.','Selang pengisi mangkuk','refill','refill'),
('Jalur untuk kelebihan air',5,'overflow','Kalau air tangki terlalu tinggi, kelebihannya masuk pipa limpasan. Ini jalur cadangan.','Jika air terlalu tinggi','overflow','overflow'),
('Ikuti satu siklus',7,'tank','Perhatikan siklusnya: tuas menarik, flapper membuka, pelampung turun, lalu tangki mengisi lagi.','Tekan → buang → isi','cycle','tank'),
('Siap dipakai lagi',6,'whole','Flapper menahan air. Pelampung mengatur pengisian. Dua tugas, satu tangki siap dipakai lagi.','Dua tugas. Satu siklus.','ready','whole'),
]
def write_plan():
    t=0; scenes=[]
    for i,(title,dur,view,vo,sub,action,_) in enumerate(rows,1):
        scenes.append(dict(id=f's{i:02d}',title=title,start=t,duration=dur,end=t+dur,view=view,vo=vo,sub=sub,action=action,poster=round(t+dur*.62,3)))
        t+=dur
    assert t==90
    (V/'scene-plan.json').write_text(json.dumps(scenes,ensure_ascii=False,indent=2),encoding='utf-8')
    (V/'frame.md').write_text((ROOT/'boards/di-balik-benda/frame.md').read_text(encoding='utf-8'),encoding='utf-8')
    (V/'assets/fonts').mkdir(parents=True,exist_ok=True)
    for x in (ROOT/'boards/di-balik-benda/assets').glob('*'):
        if x.suffix in ('.ttf','.txt'):shutil.copy2(x,V/'assets/fonts'/x.name)
    script='# SCRIPT — Tangki dua katup\n\n**Voice:** ElevenLabs eleven_v4, resolved from project .env before synthesis.\n**Voice direction:** Curious opening; clear, warm Indonesian explanation with space for visible contact.\n**Status:** agent-verified under delegated automation; no human approval.\n\n'
    for i,s in enumerate(scenes,1):
        script+=f"## Line {i} — {s['title']} (Frame {i})\n\n**Time:** {s['start']}–{s['end']}s (estimated; replace after synthesis)\n**Delivery:** Conversational, clear causal emphasis.\n\n    {s['vo']}\n\n"
    script+='## On-screen text\n\n'+ '\n'.join(f"- {s['id']}: {s['title']} / {s['sub']}" for s in scenes)+'\n\nCaptions reproduce spoken words only; no delivery tags.\n'
    (V/'SCRIPT.md').write_text(script,encoding='utf-8');(V.parent/'SCRIPT.md').write_text(script,encoding='utf-8')
    (V/'capture/extracted').mkdir(parents=True,exist_ok=True)
    (V/'capture/extracted/visible-text.txt').write_text('$shortform-production --board=di-balik-benda --topic=auto --until=export --automation\nSelected: gravity cistern with lever, chain, flapper, cup float and fill valve.',encoding='utf-8')
    (V/'capture/extracted/tokens.json').write_text(json.dumps({'title':'Tangki dua katup','description':'Two valves coordinate flushing and refill','colors':['#ECEEE9','#172B3B','#C94422','#2459C4','#167580'],'fonts':['Manrope','IBM Plex Mono']},indent=2),encoding='utf-8')
    update_tracker('storyboard')
    return scenes
def update_tracker(stage,status='in_progress'):
    p=ROOT/'TRACKER.json'; data=json.loads(p.read_text(encoding='utf-8-sig'))
    row=next((x for x in data['productions'] if x['slug']=='tangki-dua-katup'),None)
    if row is None:
        row=dict(slug='tangki-dua-katup',topic='Gravity toilet cistern: lever-chain flapper actuation, drain/refill overlap, cup-float shutoff, refill hose and overflow route',board='di-balik-benda',path='productions/tangki-dua-katup');data['productions'].append(row)
    row.update(stage=stage,status=status)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':write_plan()
