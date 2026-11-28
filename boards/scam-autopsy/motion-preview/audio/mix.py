"""Rebuild the pilot audio at 48 kHz with FFmpeg. Cue times use the final video clock."""
import subprocess
from pathlib import Path

audio = Path(__file__).resolve().parent
sources = [
    "-i", str(audio / "narration.mp3"),
    "-i", str(audio / "soft-ping.wav"),
    "-f", "lavfi", "-i", "aevalsrc=0.24*sin(2*PI*125*t)*(0.65+0.35*sin(2*PI*32*t)):s=48000:d=0.25",
    "-f", "lavfi", "-i", "sine=frequency=117:sample_rate=48000:duration=0.76",
]
graph = ";".join([
    "[0:a]aresample=48000,apad=whole_dur=16.5[voice]",
    "[1:a]volume=0.85,adelay=4420[ping]",
    "[2:a]afade=t=in:d=0.03,afade=t=out:st=0.17:d=0.08,volume=0.29,adelay=80[buzz]",
    "[3:a]afade=t=in:d=0.16,afade=t=out:st=0.2:d=0.56,volume=0.18,adelay=6570[tone]",
    "[voice][ping][buzz][tone]amix=inputs=4:duration=first:normalize=0,"
    "loudnorm=I=-14:TP=-1:LRA=7,aformat=channel_layouts=mono,aresample=48000,atrim=duration=16.5[mix]",
])
if __name__ == "__main__":
    subprocess.run(["ffmpeg", "-v", "error", "-y", *sources, "-filter_complex", graph,
                    "-map", "[mix]", "-c:a", "pcm_s16le", str(audio / "pilot-mix.wav")], check=True)
