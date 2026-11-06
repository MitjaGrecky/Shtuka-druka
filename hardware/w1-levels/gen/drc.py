#!/usr/bin/env python3
"""Local DRC with pcbnew (KiCad 7): prints the violation and unconnected counts and the first lines.
Run: python3 drc.py [report.rpt]      License: AGPL-3.0-or-later.
"""
import os
import re
import sys

import pcbnew

import design as D

HERE = os.path.dirname(os.path.abspath(__file__))
pcb = os.path.join(HERE, "..", D.NAME + ".kicad_pcb")
rpt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "drc.rpt")
b = pcbnew.LoadBoard(pcb)
pcbnew.WriteDRCReport(b, rpt, pcbnew.EDA_UNITS_MILLIMETRES, True)
t = open(rpt).read()
for key in ("DRC violations", "unconnected pads", "Footprint errors"):
    m = re.search(r"\*\* Found (\d+) " + key, t)
    print(key, m.group(1) if m else "?")
kinds = re.findall(r"^\[(\w+)\]", t, re.M)
print({k: kinds.count(k) for k in sorted(set(kinds))})
