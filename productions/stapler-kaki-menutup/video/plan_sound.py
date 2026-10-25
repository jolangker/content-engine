from pathlib import Path
import json,hashlib,re,subprocess
V=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def motion_sha(p):return hashlib.sha256(re.sub(r'\s+data-hf-id=(?:"[^"]*"|\x27[^\x27]*\x27)','',p.read_text(encoding='utf-8')).encode()).hexdigest()
assets=json.loads((V/'assets/audio/sfx/assets.json').read_text());events=json.loads((V/'motion-events.json').read_text());timing=json.loads((V/'timing.json').read_text());cues=[]
for a in assets:
    a['duration_s']=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(V/a['path'])]))
for k,event in enumerate(events):
    editorial=event['role']=='editorial';asset='editorial' if editorial else 'hinge' if 'press' in event['action'] else 'metal'
    # Wire-bending macros use a quieter steel material accent rather than a large hinge clack.
    if event['scene'] in ['s08','s09','s10','s11']:asset='metal'
    a=next(a for a in assets if a['id']==asset)
    cues.append({'id':f'sfx-{k+1:02}-{event["scene"]}','scene':event['scene'],'asset':asset,'purpose':event['role']+' cue for '+event['action'],'trigger':'visible '+event['action']+' motion onset, shared across coupled parts','start':round(event['time']*30)/30,'duration':min(a['duration_s'],.4 if editorial else .52),'volume':.42 if editorial else .7,'track':4,'role':event['role']})
# First anvil touch occurs when p reaches .4 in s09 (.35 → .6), with power2.inOut.
s=timing[8];when=s['start']+(1.1+2*(.2/4)**(1/3))*s['motion_scale']
cues.append({'id':'sfx-first-anvil-contact','scene':'s09','asset':'metal','purpose':'Decisive first tip/anvil contact','trigger':'wire tips reach fixed y=490 groove entrance at p=.4','start':round(when*30)/30,'duration':.22,'volume':.85,'track':4,'role':'illustrative material'})
plan={'version':1,'decisions':{'narration':{'mode':'use','reason':'Root-env default ElevenLabs voice, eleven_v4, tagged 197-word request; native 88.64 s speech retained, -16 LUFS normalization and 450 ms onset.'},'bgm':{'mode':'none','reason':'Board permits optional music; intentional unscored inspection makes fine contacts and speech clear.'},'sfx':{'mode':'use','reason':'Reused quiet metal/hinge material cues and distinct editorial inspection accent, synchronized to causal action.'}},'assets':assets,'cues':cues,'timing_sha256':sha(V/'timing.json'),'narration_sha256':sha(V/'assets/audio/narration-master.wav'),'motion_sources':{f'compositions/{s["id"]}.html':motion_sha(V/f'compositions/{s["id"]}.html') for s in timing},'silence':'Identification and settled observation holds intentionally quiet; continued bending shares one cue rather than repetitive ticks. No sound asserts literal acoustic realism.','creative_listening':'Unavailable: objective waveform, onset, speech and export checks only; no full-speed perceptual or phone-speaker listening claimed.'}
(V/'sound_design.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'cues':len(cues),'assets':len(assets)}))
