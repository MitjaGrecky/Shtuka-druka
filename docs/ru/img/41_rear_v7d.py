#!/usr/bin/env python3
"""Rear wall v7-D (doc 41, mixed): Neutrik D flange 26 x 31 mm (hole 24, from the engineer; NOT checked against the datasheet) for
R1 audio (20 jacks) and LAN; mini 3.5, DIN, power group and USB as in v6.1. Rear view, r = mm from the LEFT edge seen from behind
(model x = 515 - r), z = mm from the floor, wall to z 110. Imports v6.1 for zones, boards and the unchanged groups."""
import importlib.util, os
HERE = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("v", os.path.join(HERE, "41_rear_v6_1.py")); v = importlib.util.module_from_spec(sp); sp.loader.exec_module(v)
FW, FH = 26.0, 31.0
RZ = (94, 63, 32)
OC = (286, 312); IC = [338 + 26 * i for i in range(7)]
D = []   # (kind, r, z, tag, out, D?)
for (t, o), r, z in zip((("Main L", 1), ("Main R", 1), ("Aux L", 1), ("Aux R", 1), ("RCA L", 1), ("RCA R", 1)), OC * 3, [RZ[0]] * 2 + [RZ[1]] * 2 + [RZ[2]] * 2):
    D.append(("rca" if "RCA" in t else "trs", r, z, t, o, 1))
D += [("xlr", IC[0], RZ[0], "Mic/Line 1", 0, 1), ("xlr", IC[1], RZ[0], "Mic/Line 2", 0, 1), ("trs", IC[0], RZ[1], "Hi-Z 1", 0, 1), ("trs", IC[1], RZ[1], "Hi-Z 2", 0, 1),
      ("rca", IC[2], RZ[0], "Phono L", 0, 1), ("rca", IC[3], RZ[0], "Phono R", 0, 1), ("post", IC[4], RZ[0], "GND", 0, 0), ("switch", IC[5], RZ[0], "Ph/Line", 0, 0)]
for i in range(8):
    D.append(("trs", IC[2 + i % 4], RZ[1] if i < 4 else RZ[2], f"Line {i + 1}", 0, 1))
D.append(("lan", 46, 83.5, "LAN", 0, 1))
RES = [(IC[6], z) for z in RZ] + [(IC[0], RZ[2]), (IC[1], RZ[2])]       # free D slots in R1
keep = [j for j in v.J if j[1] < 272 and j[3] not in ("LAN", "USB-A") and not (j[3] == "USB-C" and j[1] == 62)]
keep += [("usba", 67, 95, "USB-A", 0), ("usbc", 67, 69, "USB-C", 0)]
v.FRAMES[:] = [("Power", 3.5, 29, 1.5, 110), ("USB/LAN", 32, 75, 1.5, 110), ("MIDI", 76, 178, 1.5, 110), ("Sync · CV", 182, 268, 1.5, 110),
               ("Audio Out", 272, 325, 1.5, 110), ("Audio In", 326, 511, 1.5, 110)]
v.SUB[:] = [s for s in v.SUB]
S, OX, OY, H, W = v.S, v.OX, v.OY, v.H, v.W
P = v.P


def tag(cx, cy, t, out, dy):
    ty = cy + dy; tw = len(t) * 4.1 + 6
    if out:
        return (f'<rect x="{cx - tw / 2}" y="{ty - 4.5}" width="{tw}" height="9" rx="2" fill="#e8ecea"/>'
                f'<text x="{cx}" y="{ty + 2.5}" font-size="7" font-weight="700" fill="#24272b" text-anchor="middle">{t}</text>')
    return (f'<rect x="{cx - tw / 2}" y="{ty - 4.5}" width="{tw}" height="9" rx="2" fill="none" stroke="#e8ecea" stroke-width="0.7"/>'
            f'<text x="{cx}" y="{ty + 2.5}" font-size="7" font-weight="700" fill="#e8ecea" text-anchor="middle">{t}</text>')


