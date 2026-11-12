#!/usr/bin/env python3
"""Write the M5 schematic (KiCad 7 format) from design.py with the shared module writer.
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
    module_sch.write(D, "7c4d9e13-2a6b-4f80-b1d2-9e3c5a8f2d05",
                     "LP5864 0x40: Gain 1 ring + Clip 1 CS9-17, Gain 2 ring + Clip 2 CS0-8; chain reads Gain 1 A B push, Gain 2 A B push, 1, 1",
                     HERE)
