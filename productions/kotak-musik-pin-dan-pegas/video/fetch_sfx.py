"""Retrieve documented CC0/CC BY samples; never generate audio."""
from pathlib import Path
import requests,re,json
V=Path(__file__).resolve().parent;D=V/'assets/audio/sfx';D.mkdir(parents=True,exist_ok=True)
session=requests.Session()
pack='https://freesound.org/people/UbikPhonik/packs/11206/'
r=session.get(pack,timeout=25);r.raise_for_status()
links=list(dict.fromkeys(re.findall(r'href="(/people/UbikPhonik/sounds/\d+/)"',r.text)))
if not links:raise ValueError('No sample links found')
entries=[]
for link in links[:3]:
    url='https://freesound.org'+link;r=session.get(url,timeout=25);r.raise_for_status();s=r.text
    licenses=list(dict.fromkeys(re.findall(r'https?://creativecommons.org/(?:licenses|publicdomain)/[^"<> ]+',s)))
    previews=list(dict.fromkeys(re.findall(r'https://[^"<> ]+(?:hq|lq)\.mp3',s)))
    valid=[l for l in licenses if '/licenses/by/' in l or '/publicdomain/zero/' in l]
    if not valid or not previews:raise ValueError('No allowed licence/preview '+url+' '+str(licenses))
    preview=next((p for p in previews if '-hq.mp3' in p),previews[0]);b=session.get(preview,timeout=25);b.raise_for_status()
    name=f'music-box-note-{len(entries)+1}.mp3';(D/name).write_bytes(b.content)
    title=re.search(r'<title>(.*?)</title>',s,re.S).group(1).strip()
    entries.append(dict(path='assets/audio/sfx/'+name,source=dict(provider='Freesound',creator='UbikPhonik',title=title,url=url,license=valid[0],download=preview,role='Illustrative real music-box tooth release; not the depicted cylinder or melody')))
    (D/f'music-box-note-{len(entries)}.source.html').write_text(s,encoding='utf-8')
(D/'retrieved.json').write_text(json.dumps(entries,indent=2)+'\n',encoding='utf-8')
print(json.dumps(entries))
