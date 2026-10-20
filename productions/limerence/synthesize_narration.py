"""Use the maintained project narration entry point; --check validates without synthesis."""
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / '.agents/skills/shortform-production/scripts'))
from narration import main

if __name__ == '__main__':
    sys.argv[1:1] = ['--video', str(Path(__file__).resolve().parent / 'video'), '--project-root', str(root)]
    main()
