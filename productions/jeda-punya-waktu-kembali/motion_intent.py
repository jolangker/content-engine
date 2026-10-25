from pathlib import Path
import json
V=Path(__file__).resolve().parent/'video'; assertions=[]
for s in json.loads((V/'scenes.json').read_text()):
    ident='f%02d'%s['n']
    # Assembly merges each source root into its host; assertions use mounted IDs.
    # f05 beat 4 is a zero-width SVG divider; its raster change is covered by motion_qa.
    late_group='b3' if s['n']==5 else 'b4'
    assertions.extend([dict(kind='appearsBy',selector=f'#host-{ident} .b1',bySec=s['start']+.5),dict(kind='appearsBy',selector=f'#host-{ident} .{late_group}',bySec=s['start']+s['duration']*.95)])
    local=V/f'compositions/frames/{ident}.motion.json'
    if local.exists():local.unlink()
assertions.append(dict(kind='keepsMoving',withinSelector='#root'))
data=dict(duration=88.32,maxStaticSec=2.2,assertions=assertions)
(V/'index.motion.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('Wrote 33 mounted-scene motion assertions')
