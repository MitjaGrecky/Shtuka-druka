"""P137-g follow-up: what blocks a 140x150x14 block (z 3..17) at typical places; true check (m.check) at a coarse grid under the deck (y < 300)."""
import math, sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
exec(open(os.path.join(HERE, "batt_bays.py"), encoding="utf-8").read().split("pos = []")[0])
P0 = [p for p in P if not p.name.startswith("Battery")]
def blockers(x, y, w, d):
    bx = ([x, y, 3.0], [x + w, y + d, 17.0])
    L = []
    for n, b in obst.items():
        g = math.sqrt(sum(max(bx[0][k] - b[1][k], b[0][k] - bx[1][k], 0.0) ** 2 for k in range(3)))
        if g < 0.5: L.append(n)
    return L
for c in ((113, 10, 140, 150), (113, 60, 140, 150), (340, 10, 140, 150), (20, 100, 140, 150)):
    print("AABB blockers", c, blockers(*c)[:6], flush=True)
good, worst_list = [], []
t0 = time.time()
for w, d in ((140.0, 150.0), (150.0, 140.0)):
    for x in range(5, int(510 - w) + 1, 15):
        for y in range(5, int(300 - d) + 1, 15):
            b = m.box("Stack", "rear", x, x + w, y, y + d, 3.0, 17.0, color="battery", est=True)
            res = m.check(P0 + [b])
            r = sorted([(round(g, 1), (a if bb == "Stack" else bb)) for g, a, bb, _ in res if "Stack" in (a, bb) and g < 0.5])
            if not r: good.append((x, y, w, d))
            else: worst_list.append((r[0][0], x, y, int(w), r[0][1]))
print("true check under the deck:", len(good), "clear;", round(time.time() - t0), "s; first:", good[:5], flush=True)
print("least bad:", sorted(worst_list, reverse=True)[:5], flush=True)
print("done", flush=True)
