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
# v5 (18.11.2026, after the user's review of v4): power at the very edge, switch on top and away from the cables;
# computer ports next to it; MIDI = DIN 2 x 3 + the three MIDI TRS in ONE block (R32: TRS inside the MIDI block, not next to CV);
# the MIDI TRS sit on the left column of R2 (R141: all mini-jacks on R2), then a gap, then Sync and CV.
J += [("switch", 14, 98, "Power", 0), ("dc", 14, 74, "DC 12–24V", 0), ("usbc", 14, 52, "USB-C PD", 0)]
J += [("lan", 40, 98, "LAN", 0), ("usba", 40, 80, "USB-A", 0), ("usbc", 40, 64, "USB-C PC", 0)]
for (t, o), (r, z) in zip((("In 1", 0), ("In 2", 0), ("Out 1", 1), ("Out 2", 1), ("Out 3", 1), ("Out 4", 1)),
                          ((70, 98), (70, 72), (94, 98), (94, 72), (118, 98), (118, 72))):
    J.append(("din", r, z, t, o))
J += [("mini", 166, 96, "TRS In", 0), ("mini", 166, 74, "TRS Out 1", 1), ("mini", 166, 52, "TRS Out 2", 1)]
sync = [186, 204, 222, 240, 258]
for c, (t, o) in zip(sync, (("Clock 1", 1), ("Clock 2", 1), ("Reset", 1), ("Clk In", 0), ("Rst In", 0))):
    J.append(("mini", c, 96, t, o))
cv = [195, 213, 231, 249]
for i in range(4):
    J.append(("mini", cv[i], 70, f"CV In {i + 1}", 0))
    J.append(("mini", cv[i], 48, f"CV Out {i + 1}", 1))
    J.append(("mini", cv[i], 26, f"CV Out {i + 5}", 1))
J += [("trs", 292, 88, "Main L", 1), ("trs", 322, 88, "Main R", 1), ("trs", 292, 57, "Aux L", 1), ("trs", 322, 57, "Aux R", 1),
      ("rca", 292, 26, "RCA L", 1), ("rca", 322, 26, "RCA R", 1)]
J += [("xlr", 370, 88, "Mic/Line 1", 0), ("xlr", 400, 88, "Mic/Line 2", 0), ("trs", 370, 35, "Hi-Z 1", 0), ("trs", 400, 35, "Hi-Z 2", 0),
      ("rca", 428, 95, "Phono L", 0), ("rca", 446, 95, "Phono R", 0), ("post", 468, 95, "GND", 0), ("switch", 490, 95, "Phono/Line", 0)]
for i in range(8):
    J.append(("trs", 428 + (i % 4) * 22, 62 if i < 4 else 31, f"Line {i + 1}", 0))

FRAMES = [("Power", 4, 25, 40, 113), ("USB/LAN", 28, 53, 54, 113), ("MIDI", 57, 177, 40, 113), ("Sync", 178, 263, 84, 113),
          ("CV", 186, 258, 14, 82), ("Audio Out", 273, 342, 14, 112), ("Audio In", 352, 510, 14, 112)]
R = {"din": 9, "xlr": 12, "trs": 6, "rca": 4.6, "mini": 3.6, "dc": 4, "post": 4}
BOX = {"lan": (16, 13), "usba": (13, 5.5), "usbc": (9, 3.5), "switch": (12, 8)}


def P(r, z):
    return OX + r * S, OY + (H - z) * S


