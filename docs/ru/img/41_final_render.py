#!/usr/bin/env python3
"""Design sketches for docs/ru/41_design_review.md, section 18: the final form without the lip (17.11.2026).
One simple 3D scene (shell extruded from the side profile + panel controls from mockup/layout/layout_v7.json),
three cameras: 3/4 front-left-top, side (left), top. Painter's algorithm, flat shading, plain SVG.
Numbers: deck 22, step 9 at y 315 (45 deg chamfer), slope to y 471 / z 131 (32.7 deg), roof 41, depth and width 515,
H5 in the rear right corner (x 391-511, y 376-496), 60 mm fan on the rear wall behind it; see doc 41 sections 15-17.
Conventions: plan corner radii are not modelled (drawn as edge highlights); knobs and buttons are simple prisms.
Run: python 41_final_render.py  -> 41_final_34.svg, 41_final_side.svg, 41_final_top.svg, 41_final_compare.svg"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LAY = json.load(open(os.path.join(HERE, "..", "..", "..", "mockup", "layout", "layout_v7.json"), encoding="utf-8"))

W, D = 515.0, 515.0
DECK, STEP_Y, STEP_Z, CH = 22.0, 315.0, 31.0, 4.0
SHELF_Y, BACK = 471.0, 131.0
SLOPE = math.atan2(BACK - STEP_Z, SHELF_Y - STEP_Y)
PROFILE = [(0, 0), (0, DECK - 3), (3, DECK), (STEP_Y, DECK), (STEP_Y, STEP_Z - CH), (STEP_Y + CH, STEP_Z),
           (SHELF_Y, BACK), (D - 3, BACK), (D, BACK - 3), (D, 0)]
SCREEN_SHIFT = 30.0
SCREEN_X, SCREEN_G, SCREEN_A = 220.75, (239.0, 147.0), (217.0, 136.0)   # centre x, glass, active area
SKIP_KINDS = ()

GRAPHITE = (44, 48, 54)
EDGE = (70, 76, 84)
MAP = {"red": (232, 86, 74), "green": (85, 194, 107), "white": (230, 230, 230), "grey": (78, 84, 92), "teal": (63, 195, 157),
       "purple": (127, 119, 221), "amber": (240, 162, 58), "blue": (74, 168, 232), "coral": (240, 128, 100), "alu": (175, 180, 186)}


def rgb(c):
    if isinstance(c, str) and c.startswith("#"):
        return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
    return MAP.get(c, (78, 84, 92))


def s_of(y):
    return (y - 300.0) / math.cos(SLOPE)


# ---------------------------------------------------------------- scene: faces = (points3d, color, normal, layer, stroke)
def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def norm(a):
    L = math.sqrt(dot(a, a)) or 1
    return (a[0] / L, a[1] / L, a[2] / L)


FACES = []


def shell():
    n = len(PROFILE)
    for i in range(n):
        (y0, z0), (y1, z1) = PROFILE[i], PROFILE[(i + 1) % n]
        if (y0, z0) == (y1, z1):
            continue
        nrm = norm((0, -(z1 - z0), (y1 - y0)))          # clockwise profile in (y, z): outward = (-dz, dy)
        nrm = (0, nrm[1], nrm[2])
        quad = [(0, y0, z0), (W, y0, z0), (W, y1, z1), (0, y1, z1)]
        FACES.append((quad, GRAPHITE, nrm, 0, None))
    left = [(0, y, z) for y, z in PROFILE]
    right = [(W, y, z) for y, z in reversed(PROFILE)]
    FACES.append((left, (56, 61, 68), (-1, 0, 0), 0, None))
    FACES.append((right, (56, 61, 68), (1, 0, 0), 0, None))


def frame_deck():
    return (0, 0, DECK), (1, 0, 0), (0, 1, 0), (0, 0, 1)


def frame_slope():
    c, s = math.cos(SLOPE), math.sin(SLOPE)
    return (0, STEP_Y + CH * 0, STEP_Z), (1, 0, 0), (0, c, s), (0, -s, c)


def prism(fp, h0, h1, frame, color, layer=1, top_color=None, stroke=None):
    O, U, V, N = frame
    P = lambda u, v, h: tuple(O[i] + u * U[i] + v * V[i] + h * N[i] for i in range(3))
    top = [P(u, v, h1) for u, v in fp]
    FACES.append((top, top_color or color, N, layer, stroke))
    k = len(fp)
    for i in range(k):
        (u0, v0), (u1, v1) = fp[i], fp[(i + 1) % k]
        q = [P(u0, v0, h0), P(u1, v1, h0), P(u1, v1, h1), P(u0, v0, h1)]
        e = (u1 - u0, v1 - v0)
        nn = norm(tuple(e[1] * U[j] - e[0] * V[j] for j in range(3)))   # footprint counter-clockwise -> outward
        FACES.append((q, tuple(int(c * 0.8) for c in color), nn, layer, None))


def rect(cx, cy, w, h):
    return [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]


def circ(cx, cy, r, k=20):
    return [(cx + r * math.cos(2 * math.pi * i / k), cy + r * math.sin(2 * math.pi * i / k)) for i in range(k)]


def controls():
    deck, slope = frame_deck(), frame_slope()
    for e in LAY["elements"]:
        k, x, y, w, h = e["kind"], e["x"], e["y"], e["w"], e["h"]
        if k in SKIP_KINDS:
            continue
        on_slope = y >= 300
        fr = slope if on_slope else deck
        v = s_of(y) if on_slope else y
        col = rgb(e.get("color", "grey"))
        if k == "pad":
            prism(rect(x, v, 25.5, 21), 0, 2.5, fr, col, top_color=col)
        elif k == "button":
            base = (66, 71, 79)
            led = rgb(e.get("color", "grey"))
            prism(rect(x, v, w, h), 0, 2.2, fr, base, top_color=tuple(int(0.55 * c + 0.45 * b) for c, b in zip(led, base)))
        elif k in ("encoder", "pot"):
            r = w / 2
            ring = rgb(e.get("color", "grey"))
            prism(circ(x, v, r + 3.5), 0, 0.4, fr, tuple(int(c * 0.9) for c in ring))       # light ring
            prism(circ(x, v, r), 0, 11 if k == "encoder" else 14, fr, (30, 32, 35) if k == "encoder" else (170, 175, 180))
        elif k == "wheel":
            prism(circ(x, v, 19, 32), 0, 8.5, fr, (24, 26, 29))
            prism(circ(x, v, 17, 32), 8.5, 8.7, fr, (40, 44, 50))
        elif k == "strip":
            prism(rect(x, v + h / 2, w, h), 0, 0.3, fr, (60, 90, 120))
        elif k == "fader":
            prism(rect(x, v, w, 4), 0, 0.3, fr, (20, 20, 20))
            prism(rect(x - 8, v, 8, 14), 0, 9, fr, (200, 200, 205))
        elif k == "meter":
            for i in range(14):
                c = (85, 194, 107) if i < 9 else ((240, 162, 58) if i < 12 else (232, 86, 74))
                prism(rect(x, v - h / 2 + 4 + i * 7.2, w - 2, 5), 0, 0.4, fr, c)
        elif k == "pocket":
            prism(rect(x, v, w, h), -1.5, 0.1, fr, (20, 22, 25))
        elif k == "power":
            prism(circ(x, v, 7), 0, 2, fr, (90, 95, 100), top_color=(200, 90, 80))
        elif k == "led":
            prism(circ(x, v, 2, 8), 0, 0.4, fr, (232, 86, 74))
    # Param 1-8 knobs (M1) are in the layout as encoders already. Screen: glass + simple UI.
    sc = s_of(365) + SCREEN_SHIFT
    prism(rect(SCREEN_X, sc, *SCREEN_G), -0.2, 0.15, slope, (14, 16, 20))
    prism(rect(SCREEN_X, sc, *SCREEN_A), 0.15, 0.2, slope, (22, 30, 42))
    cols = ["#e8564a", "#f0a23a", "#e7d24a", "#55c26b", "#3fc39d", "#4aa8e8", "#7f77dd", "#d4537e"]
    for i in range(8):
        cx = 122.75 + 28 * i
        for j in range(4):
            if (i + j) % 3 == 2:
                continue
            if abs(45 - j * 22) + 8 > SCREEN_A[1] / 2:
                continue
            prism(rect(cx, sc + 45 - j * 22, 24, 16), 0.2, 0.25, slope, rgb(cols[(7 - j) % 8]) if j else rgb(cols[i]))
    prism(rect(220.75, sc - SCREEN_A[1] / 2 + 10, 200, 4), 0.2, 0.25, slope, (120, 130, 145))
    # headphone jacks (3.5 mm, front wall) and the front edge
    for x in (32.0, 80.0):
        FACES.append(([(x - 4 + 4 * math.cos(a), 0, 11 + 4 * math.sin(a)) for a in [2 * math.pi * i / 16 for i in range(16)]],
                      (15, 15, 15), (0, -1, 0), 1, None))


def interior():
    """Dashed outlines of the inside parts (side and top views only)."""
    return [("H5", (376, 496, 391.5, 511.5, 11, 55), "#d64545"), ("вент.", (497, 512, 421.5, 481.5, 6, 66), "#8a96a3"),
            ("A1", (20, 240, 367, 467, 20, 42), "#3f9b5b"), ("АКБ", (40, 210, 367, 467, 3, 17), "#e8b84a"),
            ("PW", (245, 345, 375, 455, 6, 25), "#3f9b5b"), ("F1", (15, 105, 3, 38, 3, 8), "#3f9b5b"),
            ("R1 / R2", (4, 373, 468, 470, 8, 113), "#3f9b5b")]


# ---------------------------------------------------------------- cameras
def cam_34():
    phi, el = math.radians(32), math.radians(30)
    c = (-math.sin(phi) * math.cos(el), -math.cos(phi) * math.cos(el), math.sin(el))     # towards the camera
    r = (math.cos(phi), -math.sin(phi), 0)
    u = cross(c, r)
    if u[2] < 0:
        u = (-u[0], -u[1], -u[2])
    return c, r, u


def cam_side():
    return (-1, 0, 0), (0, 1, 0), (0, 0, 1)


def cam_top():
    return (0, 0, 1), (1, 0, 0), (0, 1, 0)


LIGHT = norm((-0.35, -0.55, 0.75))


def render(cam, fname, title, scale, notes=(), dims=None, inside=False, size=None, inset=None):
    c, r, u = cam
    pts2 = lambda p: (dot(p, r) * scale, -dot(p, u) * scale)
    vis = []
    for pts, col, n, layer, st in FACES:
        if dot(n, c) <= 1e-6:
            continue
        depth = sum(dot(p, c) for p in pts) / len(pts)
        sh = 0.5 + 0.5 * max(0.0, dot(n, LIGHT))
        cc = tuple(min(255, int(v * (0.75 + 0.5 * sh))) for v in col)
        vis.append((layer, depth, [pts2(p) for p in pts], cc))
    vis.sort(key=lambda f: (f[0], f[1]))
    xs = [x for f in vis for x, _ in f[2]]
    ys = [y for f in vis for _, y in f[2]]
    mx, my = min(xs), min(ys)
    pad = 60
    Wd, Hd = (max(xs) - mx) + 2 * pad, (max(ys) - my) + 2 * pad + 40 + 16 * len(notes)
    if size:
        Wd = max(Wd, size[0])
    off = lambda x, y: (x - mx + pad, y - my + pad + 30)
    el = [f'<rect width="100%" height="100%" fill="#f4f5f6"/>',
          f'<text x="20" y="26" font-size="16" font-weight="700" fill="#1f2933">{title}</text>']
    for layer, d, poly, cc in vis:
        el.append('<polygon points="' + " ".join(f"{off(x, y)[0]:.1f},{off(x, y)[1]:.1f}" for x, y in poly) +
                  f'" fill="rgb{cc}" stroke="rgb{tuple(max(0, v - 18) for v in cc)}" stroke-width="0.4" stroke-linejoin="round"/>')
    if inside:
        for lab, (x0, x1, y0, y1, z0, z1), col in interior():
            cs = [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
            pp = [off(*pts2(p)) for p in cs]
            ax = [p[0] for p in pp]
            ay = [p[1] for p in pp]
            el.append(f'<rect x="{min(ax):.1f}" y="{min(ay):.1f}" width="{max(ax) - min(ax):.1f}" height="{max(ay) - min(ay):.1f}" '
                      f'fill="none" stroke="{col}" stroke-width="1.6" stroke-dasharray="5 3"/>')
            el.append(f'<text x="{(min(ax) + max(ax)) / 2:.1f}" y="{(min(ay) + max(ay)) / 2 + 4:.1f}" font-size="11" font-weight="700" '
                      f'fill="{col}" text-anchor="middle">{lab}</text>')
    if dims:
        for kind, a, b, lab in dims:
            (x1, y1), (x2, y2) = off(*pts2(a)), off(*pts2(b))
            el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#d64545" stroke-width="1"/>')
            for X, Y in ((x1, y1), (x2, y2)):
                el.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="2" fill="#d64545"/>')
            el.append(f'<text x="{(x1 + x2) / 2 + (6 if kind == "v" else 0):.1f}" y="{(y1 + y2) / 2 + (4 if kind == "v" else -6):.1f}" '
                      f'font-size="12" fill="#d64545" text-anchor="{"start" if kind == "v" else "middle"}">{lab}</text>')
    if inset:
        prof, boxes, lab = inset
        k = 0.62
        x0, y0 = Wd - 548 * k - 30, Hd - 40 - 16 * len(notes) - 10
        P = lambda yy, zz: (x0 + yy * k, y0 - zz * k)
        el.append(f'<rect x="{x0 - 10:.0f}" y="{y0 - 150 * k - 30:.0f}" width="{548 * k + 20:.0f}" height="{150 * k + 50:.0f}" fill="#fff" stroke="#c9d1d9"/>')
        el.append(f'<text x="{x0:.0f}" y="{y0 - 150 * k - 12:.0f}" font-size="12" font-weight="700" fill="#1f2933">{lab}</text>')
        el.append('<polygon points="' + " ".join(f"{P(a, b)[0]:.1f},{P(a, b)[1]:.1f}" for a, b in prof) + '" fill="#3a3f45" fill-opacity="0.85" stroke="#1f2933"/>')
        for nm, (ya, yb, za, zb), col in boxes:
            (ax, ay), (bx, by) = P(ya, za), P(yb, zb)
            el.append(f'<rect x="{ax:.1f}" y="{by:.1f}" width="{bx - ax:.1f}" height="{ay - by:.1f}" fill="none" stroke="{col}" stroke-width="1.5" stroke-dasharray="4 2"/>')
            el.append(f'<text x="{(ax + bx) / 2:.1f}" y="{(ay + by) / 2 + 4:.1f}" font-size="10" fill="{col}" text-anchor="middle" font-weight="700">{nm}</text>')
    for i, t in enumerate(notes):
        el.append(f'<text x="20" y="{Hd - 14 - 16 * (len(notes) - 1 - i):.0f}" font-size="12" fill="#52606d">{t}</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd:.0f} {Hd:.0f}" width="{Wd:.0f}" height="{Hd:.0f}" '
           f'font-family="Segoe UI, Arial, sans-serif"><title>{title}</title>' + "".join(el) + "</svg>")
    with open(os.path.join(HERE, fname), "w", encoding="utf-8") as f:
        f.write(svg)
    return Wd, Hd


def compare():
    S = 1.35
    old = [(0, 0), (0, 22), (345, 22), (345, 56), (348, 56), (478, 131), (548, 131), (548, 0)]
    new = [(0, 0)] + [(y, z) for y, z in PROFILE[1:-1]] + [(515, 0)]
    Wd, Hd = 60 + 600 * S, 120 + 150 * S + 380
    P = lambda y, z, oy: (30 + y * S, oy + (140 - z) * S)
    el = ['<rect width="100%" height="100%" fill="#fff"/>',
          '<text x="30" y="26" font-size="16" font-weight="700" fill="#1f2933">Было → стало, один масштаб</text>']
    oy = 40
    for pts, col, fill, lab in ((old, "#8a96a3", "none", "было: губа 28 + дека 22, стенка 34, скат 30°, крыша 70; 548 × 515 × 131"),
                                (new, "#e8731a", "rgba(232,115,26,0.15)", "стало: дека 22 до передней стенки, ступенька 9, скат 33°, крыша 41; 515 × 515 × 131")):
        el.append('<polygon points="' + " ".join(f"{P(y, z, oy)[0]:.1f},{P(y, z, oy)[1]:.1f}" for y, z in pts) +
                  f'" fill="{fill}" stroke="{col}" stroke-width="2.5"' + (' stroke-dasharray="7 4"' if col == "#8a96a3" else "") + "/>")
    for i, (col, lab) in enumerate((("#8a96a3", "- - было (итоговая модель 16–17.11): 548 × 515, дека 22, стенка 34 мм, зад 131"),
                                     ("#e8731a", "— стало: 515 × 515, дека 22, ступенька 9 мм, скат 33°, зад 131"))):
        el.append(f'<text x="30" y="{oy + 150 * S + 22 + 16 * i:.0f}" font-size="12" fill="{col}">{lab}</text>')
    # plan outlines
    oy2 = oy + 150 * S + 70
    el.append(f'<text x="30" y="{oy2 - 8:.0f}" font-size="13" font-weight="700" fill="#1f2933">Сверху</text>')
    s2 = 0.55
    for (w, d, col, dash, x0) in ((515, 548, "#8a96a3", "7 4", 30), (515, 515, "#e8731a", None, 30 + 515 * s2 + 60)):
        el.append(f'<rect x="{x0}" y="{oy2}" width="{w * s2:.0f}" height="{d * s2:.0f}" rx="{(10 if col != "#8a96a3" else 0)}" fill="none" '
                  f'stroke="{col}" stroke-width="2.5"' + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")
        el.append(f'<text x="{x0 + w * s2 / 2:.0f}" y="{oy2 + d * s2 / 2:.0f}" font-size="13" fill="{col}" text-anchor="middle">{w} × {d}</text>')
        el.append(f'<text x="{x0 + w * s2 / 2:.0f}" y="{oy2 + d * s2 + 16:.0f}" font-size="11" fill="#52606d" text-anchor="middle">'
                  f'площадь {w * d / 1e3:.0f} тыс. мм²</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd:.0f} {Hd:.0f}" width="{Wd:.0f}" height="{Hd:.0f}" '
           f'font-family="Segoe UI, Arial, sans-serif"><title>Было и стало</title>' + "".join(el) + "</svg>")
    with open(os.path.join(HERE, "41_final_compare.svg"), "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    shell()
    controls()
    print("slope", round(math.degrees(SLOPE), 1))
    notes = ("Условности: скругления углов (R15–20) и кромки показаны не моделью, а светом; ручки и кнопки — простые призмы;",
             "цвета огней — по раскладке v7; картинка на экране — условная. Размеры — по модели посадки (док. 41, разд. 15–18).")
    render(cam_34(), "41_final_34.svg", "Штука Дрюка: итоговая форма, вид 3/4 (эскиз дизайнера)", 1.45, notes)
    render(cam_side(), "41_final_side.svg", "Вид слева, узлы внутри пунктиром", 1.35,
           ("Внутри: H5 вплотную к задней стенке (x 376–496), вентилятор 60 мм на правой стенке рядом, A1 над аккумулятором, F1 на полу под P1.",),
           dims=[("h", (0, 0, -12), (0, D, -12), "515"), ("v", (0, D + 8, 0), (0, D + 8, BACK), "131"),
                 ("v", (0, -10, 0), (0, -10, DECK), "22"), ("v", (0, STEP_Y - 8, DECK), (0, STEP_Y - 8, STEP_Z), "9"),
                 ("h", (0, SHELF_Y, BACK + 10), (0, D, BACK + 10), "41"),
                 ("h", (0, STEP_Y + 30, STEP_Z + 60), (0, STEP_Y + 30, STEP_Z + 60), f"{math.degrees(SLOPE):.0f}°")], inside=True)
    render(cam_top(), "41_final_top.svg", "Вид сверху, узлы внутри пунктиром", 1.2,
           ("Скат и экран показаны в проекции (укорочены на cos 33°).",),
           dims=[("h", (0, -14, 0), (W, -14, 0), "515"), ("v", (W + 10, 0, 0), (W + 10, D, 0), "515")], inside=True)
    compare()
