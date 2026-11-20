#!/usr/bin/env python3
"""Doc 41 section 24.10: one graphic on BOTH side walls, the fan exhaust is the through-cut part of it on the right wall only
(user, 20.11.2026: "a design of the side wall on both sides, with the holes fitted into it on the needed side").

Each row: LEFT wall seen from the LEFT (front of the case on the LEFT of the picture) and RIGHT wall seen from the RIGHT
(front on the RIGHT). Mirror images of one graphic, as a person walking around the case sees them. y = depth from the front
edge, z = height from the outer floor, mm. Geometry model3d/v8 g3 (41_geom_v8.py = g3.build(30, 0, 117, 20, 0): depth 500,
slope 33.1 deg y 300-433.4, crest 117); fan 80 x 80 x 25 on the right wall, y 390.5-470.5, z 3.5-83.5 (centre 430.5, 43.5).
Grooves: blind, 2 mm wide, 1.0-1.2 mm deep in the 3 mm wall (dark grey in the picture); through-cuts black (with dark dust mesh).
Status: concept (designer's proposal). Areas: through-cuts only, raster 0.1 mm; "over blades" = annulus r 17-39 (estimate).
Run: python 41_side_walls.py -> 41_side_walls.svg, 41_side_walls.csv"""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
import importlib.util as _iu
_s = _iu.spec_from_file_location("g41", os.path.join(os.path.dirname(os.path.abspath(__file__)), "41_geom_v8.py")); G = _iu.module_from_spec(_s); _s.loader.exec_module(G)
A = math.radians(G.ANG); TAN, COS = G.TAN, G.COS
FY0, FY1, FZ0, FZ1 = G.FY0, G.FY1, G.FZ0, G.FZ1
CY, CZ = G.CY, G.CZ
PROF = G.PROF


def top(y):
    return G.top(y)


def inset_front(z, d):
    """front-most y of the silhouette inset by d at height z"""
    if z <= 30 - d: return d
    return 300 + (z - 30 + d / COS) / TAN


# ---------- S1: echo of the silhouette (horizontal lines) ----------
def s1():
    rows = [8.5 + 5 * i for i in range(15)]            # z 8.5 ... 78.5
    grooves, cuts = [], []
    for z in rows:
        y0, y1 = inset_front(z, 10), G.D - 10
        if y1 - y0 < 5: continue
        grooves.append((y0, z, y1))
        a, b = max(y0, FY0 + 2), FY1 - 2               # through part over the fan, inside its frame
        if b > a: cuts.append((a, z, b))
    def inside(y, z):
        return any(a <= y <= b and abs(z - zz) <= 1.0 for a, zz, b in cuts)
    return grooves, cuts, inside, []


# ---------- S2: contour groove + disc of lines ----------
def s2():
    d = 8.0
    contour = [(d, d), (d, 30 - d), (inset_front(30 - d + 0.001, d), 30 - d)]
    # inset polygon of the profile (convex corners only, so line offsets are enough)
    z_slope_end = G.CREST - d
    contour = [(d, d), (d, 30 - d), (300 + (30 - d - 30 + d / COS) / TAN, 30 - d),
               (300 + (z_slope_end - 30 + d / COS) / TAN, z_slope_end), (G.D - d, z_slope_end), (G.D - d, d)]
    rows = [CZ + 4 * k for k in range(-9, 10)]
    disc = []
    for w in rows:
        dz = abs(w - CZ) + 1.0
        if dz >= 39: continue
        h = math.sqrt(39 ** 2 - dz ** 2)
        e = abs(w - CZ) - 1.0
        hi = math.sqrt(15 ** 2 - e ** 2) if e < 15 else 0
        if hi > 0: disc += [(CY - h, w, CY - hi), (CY + hi, w, CY + h)]
        else: disc.append((CY - h, w, CY + h))
    def inside(y, z):
        r = math.hypot(y - CY, z - CZ)
        return 15 <= r <= 39 and any(abs(z - w) <= 1.0 for w in rows)
    return [], disc, inside, contour


# ---------- S3: perforation gradient ----------
def s3():
    p, rh = 3.5, 3.5 * math.sqrt(3) / 2
    dots_blind, dots_cut = [], []
    for j in range(0, 40):
        z = 6 + j * rh
        for i in range(0, 160):
            y = 6 + i * p + (p / 2 if j % 2 else 0)
            if y > G.D - 6 or z > top(y) - 7 or y < 170: continue
            dia = 2.5 if y >= G.FY0 - 5 else 0.6 + 1.9 * (y - 170) / (G.FY0 - 5 - 170)
            if math.hypot(y - CY, z - CZ) <= 39 - 1.25 and dia >= 2.49:
                dots_cut.append((y, z, dia / 2))
            else:
                dots_blind.append((y, z, dia / 2))
    def inside(y, z):
        return any((y - a) ** 2 + (z - b) ** 2 <= r * r for a, b, r in dots_cut if abs(y - a) < 2 and abs(z - b) < 2)
    return dots_blind, dots_cut, inside, "dots"


VARIANTS = [("S1", "Эхо силуэта: линии", s1), ("S2", "Кант + диск", s2), ("S3", "Перфорация с растяжкой", s3)]


