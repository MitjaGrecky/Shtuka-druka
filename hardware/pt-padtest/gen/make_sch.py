#!/usr/bin/env python3
"""Write the PT schematic (KiCad 7 format) from design.py with the shared grid writer.
Run: python3 make_sch.py   (KiCad 10 PC: KICAD_SYMBOL_DIR=<repo>/hardware/common/sym7)   License: AGPL-3.0-or-later.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import design as D  # noqa: E402
import module_sch  # noqa: E402

if __name__ == "__main__":
    module_sch.write_grid(D, "7b1e4c92-3a56-4f0d-9c81-5d27ae60f4b3", "PT pad test board 4 x 4 (R194, P120)", HERE,
                          notes=(D.BUS_NOTE,
                                 "FSR1-FSR16 are copper combs of the board (no parts): pin 1 common to +3V3A, pins 2-5 zones, 10 k to GND each",
                                 "Rev 0.1: schematic and placed board, not routed"))
