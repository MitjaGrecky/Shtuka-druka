#!/usr/bin/env python3
"""Write the W3 schematic (KiCad 7 format) from design.py with the shared grid writer.
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
    module_sch.write_grid(D, "4d8a1f35-6b2e-4c97-a0d3-5e7f9b2c1a07",
                          "LP5864 0x40: D1-D2 Save, D3-D4 Project, D5 record light; LED i: CS triple i div 4, SW i mod 4", HERE,
                          notes=(D.BUS_NOTE, "Power button: off this board (behind the USB/SD pocket), see design.py"))
