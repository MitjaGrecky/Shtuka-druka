#!/usr/bin/env python3
"""Write the R2 schematic (KiCad 7 format) from design.py with the shared grid writer (parts sheet, every pin labelled;
multi-unit symbols placed unit by unit). Also writes the project file.
Run: python3 make_sch.py   (KiCad 10 PC: see hardware/m3-tempo-swing/README.md)   License: AGPL-3.0-or-later.
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
    module_sch.write_grid(D, "6f2d8c41-9a3e-4b57-8e10-3c5b7a9d2e64",
                          "RP2350A + USB2514B hub; MIDI per CA-033 (3.3 V); CV +-10 V = 8.06 (DAC - 1.25 V); CV in -10..+10 V -> 0..3.03 V",
                          HERE,
                          notes=(D.BUS_NOTE,
                                 "Power from PW: +5 V, +-12 V; MIDI DIN, USB, LAN and DC are panel parts on nuts (R141); DIN by cable to J PH headers",
                                 "Control to A1/R1: PH48_1, PH48_2, PHONO, MUTE (relays, R137), R2_OK - all pulled low while the RP2350 boots",
                                 "Rev 0.4: jack positions = 3D model of panel v7 (R142, tools/rear_panel.py v3); placed, not routed"))
    B.write_project(os.path.join(HERE, ".."), D.NAME)
