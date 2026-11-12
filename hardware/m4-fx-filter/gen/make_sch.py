#!/usr/bin/env python3
"""Write the M4 schematic (KiCad 7 format) from design.py with the shared module writer.
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
    module_sch.write(D, "5b1e7c22-8f3a-4d19-a6c0-2e9d4f7a1b04",
                     "LP5864 0x40 (ADDR 00): FX Mix ring CS9-17, Filter ring CS0-8; chain reads FX A B push, Filter A B push, 1, 1",
                     HERE)
