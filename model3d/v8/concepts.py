"""Concepts K1 (low wedge) and K3 (ridge) of the designer (docs/ru/41_design_review.md, section 20) built on the same model as build_v8.py.
Common: deck 30, no front overhang, 6.35 jacks under P1, battery under the pads, A1 on the floor, H5 in the rear right corner on 8 mm,
R1 / R2 lying (strip z 3.5-50 on x 5-388 along the rear wall), screen with right-angle plugs (cable bends removed), USB/SD pocket moved to the right side
(pocket and W3 bottom parts removed over the H5)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_v8 as B  # noqa: E402
ws = B.ws

DROP = ("R1 audio rear board", "R2 control rear board", "R2 control rear board, low arm", "R2 low arm (shortened)", "Rear jacks", "Rear jacks (left)",
        "Rear panel-mount jacks over the H5", "Fan 60 x 60 x 15 (rear wall, behind H5)", "Fan 60 x 60 x 15", "Pocket board", "Pocket board pins",
        "USB-A receptacle (C)", "SD socket (full size)", "SD card (inserted)")


def concept(kind, h5st=8, ang=28.0, shift=30, fan_y=462.0):
    fs, deck = 0, 30
    rl, D = 453.4, 500
    h5c = D - 3 - 15 - 60 - 0.5 if kind == "k1" else 425.0
    e = ws.env(deck, deck, fs, rl - 101, 6, "130,300,60,160,3", h5c, h5_st=h5st)
    e.update(FRONT_LIP=0)
    if kind == "k1":
        shelf, back = D - 3 - 41, round(deck + (D - 3 - 41 - 300) * math.tan(math.radians(ang)), 1)
    else:
        shelf, back = 440.0, 117.0
    m = ws.load(e, shelf, back, shift)
    P = m.parts()
    S = m.SKIN
    y1 = m.D - S
    P = [p for p in P if p.name not in DROP and "cable bend" not in p.name and not p.name.startswith("W3 System parts below")
         and p.name not in ("Phones 1 jack", "Phones 2 jack", "F1 headphone board", "F1 headphone board parts below")]
    for p in list(P):
        if p.name == "P1 Left parts below":
            lo = [c - h for c, h in zip(p.c, p.h)]; hi = [c + h for c, h in zip(p.c, p.h)]
            P.remove(p); P.append(m.box("P1 Left parts below (from y 43)", "panel", lo[0], hi[0], 43, hi[1], lo[2], hi[2], color="parts", est=True))
    for x in (32, 80):
        P.append(m.box(f"Phones jack 6.35 at x {x}", "front", x - 7.95, x + 7.95, 3.0, 30.0, S + 2.0, S + 14.7, color="metal", est=True))
    P.append(m.box("F1 small board", "front", 12, 102, 3.0, 40, S + 0.4, S + 2.0, color="pcb"))
    P.append(m.box("F1 relays 5.4", "front", 45, 70, 31, 40, S + 2.0, S + 7.4, color="parts", est=True))
    P.append(m.box("Rear strip: R1 / R2 lying + jacks (est.)", "rear", 5, 388, y1 - 40, y1, 3.5, 50, color="metal", est=True))
    h0, h1 = h5c - 60, h5c + 60
    P.append(m.box("H5 harness room", "rear", 391, 511, h0 - 45, h0 - 25, 3.5, 26, color="plastic", est=True))
    if kind == "k1":
        P.append(m.box("Fan 60 x 60 x 15 (rear wall)", "rear", 421, 481, y1 - 15, y1, 6, 66, color="plastic"))
        P.append(m.box("Power / USB jacks over the H5 (est.)", "rear", 451, 510, y1 - 25, y1, 70, 110, color="metal", est=True))
    else:
        # ridge: the rear wall is low (55), the back goes down from the ridge (y 440, z 117) to z 55 at the wall at about 47 deg
        P = [p for p in P if p.name not in ("Rear wall", "Shelf")]
        ang = math.degrees(math.atan2(117 - 55, y1 - 440))
        L = math.hypot(y1 - 440, 117 - 55)
        P.append(m.Box("Rear slope skin", "shell", (257.5, (440 + y1) / 2 + 1.0, (117 + 55) / 2 + 1.5), (509.0, L, 3.0), rx=-ang, color="shell"))
        P.append(m.box("Rear wall (low)", "shell", 0, m.W, y1, m.D, S, 55, color="shell"))
        d = (math.cos(math.radians(ang)), -math.sin(math.radians(ang))); n = (math.sin(math.radians(ang)), math.cos(math.radians(ang)))
        zs = 117 - (fan_y - 440) * math.tan(math.radians(ang))
        P.append(m.Box("Fan 60 x 60 x 15 (rear slope)", "rear", (451.0, fan_y - 11.5 * n[0], zs - 11.5 * n[1]), (60.0, 60.0, 15.0), rx=-ang, color="plastic"))
    return m, P


if __name__ == "__main__":
    def rep(tag, m, P):
        res = m.check(P)
        col = sorted([(round(abs(g), 1), a, b) for g, a, b, e in res if g < -0.05], reverse=True)
        print(tag, "rear", m.BACK_Z, "slope", round(math.degrees(m.SLOPE), 1), "depth", m.D + m.FL, "collisions", len(col), col[:8], flush=True)
    for ang in (28.0, 29.0, 30.0):
        rep(f"k1 {ang}", *concept("k1", ang=ang))
    for sh in (30, 12):
        rep(f"k3 shift {sh}", *concept("k3", shift=sh, ang=47.4))
