#!/usr/bin/env python3
"""Write the HU1 schematic (KiCad 7 format) from design.py with the shared grid writer, and the project file.
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
    module_sch.write_grid(D, "7d4e2a91-3c5b-4f68-a1d7-92e0b8c6f315",
                          "HU1 hold-up module +-14 V",
                          HERE,
                          notes=(D.BUS_NOTE,
                                 "P129, P130: 4 x 470 uF 25 V, 2 x 10 ohm, 2 x SS34",
                                 "Rev 0.1: schematic and placed board"))
    B.write_project(os.path.join(HERE, ".."), D.NAME, getattr(D, "LAYERS", 2))   # 21.11.2026: 4-layer rules were overwritten with 2-layer ones
