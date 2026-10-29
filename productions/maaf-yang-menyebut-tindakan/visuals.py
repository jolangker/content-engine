"""Pose the sixteen scenes, then assemble measured worker-owned animations."""
from pathlib import Path
import argparse
import html
import json

P=Path(__file__).resolve().parent;V=P/'video';C='#F3EDE3';I='#302B28';A='#A34F3F';S='#D8C8B5'
def path(d,c=I,w=5,fill='none',extra=''):return f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def line(x,y,xx,yy,c=I,w=5):return path(f'M{x} {y}L{xx} {yy}',c,w)
def circle(x,y,r,c=I,fill='none',w=5):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{w}"/>'
def rect(x,y,w,h,c=S,fill='none',r=25):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" stroke="{c}" stroke-width="5" fill="{fill}"/>'
def group(n,body):return f'<g id="beat{n}">{body}</g>'
def actor(x,y,k=1,c=I,other=False):
    d='M-72 -94C-15 -130 65 -102 88 -39C111 24 65 103 9 111C-54 121 -100 83 -105 15C-111 -35 -105 -73 -72 -94Z' if not other else 'M-75 -77C-34 -112 34 -100 72 -66C110 -31 105 24 75 71C41 120 -26 104 -63 77C-96 53 -110 -36 -75 -77Z'
    return f'<g transform="translate({x} {y}) scale({k})">{path(d,c,1,c)}</g>'
def plate(x,y,r=95,c=I):return circle(x,y,r,c)+circle(x,y,r*.64,S,w=3)+line(x-r-28,y-r*.7,x-r-28,y+r*.7,c,4)+line(x+r+30,y-r*.7,x+r+30,y+r*.7,c,4)
def bowl(x,y,k=1,c=I):return f'<g transform="translate({x} {y}) scale({k})">'+path('M-170 0Q0 260 170 0Z',c,6,S)+path('M-170 0Q0 -50 170 0',c,6)+path('M-115 5Q0 35 115 5',A,5)+'</g>'
def recipe(x,y,k=1,c=I):return f'<g transform="translate({x} {y}) scale({k})">'+rect(-110,-165,220,330,c,C)+line(-65,-100,55,-100,c,5)+circle(-62,-30,9,A,A)+line(-25,-30,65,-30,c,4)+circle(-62,30,9,A,A)+line(-25,30,65,30,c,4)+circle(-62,90,9,A,A)+line(-25,90,45,90,c,4)+'</g>'
def bubble(x,y,w=360,h=160,c=I):return path(f'M{x+25} {y}H{x+w-25}Q{x+w} {y} {x+w} {y+25}V{y+h-25}Q{x+w} {y+h} {x+w-25} {y+h}H{x+100}L{x+50} {y+h+60}L{x+60} {y+h}H{x+25}Q{x} {y+h} {x} {y+h-25}V{y+25}Q{x} {y} {x+25} {y}Z',c,5)
def ribbon(x,y,w=220,c=A):return path(f'M{x} {y}C{x+w*.3} {y-45} {x+w*.6} {y+45} {x+w} {y}',c,5)
def dough(x,y,k=1,c=I):return f'<g transform="translate({x} {y}) scale({k})">'+path('M-115 30C-145 -30 -45 -85 20 -60C70 -90 165 -10 110 50C70 100 -90 100 -115 30Z',c,5,S)+path('M-40 -15Q-10 0 -20 35M35 -20Q55 0 45 30',A,4)+'</g>'

FONTS="@font-face{font-family:'Newsreader';src:url('assets/fonts/newsreader.ttf')}@font-face{font-family:'DM Sans';src:url('assets/fonts/dm-sans.ttf')}"
def schedule(lines):
    if (V/'timing.json').exists():return json.loads((V/'timing.json').read_text(encoding='utf-8'))['scenes']
    weights=[len(x['text'].split()) for x in lines];total=sum(weights);ts=[];start=0
    for x,w in zip(lines,weights):
        end=start+90*w/total;ts.append(dict(id=x['id'],start=start,end=end,duration=end-start));start=end
    return ts
