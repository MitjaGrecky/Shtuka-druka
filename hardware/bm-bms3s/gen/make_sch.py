#!/usr/bin/env python3
"""Write the BM schematic (KiCad 7 format) from design.py with the shared grid writer, and the project file.
Run: python3 make_sch.py   (KiCad 10 PC: KICAD_SYMBOL_DIR=<repo>/hardware/common/sym7)   License: AGPL-3.0-or-later.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import design as D  # noqa: E402
import module_sch  # noqa: E402
import boardkit as B  # noqa: E402

if __name__ == "__main__":
    module_sch.write_grid(D, "b3c81f5e-47a2-4d90-9e6b-1a5c7d2f8e04",
                          "BM battery protection 3S: BQ7791500, CSD18540Q5B x 2, 5 mOhm",
                          HERE,
                          notes=(D.BUS_NOTE,
                                 "TI SLUSCU0L fig. 9-11 / table 10-1; 3S 4.2 V; OCD 60 mV / 5 mOhm = 12 A",
                                 "Rev 0.1: schematic and placed board"))
    B.write_project(os.path.join(HERE, ".."), D.NAME)
