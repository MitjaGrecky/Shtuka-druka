#!/usr/bin/env python3
"""Shtuka Druka - top panel layout v7 (single source of truth).

Design system (P69):
- Four column bands run the full depth of the body, deck and wedge alike:
  left 10-102 (time; Levels on the wedge) | grid 110-331.5 (pads; screen on the wedge) |
  tracks 339-405 (mixer; meters on the wedge) | right 413-505 (values; System on the wedge).
- Every control sits on the 25 mm pad-row rhythm: strip line, rows 1-8, scene line, knob line.
- One centre column system: pad column k = scene button k = screen knob k = screen column k (28 mm).
  The screen window is as wide as the pad grid.
- Side columns mirror each other row for row: 3 keys | 2-3 keys | gap | 3x3 block | gap | one row | - | knob line.
  One 4 mm gutter between keys: 3 keys 28 wide or 2 keys 44 wide across 92 mm.
- Three key sizes: big 28x22 (transport), standard 28x16, pair 44x16.

Coordinates in mm: x from the left edge, y from the FRONT edge. Deck y 0..300, wedge (30 deg, top
projection) y 300..430, shelf 430..460.
License: AGPL-3.0-or-later (code), CERN-OHL-S-2.0 (hardware data).
"""
import json, math, sys

W, D, WEDGE0, WEDGE1 = 515, 460, 300, 430
AXIS = W / 2
STRIP, SCENE, KNOBS = 22, 252, 277
ROW = [52 + 25 * j for j in range(8)]          # row 1 (front) .. row 8 (back)
ROWS = {"strip": STRIP, "rows": ROW, "scene": SCENE, "knobs": KNOBS}
LC = (10, 102)      # left column
GRID = (110, 331.5)  # pads
TC = (339, 405)     # track column
RC = (413, 505)     # right column
E = []  # elements


def btn(name, x, y, w, h, group, label=None, color="grey", hand=None, freq="", note=""):
    E.append(dict(kind="button", name=name, x=x, y=y, w=w, h=h, group=group,
                  label=label if label is not None else name, color=color, freq=freq, note=note))


def knob(name, x, y, d, group, label=None, kind="encoder", ring=None, color="grey", freq="", note=""):
    E.append(dict(kind=kind, name=name, x=x, y=y, w=d, h=d, group=group,
                  label=label if label is not None else name, ring=ring or d + 7,
                  color=color, freq=freq, note=note))


def other(kind, name, x, y, w, h, group, label="", color="grey", note=""):
    E.append(dict(kind=kind, name=name, x=x, y=y, w=w, h=h, group=group, label=label, color=color, note=note))


TRACK = ['#e8564a', '#f0a23a', '#e7d24a', '#55c26b', '#3fc39d', '#4aa8e8', '#7f77dd', '#d4537e']
L3 = [24, 56, 88]          # three keys across the left column
R3 = [427, 459, 491]       # three keys across the right column
L2, R2 = [32, 80], [435, 483]  # two keys across a column
R4 = [423, 447, 471, 495]      # four keys across the right column

# ---------------- LEFT COLUMN: time (left hand) ----------------
for x, (n, c) in zip(L3, [("● Rec", "red"), ("▶ Play", "green"), ("■ Stop", "white")]):
    btn(n, x, STRIP, 28, 22, "Transport", color=c, freq="часто, в долю")
for x, n in zip(L3, ["Restart", "Metronome", "Tap"]):
    btn(n, x, ROW[0], 28, 16, "Transport", freq="иногда")
btn("Capture", L2[0], ROW[1], 44, 16, "Capture", color="teal", freq="часто")
btn("Resample", L2[1], ROW[1], 44, 16, "Capture", color="teal", freq="иногда")
edit = [["Undo", "Redo", "Delete"], ["Duplicate", "Double", "New"], ["Quantize", "Length", "Automate"]]
for r, rowk in enumerate(edit):
    for x, n in zip(L3, rowk):
        btn(n, x, ROW[3 + r], 28, 16, "Edit", freq="часто" if n in ("Undo", "Delete", "Duplicate") else "иногда")
btn("Repeat", L2[0], ROW[7], 44, 16, "Repeat", freq="часто")
btn("Accent", L2[1], ROW[7], 44, 16, "Repeat", freq="иногда")
knob("Tempo", L2[0], KNOBS, 22, "Knob line", ring=30, freq="иногда")
knob("Swing", L2[1], KNOBS, 22, "Knob line", ring=30, freq="редко")

