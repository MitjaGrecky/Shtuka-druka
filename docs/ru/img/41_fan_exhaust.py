#!/usr/bin/env python3
"""Doc 41 section 24.8: four elegant fan-exhaust variants on the right wall (designer, 20.11.2026; R195, doc 42 section 6).

View: the RIGHT wall seen from the RIGHT (from the neighbour's side), so the FRONT of the case is on the RIGHT of the picture
(same as 41_walls_v7). Axes: y = depth from the front edge (mm, grows to the left in the picture), z = height from the outer
floor (mm, up). Not mirrored. Geometry: model3d/v8 g3.build(30, 10, 120, 0, 20): depth 510, deck z 30 to y 300, slope 28.85 deg
to y 463.4 / z 120, then flat to the rear; fan 80 x 80 x 25 real box y 400.5-480.5, z 3.5-83.5 (the R195 lines in g3 sit at
y 390.5-470.5, i.e. 10 mm in front of the fan: to be fixed by the engineer). Status: concept (designer's proposal).

Areas are counted on a 0.1 mm raster: gross = all openings; "over the blades" = openings inside the annulus r 17-39 mm around
the fan axis (hub ~34 mm and blade tip ~78 mm are estimates for an 80 mm fan, check against the datasheet).
Run: python 41_fan_exhaust.py   -> 41_fan_exhaust.svg, 41_fan_exhaust.csv (and prints the table)."""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
FY0, FY1, FZ0, FZ1 = 400.5, 480.5, 3.5, 83.5
CY, CZ = (FY0 + FY1) / 2, (FZ0 + FZ1) / 2          # 440.5, 43.5
TAN = math.tan(math.radians(28.85))
R_HUB, R_TIP = 17.0, 39.0


def slope_z(y):                                    # outer top edge of the right wall
    if y <= 300: return 30.0
    if y <= 463.4: return 30.0 + (y - 300) * TAN
    return 120.0


# ---- variants: each returns (inside(y, z) -> bool, svg shapes in model coords) ----
def v_a():
    """A. Ruled lines (R195, refined): 13 lines 80 x 2, pitch 5, rounded ends R1, on the real fan."""
    rows = [CZ - 30 + 5 * i for i in range(13)]
    def inside(y, z):
        return FY0 <= y <= FY1 and any(abs(z - r) <= 1.0 for r in rows)
    shapes = [("rect", FY0, r - 1, FY1, r + 1, 1.0) for r in rows]
    return inside, shapes


def v_b():
    """B. Disc of lines: horizontal slots 2 mm, pitch 4, clipped to a circle 78, solid hub disc 30 in the middle."""
    rows = [CZ + 4 * k for k in range(-9, 10)]
    def inside(y, z):
        r = math.hypot(y - CY, z - CZ)
        return 15.0 <= r <= 39.0 and any(abs(z - w) <= 1.0 for w in rows)
    shapes = []
    for w in rows:
        dz = abs(w - CZ) + 1.0
        if dz >= 39: continue
        h = math.sqrt(39 ** 2 - dz ** 2) if dz < 39 else 0
        hi = math.sqrt(max(0, 15 ** 2 - (abs(w - CZ) - 1.0) ** 2)) if abs(w - CZ) - 1.0 < 15 else 0
        if hi > 0:
            shapes += [("rect", CY - h, w - 1, CY - hi, w + 1, 1.0), ("rect", CY + hi, w - 1, CY + h, w + 1, 1.0)]
        else:
            shapes.append(("rect", CY - h, w - 1, CY + h, w + 1, 1.0))
    return inside, shapes


def v_c():
    """C. Slope hatching: 2 mm lines parallel to the slope (28.85 deg), perpendicular pitch 5, inside a 76 x 76 square."""
    a = math.radians(28.85); nx, nz = -math.sin(a), math.cos(a)        # normal to the slope direction
    ds = [5 * k for k in range(-11, 12)]
    def inside(y, z):
        if not (CY - 38 <= y <= CY + 38 and CZ - 38 <= z <= CZ + 38): return False
        d = (y - CY) * nx + (z - CZ) * nz
        return any(abs(d - s) <= 1.0 for s in ds)
    shapes = []
    ux, uz = math.cos(a), math.sin(a)
    for s in ds:                                   # clip each line to the square (parametric)
        px, pz = CY + nx * s, CZ + nz * s
        t0, t1 = -200, 200
        for p, u, lo, hi in ((px, ux, CY - 37, CY + 37), (pz, uz, CZ - 37, CZ + 37)):
            ta, tb = (lo - p) / u, (hi - p) / u
            t0, t1 = max(t0, min(ta, tb)), min(t1, max(ta, tb))
        if t1 - t0 > 3:
            shapes.append(("line", px + ux * t0, pz + uz * t0, px + ux * t1, pz + uz * t1, 2.0))
    return inside, shapes


