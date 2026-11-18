#!/usr/bin/env python3
"""Side section of the step case (git history (docs/ru/38_low_case_rework.md, deleted 18.11.2026), 3b-3d) -> step_case_section.png. Plain drawing from the numbers, not from the model."""
from PIL import Image, ImageDraw, ImageFont
import math, os
DECK, FOLD, RS = 28.0, 41.0, 60.0          # deck, fold height, shelf lengthening
BACK = FOLD + 75.0
D = 460.0 + RS                               # rear wall y
S, K = 2, 1.08
im = Image.new("RGB", (680 * S, 430 * S), "white"); d = ImageDraw.Draw(im)
Fnt = lambda n: ImageFont.truetype("C:/Windows/Fonts/arial.ttf", n * S)
f12, f14 = Fnt(12), Fnt(14)
X = lambda y: 40 + K * (y + 28)
Z = lambda z: 300 - K * z
P = lambda pts: [(x * S, y * S) for x, y in pts]
def rect(y0, y1, z0, z1, fill, out="#333"): d.rectangle([X(y0) * S, Z(z1) * S, X(y1) * S, Z(z0) * S], fill=fill, outline=out, width=S)
def text(x, y, t, f=f12, c="#222"): d.text((x * S, y * S), t, font=f, fill=c)
def line(a, b, c="#666", w=1): d.line(P([a, b]), fill=c, width=int(w * S))
def dash(pts, c="#222"):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = int(max(abs(x1 - x0), abs(y1 - y0)) / 6) + 1
        for i in range(0, n, 2):
            line((x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n), (x0 + (x1 - x0) * min(i + 1, n) / n, y0 + (y1 - y0) * min(i + 1, n) / n), c, 1)
shell = [(X(-28), Z(0)), (X(-28), Z(DECK)), (X(300), Z(DECK)), (X(300), Z(FOLD)), (X(430), Z(BACK)), (X(D), Z(BACK)), (X(D), Z(0))]
d.polygon(P(shell), fill="#efece4", outline="#555")
dash([(X(0), Z(0)), (X(0), Z(68)), (X(300), Z(68)), (X(430), Z(143)), (X(457), Z(143)), (X(457), Z(0))])
a = math.atan2(BACK - FOLD, 130); nx, ny = math.sin(a) * 8, math.cos(a) * 8      # inward normal 8 px
line((X(300) + nx, Z(FOLD) + ny), (X(430) + nx, Z(BACK) + ny), "#1D9E75", 8)
rect(4, 262, 16.9, 18.5, "#3f8f5a")
rect(60, 160, 3, 15, "#EF9F27")
rect(-25, 0, 7.6, 23.3, "#F0997B"); rect(-27, 8, 6, 7.6, "#3f8f5a")
h0, h1 = D - 0.9 - 120 - 0.0 - 0.0 - 0, D - 0.9 - 0.0
h0, h1 = 413.4 + RS - 0.9 - 120, 413.4 + RS - 0.9
rect(h0, h1, 6, 50, "#AFA9EC", "#4b3fb0"); text((X(h0) + X(h1)) / 2 - 8, Z(28) - 7, "H5", f14, "#26215C")
rect(413.4 + RS, 415 + RS, 10, 113, "#3f8f5a", "#1f5c35")
text(X(0) + 8, Z(68) - 16, "прежний контур 68 / 143 мм")
text(X(60), Z(DECK) - 52, "дека 28 мм (было 68)"); line((X(90), Z(DECK) - 38), (X(90), Z(DECK) - 2))
text(X(180), Z(FOLD) - 70, "ступенька до %d мм (было 68)" % FOLD); line((X(298), Z(FOLD) - 52), (X(300), Z(FOLD) - 6))
text(X(250), Z(BACK) - 20, "экран и скат ниже на %d мм (зад %d вместо 143)" % (68 - FOLD, BACK)); line((X(375), Z(BACK) - 6), (X(375), Z(BACK) + 34))
text(X(445), Z(BACK) - 44, "полка +%d мм" % RS); line((X(470), Z(BACK) - 30), (X(470), Z(BACK) - 4))
text(X(30), 332, "аккумулятор LiPo 12 мм под пэдами"); line((X(110), Z(15) + 4), (X(110), 326))
text(X(h0) - 40, 332, "H5 вплотную к R1 / R2, порты внутрь"); line(((X(h0) + X(h1)) / 2, Z(6) + 4), ((X(h0) + X(h1)) / 2, 326))
text(40, 362, "гнёзда 6,35 мм в губе +28 мм"); line((X(-14), Z(7.6) + 4), (X(-14), 356))
text(X(300), 362, "R1, R2 и задняя стенка назад на %d мм" % RS); line((X(414 + RS), Z(10) + 4), (X(414 + RS), 356))
text(40, 396, "Вид сбоку: слева перед. Пунктир — прежний корпус. Глубина %d мм (было 460). A1 и PW рядом с H5 по ширине, не показаны." % (28 + D), f12, "#555")
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "step_case_section.png"))
