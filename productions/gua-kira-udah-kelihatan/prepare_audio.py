"""Use the maintained acoustic-boundary repair for this preserved episode."""
from pathlib import Path
import runpy
import sys

if __name__ == '__main__':
    production = Path(__file__).resolve().parent
    helper = production.parents[1] / '.agents/skills/shortform-production/scripts/repair_audio_boundaries.py'
    sys.path.insert(0, str(helper.parent))
    sys.argv = [str(helper), '--production', str(production)]
    runpy.run_path(str(helper), run_name='__main__')
