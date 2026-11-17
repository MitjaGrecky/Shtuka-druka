#!/usr/bin/env python3
"""Sketches for docs/ru/41_design_review.md: side profiles of the current low case and three silhouettes.
Numbers: docs/ru/39_low_case_plan.md, model3d/fit/low_case_final.py (deck 22, lip 28, fold 56, rear 131, riser y 317-320, depth 548).
x = distance from the front edge of the lip, mm (model y + 28); z = height above the outer floor, mm (feet not included).
Run: python 41_make_sketches.py   (plain python, writes SVG next to itself)."""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
S = 1.45                      # px per mm
INK, PANEL, CHEEK, ACC, GRID = "#1f2933", "#3b4652", "#9a6a43", "#d64545", "#c9d1d9"

# ---- geometry, mm ----
DECK, FOLD_X, FOLD_Z, SLOPE_RUN, ROOF_Z, DEPTH = 22.0, 348.0, 56.0, 130.0, 131.0, 548.0
WALL_X0 = 345.0               # riser wall 317..320 in model y
SLOPE_END = FOLD_X + SLOPE_RUN
ANG = math.degrees(math.atan2(ROOF_Z - FOLD_Z, SLOPE_RUN))


def rounded(pts, radii):
    """Closed path through pts with a quadratic round at each vertex (radius in mm)."""
    n = len(pts)
    segs = []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        r = radii[i]
        def toward(a, b, d):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            d = min(d, L / 2)
            return (a[0] + (b[0] - a[0]) * d / L, a[1] + (b[1] - a[1]) * d / L)
        segs.append((toward(p1, p0, r), p1, toward(p1, p2, r)))
    d = ""
    for i, (a, c, b) in enumerate(segs):
        d += ("M" if i == 0 else "L") + f"{a[0]:.1f},{a[1]:.1f} Q{c[0]:.1f},{c[1]:.1f} {b[0]:.1f},{b[1]:.1f} "
    return d + "Z"


class Sheet:
    def __init__(self, w_mm, h_mm, ox=60, oy=30):
        self.w, self.h, self.ox, self.oy = w_mm, h_mm, ox, oy
        self.body = []

    def P(self, x, z):                       # model -> px (z up)
        return (self.ox + x * S, self.oy + (self.h - z) * S)

    def add(self, s):
        self.body.append(s)

    def poly(self, pts, radii=None, fill="none", stroke=INK, sw=2, dash=None, op=1):
        pp = [self.P(*p) for p in pts]
        r = [(radii[i] if radii else 0) * S for i in range(len(pts))]
        d = rounded(pp, r)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<path d="{d}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"{da} stroke-linejoin="round"/>')

    def line(self, a, b, stroke=INK, sw=1.2, dash=None, arrow=False):
        (x1, y1), (x2, y2) = self.P(*a), self.P(*b)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        m = ' marker-end="url(#ah)"' if arrow else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{da}{m}/>')

    def text(self, x, z, t, size=12, fill=INK, anchor="start", bold=False, px=False):
        X, Y = (x, z) if px else self.P(x, z)
        wgt = ' font-weight="700"' if bold else ""
        self.add(f'<text x="{X:.1f}" y="{Y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{wgt}>{t}</text>')

    def dim(self, x1, x2, z, label, col=ACC):
        self.line((x1, z), (x2, z), col, 1)
        for x in (x1, x2):
            self.line((x, z - 3), (x, z + 3), col, 1)
        self.text((x1 + x2) / 2, z + 6, label, 11, col, "middle")

    def circle(self, x, z, r_mm, fill="none", stroke=INK, sw=1.5):
        X, Y = self.P(x, z)
        self.add(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r_mm * S:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def save(self, name, title):
        W = self.ox * 2 + self.w * S
        H = self.oy * 2 + self.h * S + 60
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" '
               f'font-family="Segoe UI, Arial, sans-serif"><title>{title}</title>'
               f'<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{ACC}"/></marker></defs>'
               f'<rect width="100%" height="100%" fill="#ffffff"/>' + "".join(self.body) + "</svg>")
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
            f.write(svg)


def table(sh, x0=-60, x1=DEPTH + 40):
    sh.line((x0, 0), (x1, 0), INK, 3)
    sh.text(x0, -10, "стол", 11, "#6b7785")


def current_pts():
    return [(0, 0), (0, DECK), (WALL_X0, DECK), (WALL_X0, FOLD_Z), (FOLD_X, FOLD_Z), (SLOPE_END, ROOF_Z), (DEPTH, ROOF_Z), (DEPTH, 0)]


