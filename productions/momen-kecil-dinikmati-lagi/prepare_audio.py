"""Place unchanged native speech inside verified quiet regions before normalization."""
from pathlib import Path
import importlib.util,json,math,re,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[1];V=P/'video'
sys.path.insert(0,str(ROOT/'.agents/skills/shortform-production/scripts'))
import audio_boundaries as a
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    native=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'))['voices'][0]
    lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));words=native['words'];ends=[];cursor=0
    norm=lambda s:re.sub(r'\W','',s.casefold())
    for x in lines:
        expected=x['text'].split();actual=words[cursor:cursor+len(expected)]
        assert [norm(w) for w in expected]==[norm(w['text']) for w in actual],x['id']
        cursor+=len(expected);ends.append(cursor)
    assert cursor==len(words)==204
    samples=a.decode(V/native['path']);native_s=len(samples)/a.RATE
    pre=.16;hold=1.5;target=max(90,math.ceil((native_s+pre+.30*15+hold)*30)/30)
    weights=[1.5 if i in (7,8,9,10) else 1 for i in range(1,16)]
    budget=target-native_s-pre-hold;pauses=[budget*w/sum(weights) for w in weights]
    placed,moved,boundaries,utterances=a.place(samples,words,ends,pauses,pre)
    duration=math.ceil(max(target,len(placed)/a.RATE+hold)*30)/30
    starts=[0]+[b['visual_s'] for b in boundaries];stops=starts[1:]+[duration]
    scenes=[dict(id=x['id'],**u,start=start,end=stop,duration=stop-start,start_frame=round(start*30),end_frame=round(stop*30),dramatic=x['dramatic']) for x,u,start,stop in zip(lines,utterances,starts,stops)]
    timing=dict(duration_s=duration,voice_duration_s=len(placed)/a.RATE,words=moved,scenes=scenes,basis='Untouched native-speed recording, measured quiet-region pause insertion, integer 30fps visual anchors. Individual word timestamps remain estimates.')
    dump(V/'timing.json',timing)
    master=V/'assets/audio/narration-boundary-master.wav';raw=V/'assets/audio/narration-before-level.wav';dest=V/'assets/audio/narration.wav'
    a.write_pcm(master,samples);a.write_pcm(raw,placed);normalization=a.normalize_after_placement(raw,dest,-16,-2,7)
    receipt=dict(version=2,path=dest.relative_to(V).as_posix(),sha256=a.digest(dest),source=native['path'],source_sha256=a.digest(V/native['path']),master_path=master.relative_to(V).as_posix(),master_sha256=a.digest(master),duration_s=len(placed)/a.RATE,duration=len(placed)/a.RATE,pre_roll_s=pre,speech_speed=1,speech_samples_preserved_before_normalization=True,normalization=normalization,timestamp_precision='Acoustic scene anchors; word estimates reanchored within each utterance.',sample_rate=a.RATE,fps=30,timing_sha256=a.digest(V/'timing.json'),boundaries=boundaries)
    dump(V/'audio_boundaries.json',receipt);dump(V/'placement.json',dict(**receipt,pauses=boundaries,words=moved))
    # The canonical shared scene map needs at least eight decimals for frame fractions.
    f=P/'visuals.py';f.write_text(f.read_text(encoding='utf-8').replace(':.5f',':.8f'),encoding='utf-8')
    with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Measured narration\n\nOne synthesis call succeeded: ElevenLabs eleven_v4, root voice, {native_s:.2f}s, 204 aligned words. Native samples retained before quiet-region pause insertion and one final loudness normalization. Composition {duration:.5f}s; {len(boundaries)} verified integer-frame scene anchors. No speed change. Word timestamps remain estimates. Perceptual listening unavailable; acoustic checks and later export checks are separate evidence.\n')
    print(json.dumps(dict(native_seconds=native_s,placed_seconds=receipt['duration_s'],composition_seconds=duration,scenes=len(scenes),boundaries=len(boundaries))))
if __name__=='__main__':main()
