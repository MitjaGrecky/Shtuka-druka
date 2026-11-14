#!/usr/bin/env python3
"""Write the R1 schematic (KiCad 7 format) from design.py with the shared grid writer, and the project file.
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
    module_sch.write_grid(D, "c5e19a83-2b7d-4f60-9e14-7a3d8b2c6f91",
                          "R1 audio front end: mic/Hi-Z two paths (R117), line 1-8 (+24 dBu), phono, outputs on relays",
                          HERE,
                          notes=(D.BUS_NOTE,
                                 "Level plan in design.py: every input -> differential pair, FS 2 Vrms diff, to the Cirrus buffers on A1",
                                 "Rev 0.1: schematic only; jacks vertical-mount Neutrik NCJ6FI-V, NJ3FD-V; RCA part to choose"))
    B.write_project(os.path.join(HERE, ".."), D.NAME)
