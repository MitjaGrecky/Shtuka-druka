import math, sys, json, time
import g3
out = []
t0 = time.time()
for E in (0, 2, 4, 6, 8, 10):
    for crest in range(112, 123):
        for s_off in (0, 5, 10, 15, 20, 30):
            for shift in (0, 10, 20, 30):
                try:
                    m, P, col, tight = g3.build(30, E, float(crest), s_off, shift)
                except Exception as ex:
                    continue
                ok = (not col) and (not tight)
                out.append(dict(E=E, crest=crest, s_off=s_off, shift=shift, ang=round(math.degrees(m.SLOPE), 1), depth=m.D + m.FL, col=len(col), tight=len(tight), ok=ok,
                                first=(col[:1] or tight[:1])))
                if ok:
                    print("OK", out[-1], flush=True)
    print("E", E, "done", round(time.time() - t0), "s", flush=True)
json.dump(out, open("g3_sweep.json", "w"), ensure_ascii=False)
print("finished", len(out))
