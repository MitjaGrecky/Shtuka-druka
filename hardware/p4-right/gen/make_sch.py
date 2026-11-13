#!/usr/bin/env python3
"""Write the P4 schematic (KiCad 7 format) from design.py with the shared grid writer.
Run: python3 make_sch.py   (KiCad 10 PC: see hardware/m3-tempo-swing/README.md)   License: AGPL-3.0-or-later.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import design as D  # noqa: E402
import module_sch  # noqa: E402

if __name__ == "__main__":
    module_sch.write_grid(D, "6f3b8c24-1e9a-4d75-b8c0-7a2d5e9f1b09",
                          "LP5864 A 0x40 (U1, buttons 1-12), B 0x41 (U2, 13-20), ADS1115 0x48, AS5600 0x36 on mux channel 0 (0x72)", HERE,
                          notes=(D.BUS_NOTE, "Chain: U3 (Scene A first) -> U4 -> U5 (bit 21 wheel push) -> W3 (J3); buttons: see the Note field of SW1-SW20"))
