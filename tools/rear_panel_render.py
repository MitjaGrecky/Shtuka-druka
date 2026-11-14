#!/usr/bin/env python3
"""Rear wall rendered in the style of the 3D model of panel v7 (model3d/index.html): dark anodised panel, block frames with
titles, nuts and holes, label tags (output = filled tag, input = outlined tag, R26). Positions and labels are those of the
model (R142); rear view, x from the left edge as seen from behind, z from the bottom. Writes docs/ru/img/rear_panel_render.svg.

  python3 tools/rear_panel_render.py        (PNG: render the SVG in a browser, e.g. Edge headless --screenshot)

License: AGPL-3.0-or-later.
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "docs", "ru", "img", "rear_panel_render.svg")
W, H = 515.0, 143.0
S = 6.0                                     # px per mm
PAD = 40
PANEL, PRINT, DIM, NUT, NUT2, HOLE, BODY = "#1d2124", "#e8ecea", "#9aa3a2", "#c9ced1", "#8e9599", "#07090a", "#2b3034"

E = []                                      # SVG elements


def X(x):
    return PAD + x * S


def Z(z):
    return PAD + (H - z) * S


def hexagon(cx, cy, r):
    return " ".join(f"{cx + r * math.cos(math.pi / 6 + k * math.pi / 3):.1f},{cy + r * math.sin(math.pi / 6 + k * math.pi / 3):.1f}"
                    for k in range(6))


def nut(x, z, r_nut, r_hole, kind="hex"):
    cx, cy = X(x), Z(z)
    if kind == "hex":
        E.append(f'<polygon points="{hexagon(cx, cy, r_nut * S)}" fill="url(#alu)" stroke="{NUT2}" stroke-width="1"/>')
    else:
        E.append(f'<circle cx="{cx}" cy="{cy}" r="{r_nut * S}" fill="url(#alu)" stroke="{NUT2}" stroke-width="1"/>')
    E.append(f'<circle cx="{cx}" cy="{cy}" r="{r_hole * S}" fill="{HOLE}"/>')


def tag(text, x, z, out):
    fs = 2.5 * S
    tw = (len(text) * 0.56 * 2.5 + 2.2) * S
    th = 3.8 * S
    cx, cy = X(x), Z(z)
    if out:
        E.append(f'<rect x="{cx - tw / 2:.1f}" y="{cy - th / 2:.1f}" width="{tw:.1f}" height="{th:.1f}" rx="{0.8 * S}" fill="{PRINT}"/>')
        col = PANEL
    else:
        E.append(f'<rect x="{cx - tw / 2:.1f}" y="{cy - th / 2:.1f}" width="{tw:.1f}" height="{th:.1f}" rx="{0.8 * S}" fill="none" '
                 f'stroke="{PRINT}" stroke-width="{0.35 * S}"/>')
        col = PRINT
    E.append(f'<text x="{cx:.1f}" y="{cy + fs * 0.36:.1f}" font-size="{fs:.1f}" font-weight="600" text-anchor="middle" fill="{col}">{text}</text>')


OFF = {"xlr": 15.5, "din": 12, "trs": 9}    # tag below the jack, as in the model


def jack(kind, x, z, label, out):
    if kind == "din":
        nut(x, z, 9, 7, "round")
        for k in range(5):                  # 180 deg DIN: five contacts on an arc, key at the top
            a = math.radians(45 * k)
            E.append(f'<circle cx="{X(x + 3.6 * math.cos(a)):.1f}" cy="{Z(z) + 3.6 * S * math.sin(a):.1f}" r="{0.55 * S}" fill="{NUT2}"/>')
        E.append(f'<rect x="{X(x) - 0.8 * S:.1f}" y="{Z(z + 7):.1f}" width="{1.6 * S}" height="{1.6 * S}" fill="{PANEL}"/>')
    elif kind == "trs":
        nut(x, z, 6, 3.2)
    elif kind == "mini":
        nut(x, z, 3.6, 1.8)
    elif kind == "rca":
        nut(x, z, 4.6, 1.6, "round")
        E.append(f'<circle cx="{X(x)}" cy="{Z(z)}" r="{2.6 * S}" fill="none" stroke="{NUT2}" stroke-width="2"/>')
    elif kind == "xlr":
        nut(x, z, 12, 9.5, "round")
        E.append(f'<circle cx="{X(x)}" cy="{Z(z)}" r="{3.2 * S}" fill="{BODY}" stroke="{NUT2}" stroke-width="2"/>')
        E.append(f'<circle cx="{X(x)}" cy="{Z(z)}" r="{1.6 * S}" fill="{HOLE}"/>')
        for k in range(3):
            a = math.radians(90 + 120 * k + 60)
            E.append(f'<circle cx="{X(x) + 6.2 * S * math.cos(a):.1f}" cy="{Z(z) + 6.2 * S * math.sin(a):.1f}" r="{0.9 * S}" fill="{NUT2}"/>')
    elif kind == "dc":
        nut(x, z, 4.5, 2.2, "round")
        E.append(f'<circle cx="{X(x)}" cy="{Z(z)}" r="{0.6 * S}" fill="{NUT}"/>')
    elif kind == "gnd":
        nut(x, z, 4, 2, "round")
        E.append(f'<polygon points="{hexagon(X(x), Z(z), 2.3 * S)}" fill="url(#alu)" stroke="{NUT2}"/>')
    tag(label, x, z - OFF.get(kind, 7.5), out)


def box(w, h, x, z, fill, label, tz, rx=0.6):
    E.append(f'<rect x="{X(x - w / 2):.1f}" y="{Z(z + h / 2):.1f}" width="{w * S}" height="{h * S}" rx="{rx * S}" fill="{fill}" '
             f'stroke="{NUT2}" stroke-width="1.2"/>')
    if label:
        tag(label, x, tz, False)


def frame(x0, x1, title):
    y0, y1 = Z(H - 6), Z(4)
    tw = (len(title) * 0.6 * 3.2 + 3) * S
    E.append(f'<path d="M {X(x0) + 3 * S + tw:.1f} {y0:.1f} H {X(x1) - 2 * S:.1f} Q {X(x1):.1f} {y0:.1f} {X(x1):.1f} {y0 + 2 * S:.1f} '
             f'V {y1 - 2 * S:.1f} Q {X(x1):.1f} {y1:.1f} {X(x1) - 2 * S:.1f} {y1:.1f} H {X(x0) + 2 * S:.1f} '
             f'Q {X(x0):.1f} {y1:.1f} {X(x0):.1f} {y1 - 2 * S:.1f} V {y0 + 2 * S:.1f} Q {X(x0):.1f} {y0:.1f} {X(x0) + 2 * S:.1f} {y0:.1f} '
             f'H {X(x0) + 3 * S:.1f}" fill="none" stroke="{PRINT}" stroke-opacity=".75" stroke-width="{0.35 * S}"/>')
    E.append(f'<text x="{X(x0) + 4 * S:.1f}" y="{y0 + 1.1 * S:.1f}" font-size="{3.2 * S}" font-weight="600" fill="{PRINT}">{title}</text>')


# ---------------------------------------------------------------- the model's rear wall (model3d/index.html, R142)
frame(4.5, 78.5, "Power / USB")
box(16, 13, 20, 78, HOLE, "LAN", 67)
E.append(f'<rect x="{X(20 - 5)}" y="{Z(78 - 4.5)}" width="{10 * S}" height="{2 * S}" fill="{NUT2}"/>')
box(13, 5.5, 40, 80, HOLE, "USB-A", 72)
E.append(f'<rect x="{X(40 - 5)}" y="{Z(80 + 0.6)}" width="{10 * S}" height="{1.6 * S}" fill="{NUT2}"/>')
box(9, 3.5, 62, 80, HOLE, "USB-C (PC)", 72, rx=1.75)
jack("dc", 20, 40, "DC 12–24V", False)
box(9, 3.5, 40, 40, HOLE, "USB-C Power", 32, rx=1.75)
box(12, 8, 62, 40, BODY, "On/Off", 30)
E.append(f'<rect x="{X(62 - 4.5)}" y="{Z(40 + 3)}" width="{9 * S}" height="{6 * S}" rx="{0.5 * S}" fill="url(#alu)"/>')

frame(88.5, 262.5, "Control")
for lab, x, z, o in (("In 1", 100, 82, 0), ("Out 1", 122, 82, 1), ("Out 3", 144, 82, 1),
                     ("In 2", 100, 52, 0), ("Out 2", 122, 52, 1), ("Out 4", 144, 52, 1)):
    jack("din", x, z, lab, o)
for lab, x, o in (("TRS In", 100, 0), ("TRS O1", 122, 1), ("TRS O2", 144, 1)):
    jack("mini", x, 22, lab, o)
for i, (lab, o) in enumerate((("Clk O1", 1), ("Clk O2", 1), ("Rst O", 1), ("Clk In", 0), ("Rst In", 0))):
    jack("mini", 172 + 17 * i, 90, lab, o)
for i in range(4):
    jack("mini", 172 + 17 * i, 68, f"CV In {i + 1}", 0)
for i in range(8):
    jack("mini", 172 + 17 * (i % 4), 46 if i < 4 else 24, f"CV {i + 1}", 1)

frame(272.5, 342.5, "Audio Out")
for lab, x, z in (("Main L", 292, 80), ("Main R", 322, 80), ("Aux L", 292, 52), ("Aux R", 322, 52)):
    jack("trs", x, z, lab, 1)
jack("rca", 292, 24, "RCA L", 1)
jack("rca", 322, 24, "RCA R", 1)

frame(352.5, 510.5, "Audio In")
jack("xlr", 370, 80, "Mic/Line 1", 0)
jack("xlr", 400, 80, "Mic/Line 2", 0)
jack("trs", 370, 32, "Hi-Z 1", 0)
jack("trs", 400, 32, "Hi-Z 2", 0)
jack("rca", 428, 86, "Phono L", 0)
jack("rca", 446, 86, "Phono R", 0)
jack("gnd", 468, 86, "GND", 0)
box(5, 9, 490, 86, BODY, "Phono/Line", 78.5)
E.append(f'<rect x="{X(490 - 1.2)}" y="{Z(86 + 3.5)}" width="{2.4 * S}" height="{3.5 * S}" rx="{0.6 * S}" fill="url(#alu)"/>')
for i in range(8):
    jack("trs", 428 + 22 * (i % 4), 56 if i < 4 else 28, f"Line {i + 1}", 0)


def main():
    w, h = W * S + 2 * PAD, H * S + 2 * PAD + 60
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" '
            'font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif">'
            '<defs><linearGradient id="alu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e3e7e9"/>'
            '<stop offset=".55" stop-color="#b9bfc3"/><stop offset="1" stop-color="#8f969a"/></linearGradient>'
            '<linearGradient id="anod" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#23282b"/>'
            f'<stop offset="1" stop-color="{PANEL}"/></linearGradient></defs>'
            f'<rect width="100%" height="100%" fill="#111416"/>'
            f'<rect x="{PAD}" y="{PAD}" width="{W * S}" height="{H * S}" rx="{1.5 * S}" fill="url(#anod)" stroke="#000" stroke-width="2"/>')
    foot = (f'<text x="{PAD}" y="{h - 22:.0f}" font-size="20" fill="{DIM}">Shtuka Druka - rear wall, rear view, 515 × 143 mm '
            f'(3D model of panel v7, R142). Filled tag = output, outlined tag = input (R26). DIN, USB, LAN, DC on nuts (R141).</text></svg>')
    open(OUT, "w", encoding="utf-8").write(head + "".join(E) + foot)
    print("ok", OUT, int(w), "x", int(h))


if __name__ == "__main__":
    main()