def main():
    el = ['<rect width="100%" height="100%" fill="#ffffff"/>',
          '<text x="30" y="20" font-size="16" font-weight="700" fill="#1f2933">Задняя стенка v7-D (смешанная): Neutrik D 26×31 в R1 и LAN — предложение дизайнера, не проверено по даташиту</text>',
          '<text x="30" y="36" font-size="11" fill="#52606d">Вид сзади, лицом к стенке; r — мм от ЛЕВОГО края, x модели = 515 − r; z — мм от пола; стенка до z 110, ширина 515; v6.1 (z 95/69/43/17) как основа; геометрия R174. Статус: проект раскладки.</text>',
          '<text x="30" y="50" font-size="11" fill="#52606d">Серый прямоугольник 26×31 — фланец D, круг 24 — вырез; пунктир — резерв (5 свободных мест D); подписи D-гнёзд — на полосе фланца 3,5 мм под вырезом, в масштабе.</text>']
    x0, y0 = P(0, H)
    el.append(f'<rect x="{x0}" y="{y0 + (H - 110) * S}" width="{W * S}" height="{110 * S}" rx="8" fill="#24272b" stroke="#111" stroke-width="2"/>')
    for r0, r1, z0, z1, t in v.ZONES:
        a, b = P(r0, min(z1, 110)), P(r1, z0); bad = t.startswith("нельзя")
        el.append(f'<rect x="{a[0]}" y="{a[1]}" width="{b[0] - a[0]}" height="{b[1] - a[1]}" fill="{"#7a2b2b" if bad else "#1e3a2c"}" opacity=".3"/>')
    for nm, r0, r1, z0, z1, c in (("H5 (за стенкой)", 33, 153, 11, 56, "#d64545"), ("R2", 156, 263, 10, 113, "#3f9b5b"), ("R1", 273, 511, 8, 104, "#3f9b5b")):
        a, b = P(r0, z1), P(r1, z0)
        el.append(f'<rect x="{a[0]}" y="{a[1]}" width="{b[0] - a[0]}" height="{b[1] - a[1]}" fill="none" stroke="{c}" stroke-width="1.2" stroke-dasharray="5 4" opacity=".8"/>')
    for t, r0, r1, z0, z1 in v.FRAMES:
        a, b = P(r0, z1), P(r1, z0)
        el.append(f'<rect x="{a[0]}" y="{a[1]}" width="{b[0] - a[0]}" height="{b[1] - a[1]}" rx="5" fill="none" stroke="#e8ecea" stroke-width="0.9"/>')
        el.append(f'<rect x="{a[0] + 5}" y="{a[1] - 6}" width="{len(t) * 6.6 + 8}" height="12" fill="#24272b"/><text x="{a[0] + 9}" y="{a[1] + 4}" font-size="10.5" font-weight="700" fill="#e8ecea">{t}</text>')
    for r, z in RES:
        a, b = P(r - FW / 2, z + FH / 2), P(r + FW / 2, z - FH / 2)
        el.append(f'<rect x="{a[0]}" y="{a[1]}" width="{b[0] - a[0]}" height="{b[1] - a[1]}" fill="none" stroke="#9aa3aa" stroke-width="0.8" stroke-dasharray="4 3"/>')
    for k, r, z, t, o, isd in D:
        cx, cy = P(r, z)
        if isd:
            el.append(f'<rect x="{cx - FW * S / 2}" y="{cy - FH * S / 2}" width="{FW * S}" height="{FH * S}" fill="#3a4047" stroke="#9aa5af" stroke-width="0.8"/>'
                      f'<circle cx="{cx}" cy="{cy}" r="{12 * S}" fill="#b9bec2"/><circle cx="{cx}" cy="{cy}" r="{v.R[k] * S if k != "lan" else 0}" fill="#050506"/>')
            if k == "lan":
                el.append(f'<rect x="{cx - 8 * S}" y="{cy - 6.5 * S}" width="{16 * S}" height="{13 * S}" rx="2" fill="#050506"/>')
            el.append(tag(cx, cy, t, o, (FH / 2 - 1.75) * S))
        else:
            if k == "switch":
                el.append(f'<rect x="{cx - 6 * S}" y="{cy - 4 * S}" width="{12 * S}" height="{8 * S}" rx="2" fill="#050506" stroke="#9aa5af"/>')
            else:
                el.append(f'<circle cx="{cx}" cy="{cy}" r="{4 * S}" fill="#b9bec2"/><circle cx="{cx}" cy="{cy}" r="{2.5 * S}" fill="#050506"/>')
            el.append(tag(cx, cy, t, o, v.TAG * S))
    for k, r, z, t, o in keep:
        cx, cy = P(r, z)
        if k in v.BOX:
            w, h = v.BOX[k]
            el.append(f'<rect x="{cx - w * S / 2}" y="{cy - h * S / 2}" width="{w * S}" height="{h * S}" rx="2" fill="#050506" stroke="#9aa5af"/>')
        else:
            rr = v.R[k]; el.append(f'<circle cx="{cx}" cy="{cy}" r="{rr * S}" fill="#b9bec2"/><circle cx="{cx}" cy="{cy}" r="{rr * S * .62}" fill="#050506"/>')
        el.append(tag(cx, cy, t, o, v.TAG * S))
    a, b = P(0, -8), P(515, -8)
    el.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#d64545"/><text x="{(a[0] + b[0]) / 2}" y="{a[1] + 14}" font-size="11" fill="#d64545" text-anchor="middle">515</text>')
    Wp, Hp = OX * 2 + W * S, OY + H * S + 90
    open(os.path.join(HERE, "41_rear_v7d.svg"), "w", encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wp:.0f} {Hp:.0f}" width="{Wp:.0f}" height="{Hp:.0f}" font-family="Segoe UI, Arial, sans-serif"><title>Задняя стенка v7-D</title>' + "".join(el) + "</svg>")
    rows = ["tag,kind,r_mm,model_x_mm,z_mm,format"]
    for k, r, z, t, o, isd in D: rows.append(f"{t},{k},{r:g},{515 - r:g},{z:g},{'D 26x31' if isd else 'native'}")
    for k, r, z, t, o in keep: rows.append(f"{t},{k},{r:g},{515 - r:g},{z:g},native")
    open(os.path.join(HERE, "41_rear_v7d_jacks.csv"), "w", encoding="utf-8").write("\n".join(rows) + "\n")
    print(len(rows) - 1, "jacks;", sum(1 for d in D if d[5]), "in D")

main()
