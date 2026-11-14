#!/usr/bin/env python3
"""Write the A1 schematic (KiCad 7 format) from design.py with the shared grid writer, and the project file.
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
    module_sch.write_grid(D, "b2d84f17-3a6c-49e5-8c01-7f5e9a2d6b48",
                          "A1 digital audio: 3 ADC + DAC + 2 xcore.ai + USB isolator, clocks, quiet supplies",
                          HERE,
                          notes=(D.BUS_NOTE,
                                 "ADC buffers x 1/4 (8 Vrms FS from R1, Cirrus circuit), DAC I-V stages (AN0679), TDM master xcore A, isolated USB port B on xcore B",
                                 "Rev 0.1: schematic only; plan and pinouts in hardware/a1-digital/PLAN.md; check notes in design.py"))
    B.write_project(os.path.join(HERE, ".."), D.NAME)