# ------------------------------------------------------------------ 1. anatomy of the "printer"
def anatomy():
    sh = Sheet(DEPTH + 40, 175, 90, 40)
    table(sh)
    sh.poly(current_pts(), [4, 2, 0, 0, 0, 0, 0, 0], "#e3e7eb", INK, 2.2)
    sh.text(0, 165, "Сейчас (итоговая модель, док. 39): сбоку профиль «Z»", 14, INK, bold=True)
    sh.text(0, 150, "плоская плита, ступенька, скат-крышка, плоская «крыша», вертикальный зад — как у принтера / сканера", 11, "#52606d")
    sh.dim(0, 345, -22, "дека 22 мм × 345 мм = 1 : 15,7")
    sh.line((WALL_X0 - 6, 22), (WALL_X0 - 6, 56), ACC, 1.2)
    sh.text(WALL_X0 - 12, 36, "стенка 34 мм, 90°", 11, ACC, "end")
    sh.text(FOLD_X + 60, 112, f"скат {ANG:.0f}°, 130 мм в плане", 11, ACC, "end")
    sh.dim(SLOPE_END, DEPTH, ROOF_Z + 12, "«крыша» 70 мм")
    sh.line((DEPTH + 8, 0), (DEPTH + 8, ROOF_Z), ACC, 1.2)
    sh.text(DEPTH + 12, 70, "зад", 11, ACC)
    sh.text(DEPTH + 12, 58, "131 мм,", 11, ACC)
    sh.text(DEPTH + 12, 46, "вертикаль", 11, ACC)
    sh.dim(0, 28, 36, "губа 28", "#6b7785")
    sh.line((0, 14), (-45, 14), "#6b7785", 3)
    sh.text(-45, 24, "штекер 6,35 мм торчит вперёд", 10, "#52606d")
    sh.save("41_printer_anatomy.svg", "Профиль текущего корпуса")


# ------------------------------------------------------------------ 2. three silhouettes
def cheek_curve(n=60):
    """Cheek top line: from (0,22) rising smoothly, always above the current profile, ends on the roof."""
    pts = []
    p0, p1, p2, p3 = (0, 24), (300, 24), (330, 131), (DEPTH, 131)
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
        z = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
        pts.append((x, z))
    return pts


def silhouettes():
    ROW = 205
    sh = Sheet(DEPTH + 60, ROW * 4, 50, 20)

    def base(row, title, sub):
        z0 = (3 - row) * ROW                      # row 0 at the top
        sh.line((-50, z0), (DEPTH + 40, z0), INK, 3)
        sh.text(0, z0 + 180, title, 14, INK, bold=True)
        sh.text(0, z0 + 165, sub, 11, "#52606d")
        return z0

    # reference: current profile as a ghost in every row
    def ghost(z0):
        sh.poly([(x, z + z0) for x, z in current_pts()], None, "none", "#aab4bf", 1, "4 3")

    # A: chamfer instead of the wall
    z0 = base(0, "A. «Скос»: то же тело, ступенька → скос 60°, скругления, тонкая кромка", "минимум: платы, модель, R152–R173 не трогаем")
    ghost(z0)
    A = [(0, 0), (0, DECK), (328, DECK), (FOLD_X, FOLD_Z), (SLOPE_END, ROOF_Z), (DEPTH, ROOF_Z), (DEPTH, 0)]
    sh.poly([(x, z + z0) for x, z in A], [6, 7, 22, 40, 40, 14, 4], PANEL, INK, 2.2, None, 0.92)
    sh.text(250, z0 + 62, "скос ≈ 60° вместо стенки", 11, ACC, "end")
    sh.line((250, z0 + 58), (336, z0 + 38), ACC, 1, arrow=True)

    # B: soft wedge, no riser
    z0 = base(1, "B. «Мягкий клин»: дека наклонена 5,6°, ступеньки нет, гладкий переход в скат", "дека 22 мм только у губы; у сгиба 56; платы под панелью тоже наклонены")
    ghost(z0)
    Bp = [(0, 0), (0, DECK), (FOLD_X, FOLD_Z), (SLOPE_END, ROOF_Z), (DEPTH, ROOF_Z), (DEPTH, 0)]
    sh.poly([(x, z + z0) for x, z in Bp], [5, 4, 95, 45, 14, 4], PANEL, INK, 2.2, None, 0.92)
    tilt = math.degrees(math.atan2(FOLD_Z - DECK, FOLD_X))
    sh.text(180, z0 + 17, f"наклон {tilt:.1f}°: от 22 мм (губа) до 56 мм (у сгиба)", 11, ACC, "middle")
    sh.line((120, z0 + 26), (130, z0 + 22 + 34 * 130 / 348 + 2), ACC, 0.01)

    # C: cheeks
    z0 = base(2, "C. «Щёки»: внутри как A, снаружи боковые щёки одной плавной линией", "платы и R152–R173 не трогаем; ширина +36 мм (≈ 551); щёки — дерево или цвет")
    ghost(z0)
    sh.poly([(x, z + z0) for x, z in A], [6, 7, 22, 40, 40, 14, 4], PANEL, INK, 1.5, None, 0.9)
    cc = cheek_curve()
    cheek = [(0, 0)] + [(x, z) for x, z in cc] + [(DEPTH, 0)]
    cheek = [(x, z + z0) for x, z in cheek]
    sh.poly(cheek, [2] + [0] * len(cc) + [4], CHEEK, INK, 2.2, None, 0.88)
    sh.text(60, z0 + 92, "боковая щека (вид сбоку): одна плавная линия", 11, CHEEK, "start", True)
    sh.line((120, z0 + 88), (200, z0 + 52), CHEEK, 1.2, None, True)

    # reference row
    z0 = base(3, "Для сравнения: сейчас", "«Z»: плита 22 → стенка 34 → скат → крыша → вертикальный зад")
    sh.poly([(x, z + z0) for x, z in current_pts()], [4, 2, 0, 0, 0, 0, 0, 0], "#c9d1d9", INK, 2.2)
    sh.save("41_silhouettes.svg", "Три силуэта корпуса: сбоку")
    return tilt