def v_d():
    """D. Micro-perforation: round holes 2.5 mm, hexagonal pitch 3.5, in a circle 78 (speaker-grille texture)."""
    holes = []
    p, rowh = 3.5, 3.5 * math.sqrt(3) / 2
    for j in range(-13, 14):
        for i in range(-13, 14):
            y = CY + i * p + (p / 2 if j % 2 else 0); z = CZ + j * rowh
            if math.hypot(y - CY, z - CZ) <= 39 - 1.25: holes.append((y, z))
    def inside(y, z):
        if math.hypot(y - CY, z - CZ) > 39: return False
        j = round((z - CZ) / rowh)
        for jj in (j - 1, j, j + 1):
            off = p / 2 if jj % 2 else 0
            i = round((y - CY - off) / p)
            for ii in (i - 1, i, i + 1):
                yy, zz = CY + ii * p + off, CZ + jj * rowh
                if math.hypot(yy - CY, zz - CZ) <= 39 - 1.25 and (y - yy) ** 2 + (z - zz) ** 2 <= 1.25 ** 2: return True
        return False
    return inside, [("circle", y, z, 1.25) for y, z in holes]


def v_r195():
    """R195 as built in g3 now (13 lines 80 x 2 at y 390.5-470.5, z 13.5...): for reference."""
    rows = [14.5 + 5 * i for i in range(13)]
    def inside(y, z):
        return 390.5 <= y <= 470.5 and any(abs(z - r) <= 1.0 for r in rows)
    return inside, [("rect", 390.5, r - 1, 470.5, r + 1, 0.0) for r in rows]


VARIANTS = [("A", "Линейка (R195, уточнённая)", v_a), ("B", "Диск из линий", v_b),
            ("C", "Штриховка по скату", v_c), ("D", "Микроперфорация", v_d)]


def measure(inside, step=0.1):
    gross = blades = 0
    top_gap = 1e9
    n = int(round(100 / step))
    for iy in range(n):
        y = 392.0 + (iy + 0.5) * step
        for iz in range(n):
            z = -6.0 + (iz + 0.5) * step
            if inside(y, z):
                gross += 1
                r = math.hypot(y - CY, z - CZ)
                if R_HUB <= r <= R_TIP and FY0 <= y <= FY1: blades += 1
                top_gap = min(top_gap, slope_z(y) - z)
    a = step * step / 100.0
    return round(gross * a, 1), round(blades * a, 1), round(top_gap, 1)


# ---- drawing ----
S = 4.0                       # px per mm in the detail panels
PW, PH = 400, 470            # panel size
DY0, DY1, DZ0, DZ1 = 384, 514, -4, 124
K = 2.7                      # px per mm actually used   # detail window in model coords


def P(ox, oy, y, z):          # front on the right: y grows to the left
    return ox + (DY1 - y) * K + 20, oy + (DZ1 - z) * K + 40


