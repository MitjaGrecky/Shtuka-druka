#!/usr/bin/env python3
"""Build the P4 board (placed, mounts, nets, no routing) with the shared board writer.
Run: python3 make_pcb.py      License: AGPL-3.0-or-later.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import design as D  # noqa: E402
import module_pcb  # noqa: E402

if __name__ == "__main__":
    module_pcb.main(D, [(f"P4 Right rev {D.REV}", (D.W / 2 + 12.0, 160.0)), ("Shtuka Druka CERN-OHL-S-2.0", (D.W / 2 + 12.0, 161.6))], HERE)
