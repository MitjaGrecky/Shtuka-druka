"""Real W3 ends before the pocket (s 60.2): the old model slab over the whole slope is not a real part. Which fans fit then?"""
import os, g3
B = g3.B
os.environ["W3_X1"] = "505"
os.environ["W3_S1"] = "60.2"
for s, t in ((80, 15), (80, 25), (92, 15), (92, 25), (120, 25)):
    best = None
    for dy in (0, -6, -12, -18):
        for z0 in (3.5, 6.0):
            B.FAN_SPEC.update(s=float(s), T=float(t), dy=float(dy), z0=float(z0))
            m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
            ok = not col and not tight
            print(f"fan {s}x{s}x{t} dy {dy} z0 {z0}: ", "OK" if ok else f"{len(col)} col {col[:2]} tight {len(tight)}", flush=True)
