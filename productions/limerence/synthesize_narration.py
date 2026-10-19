"""Direct native-alignment path using the locked provider, voice, and model.

The shared engine returned no audio. This request uses the documented MP3 output
format and reports a sanitized API error rather than swallowing subprocess stderr.
"""
from pathlib import Path
import base64
import json
import os
import subprocess
import sys
from elevenlabs.client import ElevenLabs

prod=Path(__file__).resolve().parent
video=prod/'video'
for raw in (prod.parents[1]/'.env').read_text(encoding='utf-8-sig').splitlines():
    line=raw.strip()
    if line and not line.startswith('#') and '=' in line:
        k,v=line.removeprefix('export ').split('=',1)
        os.environ.setdefault(k.strip(),v.strip().strip('\"\''))
key=os.environ.get('ELEVENLABS_API_KEY','')
req=json.loads((video/'audio_request.json').read_text(encoding='utf-8'))
assert req['provider']=='elevenlabs' and req['voice']=='nPczCjzI2devNBz1zQrb' and req['tts_model']=='eleven_v4'
dest=video/'.media/audio/voice/narration-full.mp3'
dest.parent.mkdir(parents=True,exist_ok=True)
alignment_path=dest.with_suffix('.alignment.json')
if dest.exists() and alignment_path.exists():
    result=json.loads(alignment_path.read_text(encoding='utf-8'))
else:
    try:
        response=ElevenLabs(api_key=key).text_to_speech.convert_with_timestamps(
            voice_id=req['voice'],model_id=req['tts_model'],text=req['lines'][0]['text'],
            language_code='id',output_format='mp3_44100_128',
            request_options={'max_retries':0,'timeout_in_seconds':180},
        )
        result=response.model_dump()
        encoded=result.pop('audio_base64',None) or result.pop('audio_base_64',None)
        if not encoded:
            raise RuntimeError('Provider returned no audio bytes')
        dest.write_bytes(base64.b64decode(encoded))
        alignment_path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    except Exception as e:
        detail=str(e).replace(key,'[redacted]') if key else str(e)
        error={'provider':req['provider'],'voice':req['voice'],'model':req['tts_model'],'error':detail}
        (video/'audio_failure.json').write_text(json.dumps(error,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(error,ensure_ascii=False))
        sys.exit(1)

align=result.get('normalized_alignment') or result.get('alignment')
if not align:
    raise SystemExit('Audio exists, but native alignment is missing; transcribe this exact audio locally')
words=[]
current=None
tag=False
for ch,start,end in zip(align['characters'],align['character_start_times_seconds'],align['character_end_times_seconds']):
    if ch=='[':
        tag=True
    if tag:
        if ch==']':tag=False
        continue
    if ch.isspace():
        if current:words.append(current)
        current=None
    else:
        if current is None:current={'text':'','start':start,'end':end}
        current['text']+=ch
        current['end']=end
if current:words.append(current)
for i,w in enumerate(words):w['id']=f'w{i:04d}'
probe=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(dest)],capture_output=True,text=True,check=True)
duration=float(json.loads(probe.stdout)['format']['duration'])
meta={'tts_provider':'elevenlabs','voice_id':req['voice'],'tts_model':req['tts_model'],
      'voices':[{'id':'narration','path':dest.relative_to(video).as_posix(),'duration_s':duration,'words':words}],
      'sfx':[],'bgm':None,'bgm_pending':False,'total_duration_s':duration}
(video/'audio_meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'provider':meta['tts_provider'],'voice':meta['voice_id'],'model':meta['tts_model'],'duration_s':duration,'words':len(words),'path':dest.relative_to(video).as_posix()}))
