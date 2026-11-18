#!/usr/bin/env python3
"""Rear panel v4 for the main line R174 (doc 41 section 24, 18.11.2026): rear view, r = mm from the LEFT edge as seen from
behind (model x = 515 - r), z = mm from the floor. Wall 117 high. Boards: R1 r 273-511 z 8-104, R2 r 156-263 z 10-113
(rectangle, no low arm, R178), H5 behind r 19-139 z 11-55 (inside). DIN x 6 and Power / USB are panel-mount on nuts above the H5
(R141, R178). Inputs framed, outputs filled (R26); all labels in English (R45). Writes 41_rear_v4.svg and prints the jack table."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 515.0, 117.0
S = 2.0
OX, OY = 30, 60

J = []          # (kind, r, z, tag, out)
# v6 (18.11.2026): placed inside the main engineer's free-zone map behind the rear wall (model g3):
#   r 3-28: z 0-86 depth 26 (fan behind), z 86-114 depth 60;  r 33-153: z < 57 forbidden (H5), z 57-114 depth 60;
#   r 153-160: do not use;  r 160-511: z 1.5-114 depth 42.
# Power stays at the EDGE (user: switch reachable, power not "between everything"): switch on top (depth 60), DC and USB-C below
# (depth 26 behind the fan: DC 25, USB-C 20 fit); cables to PW run above the H5 (z 57-114, depth 60).
# Short tags under group titles so every tag fits its pitch: minis pitch 17-18 -> tags <= 6 characters.
ROW = (99, 73, 47, 21)
TAG = 13.5
J += [("switch", 16, 99, "Power", 0), ("dc", 16, 73, "DC In", 0), ("usbc", 16, 47, "USB-C", 0)]
J += [("lan", 53, 99, "LAN", 0), ("usba", 44, 73, "USB-A", 0), ("usbc", 62, 73, "USB-C", 0)]
for (t, o), (r, z) in zip((("In 1", 0), ("In 2", 0), ("Out 1", 1), ("Out 2", 1), ("Out 3", 1), ("Out 4", 1)),
                          ((88, 99), (88, 73), (110, 99), (110, 73), (132, 99), (132, 73))):
    J.append(("din", r, z, t, o))
J += [("mini", 167, 99, "In", 0), ("mini", 167, 73, "Out 1", 1), ("mini", 167, 47, "Out 2", 1)]
for c, (t, o) in zip((190, 207, 224, 241, 258), (("Clk 1", 1), ("Clk 2", 1), ("Reset", 1), ("Clk In", 0), ("Rst In", 0))):
    J.append(("mini", c, 99, t, o))
for i, c in enumerate((190, 207, 224, 241)):
    J.append(("mini", c, 73, f"In {i + 1}", 0))
    J.append(("mini", c, 47, f"Out {i + 1}", 1))
    J.append(("mini", c, 21, f"Out {i + 5}", 1))
J += [("trs", 292, 99, "Main L", 1), ("trs", 314, 99, "Main R", 1), ("trs", 292, 73, "Aux L", 1), ("trs", 314, 73, "Aux R", 1),
      ("rca", 292, 47, "RCA L", 1), ("rca", 314, 47, "RCA R", 1)]
AC = [434, 456, 478, 500]
J += [("xlr", 362, 99, "Mic/Line 1", 0), ("xlr", 394, 99, "Mic/Line 2", 0), ("trs", 362, 73, "Hi-Z 1", 0), ("trs", 394, 73, "Hi-Z 2", 0),
      ("rca", AC[0], 99, "Phono L", 0), ("rca", AC[1], 99, "Phono R", 0), ("post", AC[2], 99, "GND", 0), ("switch", AC[3], 99, "Ph/Line", 0)]
for i in range(8):
    J.append(("trs", AC[i % 4], 73 if i < 4 else 47, f"Line {i + 1}", 0))

FRAMES = [("Power", 3.5, 29, 1.5, 114), ("USB/LAN", 33, 72, 1.5, 114), ("MIDI", 76, 178, 1.5, 114), ("Sync · CV", 182, 268, 1.5, 114),
          ("Audio Out", 272, 336, 1.5, 114), ("Audio In", 340, 511, 1.5, 114)]
SUB = [("TRS", 167, 107.5), ("CV", 258, 72)]          # small group titles: text, r, z
ZONES = [(3, 28, 0, 86, "глубина 26 (вентилятор)"), (3, 28, 86, 114, "60"), (33, 153, 0, 56, "нельзя: H5"), (33, 153, 57, 114, "60"),
         (153, 160, 0, 114, "нельзя"), (160, 511, 1.5, 114, "42")]
R = {"din": 9, "xlr": 11, "trs": 6, "rca": 4.6, "mini": 3.6, "dc": 4, "post": 4}
BOX = {"lan": (16, 13), "usba": (13, 5.5), "usbc": (9, 3.5), "switch": (12, 8)}


def P(r, z):
    return OX + r * S, OY + (H - z) * S


def main():
    el = []
    Wpx, Hpx = OX * 2 + W * S, OY + H * S + 120
    el.append(f'<rect width="100%" height="100%" fill="#ffffff"/>')
    el.append('<text x="30" y="26" font-size="16" font-weight="700" fill="#1f2933">Задняя стенка v6 (линия R174), по карте свободных зон, вид сзади, мм; высота 117</text>')
    el.append('<text x="30" y="44" font-size="11" fill="#52606d">Входы — рамка, выходы — заливка (R26); подписи на английском (R45). Фон: зелёный — можно (цифра — глубина, мм), красный — нельзя (H5). Пунктир — платы и H5.</text>')
    x0, y0 = P(0, H)
    el.append(f'<rect x="{x0}" y="{y0}" width="{W * S}" height="{H * S}" rx="8" fill="#24272b" stroke="#111" stroke-width="2"/>')
    for r0, r1, z0, z1, t in ZONES:
        a, b = P(r0, z1), P(r1, z0)
        bad = t.startswith("нельзя")
        el.append(f'<rect x="{a[0]}" y="{a[1]}" width="{b[0] - a[0]}" height="{b[1] - a[1]}" fill="{"#7a2b2b" if bad else "#1e3a2c"}" opacity=".3"/>')
    # boards behind (dashed)
    for nm, r0, r1, z0, z1, c in (("H5 (за стенкой)", 33, 153, 11, 56, "#d64545"), ("R2", 156, 263, 10, 113, "#3f9b5b"), ("R1", 273, 511, 8, 104, "#3f9b5b")):
        a, b = P(r0, z1), P(r1, z0)
        el.append(f'<rect x="{a[0]}" y="{a[1]}" width="{b[0] - a[0]}" height="{b[1] - a[1]}" fill="none" stroke="{c}" stroke-width="1.2" stroke-dasharray="5 4" opacity=".8"/>')
        el.append(f'<text x="{a[0] + 4}" y="{b[1] - 4}" font-size="10" fill="{c}" opacity=".9">{nm}</text>')
    for t, r0, r1, z0, z1 in FRAMES:
        a, b = P(r0, z1), P(r1, z0)
        el.append(f'<rect x="{a[0]}" y="{a[1]}" width="{b[0] - a[0]}" height="{b[1] - a[1]}" rx="5" fill="none" stroke="#e8ecea" stroke-width="0.9"/>')
        el.append(f'<rect x="{a[0] + 5}" y="{a[1] - 6}" width="{len(t) * 6.6 + 8}" height="12" fill="#24272b"/>')
        el.append(f'<text x="{a[0] + 9}" y="{a[1] + 4}" font-size="10.5" font-weight="700" fill="#e8ecea">{t}</text>')
    a, b = P(185, 84), P(265, 84)
    el.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#9aa3aa" stroke-width="0.7" stroke-dasharray="3 2"/>')
    for t, r, z in SUB:
        cx, cy = P(r, z)
        el.append(f'<text x="{cx}" y="{cy + 3}" font-size="8" font-weight="700" fill="#9aa3aa" text-anchor="middle">{t}</text>')
    for k, r, z, tag, out in J:
        cx, cy = P(r, z)
        if k in BOX:
            w, h = BOX[k]
            el.append(f'<rect x="{cx - w * S / 2}" y="{cy - h * S / 2}" width="{w * S}" height="{h * S}" rx="2" fill="#050506" stroke="#9aa5af" stroke-width="1"/>')
            ext = h / 2
        else:
            rr = R[k]
            el.append(f'<circle cx="{cx}" cy="{cy}" r="{rr * S}" fill="#b9bec2"/><circle cx="{cx}" cy="{cy}" r="{rr * S * 0.62}" fill="#050506"/>')
            ext = rr
        ty = cy + TAG * S
        tw = len(tag) * 4.1 + 6
        if out:
            el.append(f'<rect x="{cx - tw / 2}" y="{ty - 4.5}" width="{tw}" height="9" rx="2" fill="#e8ecea"/>')
            el.append(f'<text x="{cx}" y="{ty + 2.5}" font-size="7" font-weight="700" fill="#24272b" text-anchor="middle">{tag}</text>')
        else:
            el.append(f'<rect x="{cx - tw / 2}" y="{ty - 4.5}" width="{tw}" height="9" rx="2" fill="none" stroke="#e8ecea" stroke-width="0.7"/>')
            el.append(f'<text x="{cx}" y="{ty + 2.5}" font-size="7" font-weight="700" fill="#e8ecea" text-anchor="middle">{tag}</text>')
    # scale
    a, b = P(0, -8), P(515, -8)
    el.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#d64545"/><text x="{(a[0] + b[0]) / 2}" y="{a[1] + 14}" font-size="11" fill="#d64545" text-anchor="middle">515 (r от левого края при виде сзади; x модели = 515 − r)</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wpx:.0f} {Hpx:.0f}" width="{Wpx:.0f}" height="{Hpx:.0f}" '
           f'font-family="Segoe UI, Arial, sans-serif"><title>Задняя стенка v6</title>' + "".join(el) + "</svg>")
    open(os.path.join(HERE, "41_rear_v6.svg"), "w", encoding="utf-8").write(svg)
    for k, r, z, tag, out in J:
        print(f"{tag}\t{k}\tr {r:g}\tx {515 - r:g}\tz {z:g}\t{'out' if out else 'in'}")


if __name__ == "__main__":
    main()
