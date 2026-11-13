#!/usr/bin/env python3
"""Write the M2 schematic (KiCad 7 format) from design.py with the shared grid writer (parts sheet, every pin labelled).
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
    module_sch.write_grid(D, "3c7a91e4-52b8-4f6d-9a0e-8b1d2f4c6e15",
                          "LP5864 0x40-0x43 (cells A-D: ring pairs Level 8+7, 6+5, 4+3, 2+1); CY8CMBR3108 0x37 on the encoder frames",
                          HERE,
                          notes=(D.BUS_NOTE,
                                 "Chain: U6 (Q7 -> SR_OUT) reads Level 8 A B push, Level 7 ..., U8 last (DS <- SR_IN, R3 pull-up)",
                                 "Touch: TR0-7 -> 560 R -> TOUCH0-7 = frame MP of ENC1-8 (Level 8 ... Level 1), as M1"))
