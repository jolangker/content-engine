from pathlib import Path
P=Path(__file__).resolve().parent;O=P.parent/'terima-kasih-yang-melihat'
for name in ('capture_motion.py','seek_qa.py','preview_qa.py','cleanup_preview.py'):
    s=(O/name).read_text(encoding='utf-8').replace('hyperframes@0.8.206','hyperframes@0.8.209').replace('terima-kasih-yang-melihat','jeda-balasan-dan-dugaan')
    (P/name).write_text(s,encoding='utf-8')
