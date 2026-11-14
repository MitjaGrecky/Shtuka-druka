#!/usr/bin/env python3
"""Write the F1 schematic (KiCad 7 format) from design.py with the shared grid writer, and the project file.
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
    module_sch.write_grid(D, "e7b3a914-6d28-4c05-a1f7-9c2d4e8b5a36",
                          "F1 headphones: 2 x OPA1622 difference amps x2, mute relays, NMJ6HCD2",
                          HERE,
                          notes=(D.BUS_NOTE,
                                 "Gain 2: 2 Vrms diff from A1 -> 4 Vrms (R67); volume = DAC attenuator (R87); EN follows MUTE",
                                 "Rev 0.1: schematic only; right-angle Neutrik NMJ6HCD2 on a horizontal board (P94)"))
    B.write_project(os.path.join(HERE, ".."), D.NAME)
