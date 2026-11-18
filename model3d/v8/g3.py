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
PACKS = "113,219,6,226,3;225,331,6,226,3"      # two packs under P2 (x0,x1,y0,y1,shelf z0); P2 tall bottom parts start at y 227.8
LIPO = 11.0


def vents_and_feet(m):
    """R185 (user): holes through the case walls are removed; only slots in the hatch under the batteries stay.
    12 slots 4 x 40 mm per compartment (2 columns x 6 rows, pitch 34 mm), about 19 cm2 per pack. No wall slots, no feet."""
    out = []
    for k, x0 in enumerate((113.0, 225.0)):
        for cx in (x0 + 26.0, x0 + 80.0):
            for r in range(6):
                y0 = 20.0 + r * 34.0
                out.append(m.box(f"Hatch vent slot {k + 1}.{int(cx)}.{r}", "vents", cx - 2, cx + 2, y0, y0 + 40, -0.4, 0.0, color="grey", est=True, check=False))
    # R187: fan exhaust = one flat slot 60 x 3 in the right wall opposite the fan; 4 square feet 20 x 20 x 3
    out.append(m.box("Fan exhaust slot (right wall)", "vents", 512, 515, 400.5, 460.5, 38.5, 41.5, color="grey", est=True, check=False))
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
    P += vents_and_feet(m)
    res = m.check(P)
    col = sorted([(round(abs(g), 1), a, b) for g, a, b, _ in res if g < -0.05], reverse=True)
    tight = sorted([(round(g, 1), a, b) for g, a, b, _ in res if -0.05 <= g < 1.0 and "harness room" not in a + b])
    return m, P, col, tight


if __name__ == "__main__":
    t = time.time()
    m, P, col, tight = build(30, 10, 120, 0, 20)
    print("one run", round(time.time() - t, 1), "s", len(col), "col", col[:4], len(tight), "tight", tight[:6], flush=True)
