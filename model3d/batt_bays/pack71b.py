"""Variant B follow-up: which parts prevent a second 170x51x24 pack (gap 1)? Pairs with one obstacle group removed; extents of free positions."""
import itertools, math, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
exec(open(os.path.join(HERE, "batt_bays.py"), encoding="utf-8").read().split("pos = []")[0])
GAP = 1.0
def run(excl):
    ob = {n: b for n, b in obst.items() if not any(n.startswith(e) for e in excl)}
    pos = []
    for w, d in ((170.0, 51.0), (51.0, 170.0)):
        for x in range(5, int(510 - w) + 1, 3):
            for y in range(5, int(495 - d) + 1, 3):
                if Z0 + 24.0 + (GAP if y > 300 else 0.0) > ceil(y): continue
                bx = ([x, y, Z0], [x + w, y + d, Z0 + 24.0])
                if all(math.sqrt(sum(max(bx[0][k] - b[1][k], b[0][k] - bx[1][k], 0.0) ** 2 for k in range(3))) >= GAP for b in ob.values()):
                    pos.append((x, y, w, d))
    sep = lambda a, b: a[0] + a[2] + GAP <= b[0] or b[0] + b[2] + GAP <= a[0] or a[1] + a[3] + GAP <= b[1] or b[1] + b[3] + GAP <= a[1]
    pairs = sum(1 for a, b in itertools.combinations(pos[::2], 2) if sep(a, b))
    ex = (min(p[0] for p in pos), max(p[0] for p in pos), min(p[1] for p in pos), max(p[1] for p in pos)) if pos else None
    return len(pos), pairs, ex
for label, ex in (("as is", ()), ("A1", ("A1 audio", "Standoff A1")), ("PW", ("PW power", "Standoff PW")), ("H5", ("H5 ", "Mini-ITX")), ("A1+PW", ("A1 audio", "Standoff A1", "PW power", "Standoff PW"))):
    print(f"{label:8s}", run(ex))