# ------------------------------------------------------------------ 3. ergonomics sheet
def ergonomics():
    sh = Sheet(DEPTH + 120, 300, 100, 30)
    table(sh, -100, DEPTH + 60)
    sh.poly(current_pts(), [4, 2, 0, 0, 0, 0, 0, 0], "#e3e7eb", INK, 2.0)
    sh.text(-40, 288, "Эргономика текущего корпуса (дальше — проверить на макете 1:1, R43)", 14, INK, bold=True)
    # hand zones in x from front edge (layout y + 28)
    zones = [(80, 276, "пэды 8 × 8\n80–276 мм", "#1d7a5a"), (294, 316, "ручки M1", "#b7791f"), (286, 324, "колесо", "#6b46c1")]
    sh.dim(80, 276, -22, "пэды: 80–276 мм от края", "#1d7a5a")
    sh.dim(294, 316, -40, "ручки 294–316", "#b7791f")
    sh.dim(286, 324, -58, "колесо 286–324", "#6b46c1")
    sh.dim(316, 345, 70, "29 мм до стенки", ACC)
    sh.dim(324, 345, 85, "21 мм (колесо)", ACC)
    # wrist: on the lip
    sh.circle(-2, 30, 16, "#fbe8d3", "#a0763c", 1.2)
    sh.text(-2, 54, "запястье на губе", 11, "#a0763c", "middle")
    # forearm
    sh.line((-95, 80), (-2, 36), "#a0763c", 6)
    # sight line and glare, units: screen centre
    cx, cz = FOLD_X + 65 + 3, FOLD_Z + 37.5
    # eye 300 mm in front of the edge, 430 mm over the table -> direction from the screen to the eye
    ex, ez = -300.0, 430.0
    dx, dz = ex - cx, ez - cz
    el = math.degrees(math.atan2(dz, -dx))
    dist = math.hypot(dx, dz)
    # normal of the slope surface, pointing to the user
    nx, nz = -math.sin(math.radians(ANG)), math.cos(math.radians(ANG))
    nel = math.degrees(math.atan2(nz, -nx))
    off = nel - el
    L = 190
    ux, uz = dx / dist, dz / dist
    sh.line((cx, cz), (cx + ux * L, cz + uz * L), "#2b6cb0", 1.5, "6 3", True)
    sh.text(cx + ux * L - 8, cz + uz * L - 12, f"к глазам: {el:.0f}° над горизонтом", 11, "#2b6cb0", "end")
    sh.line((cx, cz), (cx + nx * 80, cz + nz * 80), "#2f855a", 1.5, None, True)
    sh.text(cx + nx * 80 - 6, cz + nz * 80 + 6, f"нормаль экрана {nel:.0f}°", 11, "#2f855a", "end")
    # glare: overhead light straight down, mirrored about the normal
    sh.line((cx, cz + 90), (cx, cz), "#b7791f", 1.3, "2 2", True)
    rx = -(0 - 2 * (-nz) * nx)                 # reflected direction r = d - 2(d.n)n, d = (0,-1)
    dn = -nz
    rx, rz = 0 - 2 * dn * nx, -1 - 2 * dn * nz
    rel = math.degrees(math.atan2(rz, -rx))
    sh.line((cx, cz), (cx + rx * 200, cz + rz * 200), "#b7791f", 1.8, None, True)
    sh.text(cx + 8, cz + 92, "лампа над головой", 11, "#b7791f")
    sh.text(cx + rx * 200 - 10, cz + rz * 200 + 12, f"блик уходит под {rel:.0f}° — почти в глаза ({el:.0f}°)", 11, "#b7791f", "end")
    sh.save("41_ergonomics.svg", "Эргономика текущего корпуса")
    return dict(eye_elev=el, dist=dist, normal_elev=nel, off_axis=off, glare_elev=rel)



