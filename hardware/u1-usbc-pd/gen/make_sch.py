#!/usr/bin/env python3
"""Write the U1 schematic (KiCad 7 format) from design.py with the shared grid writer, and the project file.
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
    module_sch.write_grid(D, "c4d92a6f-58b3-4e01-8f7c-2b6d8e3a9f15",
                          "U1 USB-C PD input board: GCT USB4105-GF-A",
                          HERE,
                          notes=(D.BUS_NOTE,
                                 "GCT USB4105-GF-A: 5 A USB-C receptacle, VBUS x 2, GND x 2, CC1, CC2 to PW J2 (TPS25730 stays on PW)",
                                 "Rev 0.1: schematic and placed board"))
    # the GCT USB4105 footprint (KiCad library, from the GCT drawing) has its NPTH pegs 0.2 mm from the GND pads: hole clearance 0.15 mm for this board
    B.write_project(os.path.join(HERE, ".."), D.NAME, 2, D.HOLE_CLEARANCE)
