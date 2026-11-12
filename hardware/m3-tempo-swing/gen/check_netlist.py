#!/usr/bin/env python3
"""Schematic netlist == design.py, pin by pin (shared checker in hardware/common/gen).
Run: python3 check_netlist.py      License: AGPL-3.0-or-later.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import check_netlist as C  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(1 if C.check(HERE) else 0)
