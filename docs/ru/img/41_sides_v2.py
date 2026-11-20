#!/usr/bin/env python3
"""Doc 41 section 24.12: both side walls designed as one graphic, the fan exhaust hidden in it (user, 20.11.2026:
"play both sides beautifully; not necessarily as I drew, I only gave the meaning").

Three concepts, each identical on both walls (mirror), blind grooves everywhere, through-cuts only on the right wall inside
the fan frame (76 x 76 around the fan axis y 440.5, z 43.5):
  K1 "Sail"   - lines parallel to the slope, pitch 5, field = the wedge behind the deck fold (front edge vertical at y 310).
  K2 "Pipes"  - vertical bars, pitch 5, from z 10 up to the slope edge inset 10, y 310-500 (organ pipes rising with the slope).
  K3 "Release"- vertical bars, pitch 5, full height over the fan, then their tops decay exponentially towards the front
                (a sound envelope's release), the tail running under the deck to y ~ 180.
Outputs: 41_sides_v2_persp.svg (3/4 perspective: left wall from front-left, right wall from front-right) and
41_sides_v2_elev.svg (elevations: left wall from the LEFT, front on the left; right wall from the RIGHT, front on the right;
y depth from the front edge, z from the outer floor, mm; not mirrored beyond the natural view), 41_sides_v2.csv.
Geometry model3d/v8 g3: W 515, D 510, deck z 30 to y 300, slope 28.85 deg to y 463.4 / z 120; fan y 400.5-480.5, z 3.5-83.5.
Status: concept (designer's proposal); not checked by airflow test; strength of a 3 mm wall with 1-1.2 mm grooves not checked."""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
A = math.radians(28.85); TAN, COS = math.tan(A), math.cos(A)
W, D = 515.0, 510.0
FY0, FY1, FZ0, FZ1 = 400.5, 480.5, 3.5, 83.5
CY, CZ = 440.5, 43.5
WIN = (CY - 38, CY + 38, CZ - 38, CZ + 38)
PROF = [(0, 0), (0, 30), (300, 30), (463.4, 120), (510, 120), (510, 0)]
INS, PITCH = 10.0, 5.0


def slope_line(y, off=0.0):
    return 30 + (y - 300) * TAN - off


def top_inset(y):
    return min(max(30 - INS, slope_line(y, INS / COS)), 120 - INS)


def clip_param(fn, y0, y1, ok, n=4000):
    """y-interval of [y0, y1] where ok(y, fn(y)) holds (assumes one interval)"""
    ys = [y0 + (y1 - y0) * i / n for i in range(n + 1)]
    good = [y for y in ys if ok(y, fn(y))]
    return (good[0], good[-1]) if good else None


# ---------- concepts: list of segments ((y0, z0), (y1, z1)) ----------
def k1():
    segs, k = [], 0
    while True:
        off = INS / COS + k * PITCH / COS
        f = lambda y, o=off: slope_line(y, o)
        if f(D - INS) < INS: break
        r = clip_param(f, 310, D - INS, lambda y, z: INS <= z <= top_inset(y))
        if r and r[1] - r[0] > 8: segs.append(((r[0], f(r[0])), (r[1], f(r[1]))))
        k += 1
    return segs


def k2():
    segs = []
    y = D - INS
    while y >= 310:
        t = top_inset(y)
        if t - INS > 4: segs.append(((y, INS), (y, t)))
        y -= PITCH
    return segs


def k3():
    segs = []
    e0 = top_inset(400)
    y = D - INS
    while y > 100:
        if y >= 400: t = top_inset(y)
        else: t = min(top_inset(y), INS + (e0 - INS) * math.exp(-(400 - y) / 55))
        if t - INS < 1.5: break
        segs.append(((y, INS), (y, t)))
        y -= PITCH
    return segs


CONCEPTS = [("K1", "Парус", "линии ∥ скату, шаг 5, поле — клин за перегибом деки", k1),
            ("K2", "Трубы", "вертикальные штрихи, шаг 5, верх по скату", k2),
            ("K3", "Затухание", "вертикальные штрихи, верх затухает к переду, как release", k3)]


