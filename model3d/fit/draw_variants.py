#!/usr/bin/env python3
"""Draw the case variants with make_drawing.py, each in a clean environment (16.11.2026).
  drawing                  - current case (68 / 143, H5 under P2)
  drawing_step_batt_screen - step case, deck 22, fold 56, one LiPo pack under the screen, 60 mm fan on the right wall
Run: python draw_variants.py   (KiCad 10 python)."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VARIANTS = {
    "drawing": {},
    "drawing_step_batt_screen": dict(WHEEL_TRACK=1, COMPUTER="H5REAR", BATT_LIPO=0, P2_PARTS=1.5, PANEL_PARTS=3, H5_REAR_X=410,
                                     H5_REAR_Y=369.4, PW_X0=245, A1_X0=20, H5_PORT="E", F1_MODE="LIP", FRONT_LIP=28, REAR_SHIFT=20,
                                     DECK=22, FRONT_Z=56, BATT_BOXES="10,180,325,425,29", FAN="400,4,60"),
}
KEEP = ("PATH", "SYSTEMROOT", "TEMP", "TMP", "USERPROFILE", "PYTHONPATH", "KICAD_SYMBOL_DIR", "KICAD_FOOTPRINT_DIR", "APPDATA", "LOCALAPPDATA")
for name, env in VARIANTS.items():
    e = {k: v for k, v in os.environ.items() if k.upper() in KEEP}
    e.update({k: str(v) for k, v in env.items()}, DRAWING_NAME=name)
    subprocess.run([sys.executable, os.path.join(HERE, "make_drawing.py")], env=e, check=True)
