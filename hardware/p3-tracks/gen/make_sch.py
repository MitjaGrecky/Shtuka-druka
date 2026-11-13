#!/usr/bin/env python3
"""Write the P3 schematic (KiCad 7 format) from design.py with the shared grid writer.
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
    module_sch.write_grid(D, "8a4c2e57-3b1f-4d96-a7e0-1c5f9d3b6e10",
                          "LP5864 A 0x40 (U1, buttons 1-12), B 0x41 (U2, 13-21) on mux channel 0 (0x71); LED j: cell j div 24, CS triple (j mod 24) div 4, SW j mod 4", HERE,
                          notes=(D.BUS_NOTE, "Chain: U3 (Solo first) -> U4 -> U5 -> M2 (J2) -> M4 (J3); W2 (J4) not in the chain; buttons: Note field of SW1-SW21"))
