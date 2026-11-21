"""R207 variant: deck raised by +12 mm (deck top 42): bays under the deck; obstacles as in g3 (panel boards are NOT moved, so overlaps are real conflicts)."""
import math, sys, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
exec(open(os.path.join(HERE, "batt_bays.py"), encoding="utf-8").read().split("pos = []")[0])
hung = {n for n,b in obst.items() if b[0][2] >= 12.0}
low = {n:b for n,b in obst.items() if n not in hung}
print("deck-hung (moves with deck):", len(hung), "| staying low:", sorted(low)[:12])
ceil2 = lambda y: 39.0 if y <= 300 else ceil(y)
pos = []
for w, d in ((115.0, 110.0), (110.0, 115.0)):
    for x in range(5, int(510 - w) + 1, 2):
        for y in range(5, int(300 - d + 10) + 1, 2):
            if Z0 + HB + GAP > ceil2(y + 0): continue
            bx = ([x, y, Z0], [x + w, y + d, Z0 + HB])
            worst = min((math.sqrt(sum(max(bx[0][k] - b[1][k], b[0][k] - bx[1][k], 0.0) ** 2 for k in range(3))), n) for n, b in low.items())
            if worst[0] >= GAP: pos.append((x, y, w, d))
sep = lambda a, b: a[0] + a[2] + GAP <= b[0] or b[0] + b[2] + GAP <= a[0] or a[1] + a[3] + GAP <= b[1] or b[1] + b[3] + GAP <= a[1]
pairs = [(a, b) for a, b in itertools.combinations(pos[::2], 2) if sep(a, b)]
print("deck +12: free bays", len(pos), "pairs", len(pairs))
if pairs:
    best = max(pairs, key=lambda p: (min(p[0][0], p[1][0]), -abs(p[0][1] - p[1][1])))
    print("example pair:", best)
    xs = [x for x in (p[0] for p in pos)]; print("x range of free bays:", min(xs), max(xs))
