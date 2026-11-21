"""R208: ribs between the three battery bays and the long board BB1 along the rear ends of the blocks (blocks3.csv: blocks x 5-135 / 180-310 / 380-510, y 155-300, z 3-12.5; BM x136-174 and 312-350, y 262-300).
Ribs 2 mm: x 136-138, 178-180, 312-314, 378-380; y 155-260; z 3-15.5 (P parts bottom 15.9). BB1: strip x X0..X1, y Y0..Y0+28, envelope z 3..14 (board on 3 mm standoffs + connectors).
Real check (m.check) of ribs + BB1 candidates; writes bb1_outline.csv (outline, connectors) and p137_parts.json for the snapshot. Log runs/bb1.log."""
import csv, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "v8"))
import g3
m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
print("base collisions:", len(col), flush=True)
ribs = [(136, 138), (178, 180), (312, 314), (378, 380)]
RB = [m.box(f"Rib {i + 1}", "shell", a, b, 155.0, 260.0, 3.0, 15.5, color="metal", est=True) for i, (a, b) in enumerate(ribs)]
r = m.check(P + RB)
print("ribs vs model:", sorted([(round(g, 1), a, b) for g, a, b, _ in r if g < 0.0 and "Rib" in a + b])[:5] or "clear", flush=True)
found = None
for X0, X1 in ((15, 500), (15, 470), (15, 440)):
    for Y0 in (302, 304, 306, 309, 312):
        bb = m.box("BB1 (long board)", "pcb", X0, X1, Y0, Y0 + 28.0, 3.0, 14.0, color="pcb", est=True)
        bad = sorted([(round(g, 1), a, b) for g, a, b, _ in m.check(P + RB + [bb]) if g < 0.0 and "BB1" in a + b])
        print(f"BB1 x {X0}-{X1} y {Y0}-{Y0 + 28}:", bad[:3] or "CLEAR", flush=True)
        if not bad and not found: found = (X0, X1, Y0)
    if found: break
if found:
    X0, X1, Y0 = found
    bb = m.box("BB1 (long board)", "pcb", X0, X1, Y0, Y0 + 28.0, 3.0, 14.0, color="pcb", est=True)
    near = sorted([(round(g, 2), a, b) for g, a, b, _ in m.check(P + RB + [bb]) if 0.0 <= g < 1.0 and "BB1" in a + b])
    print("BB1 chosen", found, "| near < 1 mm:", near[:4], flush=True)
    rows = [("outline", X0, Y0, X1, Y0 + 28.0, 3.0, 14.0)]
    for i, cx in enumerate((57.5, 82.5, 232.5, 257.5, 432.5, 457.5)):
        rows.append((f"cell connector {i + 1} (block {i // 2 + 1}, pack {'AB'[i % 2]})", cx - 4, Y0 + 3, cx + 4, Y0 + 11, 3.0, 12.0))
    rows += [("BM1 link", 312, Y0 + 14, 350, Y0 + 24, 3.0, 12.0), ("BM2 link", 136, Y0 + 14, 174, Y0 + 24, 3.0, 12.0), ("PW Micro-Fit 2x3 #1", 262, Y0 + 14, 282, Y0 + 26, 3.0, 13.5), ("PW Micro-Fit 2x3 #2", 292, Y0 + 14, 312, Y0 + 26, 3.0, 13.5)]
    with open(os.path.join(HERE, "bb1_outline.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["name", "x0", "y0", "x1", "y1", "z0", "z1"]); w.writerows(rows)
    P2 = P + RB + [bb]
else: P2 = P + RB
json.dump([{"n": p.name, "g": getattr(p, "group", ""), "a": [round(c - h, 2) for c, h in zip(p.c, p.h)], "b": [round(c + h, 2) for c, h in zip(p.c, p.h)]} for p in P2 if not p.name.startswith("Hatch vent") and "groove" not in p.name], open(os.path.join(HERE, "p137_parts.json"), "w"))
print("done", flush=True)
