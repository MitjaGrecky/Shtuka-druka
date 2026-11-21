"""P137-v: where is the screen LCM and how does a 170x51x24 pack at (100, 299) collide for several screen offsets (g3.build 4th/5th args)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "v8"))
import g3
for s_off, shift in ((20, 0), (20, 3), (20, -3), (23, 0), (17, 0)):
    m, P, col, tight = g3.build(30, 0, 117.0, s_off, shift)
    P0 = [p for p in P if not p.name.startswith("Battery")]
    if (s_off, shift) == (20, 0):
        for p in P0:
            if p.name.startswith(("Screen", "W1 Levels", "A1 audio", "R1 audio")):
                print(p.name, [round(c - h, 1) for c, h in zip(p.c, p.h)], [round(c + h, 1) for c, h in zip(p.c, p.h)], flush=True)
    b = m.box("Pack", "rear", 100, 270, 299, 350, 3.0, 27.0, color="battery", est=True)
    res = m.check(P0 + [b])
    print("s_off", s_off, "shift", shift, "collisions in model:", len(col), "| pack:", sorted([(round(g, 1), a if bb == "Pack" else bb) for g, a, bb, _ in res if "Pack" in (a, bb) and g < 1.0])[:4], flush=True)
