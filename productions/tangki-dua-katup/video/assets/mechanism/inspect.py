from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mechanism import svg
out=Path(__file__).parent
out.joinpath('inspection.html').write_text('<html><body style="margin:0;background:#ECEEE9">'+svg()+'</body></html>',encoding='utf-8')
