#!/usr/bin/env python3
"""Doc 41 section 24.5: right wall with the single thin fan slot and the 3 mm feet (18.11.2026, engineer's decision on the fan).
Right wall seen from the RIGHT, so the FRONT of the case is at the RIGHT of the picture. y from the front edge, z from the outer floor.
Numbers (main engineer): fan 80 x 80 x 25 on the right wall, centre y 430.5, z 3.5-83.5 (as in the v8 model, g3); slot 60 x 3 mm, z 40, centred on the fan; four flat
square feet 3 mm high in the corners (size and place are the designer's proposal: 20 x 20 mm, 25 mm from the corners)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
S = 1.7
OX, OY, FOOT = 40, 70, 3
PROF = [(0, 0), (0, 30), (300, 30), (433.4, 117), (500, 117), (500, 0)]
Z0 = FOOT


def P(y, z):                                   # front on the right
    return OX + (500 - y) * S, OY + (130 - (z + Z0)) * S


def main():
    el = ['<rect width="100%" height="100%" fill="#fff"/>',
          '<text x="30" y="26" font-size="16" font-weight="700" fill="#1f2933">Правая стенка (вид справа: перед — справа) и ножки, мм</text>',
          '<text x="30" y="44" font-size="11" fill="#52606d">Одна тонкая прорезь 60 × 3 мм напротив вентилятора 80 × 80 × 25, в цвет корпуса, без решётки; четыре плоские ножки 3 мм.</text>']
    pts = " ".join(f"{P(y, z)[0]:.1f},{P(y, z)[1]:.1f}" for y, z in PROF)
    el.append(f'<polygon points="{pts}" fill="#2a2e33" stroke="#111" stroke-width="2" stroke-linejoin="round"/>')
    a, b = P(390.5, 83.5), P(470.5, 3.5)
    el.append(f'<rect x="{min(a[0], b[0])}" y="{a[1]}" width="{abs(b[0] - a[0])}" height="{b[1] - a[1]}" rx="6" fill="none" stroke="#ff7b72" stroke-width="1.4" stroke-dasharray="6 4"/>')
    el.append(f'<text x="{(a[0] + b[0]) / 2}" y="{a[1] + 16}" font-size="10" fill="#ff9d96" text-anchor="middle">вентилятор 80 × 80 × 25 (внутри)</text>')
    a, b = P(400.5, 41.5), P(460.5, 38.5)
    el.append(f'<rect x="{min(a[0], b[0])}" y="{a[1]}" width="{abs(b[0] - a[0])}" height="{b[1] - a[1]}" rx="1.5" fill="#050506" stroke="#5d6970" stroke-width="0.8"/>')
    c = P(430.5, 41.5)
    el.append(f'<line x1="{c[0]}" y1="{c[1] - 8}" x2="{c[0]}" y2="{c[1] - 34}" stroke="#e8ecea" stroke-width="1"/>')
    el.append(f'<text x="{c[0]}" y="{c[1] - 38}" font-size="11" font-weight="700" fill="#e8ecea" text-anchor="middle">прорезь 60 × 3, z 40</text>')
    for y0, y1 in ((25, 45), (455, 475)):
        a, b = P(y0, 0), P(y1, -FOOT)
        el.append(f'<rect x="{min(a[0], b[0])}" y="{a[1] - 0}" width="{abs(b[0] - a[0])}" height="{abs(b[1] - a[1])}" fill="#111" stroke="#555"/>')
    a, b = P(0, -FOOT - 14), P(500, -FOOT - 14)
    el.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#d64545"/><text x="{(a[0] + b[0]) / 2}" y="{a[1] + 14}" font-size="11" fill="#d64545" text-anchor="middle">500</text>')
    a = P(10, 0)
    el.append(f'<text x="{OX + 250 * S}" y="{OY + 133 * S + 44}" font-size="11" fill="#52606d" text-anchor="middle">ножки: 4 шт., 20 × 20 × 3, в 25 мм от углов</text>')
    W, H = OX * 2 + 500 * S, OY + 130 * S + 70
    open(os.path.join(HERE, "41_walls_v7.svg"), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" font-family="Segoe UI, Arial, sans-serif">' + "".join(el) + "</svg>")
    print(int(W), int(H))


if __name__ == "__main__":
    main()
