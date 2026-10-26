from pathlib import Path
import shutil,json
V=Path(__file__).resolve().parent;B=V/'boards';archive=B/'revisions/pre-audio';archive.mkdir(parents=True,exist_ok=True)
for name in ['storyboard.png','storyboard.html','verification.json']:
    if not (archive/name).exists():shutil.copy2(B/name,archive/name)
changes=[]
for index,source,t in [(9,'frame-02-at-54.4s.png',54.4),(11,'frame-05-at-64.7s.png',64.7),(14,'frame-06-at-82.7s.png',82.7)]:
    old=list((B/'stills').glob(f'frame-{index:02}-*.png'));assert len(old)==1
    saved=archive/old[0].name
    if not saved.exists():shutil.copy2(old[0],saved)
    dst=B/'stills'/f'frame-{index:02}-at-{t:g}s.png';shutil.copy2(V/'verification/review-fixed'/source,dst)
    if old[0]!=dst:old[0].unlink()
    changes.append(dict(scene_index=index+1,capture_time=t,source='verification/review-fixed/'+source,still=dst.relative_to(V).as_posix()))
(B/'revision-v2.json').write_text(json.dumps(dict(reason='Fresh-eyes P1 fixes: enlarged pinion view and center witness; reduced arm occlusion/contact marker; readable diagnostic labels.',pre_audio_board='boards/revisions/pre-audio/storyboard.png',changed=changes),indent=2)+'\n',encoding='utf-8')