def main():
    el = []
    Wpx, Hpx = OX * 2 + W * S, OY + H * S + 120
    el.append(f'<rect width="100%" height="100%" fill="#ffffff"/>')
    el.append('<text x="30" y="26" font-size="16" font-weight="700" fill="#1f2933">Задняя стенка v5 (линия R174), вид сзади, мм; высота 117</text>')
    el.append('<text x="30" y="44" font-size="11" fill="#52606d">Входы — рамка, выходы — заливка (R26); подписи на английском (R45). Пунктир — платы и H5 за стенкой.</text>')
    x0, y0 = P(0, H)
    el.append(f'<rect x="{x0}" y="{y0}" width="{W * S}" height="{H * S}" rx="8" fill="#24272b" stroke="#111" stroke-width="2"/>')
    # boards behind (dashed)
    for nm, r0, r1, z0, z1, c in (("H5 (за стенкой)", 22, 139, 11, 55, "#d64545"), ("R2", 156, 263, 10, 113, "#3f9b5b"), ("R1", 273, 511, 8, 104, "#3f9b5b")):
        a, b = P(r0, z1), P(r1, z0)
        el.append(f'<rect x="{a[0]}" y="{a[1]}" width="{b[0] - a[0]}" height="{b[1] - a[1]}" fill="none" stroke="{c}" stroke-width="1.2" stroke-dasharray="5 4" opacity=".8"/>')
        el.append(f'<text x="{a[0] + 4}" y="{b[1] - 4}" font-size="10" fill="{c}" opacity=".9">{nm}</text>')
    for t, r0, r1, z0, z1 in FRAMES:
        a, b = P(r0, z1), P(r1, z0)
        el.append(f'<rect x="{a[0]}" y="{a[1]}" width="{b[0] - a[0]}" height="{b[1] - a[1]}" rx="5" fill="none" stroke="#e8ecea" stroke-width="0.9"/>')
        el.append(f'<rect x="{a[0] + 5}" y="{a[1] - 6}" width="{len(t) * 6.6 + 8}" height="12" fill="#24272b"/>')
        el.append(f'<text x="{a[0] + 9}" y="{a[1] + 4}" font-size="10.5" font-weight="700" fill="#e8ecea">{t}</text>')
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
        ty = cy + (ext + 4.2) * S
        tw = len(tag) * 4.4 + 6
        if out:
            el.append(f'<rect x="{cx - tw / 2}" y="{ty - 6}" width="{tw}" height="11" rx="2" fill="#e8ecea"/>')
            el.append(f'<text x="{cx}" y="{ty + 2}" font-size="7.6" font-weight="700" fill="#24272b" text-anchor="middle">{tag}</text>')
        else:
            el.append(f'<rect x="{cx - tw / 2}" y="{ty - 6}" width="{tw}" height="11" rx="2" fill="none" stroke="#e8ecea" stroke-width="0.7"/>')
            el.append(f'<text x="{cx}" y="{ty + 2}" font-size="7.6" font-weight="700" fill="#e8ecea" text-anchor="middle">{tag}</text>')
    # logo strip in the free field under Power / USB, in front of the H5
    cx, cy = P(85, 28)
    el.append(f'<text x="{cx}" y="{cy}" font-size="13" font-weight="700" fill="#5d6970" text-anchor="middle" letter-spacing="2">SHTUKA DRUKA</text>')
    cx, cy = P(85, 18)
    el.append(f'<text x="{cx}" y="{cy}" font-size="8" fill="#5d6970" text-anchor="middle">serial · CE · rating label</text>')
    # scale
    a, b = P(0, -8), P(515, -8)
    el.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#d64545"/><text x="{(a[0] + b[0]) / 2}" y="{a[1] + 14}" font-size="11" fill="#d64545" text-anchor="middle">515 (r от левого края при виде сзади; x модели = 515 − r)</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wpx:.0f} {Hpx:.0f}" width="{Wpx:.0f}" height="{Hpx:.0f}" '
           f'font-family="Segoe UI, Arial, sans-serif"><title>Задняя стенка v5</title>' + "".join(el) + "</svg>")
    open(os.path.join(HERE, "41_rear_v5.svg"), "w", encoding="utf-8").write(svg)
    for k, r, z, tag, out in J:
        print(f"{tag}\t{k}\tr {r:g}\tx {515 - r:g}\tz {z:g}\t{'out' if out else 'in'}")


if __name__ == "__main__":
    main()
