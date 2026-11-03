"""Adapt inherited technical helpers to this episode, without modifying history."""
from pathlib import Path
P=Path(__file__).resolve().parent
f=P/'finish_audio.py';s=f.read_text(encoding='utf-8').replace("g['scene'] in (8,10)","g['scene'] in (8,11)")
a=s.index('    requests=[');b=s.index('\n    cues=[]',a)
s=s[:a]+'''    requests=[(1,'contact',.43,'the supporter arrives beside the reopened book'),(6,'contact',.43,'the pencil returns to the blank page'),(10,'connection',.73,'a possible practice interval becomes visible'),(12,'air',.73,'the partner reply space opens after the viewer question'),(14,'contact',.73,'the partner settles at the offered practice table'),(15,'connection',.73,'the partner develops the plant drawing on their own page')]'''+s[b:]
s=s.replace('The park conversation stays open to different meanings; exposed pauses leave room for the partner answer without an emotional prescription.','The partner aspiration stays open; exposed pauses leave room for the answer without an emotional prescription.').replace('Six sparse frozen material cues mark sitting, shared meaning, the practical route, speaking and listening; no cue on every cut.','Six sparse frozen material cues mark arriving, pencil return, practice time, reply room and the partner drawing; no cue on every cut.').replace('No SFX in dark 08/10, practical continuation 14 or final hold 16; no BGM throughout.','No SFX in dark 08/11 or final hold 16; no BGM throughout.')
f.write_text(s,encoding='utf-8')
f=P/'prepare_audio.py';s=f.read_text(encoding='utf-8').replace('i in (7,8,9,10)','i in (7,8,10,11)');f.write_text(s,encoding='utf-8')
f=P/'verify_export.py';s=f.read_text(encoding='utf-8').replace("FILE=E/'bangku-di-jalan-pulang-v1.mp4'","FILE=E/f'{P.name}-v1.mp4'");f.write_text(s,encoding='utf-8')
f=P/'animate.py';s=f.read_text(encoding='utf-8');a=s.index('MOVES.update(');b=s.index('\ndef main',a)
s=s[:a]+'''MOVES.update({1:[('down',.14),('arrive',.43),('draw',.73)],3:[('draw',.14),('settle',.43),('down',.73)],4:[('arrive',.14),('draw',.43),('draw',.73)],6:[('draw',.14),('settle',.43),('down',.73)],7:[('draw',.14),('draw',.43),('down',.73)],10:[('draw',.14),('settle',.43),('draw',.73)],12:[('draw',.14),('draw',.43),('draw',.73)],13:[('draw',.14),('draw',.43),('settle',.73)],14:[('draw',.14),('arrive',.43),('down',.73)],15:[('down',.14),('settle',.43),('draw',.73)],16:[('down',.14),('arrive',.43),('settle',.73)]})'''+s[b:]
f.write_text(s,encoding='utf-8')
print('Adapted captions, palettes, motion roles, cue meanings and export filename.')
