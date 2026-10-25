from pathlib import Path
import json
V=Path(__file__).resolve().parent
for p in list(V.glob('verification*.json'))+[V/'catalog-captions.json']:
    raw=p.read_bytes()
    if not raw.strip():continue
    text=raw.decode('utf-16') if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else raw.decode('utf-8-sig')
    d=json.loads(text);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Structured reports normalized to UTF-8')
