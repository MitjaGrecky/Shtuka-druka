#!/usr/bin/env python3
"""General-arrangement drawing of the device from the fit model (fit_model.parts()): SVG + PNG.

  python model3d/fit/make_drawing.py            -> model3d/fit/drawing.svg, drawing.png

Views (millimetres, one scale): panel from above, inside from above (no skin, no panel parts), left side,
front. Every box of the model is projected (its 8 corners, convex hull), so the slope parts come out right.
The same environment variables as fit_model.py choose the variant (FRONT_Z, COMPUTER, F1_MODE, ...).
License: AGPL-3.0-or-later.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fit_model as F  # noqa: E402

COL = {"shell": ("#e9e5dc", "#8a857a"), "pcb": ("#3f8f5a", "#1f5c35"), "parts": ("#b9c4bb", "#7c877e"),
       "metal": ("#a7adb5", "#5d636b"), "knob": ("#3b3f46", "#1c1f24"), "plastic": ("#d9dde3", "#7d838c"),
       "battery": ("#e8a33d", "#9a6516"), "chip": ("#2b2b2b", "#111"), "led": ("#f4d03f", "#a88d14"),
       "glass": ("#bcd7ea", "#5a86a6"), "lcd": ("#27323d", "#10161c"), "grey": ("#c8c8c8", "#777")}
S = 1.0          # px per mm in the SVG (the PNG is rendered larger)


def corners(b):
    out = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                p = [b.c[i] + sx * b.h[0] * b.ax[0][i] + sy * b.h[1] * b.ax[1][i] + sz * b.h[2] * b.ax[2][i] for i in range(3)]
                out.append(p)
    return out


def hull(pts):
    pts = sorted(set((round(x, 3), round(y, 3)) for x, y in pts))
    if len(pts) < 3:
        return pts

    def half(seq):
        h = []
        for p in seq:
            while len(h) >= 2 and (h[-1][0] - h[-2][0]) * (p[1] - h[-2][1]) - (h[-1][1] - h[-2][1]) * (p[0] - h[-2][0]) <= 0:
                h.pop()
            h.append(p)
        return h
    lo, up = half(pts), half(reversed(pts))
    return lo[:-1] + up[:-1]


class View:
    def __init__(self, title, ox, oy, proj, sx=1, sy=-1):
        self.title, self.ox, self.oy, self.proj, self.sx, self.sy = title, ox, oy, proj, sx, sy
        self.out = []

    def pt(self, u, v):
        return self.ox + self.sx * u * S, self.oy + self.sy * v * S

    def poly(self, b, opacity=1.0, outline_only=False):
        pts = hull([self.proj(p) for p in corners(b)])
        if len(pts) < 3:
            return
        fill, stroke = COL.get(b.color, COL["grey"])
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in (self.pt(u, v) for u, v in pts))
        f = "none" if outline_only else fill
        self.out.append(f'<polygon points="{d}" fill="{f}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="0.35"/>')

    def text(self, u, v, s, size=7, anchor="middle", color="#222", weight="normal"):
        x, y = self.pt(u, v)
        self.out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{color}" '
                        f'font-weight="{weight}" font-family="Arial, sans-serif">{s}</text>')

    def dim(self, u0, v0, u1, v1, off, label, vertical=False):
        """Dimension line between two points, shifted by off (mm) to the side."""
        if vertical:
            a, b = self.pt(u0 + off, v0), self.pt(u1 + off, v1)
            e0, e1 = self.pt(u0, v0), self.pt(u1, v1)
        else:
            a, b = self.pt(u0, v0 + off), self.pt(u1, v1 + off)
            e0, e1 = self.pt(u0, v0), self.pt(u1, v1)
        c = "#c0392b"
        self.out.append(f'<line x1="{e0[0]:.1f}" y1="{e0[1]:.1f}" x2="{a[0]:.1f}" y2="{a[1]:.1f}" stroke="{c}" stroke-width="0.3"/>')
        self.out.append(f'<line x1="{e1[0]:.1f}" y1="{e1[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{c}" stroke-width="0.3"/>')
        self.out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{c}" stroke-width="0.4" '
                        'marker-start="url(#ar)" marker-end="url(#ar)"/>')
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        if vertical:
            self.out.append(f'<text x="{mx - 2:.1f}" y="{my:.1f}" font-size="7" fill="{c}" text-anchor="middle" '
                            f'font-family="Arial, sans-serif" transform="rotate(-90 {mx - 2:.1f} {my:.1f})">{label}</text>')
        else:
            self.out.append(f'<text x="{mx:.1f}" y="{my - 2:.1f}" font-size="7" fill="{c}" text-anchor="middle" '
                            f'font-family="Arial, sans-serif">{label}</text>')

    def header(self, u, v):
        self.text(u, v, self.title, size=10, anchor="start", weight="bold")


def main():
    P = F.parts()
    FLv = getattr(F, "FL", 0.0)               # front lip: the case starts at y = -FL
    W, D, TZ, BZ = F.W, F.D + FLv, F.TOP_Z, F.BACK_Z
    FY, SY = F.FOLD_Y + FLv, F.SHELF_Y + FLv
    shell = [b for b in P if b.group == "shell"]
    inner = [b for b in P if b.group not in ("shell", "top", "m1led")]
    top = [b for b in P if b.group in ("top", "m1led")]
    order = lambda bs: sorted(bs, key=lambda b: b.c[2] - b.h[2])     # low first

    M = 40                                   # margin
    views = []
    # 1. panel from above (front edge at the bottom)
    v1 = View("Вид сверху: панель", M, M + D, lambda p: (p[0], p[1] + FLv))
    for b in shell:
        if b.name.startswith(("Top skin", "Slope skin", "Shelf")):
            v1.poly(b, 1.0)
    for b in P:
        if b.name == "Screen glass":
            v1.poly(b)
    for b in order(top):
        v1.poly(b)
    v1.dim(0, 0, W, 0, -14, f"{W:g}")
    v1.dim(0, 0, 0, D, -14, f"{D:g}", vertical=True)
    v1.dim(W, 0, W, FY, 12, f"{FY:g} (до ската)", vertical=True)
    v1.dim(W, FY, W, SY, 12, f"{SY - FY:g}", vertical=True)
    v1.dim(W, SY, W, D, 12, f"{D - SY:g}", vertical=True)
    v1.text(W / 2, -26, "перед (к музыканту)", size=8, color="#555")
    v1.header(0, D + 10)
    views.append(v1)

    # 2. inside from above
    ox2 = M + W + 70
    v2 = View("Вид сверху без обшивки: платы и узлы", ox2, M + D, lambda p: (p[0], p[1] + FLv))
    for b in shell:
        if b.name.startswith(("Floor",)):
            v2.poly(b, 1.0)
        elif b.name.startswith(("Front wall", "Rear wall", "Side")):
            v2.poly(b, 1.0)
    for b in order(inner):
        if b.group == "screen" and b.name in ("Screen glass", "Screen LCM + back"):
            v2.poly(b, outline_only=True)            # the screen would hide everything under the slope
        else:
            v2.poly(b, 0.55 if b.color in ("pcb", "parts") else 0.9)
    labels = {"P1 Left": "P1", "P2 Grid": "P2 Grid", "P3 Tracks": "P3", "P4 Right": "P4", "M1 board": "M1",
              "Mini-ITX board": "ODROID-H5", "A1 audio board": "A1", "PW power": "PW", "Battery bay": "АКБ",
              "R1 audio rear board": "R1", "R2 control rear board": "R2", "F1 headphone board": "F1", "Battery pack 1": "АКБ 1", "Battery pack 2": "АКБ 2"}
    for b in P:
        if b.name in labels:
            dy = {"P2 Grid": 40, "Mini-ITX board": -10}.get(b.name, -3)
            v2.text(b.c[0], b.c[1] + FLv + dy, labels[b.name], size=9, weight="bold", color="#0b3d1f")
        elif b.name.startswith(("W1", "W2", "W3")) and "board" in b.name.lower():
            v2.text(b.c[0], b.c[1] + FLv - 3, b.name.split()[0], size=9, weight="bold", color="#0b3d1f")
        elif b.name.startswith("Fan "):
            v2.text(b.c[0] - 14, b.c[1] + FLv, "вент.", size=8, weight="bold", color="#333", anchor="end")
        elif b.name.startswith("Screen glass"):
            v2.text(b.c[0], b.c[1] + FLv + 55, "контур экрана 10.1\"", size=8, color="#345")
    v2.dim(0, 0, W, 0, -14, f"{W:g}")
    v2.header(0, D + 10)
    views.append(v2)

    # 3. left side (front at the left), z up
    oy3 = M + D + 70 + BZ
    v3 = View("Вид слева (все узлы насквозь)", M, oy3, lambda p: (p[1] + FLv, p[2]))
    for b in shell:
        v3.poly(b, 0.35)
    for b in order(inner + top):
        v3.poly(b, 0.6)
    v3.dim(0, 0, 0, TZ, -12, f"{TZ:g}", vertical=True)
    v3.dim(D, 0, D, BZ, 12, f"{BZ:g}", vertical=True)
    v3.dim(0, 0, D, 0, -14, f"{D:g}")
    if F.FOLD_Z > TZ + 0.01:
        v3.dim(FY, 0, FY, F.FOLD_Z, -6, f"ступенька {F.FOLD_Z:g}", vertical=True)
    v3.dim(FY, BZ, SY, BZ, 10, f"скат {math.degrees(F.SLOPE):.0f}°, {F.SLOPE_LEN:.0f}")
    v3.header(0, BZ + 28)
    views.append(v3)

    # 4. front, z up
    v4 = View("Вид спереди (все узлы насквозь)", ox2, oy3, lambda p: (p[0], p[2]))
    for b in shell:
        v4.poly(b, 0.35)
    for b in order(inner + top):
        v4.poly(b, 0.6)
    v4.dim(0, 0, W, 0, -14, f"{W:g}")
    v4.dim(W, 0, W, BZ, 12, f"{BZ:g}", vertical=True)
    v4.dim(0, 0, 0, TZ, -12, f"{TZ:g}", vertical=True)
    v4.header(0, BZ + 28)
    views.append(v4)

    width = ox2 + W + 50
    height = oy3 + 60
    notes = [f"«Штука Дрюка» — общий вид, мм. Собран из model3d/fit/fit_model.py ({'H5 под P2' if F.COMPUTER == 'H5' else F.COMPUTER}, "
             f"экран EP, повёрнут {F.SCREEN_ROT}°, высота спереди {TZ:g}, у сгиба {F.FOLD_Z:g}, сзади {BZ:g}).",
             "Платы — реальные контуры из генераторов; объёмы деталей под платами и задние гнёзда — оценка (огибающие). "
             "Не для изготовления корпуса.",
             f"Вариант задаётся переменными окружения fit_model.py (FRONT_Z, COMPUTER, F1_MODE …). 16.11.2026."]
    body = []
    for v in views:
        body += v.out
    for i, s in enumerate(notes):
        body.append(f'<text x="{M}" y="{height - 34 + 11 * i}" font-size="8" fill="#444" font-family="Arial, sans-serif">{s}</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
           f'viewBox="0 0 {width:.0f} {height:.0f}">'
           '<defs><marker id="ar" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto-start-reverse">'
           '<path d="M0,0 L6,3 L0,6 z" fill="#c0392b"/></marker></defs>'
           f'<rect width="100%" height="100%" fill="#ffffff"/>' + "".join(body) + "</svg>")
    out = os.path.join(HERE, os.environ.get("DRAWING_NAME", "drawing") + ".svg")
    open(out, "w", encoding="utf-8").write(svg)
    print("svg:", out, f"{width:.0f} x {height:.0f}")
    try:
        import fitz
        doc = fitz.open(out)
        pix = doc[0].get_pixmap(matrix=fitz.Matrix(3, 3))
        png = out[:-4] + ".png"
        pix.save(png)
        pdf = fitz.open("pdf", doc.convert_to_pdf())
        pdf.save(out[:-4] + ".pdf")
        print("png/pdf:", png)
    except Exception as e:  # noqa: BLE001
        print("no PNG:", e)


if __name__ == "__main__":
    main()
