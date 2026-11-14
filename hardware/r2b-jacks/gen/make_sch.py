#!/usr/bin/env python3
"""Write the R2b schematic (KiCad 7 format) from design.py with the shared grid writer, and the project file.
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
    module_sch.write_grid(D, "3b7e1f52-8c4d-4a69-b2e0-5d9a6c1f7e83",
                          "R2b jack shelf (R139): MIDI DIN 2 in / 4 out, USB-C PC, USB-A, USB-C PD 5 A, DC",
                          HERE,
                          notes=(D.BUS_NOTE,
                                 "MIDI parts (CA-033 resistors, TLP2361) are on R2; this board carries jacks, ESD and cables only",
                                 "Rev 0.1: schematic only; outline and jack positions follow the rear panel v2 (tools/rear_panel.py)"))
    B.write_project(os.path.join(HERE, ".."), D.NAME)
