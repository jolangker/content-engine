"""Place native narration with explicit editorial pauses and measured word timings."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import wave
import numpy as np

P=Path(__file__).resolve().parent;V=P/'video'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    meta=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'))
    source=meta['voices'][0]; words=source['words']; lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'))
    expected=[w for x in lines for w in x['text'].split()]
    norm=lambda s:re.sub(r'\W','',s.casefold())
    assert len(words)==len(expected)
    assert [norm(w['text']) for w in words]==[norm(w) for w in expected], 'Alignment text differs from the locked script'
    src=V/source['path'];rate=48000
    raw=subprocess.run(['ffmpeg','-v','error','-i',str(src),'-ac','1','-ar',str(rate),'-f','f32le','pipe:1'],capture_output=True,check=True)
    samples=np.frombuffer(raw.stdout,dtype='<f4')
    budget=max(0,90-1.2-len(samples)/rate)
    weights=[1.3,.6,.6,.8,.6,.6,.6,1.6,.7,1.8,.6,.8,.7,.7,.8]
    durations=[budget*w/sum(weights) for w in weights]
    pauses=[];cursor=0
    for n,seconds in enumerate(durations,1):
        cursor+=len(lines[n-1]['text'].split())
        at=(words[cursor-1]['end']+words[cursor]['start'])/2
        pauses.append({'after_scene':n,'original_time':at,'seconds':seconds,'sample':round(at*rate)})
    chunks=[];offset=0
    for p in pauses:
        chunks.extend([samples[offset:p['sample']],np.zeros(round(p['seconds']*rate),dtype='<f4')]);offset=p['sample']
    chunks.append(samples[offset:]);placed=np.concatenate(chunks)
    (V/'assets/audio').mkdir(parents=True,exist_ok=True)
    temp=V/'assets/audio/narration-editorial.wav'
    with wave.open(str(temp),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes((np.clip(placed,-1,1)*32767).astype('<i2').tobytes())
    first=subprocess.run(['ffmpeg','-hide_banner','-i',str(temp),'-af','loudnorm=I=-16:TP=-2:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    measured=json.JSONDecoder().raw_decode(first.stderr[first.stderr.rfind('{'):])[0]
    af=f"loudnorm=I=-16:TP=-2:LRA=7:measured_I={measured['input_i']}:measured_TP={measured['input_tp']}:measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}:offset={measured['target_offset']}:linear=true:print_format=json"
    dest=V/'assets/audio/narration.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(temp),'-af',af,'-ar',str(rate),'-ac','1','-c:a','pcm_s16le',str(dest)],check=True)
    moved=[]
    for old,original in zip(words,expected):
        shift=sum(p['seconds'] for p in pauses if p['original_time']<=old['start'])
        moved.append({**old,'text':original,'start':round(old['start']+shift,5),'end':round(old['end']+shift,5)})
    voice_duration=len(placed)/rate;total=math_ceil_frame(voice_duration+1.2)
    scenes=[];cursor=0;start=0
    for i,x in enumerate(lines):
        begin=cursor;cursor+=len(x['text'].split())
        end=(pauses[i]['original_time']+sum(p['seconds'] for p in pauses[:i+1])) if i<15 else total
        scenes.append({'id':i+1,'start':round(start,5),'end':round(end,5),'duration':round(end-start,5),'word_start':begin,'word_end':cursor,'speech_start':moved[begin]['start'],'speech_end':moved[cursor-1]['end']})
        start=end
    placement={'source':source['path'],'source_sha256':digest(src),'path':dest.relative_to(V).as_posix(),'sha256':digest(dest),'original_duration':len(samples)/rate,'duration':voice_duration,'pauses':pauses,'speech_speed':1,'normalization':{'target_i':-16,'target_tp':-2,'target_lra':7,'input_measurement':measured}}
    timing={'duration_s':total,'voice_duration_s':voice_duration,'original_voice_duration_s':len(samples)/rate,'basis':f'Native ElevenLabs word alignment; {sum(durations):.4f} seconds of explicit editorial pauses, native speech speed 1, plus 1.2-second final visual hold. No speech retiming.','words':moved,'scenes':scenes}
    (V/'placement.json').write_text(json.dumps(placement,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (V/'timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'original_duration':len(samples)/rate,'placed_voice_duration':voice_duration,'final_duration':total,'editorial_pauses':sum(durations),'aligned_words':len(moved)}))
def math_ceil_frame(t):
    import math
    return math.ceil((t-1e-7)*30)/30
if __name__=='__main__':main()
