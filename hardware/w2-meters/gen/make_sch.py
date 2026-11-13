#!/usr/bin/env python3
"""Write the W2 schematic (KiCad 7 format) from design.py with the shared grid writer.
Run: python3 make_sch.py   (KiCad 10 PC: see hardware/m3-tempo-swing/README.md)   License: AGPL-3.0-or-later.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import design as D  # noqa: E402
import module_sch  # noqa: E402

if __name__ == "__main__":
    module_sch.write_grid(D, "9e2f4b67-1c3d-4a58-8b90-3f6e1d2c7a06",
                          "LP5864 L 0x40 (U1, D1-D14), R 0x41 (U2, D15-D28); LED i: CS triple i div 4, SW i mod 4", HERE,
                          notes=(D.BUS_NOTE, "Meters L and R: 14 RGB each, D1/D15 at the bottom (fold side)"))
