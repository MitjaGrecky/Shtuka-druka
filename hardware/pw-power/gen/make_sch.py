#!/usr/bin/env python3
"""Write the PW schematic (KiCad 7 format) from design.py with the shared grid writer, and the project file.
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
    module_sch.write_grid(D, "8a41c2d7-5e93-4f0b-b6a8-2c7d9e1f3a54",
                          "PW power: DC / USB-C PD / battery -> ideal diodes -> On/Off -> BUS -> 19 V, +5 V x 2, +-12 V, +48 V",
                          HERE,
                          notes=(D.BUS_NOTE,
                                 "Values after the TI datasheet examples, scaled; every 'check' note is verified before the board",
                                 "Rev 0.1: schematic only (R145: USB-C Power is separate from the isolated USB-C PC port)"))
    B.write_project(os.path.join(HERE, ".."), D.NAME)
