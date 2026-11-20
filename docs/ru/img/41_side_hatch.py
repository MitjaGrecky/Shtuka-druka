#!/usr/bin/env python3
"""Doc 41 section 24.11 (variant S4): the user's sketch on variant C (20.11.2026) - slope-parallel hatching over the whole
rear part of BOTH side walls, so the fan is not visible as a separate element; only on the right wall the lines over the
fan are cut through. User: "hide the fan from the design point of view, the same on both sides, through slots on one side only".

Views: LEFT wall seen from the LEFT (front on the LEFT), RIGHT wall seen from the RIGHT (front on the RIGHT), mirror images as a
person walking around the case sees them; detail: right wall around the fan. y = depth from the front edge, z = height from the
outer floor, mm. Geometry 41_geom_v8.py = g3.build(30, 0, 117, 20, 0): depth 500, slope 33.1 deg y 300-433.4, crest 117;
fan 80 x 80 x 25 at y 390.5-470.5, z 3.5-83.5. Lines 2 mm, perpendicular pitch P, parallel to the slope; the field is the side
silhouette inset by 10 mm (top line = slope edge inset 10). Blind grooves 1-1.2 mm deep, dark bottom; through only inside the
fan frame (76 x 76). Status: concept (designer's proposal). Run: python 41_side_hatch.py -> 41_side_hatch.svg / .csv"""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
import importlib.util as _iu
_s = _iu.spec_from_file_location("g41", os.path.join(os.path.dirname(os.path.abspath(__file__)), "41_geom_v8.py")); G = _iu.module_from_spec(_s); _s.loader.exec_module(G)
A = math.radians(G.ANG); TAN, COS = G.TAN, G.COS
FY0, FY1, FZ0, FZ1 = G.FY0, G.FY1, G.FZ0, G.FZ1
CY, CZ = G.CY, G.CZ
WIN = (CY - 38, CY + 38, CZ - 38, CZ + 38)         # inside the fan frame
PROF = G.PROF
INSET = 10.0


def top_inset(y):
    """top edge inset by INSET: reflex corner at the fold (max), convex corner at the crest (min)"""
    s = 30 + (y - 300) * TAN - INSET / COS
    return min(max(30 - INSET, s), G.CREST - INSET)


def lines(pitch):
    out = []
    v0 = INSET / COS
    k = 0
    while True:
        off = v0 + k * pitch / COS                        # vertical offset below the slope edge line
        f = lambda y: 30 + (y - 300) * TAN - off
        ys = [y / 20 for y in range(int(INSET * 20), int((G.D - INSET) * 20) + 1)]
        ok = [y for y in ys if INSET - 1e-9 <= f(y) <= top_inset(y) + 1e-9]
        if f(G.D - INSET) < INSET: break
        if ok and ok[-1] - ok[0] > 10: out.append((ok[0], f(ok[0]), ok[-1], f(ok[-1]), off))
        k += 1
    return out


def through(ls):
    cuts = []
    for y0, z0, y1, z1, off in ls:
        f = lambda y: 30 + (y - 300) * TAN - off
        ys = [y / 20 for y in range(int(WIN[0] * 20), int(WIN[1] * 20) + 1)]
        ok = [y for y in ys if y0 <= y <= y1 and WIN[2] + 1 <= f(y) <= WIN[3] - 1]
        if ok and ok[-1] - ok[0] > 3: cuts.append((ok[0], f(ok[0]), ok[-1], f(ok[-1]), off))
    return cuts


def measure(cuts, step=0.1):
    g = b = 0
    for iy in range(int(80 / step)):
        y = WIN[0] - 2 + (iy + .5) * step
        for iz in range(int(80 / step)):
            z = WIN[2] - 2 + (iz + .5) * step
            for y0, z0, y1, z1, off in cuts:
                zl = 30 + (y - 300) * TAN - off
                # distance to the line, and within the segment (with round caps)
                if abs(z - zl) * COS <= 1.0 and y0 - 1 <= y <= y1 + 1:
                    if (y0 <= y <= y1) or math.hypot(y - y0, z - z0) <= 1 or math.hypot(y - y1, z - z1) <= 1:
                        g += 1
                        if 17 <= math.hypot(y - CY, z - CZ) <= 39: b += 1
                        break
    a = step * step / 100
    return round(g * a, 1), round(b * a, 1)


def T(ox, oy, k, y, z, right, y_from=0):
    x = ((G.D - y) if right else y) if y_from == 0 else ((y_from[1] - y) if right else (y - y_from[0]))
    return ox + x * k, oy + (124 - z) * k


