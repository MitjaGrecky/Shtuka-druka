#!/usr/bin/env python3
"""Rear panel sketch (proposal, not a decision): rear view, x from the left edge as seen from behind, z from the bottom.
Zones per doc 13 (3.3, 3.5), doc 34, R26 (inputs framed, outputs filled), R44 (rear wall 143 mm), R45 (English labels).
Writes docs/ru/img/rear_panel_v1.svg, .png and prints the R2 jack table (markdown).

  python3 tools/rear_panel.py

License: AGPL-3.0-or-later.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "docs", "ru", "img")
W, H = 515.0, 143.0          # rear wall: panel width (doc 13: ~515), height (R44)
R2_X = (5.0, 263.0)          # R2 zone in the rear view = panel x 252-510 seen from behind (x_rear = 515 - x_panel)
R1_X = (273.0, 511.0)

# kind: mini (3.5 mm PJ398SM, hole 6), din (5-pin DIN, ring 19), usbc, usba, dc, trs (6.3 mm, hole 11), combo, rca, gnd, sw
SIZE = {"mini": (6, 6), "din": (19, 19), "usbc": (9.4, 3.6), "usba": (13.5, 6.0), "dc": (11, 11), "trs": (11, 11),
        "combo": (24, 30), "rca": (10, 10), "gnd": (8, 8), "sw": (8, 4)}
J = []      # (board, zone, label, kind, x, z, direction)


def jack(board, zone, label, kind, x, z, d):
    J.append((board, zone, label, kind, x, z, d))


# ---------------------------------------------------------------- R2: power and USB (2 rows)
jack("R2", "POWER / USB", "DC 12-24V", "dc", 18, 35, "in")
jack("R2", "POWER / USB", "USB-C PD", "usbc", 46, 35, "in")
jack("R2", "POWER / USB", "USB-C PC", "usbc", 18, 70, "io")
jack("R2", "POWER / USB", "USB-A", "usba", 46, 70, "io")
# ---------------------------------------------------------------- R2: MIDI (DIN 3 x 2, TRS column)
jack("R2", "MIDI", "MIDI IN 1", "din", 84, 70, "in")
jack("R2", "MIDI", "MIDI IN 2", "din", 84, 35, "in")
for k, (x, z) in enumerate(((108, 70), (132, 70), (108, 35), (132, 35))):
    jack("R2", "MIDI", f"MIDI OUT {k + 1}", "din", x, z, "out")
jack("R2", "MIDI", "TRS IN", "mini", 158, 80, "in")
jack("R2", "MIDI", "TRS OUT 1", "mini", 158, 55, "out")
jack("R2", "MIDI", "TRS OUT 2", "mini", 158, 30, "out")
# ---------------------------------------------------------------- R2: CV and sync (6 x 3, pitch 14 x 25)
cols = [184 + 14.5 * i for i in range(6)]
for i, lab in enumerate(["CV IN 1", "CV IN 2", "CV IN 3", "CV IN 4", "CLK IN", "RESET IN"]):
    jack("R2", "CV / SYNC", lab, "mini", cols[i], 80, "in")
for i in range(6):
    jack("R2", "CV / SYNC", f"CV OUT {i + 1}", "mini", cols[i], 55, "out")
for i, lab in enumerate(["CV OUT 7", "CV OUT 8", "CLK OUT 1", "CLK OUT 2", "RESET OUT"]):
    jack("R2", "CV / SYNC", lab, "mini", cols[i], 30, "out")
# ---------------------------------------------------------------- R1: outputs (2 rows x 3)
for i, lab in enumerate(["MAIN L", "MAIN R", "AUX L"]):
    jack("R1", "OUTPUTS", lab, "trs", 285 + 23 * i, 75, "out")
jack("R1", "OUTPUTS", "AUX R", "trs", 285, 38, "out")
jack("R1", "OUTPUTS", "RCA L", "rca", 308, 38, "out")
jack("R1", "OUTPUTS", "RCA R", "rca", 331, 38, "out")
# ---------------------------------------------------------------- R1: inputs
jack("R1", "INPUTS", "MIC/LINE 1", "combo", 368, 75, "in")
jack("R1", "INPUTS", "MIC/LINE 2", "combo", 396, 75, "in")
jack("R1", "INPUTS", "HI-Z 1", "trs", 368, 35, "in")
jack("R1", "INPUTS", "HI-Z 2", "trs", 396, 35, "in")
jack("R1", "INPUTS", "PHONO L", "rca", 421, 82, "in")
jack("R1", "INPUTS", "PHONO R", "rca", 421, 60, "in")
jack("R1", "INPUTS", "GND", "gnd", 421, 39, "in")
jack("R1", "INPUTS", "PHONO/LINE", "sw", 421, 20, "in")
for i in range(8):
    jack("R1", "INPUTS", f"LINE {i + 1}", "trs", 443 + 21 * (i % 4), 75 if i < 4 else 38, "in")

ZONES = [("R2", "POWER / USB", 5, 63), ("R2", "MIDI", 71, 167), ("R2", "CV / SYNC", 175, 263),
         ("R1", "OUTPUTS", 273, 343), ("R1", "INPUTS", 353, 511)]


def svg():
    s = 2.4                                            # px per mm
    pad = 30
    w, h = W * s + 2 * pad, H * s + 2 * pad + 40
    X = lambda x: pad + x * s                          # noqa: E731
    Z = lambda z: pad + 40 + (H - z) * s               # noqa: E731
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" '
         'font-family="Helvetica, Arial, sans-serif">',
         f'<rect width="100%" height="100%" fill="#ffffff"/>',
         f'<text x="{pad}" y="22" font-size="15" font-weight="bold">Rear panel - proposal v1 (rear view, mm; R26: inputs framed, outputs filled)</text>',
         f'<rect x="{X(0)}" y="{Z(H)}" width="{W * s}" height="{H * s}" fill="#f4f4f2" stroke="#222" stroke-width="1.5"/>']
    # usable band: jack tops below ~116 mm at 40 mm depth (doc 13, 3.6)
    o.append(f'<line x1="{X(0)}" y1="{Z(116)}" x2="{X(W)}" y2="{Z(116)}" stroke="#c33" stroke-dasharray="6 4"/>'
             f'<text x="{X(W) - 4}" y="{Z(116) - 4}" font-size="10" fill="#c33" text-anchor="end">jack tops below ~116 mm (doc 13, 3.6)</text>')
    for b, (x0, x1) in (("R2 control board", R2_X), ("R1 audio board", R1_X)):
        o.append(f'<rect x="{X(x0)}" y="{Z(104)}" width="{(x1 - x0) * s}" height="{96 * s}" fill="none" stroke="#88a" '
                 f'stroke-dasharray="3 3"/><text x="{X(x0) + 4}" y="{Z(104) + 12}" font-size="10" fill="#557">{b} (z 8-104)</text>')
    for b, name, x0, x1 in ZONES:
        o.append(f'<text x="{X((x0 + x1) / 2)}" y="{Z(H) - 6}" font-size="11" font-weight="bold" text-anchor="middle">{name}</text>'
                 f'<line x1="{X(x0)}" y1="{Z(H) - 2}" x2="{X(x1)}" y2="{Z(H) - 2}" stroke="#222"/>')
    for b, zone, lab, kind, x, z, d in J:
        sw, sh = SIZE[kind]
        fill = "#2b2b2b" if d == "out" else "#ffffff"
        tcol = "#ffffff" if d == "out" else "#222"
        bw, bh = max(sw + 4, 13), sh + (14 if kind == "mini" else 12)
        # R26 marking: output = filled plate, input = frame
        o.append(f'<rect x="{X(x - bw / 2)}" y="{Z(z + sh / 2 + 3)}" width="{bw * s}" height="{bh * s}" rx="3" '
                 f'fill="{fill if d == "out" else "none"}" stroke="#222" stroke-width="{1.4 if d != "out" else 0}"/>')
        hole = "#bbbbbb" if d == "out" else "#dddddd"
        if kind in ("usbc", "usba", "sw"):
            o.append(f'<rect x="{X(x - sw / 2)}" y="{Z(z + sh / 2)}" width="{sw * s}" height="{sh * s}" rx="2" fill="{hole}" stroke="#222"/>')
        elif kind == "combo":
            o.append(f'<circle cx="{X(x)}" cy="{Z(z)}" r="{11 * s}" fill="{hole}" stroke="#222"/>'
                     f'<circle cx="{X(x)}" cy="{Z(z)}" r="{3.2 * s}" fill="#fff" stroke="#222"/>')
        else:
            o.append(f'<circle cx="{X(x)}" cy="{Z(z)}" r="{sw / 2 * s}" fill="{hole}" stroke="#222"/>')
        lines = lab.rsplit(" ", 1) if kind == "mini" and " " in lab else [lab]
        fs = (6.0 if len(lines[0]) > 7 else 7.0) if kind == "mini" else (7.5 if len(lab) > 9 else 8.5)
        for k, t in enumerate(lines):
            o.append(f'<text x="{X(x)}" y="{Z(z - sh / 2 - 4.5) + k * 9}" font-size="{fs}" text-anchor="middle" fill="{tcol}">{t}</text>')
    o.append(f'<text x="{pad}" y="{h - 8}" font-size="10" fill="#555">Proposal by Claude (cloud), 14.11.2026, task #20 - '
             f'positions are centres (x from the left seen from behind, z from the bottom). Not decided: see questions in notes/handoff.md.</text>')
    o.append("</svg>")
    return "\n".join(o), w, h


def main():
    os.makedirs(OUT, exist_ok=True)
    text, w, h = svg()
    p = os.path.join(OUT, "rear_panel_v1.svg")
    open(p, "w").write(text)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            pg = b.new_page(viewport={"width": int(w), "height": int(h)}, device_scale_factor=2)
            pg.goto("file://" + os.path.abspath(p))
            pg.screenshot(path=p[:-4] + ".png")
            b.close()
    except ImportError:
        print("playwright missing: PNG not written")
    print("| Jack | Zone | Kind | x (rear view) | z | Panel x | Direction |")
    print("|---|---|---|---|---|---|---|")
    for b, zone, lab, kind, x, z, d in J:
        if b == "R2":
            print(f"| {lab} | {zone} | {kind} | {x:g} | {z:g} | {W - x:g} | {d} |")


if __name__ == "__main__":
    main()
