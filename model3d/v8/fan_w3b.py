import os, g3
B = g3.B
for w3x1 in (496,):
    os.environ["W3_X1"] = str(w3x1)
    for s, t in ((80, 15), (80, 25), (92, 15)):
        for dy in (-2, -4, -6, -8, -10, -12):
            B.FAN_SPEC.update(s=float(s), T=float(t), dy=float(dy), z0=3.5)
            m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
            print(f"fan {s}x{s}x{t} dy {dy}: ", "OK" if (not col and not tight) else f"{len(col)} col {col[:2]} tight {len(tight)} {tight[:1]}", flush=True)
