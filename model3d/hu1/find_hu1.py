#!/usr/bin/env python3
"""P130: place of module HU1 (35 x 45 x 14, 4 electrolytics, harness <= 80 mm to PW). Production g3.build(30, 0, 117, 20, 0).
Search: AABB 35x45 (both orientations) x 14 high on the floor (z 3..17), grid 1 mm; free of ALL parts with gap >= GAP, below the slope
(ceiling = outer top - 3 skin - 1), inside walls; harness = Manhattan distance from the module edge to the PW box <= 80 minus 15 (tails);
min distance to analog boards A1/R1 >= AN, to heat (H5, fan, batteries, PW) >= HEAT (PW itself excluded from heat: harness must be short).
Run: python find_hu1.py -> hu1_candidates.json + table. Concept: coordinates are x (left->right), y (front->back), z from the outer floor."""
import itertools, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v8"))
import g3
GAP, AN, HEAT, HARN = 1.0, 40.0, 15.0, 65.0
m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
boxes = {}
for p in P:
    lo = [c - h for c, h in zip(p.c, p.h)]; hi = [c + h for c, h in zip(p.c, p.h)]
    boxes[p.name] = (lo, hi)
skip = ("Floor", "Front wall", "Rear wall", "Top skin", "Slope skin", "Hatch vent", "exhaust", "Front intake", "Foot")
obst = {n: b for n, b in boxes.items() if not n.startswith(skip) and "groove" not in n}
TAN = math.tan(math.atan((117 - 30) / (433.4 - 300)))


def ceiling(y):
    return (30.0 if y <= 300 else 30 + (y - 300) * TAN if y <= 433.4 else 117.0) - 3.0 - 1.0


def dist(a, b):
    d = [max(a[0][k] - b[1][k], b[0][k] - a[1][k], 0.0) for k in range(3)]
    return math.sqrt(sum(x * x for x in d))


def mdist(a, b):               # manhattan in plan
    return sum(max(a[0][k] - b[1][k], b[0][k] - a[1][k], 0.0) for k in range(2))


pw = boxes["PW power"]
analog = [boxes["A1 audio board"], boxes["R1 audio rear board"]]
heat = [boxes[n] for n in boxes if n.startswith(("H5 plugs", "Fan 80", "Battery pack"))]
Z0, H = 3.0, 14.0
res = []
for w, d in ((35.0, 45.0), (45.0, 35.0)):
    for x in range(4, int(512 - w)):
        for y in range(4, int(497 - d)):
            bx = ([x, y, Z0], [x + w, y + d, Z0 + H])
            if Z0 + H > ceiling(y): continue                          # front edge is the lowest ceiling
            if any(dist(bx, b) < GAP for b in obst.values()): continue
            h = mdist(bx, pw)
            if h > HARN: continue
            a = min(dist(bx, b) for b in analog)
            if a < AN: continue
            ht = min(dist(bx, b) for b in heat)
            if ht < HEAT: continue
            res.append(dict(x=x, y=y, w=w, d=d, harness=round(h, 1), analog=round(a, 1), heat=round(ht, 1),
                            gap=round(min(dist(bx, b) for b in obst.values()), 1), ceiling=round(ceiling(y) - Z0 - H, 1)))
print("free positions:", len(res), "| g3 collisions:", len(col))
cand = []
if res:
    cand.append(("A: ближе всего к PW", min(res, key=lambda r: (r["harness"], -r["analog"]))))
    cand.append(("B: дальше всего от аналога", max(res, key=lambda r: (r["analog"], -r["harness"]))))
    cand.append(("C: дальше всего от тепла", max(res, key=lambda r: (min(r["heat"], 60), -r["harness"]))))
for n, r in cand: print(n, r)
json.dump({"params": dict(GAP=GAP, AN=AN, HEAT=HEAT, HARN=HARN), "n": len(res), "candidates": [dict(name=n, **r) for n, r in cand]}, open(os.path.join(HERE, "hu1_candidates.json"), "w"), ensure_ascii=False, indent=1)