def through(segs):
    out = []
    for (y0, z0), (y1, z1) in segs:
        if abs(y1 - y0) < 1e-6:                          # vertical
            if WIN[0] + 1 <= y0 <= WIN[1] - 1:
                a, b = max(z0, WIN[2] + 1), min(z1, WIN[3] - 1)
                if b - a > 3: out.append(((y0, a), (y0, b)))
        else:
            f = lambda y: z0 + (z1 - z0) * (y - y0) / (y1 - y0)
            r = clip_param(f, max(y0, WIN[0]), min(y1, WIN[1]), lambda y, z: WIN[2] + 1 <= z <= WIN[3] - 1, 800)
            if r and r[1] - r[0] > 3: out.append(((r[0], f(r[0])), (r[1], f(r[1]))))
    return out


def seg_dist(p, a, b):
    (px, pz), (ax, az), (bx, bz) = p, a, b
    dx, dz = bx - ax, bz - az
    L = dx * dx + dz * dz
    t = 0 if L == 0 else max(0, min(1, ((px - ax) * dx + (pz - az) * dz) / L))
    return math.hypot(px - ax - t * dx, pz - az - t * dz)


def measure(cuts, step=0.1):
    g = b = 0
    for iy in range(int(80 / step)):
        y = WIN[0] - 2 + (iy + .5) * step
        near = [c for c in cuts if min(c[0][0], c[1][0]) - 1.1 <= y <= max(c[0][0], c[1][0]) + 1.1]
        if not near: continue
        for iz in range(int(80 / step)):
            z = WIN[2] - 2 + (iz + .5) * step
            if any(seg_dist((y, z), a, bb) <= 1.0 for a, bb in near):
                g += 1
                if 17 <= math.hypot(y - CY, z - CZ) <= 39: b += 1
    a = step * step / 100
    return round(g * a, 1), round(b * a, 1)


# ---------- perspective ----------
def camera(eye, look, f=1100.0):
    ex, ey, ez = eye
    fx, fy, fz = (look[0] - ex, look[1] - ey, look[2] - ez)
    n = math.sqrt(fx * fx + fy * fy + fz * fz); fx, fy, fz = fx / n, fy / n, fz / n
    rx, ry, rz = fy * 1 - fz * 0, fz * 0 - fx * 1, 0.0               # right = f x up(0,0,1)
    n = math.hypot(rx, ry); rx, ry = rx / n, ry / n
    ux, uy, uz = ry * fz - rz * fy, rz * fx - rx * fz, rx * fy - ry * fx
    def P(p):
        dx, dy, dz = p[0] - ex, p[1] - ey, p[2] - ez
        zc = dx * fx + dy * fy + dz * fz
        return (f * (dx * rx + dy * ry + dz * rz) / zc, -f * (dx * ux + dy * uy + dz * uz) / zc, zc)
    return P


FACES = [  # (points, outward normal, shade)
    ([(W, y, z) for y, z in PROF], (1, 0, 0), "#3a3f45"),
    ([(0, y, z) for y, z in PROF], (-1, 0, 0), "#3a3f45"),
    ([(0, 0, 0), (W, 0, 0), (W, 0, 30), (0, 0, 30)], (0, -1, 0), "#454b52"),
    ([(0, 0, 30), (W, 0, 30), (W, 300, 30), (0, 300, 30)], (0, 0, 1), "#50575e"),
    ([(0, 300, 30), (W, 300, 30), (W, 463.4, 120), (0, 463.4, 120)], (0, -math.sin(A), math.cos(A)), "#4a5158"),
    ([(0, 463.4, 120), (W, 463.4, 120), (W, D, 120), (0, D, 120)], (0, 0, 1), "#50575e"),
    ([(0, D, 0), (W, D, 0), (W, D, 120), (0, D, 120)], (0, 1, 0), "#30353a"),
]


