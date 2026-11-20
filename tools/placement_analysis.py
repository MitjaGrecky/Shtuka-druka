#!/usr/bin/env python3
"""Why a placed board does not route: geometry of the placement and of every unrouted connection (no router, no kicad-cli).

  python tools/placement_analysis.py hardware/<board>/<board>.kicad_pcb [DRC_JSON ...] [--md OUT.md]

Placement metrics (courtyards, pads, nearest-neighbour gaps, walls of parts) come from the placed board through pcbnew (KiCad Python).
For each 'unconnected_items' entry of a DRC json (kicad-cli drc --format json of a routed copy) the two ends are looked up and the
straight line between them is tested against the courtyards. Units: mm. License: AGPL-3.0-or-later.
"""
import json
import math
import os
import re
import sys

import pcbnew

MM = 1e-6


def mm(v):
    return v * MM


class Part:
    def __init__(self, f):
        self.ref = f.GetReference()
        self.side = "B" if f.GetLayer() == pcbnew.B_Cu else "F"
        cy = f.GetCourtyard(pcbnew.B_CrtYd if self.side == "B" else pcbnew.F_CrtYd)
        if cy.OutlineCount():
            b = cy.BBox()
            self.box = (mm(b.GetX()), mm(b.GetY()), mm(b.GetRight()), mm(b.GetBottom()))
        else:
            b = f.GetBoundingBox(False, False)
            self.box = (mm(b.GetX()), mm(b.GetY()), mm(b.GetRight()), mm(b.GetBottom()))
        self.pads = [(mm(p.GetPosition().x), mm(p.GetPosition().y), p.GetNetname(), p.GetNumber(), mm(p.GetSizeX()), mm(p.GetSizeY())) for p in f.Pads()]
        self.value = f.GetValue()
        self.npads = len(self.pads)


def rect_gap(a, b):
    dx = max(b[0] - a[2], a[0] - b[2], 0.0)
    dy = max(b[1] - a[3], a[1] - b[3], 0.0)
    return math.hypot(dx, dy)


def seg_rect_hit(p, q, r, margin=0.0):
    """Liang-Barsky: does the segment p-q cross the rectangle r (grown by margin)?"""
    x0, y0, x1, y1 = r[0] - margin, r[1] - margin, r[2] + margin, r[3] + margin
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pp == 0:
            if qq < 0:
                return False
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def pt_rect_dist(p, r):
    return rect_gap((p[0], p[1], p[0], p[1]), r)


