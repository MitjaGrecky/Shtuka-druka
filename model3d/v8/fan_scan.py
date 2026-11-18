import g3
B = g3.B
ok = []
for s in (80, 92):
    for t in (15, 25):
        for dy in (0, -6, -12, -18, -24):
            for z0 in (3.5, 6.0):
                B.FAN_SPEC.update(s=float(s), T=float(t), dy=float(dy), z0=float(z0))
                m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
                if not col and not tight:
                    ok.append((s, t, dy, z0)); print("OK", s, t, dy, z0, flush=True)
print("done", len(ok))
