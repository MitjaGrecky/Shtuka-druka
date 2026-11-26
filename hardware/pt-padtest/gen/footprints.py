#!/usr/bin/env python3
"""Footprints of the 4 x 4 pad test board (R194, P120) into the shared project library: 8 interdigitated electrode pads
(zones as quadrants or triangles, 7 or 10 mil comb, two light-slot sizes) and the reverse-mount RGB LED under them.

Electrode footprint: pad 1 = common electrode (a frame round the 21 x 17 mm field with its fingers), pads 2..5 = the four
zones (quad: top-left, top-right, bottom-left, bottom-right; tri: top, right, bottom, left). Fingers and gaps have the same
width (7 mil = 0.178 mm or 10 mil = 0.254 mm). The mask is open over the whole field (the FSR film lies on the ENIG copper).
The finger length is found numerically: the longest rectangle that keeps one gap to the zone's bus.

LED footprint: pads and slot of the EasyEDA / LCSC library footprint of C51933363 (GL6028RGB01-B, common anode on pad 3);
the pads are shortened at the inner end from x 1.85 to 1.95 mm, so that the copper keeps 0.2 mm from the routed slot
(the library has 0.1 mm). The 4 mm variant stretches the slot along y only.   License: AGPL-3.0-or-later.
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.abspath(os.path.join(HERE, "..", "..", "m1-screen-knobs", "lib", "ShtukaDruka.pretty"))

FX, FY = 10.5, 8.5                    # half size of the comb field: 21 x 17 mm (P120)
RING = 0.5                            # width of the common frame
XI, YI = FX - RING, FY - RING
BW = 0.3                              # width of a zone bus
SLOT_X = 1.75                         # half width of the light slot (library)
CUTS = {"31": 1.55, "40": 2.0}        # half height of the slot: 3.1 mm ("3 mm" variant, library) and 4.0 mm ("4 mm")
EDGE = 0.3                            # copper to slot edge
GAPS = {"7": 0.1778, "10": 0.254}
KT = FY * 2 / (FX * 2)                # slope of the diagonals of the triangle zones
LED_NAME = "LED_RGB_6028_ReverseMount_C51933363_slot{}"
PAD_NAME = "PT44_comb_{}_{}mil_slot{}"


def seg_dist(p, a, b):
    ax, ay = a
    dx, dy = b[0] - ax, b[1] - ay
    t = 0.0 if dx == dy == 0 else max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)


def rect_clear(x0, y0, x1, y1, line, limit):
    """True if every segment of the polyline stays at least `limit` from the rectangle (sampled, 0.01 mm)."""
    for a, b in zip(line, line[1:]):
        n = max(2, int(math.hypot(b[0] - a[0], b[1] - a[1]) / 0.01) + 1)
        for i in range(n + 1):
            px, py = a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n
            if px < x0 - limit or px > x1 + limit or py < y0 - limit or py > y1 + limit:
                continue
            if math.hypot(max(x0 - px, 0, px - x1), max(y0 - py, 0, py - y1)) < limit:
                return False
    return True


def longest(rect_of, lmax, line, limit):
    """Largest length l in [0, lmax] for which rect_of(l) is clear of the line."""
    if rect_clear(*rect_of(lmax), line, limit):
        return lmax
    lo, hi = 0.0, lmax
    for _ in range(14):
        mid = (lo + hi) / 2
        if rect_clear(*rect_of(mid), line, limit):
            lo = mid
        else:
            hi = mid
    return lo


def quad_zone(g, ky):
    """Top-right quadrant: (bus polyline, anchor, zone fingers, common fingers)."""
    kx = SLOT_X + EDGE + BW / 2
    x0, y0 = 0.55, 0.45
    ytop = YI - g - BW / 2
    yk = ky + EDGE + BW / 2
    bus = [(x0, ytop), (x0, yk), (kx, yk), (kx, y0)]
    zone, com = [], []
    k = 0
    y = YI - g - g / 2
    while y - g / 2 >= y0 - BW / 2 - 1e-9:
        if k % 2 == 0:
            xs = x0 if y >= yk else kx
            zone.append((xs, y - g / 2, XI - g, y + g / 2))
        else:
            rect = lambda l, y=y: (XI - l, y - g / 2, XI, y + g / 2)      # noqa: E731
            l = longest(rect, XI - 0.1, bus, BW / 2 + g + 0.002)
            if l > 0.3:
                com.append(rect(l))
        y -= 2 * g
        k += 1
    return bus, (x0, ytop), zone, com


def tri_zone(g, ky, side):
    """Triangle zone: side "v" = top triangle (vertical fingers), "h" = right triangle (horizontal fingers)."""
    kx = SLOT_X + EDGE + BW / 2
    yk = ky + EDGE + BW / 2
    zone, com = [], []
    if side == "v":
        off = 0.55
        xm = (YI - g - BW / 2 - off) / KT
        xf = max(0.0, min(kx, (yk - off) / KT))            # flat part under the slot
        right = [(xf, max(KT * xf + off, yk)), (max(xf, kx), max(KT * max(xf, kx) + off, yk if xf >= kx else 0)), (xm, KT * xm + off)]
        bus = [(-x, y) for x, y in reversed(right)] + right
        n = int(xm / (2 * g))
        for i in range(-n, n + 1):
            x = i * 2 * g
            if i % 2 == 0:
                ys = max(KT * abs(x) + off, yk if abs(x) <= xf else 0)
                if YI - g - ys > 0.3:
                    zone.append((x - g / 2, ys, x + g / 2, YI - g))
            else:
                rect = lambda l, x=x: (x - g / 2, YI - l, x + g / 2, YI)  # noqa: E731
                l = longest(rect, YI - 0.1, bus, BW / 2 + g + 0.002)
                if l > 0.3:
                    com.append(rect(l))
        return bus, (0.0, bus[len(bus) // 2][1]), zone, com
    off = 0.65
    ym = (XI - g - BW / 2 - off) * KT
    yf = (kx - off) * KT                                   # vertical part beside the slot, up to where the diagonal reaches it
    upper = [(kx, yf), (ym / KT + off, ym)]
    bus = [(x, -y) for x, y in reversed(upper)] + upper
    n = int(ym / (2 * g))
    for i in range(-n, n + 1):
        y = i * 2 * g
        if i % 2 == 0:
            xs = max(abs(y) / KT + off, kx if abs(y) <= yf else 0)
            if XI - g - xs > 0.3:
                zone.append((xs, y - g / 2, XI - g, y + g / 2))
        else:
            rect = lambda l, y=y: (XI - l, y - g / 2, XI, y + g / 2)      # noqa: E731
            l = longest(rect, XI - 0.1, bus, BW / 2 + g + 0.002)
            if l > 0.3:
                com.append(rect(l))
    return bus, (kx, 0.0), zone, com


def mirror(z, sx, sy):
    bus, a, zone, com = z
    m = lambda p: (sx * p[0], sy * p[1])                    # noqa: E731
    r = lambda q: (min(sx * q[0], sx * q[2]), min(sy * q[1], sy * q[3]), max(sx * q[0], sx * q[2]), max(sy * q[1], sy * q[3]))  # noqa: E731
    return [m(p) for p in bus], m(a), [r(q) for q in zone], [r(q) for q in com]


def f(v):
    return f"{v:.4f}".rstrip("0").rstrip(".") if abs(v) > 5e-5 else "0"


def poly(rect, ax, ay):
    x0, y0, x1, y1 = rect
    pts = "".join(f"(xy {f(x - ax)} {f(y - ay)})" for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)))
    return f"        (gr_poly (pts {pts}) (width 0) (fill yes))\n"


def pad(num, anchor, rects, lines, size):
    ax, ay = anchor
    prim = "".join(poly(r, ax, ay) for r in rects)
    prim += "".join(f"        (gr_line (start {f(a[0] - ax)} {f(a[1] - ay)}) (end {f(b[0] - ax)} {f(b[1] - ay)}) (width {BW}))\n"
                    for line in lines for a, b in zip(line, line[1:]) if math.hypot(b[0] - a[0], b[1] - a[1]) > 1e-6)
    return (f'  (pad "{num}" smd custom (at {f(ax)} {f(ay)}) (size {size} {size}) (layers "F.Cu")\n'
            f'    (options (clearance outline) (anchor circle))\n    (primitives\n{prim}    ))\n')


def head(name, descr, attr):
    return (f'(footprint "{name}" (version 20221018) (generator pt44)\n  (layer "F.Cu")\n  (descr "{descr}")\n  (attr {attr})\n'
            f'  (fp_text reference "REF**" (at 0 -10) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))\n'
            f'  (fp_text value "{name}" (at 0 10) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))\n')


def rect_gfx(x, y, layer, width, fill="none"):
    return (f'  (fp_rect (start {f(-x)} {f(-y)}) (end {f(x)} {f(y)}) (stroke (width {width}) (type solid)) (fill {fill}) '
            f'(layer "{layer}"))\n')


def electrode(kind, mil, slot):
    g, ky = GAPS[mil], CUTS[slot]
    if kind == "quad":
        tr = quad_zone(g, ky)
        zones = [mirror(tr, -1, 1), tr, mirror(tr, -1, -1), mirror(tr, 1, -1)]
        # KiCad y grows downwards: "top" is negative y
        zones = [mirror(z, 1, -1) for z in zones]
    else:
        v, h = tri_zone(g, ky, "v"), tri_zone(g, ky, "h")
        zones = [mirror(v, 1, -1), h, v, mirror(h, -1, 1)]          # top, right, bottom, left
    name = PAD_NAME.format(kind, mil, slot)
    s = head(name, f"Pad test comb {kind} zones, {mil} mil, light slot {slot}, field 21 x 17 mm (R194, P120)",
             "smd exclude_from_pos_files exclude_from_bom allow_soldermask_bridges")
    ring = [(-FX, -FY, FX, -YI), (-FX, YI, FX, FY), (-FX, -FY, -XI, FY), (XI, -FY, FX, FY)]
    com = ring + [r for z in zones for r in z[3]]
    s += pad("1", (-(FX + XI) / 2, 0.0), com, [], 0.4)
    for n, (bus, anchor, fingers, _) in enumerate(zones, 2):
        s += pad(str(n), anchor, fingers, [bus], BW)
    s += rect_gfx(FX + 0.15, FY + 0.15, "F.Mask", 0, "solid")
    s += rect_gfx(FX + 0.25, FY + 0.25, "F.CrtYd", 0.05)
    s += (f'  (fp_text user "{kind[0].upper()}{mil} S{slot}" (at 0 {f(FY + 1.4)}) (layer "F.SilkS") '
          f'(effects (font (size 1 1) (thickness 0.15))))\n)\n')
    open(os.path.join(LIB, name + ".kicad_mod"), "w", encoding="utf-8", newline="\n").write(s)
    return name, [len(z[2]) for z in zones], [len(z[3]) for z in zones]


def led(slot):
    ky, r = CUTS[slot], 0.4
    name = LED_NAME.format(slot)
    s = head(name, "Reverse-mount RGB 6028, common anode pad 3 (EasyEDA/LCSC footprint of C51933363, pads shortened to x 1.95; "
             f"slot 3.5 x {2 * ky:g} mm)", "smd")
    for num, x, y in (("3", -2.75, -0.73), ("1", -2.75, 0.73), ("2", 2.75, 0.73), ("4", 2.75, -0.73)):
        s += f'  (pad "{num}" smd rect (at {x} {y}) (size 1.6 0.8) (layers "F.Cu" "F.Paste" "F.Mask"))\n'
    x = SLOT_X
    edge = '(stroke (width 0.05) (type solid)) (layer "Edge.Cuts")'
    for a, b in (((-x + r, -ky), (x - r, -ky)), ((x, -ky + r), (x, ky - r)), ((x - r, ky), (-x + r, ky)), ((-x, ky - r), (-x, -ky + r))):
        s += f'  (fp_line (start {f(a[0])} {f(a[1])}) (end {f(b[0])} {f(b[1])}) {edge})\n'
    c = r * (1 - math.sqrt(0.5))
    for a, m, b in (((x - r, -ky), (x - c, -ky + c), (x, -ky + r)), ((x, ky - r), (x - c, ky - c), (x - r, ky)),
                    ((-x + r, ky), (-x + c, ky - c), (-x, ky - r)), ((-x, -ky + r), (-x + c, -ky + c), (-x + r, -ky))):
        s += f'  (fp_arc (start {f(a[0])} {f(a[1])}) (mid {f(m[0])} {f(m[1])}) (end {f(b[0])} {f(b[1])}) {edge})\n'
    s += rect_gfx(3.8, max(ky + 0.3, 1.65), "F.CrtYd", 0.05)
    s += ")\n"
    open(os.path.join(LIB, name + ".kicad_mod"), "w", encoding="utf-8", newline="\n").write(s)
    return name


if __name__ == "__main__":
    for slot in CUTS:
        print(led(slot))
        for kind in ("quad", "tri"):
            for mil in GAPS:
                print(*electrode(kind, mil, slot))
