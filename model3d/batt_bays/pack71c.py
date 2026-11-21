"""Variant B: true check (m.check handles tilted parts) of pack boxes 170x51x24 (z 3..27) on the strip found by AABB search; also 51x170 orientation."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "v8"))
import g3
m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
P0 = [p for p in P if not p.name.startswith("Battery")]
import time
best = []
t0 = time.time()
cands = [(x, y, w, d) for w, d in ((170.0, 51.0), (51.0, 170.0)) for x in range(5, int(510 - w) + 1, 30) for y in range(5, int(495 - d) + 1, 30)]
print('candidates', len(cands), flush=True)
for x, y, w, d in cands:
    b = m.box("Pack 71Wh", "rear", x, x + w, y, y + d, 3.0, 27.0, color="battery", est=True)
    res = m.check(P0 + [b])
    worst = min([g for g, a, bb, _ in res if "Pack 71Wh" in (a, bb)] or [9.0])
    who = [(a if bb == "Pack 71Wh" else bb) for g, a, bb, _ in res if "Pack 71Wh" in (a, bb) and g == worst][:1]
    best.append((round(worst, 1), x, y, who))
print("clear (gap >= 0):", [r for r in best if r[0] >= 0], flush=True)
print("best misses:", sorted(best, reverse=True)[:5], flush=True)
