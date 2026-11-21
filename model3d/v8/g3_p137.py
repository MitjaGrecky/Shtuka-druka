#!/usr/bin/env python3
"""P137: deck +12 (42), two pack bays 115 x 110 x 34 front left (x 5-115, y 5-120) and front right (x 399-509, y 5-120), thin 11 mm bays removed.
Parameter DECK_UP; everything else is the production g3.build. R195 front line is clipped to the free stretch between the bays (x 120-394).
Run: python g3_p137.py -> prints the check; writes ../batt_bays/p137_parts.json (boxes for the snapshot)."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import g3
import os as _os
DECK_UP = float(_os.environ.get("DECK_UP", "12"))
BAYS = _os.environ.get("BAYS", "5,115,5,115,3;399,509,5,115,3")          # x0,x1,y0,y1, shelf underside z0 (shelf 2 mm; pack box = bay envelope)
LIPO = float(_os.environ.get("LIPO", "32"))          # pack box height: bay z 3..37 = shelf 2 + 32 (env LIPO)
def build(line=(120.0, 394.0)):
    m, P, col, tight = g3.build(30 + DECK_UP, 0, 117.0, 20, float(_os.environ.get("SHIFT", "0")), packs=BAYS, lipo=LIPO)
    out = []
    for p in P:
        if p.name.startswith("Front intake line"):
            continue                              # replaced below
        out.append(p)
    out.append(m.box("Front intake line 2 mm (clipped to the free stretch)", "vents", line[0], line[1], 0.0, 3.0, 3.0, 5.0, color="grey", est=True, check=False))
    res = m.check(out)
    col = sorted([(round(abs(g), 1), a, b) for g, a, b, _ in res if g < -0.05], reverse=True)
    tight = sorted([(round(g, 1), a, b) for g, a, b, _ in res if -0.05 <= g < 2.0 and "harness room" not in a + b])
    return m, out, col, tight
if __name__ == "__main__":
    m, P, col, tight = build()
    print("deck", 30 + DECK_UP, "| collisions:", len(col), col[:5], "| tight < 2 mm:", len(tight), tight[:6])
    boxes = {p.name: p for p in P}
    for n in ("Battery pack 1", "Battery pack 2", "Battery shelf 1", "Front intake line 2 mm (clipped to the free stretch)"):
        p = boxes.get(n)
        if p: print(n, [round(c - h, 1) for c, h in zip(p.c, p.h)], [round(c + h, 1) for c, h in zip(p.c, p.h)])
    skip = ("Hatch vent", "groove")
    data = [{"n": p.name, "g": getattr(p, "group", ""), "a": [round(c - h, 2) for c, h in zip(p.c, p.h)], "b": [round(c + h, 2) for c, h in zip(p.c, p.h)]} for p in P if not p.name.startswith(skip) and "groove" not in p.name]
    json.dump(data, open(os.path.join(HERE, "..", "batt_bays", "p137_parts.json"), "w"))
    print("boxes", len(data))
