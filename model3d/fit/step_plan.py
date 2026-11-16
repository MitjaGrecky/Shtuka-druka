#!/usr/bin/env python3
"""Plan view (from above) of the step case -> step_case_plan.png. Plain drawing from the numbers of docs/ru/38_low_case_rework.md 3b-3g."""
from PIL import Image, ImageDraw, ImageFont
import os
S = 2
im = Image.new("RGB", (680 * S, 700 * S), "white"); d = ImageDraw.Draw(im)
F = lambda n: ImageFont.truetype("C:/Windows/Fonts/arial.ttf", n * S)
f11, f12, f14 = F(11), F(12), F(14)
K = 1.08
X = lambda x: 40 + K * x
Y = lambda y: 60 + K * (480 - y)
def rect(x0, y0, x1, y1, fill=None, out="#444", w=1):
    d.rectangle([X(x0) * S, Y(y1) * S, X(x1) * S, Y(y0) * S], fill=fill, outline=out, width=w * S)
def text(x, y, t, f=f12, c="#222", anchor="la"): d.text((x * S, y * S), t, font=f, fill=c, anchor=anchor)
def label(x0, x1, y0, y1, t, f=f11, c="#222"):
    text((X(x0) + X(x1)) / 2, (Y(y0) + Y(y1)) / 2, t, f, c, "mm")
rect(0, -28, 515, 480, "#f4f1ea", "#555", 2)
rect(0, 430, 515, 480, "#e6e2d8", "#aaa")
rect(0, -28, 515, 0, "#fbe3d9", "#d97a55")
rect(4, 4, 102, 291, None, "#7aa38a"); rect(110, 4, 334, 262, None, "#3f8f5a", 2); rect(339, 4, 405, 291, None, "#7aa38a"); rect(413, 4, 505, 291, None, "#7aa38a")
rect(108, 263, 333, 297, "#d6e8dc", "#3f8f5a")
rect(130, 60, 300, 160, "#f7c775", "#a8741a")
rect(20, 325, 240, 425, "#bfe3d4", "#2f7d63"); rect(245, 340, 345, 420, "#d8e2f0", "#5a73a0")
rect(350, 312.5, 470, 432.5, "#b9b2ef", "#4b3fb0", 2)
rect(470, 312.5, 495, 432.5, "#e4e1fa", "#4b3fb0")
rect(292, 343, 327, 407, "#f5b9a2", "#d9603a")
rect(4, 433.4, 242, 435, "#3f8f5a", "#1f5c35"); rect(252, 433.4, 359, 435, "#3f8f5a", "#1f5c35"); rect(359, 433.4, 427, 435, "#3f8f5a", "#1f5c35")
rect(5, 436, 510, 477, None, "#aaa")
d.line([X(0) * S, Y(300) * S, X(515) * S, Y(300) * S], fill="#222", width=3 * S)
rect(20, -24, 100, 0, "#e9906c", "#a8431d"); 
label(0, 515, -28, 0, "губа +28 мм: гнёзда 6,35 мм, F1", f12, "#7a2d10")
label(110, 334, 160, 262, "P2 Grid (пэды), под ней аккумулятор", f12, "#1f5c35")
label(130, 300, 60, 160, "аккумулятор LiPo 170×100×12", f11, "#6b4608")
label(108, 333, 263, 297, "M1: ручки экрана", f11, "#1f5c35")
label(350, 470, 312.5, 432.5, "ODROID-H5 120 × 120\nвплотную к R1/R2", f12, "#26215C")
label(470, 495, 312.5, 432.5, "порты", f11, "#26215C")
label(20, 240, 325, 425, "A1 аудио", f12, "#0b4a38"); label(245, 345, 340, 420, "PW", f12, "#2b3f66")
label(292, 327, 343, 407, "кабели\nэкрана", f11, "#7a2d10")
label(4, 427, 433.4, 435, "R1 / R2", f11, "#fff")
label(0, 515, 436, 477, "гнёзда у задней стенки (+20 мм полки)", f11, "#555")
text(X(515) + 6, Y(300), "← сгиб, ступенька", f11, "#222", "lm")
text(X(515) + 6, Y(430), "← конец ската", f11, "#555", "lm")
text(40, 14, "Вид сверху, перед внизу. H5 стоит между ступенькой (y 300) и R1 (y 433): 12,5 мм спереди, 0,9 мм сзади.", f12, "#333")
text(40, 32, "Под скатом экран (x 101–340) наклонён; H5 высотой 50 мм ниже ската на ≥ 9 мм.", f12, "#333")
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "step_case_plan.png"))