def measure(inside, step=0.1):
    g = b = 0
    for iy in range(900):
        y = G.FY0 - 4.5 + (iy + .5) * step
        for iz in range(900):
            z = -1 + (iz + .5) * step
            if inside(y, z):
                g += 1
                if 17 <= math.hypot(y - CY, z - CZ) <= 39: b += 1
    return round(g * step * step / 100, 1), round(b * step * step / 100, 1)


K = 1.45
PW = G.D * K + 30
WH = 124 * K + 40          # one wall block height


def T(ox, oy, y, z, right):
    x = (G.D - y) if right else y                       # right wall from the right: front on the right
    return ox + 15 + x * K, oy + 34 + (124 - z) * K


def wall(ox, oy, right, data, kind):
    grooves, cuts, _, extra = data
    el = []
    el.append('<polygon points="' + " ".join("%.1f,%.1f" % T(ox, oy, y, z, right) for y, z in PROF) +
              '" fill="#33383e" stroke="#111" stroke-width="1.2" stroke-linejoin="round"/>')
    gcol, ccol = "#15171a", "#000"
    if kind == "dots":
        for y, z, r in grooves:
            c = T(ox, oy, y, z, right); el.append(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r * K:.2f}" fill="{gcol}"/>')
        for y, z, r in cuts:
            c = T(ox, oy, y, z, right); el.append(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r * K:.2f}" fill="{ccol if right else gcol}"/>')
    else:
        for y0, z, y1 in grooves:
            a, b = T(ox, oy, y0, z, right), T(ox, oy, y1, z, right)
            el.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{gcol}" stroke-width="{2 * K:.2f}" stroke-linecap="round"/>')
        for y0, z, y1 in cuts:
            a, b = T(ox, oy, y0, z, right), T(ox, oy, y1, z, right)
            el.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{ccol if right else gcol}" stroke-width="{2 * K:.2f}" stroke-linecap="round"/>')
        if extra:
            el.append('<polygon points="' + " ".join("%.1f,%.1f" % T(ox, oy, y, z, right) for y, z in extra) +
                      f'" fill="none" stroke="{gcol}" stroke-width="{1.5 * K:.2f}" stroke-linejoin="round"/>')
    if right:
        a, b = T(ox, oy, FY1, FZ1, right), T(ox, oy, FY0, FZ0, right)
        el.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" rx="3" fill="none" stroke="#ff7b72" stroke-width="0.8" stroke-dasharray="4 3"/>')
    lab = "Правая стенка, вид справа (перед →)" if right else "Левая стенка, вид слева (← перед)"
    el.append(f'<text x="{ox + 15}" y="{oy + 24}" font-size="11" fill="#52606d">{lab}</text>')
    return el


def main():
    W = 30 + PW
    H = int(150 + 3 * (2 * WH + 40))
    el = ['<rect width="100%" height="100%" fill="#fff"/>',
          '<text x="20" y="28" font-size="18" font-weight="700" fill="#1f2933">Боковые стенки: один рисунок с двух сторон</text>',
          '<text x="20" y="48" font-size="12" fill="#52606d">Выход вентилятора — сквозная часть рисунка, только на правой стенке. Концепт дизайнера, 20.11.2026.</text>',
          '<text x="20" y="66" font-size="12" fill="#52606d">Левая стенка — вид слева (перед слева); правая — вид справа (перед справа): как видит человек, обходя корпус.</text>',
          f'<text x="20" y="84" font-size="12" fill="#52606d">y — глубина, z — высота, мм; геометрия model3d/v8 {G.LABEL}. Пунктир — вентилятор 80 × 80 (только справа).</text>',
          '<text x="20" y="102" font-size="12" fill="#52606d">Тёмные — глухие канавки 2 мм, глубина 1–1,2; чёрные — сквозные (за ними сетка). Площади — только сквозные.</text>']
    rows = []
    for i, (key, title, fn) in enumerate(VARIANTS):
        data = fn()
        kind = "dots" if data[3] == "dots" else "lines"
        area = measure(data[2])
        rows.append((key, title, area, len(data[0]), len(data[1])))
        print(key, title, area, len(data[0]), len(data[1]))
        oy = 125 + i * (2 * WH + 40)
        el.append(f'<text x="20" y="{oy + 8}" font-size="15" font-weight="700" fill="#1f2933">{key}. {title}: сквозные {str(area[0]).replace(".", ",")} см², над лопастями {str(area[1]).replace(".", ",")} см²</text>')
        el += wall(5, oy, False, data, kind)
        el += wall(5, oy + WH, True, data, kind)
    open(os.path.join(HERE, "41_side_walls.svg"), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H}" width="{W:.0f}" height="{H}" font-family="Segoe UI, Arial, sans-serif">' + "".join(el) + "</svg>")
    with open(os.path.join(HERE, "41_side_walls.csv"), "w", encoding="utf-8") as f:
        f.write("variant,title,through_cm2,over_blades_cm2,blind_elements,through_elements\n")
        for key, title, (a, b), nb, nc in rows: f.write(f"{key},{title},{a},{b},{nb},{nc}\n")
    print(round(W), H)


if __name__ == "__main__":
    main()
