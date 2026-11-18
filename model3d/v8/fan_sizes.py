"""R182: which fans fit on the right wall of the main line (g3): size x thickness, collisions and gaps (all >= 1 mm required)."""
import sys
import g3
B = g3.B
for s, t in ((60, 15), (60, 25), (80, 15), (80, 25), (92, 15), (92, 25), (120, 25)):
    B.FAN_SPEC.update(s=float(s), T=float(t))
    m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
    print(f"fan {s}x{s}x{t}: collisions {len(col)} {col[:3]}; tight {len(tight)} {tight[:3]}", flush=True)
