#!/usr/bin/env python3
"""Write the P2 schematic (KiCad 7 format) from design.py with the shared grid writer, and the project file.
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
    module_sch.write_grid(D, "5a1c7e02-93bd-4f68-8d14-b7e3a96c0f25",
                          "P2 grid deck: RP2350, 64 FSR pads, 109 RGB, scene buttons, buses",
                          HERE,
                          notes=(D.BUS_NOTE,
                                 "64 pads = 8 x 74HC4051 + ADC128S102 (V17); LP5864 x5 on a TCA9546A (0x73)",
                                 "Rev 0.1: schematic only; electrodes are placeholders until the board is drawn"))
    B.write_project(os.path.join(HERE, ".."), D.NAME)
