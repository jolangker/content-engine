"""Build animated compositions, robust Pill Karaoke captions, and root timeline for Kerja Rodi Daendels."""
from pathlib import Path
import json, re

root = Path(__file__).resolve().parent
timing = json.loads((root / 'timing.json').read_text(encoding='utf-8'))
audio_meta = json.loads((root / 'audio_meta.json').read_text(encoding='utf-8'))
total_d = audio_meta['total_duration_s']

# 1. Build captions.html with full transcript and pre-built DOM (0 warnings)
transcript = []
for f in timing:
    s_offset = f['start'] + f['voice_offset']
    for w in f['words']:
        transcript.append({
            'text': w['text'],
            'start': round(s_offset + w['start'], 3),
            'end': round(s_offset + w['end'], 3)
        })

captions_html = f'''<template>
<style>
@font-face {{
  font-family: 'Space Grotesk';
  src: url('assets/fonts/space-grotesk-bold.ttf') format('truetype');
  font-weight: 700;
  font-display: block;
}}
@font-face {{
  font-family: 'Space Grotesk';
  src: url('assets/fonts/space-grotesk-medium.ttf') format('truetype');
  font-weight: 500;
  font-display: block;
}}

#captions-root {{
  position: absolute;
  inset: 0;
  width: 1080px;
  height: 1920px;
  pointer-events: none;
}}

.caption-layer {{
  position: absolute;
  inset: 0;
}}

.safe-zone {{
  position: absolute;
  top: 1580px;
  left: 108px;
  width: 864px;
  height: 110px;
  display: flex;
  align-items: center;
  justify-content: center;
}}

.caption-group {{
  position: absolute;
  inset: 0;
  width: 864px;
  height: 110px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
}}

.caption-pill {{
  max-width: 864px;
  padding: 12px 28px;
  border-radius: 8px;
  background: rgba(24, 22, 21, 0.94);
  border: 1px solid rgba(195, 40, 34, 0.4);
  box-shadow: 0 10px 30px rgba(0,0,0,0.8);
  text-align: center;
}}

.caption-copy {{
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 38px;
  font-weight: 500;
  line-height: 1.25;
}}

.caption-word {{
  display: inline-block;
  color: #8C8579;
}}
</style>

<div id="captions-root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{total_d}">
  <div class="caption-layer">
    <div id="caption-stage" class="safe-zone"></div>
  </div>
</div>

<script>
  var DURATION = {total_d};
  var TRANSCRIPT = {json.dumps(transcript)};
  var COLOR_INACTIVE = "#8C8579";
  var COLOR_ACTIVE = "#EAE0D0";
  var COLOR_FADE_DURATION = 0.08;

  function makeGroups(words) {{
    var groups = [];
    var current = [];
    words.forEach(function(word, index) {{
      current.push(word);
      var nextWord = words[index + 1];
      var hasPunctuation = /[,.:!?]$/.test(word.text);
      var pauseDuration = nextWord ? (nextWord.start - word.end) : 0;
      var hasPause = pauseDuration >= 0.35;
      if (current.length >= 4 || hasPunctuation || hasPause || !nextWord) {{
        groups.push({{
          words: current.slice(),
          start: current[0].start,
          end: current[current.length - 1].end
        }});
        current = [];
      }}
    }});
    if (current.length) {{
      groups.push({{
        words: current.slice(),
        start: current[0].start,
        end: current[current.length - 1].end
      }});
    }}
    return groups;
  }}

  function buildCaptions(groups) {{
    var stage = document.getElementById("caption-stage");
    groups.forEach(function(group, groupIndex) {{
      var groupEl = document.createElement("div");
      groupEl.id = "caption-group-" + groupIndex;
      groupEl.className = "caption-group";

      var pillEl = document.createElement("div");
      pillEl.className = "caption-pill";

      var copyEl = document.createElement("div");
      copyEl.className = "caption-copy";

      group.words.forEach(function(word, wordIndex) {{
        var wordEl = document.createElement("span");
        wordEl.id = "caption-word-" + groupIndex + "-" + wordIndex;
        wordEl.className = "caption-word";
        wordEl.textContent = word.text;
        copyEl.appendChild(wordEl);
      }});

      pillEl.appendChild(copyEl);
      groupEl.appendChild(pillEl);
      stage.appendChild(groupEl);
    }});
  }}

  var GROUPS = makeGroups(TRANSCRIPT);
  buildCaptions(GROUPS);

  window.__timelines = window.__timelines || {{}};
  var tl = gsap.timeline({{ paused: true }});

  GROUPS.forEach(function(group, groupIndex) {{
    var groupEl = document.getElementById("caption-group-" + groupIndex);
    var nextGroup = GROUPS[groupIndex + 1];
    var isLastGroup = groupIndex === GROUPS.length - 1;
    var effectiveEnd = isLastGroup ? DURATION : Math.min(nextGroup.start, group.end + 0.25);
    var visibleStart = Math.max(0, group.start - 0.05);

    tl.set(groupEl, {{ opacity: 1, visibility: "visible" }}, visibleStart);
    tl.set(groupEl, {{ opacity: 0, visibility: "hidden" }}, effectiveEnd);

    group.words.forEach(function(word, wordIndex) {{
      var wordEl = document.getElementById("caption-word-" + groupIndex + "-" + wordIndex);
      var isFirstWord = (wordIndex === 0);
      tl.set(wordEl, {{ color: isFirstWord ? COLOR_ACTIVE : COLOR_INACTIVE }}, visibleStart);
      if (!isFirstWord) {{
        tl.to(wordEl, {{ color: COLOR_ACTIVE, duration: COLOR_FADE_DURATION, ease: "none" }}, word.start);
      }}
    }});
  }});

  window.__timelines["captions"] = tl;
</script>
</template>'''