def persp(bx, by, bw, bh, eye, look, segs, cuts, right):
    """3/4 view auto-fitted into the box (bx, by, bw, bh)"""
    P0 = camera(eye, look)
    vis = []
    for pts, nrm, col in FACES:
        c = [sum(p[i] for p in pts) / len(pts) for i in range(3)]
        if sum(nrm[i] * (eye[i] - c[i]) for i in range(3)) <= 0: continue
        pr = [P0(p) for p in pts]
        vis.append((sum(p[2] for p in pr) / len(pr), pr, col))
    xs = [p[0] for _, pr, _ in vis for p in pr]; ys = [p[1] for _, pr, _ in vis for p in pr]
    sc = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    ox = bx + (bw - (max(xs) - min(xs)) * sc) / 2 - min(xs) * sc
    oy = by + (bh - (max(ys) - min(ys)) * sc) / 2 - min(ys) * sc
    el = []
    for _, pr, col in sorted(vis, key=lambda t: -t[0]):
        el.append('<polygon points="' + " ".join("%.1f,%.1f" % (ox + p[0] * sc, oy + p[1] * sc) for p in pr) +
                  f'" fill="{col}" stroke="#1d2024" stroke-width="0.8" stroke-linejoin="round"/>')
    x = W if right else 0.0
    def line(a, b, col, w):
        p, q = P0((x, a[0], a[1])), P0((x, b[0], b[1]))
        s = sc * 1100 / ((p[2] + q[2]) / 2) * w
        return f'<line x1="{ox + p[0] * sc:.1f}" y1="{oy + p[1] * sc:.1f}" x2="{ox + q[0] * sc:.1f}" y2="{oy + q[1] * sc:.1f}" stroke="{col}" stroke-width="{max(s, 0.6):.2f}" stroke-linecap="round"/>'
    for a, b in segs:
        el.append(line((a[0], a[1] - 0.9), (b[0], b[1] - 0.9), "#646c74", 0.8))
        el.append(line(a, b, "#17191c", 2.0))
    if right:
        for a, b in cuts:
            el.append(line(a, b, "#0e0f11", 2.0))
    p, q = P0((110, 0, 4)), P0((490, 0, 4))
    el.append(f'<line x1="{ox + p[0] * sc:.1f}" y1="{oy + p[1] * sc:.1f}" x2="{ox + q[0] * sc:.1f}" y2="{oy + q[1] * sc:.1f}" stroke="#0b0c0d" stroke-width="1.4"/>')
    return el


def elev(ox, oy, k, right, segs, cuts):
    T = lambda y, z: (ox + ((D - y) if right else y) * k, oy + (124 - z) * k)
    el = ['<polygon points="' + " ".join("%.1f,%.1f" % T(y, z) for y, z in PROF) + '" fill="#3a3f45" stroke="#111" stroke-width="1.1" stroke-linejoin="round"/>']
    for a, b in segs:
        p, q = T(*a), T(*b)
        el.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="#16181b" stroke-width="{2 * k:.2f}" stroke-linecap="round"/>')
    if right:
        for a, b in cuts:
            p, q = T(*a), T(*b)
            el.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="#000" stroke-width="{2 * k:.2f}" stroke-linecap="round"/>')
        p, q = T(FY1, FZ1), T(FY0, FZ0)
        el.append(f'<rect x="{p[0]:.1f}" y="{p[1]:.1f}" width="{q[0] - p[0]:.1f}" height="{q[1] - p[1]:.1f}" rx="3" fill="none" stroke="#ff7b72" stroke-width="0.8" stroke-dasharray="4 3"/>')
    return el


