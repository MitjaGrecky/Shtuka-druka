#!/usr/bin/env python3
"""Convert an EasyEDA (LCSC library) through-hole footprint to a KiCad .kicad_mod - for connectors that KiCad's library
lacks (CUI SDS-50J DIN-5, Kycon KLDHCX DC jack). Reads the JSON that EasyEDA's public component API returns
(https://easyeda.com/api/products/<LCSC>/components?version=6.4.19.5), saved to a file first.

Handles: round and oval (slotted) through-hole pads, plain holes (NPTH), the body rectangle (layer 99) as F.Fab and the
courtyard (+0.25 mm), silkscreen tracks (layer 3). The footprint origin is the centre of the pad field (the board writer
centres connectors on it). Unnumbered pads (EasyEDA "E", shield tabs) become mechanical pads with no number.

Usage: lcsc_fp.py JSON NAME OUT_DIR [--descr TEXT] [--rename 1=S,2=T,3=R]        License: AGPL-3.0-or-later.
"""
import argparse
import json
import re

U = 0.254      # EasyEDA standard unit (10 mil) in mm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("name")
    ap.add_argument("out_dir")
    ap.add_argument("--descr", default="")
    ap.add_argument("--rename", default="", help="pad renames, e.g. 1=S,2=T,3=R (to match the KiCad symbol's pin numbers)")
    a = ap.parse_args()
    d = json.load(open(a.json, encoding="utf-8"))["result"]
    shapes = d["packageDetail"]["dataStr"]["shape"]
    pads, holes, body, silk = [], [], None, []
    for s in shapes:
        f = s.split("~")
        if f[0] == "PAD":
            kind, x, y, w, h, num, hole_r = f[1], float(f[2]), float(f[3]), float(f[4]), float(f[5]), f[8], float(f[9] or 0)
            rot = float(f[11] or 0)
            slot = float(f[13]) if len(f) > 13 and f[13] else 0.0
            pts = [float(v) for v in f[10].split()] if f[10].strip() else []
            horiz = len(pts) >= 4 and abs(pts[2] - pts[0]) >= abs(pts[3] - pts[1])   # slot direction from its end points
            pads.append((kind, x, y, w, h, num, hole_r, rot, slot, horiz))
        elif f[0] == "HOLE":
            holes.append((float(f[1]), float(f[2]), float(f[3])))
        elif f[0] == "SOLIDREGION" and f[1] == "99":
            xs, ys, r = [], [], 0.0
            for cmd, args in re.findall(r"([MLA])\s*([-\d.,\s]+)", f[3]):
                v = [float(t) for t in re.split(r"[\s,]+", args.strip()) if t]
                if cmd == "A":                                  # rx ry rot large sweep x y: keep the end point and radius
                    r = max(r, v[0])
                    v = v[5:7]
                xs += v[0::2]
                ys += v[1::2]
            if r:                                               # circle made of arcs: centre +- r
                mx, my = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
                body = (mx - r, my - r, mx + r, my + r)
            else:
                body = (min(xs), min(ys), max(xs), max(ys))
        elif f[0] == "TRACK" and f[2] == "3":
            pts = [float(v) for v in f[4].split()]
            silk.append(list(zip(pts[0::2], pts[1::2])))
    cx = (min(p[1] for p in pads) + max(p[1] for p in pads)) / 2
    cy = (min(p[2] for p in pads) + max(p[2] for p in pads)) / 2
    X = lambda v: round((v - cx) * U, 4)                     # noqa: E731
    Y = lambda v: round((v - cy) * U, 4)                     # noqa: E731
    o = [f'(footprint "{a.name}" (version 20221018) (generator lcsc_fp)', '  (layer "F.Cu")',
         f'  (descr "{a.descr} (from the EasyEDA/LCSC footprint {d["packageDetail"]["title"]}, LCSC {d["lcsc"]["number"]})")',
         '  (attr through_hole)',
         f'  (fp_text reference "REF**" (at 0 {Y(body[1]) - 1.5:g}) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))',
         f'  (fp_text value "{a.name}" (at 0 {Y(body[3]) + 1.5:g}) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))']
    x0, y0, x1, y1 = X(body[0]), Y(body[1]), X(body[2]), Y(body[3])
    o.append(f'  (fp_rect (start {x0:g} {y0:g}) (end {x1:g} {y1:g}) (stroke (width 0.1) (type solid)) (fill none) (layer "F.Fab"))')
    # courtyard: body and pads, +0.25
    px0 = min([x0] + [X(p[1]) - max(p[3], p[4]) * U / 2 for p in pads]) - 0.25
    px1 = max([x1] + [X(p[1]) + max(p[3], p[4]) * U / 2 for p in pads]) + 0.25
    py0 = min([y0] + [Y(p[2]) - max(p[3], p[4]) * U / 2 for p in pads]) - 0.25
    py1 = max([y1] + [Y(p[2]) + max(p[3], p[4]) * U / 2 for p in pads]) + 0.25
    o.append(f'  (fp_rect (start {px0:g} {py0:g}) (end {px1:g} {py1:g}) (stroke (width 0.05) (type solid)) (fill none) (layer "F.CrtYd"))')
    for line in silk:
        for (ax, ay), (bx, by) in zip(line, line[1:]):
            o.append(f'  (fp_line (start {X(ax):g} {Y(ay):g}) (end {X(bx):g} {Y(by):g}) (stroke (width 0.12) (type solid)) (layer "F.SilkS"))')
    ren = dict(kv.split("=") for kv in a.rename.split(",") if kv)
    for kind, x, y, w, h, num, hr, rot, slot, horiz in pads:
        num = "" if not num.isdigit() else ren.get(num, num)
        size_w, size_h = w * U, h * U
        drill_d = 2 * hr * U
        if kind == "OVAL" and slot:                           # slot and the pad's long side along the hole's end points
            slot_l = slot * U
            lo, sh = max(size_w, size_h), min(size_w, size_h)
            size_w, size_h = (lo, sh) if horiz else (sh, lo)
            drill = f"(drill oval {slot_l:g} {drill_d:g})" if horiz else f"(drill oval {drill_d:g} {slot_l:g})"
            shape = "oval"
        else:
            drill = f"(drill {drill_d:g})"
            shape = "circle" if kind == "ELLIPSE" else ("rect" if kind == "RECT" else "oval")
        o.append(f'  (pad "{num}" thru_hole {shape} (at {X(x):g} {Y(y):g}) (size {size_w:g} {size_h:g}) {drill} '
                 f'(layers "*.Cu" "*.Mask"))')
    for x, y, r in holes:
        dd = 2 * r * U
        o.append(f'  (pad "" np_thru_hole circle (at {X(x):g} {Y(y):g}) (size {dd:g} {dd:g}) (drill {dd:g}) (layers "*.Cu" "*.Mask"))')
    o.append(")")
    path = f"{a.out_dir}/{a.name}.kicad_mod"
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(o) + "\n")
    print("ok", path, len(pads), "pads", len(holes), "holes; body", (x0, y0, x1, y1))


if __name__ == "__main__":
    main()
