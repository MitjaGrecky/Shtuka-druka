"""P140 phase 3 (fixed triple from blocks3.py): blocks (rotated 130 x 145) x 5-135 / 180-310 / 380-510, y 155-300, z 3-12.5; 2 BM 38 x 38 x 10.5 in the gaps next to y 300 (closest to PW), NTC per block pair.
Real check of everything together, CoG, harness Manhattan to PW edge. Writes blocks3.csv (6 cells + 2 BM + 3 NTC) and p137_parts.json for the snapshot."""
import csv, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "v8"))
import g3
m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
P0 = [p for p in P if not p.name.startswith("Battery")]
BL = [(5, 155, 130, 145), (180, 155, 130, 145), (380, 155, 130, 145)]
BM = [(312, 262), (136, 262)]
BM2_OPTIONS = [(136, 262), (140, 262), (136, 258), (132, 262), (140, 256), (136, 252), (132, 252)]
add, rows = [], []
def trial(bm2):
    L = [m.box(f"Block {i}", "rear", x, x + w, y, y + d, 3.0, 12.5, color="battery", est=True) for i, (x, y, w, d) in enumerate(BL)]
    L.append(m.box("BM 1 board (38 x 38)", "rear", BM[0][0], BM[0][0] + 38, BM[0][1], BM[0][1] + 38, 3.0, 13.5, color="pcb", est=True))
    L.append(m.box("BM 2 board (38 x 38)", "rear", bm2[0], bm2[0] + 38, bm2[1], bm2[1] + 38, 3.0, 13.5, color="pcb", est=True))
    return not [1 for g, a, b, _ in m.check(P0 + L) if g < 0.0 and any(t in a + b for t in ("Block", "BM "))]
for opt in BM2_OPTIONS:
    ok = trial(opt); print("BM 2 at", opt, "clear" if ok else "collides", flush=True)
    if ok: BM[1] = opt; break
for i, (x, y, w, d) in enumerate(BL):
    add.append(m.box(f"Block {i + 1} (2 cells, 145 x 130 x 9.5)", "rear", x, x + w, y, y + d, 3.0, 12.5, color="battery", est=True))
    for k, (za, zb) in enumerate(((3.5, 7.5), (8.0, 12.0))):
        rows.append((f"Cell block{i + 1} pack {'AB'[k]}", x + 2.5, x + w - 2.5, y + 2.5, y + d - 2.5, za, zb))
    add.append(m.box(f"NTC block {i + 1}", "rear", x + w / 2 - 2, x + w / 2 + 2, y + d - 6, y + d - 2, 12.5, 13.5, color="parts", est=True))
    rows.append((f"NTC block{i + 1}", x + w / 2 - 2, x + w / 2 + 2, y + d - 6, y + d - 2, 12.5, 13.5))
for k, (x, y) in enumerate(BM):
    add.append(m.box(f"BM {k + 1} board (38 x 38)", "rear", x, x + 38, y, y + 38, 3.0, 13.5, color="pcb", est=True))
    rows.append((f"BM {k + 1}", x, x + 38, y, y + 38, 3.0, 13.5))
res = m.check(P0 + add)
bad = sorted([(round(g, 1), a, b) for g, a, b, _ in res if g < 0.0 and (any(t in a + b for t in ("Block", "BM ", "NTC")))])
print("collisions with blocks/BM/NTC:", bad[:6] or 0, "| near (<1 mm):", sorted([(round(g, 2), a, b) for g, a, b, _ in res if 0.0 <= g < 1.0 and any(t in a + b for t in ("Block", "BM ", "NTC"))])[:5], flush=True)
pw = [p for p in P if p.name == "PW power"][0]
x0, x1, y0 = pw.c[0] - pw.h[0], pw.c[0] + pw.h[0], pw.c[1] - pw.h[1]
for k, (x, y) in enumerate(BM):
    print(f"BM {k + 1} harness (Manhattan to PW edge x {x0:.0f}-{x1:.0f}, y {y0:.0f}):", round(max(x0 - (x + 38), x - x1, 0) + (y0 - (y + 38))), "mm")
cx = sum(x + w / 2 for x, y, w, d in BL) / 3; cy = sum(y + d / 2 for x, y, w, d in BL) / 3
print("CoG of blocks:", round(cx, 1), round(cy, 1), "| from centre (257.5, 250): x", round(cx - 257.5, 1), "y", round(cy - 250, 1))
print("R195: blocks start at y 155, line y 0-3 untouched")
with open(os.path.join(HERE, "blocks3.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["name", "x0", "x1", "y0", "y1", "z0", "z1"]); w.writerows(rows)
json.dump([{"n": p.name, "g": getattr(p, "group", ""), "a": [round(c - h, 2) for c, h in zip(p.c, p.h)], "b": [round(c + h, 2) for c, h in zip(p.c, p.h)]} for p in P0 + add if not p.name.startswith("Hatch vent") and "groove" not in p.name], open(os.path.join(HERE, "p137_parts.json"), "w"))
print("done", flush=True)
