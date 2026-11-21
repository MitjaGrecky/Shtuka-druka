"""R207: which parts block the 115x110x34 bay? Count free positions when one obstacle (group) is removed; and the 3-pack variant 175x55x26 bays."""
import math, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
src = open(os.path.join(HERE, "batt_bays.py"), encoding="utf-8").read().split("pos = []")[0]
exec(src)
def count(excl, w0, d0, h, step=4):
    ob = {n: b for n, b in obst.items() if not any(n.startswith(e) for e in excl)}
    c = 0; ex = None
    for w, d in ((w0, d0), (d0, w0)):
        for x in range(5, int(510 - w) + 1, step):
            for y in range(5, int(495 - d) + 1, step):
                if Z0 + h + GAP > ceil(y): continue
                bx = ([x, y, Z0], [x + w, y + d, Z0 + h])
                if all(math.sqrt(sum(max(bx[0][k] - b[1][k], b[0][k] - bx[1][k], 0.0) ** 2 for k in range(3))) >= GAP for b in ob.values()):
                    c += 1; ex = ex or (x, y, w, d)
    return c, ex
for label, ex in (("none", ()), ("PW", ("PW power", "Standoff PW")), ("A1", ("A1 audio", "Standoff A1")), ("H5", ("H5 ", "Mini-ITX")), ("R1/R2 rear boards", ("R1 audio", "R2 control")),
                  ("rear jacks", ("Rear jacks",)), ("PW+A1", ("PW power", "Standoff PW", "A1 audio", "Standoff A1")), ("PW+A1+H5", ("PW power", "Standoff PW", "A1 audio", "Standoff A1", "H5 ", "Mini-ITX"))):
    print(f"{label:20s} 115x110x34: {count(ex, 115.0, 110.0, 34.0)}")
print("3-pack bay 175x55x26 (none removed):", count((), 175.0, 55.0, 26.0))
print("3-pack bay, PW+A1 removed:", count(("PW power", "Standoff PW", "A1 audio", "Standoff A1"), 175.0, 55.0, 26.0))