def main():
    data = []
    for key, name, desc, fn in CONCEPTS:
        segs = fn(); cuts = through(segs); area = measure(cuts)
        data.append((key, name, desc, segs, cuts, area))
        print(key, name, len(segs), "grooves,", len(cuts), "through,", area)
    # perspective sheet
    CW, CH = 560, 330
    Wp, Hp = 2 * CW + 30, 120 + 3 * CH
    el = ['<rect width="100%" height="100%" fill="#fff"/>',
          '<text x="20" y="30" font-size="19" font-weight="700" fill="#1f2933">Боковины одним рисунком: три концепта, вид 3/4</text>',
          '<text x="20" y="52" font-size="12.5" fill="#52606d">Слева — корпус спереди-слева (видна левая стенка), справа — спереди-справа (правая). Рисунок на обеих стенках одинаковый, зеркальный.</text>',
          '<text x="20" y="70" font-size="12.5" fill="#52606d">Тёмное — глухие канавки 2 мм (глубина 1–1,2, дно тёмное); чёрное — сквозные, только справа над вентилятором. Внизу спереди — линия входа R195.</text>',
          '<text x="20" y="88" font-size="12.5" fill="#52606d">Геометрия model3d/v8 g3, перспектива без деталей деки. Статус: концепт дизайнера, 20.11.2026.</text>']
    for i, (key, name, desc, segs, cuts, area) in enumerate(data):
        oy = 110 + i * CH
        el.append(f'<rect x="10" y="{oy}" width="{Wp - 20}" height="{CH - 12}" rx="12" fill="#eef0ec"/>')
        el.append(f'<text x="26" y="{oy + 26}" font-size="15.5" font-weight="700" fill="#1f2933">{key}. {name}</text>')
        el.append(f'<text x="26" y="{oy + 45}" font-size="12" fill="#52606d">{desc}; сквозные {str(area[0]).replace(".", ",")} см², над лопастями {str(area[1]).replace(".", ",")} см²</text>')
        el += persp(24, oy + 56, CW - 40, CH - 80, (-620, 40, 300), (90, 330, 40), segs, cuts, False)
        el += persp(24 + CW, oy + 56, CW - 40, CH - 80, (W + 620, 40, 300), (W - 90, 330, 40), segs, cuts, True)
    open(os.path.join(HERE, "41_sides_v2_persp.svg"), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wp} {Hp}" width="{Wp}" height="{Hp}" font-family="Segoe UI, Arial, sans-serif">' + "".join(el) + "</svg>")
    # elevation sheet
    k = 1.0
    We, He = int(2 * D * k + 60), 110 + 3 * int(124 * k + 60)
    el = ['<rect width="100%" height="100%" fill="#fff"/>',
          '<text x="20" y="28" font-size="17" font-weight="700" fill="#1f2933">Боковины, виды сбоку (размеры к 24.12)</text>',
          '<text x="20" y="48" font-size="12" fill="#52606d">Левая — вид слева (перед слева); правая — вид справа (перед справа). y — глубина от переднего края, z — от низа, мм; масштаб 1 px = 1 мм.</text>',
          '<text x="20" y="66" font-size="12" fill="#52606d">Пунктир — вентилятор 80 × 80 (y 400,5–480,5, z 3,5–83,5). Канавки 2 мм, шаг 5, отступ от кромок 10. Геометрия g3.</text>']
    for i, (key, name, desc, segs, cuts, area) in enumerate(data):
        oy = 90 + i * int(124 * k + 60)
        el.append(f'<text x="20" y="{oy + 12}" font-size="13.5" font-weight="700" fill="#1f2933">{key}. {name}: сквозные {str(area[0]).replace(".", ",")} см² ({len(segs)} канавок, {len(cuts)} сквозных отрезков)</text>')
        el += elev(20, oy + 22, k, False, segs, cuts)
        el += elev(40 + D * k, oy + 22, k, True, segs, cuts)
    open(os.path.join(HERE, "41_sides_v2_elev.svg"), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {We} {He}" width="{We}" height="{He}" font-family="Segoe UI, Arial, sans-serif">' + "".join(el) + "</svg>")
    with open(os.path.join(HERE, "41_sides_v2.csv"), "w", encoding="utf-8") as f:
        f.write("concept,name,grooves,through_segments,through_cm2,over_blades_cm2\n")
        for key, name, desc, segs, cuts, area in data:
            f.write(f"{key},{name},{len(segs)},{len(cuts)},{area[0]},{area[1]}\n")
    print(Wp, Hp, We, He)


if __name__ == "__main__":
    main()
