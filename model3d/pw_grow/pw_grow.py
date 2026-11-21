#!/usr/bin/env python3
"""P131: how far PW (100.1 x 110.1 mm board) can grow in the production g3.build(30, 0, 117, 20, 0). No electrics.
PW envelope: board plan x 245..345.1, y 342.3..452.4 (the model PW box is 100 x 80, y 360-440; the real board 100.1 x 110.1 does not fit at y 360 because R2 control rear board stands at y 453.4, z 10-109) (model box PW power is x 245-345, y 360-440: shorter than the real board, see tasks/09),
z 3..28 (floor to tallest top part; bottom electrolytics 10.5 mean board bottom >= 14.5). Gap >= 1 to all parts (not walls/skins/vents/feet),
ceiling under the slope = outer top - 3 skin - 1. Run: python pw_grow.py -> pw_grow.json + table (one g3 build, ~1 min)."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v8"))
import g3
m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
skip = ("Floor", "Front wall", "Rear wall", "Top skin", "Slope skin", "Hatch vent", "groove", "Front intake", "Foot", "PW power", "Standoff PW")
obst = {}
for p in P:
    if p.name.startswith(skip) or "groove" in p.name: continue
    obst[p.name] = ([c - h for c, h in zip(p.c, p.h)], [c + h for c, h in zip(p.c, p.h)])
TAN = math.tan(math.atan((117 - 30) / (433.4 - 300)))
ceil = lambda y: (30.0 if y <= 300 else 30 + (y - 300) * TAN if y <= 433.4 else 117.0) - 4.0
GAP, ZT = 1.0, 28.0
BASE = (245.0, 342.3, 345.1, 452.4)   # 100.1 x 110.1 pushed back to R2 (y 453.4) with 1 mm gap


def ok(x0, y0, x1, y1):
    if x0 < 4 or x1 > 511 or y0 < 4 or y1 > 496 or ZT > ceil(y0): return None
    bx = ([x0, y0, 3.0], [x1, y1, ZT])
    worst, who = 99.0, ""
    for n, b in obst.items():
        d = [max(bx[0][k] - b[1][k], b[0][k] - bx[1][k], 0.0) for k in range(3)]
        g = math.sqrt(sum(v * v for v in d))
        if g < worst: worst, who = g, n
    return (worst, who) if worst >= GAP else None


def grow(dx0, dx1, dy0, dy1):
    return ok(BASE[0] - dx0, BASE[1] - dy0, BASE[2] + dx1, BASE[3] + dy1)


res = {"base": grow(0, 0, 0, 0)}
print("base 100.1 x 110.1:", res["base"])
lim = {}
for name, kw in (("-X", 0), ("+X", 1), ("-Y", 2), ("+Y", 3)):
    best = 0
    for d in range(1, 120):
        a = [0, 0, 0, 0]; a[kw] = d
        if grow(*a): best = d
        else: break
    a = [0, 0, 0, 0]; a[kw] = best + 1
    r = ok(BASE[0] - a[0], BASE[1] - a[2], BASE[2] + a[1], BASE[3] + a[3])
    lim[name] = best
    # who blocks
    bx = ([BASE[0] - a[0], BASE[1] - a[2], 3.0], [BASE[2] + a[1], BASE[3] + a[3], ZT])
    who = min(obst, key=lambda n: math.sqrt(sum(max(bx[0][k] - obst[n][1][k], obst[n][0][k] - bx[1][k], 0.0) ** 2 for k in range(3))))
    print(name, "max", best, "mm; blocked by", who)
    res[name] = {"max": best, "blocker": who}
combos = {"+15 по X": (0, 15, 0, 0), "+30 по X": (0, 30, 0, 0), "+30 по Y (вперёд)": (0, 0, 30, 0), "+15 X / +30 Y(вперёд)": (0, 15, 30, 0), "+20 X / +20 Y(вперёд)": (0, 20, 20, 0)}
for n, a in combos.items():
    r = grow(*a); res[n] = r
    print(n, "->", (round(r[0], 1), r[1]) if r else "COLLISION")
json.dump(res, open(os.path.join(HERE, "pw_grow.json"), "w"), ensure_ascii=False, indent=1, default=str)
if __name__ == "__main__" and "--near" in sys.argv:
    bx = ([BASE[0], BASE[1], 3.0], [BASE[2], BASE[3], ZT])
    L = []
    for n, b in obst.items():
        g = math.sqrt(sum(max(bx[0][k] - b[1][k], b[0][k] - bx[1][k], 0.0) ** 2 for k in range(3)))
        L.append((round(g, 1), n, [round(v, 1) for v in b[0]], [round(v, 1) for v in b[1]]))
    for r in sorted(L)[:8]: print(r)
