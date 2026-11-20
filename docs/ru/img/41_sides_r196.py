#!/usr/bin/env python3
"""Doc 41 section 24.13: side walls by R196 (user, 20.11.2026): "Pipes, but with decay. That is, following the case lines,
but continuing until full decay" = hybrid of K2 "Pipes" and K3 "Release" (24.12).

Rule: vertical grooves 2 mm wide, pitch 5, bottoms on z 10 (inset 10 from the bottom edge).
  - behind the deck fold (wedge): top = the slope edge inset 10 (K2: the bars follow the case lines), up to the crest inset;
  - in front of the point where the inset slope meets the deck inset (z 20), the bars continue forward under the deck and their
    height decays exponentially from 10 mm, h = 10 * exp(-(y_k - y) / TAU), until h < H_MIN (full decay: the last ones are dots).
Both walls identical (mirror); blind grooves 1-1.2 mm deep with a dark bottom; through-cuts only on the RIGHT wall inside the fan
frame 76 x 76. Geometry: 41_geom_v8.py (production g3.build(30, 0, 117, 20, 0)).
Views: top - 3/4 perspective (left wall from front-left, right wall from front-right); bottom - elevations: LEFT wall seen from
the LEFT (front on the left), RIGHT wall seen from the RIGHT (front on the right); y depth from the front edge, z from the outer
floor, mm, 1 px = 1 mm. Status: concept (designer's proposal by R196). Run: python 41_sides_r196.py"""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
import importlib.util as _iu
_s = _iu.spec_from_file_location("g41", os.path.join(HERE, "41_geom_v8.py")); G = _iu.module_from_spec(_s); _s.loader.exec_module(G)
V2 = G.load("41_sides_v2")

INS, PITCH, TAU, H_MIN = 10.0, 5.0, 85.0, 1.0


def y_knee():
    """where the inset slope edge reaches the deck inset (z 20)"""
    return G.FOLD_Y + (INS / G.COS - INS) / G.TAN    # 30 + (y - 300) tan - 10/cos = 20


def bars():
    yk = y_knee()
    segs, y = [], G.D - INS
    while y > INS:
        if y >= yk:
            t = V2.top_inset(y)
        else:
            h = (G.DECK - 2 * INS) * math.exp(-(yk - y) / TAU)
            if h < H_MIN: break
            t = INS + max(h, 0.0)
        segs.append(((y, INS), (y, t)))
        y -= PITCH
    return segs


def dims(ox, oy, k, segs, right):
    T = lambda y, z: (ox + ((G.D - y) if right else y) * k, oy + (124 - z) * k)
    el = []
    yk, yend = y_knee(), segs[-1][0][0]
    for y, lab in ((G.FOLD_Y, "перегиб 300"), (yend, f"конец {yend:.0f}".replace(".", ","))):
        a, b = T(y, -4), T(y, -14)
        el.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#d64545"/>')
        el.append(f'<text x="{b[0]:.1f}" y="{b[1] + 12:.1f}" font-size="10" fill="#d64545" text-anchor="middle">{lab}</text>')
    return el


def main():
    segs = bars(); cuts = V2.through(segs); area = V2.measure(cuts)
    yk = y_knee(); yend = segs[-1][0][0]
    n_wedge = sum(1 for (a, b) in segs if a[0] >= yk)
    print(f"bars {len(segs)} (wedge {n_wedge}, decay {len(segs) - n_wedge}), through {len(cuts)}, area {area}, knee y {yk:.1f}, last bar y {yend:.1f} h {segs[-1][1][1] - INS:.2f}")
    Wd = 1150
    el = ['<rect width="100%" height="100%" fill="#fff"/>',
          '<text x="20" y="30" font-size="19" font-weight="700" fill="#1f2933">Боковины по R196: «Трубы» с затуханием</text>',
          '<text x="20" y="52" font-size="12.5" fill="#52606d">Вертикальные канавки 2 мм, шаг 5, низ z 10. На клине верх идёт по скату (отступ 10) — «соответствие линиям корпуса»; дальше под декой</text>',
          f'<text x="20" y="70" font-size="12.5" fill="#52606d">высота затухает от 10 мм: h = 10·exp(−(y₀ − y)/{TAU:.0f}), y₀ = {str(round(yk, 1)).replace(".", ",")}, до полного затухания (последние — точки). Обе стенки одинаковые, зеркально.</text>',
          '<text x="20" y="88" font-size="12.5" fill="#52606d">Тёмные — глухие канавки (глубина 1–1,2, дно тёмное); сквозные — только справа в рамке вентилятора 76 × 76. Геометрия — боевая g3 (41_geom_v8.py).</text>',
          f'<text x="20" y="112" font-size="15" font-weight="700" fill="#1f2933">Сквозные {str(area[0]).replace(".", ",")} см², над лопастями {str(area[1]).replace(".", ",")} см²; канавок {len(segs)} на стенку ({n_wedge} на клине, {len(segs) - n_wedge} в затухании, до y {yend:.0f}). Статус: концепт.</text>']
    CW, CH = 565, 360
    el.append(f'<rect x="10" y="126" width="{Wd - 20}" height="{CH}" rx="12" fill="#eef0ec"/>')
    el.append('<text x="26" y="150" font-size="12" fill="#52606d">Вид 3/4: спереди-слева (левая стенка)</text>')
    el.append(f'<text x="{26 + CW}" y="150" font-size="12" fill="#52606d">Вид 3/4: спереди-справа (правая стенка)</text>')
    el += V2.persp(24, 160, CW - 40, CH - 50, (-620, 40, 300), (90, 330, 40), segs, cuts, False)
    el += V2.persp(24 + CW, 160, CW - 40, CH - 50, (G.W + 620, 40, 300), (G.W - 90, 330, 40), segs, cuts, True)
    oy = 126 + CH + 30
    el.append(f'<text x="20" y="{oy}" font-size="12" fill="#52606d">Левая стенка — вид слева (← перед)</text>')
    el.append(f'<text x="{40 + G.D}" y="{oy}" font-size="12" fill="#52606d">Правая стенка — вид справа (перед →); пунктир — вентилятор 80 × 80</text>')
    el += V2.elev(20, oy + 10, 1.0, False, segs, cuts) + dims(20, oy + 10, 1.0, segs, False)
    el += V2.elev(40 + G.D, oy + 10, 1.0, True, segs, cuts) + dims(40 + G.D, oy + 10, 1.0, segs, True)
    H = int(oy + 10 + 124 + 40)
    open(os.path.join(HERE, "41_sides_r196.svg"), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd} {H}" width="{Wd}" height="{H}" font-family="Segoe UI, Arial, sans-serif">' + "".join(el) + "</svg>")
    with open(os.path.join(HERE, "41_sides_r196.csv"), "w", encoding="utf-8") as f:
        f.write("y_mm,z_bottom,z_top,through\n")
        cut_y = {round(a[0], 2) for a, b in cuts}
        for a, b in segs:
            f.write(f"{a[0]:.1f},{a[1]:.1f},{b[1]:.2f},{int(round(a[0], 2) in cut_y)}\n")
    print(Wd, H)


if __name__ == "__main__":
    main()
