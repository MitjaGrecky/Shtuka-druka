"""Orange variant (deck 22, step 9, no front overhang, 3.5 mm jacks): move the fan away from behind the H5 so the H5 can sit against the rear wall.
A: fan on the right wall, H5 shifted left by 15 (x 376-496), R2 arm to 373.  B: fan on the rear wall LEFT of the H5 (x 331-391), R2 arm to 328.  C: current (fan behind H5)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_v8 as B
ws = B.ws


def orange(opt):
    fs, deck, roof, ang = 15, 22, 41, 33
    rl, D = 453.4 + fs, 500 + fs
    y1 = D - 3
    flush = opt in ("A", "B")
    h5c = (y1 - 60 - 0.5) if flush else (y1 - 15 - 60 - 0.5)
    e = ws.env(22, 31, fs, rl - 101, 20, f"40,210,{rl - 101},{rl - 1},3", h5c, h5_st=8)
    e.update(FRONT_LIP=0)
    if opt == "A":
        e.update(H5_REAR_X=436)
    run_len = D - 3 - roof - (300 + fs)
    back = round(31 + run_len * math.tan(math.radians(ang)), 1)
    m = ws.load(e, D - 3 - roof, back, 30)
    S = m.SKIN
    h0 = h5c - 60
    h5x0 = 376 if opt == "A" else 391
    harness = (h5x0, h5x0 + 120, h0 - 45, h0 - 25, 3.5, 26)
    P0 = m.parts()
    if opt == "C":
        rw = ws.corner_rework2(harness=harness)
        P = rw(m, P0)
    else:
        arm = 373 if opt == "A" else 328
        keep = [p for p in P0 if p.name not in ("R2 control rear board, low arm", "Rear jacks", "Rear jacks (right)")]
        y0 = 413.4 + m.RS
        jt = m.REAR_JACK_TOP
        keep.append(m.box("R2 low arm (shortened)", "rear", m.R2_TALL_X1, arm, y0, y0 + 1.6, 10, 38, color="pcb"))
        keep.append(m.box("Rear jacks (left)", "rear", 5, arm, y0 + 1.6, y1, 8, jt, color="metal", est=True))
        keep.append(m.box("Rear panel-mount jacks over the H5", "rear", h5x0, 510, y1 - 25, y1, 70, min(jt, 112), color="metal", est=True))
        keep.append(m.box("H5 harness room", "rear", *harness, color="plastic", est=True))
        if opt == "A":
            keep.append(m.box("Fan 60 x 60 x 15 (right wall)", "rear", 497, 512, h5c - 30, h5c + 30, 6, 66, color="plastic"))
        else:
            keep.append(m.box("Fan 60 x 60 x 15 (rear wall, left of H5)", "rear", 331, 391, y1 - 15, y1, 6, 66, color="plastic"))
        P = keep
    P = [p for p in P if p.name not in ("Phones 1 jack", "Phones 2 jack", "F1 headphone board", "F1 headphone board parts below")]
    for p in list(P):
        if p.name == "P1 Left parts below":
            lo = [c - h for c, h in zip(p.c, p.h)]; hi = [c + h for c, h in zip(p.c, p.h)]
            P.remove(p); P.append(m.box("P1 Left parts below (from y 43)", "panel", lo[0], hi[0], 43, hi[1], lo[2], hi[2], color="parts", est=True))
    for x in (32, 80):
        P.append(m.box(f"Phones jack 3.5 at x {x}", "front", x - 4.5, x + 4.5, 3.0, 16.0, S + 2.0, S + 7.5, color="metal", est=True))
    P.append(m.box("F1 small board", "front", 12, 102, 3.0, 38, S + 0.4, S + 2.0, color="pcb"))
    P.append(m.box("F1 relays 5.4", "front", 45, 70, 18, 36, S + 2.0, S + 7.4, color="parts", est=True))
    P.append(m.box("F1 low parts 2.5", "front", 72, 100, 18, 36, S + 2.0, S + 4.5, color="parts", est=True))
    return m, P


if __name__ == "__main__":
    for opt in ("C", "A", "B"):
        m, P = orange(opt)
        res = m.check(P)
        col = sorted([(round(abs(g), 1), a, b) for g, a, b, e in res if g < -0.05], reverse=True)
        print(opt, "depth", m.D + m.FL, "rear", m.BACK_Z, "collisions", len(col), col[:8], flush=True)
