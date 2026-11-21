"""P138-b: block A (x 112-252, y 6-156, z 3-17 under P2) + block B (x 345-495, y 148-288, z 3-15.5 under P3/P4) in the production g3 (g3.py PACKS + vents_and_feet).
Real check + CoG of equal masses; writes p137_parts.json for the snapshot. Log runs/p138b.log."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "v8"))
import g3
m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
cl = sorted([(round(abs(x), 1), a, b) for x, a, b, _ in m.check(P) if x < -0.05], reverse=True)
print("model collisions:", len(cl), cl[:5])
res = m.check(P)
print("gap < 1 mm to a block:", sorted([(round(x, 2), a, b) for x, a, b, _ in res if -0.05 <= x < 1.0 and ("Battery" in a + b)])[:6])
for p in P:
    if p.name.startswith("Battery") and "shelf" not in p.name: print(p.name, [round(c - h, 1) for c, h in zip(p.c, p.h)], [round(c + h, 1) for c, h in zip(p.c, p.h)])
cx, cy = (182 + 420) / 2, (81 + 218) / 2
print("CoG of the two blocks:", cx, cy, "| from centre (257.5, 250): x", cx - 257.5, "y", cy - 250)
json.dump([{"n": p.name, "g": getattr(p, "group", ""), "a": [round(c - h, 2) for c, h in zip(p.c, p.h)], "b": [round(c + h, 2) for c, h in zip(p.c, p.h)]} for p in P if not p.name.startswith("Hatch vent") and "groove" not in p.name], open(os.path.join(HERE, "p137_parts.json"), "w"))
print("done", flush=True)