def analyse_board(path):
    b = pcbnew.LoadBoard(path)
    bb = b.GetBoardEdgesBoundingBox()
    area_box = (mm(bb.GetX()), mm(bb.GetY()), mm(bb.GetRight()), mm(bb.GetBottom()))
    W, H = area_box[2] - area_box[0], area_box[3] - area_box[1]
    parts = [Part(f) for f in b.GetFootprints() if f.GetReference() and not f.GetReference().startswith("H")]
    res = {"W": W, "H": H, "parts": parts, "box": area_box, "layers": b.GetCopperLayerCount()}
    # coverage of the board by courtyards, per side (raster 0.25 mm)
    step = 0.25
    nx, ny = int(W / step) + 1, int(H / step) + 1
    cov = {"F": set(), "B": set()}
    for p in parts:
        for ix in range(int((p.box[0] - area_box[0]) / step), int((p.box[2] - area_box[0]) / step) + 1):
            for iy in range(int((p.box[1] - area_box[1]) / step), int((p.box[3] - area_box[1]) / step) + 1):
                if 0 <= ix < nx and 0 <= iy < ny:
                    cov[p.side].add((ix, iy))
    total = nx * ny
    res["cov_F"], res["cov_B"] = 100.0 * len(cov["F"]) / total, 100.0 * len(cov["B"]) / total
    res["cov_any"] = 100.0 * len(cov["F"] | cov["B"]) / total
    npads = sum(p.npads for p in parts)
    res["npads"] = npads
    res["pad_density"] = npads / (W * H / 100.0)
    # nearest courtyard gap per part (same side)
    gaps = []
    for i, p in enumerate(parts):
        g = min((rect_gap(p.box, q.box) for j, q in enumerate(parts) if j != i and q.side == p.side), default=99.0)
        gaps.append(g)
    gaps.sort()
    res["gap_median"] = gaps[len(gaps) // 2]
    res["gap_lt05"] = 100.0 * sum(1 for g in gaps if g < 0.5) / len(gaps)
    res["gap_lt10"] = 100.0 * sum(1 for g in gaps if g < 1.0) / len(gaps)
    res["gap_lt20"] = 100.0 * sum(1 for g in gaps if g < 2.0) / len(gaps)
    # fine-pitch ICs: pad pitch <= 0.65 and >= 8 pads
    fine = []
    for p in parts:
        if p.npads >= 8:
            pts = [(x, y) for x, y, *_ in p.pads]
            d = sorted(math.hypot(a[0] - c[0], a[1] - c[1]) for a in pts[:6] for c in pts if c is not a)
            pitch = min((v for v in d if v > 0.05), default=9)
            if pitch <= 0.66:
                fine.append((p.ref, p.value, p.npads, round(pitch, 2)))
    res["fine"] = fine
    # walls: parts on one side in a band, chained with gaps < 0.8 mm
    walls = []
    for side in ("F", "B"):
        ps = [p for p in parts if p.side == side]
        for axis in (0, 1):                          # 0: row along x (same y band), 1: column along y
            used = set()
            ps_sorted = sorted(ps, key=lambda p: (p.box[1 - axis] + p.box[3 - axis]) / 2)
            for p in ps_sorted:
                if p.ref in used:
                    continue
                c0 = (p.box[1 - axis] + p.box[3 - axis]) / 2
                band = [q for q in ps if abs((q.box[1 - axis] + q.box[3 - axis]) / 2 - c0) < 1.6]
                band.sort(key=lambda q: q.box[axis])
                chain = [band[0]] if band else []
                for q in band[1:]:
                    if q.box[axis] - chain[-1].box[axis + 2] < 0.8:
                        chain.append(q)
                    else:
                        if len(chain) >= 4 and chain[-1].box[axis + 2] - chain[0].box[axis] >= 12.0:
                            walls.append((side, "x" if axis == 0 else "y", len(chain), round(chain[-1].box[axis + 2] - chain[0].box[axis], 1), chain[0].ref + ".." + chain[-1].ref))
                        chain = [q]
                if len(chain) >= 4 and chain[-1].box[axis + 2] - chain[0].box[axis] >= 12.0:
                    walls.append((side, "x" if axis == 0 else "y", len(chain), round(chain[-1].box[axis + 2] - chain[0].box[axis], 1), chain[0].ref + ".." + chain[-1].ref))
                used.update(q.ref for q in band)
    res["walls"] = sorted(set(walls), key=lambda w: -w[3])[:6]
    return res


def ends_of(item):
    d = item["description"]
    m = re.search(r"\[([^\]]*)\]", d)
    return (item["pos"]["x"], item["pos"]["y"]), (m.group(1) if m else "?"), d


def analyse_unrouted(res, drc):
    out = []
    parts = res["parts"]
    for u in drc.get("unconnected_items", []):
        if len(u["items"]) < 2:
            continue
        a, net, da = ends_of(u["items"][0])
        c, _, dc = ends_of(u["items"][1])
        length = math.hypot(a[0] - c[0], a[1] - c[1])
        crossed = [p.ref for p in parts if seg_rect_hit(a, c, p.box) and not (pt_rect_dist(a, p.box) < 0.3 or pt_rect_dist(c, p.box) < 0.3)]
        # clearance profile along the line to the nearest courtyard that does not contain the end points
        worst = 99.0
        steps = max(4, int(length / 0.5))
        for k in range(1, steps):
            t = k / steps
            pt = (a[0] + (c[0] - a[0]) * t, a[1] + (c[1] - a[1]) * t)
            g = min((pt_rect_dist(pt, p.box) for p in parts if pt_rect_dist(a, p.box) > 0.3 and pt_rect_dist(c, p.box) > 0.3), default=99.0)
            worst = min(worst, g)
        # other-net pads near the ends
        near = []
        for e in (a, c):
            n = 0
            for p in parts:
                for x, y, nn, num, sx, sy in p.pads:
                    if nn != net and math.hypot(x - e[0], y - e[1]) < 1.0:
                        n += 1
            near.append(n)
        # local courtyard coverage: fraction of a 6x6 mm window around each end covered by courtyards (any side)
        cov = []
        for e in (a, c):
            tot = hit = 0
            for ix in range(12):
                for iy in range(12):
                    pt = (e[0] - 3 + (ix + 0.5) * 0.5, e[1] - 3 + (iy + 0.5) * 0.5)
                    tot += 1
                    if any(p.box[0] <= pt[0] <= p.box[2] and p.box[1] <= pt[1] <= p.box[3] for p in parts):
                        hit += 1
            cov.append(round(100.0 * hit / tot))
        out.append(dict(net=net, a=a, c=c, ref_a=da[:60], ref_c=dc[:60], length=length, crossed=crossed, worst=worst, near=near, cov=cov))
    return out


def report(path, drcs, md):
    res = analyse_board(path)
    name = os.path.basename(path).replace(".kicad_pcb", "")
    L = []
    L.append(f"### {name}: {res['W']:.0f} x {res['H']:.0f} mm, {res['layers']} layers, {len(res['parts'])} parts, {res['npads']} pads")
    L.append("")
    L.append(f"- pad density {res['pad_density']:.0f} per cm2; courtyards cover {res['cov_any']:.0f} % of the board (F {res['cov_F']:.0f} %, B {res['cov_B']:.0f} %)")
    L.append(f"- nearest courtyard gap per part: median {res['gap_median']:.2f} mm; < 0.5 mm: {res['gap_lt05']:.0f} % of parts, < 1 mm: {res['gap_lt10']:.0f} %, < 2 mm: {res['gap_lt20']:.0f} %")
    L.append("- fine-pitch ICs (pitch <= 0.65 mm): " + (", ".join(f"{r} {v} ({n} pins, {p} mm)" for r, v, n, p in res["fine"]) or "none"))
    L.append("- walls (>= 4 parts in a row, gaps < 0.8 mm, >= 12 mm): " + ("; ".join(f"{s}:{ax} {n} parts {ln} mm ({r})" for s, ax, n, ln, r in res["walls"]) or "none"))
    for dj in drcs:
        d = json.load(open(dj, encoding="utf-8"))
        un = analyse_unrouted(res, d)
        L.append("")
        L.append(f"Unrouted in `{dj}`: {len(un)}")
        L.append("")
        L.append("| net | end A | end B | length | courtyards crossed | min clearance on the line | foreign pads <= 1 mm at ends | courtyard cover around ends % |")
        L.append("|---|---|---|---|---|---|---|---|")
        for u in sorted(un, key=lambda u: -u["length"])[:25]:
            L.append(f"| {u['net']} | ({u['a'][0]:.1f}, {u['a'][1]:.1f}) {u['ref_a'][:34]} | ({u['c'][0]:.1f}, {u['c'][1]:.1f}) {u['ref_c'][:34]} | {u['length']:.1f} | {','.join(u['crossed'][:8]) or '-'}{'+' if len(u['crossed'])>8 else ''} | {u['worst']:.2f} | {u['near'][0]}/{u['near'][1]} | {u['cov'][0]}/{u['cov'][1]} |")
    text = "\n".join(L)
    print(text)
    if md:
        with open(md, "a", encoding="utf-8") as f:
            f.write(text + "\n\n")
    return res


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    md = None
    if "--md" in sys.argv:
        md = sys.argv[sys.argv.index("--md") + 1]
        args = [a for a in args if a != md]
    report(args[0], args[1:], md)
