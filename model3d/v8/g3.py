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
B.FAN_SPEC.update(s=80.0, T=25.0, dy=-6.0, z0=3.5)   # R182: 80 x 80 x 25 fan on the right wall
PACKS = "113,219,6,226,3;225,331,6,226,3"      # two packs under P2 (x0,x1,y0,y1,shelf z0); P2 tall bottom parts start at y 227.8
LIPO = 11.0


def vents_and_feet(m):
    """R184 (user: "Щели в стенках"): intake slots in the front wall (x 120-325) and the left wall (y 10-230) at the battery level z 5.5-17.5,
    about 59 cm2 together (an 80 mm fan needs about 50 cm2 of intake); no feet, no floor slots. Exhaust: the fan on the right wall."""
    out = []
    for i in range(14):                        # front wall: 14 slots 14 x 12 mm, pitch 15.5
        x0 = 120.0 + i * 15.5
        out.append(m.box(f"Front wall vent slot {i + 1}", "vents", x0, x0 + 14, -0.4, 0.2, 5.5, 17.5, color="grey", est=True, check=False))
    for j in range(10):                        # left wall: 10 slots 30 x 12 mm, pitch 22
        y0 = 10.0 + j * 22.0
        out.append(m.box(f"Left wall vent slot {j + 1}", "vents", -0.4, 0.2, y0, y0 + 30, 5.5, 17.5, color="grey", est=True, check=False))
    return out


def build(deck, E, crest, s_off, shift, packs=PACKS, lipo=LIPO, pwx=245, jacks="6.35"):
    rs = 40 + E
    rl, D = 413.4 + rs, 460 + rs
    h5y = D - 3 - 60 - 0.5
    B.FAN_H5C["c"] = h5y
    e = ws.env(deck, deck, 0, rl - 101, 6, packs, h5y)
    e.update(FRONT_LIP=0, REAR_SHIFT=rs, H5_REAR_X=451 - B.FAN_SPEC["T"], PW_X0=pwx, LIPO_H=lipo)
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
