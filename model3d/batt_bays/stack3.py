"""P137-g: two blocks of a LiPo 36125140 x3 stack (block 140 x 150 x 14, z 3..17, rotation 90 deg) in the current case: deck and A1 unchanged.
Step 1 AABB prefilter (gap 0.5, floor z 3..17), step 2 true check (m.check) of the survivors; then pairs of truly clear positions. Log runs/stack3.log."""
import itertools, math, sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
exec(open(os.path.join(HERE, "batt_bays.py"), encoding="utf-8").read().split("pos = []")[0])
GAP = 0.5
HB = 14.0
cands = []
for w, d in ((140.0, 150.0), (150.0, 140.0)):
    for x in range(5, int(510 - w) + 1, 5):
        for y in range(5, int(495 - d) + 1, 5):
            if Z0 + HB > ceil(y): continue
            bx = ([x, y, Z0], [x + w, y + d, Z0 + HB])
            if all(math.sqrt(sum(max(bx[0][k] - b[1][k], b[0][k] - bx[1][k], 0.0) ** 2 for k in range(3))) >= GAP for b in obst.values()):
                cands.append((x, y, w, d))
print("AABB survivors:", len(cands), "x range", (min(c[0] for c in cands), max(c[0] for c in cands)) if cands else None, flush=True)
P0 = [p for p in P if not p.name.startswith("Battery")]
good = []
t0 = time.time()
step = max(1, len(cands) // 120)
for x, y, w, d in cands[::step]:
    b = m.box("Stack", "rear", x, x + w, y, y + d, 3.0, 17.0, color="battery", est=True)
    res = m.check(P0 + [b])
    worst = min([g for g, a, bb, _ in res if "Stack" in (a, bb)] or [9.0])
    if worst >= 0: good.append((x, y, w, d, round(worst, 1)))
print("true-check clear:", len(good), "of", len(cands[::step]), "in", round(time.time() - t0), "s", flush=True)
sep = lambda a, b: a[0] + a[2] <= b[0] or b[0] + b[2] <= a[0] or a[1] + a[3] <= b[1] or b[1] + b[3] <= a[1]
pairs = [(a, b) for a, b in itertools.combinations(good, 2) if sep(a, b)]
print("pairs:", len(pairs), pairs[:3], flush=True)
print("good sample:", good[:6], flush=True)
print("done", flush=True)
