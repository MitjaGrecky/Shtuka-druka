"""Green-2 compressed ("g3"): deck 30, two packs under P2 (1 mm clearances), angled screen plugs, crest and rear shift swept; all gaps >= 1 mm required."""
import importlib.util, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import build_v8 as B
ws = B.ws
spec = importlib.util.spec_from_file_location("cs", os.path.join(REPO, "docs", "ru", "img", "41_crest_study.py"))
cs = importlib.util.module_from_spec(spec); spec.loader.exec_module(cs)

PACKS = "113,219,6,226,3;225,331,6,226,3"      # two packs under P2 (x0,x1,y0,y1,shelf z0); P2 tall bottom parts start at y 227.8
LIPO = 11.0


def build(deck, E, crest, s_off, shift, packs=PACKS, lipo=LIPO, pwx=245, jacks="6.35"):
    rs = 40 + E
    rl, D = 413.4 + rs, 460 + rs
    h5y = D - 3 - 60 - 0.5
    B.FAN_H5C["c"] = h5y
    e = ws.env(deck, deck, 0, rl - 101, 6, packs, h5y)
    e.update(FRONT_LIP=0, REAR_SHIFT=rs, H5_REAR_X=436, PW_X0=pwx, LIPO_H=lipo)
    m = ws.load(e, rl - s_off, crest, shift)
    B._H["h"] = (391, 511, h5y - 60 - 45, h5y - 60 - 25, 3.5, 26)
    P = B.rw_factory(jacks, "right")(m, m.parts())
    P = cs.angled(P, m)
    res = m.check(P)
    col = sorted([(round(abs(g), 1), a, b) for g, a, b, _ in res if g < -0.05], reverse=True)
    tight = sorted([(round(g, 1), a, b) for g, a, b, _ in res if -0.05 <= g < 1.0 and "harness room" not in a + b])
    return m, P, col, tight


if __name__ == "__main__":
    t = time.time()
    m, P, col, tight = build(30, 10, 120, 0, 20)
    print("one run", round(time.time() - t, 1), "s", len(col), "col", col[:4], len(tight), "tight", tight[:6], flush=True)
