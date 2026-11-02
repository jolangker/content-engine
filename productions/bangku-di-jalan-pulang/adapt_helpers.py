"""Adapt retained technical helpers to this episode's scene semantics."""
from pathlib import Path
import re
P=Path(__file__).resolve().parent
f=P/'animate.py';s=f.read_text(encoding='utf-8');a=s.index('MOVES=');b=s.index('def main():',a)
s=s[:a]+'''MOVES={n:[('draw',.14),('draw',.43),('draw',.73)] for n in range(1,17)}
MOVES.update({1:[('arrive',.14),('down',.43),('draw',.73)],3:[('down',.14),('down',.43),('draw',.73)],5:[('down',.14),('down',.43),('draw',.73)],6:[('draw',.14),('settle',.43),('draw',.73)],7:[('draw',.14),('draw',.43),('settle',.73)],11:[('draw',.14),('settle',.43),('draw',.73)],14:[('draw',.14),('arrive',.43),('arrive',.73)],15:[('settle',.14),('draw',.43),('draw',.73)],16:[('down',.14),('draw',.43),('draw',.73)]})
'''+s[b:]
s=s.replace("        if n==3:\n            js+=f\"tl.to('#{cid}-beat2',{{opacity:0,duration:.12}},{dur*.73:.5f});\\n\"\n",'')
f.write_text(s,encoding='utf-8')
f=P/'capture_board.py';s=f.read_text(encoding='utf-8').replace('Editorial v1.3','Editorial v1.4').replace('A phone interrupts dinner conversation; an explicit request and visible return restore room for the story. Exactly two charcoal turns: 08 and 13.','A recurring park stop has personal meaning; ask whether the partner shares that meaning. Exactly two charcoal turns: 08 and 10.')
f.write_text(s,encoding='utf-8')
f=P/'finish_audio.py';s=f.read_text(encoding='utf-8');a=s.index('    requests=');b=s.index('    cues=[]',a)
s=s[:a]+'''    requests=[(1,'contact',.43,'the second participant settles at the familiar bench'),(3,'connection',.73,'the shared meaning enclosure completes'),(6,'air',.73,'the practical onward route appears'),(11,'contact',.43,'the viewer names the bench in their own speech space'),(13,'connection',.73,'separate perspectives find a shared point at the bench'),(15,'connection',.73,'the opening park view gains the shared enclosure')]
'''+s[b:]
s=s.replace('The dinner conversation and pauses remain exposed so the score does not prescribe a feeling or imply a magical repair.','The park conversation stays open to different meanings; exposed pauses leave room for the partner answer without an emotional prescription.')
s=s.replace('Six restrained frozen material cues mark phone attention, interrupted direction, inquiry, setting the phone aside and the reopened story; no notification ping or transition quota.','Six sparse frozen material cues mark sitting, shared meaning, the practical route, speaking and listening; no cue on every cut.')
s=s.replace('No SFX in dark 08/10, needs discussion 14 or final hold 16','No SFX in dark 08/10, practical continuation 14 or final hold 16')
f.write_text(s,encoding='utf-8')
print('Episode helper adaptations complete')
