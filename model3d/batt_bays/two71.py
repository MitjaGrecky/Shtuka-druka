"""P137-v: real check of two 170x51x24 packs after a screen shift: pack 1 (104..274, 299..350), pack 2 (276..446, 299..350); g3.build 5th arg = screen shift."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "v8"))
import g3
for shift in (6, 8):
    m, P, col, tight = g3.build(30, 0, 117.0, 20, shift)
    P0 = [p for p in P if not p.name.startswith("Battery")]
    for name, x0 in (("Pack A", 104), ("Pack B", 276)):
        b = m.box(name, "rear", x0, x0 + 170, 299, 350, 3.0, 27.0, color="battery", est=True)
        res = m.check(P0 + [b])
        print("shift", shift, name, "model collisions", len(col), sorted([(round(g, 1), a if bb == name else bb) for g, a, bb, _ in res if name in (a, bb) and g < 1.0])[:5], flush=True)
print("done", flush=True)