def panel(ox, oy, key, title, shapes, area):
    k = K
    el = [f'<rect x="{ox}" y="{oy}" width="{PW - 10}" height="{PH - 10}" rx="10" fill="#f4f5f2" stroke="#d5d8d2"/>',
          f'<text x="{ox + 16}" y="{oy + 26}" font-size="15" font-weight="700" fill="#1f2933">{key}. {title}</text>']
    prof = [(DY0, 0), (DY0, slope_z(DY0))] + [(y, slope_z(y)) for y in (400, 463.4)] + [(510, 120), (510, 0)]
    pts = " ".join("%.1f,%.1f" % P(ox, oy, y, z) for y, z in prof)
    el.append(f'<polygon points="{pts}" fill="#2a2e33" stroke="#111" stroke-width="1.5" stroke-linejoin="round"/>')
    a, b = P(ox, oy, FY1, FZ1), P(ox, oy, FY0, FZ0)
    el.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" rx="5" fill="none" stroke="#ff7b72" stroke-width="1" stroke-dasharray="5 4"/>')
    c = P(ox, oy, CY, CZ)
    for shp in shapes:
        if shp[0] == "rect":
            _, y0, z0, y1, z1, rr = shp
            a, b = P(ox, oy, y1, z1), P(ox, oy, y0, z0)
            el.append(f'<rect x="{a[0]:.2f}" y="{a[1]:.2f}" width="{b[0] - a[0]:.2f}" height="{b[1] - a[1]:.2f}" rx="{rr * k:.2f}" fill="#060607"/>')
        elif shp[0] == "line":
            _, y0, z0, y1, z1, w = shp
            a, b = P(ox, oy, y0, z0), P(ox, oy, y1, z1)
            el.append(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="#060607" stroke-width="{w * k:.2f}" stroke-linecap="round"/>')
        else:
            _, y, z, r = shp
            a = P(ox, oy, y, z)
            el.append(f'<circle cx="{a[0]:.2f}" cy="{a[1]:.2f}" r="{r * k:.2f}" fill="#060607"/>')
    # dimensions: fan box and rear edge
    a, b = P(ox, oy, FY1, -2), P(ox, oy, FY0, -2)
    el.append(f'<text x="{ox + 16}" y="{oy + PH - 64}" font-size="10.5" fill="#52606d" >вентилятор y 400,5–480,5, z 3,5–83,5 (пунктир)</text>')
    gross, blades, gap = area
    el.append(f'<text x="{ox + 16}" y="{oy + PH - 46}" font-size="12.5" fill="#1f2933">Площадь {str(gross).replace(".", ",")} см², над лопастями {str(blades).replace(".", ",")} см²</text>')
    el.append(f'<text x="{ox + 16}" y="{oy + PH - 28}" font-size="11" fill="#52606d">мин. перемычка до кромки ската {str(gap).replace(".", ",")} мм</text>')
    t = P(ox, oy, 508, -6)
    el.append(f'<text x="{t[0]:.0f}" y="{t[1]:.0f}" font-size="10" fill="#9aa5b1">зад ←</text>')
    t = P(ox, oy, 386, -6)
    el.append(f'<text x="{t[0]:.0f}" y="{t[1]:.0f}" font-size="10" fill="#9aa5b1" text-anchor="end">→ перед</text>')
    return el


def main():
    rows = []
    for key, title, fn in VARIANTS + [("R195", "как сейчас в g3", v_r195)]:
        inside, shapes = fn()
        rows.append((key, title, shapes, measure(inside)))
        print(key, title, rows[-1][3])
    W, H = 30 + 2 * PW, 110 + 2 * PH + 30
    el = ['<rect width="100%" height="100%" fill="#fff"/>',
          '<text x="24" y="30" font-size="18" font-weight="700" fill="#1f2933">Выход вентилятора на правой стенке: четыре варианта (концепт дизайнера, 20.11.2026)</text>',
          '<text x="24" y="52" font-size="12" fill="#52606d">Вид справа (со стороны соседа), перед корпуса справа, без зеркала. y — глубина от переднего края, z — высота от низа корпуса, мм.</text>',
          '<text x="24" y="70" font-size="12" fill="#52606d">Геометрия: model3d/v8 g3 (дека 30, скат 28,85°, макушка 120, глубина 510). Условие инженера (док. 42 §6): выход ≥ 17–21 см².</text>',
          '<text x="24" y="88" font-size="12" fill="#52606d">Все прорези в цвет корпуса, кромки скруглены R1 / фаска 0,5; за ними сетка от пыли, тёмная. Статус: предложение, не проверено продувкой.</text>']
    for i, (key, title, shapes, area) in enumerate(rows[:4]):
        el += panel(15 + (i % 2) * PW, 100 + (i // 2) * PH, key, title, shapes, area)
    g = rows[4][3]
    el.append(f'<text x="24" y="{H - 14}" font-size="11" fill="#b42318">Для сравнения R195 в g3 сейчас: {str(g[0]).replace(".", ",")} см², над лопастями {str(g[1]).replace(".", ",")} см² — линии стоят на y 390,5–470,5, на 10 мм впереди вентилятора (исправить в g3).</text>')
    open(os.path.join(HERE, "41_fan_exhaust.svg"), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Segoe UI, Arial, sans-serif">' + "".join(el) + "</svg>")
    with open(os.path.join(HERE, "41_fan_exhaust.csv"), "w", encoding="utf-8") as f:
        f.write("variant,title,gross_cm2,over_blades_cm2,min_web_to_slope_mm\n")
        for key, title, _, (a, b, gp) in rows:
            f.write(f"{key},{title},{a},{b},{gp}\n")
    print(W, H)


if __name__ == "__main__":
    main()
