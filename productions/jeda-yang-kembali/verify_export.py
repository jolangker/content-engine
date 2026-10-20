"""Validate the current local corrective export; v1 verifier is archived in revisions/v1."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().with_name('verify_export_v2.py')),run_name='__main__')
