#!/usr/bin/env python3
"""Write the BB1 schematic (KiCad 7 format) from design.py with the shared grid writer, and the project file.
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
    module_sch.write_grid(D, "c2a7e5b0-8d31-4f94-b6e2-5a1d9c3f7e18",
                          "BB1 battery board: 6 cells, 2 x BQ7791500",
                          HERE,
                          notes=(D.BUS_NOTE,
                                 "P143, R208: 6 cells XT60PW-M, two 3S packs with BQ7791500 (circuit of bm-bms3s)",
                                 "Rev 0.1: schematic and placed board"))
    B.write_project(os.path.join(HERE, ".."), D.NAME, getattr(D, "LAYERS", 2))   # 21.11.2026: 4-layer rules were overwritten with 2-layer ones
