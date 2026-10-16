"""Generate the explicitly selected Indonesian voice and retain native timings."""
from pathlib import Path
import asyncio, json, re, subprocess, sys

root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'.media/tts-packages'))
import edge_tts
frames=json.loads((root/'boards/frame-manifest.json').read_text(encoding='utf-8'))
out=root/'assets/voice'
out.mkdir(parents=True,exist_ok=True)
voice='id-ID-ArdiNeural'
rate='+15%'

def duration(path):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(path)],text=True).split('"duration": "')[1].split('"')[0])

async def main():
    sem=asyncio.Semaphore(2)
    async def line(f):
        mp3=out/f"scene-{f['n']:02d}-ardi.mp3"
        meta=mp3.with_suffix('.words.json')
        receipt=mp3.with_suffix('.receipt.json')
        request={'voice':voice,'rate':rate,'text':f['vo']}
        if mp3.exists() and meta.exists() and receipt.exists() and json.loads(receipt.read_text(encoding='utf-8'))==request:
            words=json.loads(meta.read_text(encoding='utf-8'))
        else:
            async with sem:
                words=[]
                with mp3.open('wb') as audio:
                    communicate=edge_tts.Communicate(f['vo'],voice=voice,rate=rate,boundary='WordBoundary')
                    async for chunk in communicate.stream():
                        if chunk['type']=='audio':audio.write(chunk['data'])
                        elif chunk['type']=='WordBoundary':
                            words.append({'id':f"w{len(words)}",'text':chunk['text'],'start':chunk['offset']/10_000_000,'end':(chunk['offset']+chunk['duration'])/10_000_000})
                assert words and mp3.stat().st_size>1000,f'Missing audio/timings for {f["n"]}'
                meta.write_text(json.dumps(words,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
                receipt.write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        d=duration(mp3)
        assert words[-1]['end'] <= d+.1,(f['n'],d,words[-1])
        return {'id':str(f['n']),'frame':f['n'],'provider':'edge-tts','voice':voice,'path':mp3.relative_to(root).as_posix(),'duration_s':d,'words':words,'timing_source':'native Microsoft WordBoundary, 100ns ticks converted to seconds','text':f['vo'],'rate':rate}
    voices=await asyncio.gather(*(line(f) for f in frames))
    position=0
    for i,(f,v) in enumerate(zip(frames,voices)):
        f['original_start']=f['start'];f['original_duration']=f['duration']
        f['start']=round(position,3)
        f['voice_offset']=.3
        f['voice_duration']=v['duration_s']
        tail=1.1 if i==5 else .5
        f['duration']=round(f['voice_offset']+v['duration_s']+tail,3)
        f['poster']=round(position+f['duration']-.5,3)
        f['words']=v['words']
        f['audio']=v['path']
        v['start_s']=round(position+f['voice_offset'],3)
        position+=f['duration']
    manifest={'voices':voices,'sfx':[],'bgm':None,'total_duration_s':round(position,3),'provider':'edge-tts','voice':voice,'rate':rate,'source_script':'../SCRIPT.md v1 approved','timings':'native word boundary; no uniform interpolation','notes':'Ardi chosen explicitly. Preview v1 has narration with deliberate pauses; music/SFX not selected.'}
    (root/'audio_meta.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (root/'timing.json').write_text(json.dumps(frames,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    ledger=root/'.media/manifest.jsonl';ledger.parent.mkdir(exist_ok=True)
    with ledger.open('a',encoding='utf-8') as fp:
        for v in voices:
            fp.write(json.dumps({'type':'voice','path':v['path'],'provider':'edge-tts','voice':voice,'rate':rate,'source_text':v['text'],'authorization':'User selected Ardi/Microsoft Edge on 2026-10-17','duration_s':v['duration_s'],'word_timestamps':'native'},ensure_ascii=False)+'\n')
    print(json.dumps({'voice':voice,'rate':rate,'total_duration_s':manifest['total_duration_s'],'scenes':[{'frame':f['n'],'duration':f['duration'],'words':len(f['words'])} for f in frames]}))

asyncio.run(main())
