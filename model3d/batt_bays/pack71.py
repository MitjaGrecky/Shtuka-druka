"""P137-b / variant B: two Batteryspace 7548168-1C packs 170 x 51 x 24 in the current case (deck unchanged, 24 mm under the deck).
Free positions of a pack box (24 high on the floor z 3..27) with gap 1 or 2 mm (both orientations), obstacles = g3 production parts except old bays;
ceiling under the deck 27, under the slope top-3. Then pairs, nearest to symmetry. Run: python pack71.py (one g3 build + search, ~2-3 min)."""
import itertools, math, sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
exec(open(os.path.join(HERE, "batt_bays.py"), encoding="utf-8").read().split("pos = []")[0])
out = {}
for gap in (2.0, 1.0):
    GAP = gap
    pos = []
    for w, d in ((170.0, 51.0), (51.0, 170.0)):
        for x in range(5, int(510 - w) + 1, 2):
            for y in range(5, int(495 - d) + 1, 2):
                if Z0 + 24.0 + (GAP if y > 300 else 0.0) > ceil(y): continue
                bx = ([x, y, Z0], [x + w, y + d, Z0 + 24.0])
                if all(math.sqrt(sum(max(bx[0][k] - b[1][k], b[0][k] - bx[1][k], 0.0) ** 2 for k in range(3))) >= GAP for b in obst.values()):
                    pos.append((x, y, w, d))
    sep = lambda a, b: a[0] + a[2] + GAP <= b[0] or b[0] + b[2] + GAP <= a[0] or a[1] + a[3] + GAP <= b[1] or b[1] + b[3] + GAP <= a[1]
    pairs = [(a, b) for a, b in itertools.combinations(pos[::2], 2) if sep(a, b)]
    print(f"gap {gap}: free positions {len(pos)}, pairs {len(pairs)}; examples {pos[:3]}")
    out[str(gap)] = {"positions": len(pos), "pairs": len(pairs), "first": pos[:5], "ymin": min((p[1] for p in pos), default=None)}
json.dump(out, open(os.path.join(HERE, "pack71.json"), "w"), default=str)
