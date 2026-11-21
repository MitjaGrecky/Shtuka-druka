"""P138: real check (m.check) of two LiPo-stack blocks 150 x 140 x 12.5 (z 3..15.5) under P3/P4: x 345-495, y 6-146 and y 148-288, deck and A1 unchanged,
old thin bays (g3 default packs) removed. Also R195 (front line x 110-490 stays full: the blocks start at y 6) and CoG of the two blocks.
Run: python p138.py -> runs/p138.log, p137_parts.json for the snapshot."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "v8"))
import g3_p137 as G
G.DECK_UP = 0.0
G.BAYS = "345,495,6,146,3;345,495,148,288,3"
G.LIPO = 12.5 - 2.0                                  # shelf 2 + 10.5 -> top z 15.5
m, P, col, tight = G.g3.build(30, 0, 117.0, 20, 0, packs=G.BAYS, lipo=G.LIPO)
res = m.check(P)
cl = sorted([(round(abs(g), 1), a, b) for g, a, b, _ in res if g < -0.05], reverse=True)
tg = sorted([(round(g, 2), a, b) for g, a, b, _ in res if -0.05 <= g < 1.0 and ("Battery" in a + b)])
print("model collisions:", len(cl), cl[:5])
print("blocks vs parts, gap < 1:", tg[:8])
B = {p.name: p for p in P}
for n in ("Battery pack 1", "Battery pack 2"):
    p = B[n]; print(n, [round(c - h, 1) for c, h in zip(p.c, p.h)], [round(c + h, 1) for c, h in zip(p.c, p.h)])
cx = (420 + 420) / 2; cy = (76 + 218) / 2
print("CoG of the two blocks (x, y):", cx, cy, "| case centre 257.5, 250 -> shift right", cx - 257.5, "mm, front", 250 - cy, "mm")
json.dump([{"n": p.name, "g": getattr(p, "group", ""), "a": [round(c - h, 2) for c, h in zip(p.c, p.h)], "b": [round(c + h, 2) for c, h in zip(p.c, p.h)]} for p in P if not p.name.startswith(("Hatch vent",)) and "groove" not in p.name], open(os.path.join(HERE, "p137_parts.json"), "w"))
print("done", flush=True)