def wall(ox, oy, k, right, ls, cuts, view=None, ztop=124):
    el = []
    yf = 0 if view is None else view
    P = lambda y, z: T(ox, oy - (124 - ztop) * k, k, y, z, right, yf)
    clip = f'clip{int(ox)}_{int(oy)}'
    el.append(f'<clipPath id="{clip}"><polygon points="' + " ".join("%.1f,%.1f" % P(y, z) for y, z in PROF) + '"/></clipPath>')
    if view is not None:
        a, b = P(view[1] if right else view[0], ztop), P(view[0] if right else view[1], -4)
        el.append(f'<clipPath id="{clip}w"><rect x="{min(a[0], b[0]):.1f}" y="{a[1]:.1f}" width="{abs(b[0] - a[0]):.1f}" height="{b[1] - a[1]:.1f}"/></clipPath><g clip-path="url(#{clip}w)">')
    el.append('<polygon points="' + " ".join("%.1f,%.1f" % P(y, z) for y, z in PROF) + '" fill="#33383e" stroke="#111" stroke-width="1.2" stroke-linejoin="round"/>')
    for y0, z0, y1, z1, _ in ls:
        a, b = P(y0, z0), P(y1, z1)
        el.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#15171a" stroke-width="{2 * k:.2f}" stroke-linecap="round"/>')
    if right:
        for y0, z0, y1, z1, _ in cuts:
            a, b = P(y0, z0), P(y1, z1)
            el.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#000" stroke-width="{2 * k:.2f}" stroke-linecap="round"/>')
        a, b = P(FY1, FZ1), P(FY0, FZ0)
        el.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" rx="3" fill="none" stroke="#ff7b72" stroke-width="0.9" stroke-dasharray="5 4"/>')
    if view is not None: el.append('</g>')
    return el


def main():
    pitch = 5.0
    ls = lines(pitch); cuts = through(ls); area = measure(cuts)
    ls4 = lines(4.0); cuts4 = through(ls4); area4 = measure(cuts4)
    print("pitch 5:", len(ls), "lines,", len(cuts), "through,", area, "| pitch 4:", len(ls4), len(cuts4), area4)
    print("field front tip y", round(min(l[0] for l in ls), 1))
    K = 1.45
    W = int(20 + G.D * K + 20)
    el = ['<rect width="100%" height="100%" fill="#fff"/>',
          '<text x="20" y="28" font-size="18" font-weight="700" fill="#1f2933">S4. Штриховка по скату на обеих стенках (по наброску пользователя)</text>',
          '<text x="20" y="48" font-size="12" fill="#52606d">Линии 2 мм параллельно скату 33,1°, шаг 5 по нормали; поле — силуэт стенки с отступом 10.</text>',
          '<text x="20" y="64" font-size="12" fill="#52606d">Тёмные — глухие канавки на обеих стенках; чёрные — сквозные, только справа внутри рамки вентилятора 76 × 76.</text>',
          '<text x="20" y="80" font-size="12" fill="#52606d">y — глубина, z — высота, мм; геометрия g3 боевая (глубина 500, скат 33,1°, макушка 117). Статус: концепт дизайнера, 20.11.2026.</text>',
          f'<text x="20" y="104" font-size="14" font-weight="700" fill="#1f2933">Сквозные {str(area[0]).replace(".", ",")} см², над лопастями {str(area[1]).replace(".", ",")} см² (шаг 4 в зоне вентилятора: {str(area4[0]).replace(".", ",")} / {str(area4[1]).replace(".", ",")})</text>']
    oy = 118
    el.append(f'<text x="20" y="{oy + 12}" font-size="11.5" fill="#52606d">Левая стенка, вид слева (← перед)</text>')
    el += wall(20, oy + 20, K, False, ls, cuts)
    oy2 = oy + 20 + 124 * K + 30
    el.append(f'<text x="20" y="{oy2 + 12}" font-size="11.5" fill="#52606d">Правая стенка, вид справа (перед →); пунктир — вентилятор 80 × 80</text>')
    el += wall(20, oy2 + 20, K, True, ls, cuts)
    oy3 = oy2 + 20 + 124 * K + 30
    K2 = 3.6
    el.append(f'<text x="20" y="{oy3 + 12}" font-size="11.5" fill="#52606d">Деталь: правая стенка у вентилятора, вид справа (перед →), y 370–500, масштаб ≈ 2,5× к верхним</text>')
    el += wall(20, oy3 + 20, K2, True, ls, cuts, view=(G.FY0 - 20, G.D), ztop=124)
    H = int(oy3 + 20 + 128 * K2 + 30)
    open(os.path.join(HERE, "41_side_hatch.svg"), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Segoe UI, Arial, sans-serif">' + "".join(el) + "</svg>")
    with open(os.path.join(HERE, "41_side_hatch.csv"), "w", encoding="utf-8") as f:
        f.write("pitch_mm,lines,through_lines,through_cm2,over_blades_cm2\n")
        f.write(f"5,{len(ls)},{len(cuts)},{area[0]},{area[1]}\n4,{len(ls4)},{len(cuts4)},{area4[0]},{area4[1]}\n")
    print(W, H)


if __name__ == "__main__":
    main()
