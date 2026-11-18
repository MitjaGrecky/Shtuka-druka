#!/usr/bin/env python3
"""Render of the step case from fit_model.py (orthographic, flat shading, painter's algorithm) -> step_case_render.png:
top = interior (no skin, no pads), bottom = outside. Config: git history (history in git, deleted 18.11.2026) 3b-3d (deck 28, lip 28, fold 41, shelf +60, H5 at the rear).
Run: python render_step.py  (KiCad python). Environment variables of fit_model.py override the configuration."""
import importlib.util, math, os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = dict(WHEEL_TRACK=1, COMPUTER="H5REAR", BATT_LIPO=1, P2_PARTS=1.5, PANEL_PARTS=3, H5_REAR_X=410, PW_X0=245, A1_X0=20, H5_PORT="E",
           F1_MODE="LIP", FRONT_LIP=28, REAR_SHIFT=60, DECK=28, FRONT_Z=41, H5_REAR_Y=413.4 + 60 - 60.9)
for k, v in CFG.items():
    os.environ.setdefault(k, str(v))
spec = importlib.util.spec_from_file_location("fm", os.path.join(HERE, "fit_model.py"))
fm = importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
P = fm.parts()
COL = {"pcb": (63, 143, 90), "parts": (150, 165, 175), "metal": (167, 173, 181), "plastic": (214, 218, 224), "battery": (239, 159, 39),
       "glass": (120, 170, 200), "lcd": (50, 60, 75), "chip": (40, 40, 40), "knob": (60, 64, 72), "led": (240, 220, 120), "shell": (233, 229, 220),
       "grey": (180, 180, 180)}
def color(p):
    if p.name.startswith("Mini-ITX parts"): return (175, 169, 236)
    if p.name.startswith("Mini-ITX board"): return (110, 100, 200)
    if p.group == "itx": return (200, 195, 245)
    return COL.get(p.color, (180, 180, 180))
yaw, pitch = math.radians(-38), math.radians(30)
cy, sy, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch)
def proj(x, y, z):
    xr = x * cy - y * sy; yr = x * sy + y * cy
    return xr, z * cp + yr * sp, yr * cp - z * sp          # u, v (up), depth (bigger = farther)
def corners(b):
    out = []
    for sx in (-1, 1):
        for sy_ in (-1, 1):
            for sz in (-1, 1):
                out.append(tuple(b.c[k] + sx * b.h[0] * b.ax[0][k] + sy_ * b.h[1] * b.ax[1][k] + sz * b.h[2] * b.ax[2][k] for k in range(3)))
    return out
FACES = [((0, 1, 3, 2), (-1, 0, 0)), ((4, 5, 7, 6), (1, 0, 0)), ((0, 1, 5, 4), (0, -1, 0)), ((2, 3, 7, 6), (0, 1, 0)), ((0, 2, 6, 4), (0, 0, -1)), ((1, 3, 7, 5), (0, 0, 1))]
# corner index = sx*4 + sy*2 + sz with (-1->0, 1->1)
FACES = [((0, 1, 3, 2), 0, -1), ((4, 5, 7, 6), 0, 1), ((0, 1, 5, 4), 1, -1), ((2, 3, 7, 6), 1, 1), ((0, 2, 6, 4), 2, -1), ((1, 3, 7, 5), 2, 1)]
def faces(boxes, alpha_glass=True):
    out = []
    for b in boxes:
        cs = corners(b); col = color(b)
        for idx, ax, sgn in FACES:
            n = tuple(sgn * b.ax[ax][k] for k in range(3))
            # view direction (towards viewer) in world coordinates
            vd = (-(sy * -0 + 0), 0, 0)
            nr_y = n[0] * sy + n[1] * cy; nz = n[2]
            facing = -(nr_y * cp - nz * sp)                # normal . (towards camera) with camera at -yr, +z
            if facing <= 0: continue
            pts = [proj(*cs[i]) for i in idx]
            dep = sum(p[2] for p in pts) / 4
            light = 0.55 + 0.45 * max(0.0, (n[2] * 0.8 + n[0] * -0.4 + n[1] * -0.4))
            out.append((dep, [(p[0], p[1]) for p in pts], tuple(int(c * light) for c in col), b))
    return out
def draw(boxes, W, H, title, lip=False):
    fs = faces(boxes); fs.sort(key=lambda f: -f[0])
    allp = [q for f in fs for q in f[1]]
    u0, u1 = min(q[0] for q in allp), max(q[0] for q in allp); v0, v1 = min(q[1] for q in allp), max(q[1] for q in allp)
    k = min((W - 60) / (u1 - u0), (H - 90) / (v1 - v0))
    T = lambda q: (30 + (q[0] - u0) * k, H - 30 - (q[1] - v0) * k)
    im = Image.new("RGBA", (W, H), "white"); d = ImageDraw.Draw(im, "RGBA")
    for dep, pts, col, b in fs:
        a = 120 if b.color == "glass" else 255
        d.polygon([T(q) for q in pts], fill=col + (a,), outline=(40, 40, 40, 90))
    d.text((20, 10), title, fill=(30, 30, 30), font=ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20))
    return im
inner = [p for p in P if p.group not in ("shell", "top", "m1led", "standoff")]
for p in P:       # shell as thin floor only in the interior view
    if p.name == "Floor": inner.insert(0, p)
outer = [p for p in P if p.group not in ("m1led", "standoff") and not p.name.startswith(("Screen driver", "Screen LCM", "Screen HDMI", "Screen USB"))]
W, H = 960, 640
a = draw(inner, W, H, "Внутри (без обшивки): дека 28 мм, губа +28, сгиб 41, зад 116, глубина 548 мм")
b = draw(outer, W, H, "Снаружи")
im = Image.new("RGB", (W, 2 * H), "white"); im.paste(a.convert("RGB"), (0, 0)); im.paste(b.convert("RGB"), (0, H))
im.save(os.path.join(HERE, "step_case_render.png")); print("ok", len(P), "parts")
