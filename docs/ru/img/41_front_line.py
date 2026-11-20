#!/usr/bin/env python3
"""Doc 41 section 24.8: the front intake line (R195) as the musician sees it, plus a section with the proposed drip edge and sill.
Top view: FRONT wall seen from the musician (from the front), x from the left edge of the case (musician's left = x 0), z from the
outer floor; not mirrored. Bottom view: section at x 300 seen from the LEFT (front of the case on the LEFT), y from the front edge.
Numbers: model3d/v8 g3 (width 515, deck/front height 30, skin 3, feet 3); phones jacks 6.35 at x 32 and 80, body z 5-17.7
(hole diameter 11 is an estimate); battery packs from y 6 (x 113-331). Line now in g3: x 110-505, z 3-5.
Designer's proposal (concept): x 110-490 (24.5 mm from the jack hole and from the right edge), z 3-5, rounded ends, drip-edge
chamfer, dark mesh 2-3 mm deep, internal sill 4 mm. Run: python 41_front_line.py -> 41_front_line.svg"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
K = 1.85           # px/mm, front view
OX, OY = 30, 110


def F(x, z):
    return OX + x * K, OY + (36 - z) * K


def main():
    el = ['<rect width="100%" height="100%" fill="#fff"/>',
          '<text x="24" y="30" font-size="18" font-weight="700" fill="#1f2933">Передняя линия входа воздуха (R195): вид музыканта и разрез (концепт дизайнера, 20.11.2026)</text>',
          '<text x="24" y="52" font-size="12" fill="#52606d">Сверху: передний торец, вид спереди (со стороны музыканта), x от левого края, z от низа корпуса, мм, без зеркала. Высота торца 30 (дека), ножки 3.</text>',
          '<text x="24" y="70" font-size="12" fill="#52606d">Серая пунктирная — линия в g3 сейчас (x 110–505); чёрная — предложение (x 110–490, отступы 24,5 = 24,5). Геометрия model3d/v8 g3.</text>']
    # front wall
    a, b = F(0, 30), F(515, 0)
    el.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" rx="3" fill="#2a2e33" stroke="#111"/>')
    for fx in (25, 470):                                 # feet
        a, b = F(fx, 0), F(fx + 20, -3)
        el.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" fill="#111"/>')
    a, b = F(-10, -3), F(525, -3)
    el.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#9aa5b1" stroke-dasharray="2 3"/>')
    el.append(f'<text x="{b[0] - 2:.0f}" y="{b[1] + 13:.0f}" font-size="10" fill="#9aa5b1" text-anchor="end">стол</text>')
    for x in (32, 80):                                   # phones jacks
        c = F(x, 11.35)
        el.append(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{5.5 * K:.1f}" fill="#0b0c0d" stroke="#8a949c" stroke-width="1.2"/>')
    a, b = F(110, 5), F(505, 3)                          # current line
    el.append(f'<rect x="{a[0]:.1f}" y="{a[1] - 7:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" fill="none" stroke="#9aa5b1" stroke-dasharray="4 3"/>')
    a, b = F(110, 5), F(490, 3)                          # proposal
    el.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" rx="{1 * K:.1f}" fill="#000"/>')
    for x, t in ((32, "PHONES 1"), (80, "PHONES 2")):
        c = F(x, 22)
        el.append(f'<text x="{c[0]:.1f}" y="{c[1]:.1f}" font-size="8" fill="#c9d1d6" text-anchor="middle">{t}</text>')
    # dimensions
    y = F(0, -12)[1]
    for x0, x1, t in ((85.5, 110, "24,5"), (110, 490, "380 (2 мм; 7,6 см²)"), (490, 515, "25")):
        a, b = F(x0, 0), F(x1, 0)
        el.append(f'<line x1="{a[0]:.1f}" y1="{y:.1f}" x2="{b[0]:.1f}" y2="{y:.1f}" stroke="#d64545"/>')
        el.append(f'<text x="{(a[0] + b[0]) / 2:.1f}" y="{y + 13:.1f}" font-size="10.5" fill="#d64545" text-anchor="middle">{t}</text>')
    c = F(455, 7.5)
    el.append(f'<text x="{c[0]:.0f}" y="{c[1] + 4:.0f}" font-size="10.5" fill="#c9d1d6">z 3–5</text>')
    c = F(32, 36)
    el.append(f'<text x="{c[0]:.0f}" y="{c[1]:.0f}" font-size="10" fill="#52606d" text-anchor="middle">x 32</text>')
    c = F(80, 36)
    el.append(f'<text x="{c[0]:.0f}" y="{c[1]:.0f}" font-size="10" fill="#52606d" text-anchor="middle">x 80</text>')

    # section at x 300, seen from the left: front of the case on the left
    S, SX, SY = 13.0, 70, 300
    def Q(yy, zz):
        return SX + yy * S, SY + (16 - zz) * S
    el.append(f'<text x="24" y="{SY - 30}" font-size="14" font-weight="700" fill="#1f2933">Разрез по x 300, вид слева (перед корпуса слева), масштаб ≈ 9:1</text>')
    wall = [(0, 0), (0, 3), (0, 5), (0, 16), (3, 16), (3, 3), (12, 3), (12, 0)]
    # outer front wall y 0-3 with the slot z 3-5, floor skin z 0-3
    parts = [[(0, 0), (12, 0), (12, 3), (3, 3), (3, 3), (0.0, 3)],          # floor + lower lip (below the slot)
             [(0, 5), (0, 16), (3, 16), (3, 5)]]                            # wall above the slot
    for poly in parts:
        el.append('<polygon points="' + " ".join("%.1f,%.1f" % Q(*p) for p in poly) + '" fill="#2a2e33" stroke="#111"/>')
    # drip edge: 0.8 mm chamfer at the top outer edge of the slot
    p = [Q(0, 5), Q(0, 5.8), Q(0.8, 5)]
    el.append('<polygon points="' + " ".join("%.1f,%.1f" % t for t in p) + '" fill="#fff" stroke="#111"/>')
    # mesh at y 3.5 and sill y 4.2-5.0, z 3-7
    a, b = Q(3.4, 5), Q(3.6, 3)
    el.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" fill="#55606a"/>')
    a, b = Q(4.2, 7), Q(5.0, 3)
    el.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" fill="#2a2e33" stroke="#111"/>')
    a, b = Q(6, 14), Q(12, 3.2)
    el.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" fill="#e9eef2" stroke="#9aa5b1" stroke-dasharray="4 3"/>')
    c = Q(9, 9)
    el.append(f'<text x="{c[0]:.0f}" y="{c[1]:.0f}" font-size="11" fill="#52606d" text-anchor="middle">аккумулятор</text>')
    el.append(f'<text x="{c[0]:.0f}" y="{c[1] + 14:.0f}" font-size="11" fill="#52606d" text-anchor="middle">(с y 6)</text>')
    # air arrow
    a, b, c2 = Q(-3, 4), Q(4.6, 4), Q(4.6, 8.5)
    el.append(f'<polyline points="{a[0]:.0f},{a[1]:.0f} {Q(3.9, 4)[0]:.0f},{a[1]:.0f} {Q(3.9, 8.5)[0]:.0f},{c2[1]:.0f} {Q(5.8, 8.5)[0]:.0f},{c2[1]:.0f}" fill="none" stroke="#2f80ed" stroke-width="2"/>')
    el.append(f'<text x="{Q(-3, 4)[0]:.0f}" y="{Q(-3, 4)[1] - 8:.0f}" font-size="11" fill="#2f80ed">воздух</text>')
    a, b = Q(-4, -0.0), Q(14, 0)
    el.append(f'<line x1="{a[0]:.0f}" y1="{Q(0, -3)[1]:.0f}" x2="{b[0]:.0f}" y2="{Q(0, -3)[1]:.0f}" stroke="#9aa5b1" stroke-dasharray="2 3"/>')
    el.append(f'<text x="{Q(13, -3)[0]:.0f}" y="{Q(0, -3)[1] + 14:.0f}" font-size="10" fill="#9aa5b1">стол (ножки 3)</text>')
    notes = ["① капельник: фаска 0,8 на верхней наружной кромке — капля со ската деки по торцу срывается, а не затекает",
             "② сетка от пыли тёмная, утоплена на 3–3,5 мм: линия читается как тень, а не как дырка с потрохами",
             "③ порожек 4 мм (z 3–7) в зазоре y 3–6 перед аккумуляторами: лужа на столе до 4 мм не проходит",
             "Проверить (инженер): место под порожек при аккумуляторах с y 6; прочность нижней губы 3 мм под линией;",
             "оснастка/печать прорези 2 × 380 в стенке 3 мм. Статус: предложение."]
    for i, t in enumerate(notes):
        el.append(f'<text x="{SX + 16 * S + 40}" y="{SY + 10 + i * 20}" font-size="11.5" fill="#1f2933">{t}</text>')
    W, H = 1010, 580
    for i, t in enumerate(["①", "②", "③"]):
        pos = (Q(1.4, 7.4), Q(3.5, -1.9), Q(6.0, 6.0))[i]
        el.append(f'<text x="{pos[0]:.0f}" y="{pos[1]:.0f}" font-size="12" fill="#b42318" text-anchor="middle">{t}</text>')
    open(os.path.join(HERE, "41_front_line.svg"), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Segoe UI, Arial, sans-serif">' + "".join(el) + "</svg>")
    print(W, H)


if __name__ == "__main__":
    main()
