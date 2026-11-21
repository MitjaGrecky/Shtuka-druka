#!/usr/bin/env python3
"""R207: do two Batteryspace packs (bay 115 x 110 x 34, rotation 90 deg allowed) fit in the production g3.build(30, 0, 117, 20, 0)?
Obstacles: every part except floor/walls/skins/vents/grooves/feet and the old thin battery bays (they are replaced); gap >= 2 to parts and to the
walls (inner x 3..512, y 3..497), floor z 3, ceiling under deck 27 / under the slope outer top - 3 (checked at the front edge); step 2 mm.
Run: python batt_bays.py -> batt_bays.json + table (one g3 build + search, ~2 min)."""
import itertools, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v8"))
import g3
m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
skip = ("Floor", "Front wall", "Rear wall", "Top skin", "Slope skin", "Hatch vent", "groove", "Front intake", "Foot", "Battery")
obst = {p.name: ([c - h for c, h in zip(p.c, p.h)], [c + h for c, h in zip(p.c, p.h)]) for p in P if not p.name.startswith(skip) and "groove" not in p.name}
TAN = math.tan(math.atan((117 - 30) / (433.4 - 300)))
ceil = lambda y: (30.0 if y <= 300 else 30 + (y - 300) * TAN if y <= 433.4 else 117.0) - 3.0
GAP, Z0, HB = 2.0, 3.0, 34.0
print("interior height under the deck:", 27.0 - 3.0, "mm; pack bay needs", HB, "+", GAP)
ymin_h = 300 + ((Z0 + HB + GAP) - 30 + 3.0) / TAN
print("front edge of a 34 mm bay must be at y >=", round(ymin_h, 1), "(slope ceiling)")
pos = []
for w, d in ((115.0, 110.0), (110.0, 115.0)):
    for x in range(5, int(510 - w) + 1, 2):
        for y in range(5, int(495 - d) + 1, 2):
            if Z0 + HB + GAP > ceil(y): continue
            bx = ([x, y, Z0], [x + w, y + d, Z0 + HB])
            if all(math.sqrt(sum(max(bx[0][k] - b[1][k], b[0][k] - bx[1][k], 0.0) ** 2 for k in range(3))) >= GAP for b in obst.values()):
                pos.append((x, y, w, d))
print("single free bay positions:", len(pos))
pairs = []
def sep(a, b):
    return a[0] + a[2] + GAP <= b[0] or b[0] + b[2] + GAP <= a[0] or a[1] + a[3] + GAP <= b[1] or b[1] + b[3] + GAP <= a[1]
if pos:
    for a, b in itertools.combinations(pos[::3], 2):
        if sep(a, b): pairs.append((a, b))
print("pairs (every 3rd position sampled):", len(pairs))
out = {"singles": len(pos), "pairs": len(pairs), "examples": []}
if pairs:
    best = min(pairs, key=lambda p: abs((p[0][0] + p[0][2] / 2 + p[1][0] + p[1][2] / 2) / 2 - 257.5))
    out["examples"].append(best); print("pair nearest to the centre line x 257.5:", best)
else:
    # what blocks: largest free single and the gap shortage for the best single
    best = None
    near = []
    for w, d in ((115.0, 110.0), (110.0, 115.0)):
        for x in range(5, int(510 - w) + 1, 4):
            for y in range(5, int(495 - d) + 1, 4):
                if Z0 + HB + GAP > ceil(y): continue
                bx = ([x, y, Z0], [x + w, y + d, Z0 + HB])
                worst = min((math.sqrt(sum(max(bx[0][k] - b[1][k], b[0][k] - bx[1][k], 0.0) ** 2 for k in range(3))), n) for n, b in obst.items())
                near.append((round(worst[0], 1), worst[1], x, y, w, d))
    near.sort(reverse=True); out["closest"] = near[:3]; print("closest misses (min gap, blocker, x, y, w, d):", near[:3])
json.dump(out, open(os.path.join(HERE, "batt_bays.json"), "w"), ensure_ascii=False, indent=1, default=str)
