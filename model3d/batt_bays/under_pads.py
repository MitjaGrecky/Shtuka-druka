"""User correction 21.11 (sketch on the v8 view): batteries, ribs and the BMS board are UNDER THE PADS (front half of the pad zone), not behind them under the slope.
Three blocks 130 (x) x 145 (y) x 9.5 (z 3-12.5): x 104-234, 238-368, 372-502, y 8-153 (x >= 104: F1 and the phones jacks occupy x 12-102, y 3-40); ribs 2 mm x 235-237 and 369-371, y 8-153, z 3-15.5;
BB1 long board behind the blocks inside the pad zone: x 104-502, y 156-184 (28 wide), z 3-14. Real check of everything (m.check). Writes under_pads.csv and p137_parts.json."""
import csv, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "v8"))
import g3
m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
P0 = [p for p in P if not p.name.startswith(("Battery", "Cell", "BM", "NTC", "BB1", "Bay rib"))]
BL = [(104, 8, 130, 145), (238, 8, 130, 145), (372, 8, 130, 145)]
add, rows = [], []
for i, (x, y, w, d) in enumerate(BL):
    add.append(m.box(f"Block {i + 1} (2 cells)", "rear", x, x + w, y, y + d, 3.0, 12.5, color="battery", est=True)); rows.append((f"Block {i + 1} envelope", x, x + w, y, y + d, 3.0, 12.5))
    add.append(m.box(f"NTC block {i + 1}", "rear", x + w / 2 - 2, x + w / 2 + 2, y + d - 6, y + d - 2, 12.5, 13.5, color="parts", est=True)); rows.append((f"NTC block{i + 1}", x + w / 2 - 2, x + w / 2 + 2, y + d - 6, y + d - 2, 12.5, 13.5))
for i, (a, b) in enumerate(((235, 237), (369, 371))):
    add.append(m.box(f"Bay rib {i + 1}", "shell", a, b, 8.0, 153.0, 3.0, 15.5, color="metal", est=True)); rows.append((f"Rib {i + 1}", a, b, 8.0, 153.0, 3.0, 15.5))
add.append(m.box("BB1 board", "pcb", 104.0, 502.0, 156.0, 184.0, 3.0, 14.0, color="pcb", est=True)); rows.append(("BB1 board", 104.0, 502.0, 156.0, 184.0, 3.0, 14.0))
res = m.check(P0 + add)
bad = sorted([(round(g, 1), a, b) for g, a, b, _ in res if g < 0.0 and any(t in a + b for t in ("Block", "NTC", "rib", "BB1"))])
print("collisions of the battery set:", bad[:8] or 0, "| model total:", len([1 for g, a, b, _ in res if g < -0.05]), flush=True)
print("near < 1 mm:", sorted([(round(g, 2), a, b) for g, a, b, _ in res if 0.0 <= g < 1.0 and any(t in a + b for t in ("Block", "NTC", "rib", "BB1"))])[:6], flush=True)
cx = sum(x + w / 2 for x, y, w, d in BL) / 3; cy = 8 + 72.5
print("CoG of blocks:", round(cx, 1), cy, "| from centre (257.5, 250): x", round(cx - 257.5, 1), "y", round(cy - 250, 1), flush=True)
with open(os.path.join(HERE, "under_pads.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["name", "x0", "x1", "y0", "y1", "z0", "z1"]); w.writerows(rows)
json.dump([{"n": p.name, "g": getattr(p, "group", ""), "a": [round(c - h, 2) for c, h in zip(p.c, p.h)], "b": [round(c + h, 2) for c, h in zip(p.c, p.h)]} for p in P0 + add if not p.name.startswith("Hatch vent") and "groove" not in p.name], open(os.path.join(HERE, "p137_parts.json"), "w"))
print("done", flush=True)
