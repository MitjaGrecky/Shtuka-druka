"""P140: 3 thin blocks (2 Ampul cells each, 145 x 130 x 9.5, z 3..12.5, rotation 90 deg allowed) + 2 BM (38 x 38 x 11, z 3..14) under P1/P2/P3-P4, deck and A1 unchanged.
Phase 1: real check (m.check) of block candidates on a 25 mm grid in the under-deck zone (y <= 300). Phase 2: best disjoint triple by CoG distance to the centre (257.5, 250).
Phase 3: BM candidates next to the blocks (real check), harness = Manhattan distance BM -> PW edge. CSV blocks3.csv. Log runs/blocks3.log."""
import csv, itertools, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "v8"))
import g3
m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
P0 = [p for p in P if not p.name.startswith("Battery")]
Z0, Z1 = 3.0, 12.5
t0 = time.time()
good = []
for w, d in ((145.0, 130.0), (130.0, 145.0)):
    for x in range(5, int(510 - w) + 1, 25):
        for y in range(5, int(300 - d) + 1, 25):
            b = m.box("Blk", "rear", x, x + w, y, y + d, Z0, Z1, color="battery", est=True)
            if not [g for g, a, bb, _ in m.check(P0 + [b]) if g < 0.0 and "Blk" in (a + bb)]: good.append((x, y, w, d))
print("clear block positions:", len(good), "of the grid; ", round(time.time() - t0), "s", flush=True)
sep = lambda a, b: a[0] + a[2] + 1.0 <= b[0] or b[0] + b[2] + 1.0 <= a[0] or a[1] + a[3] + 1.0 <= b[1] or b[1] + b[3] + 1.0 <= a[1]
CX, CY = 257.5, 250.0
best = None
for tri in itertools.combinations(good, 3):
    if all(sep(a, b) for a, b in itertools.combinations(tri, 2)):
        cx = sum(a[0] + a[2] / 2 for a in tri) / 3; cy = sum(a[1] + a[3] / 2 for a in tri) / 3
        dist = math.hypot(cx - CX, cy - CY)
        if best is None or dist < best[0]: best = (dist, tri, cx, cy)
if not best:
    print("no triple of disjoint clear blocks", flush=True); print("done", flush=True); sys.exit()
dist, tri, cx, cy = best
print("best triple:", tri, "| CoG", round(cx, 1), round(cy, 1), "-> from centre x", round(cx - CX, 1), "y", round(cy - CY, 1), flush=True)
blocks = [m.box(f"Blk{i}", "rear", x, x + w, y, y + d, Z0, Z1, color="battery", est=True) for i, (x, y, w, d) in enumerate(tri)]
pw = [p for p in P if p.name == "PW power"][0]
bm = []
for k in range(2):
    cand = None
    for (x, y, w, d) in tri:
        for bx, by in ((x - 39, y), (x + w + 1, y), (x, y + d + 1), (x - 39, y + d - 38), (x + w + 1, y + d - 38), (x + w - 38, y + d + 1)):
            if bx < 4 or by < 4 or bx + 38 > 511 or by + 38 > 295: continue
            if any(abs(bx - e[0]) < 38 and abs(by - e[1]) < 38 for e in bm): continue
            b = m.box("BM", "rear", bx, bx + 38, by, by + 38, 3.0, 14.0, color="pcb", est=True)
            if [g for g, a, bb, _ in m.check(P0 + blocks + [b] + [m.box("BMo", "rear", e[0], e[0] + 38, e[1], e[1] + 38, 3.0, 14.0, color="pcb", est=True) for e in bm]) if g < 0.0 and ("BM" in (a + bb) or "Blk" in (a + bb))]: continue
            dpw = max(pw.c[0] - pw.h[0] - (bx + 38), (bx) - (pw.c[0] + pw.h[0]), 0) + max(pw.c[1] - pw.h[1] - (by + 38), 0)
            if cand is None or dpw < cand[0]: cand = (dpw, bx, by)
    print(f"BM {k + 1}:", cand, flush=True)
    if cand: bm.append((cand[1], cand[2], cand[0]))
rows = []
for i, (x, y, w, d) in enumerate(tri):
    for k, (za, zb) in enumerate(((3.0 + 0.7, 7.7), (8.2, 12.2))):
        rows.append((f"Cell B{i + 1}-{'AB'[k]}", x + 2.5, x + w - 2.5, y + 2.5, y + d - 2.5 if d > 0 else y, za, zb))
for k, (x, y, dpw) in enumerate(bm): rows.append((f"BM {k + 1}", x, x + 38, y, y + 38, 3.0, 14.0))
with open(os.path.join(HERE, "blocks3.csv"), "w", newline="") as f:
    wtr = csv.writer(f); wtr.writerow(["name", "x0", "x1", "y0", "y1", "z0", "z1"]); wtr.writerows(rows)
print("harness lengths (Manhattan BM -> PW edge, straight):", [round(b[2]) for b in bm], flush=True)
print("done", flush=True)