(root / 'compositions/captions.html').write_text(captions_html, encoding='utf-8')
print("Wrote captions.html with pre-built DOM")

# 2. Update scenes with adjusted padding and GSAP animations
# Frame 1
f1_path = root / 'compositions/frames/01-hook-anomali.html'
f1_content = f1_path.read_text(encoding='utf-8')
f1_anim = '''<script>
  const tl = gsap.timeline({ paused: true });
  tl.fromTo(".dossier-card", { opacity: 0, y: 35 }, { opacity: 1, y: 0, duration: 0.65, ease: "power3.out" }, 0.15);
  tl.fromTo(".stamp-badge", { scale: 1.25, opacity: 0, rotate: 10 }, { scale: 1, opacity: 1, rotate: -3, duration: 0.45, ease: "back.out(1.5)" }, 0.4);
  tl.fromTo(".quote-block", { opacity: 0 }, { opacity: 1, duration: 0.5 }, 1.2);
  tl.fromTo(".redacted-highlight", { opacity: 0.3 }, { opacity: 1, duration: 0.35, ease: "power2.inOut" }, 4.2);
  tl.fromTo(".bottom-evidence", { opacity: 0, y: 15 }, { opacity: 1, y: 0, duration: 0.5 }, 5.0);
  window.__timelines = window.__timelines || {};
  window.__timelines["scene-01"] = tl;
</script>'''
f1_content = re.sub(r'<script>.*?</script>', f1_anim, f1_content, flags=re.DOTALL)
f1_path.write_text(f1_content, encoding='utf-8')

# Frame 3
f3_path = root / 'compositions/frames/03-upah-bertingkat.html'
f3_content = f3_path.read_text(encoding='utf-8')
f3_content = f3_content.replace('padding: 140px 64px 280px;', 'padding: 140px 64px 380px;')
f3_content = f3_content.replace('color: #7C756B;', 'color: #A39B8F;')
f3_anim = '''<script>
  const tl = gsap.timeline({ paused: true });
  tl.fromTo(".section-head", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5 }, 0.15);
  tl.fromTo(".rate-card:nth-child(1)", { opacity: 0, x: -25 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, 1.0);
  tl.fromTo(".rate-card:nth-child(2)", { opacity: 0, x: 25, scale: 0.96 }, { opacity: 1, x: 0, scale: 1, duration: 0.65, ease: "power3.out" }, 6.2);
  tl.fromTo(".summary-card", { opacity: 0, y: 15 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 10.5);
  window.__timelines = window.__timelines || {};
  window.__timelines["scene-03"] = tl;
</script>'''
f3_content = re.sub(r'<script>.*?</script>', f3_anim, f3_content, flags=re.DOTALL)
f3_path.write_text(f3_content, encoding='utf-8')

# Frame 5
f5_path = root / 'compositions/frames/05-rantai-feodal.html'
f5_content = f5_path.read_text(encoding='utf-8')
f5_content = f5_content.replace('padding: 140px 64px 280px;', 'padding: 140px 64px 380px;')
f5_content = f5_content.replace('gap: 16px;', 'gap: 12px;')
f5_content = f5_content.replace('padding: 24px 32px;', 'padding: 20px 28px;')
f5_anim = '''<script>
  const tl = gsap.timeline({ paused: true });
  tl.fromTo(".flow-node:nth-of-type(1)", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 0.2);
  tl.fromTo(".arrow-divider:nth-of-type(2)", { opacity: 0 }, { opacity: 1, duration: 0.35 }, 4.0);
  tl.fromTo(".flow-node.highlight", { opacity: 0, scale: 0.97, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.65, ease: "power3.out" }, 4.5);
  tl.fromTo(".arrow-divider:nth-of-type(4)", { opacity: 0 }, { opacity: 1, duration: 0.35 }, 10.5);
  tl.fromTo(".flow-node:nth-of-type(5)", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 11.2);
  tl.fromTo(".end-card", { opacity: 0, y: 15 }, { opacity: 1, y: 0, duration: 0.5 }, 14.8);
  window.__timelines = window.__timelines || {};
  window.__timelines["scene-05"] = tl;
</script>'''
f5_content = re.sub(r'<script>.*?</script>', f5_anim, f5_content, flags=re.DOTALL)
f5_path.write_text(f5_content, encoding='utf-8')

print("Refined scenes and animations")
