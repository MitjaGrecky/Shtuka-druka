"""Green-2 compressed ("g3"): deck 30, two packs under P2 (1 mm clearances), angled screen plugs, crest and rear shift swept; all gaps >= 1 mm required."""
import importlib.util, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import build_v8 as B
ws = B.ws
spec = importlib.util.spec_from_file_location("cs", os.path.join(REPO, "docs", "ru", "img", "41_crest_study.py"))
cs = importlib.util.module_from_spec(spec); spec.loader.exec_module(cs)

import os
os.environ["W3_X1"] = "505"
os.environ["W3_S1"] = "60.2"       # the real W3 (hardware/w3-system) ends at s 60.2 before the pocket; the old model slab over the whole slope was an overestimate
B.FAN_SPEC.update(s=80.0, T=25.0, dy=-6.0, z0=3.5, gap=5.0)   # R182: 80 x 80 x 25 fan on the right wall
PACKS = "104,234,8,153,3;238,368,8,153,3;372,502,8,153,3"   # P144 (21.11): three blocks under the pads (front half of the pad zone); shelves/packs are replaced by the cells in build()
LIPO = 7.5                                     # shelf 2 + 7.5 = top z 12.5; the pack boxes are replaced by the 6 cells (batt_bays/blocks3.csv) in build()


def battery_parts(m):
    """P144/P145: battery set UNDER THE PADS from model3d/batt_bays/under_pads.csv: 3 blocks x 2 Ampul 40125140 cells on 3 mm rails (air gap under the cells,
    cells z 6.0-14.5; P3/P4 parts bottom 15.9), NTC, 2 ribs with air windows (y 40-120, z 3-12.5), long board BB1 (398 x 28)."""
    import csv
    out = []
    with open(os.path.join(HERE, "..", "batt_bays", "under_pads.csv"), newline="") as f:
        for r in csv.DictReader(f):
            n = r["name"]; v = [float(r[k]) for k in ("x0", "x1", "y0", "y1", "z0", "z1")]
            if n.endswith("envelope"):
                for k, (za, zb) in enumerate(((6.0, 10.0), (10.5, 14.5))):
                    out.append(m.box(f"Cell {n.split()[1]}{'AB'[k]} Ampul 40125140", "rear", v[0] + 2.5, v[1] - 2.5, v[2] + 2.5, v[3] - 2.5, za, zb, color="battery", est=True))
                for j, dx in enumerate((10.0, 117.0)):
                    out.append(m.box(f"Block {n.split()[1]} rail {j + 1}", "rear", v[0] + dx, v[0] + dx + 3.0, v[2] + 2.5, v[3] - 2.5, 3.0, 6.0, color="metal", est=True))
            elif n.startswith("NTC"): out.append(m.box(n, "rear", v[0], v[1], v[2], v[3], v[4] + 2.0, v[5] + 2.0, color="parts", est=True))
            elif n.startswith("Rib"):
                out.append(m.box("Bay " + n.lower() + " front", "shell", v[0], v[1], v[2], 40.0, 3.0, 15.5, color="metal", est=True))
                out.append(m.box("Bay " + n.lower() + " rear", "shell", v[0], v[1], 120.0, v[3], 3.0, 15.5, color="metal", est=True))
                out.append(m.box("Bay " + n.lower() + " top bar", "shell", v[0], v[1], 40.0, 120.0, 12.5, 15.5, color="metal", est=True))
            elif n == "BB1 board": out.append(m.box("BB1 board 398 x 28", "rear", *v, color="pcb", est=True))
    return out


