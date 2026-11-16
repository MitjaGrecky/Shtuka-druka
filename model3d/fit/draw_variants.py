#!/usr/bin/env python3
"""Draw the case variants with make_drawing.py, each in a clean environment (16.11.2026).
  drawing                  - current case (68 / 143, H5 under P2)
  drawing_step_batt_screen - step case, deck 22, fold 56, one LiPo pack under the screen, 60 mm fan on the right wall
Run: python draw_variants.py   (KiCad 10 python)."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
VARIANTS = {
    "drawing": {},
    # doc 39: the agreed low case: shelf +40 (R166), riser 20 mm further back (R167), fold 56 with 8 mm under the H5
    "drawing_low_case": dict(__import__("low_case_final").config(40, fs=20), FRONT_Z=56),
}
KEEP = ("PATH", "SYSTEMROOT", "TEMP", "TMP", "USERPROFILE", "PYTHONPATH", "KICAD_SYMBOL_DIR", "KICAD_FOOTPRINT_DIR", "APPDATA", "LOCALAPPDATA")
for name, env in VARIANTS.items():
    e = {k: v for k, v in os.environ.items() if k.upper() in KEEP}
    e.update({k: str(v) for k, v in env.items()}, DRAWING_NAME=name)
    subprocess.run([sys.executable, os.path.join(HERE, "make_drawing.py")], env=e, check=True)