def pose(x,t):
    n=x['id'];cid=f'f{n:02d}';d=t['duration'];ink=C if x['dramatic'] else I;bg=I if x['dramatic'] else C
    chrome=(V/'assets/board/components/chrome.html').read_text(encoding='utf-8').replace('{{frame_number}}',f'{n:02d}').replace('{{frame_count}}','16')
    css=FONTS+(V/'assets/board/components/chrome.css').read_text(encoding='utf-8')+f"#root{{position:absolute;inset:0;width:100%;height:100%;color:{ink};--rda-meta-ink:{ink};font-family:'DM Sans',sans-serif}}.ground{{position:absolute;inset:0;background:{bg}}}.drawing{{position:absolute;inset:0;width:1080px;height:1920px}}.heading{{position:absolute;left:88px;top:270px;width:848px;margin:0;font:400 {76 if n==2 else 82}px/1.06 'Newsreader',serif;letter-spacing:-.02em}}.pose-caption{{position:absolute;left:88px;top:1550px;width:848px;text-align:center;font:500 46px/1.25 'DM Sans',sans-serif}}"
    variables=html.escape(json.dumps([dict(id='emphasis',type='string',label='Scene emphasis',default=x['emphasis'])],ensure_ascii=False),quote=True)
    main=f'<div id="root" data-composition-id="{cid}" data-composition-variables="{variables}" data-start="0" data-duration="{d:.17g}" data-width="1080" data-height="1920"><div id="ground" class="clip ground" data-start="0" data-duration="{d:.17g}" data-track-index="0"></div>{chrome}<svg id="drawing" class="clip drawing" data-start="0" data-duration="{d:.17g}" data-track-index="1" viewBox="0 0 1080 1920" aria-label="{html.escape(DESIGNS[n-1][0])}">{"".join(art(n,x["dramatic"]))}</svg>'
    if x['emphasis']:main+=f'<h1 id="heading" class="clip heading" data-var-text="emphasis" data-start="0" data-duration="{d:.17g}" data-track-index="2">{html.escape(x["emphasis"])}</h1>'
    main+=f'<div class="pose-caption">{html.escape(" ".join(x["text"].split()[:6]))}</div></div>'
    return f'<template><style>{css}</style>{main}<script>const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration:{d:.17g}}},0);window.__timelines["{cid}"]=tl;</script></template>'
def index(lines,ts,animated):
    total=ts[-1]['end'];hosts=[]
    for x,t in zip(lines,ts):
        n=x['id'];hosts.append(f'<div id="scene-{n:02d}" class="clip scene-host" data-composition-id="f{n:02d}" data-composition-src="compositions/frames/f{n:02d}.html" data-start="{t["start"]:.17g}" data-duration="{t["duration"]:.17g}" data-width="1080" data-height="1920" data-track-index="1" data-track-kind="graphics" style="z-index:{n}"></div>')
    if animated:
        pl=json.loads((V/'placement.json').read_text(encoding='utf-8'))
        hosts+=[f'<audio id="narration" class="clip" src="{pl["path"]}" data-start="0" data-duration="{pl["duration"]:.17g}" data-volume="1" data-track-index="3"></audio>',f'<div id="caption-host" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{total:.17g}" data-width="1080" data-height="1920" data-track-index="2" data-track-kind="captions" style="z-index:100"></div>']
    return f'<!doctype html><html lang="id" data-resolution="portrait"><head><meta charset="UTF-8"><title>Maaf yang menyebut tindakan</title><script src="vendor/gsap.min.js"></script><style>{FONTS}*{{box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:{C}}}#root{{position:relative;width:100%;height:100%;background:{C}}}.scene-host{{position:absolute;inset:0}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{total:.17g}" data-width="1080" data-height="1920">{"".join(hosts)}</div><script>const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration:{total:.17g}}},0);window.__timelines.main=tl;</script></body></html>'
