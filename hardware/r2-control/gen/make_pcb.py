#!/usr/bin/env python3
"""Build the R2 board (placed, nets, no routing) with the shared board writer.
Run: python3 make_pcb.py   (KiCad 10 PC: KICAD_FOOTPRINT_DIR=<KiCad>/share/kicad/footprints)   License: AGPL-3.0-or-later.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import design as D  # noqa: E402
import module_pcb  # noqa: E402

if __name__ == "__main__":
    module_pcb.main(D, [(f"R2 Control rev {D.REV}", (30.0, 70.0)), ("Shtuka Druka CERN-OHL-S-2.0", (30.0, 71.6))], HERE)
