#!/usr/bin/env python3
"""Doc 41 section 23: the user's sketch on artifact v8 (17.11.2026, green): lower the crest (red), make the case longer
by moving the whole rear (R1 / R2, rear jacks, H5, fan, A1, PW) back by E (yellow), and let the screen slope end at the
top front edge of the rear-jack block. Sweep E and the crest height; report collisions and tight places (< 1 mm).
Uses model3d/v8/build_v8.py (fan on the right wall, H5 against the rear wall) and 41_wedge_study.py; reads the model only.
Run: python 41_crest_study.py"""
import importlib.util
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
spec = importlib.util.spec_from_file_location("b8", os.path.join(REPO, "model3d", "v8", "build_v8.py"))
b8 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b8)
ws = b8.ws


def build(deck, E, crest, shift, jacks="6.35"):
    rs = 40 + E
    rl, D = 413.4 + rs, 460 + rs
    h5y = D - 3 - 60 - 0.5
    b8.FAN_H5C["c"] = h5y
    if deck >= 28:
        e = ws.env(deck, deck, 0, rl - 101, 6, "130,300,60,160,3", h5y)
    else:
        e = ws.env(22, 31, 0, rl - 101, 20, f"40,210,{rl - 101},{rl - 1},3", h5y)
    e.update(FRONT_LIP=0, REAR_SHIFT=rs, H5_REAR_X=436)
    shelf = rl                                   # slope ends at the front face of the rear block
    m = ws.load(e, shelf, crest, shift)
    b8._H["h"] = (391, 511, h5y - 60 - 45, h5y - 60 - 25, 3.5, 26)
    P = b8.rw_factory(jacks, "right")(m, m.parts())
    res = m.check(P)
    col = sorted([(round(abs(g), 1), a, b) for g, a, b, _ in res if g < -0.05], reverse=True)
    tight = sorted([(round(g, 1), a, b) for g, a, b, _ in res if -0.05 <= g < 1.0])
    return m, P, col, tight


if __name__ == "__main__" and os.environ.get("PW") != "1":
    best = []
    for deck in (30, 22):
        for crest in (117, 120, 124):
            for E in (0, 10, 20, 30):
                r = None
                for sh in (-10, 0, 10, 20, 30):
                    m, P, col, tight = build(deck, E, crest, sh, "6.35" if deck >= 28 else "3.5")
                    key = (len(col), len(tight))
                    if r is None or key < r[0]:
                        r = (key, sh, m, col, tight)
                (nc, nt), sh, m, col, tight = r
                print(f"deck {deck}, crest {crest}, rear +{E}: slope {math.degrees(m.SLOPE):.1f} deg, depth {m.D:g}, screen shift {sh}: "
                      f"{nc} collisions, {nt} tight; {col[:4]} {tight[:3]}", flush=True)


def build_pw(deck, E, crest, shift, pwx, jacks="6.35"):
    rs = 40 + E
    rl, D = 413.4 + rs, 460 + rs
    h5y = D - 3 - 60 - 0.5
    b8.FAN_H5C["c"] = h5y
    if deck >= 28:
        e = ws.env(deck, deck, 0, rl - 101, 6, "130,300,60,160,3", h5y)
    else:
        e = ws.env(22, 31, 0, rl - 101, 20, f"40,210,{rl - 101},{rl - 1},3", h5y)
    e.update(FRONT_LIP=0, REAR_SHIFT=rs, H5_REAR_X=436, PW_X0=pwx)
    m = ws.load(e, rl, crest, shift)
    b8._H["h"] = (391, 511, h5y - 60 - 45, h5y - 60 - 25, 3.5, 26)
    P = b8.rw_factory(jacks, "right")(m, m.parts())
    res = m.check(P)
    col = sorted([(round(abs(g), 1), a, b) for g, a, b, _ in res if g < -0.05], reverse=True)
    tight = sorted([(round(g, 1), a, b) for g, a, b, _ in res if -0.05 <= g < 1.0 and "harness room" not in a + b])
    return m, P, col, tight


if __name__ == "__main__" and os.environ.get("PW") == "1":
    for deck in (30, 22):
        for crest in (117, 120):
            for E in (10, 20):
                for pwx in (260, 272):
                    for sh in (10, 20, 30):
                        m, P, col, tight = build_pw(deck, E, crest, sh, pwx, "6.35" if deck >= 28 else "3.5")
                        print(f"deck {deck} crest {crest} +{E} PW x {pwx} sh {sh}: slope {math.degrees(m.SLOPE):.1f}, {len(col)} col, {len(tight)} tight {col[:3]} {tight[:3]}", flush=True)


def angled(P, m):
    """Angled (90 deg) HDMI / USB-C plugs on the screen driver: the cable runs flat along the screen back instead of a bend
    that hangs down 30-50 mm (assumption: low-profile angled plugs, <= 12 mm behind the driver board)."""
    return [p for p in P if not (p.name.startswith("Screen") and ("bend" in p.name or "cable down" in p.name))]


if __name__ == "__main__" and os.environ.get("PW") == "2":
    for deck in (30, 22):
        for crest in (117, 120):
            for E in (0, 10, 20):
                for sh in (20, 30):
                    m, P, col, tight = build_pw(deck, E, crest, sh, 245, "6.35" if deck >= 28 else "3.5")
                    P2 = angled(P, m)
                    res = m.check(P2)
                    c2 = sorted([(round(abs(g), 1), a, b) for g, a, b, _ in res if g < -0.05], reverse=True)
                    t2 = sorted([(round(g, 1), a, b) for g, a, b, _ in res if -0.05 <= g < 1.0 and "harness room" not in a + b])
                    print(f"deck {deck} crest {crest} +{E} sh {sh}: slope {math.degrees(m.SLOPE):.1f}, depth {m.D:g}: {len(c2)} col {c2[:3]}; tight {len(t2)} {t2[:4]}", flush=True)
