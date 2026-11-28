"""Retime 24fps 1x motion-preview master to 1.25x 30fps delivery with two-pass loudnorm,
extract verification frames and audio mix, and run episode_qa.py --fingerprint."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

mp = Path(__file__).resolve().parent
r10 = mp.parent
ver = mp / "verification"
frames_dir = ver / "frames"
ver.mkdir(parents=True, exist_ok=True)
frames_dir.mkdir(parents=True, exist_ok=True)

master = ver / "master-24fps.mp4"
delivered = r10 / "motion-preview.mp4"
mix_mp3 = ver / "delivered-mix.mp3"

# Pass 1: measure loudnorm stats on atempo=1.25 audio
p1 = subprocess.run(
    [
        "ffmpeg", "-y", "-i", str(master),
        "-vn", "-af", "atempo=1.25,loudnorm=I=-14.0:TP=-1.5:LRA=11:print_format=json",
        "-f", "null", "-",
    ],
    capture_output=True, text=True, check=True,
)
m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p1.stderr, re.S)
if not m:
    raise RuntimeError(f"Could not parse loudnorm pass 1:\n{p1.stderr[-800:]}")
stats = json.loads(m.group(0))
ln_filter = (
    f"atempo=1.25,loudnorm=I=-14.0:TP=-1.5:LRA=11:linear=true:"
    f"measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:"
    f"measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:"
    f"offset={stats['target_offset']}"
)

# Pass 2: restamp 24fps -> 30fps (exact 1.25x speed) with pitch-kept two-pass loudnorm audio
subprocess.check_call([
    "ffmpeg", "-y", "-v", "error",
    "-i", str(master),
    "-vf", "setpts=PTS/1.25,fps=30",
    "-af", ln_filter,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
    "-movflags", "+faststart",
    str(delivered),
])

# Extract delivered audio stream for native listening verification
subprocess.check_call([
    "ffmpeg", "-y", "-v", "error", "-i", str(delivered),
    "-vn", "-c:a", "libmp3lame", "-b:a", "192k", str(mix_mp3),
])

# Extract 10 representative decoded frames at 1.25x timestamps
# 1x -> 1.25x divide by 1.25:
# 0.55s (dig), 2.75s (liner), 4.25s (water fill), 5.60s (fish wide), 7.75s (fish toss),
# 11.15s (tag drop), 15.80s (total hold), 19.50s (dusk parallax + lit window),
# 23.10s (yellow signature + handle), 24.55s (end card)
stamps_1x = [0.55, 2.75, 4.25, 5.60, 7.75, 11.15, 15.80, 19.50, 23.10, 24.55]
for idx, t1 in enumerate(stamps_1x, 1):
    td = t1 / 1.25
    out_png = frames_dir / f"f{idx:02d}_1x-{t1:05.2f}s.png"
    subprocess.check_call([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{td:.3f}", "-i", str(delivered),
        "-frames:v", "1", str(out_png),
    ])

# Also build a single 5x2 contact sheet for fast visual review
contact = ver / "contact-sheet.png"
subprocess.check_call([
    "ffmpeg", "-y", "-v", "error",
    "-pattern_type", "sequence", "-i", str(frames_dir / "f%02d_*.png"),
    "-vf", "scale=360:-1,tile=5x2", str(contact),
]) if False else None

from PIL import Image
imgs = [Image.open(p).resize((360, 640), Image.LANCZOS) for p in sorted(frames_dir.glob("f*.png"))]
sheet = Image.new("RGB", (360 * 5, 640 * 2), (20, 24, 28))
for i, im in enumerate(imgs):
    sheet.paste(im, ((i % 5) * 360, (i // 5) * 640))
sheet.save(contact)

digest = hashlib.sha256(delivered.read_bytes()).hexdigest()
print(f"Delivered: {delivered} ({delivered.stat().st_size} bytes, sha256={digest[:16]})")

# Run episode_qa.py --fingerprint
qa = subprocess.run(
    [
        "python", ".agents/skills/shortform-production/scripts/episode_qa.py",
        "--fingerprint", str(delivered),
        "--caption-region", "88,1380,904,190",
    ],
    capture_output=True, text=True, check=True,
)
print(qa.stdout)
(ver / "fingerprint.json").write_text(qa.stdout, encoding="utf-8")