# ---------------- CENTER: strip, pads, scenes, screen knobs ----------------
GX = (GRID[0] + GRID[1]) / 2                     # centre of the grid = centre of the screen
PX = [GRID[0] + 12.75 + 28 * i for i in range(8)]
btn("Arrow ◄", GRID[0] + 8, STRIP, 16, 14, "Grid scroll", label="◄", freq="часто", note="ход потуже")
other("strip", "Touch strip", GX, STRIP, GRID[1] - GRID[0] - 40, 18, "Strip", label="")
btn("Arrow ►", GRID[1] - 8, STRIP, 16, 14, "Grid scroll", label="►", freq="часто", note="ход потуже")
for j in range(8):
    for i in range(8):
        other("pad", f"Pad {i+1}.{8-j}", PX[i], ROW[j], 25.5, 21, "Grid", color=TRACK[7 - j])
for i in range(8):
    btn(f"Scene {i+1}", PX[i], SCENE, 25.5, 10, "Scenes", label=str(i + 1), freq="часто, в долю")
for k in range(8):
    knob(f"Param {k+1}", PX[k], KNOBS, 18, "Knob line", label="", ring=24, color="purple",
         note="низкая, с касанием", freq="постоянно")

# ---------------- TRACK COLUMN ----------------
MX, SX, KX = 349, 371, 394.5
TX = (TC[0] + TC[1]) / 2
btn("Solo", MX, STRIP, 16, 14, "Tracks", color="blue", note="держать + Select", freq="иногда")
btn("Arm", SX, STRIP, 16, 14, "Tracks", color="red", note="держать + Select", freq="иногда")
btn("Arrow ▼", KX, STRIP, 16, 14, "Grid scroll", label="▼", freq="часто")
for j in range(8):
    n = 8 - j
    btn(f"Mute {n}", MX, ROW[j], 16, 16, "Tracks", label="M", color="amber", freq="постоянно, в долю")
    btn(f"Select {n}", SX, ROW[j], 16, 16, "Tracks", label=str(n), color=TRACK[n - 1], freq="постоянно")
    knob(f"Level {n}", KX, ROW[j], 14, "Tracks", label="", ring=21, color=TRACK[n - 1], note="низкая, с касанием", freq="часто")
btn("Stop All", (MX + SX) / 2, SCENE, 38, 10, "Scenes", freq="иногда")
btn("Arrow ▲", KX, SCENE, 16, 10, "Grid scroll", label="▲", freq="часто")
knob("FX Mix", TX - 17, KNOBS, 22, "Knob line", ring=30, color="coral", freq="часто")
knob("Filter", TX + 17, KNOBS, 22, "Knob line", ring=30, color="coral", freq="часто")

# ---------------- RIGHT COLUMN: values (right hand), mirrors the left column row for row ----------------
btn("Scene A", 421, STRIP, 14, 12, "Live", label="A", color="red")
other("fader", "Crossfader", 459, STRIP, 52, 4, "Live", label="")
btn("Scene B", 497, STRIP, 14, 12, "Live", label="B", color="blue")
for x, n in zip(R3, ["Chords", "Touch FX", "Scale"]):
    btn(n, x, ROW[0], 28, 16, "Pad modes", color="teal" if n != "Scale" else "grey", freq="часто")
for x, n in zip(R3, ["Clips", "Steps", "Notes"]):
    btn(n, x, ROW[1], 28, 16, "Pad modes", color="teal", freq="часто")
# screen pages 3 x 3 (rows 4-6), mirrors Edit: the track's sound / the whole project / sources and device
pages = [["Sound", "Effects", "Mod"], ["Mixer", "Song", "Browser"], ["Sampler", "Inputs", "Settings"]]
for r, rowk in enumerate(pages):
    for x, n in zip(R3, rowk):
        btn(n, x, ROW[3 + r], 28, 16, "Screen modes", color="purple", freq="редко" if n == "Settings" else "часто")
# screen navigation: three keys on row 8, the wheel on the knob line right above them (push = OK)
for x, (n, lab) in zip(R3, [("Page ◄", "◄ Page"), ("Back", "Back"), ("Page ►", "Page ►")]):
    btn(n, x, ROW[7], 28, 16, "Navigation", label=lab, freq="часто")
other("wheel", "Wheel", R3[1], KNOBS, 38, 38, "Navigation", label="")

# ---------------- WEDGE (top projection y 300..430): every block sits over its deck column ----------------
SC = 365                                   # screen centre (top projection)
WR = [SC - 42, SC - 14, SC + 14, SC + 42]  # four wedge rows, 28 mm apart, centred on the screen
for (x, y, n, f) in [(L2[0], WR[0], "Main", "редко, аварийно"), (L2[1], WR[0], "Cue Mix", "редко"),
                     (L2[0], WR[1], "Phones 1", "иногда"), (L2[1], WR[1], "Phones 2", "иногда")]:
    knob(n, x, y, 15, "Levels", kind="pot", color="alu", freq=f)
