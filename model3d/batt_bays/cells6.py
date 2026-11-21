"""P139-b: 6 Ampul 40125140 cells (140 x 125 x 4.0) as 2 stacks of 3 under P2 + 2 BM boards (38 x 38, parts up to 12.5, z 3..15.5) at the stack ends + NTC per stack.
Stack 1: x 189.5-329.5 (centred in 187-332), y 8.5-133.5; stack 2: y 140.5-265.5; cells z 3.3 + k*4.7 (gap 0.7): top 16.7 (< P2 parts 17.4). Real check (m.check).
BM positions: coarse grid at both x sides of the stacks, first clear nearest-to-PW chosen. CSV -> cells6.csv. Log runs/cells6.log."""
import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "v8"))
import g3
m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
P0 = [p for p in P if not p.name.startswith("Battery")]
cells, rows = [], []
for s, y0 in ((1, 8.5), (2, 140.5)):
    for k in range(3):
        z0 = 3.3 + k * 4.7
        cells.append(m.box(f"Cell S{s}C{k + 1} Ampul 40125140", "rear", 189.5, 329.5, y0, y0 + 125.0, z0, z0 + 4.0, color="battery", est=True))
        rows.append((f"Cell S{s}C{k + 1}", 189.5, 329.5, y0, y0 + 125.0, round(z0, 2), round(z0 + 4.0, 2)))
    ntc = (329.0, 331.0, y0 + 60, y0 + 64, 16.7, 17.2)
    cells.append(m.box(f"NTC S{s}", "rear", *ntc, color="parts", est=True)); rows.append((f"NTC S{s}",) + ntc[0:2] + ntc[2:4] + ntc[4:6])
base = P0 + cells
print("cells+NTC collisions:", sorted([(round(g, 1), a, b) for g, a, b, _ in m.check(base) if g < 0.0 and ("Cell" in a + b or "NTC" in a + b)])[:4], flush=True)
pw = [p for p in P if p.name == "PW power"][0]
pwc = (pw.c[0], pw.c[1])
chosen = []
for s, (ylo, yhi) in ((1, (6, 136)), (2, (138, 268))):
    best = None
    for side, xs in (("right", range(331, 380, 4)), ("left", range(110, 152, 4))):
        for x in xs:
            for y in range(int(ylo) - 0, int(yhi - 38) + 1, 8):
                b = m.box(f"BM S{s}", "rear", x, x + 38, y, y + 38, 3.0, 15.5, color="pcb", est=True)
                bad = [g for g, a, bb, _ in m.check(base + [b]) if g < 0.0 and "BM S" in (a + bb)]
                if bad: continue
                d = abs(x + 19 - pwc[0]) + abs(y + 19 - pwc[1])
                if best is None or d < best[0]: best = (d, side, x, y)
    print(f"BM S{s}:", best, flush=True)
    if best: chosen.append((s, best))
for s, (d, side, x, y) in chosen:
    rows.append((f"BM S{s}", x, x + 38, y, y + 38, 3.0, 15.5)); print(f"BM S{s} {side} x {x}-{x + 38}, y {y}-{y + 38}: Manhattan to PW centre {round(d)} mm")
with open(os.path.join(HERE, "cells6.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["name", "x0", "x1", "y0", "y1", "z0", "z1"]); w.writerows(rows)
print("done", flush=True)
