import os, g3
B = g3.B
res = []
for w3x1 in (505, 496, 492, 488, 484):
    os.environ["W3_X1"] = str(w3x1)
    for s, t in ((80, 15), (80, 25), (92, 15), (92, 25)):
        for dy in (0, -10, -20):
            for z0 in (3.5,):
                B.FAN_SPEC.update(s=float(s), T=float(t), dy=float(dy), z0=float(z0))
                m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
                tag = "OK" if (not col and not tight) else f"{len(col)} col {col[:1]} tight {len(tight)}"
                print(f"W3 end {w3x1}, fan {s}x{s}x{t} dy {dy}: {tag}", flush=True)
