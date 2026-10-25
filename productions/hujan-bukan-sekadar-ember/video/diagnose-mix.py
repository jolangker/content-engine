from pathlib import Path
s=Path('verify-export.py').read_text(encoding='utf-8')
start=s.index('def pcm(')
end=s.index("assert corr>.98")
exec('from pathlib import Path\nimport json,subprocess,numpy as np\nfrom scipy.signal import correlate,correlation_lags\nV=Path.cwd();out=V.parent/\"exports/hujan-bukan-sekadar-ember.mp4\"\ndef run(args): return subprocess.run(args,capture_output=True,check=True)\n'+s[start:end])
