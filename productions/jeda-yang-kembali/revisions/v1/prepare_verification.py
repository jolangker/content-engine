import json,pathlib
P=pathlib.Path(__file__).resolve().parent;V=P/'video'
t=json.loads((V/'timing.json').read_text(encoding='utf-8'))
assertions=[]
for s in t['scenes']:
    scope=f'[data-composition-id="{s["id"]}"]'
    assertions.extend([
        {'kind':'appearsBy','selector':scope+' .headline','bySec':s['start']+.8},
        {'kind':'staysInFrame','selector':scope+' .actor:not(.actor-b)'},
        {'kind':'staysInFrame','selector':scope+' .actor-b'}
    ])
(V/'index.motion.json').write_text(json.dumps({'duration':t['duration'],'assertions':assertions},indent=2),encoding='utf-8')
print('42 root-level motion assertions prepared')
