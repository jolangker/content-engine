from pathlib import Path
import json,re,difflib
from faster_whisper import WhisperModel
V=Path(__file__).resolve().parent
model=WhisperModel('base',device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
segments,info=model.transcribe(str(V/'assets/audio/narration-master.wav'),language='id',beam_size=5,vad_filter=True)
transcript=[dict(start=s.start,end=s.end,text=s.text) for s in segments]
expected=' '.join(s['vo'] for s in json.loads((V/'scene-plan.json').read_text(encoding='utf-8')))
actual=' '.join(s['text'] for s in transcript)
norm=lambda x:re.sub(r'[^\w\s]','',x.lower()).split()
comparison=difflib.SequenceMatcher(None,norm(expected),norm(actual))
report=dict(model='faster-whisper base local int8',language=info.language,language_probability=info.language_probability,transcript=transcript,token_similarity=comparison.ratio(),differences=[dict(kind=tag,expected=norm(expected)[i:j],recognized=norm(actual)[a:b]) for tag,i,j,a,b in comparison.get_opcodes() if tag!='equal'],limitation='Automated ASR is not perceptual listening and may misrecognize Indonesian words. No subjective prosody approval is claimed.')
(V/'verification').mkdir(exist_ok=True);(V/'verification/asr.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='transcript'},ensure_ascii=False))