def vents_and_feet(m):
    """Vents and feet: R196 side grooves, fan exhaust, front intake line, P144 battery hatches, P145 lid slots, R187 feet.
    2026-11-26 (user): the old R185 floor slots under the old battery packs are removed; battery air goes through the P145 lid slots."""
    out = []
    # R196 rev 3.1 (user): vertical grooves 2 mm, pitch 5, on BOTH side walls (x 0-3 and 512-515), blind depth 1.2 mm,
    # down to the bottom edge z 0; 15 grooves on the right wall go through over the fan (R195/P115). Source: docs/ru/img/41_sides_r196.csv
    import csv
    with open(os.path.join(REPO, "docs", "ru", "img", "41_sides_r196.csv"), encoding="utf-8") as fh:
        for i, r in enumerate(csv.DictReader(fh)):
            y, zt = float(r["y_mm"]), float(r["z_top"]) + 1.0
            for nm, x0, x1 in (("L", 0.0, 1.2), ("R", 513.8, 515.0)):
                out.append(m.box(f"Side groove {nm}{i}", "vents", x0, x1, y - 1, y + 1, 0.0, zt, color="grey", est=True, check=False))
            if r["through_z0"]:
                out.append(m.box(f"Fan exhaust groove {i} (right wall, through)", "vents", 512, 515, y - 1, y + 1, float(r["through_z0"]) - 1.0, float(r["through_z1"]) + 1.0, color="grey", est=True, check=False))
    out.append(m.box("Front intake line 2 mm", "vents", 110, 490, 0.0, 3.0, 3.0, 5.0, color="grey", est=True, check=False))
    # P144: three battery hatches in the floor over the blocks (block + 1.5 mm each side, the 2 mm ribs between them take the M3 lid screws); plates drawn 0.4 mm below the floor
    for k, (xa, xb) in enumerate(((102.5, 235.0), (237.0, 369.0), (371.0, 503.5))):
        out.append(m.box(f"Battery hatch {k + 1} (floor)", "vents", xa, xb, 6.5, 154.5, -0.4, 0.0, color="grey", est=True, check=False))
    # P145: inlet slots 4 x 40 mm in the three hatch lids, 4 columns x 2 rows per lid = 24 slots (38.4 cm2), between the rails, under the air gap below the cells
    for k, bx0 in enumerate((104.0, 238.0, 372.0)):
        for cx in (26.0, 50.0, 74.0, 98.0):
            for ry in (16.0, 88.0):
                out.append(m.box(f"Lid slot {k + 1}.{int(cx)}.{int(ry)}", "vents", bx0 + cx - 2, bx0 + cx + 2, 8.0 + ry, 8.0 + ry + 40.0, -0.4, 0.0, color="grey", est=True, check=False))
    # R187: 4 square feet 20 x 20 x 3
    for fx in (25.0, 470.0):
        for fy in (25.0, 455.0):
            out.append(m.box("Foot 20 x 20 x 3", "vents", fx, fx + 20, fy, fy + 20, -3.0, 0.0, color="grey", est=True, check=False))
    return out


def build(deck, E, crest, s_off, shift, packs=PACKS, lipo=LIPO, pwx=245, jacks="6.35"):
    rs = 40 + E
    rl, D = 413.4 + rs, 460 + rs
    h5y = D - 3 - 60 - 0.5
    B.FAN_H5C["c"] = h5y
    e = ws.env(deck, deck, 0, rl - 101, 6, packs, h5y)
    e.update(FRONT_LIP=0, REAR_SHIFT=rs, H5_REAR_X=452 - B.FAN_SPEC["T"] - B.FAN_SPEC["gap"], PW_X0=pwx, LIPO_H=lipo)
    m = ws.load(e, rl - s_off, crest, shift)
    B._H["h"] = (391, 511, h5y - 60 - 45, h5y - 60 - 25, 3.5, 26)
    P = B.rw_factory(jacks, "right")(m, m.parts())
    P = cs.angled(P, m)
    P = [p for p in P if not p.name.startswith(("Battery pack", "Battery shelf"))]   # P141: block envelopes and shelves replaced by the cells (foam on the floor)
    P += battery_parts(m)
    P += vents_and_feet(m)
    res = m.check(P)
    col = sorted([(round(abs(g), 1), a, b) for g, a, b, _ in res if g < -0.05], reverse=True)
    tight = sorted([(round(g, 1), a, b) for g, a, b, _ in res if -0.05 <= g < 1.0 and "harness room" not in a + b])
    return m, P, col, tight


if __name__ == "__main__":
    t = time.time()
    m, P, col, tight = build(30, 10, 120, 0, 20)
    print("one run", round(time.time() - t, 1), "s", len(col), "col", col[:4], len(tight), "tight", tight[:6], flush=True)
