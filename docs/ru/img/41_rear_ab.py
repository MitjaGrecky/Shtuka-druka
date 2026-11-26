#!/usr/bin/env python3
"""Rear wall variants A and B on Neutrik datasheet sizes (docs/ru/48 sec. 6, datasheets/text/neutrik_*.md), doc 41 sec. 24.7.
A = v6.1 as is: TRS NJ3FD-V (hole 12, nut 14.5, NOT D), combo NCJ6FI flange 27x30 hole 23.8.
B = A + LAN NE8FDP and USB-A NAUSB-W in D (26x31, hole 24); DIN moved +6 mm, USB-C PC moved to the power block (z 17).
Rear view, r = mm from LEFT edge (model x = 515 - r), z from floor, wall to z 110. Writes 41_rear_A/B .svg/.csv."""
import importlib.util, os
HERE = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("v", os.path.join(HERE, "41_rear_v6_1.py")); v = importlib.util.module_from_spec(sp); sp.loader.exec_module(v)
S, OX, H, W, P = v.S, v.OX, v.H, v.W, v.P
DEPTH = {"switch": 25, "dc": 25, "usbc": 15, "lan": 35, "usba": 20, "din": 19.2, "mini": 15, "trs": 24, "rca": 13, "xlr": 24, "post": 15}
ZD = [(3, 28, 0, 86, 26), (3, 28, 86, 110, 60), (33, 153, 57, 110, 60), (160, 511, 1.5, 110, 42)]


def zdepth(r, z):
    for a, b, c, d, dep in ZD:
        if a <= r <= b and c <= z <= d: return dep
    return None


def tag(cx, cy, t, out, dy, box=True):
    ty = cy + dy; tw = len(t) * 4.1 + 6
    if not box:
        return f'<text x="{cx}" y="{ty + 2}" font-size="6.2" font-weight="700" fill="#e8ecea" text-anchor="middle">{t}</text>'
    if out:
        return (f'<rect x="{cx - tw / 2}" y="{ty - 4.5}" width="{tw}" height="9" rx="2" fill="#e8ecea"/>'
                f'<text x="{cx}" y="{ty + 2.5}" font-size="7" font-weight="700" fill="#24272b" text-anchor="middle">{t}</text>')
    return (f'<rect x="{cx - tw / 2}" y="{ty - 4.5}" width="{tw}" height="9" rx="2" fill="none" stroke="#e8ecea" stroke-width="0.7"/>'
            f'<text x="{cx}" y="{ty + 2.5}" font-size="7" font-weight="700" fill="#e8ecea" text-anchor="middle">{t}</text>')


def build(mode):
    J = [list(j) for j in v.J]
    ex = []                                   # extra D drawings: (kind, r, z, tag)
    if mode == "A1":
        pos = {"In 1": (85.5, 83.5), "Out 1": (112.5, 83.5), "Out 3": (139.5, 83.5), "In 2": (355, 33), "Out 2": (382, 33), "Out 4": (409, 33)}
        for j in J:
            if j[0] == "din": j[1], j[2] = pos[j[3]]
    if mode == "A3":
        for j in J:
            if j[0] == "din": j[1] = {88: 88, 110: 112, 132: 136}[j[1]]
    if mode == "B":
        for j in J:
            if j[0] == "din": j[1] += 6
            if j[3] == "LAN": j[:] = ["lan", 46, 83.5, "LAN", 0]
            if j[3] == "USB-A": j[:] = ["usba", 72, 83.5, "USB-A", 0]
            if j[3] == "USB-C" and j[1] == 62: j[:] = ["usbc", 16, 17, "USB-C PC", 0]
    return J


