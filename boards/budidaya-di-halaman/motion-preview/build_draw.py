"""Rebuild motion-preview self-contained assets from the board's helpers and organic SFX library."""
import shutil
from pathlib import Path

mp = Path(__file__).resolve().parent
board = mp.parent

(mp / "assets/fonts").mkdir(parents=True, exist_ok=True)
(mp / "assets/audio").mkdir(parents=True, exist_ok=True)

shutil.copy2(board / "assets/world-v5.js", mp / "assets/world-v5.js")
for f in (board / "assets/sfx").glob("*.mp3"):
    shutil.copy2(f, mp / "assets/audio" / f.name)
shutil.copy2(board / "assets/sfx/CREDITS.md", mp / "assets/audio/CREDITS.md")

def cut(text: str) -> str:
    return text[: text.rindex("for (const [id, draw] of Object.entries(")]

a = cut((board / "assets/studies.js").read_text(encoding="utf-8"))
b = cut((board / "assets/studies-r6.js").read_text(encoding="utf-8")).replace('"use strict";\n', "")
(mp / "assets/draw.js").write_text(
    "// Generated from ../assets/studies.js and ../assets/studies-r6.js (helpers only). Rebuild with build_draw.py.\n" + a + b,
    encoding="utf-8",
)
print("rebuilt motion-preview assets OK")
