#!/usr/bin/env python3
"""Write the P1 schematic (KiCad 7 format) from design.py with the shared grid writer.
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
    module_sch.write_grid(D, "2c7e5a91-8d4f-4b36-9e12-6a0b3f8d5c08",
                          "LP5864 A 0x40 (U1, buttons 1-12), B 0x41 (U2, buttons 13-19) on mux channel 0; LED j: cell j div 24, CS triple (j mod 24) div 4, SW j mod 4", HERE,
                          notes=(D.BUS_NOTE, "Chain: U3 (Rec first) -> U4 -> U5 -> M3 (J2) -> W1 (J3) -> M5; buttons: see the Note field of SW1-SW19"))