# ------------------------------------------------------------------ 4. analogues: side silhouettes in one scale
ANALOGS = [  # name, depth mm, height mm, note (max height from retail / maker specs, 17.11.2026 web search; see doc 41 section 10)
    ("Ableton Move", 146.3, 34, ""),
    ("Push 3 (standalone)", 318, 44.5, "29–44,5: источники расходятся"),
    ("Maschine MK3", 301, 41, ""),
    ("MPC Live II", 243.8, 45.7, ""),
    ("Maschine+", 301, 51, ""),
    ("MPC One", 272, 53, ""),
    ("Roland MC-707", 263, 60, ""),
    ("Digitakt II / Syntakt", 176, 63, ""),
    ("Octatrack MKII", 184, 63, ""),
    ("SP-404 MKII", 275.8, 70.5, ""),
    ("Akai Force", 389, 72.5, ""),
    ("MPC X (экран лёжа)", 424, 86, "с поднятым экраном 214"),
]


def analogs():
    X0, SC, GAP = 215, 0.95, 24
    W = X0 + 548 * SC + 40
    out = ['<title>Аналоги: боковые силуэты в одном масштабе</title><rect width="100%" height="100%" fill="#ffffff"/>',
           '<text x="20" y="28" font-size="15" font-weight="700" fill="#1f2933">Аналоги и Штука Дрюка: вид сбоку, один масштаб (глубина × высота, мм)</text>',
           '<text x="20" y="46" font-size="11" fill="#52606d">Аналоги — габариты из спецификаций магазинов и производителей (максимальная высота, форма условная). Штука — из модели.</text>']
    y = 62

    def label(yb, h, name, dh):
        ym = yb - h * SC / 2
        out.append(f'<text x="{X0 - 10}" y="{ym - 1:.0f}" font-size="12" fill="#1f2933" text-anchor="end">{name}</text>')
        out.append(f'<text x="{X0 - 10}" y="{ym + 12:.0f}" font-size="10" fill="#6b7785" text-anchor="end">{dh}</text>')

    for name, d, h, note in ANALOGS:
        yb = y + h * SC
        out.append(f'<rect x="{X0}" y="{y:.1f}" width="{d * SC:.1f}" height="{h * SC:.1f}" rx="3" fill="#c9d1d9" stroke="#1f2933" stroke-width="1.5"/>')
        label(yb, h, name, f"{d:g} × {h:g}" + (f" ({note})" if note else ""))
        y = yb + GAP * 0.6
    y += 14
    ours = [("Штука: первый вариант (R44)", 460, [(0, 68), (300, 68), (430, 143), (460, 143)], "68 / 143"),
            ("Штука: версия со скриншотов", 548, [(0, 28), (297, 28), (297, 41), (367, 41), (497, 116), (548, 116)], "28 / 41 / 116"),
            ("Штука: итог сейчас", 548, [(0, 22), (345, 22), (345, 56), (348, 56), (478, 131), (548, 131)], "22 / 56 / 131")]
    for name, d, prof, dh in ours:
        hmax = max(z for _, z in prof)
        yb = y + hmax * SC
        pts = [(X0, yb)] + [(X0 + x * SC, yb - z * SC) for x, z in prof] + [(X0 + d * SC, yb)]
        out.append('<polygon points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) + '" fill="#f5c6c6" stroke="#d64545" stroke-width="2"/>')
        label(yb, 40, name, f"{d} × {dh}")
        y = yb + GAP
    H = y + 6
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" '
           f'font-family="Segoe UI, Arial, sans-serif">' + "".join(out) + "</svg>")
    with open(os.path.join(HERE, "41_analogs.svg"), "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    anatomy()
    t = silhouettes()
    e = ergonomics()
    analogs()
    print("tilt B, deg:", round(t, 2))
    print({k: round(v, 1) for k, v in e.items()})
    # knee blend for B: radius 100 mm tangent length
    d = math.radians(ANG - t)
    for r in (100, 150, 200):
        print("B knee R", r, "tangent", round(r * math.tan(d / 2), 1), "mm, drop", round(r * (1 / math.cos(d / 2) - 1), 1))
    # B heights at the controls (x = layout y + 28)
    for name, y in (("pad row 1 front", 52), ("pad row 8 back", 248), ("knob row", 277), ("wheel", 277)):
        x = y + 28
        print(name, "x", x, "deck z", round(DECK + (FOLD_Z - DECK) * x / FOLD_X, 1))
    print("tilt volume gain, L:", round(0.5 * 348 * 34 * 515 / 1e6, 2))
