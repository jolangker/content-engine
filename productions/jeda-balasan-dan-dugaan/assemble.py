"""Assemble verified static layouts with episode-specific motion and measured audio."""
from pathlib import Path
import subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
f=P/'animate.py';s=f.read_text(encoding='utf-8');s=s.replace("and(!p.getAttribute", "and(!p.getAttribute")
s=s.replace("p.getTotalLength&&(!p.getAttribute('fill')", "p.getTotalLength&&!p.hasAttribute('stroke-dasharray')&&(!p.getAttribute('fill')")
s=s.replace('if n==4:', 'if False:')
f.write_text(s,encoding='utf-8')
for script,args in [('build.py',[]),('animate.py',[]),('finish_audio.py',[]),('build.py',['--assemble'])]:subprocess.run([sys.executable,str(P/script),*args],check=True)
subprocess.run([sys.executable,str(ROOT/'.agents/skills/shortform-production/scripts/sound_design.py'),'--video',str(P/'video'),'--apply'],check=True)