def draw(mode):
    J = build(mode)
    ttl = {"A3": "A3 (A + 6 DIN Lumberg 0107 05, шаг 24 по r)", "A2": "A2 (A + 6 DIN одним блоком как v6.1, вырез Ø16 — предположение)", "A1": "A1 (утверждённый A + 6 DIN в D-фланце 26×31, два места)", "A": "A: v6.1 как есть, TRS = NJ3FD-V (не D), combo на плате", "B": "B: A + LAN и USB-A в D (26×31), TRS остаются NJ3FD-V"}[mode]
    el = ['<rect width="100%" height="100%" fill="#fff"/>',
          f'<text x="30" y="20" font-size="16" font-weight="700" fill="#1f2933">Задняя стенка, вариант {ttl}</text>',
          '<text x="30" y="36" font-size="11" fill="#52606d">Размеры по даташитам Neutrik (док. 48, разд. 6); остальные гнёзда — размеры v6.1 (не сверены). Вид сзади, r — мм от ЛЕВОГО края, x модели = 515 − r; z от пола; стенка до z 110, ширина 515.</text>',
          '<text x="30" y="50" font-size="11" fill="#52606d">Фон: зелёный — можно (цифра — глубина зоны, мм), красный — нельзя (H5). Серый фланец — D 26×31 / combo 27×30; круг — вырез. Статус: проект раскладки, геометрия R174.</text>']
    x0, y0 = P(0, H)
    el.append(f'<rect x="{x0}" y="{y0 + (H - 110) * S}" width="{W * S}" height="{110 * S}" rx="8" fill="#24272b" stroke="#111" stroke-width="2"/>')
    for r0, r1, z0, z1, t in v.ZONES:
        a, b = P(r0, min(z1, 110)), P(r1, z0); bad = t.startswith("нельзя")
        el.append(f'<rect x="{a[0]}" y="{a[1]}" width="{b[0] - a[0]}" height="{b[1] - a[1]}" fill="{"#7a2b2b" if bad else "#1e3a2c"}" opacity=".3"/>')
        if not bad and t != "60": pass
    for nm, r0, r1, z0, z1, c in (("H5", 33, 153, 11, 56, "#d64545"), ("R2", 156, 263, 10, 113, "#3f9b5b"), ("R1", 273, 511, 8, 104, "#3f9b5b")):
        a, b = P(r0, z1), P(r1, z0)
        el.append(f'<rect x="{a[0]}" y="{a[1]}" width="{b[0] - a[0]}" height="{b[1] - a[1]}" fill="none" stroke="{c}" stroke-width="1.2" stroke-dasharray="5 4" opacity=".8"/>')
    if mode == "A1":
        for r0, r1, z0, z1, t in ((72, 153, 57, 110, ""), (340, 425, 1.5, 50, "")):
            a, b = P(r0, z1), P(r1, z0)
            el.append(f'<rect x="{a[0]}" y="{a[1]}" width="{b[0] - a[0]}" height="{b[1] - a[1]}" fill="none" stroke="#e8b84a" stroke-width="1" stroke-dasharray="4 3"/>')
    fr = [("Power", 3.5, 29, 1.5, 110), ("USB/LAN", 32, 82 if mode == "B" else 75, 1.5, 110), ("MIDI", 83 if mode == "B" else 76, 178 if mode == "A" else 178, 1.5, 110)] + \
         [("Sync · CV", 182, 268, 1.5, 110), ("Audio Out", 272, 336, 1.5, 110), ("Audio In", 340, 511, 1.5, 110)]
    if mode == "A1": fr[2] = ("MIDI 1", 72, 153, 57, 110); fr += [("MIDI 2", 340, 425, 1.5, 50)]; fr[4] = ("Audio Out", 272, 336, 1.5, 110); fr[5] = ("Audio In", 340, 511, 1.5, 110)
    if mode == "B": fr[1] = ("USB/LAN", 32, 85, 1.5, 110); fr[2] = ("MIDI", 86, 178, 1.5, 110)
    for t, r0, r1, z0, z1 in fr:
        a, b = P(r0, z1), P(r1, z0)
        el.append(f'<rect x="{a[0]}" y="{a[1]}" width="{b[0] - a[0]}" height="{b[1] - a[1]}" rx="5" fill="none" stroke="#e8ecea" stroke-width="0.9"/>')
        el.append(f'<rect x="{a[0] + 5}" y="{a[1] - 6}" width="{len(t) * 6.6 + 8}" height="12" fill="#24272b"/><text x="{a[0] + 9}" y="{a[1] + 4}" font-size="10.5" font-weight="700" fill="#e8ecea">{t}</text>')
    rows = ["tag,kind,r_mm,model_x_mm,z_mm,depth_mm,zone_depth_mm,ok"]
    for k, r, z, t, o in J:
        cx, cy = P(r, z)
        dy, box = v.TAG * S, True
        if k == "xlr":                                           # NCJ6FI combo flange 27x30, hole 23.8
            el.append(f'<rect x="{cx - 13.5 * S}" y="{cy - 15 * S}" width="{27 * S}" height="{30 * S}" fill="#3a4047" stroke="#9aa5af" stroke-width="0.8"/>'
                      f'<circle cx="{cx}" cy="{cy}" r="{11.9 * S}" fill="#b9bec2"/><circle cx="{cx}" cy="{cy}" r="{8 * S}" fill="#050506"/>')
            dy, box = (15 + 2.6) * S, False
        elif k == "din" and mode == "A3":                         # Lumberg 0107 05: hole 17, flange 21.8 wide, 2 x 3 mm ears horizontal (offset +-9 assumed)
            el.append(f'<rect x="{cx - 10.9 * S}" y="{cy - 9 * S}" width="{21.8 * S}" height="{18 * S}" rx="3" fill="#3a4047" stroke="#9aa5af" stroke-width="0.6"/>'
                      f'<circle cx="{cx}" cy="{cy}" r="{8.5 * S}" fill="#b9bec2"/><circle cx="{cx}" cy="{cy}" r="{5.5 * S}" fill="#050506"/>')
            for sg in (-1, 1):
                el.append(f'<circle cx="{cx + sg * 9.4 * S}" cy="{cy}" r="{1.5 * S}" fill="#050506"/>')
        elif k == "din" and mode == "A2":                         # round DIN, hole 16 (assumed), 2 x M3 holes 3.2 on the diagonal, 21.5 apart
            el.append(f'<circle cx="{cx}" cy="{cy}" r="{8 * S}" fill="#b9bec2"/><circle cx="{cx}" cy="{cy}" r="{5.5 * S}" fill="#050506"/>')
            for sg in (-1, 1):
                el.append(f'<circle cx="{cx + sg * 7.6 * S}" cy="{cy - sg * 7.6 * S}" r="{1.6 * S}" fill="#050506" stroke="#9aa5af" stroke-width="0.5"/>')
        elif k == "din" and mode == "A1":                         # MIDI socket, D flange 26x31, hole 24
            el.append(f'<rect x="{cx - 13 * S}" y="{cy - 15.5 * S}" width="{26 * S}" height="{31 * S}" fill="#3a4047" stroke="#9aa5af" stroke-width="0.8"/>'
                      f'<circle cx="{cx}" cy="{cy}" r="{12 * S}" fill="#b9bec2"/><circle cx="{cx}" cy="{cy}" r="{7.5 * S}" fill="#050506"/>')
            dy = (15.5 + 4.2) * S
        elif k in ("lan", "usba") and mode == "B":               # D 26x31
            el.append(f'<rect x="{cx - 13 * S}" y="{cy - 15.5 * S}" width="{26 * S}" height="{31 * S}" fill="#3a4047" stroke="#9aa5af" stroke-width="0.8"/>'
                      f'<circle cx="{cx}" cy="{cy}" r="{12 * S}" fill="#b9bec2"/>')
            w, h = (16, 13) if k == "lan" else (13, 5.5)
            el.append(f'<rect x="{cx - w * S / 2}" y="{cy - h * S / 2}" width="{w * S}" height="{h * S}" rx="2" fill="#050506"/>')
            dy = (15.5 + 4.2) * S
        elif k == "trs":                                          # NJ3FD-V: nut 14.5, hole 12
            el.append(f'<circle cx="{cx}" cy="{cy}" r="{7.25 * S}" fill="#b9bec2"/><circle cx="{cx}" cy="{cy}" r="{4.8 * S}" fill="#050506"/>')
        elif k in v.BOX:
            w, h = v.BOX[k]
            el.append(f'<rect x="{cx - w * S / 2}" y="{cy - h * S / 2}" width="{w * S}" height="{h * S}" rx="2" fill="#050506" stroke="#9aa5af"/>')
        else:
            rr = v.R[k]; el.append(f'<circle cx="{cx}" cy="{cy}" r="{rr * S}" fill="#b9bec2"/><circle cx="{cx}" cy="{cy}" r="{rr * S * .62}" fill="#050506"/>')
        el.append(tag(cx, cy, t, o, dy, box))
        d = {"lan": 36 if mode == "B" else 35, "usba": 40.6 if mode == "B" else 20}.get(k, DEPTH[k])
        zd = zdepth(r, z); rows.append(f"{t},{k},{r:g},{515 - r:g},{z:g},{d},{zd},{'ok' if zd and d <= zd else 'NO'}")
    a, b = P(0, -8), P(515, -8)
    el.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#d64545"/><text x="{(a[0] + b[0]) / 2}" y="{a[1] + 14}" font-size="11" fill="#d64545" text-anchor="middle">515</text>')
    Wp, Hp = OX * 2 + W * S, 60 + H * S + 90
    open(os.path.join(HERE, f"41_rear_{mode}.svg"), "w", encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wp:.0f} {Hp:.0f}" width="{Wp:.0f}" height="{Hp:.0f}" font-family="Segoe UI, Arial, sans-serif"><title>Задняя стенка {mode}</title>' + "".join(el) + "</svg>")
    open(os.path.join(HERE, f"41_rear_{mode}_jacks.csv"), "w", encoding="utf-8").write("\n".join(rows) + "\n")
    print(mode, [r for r in rows if r.endswith("NO")])


draw("A"); draw("B"); draw("A1"); draw("A2"); draw("A3")
