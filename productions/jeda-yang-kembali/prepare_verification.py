"""Check the current generated motion specification without replacing scene-specific assertions."""
from pathlib import Path
import json
p=Path(__file__).resolve().parent/'video'
spec=json.loads((p/'index.motion.json').read_text(encoding='utf-8'))
timing=json.loads((p/'timing.json').read_text(encoding='utf-8'))
assert abs(spec['duration']-timing['duration'])<1e-5
for scene in timing['scenes']:
    assert any(scene['id'] in item.get('selector','') for item in spec['assertions'])
print(f"{len(spec['assertions'])} scene-specific assertions retained; run the HyperFrames browser check next")
