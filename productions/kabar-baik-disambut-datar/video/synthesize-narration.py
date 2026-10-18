"""One full-script ElevenLabs request, preserving native character alignment."""
from pathlib import Path
import os,json,base64,re,subprocess,hashlib
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.types import VoiceSettings

ROOT=Path(__file__).resolve().parent
load_dotenv(ROOT.parents[2]/'.env')
DEST=ROOT/'assets/voice/narration-v1'
DEST.mkdir(parents=True,exist_ok=True)
audio_path=DEST/'narration.mp3'
response_path=DEST/'alignment.json'
text=(ROOT/'assets/approved-narration.txt').read_text(encoding='utf-8').strip()
voice=os.environ['ELEVENLABS_VOICE_ID']
request={'provider':'elevenlabs','voice_id':voice,'model_id':'eleven_multilingual_v2','output_format':'mp3_44100_128','voice_settings':{'speed':1.0},'text':text,'automatic_retries':0}
(DEST/'request.json').write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if not audio_path.exists():
    client=ElevenLabs(api_key=os.environ['ELEVENLABS_API_KEY'],timeout=120)
    try:
        response=client.text_to_speech.convert_with_timestamps(voice_id=voice,text=text,model_id=request['model_id'],output_format=request['output_format'],voice_settings=VoiceSettings(speed=1.0),request_options={'max_retries':0})
    except Exception as exc:
        message=str(exc).replace(os.environ['ELEVENLABS_API_KEY'],'[redacted]')
        (DEST/'error.json').write_text(json.dumps({'error':message,'syntheses_succeeded':0},ensure_ascii=False,indent=2),encoding='utf-8')
        raise RuntimeError(message) from None
    audio=getattr(response,'audio_base_64',None) or getattr(response,'audio_base64',None)
    audio_path.write_bytes(base64.b64decode(audio))
    def dump(value):
        return value.model_dump(mode='json') if value is not None else None
    response_path.write_text(json.dumps({'alignment':dump(response.alignment),'normalized_alignment':dump(response.normalized_alignment)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
else:
    print('Reusing the saved narration; no additional synthesis request.')

payload=json.loads(response_path.read_text(encoding='utf-8'))
source_words=re.findall(r'\S+',text)
normal=lambda x: ''.join(c.casefold() for c in x if c.isalnum())
expected=normal(text)
alignment=None
for name in ('normalized_alignment','alignment'):
    candidate=payload.get(name)
    if candidate and normal(''.join(candidate['characters']))==expected:
        alignment=candidate;alignment_source=name;break
if alignment is None:
    raise RuntimeError('Saved audio requires alignment repair; do not synthesize again automatically')
chars=alignment['characters']
starts=alignment['character_start_times_seconds']
ends=alignment['character_end_times_seconds']
flat=[]
for c,s,e in zip(chars,starts,ends):
    for letter in c:
        if letter.isalnum():flat.append((letter.casefold(),s,e))
cursor=0
words=[]
for i,w in enumerate(source_words):
    token=normal(w)
    if not token:continue
    letters=flat[cursor:cursor+len(token)]
    if ''.join(x[0] for x in letters)!=token:raise RuntimeError('Source word mismatch at '+str(i))
    words.append({'id':f'w{i}','text':w,'start':letters[0][1],'end':letters[-1][2]})
    cursor+=len(token)
duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(audio_path)],text=True).strip())
if any(w['start']<0 or w['end']<w['start'] or w['end']>duration+0.05 for w in words):raise RuntimeError('Word timing outside audio')
if any(a['start']>b['start'] for a,b in zip(words,words[1:])):raise RuntimeError('Word timing order is not monotonic')
subprocess.run(['ffmpeg','-v','error','-i',str(audio_path),'-f','null','-'],check=True,capture_output=True)
meta={'tts_provider':'elevenlabs','voice_id':voice,'model_id':request['model_id'],'bgm':None,'bgm_pending':False,'sfx':[],'voices':[{'id':'narration','path':audio_path.relative_to(ROOT).as_posix(),'duration_s':duration,'words':words}],'total_duration_s':duration}
(ROOT/'audio_meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(DEST/'words.json').write_text(json.dumps(words,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
proof={'provider':'elevenlabs','voice_id':voice,'model_id':request['model_id'],'output_format':request['output_format'],'duration_s':duration,'word_count':len(words),'alignment_source':alignment_source,'source_text_matches':True,'timings_monotonic':True,'full_decode_passed':True,'sha256':hashlib.sha256(audio_path.read_bytes()).hexdigest(),'successful_synthesis_requests':1,'automatic_retries':0,'shared_engine_attempt':'failed without a history item; its pcm_44100 format requires Pro, configured account tier is free'}
(DEST/'verification.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in proof.items() if k not in ('sha256','shared_engine_attempt')},ensure_ascii=False))