knob("Gain 1", L2[0], WR[2], 16, "Levels", ring=21, note="утоплен", freq="редко")
knob("Gain 2", L2[1], WR[2], 16, "Levels", ring=21, note="утоплен", freq="редко")
other("led", "Clip 1", L2[0] + 16, WR[2] + 7, 4, 4, "Levels", color="red")
other("led", "Clip 2", L2[1] + 16, WR[2] + 7, 4, 4, "Levels", color="red")
btn("P48 1", L2[0], WR[3], 20, 10, "Levels", label="P48", color="amber", note="утоплена, удержание 1 с", freq="редко")
btn("P48 2", L2[1], WR[3], 20, 10, "Levels", label="P48", color="amber", note="утоплена, удержание 1 с", freq="редко")
# window = active area of a 10.1" 16:10 panel (217.5 x 136 mm) + 2.75 mm; 141 mm along the slope = 122 in projection
other("screen", "Screen 10.1in", GX, SC, 223, 122, "Screen")
other("meter", "Meter L", TX - 8, SC, 9, 104, "Meters", label="L")
other("meter", "Meter R", TX + 8, SC, 9, 104, "Meters", label="R")
btn("Save", R2[0], WR[0], 44, 16, "System", freq="иногда")
btn("Project", R2[1], WR[0], 44, 16, "System", freq="редко")
other("pocket", "USB-A + SD", (RC[0] + RC[1]) / 2, SC, 92, 24, "System", label="USB · SD", note="огонь записи внутри кармана")
other("power", "Power", (RC[0] + RC[1]) / 2, WR[3], 14, 14, "System", note="утоплена, удержание 2 с")

# =============== CHECKS ===============
def bbox(e, pad=0):
    w = e.get("ring", e["w"]) if e["kind"] in ("encoder", "pot") else e["w"]
    h = e.get("ring", e["h"]) if e["kind"] in ("encoder", "pot") else e["h"]
    return (e["x"] - w / 2 - pad, e["y"] - h / 2 - pad, e["x"] + w / 2 + pad, e["y"] + h / 2 + pad)


def overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


problems = []
ctl = [e for e in E if e["kind"] not in ("zone", "screen", "meter")]
for i in range(len(ctl)):
    for j in range(i + 1, len(ctl)):
        if overlap(bbox(ctl[i], 1), bbox(ctl[j], 1)):
            problems.append(f"overlap/clearance<2mm: {ctl[i]['name']} <-> {ctl[j]['name']}")
# pitch rules: knobs >= 25 mm c-c, buttons >= 19 mm c-c (nearest neighbour of same kind class)
knobs = [e for e in E if e["kind"] in ("encoder", "pot", "wheel")]
btns = [e for e in E if e["kind"] == "button"]
pads = [e for e in E if e["kind"] == "pad"]
def mind(lst):
    out = []
    for a in lst:
        d = min(math.hypot(a["x"] - b["x"], a["y"] - b["y"]) for b in lst if b is not a)
        out.append((d, a["name"]))
    return sorted(out)[:3]
kmin, bmin = mind(knobs), mind(btns)
if kmin[0][0] < 25 - 1e-6: problems.append(f"knob pitch < 25: {kmin}")
if bmin[0][0] < 19 - 1e-6: problems.append(f"button pitch < 19: {bmin}")
for e in E:
    x0, y0, x1, y1 = bbox(e)
    if x0 < 5 or x1 > W - 5 or y0 < 3 or y1 > WEDGE1 - 2:
        problems.append(f"too close to edge: {e['name']} {tuple(round(v,1) for v in (x0,y0,x1,y1))}")
    if e["kind"] not in ("screen", "zone") and y0 - 2 < WEDGE0 < y1 + 2:
        problems.append(f"on the fold line: {e['name']}")
freq_far = [e["name"] for e in E if e.get("freq", "").startswith(("часто", "постоянно")) and e["y"] > 330]

counts = {
    "buttons": len(btns), "encoders": sum(e["kind"] == "encoder" for e in E),
    "pots": sum(e["kind"] == "pot" for e in E), "pads": len(pads),
}
if __name__ == "__main__":
    print(json.dumps(counts, ensure_ascii=False))
    print("knob min pitch", [(round(d, 1), n) for d, n in kmin])
    print("button min pitch", [(round(d, 1), n) for d, n in bmin])
    print("frequent beyond 330 mm:", freq_far)
    print("problems:", len(problems))
    for p in problems: print(" -", p)
    json.dump({"W": W, "D": D, "F0": WEDGE0, "F1": WEDGE1, "rows": ROWS, "elements": E}, open("layout_v7.json", "w"), ensure_ascii=False, indent=1)
