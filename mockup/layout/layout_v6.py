#!/usr/bin/env python3
"""Shtuka Druka - top panel layout v6 (single source of truth).

Coordinates in mm: x from the left edge, y from the FRONT edge (towards the screen).
Deck (flat) y 0..312, wedge (30 deg, shown in top projection) y 312..442, shelf 442..472 (P66).
License: AGPL-3.0-or-later (code), CERN-OHL-S-2.0 (hardware data).
"""
import json, math, sys

W, D, WEDGE0, WEDGE1 = 515, 472, 312, 442   # depth 500 -> 472, shelf stays 30 mm (P66)
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

# ---------------- LEFT ZONE: time (left hand), x 8..106 ----------------
for i, (n, c) in enumerate([("● Rec", "red"), ("▶ Play", "green"), ("■ Stop", "white")]):
    btn(n, 24 + 33 * i, 28, 28, 24, "Transport", color=c, freq="часто, в долю")
for i, n in enumerate(["Restart", "Metronome", "Tap"]):
    btn(n, 24 + 33 * i, 58, 28, 14, "Transport", freq="иногда")
btn("Capture", 32, 98, 44, 24, "Capture", color="teal", freq="часто")
btn("Resample", 82, 98, 44, 24, "Capture", color="teal", freq="иногда")
edit = [["Undo", "Redo", "Delete"], ["Duplicate", "Double", "New"], ["Quantize", "Length", "Automate"]]
for r, row in enumerate(edit):
    for c, n in enumerate(row):
        btn(n, 24 + 33 * c, 140 + 24 * r, 30, 18, "Edit", freq="часто" if n in ("Undo", "Delete", "Duplicate") else "иногда")
btn("Repeat", 32, 224, 44, 18, "Repeat", freq="часто")
btn("Accent", 82, 224, 44, 18, "Repeat", freq="иногда")
knob("Tempo", 32, 278, 18, "Tempo", freq="иногда")
knob("Swing", 82, 278, 18, "Tempo", freq="редко")

# ---------------- CENTER: pads 25.5 x 21 mm (wider, for two fingers, R106), pitch 28 x 25 ----------------
PX = [123.75 + 28 * i for i in range(8)]
PY = [56.5 + 25 * j for j in range(8)]
btn("Arrow ◄", 120, 22, 15, 14, "Grid scroll", label="◄", freq="часто", note="ход потуже")
other("strip", "Touch strip", 222, 22, 178, 18, "Strip", label="MOD · SCROLL")
btn("Arrow ►", 325, 22, 15, 14, "Grid scroll", label="►", freq="часто", note="ход потуже")
for j in range(8):
    for i in range(8):
        other("pad", f"Pad {i+1}.{8-j}", PX[i], PY[j], 25.5, 21, "Grid", color=TRACK[7 - j])
for i in range(8):
    btn(f"Scene {i+1}", PX[i], 256, 22, 10, "Scenes", label=str(i + 1), freq="часто, в долю")
btn("Stop All", 352, 256, 30, 10, "Scenes", freq="иногда")
btn("Solo", 345, 28, 18, 14, "Tracks", color="blue", note="держать + Select", freq="иногда")
btn("Arm", 367, 28, 18, 14, "Tracks", color="red", note="держать + Select", freq="иногда")
btn("Arrow ▼", 391, 28, 15, 14, "Grid scroll", label="▼", freq="часто")
btn("Arrow ▲", 391, 256, 15, 10, "Grid scroll", label="▲", freq="часто")
for j in range(8):
    y = PY[j]
    n = 8 - j  # track 1 is the far row, like the list on the screen
    btn(f"Mute {n}", 345, y, 16, 16, "Tracks", label="M", color="amber", freq="постоянно, в долю")
    btn(f"Select {n}", 367, y, 16, 16, "Tracks", label=str(n), color=TRACK[n - 1], freq="постоянно")
    knob(f"Level {n}", 391, y, 14, "Tracks", label="", ring=21, color=TRACK[n - 1], note="низкая, с касанием", freq="часто")
SCX = 275   # screen centre, shifted 20 mm right (P66)
for k in range(8):
    knob(f"Param {k+1}", SCX - 95 + 27.14 * k, 286, 18, "Screen knobs", label="", ring=24, color="purple",
         note="низкая, с касанием", freq="постоянно")

# ---------------- RIGHT ZONE: values (right hand), x 406..507 ----------------
btn("Scene A", 412, 24, 14, 12, "Live", label="A", color="red")
other("fader", "Crossfader", 456, 24, 64, 4, "Live", label="Scene A ↔ B")
btn("Scene B", 500, 24, 14, 12, "Live", label="B", color="blue")
gm = [["Chords", "Touch FX", "Scale"], ["Clips", "Steps", "Notes"]]  # front -> back
for r, row in enumerate(gm):
    for c, n in enumerate(row):
        btn(n, 422 + 34 * c, 56 + 24 * r, 30, 16, "Pad modes", color="teal" if n != "Scale" else "grey", freq="часто")
btn("Back", 432, 126, 50, 16, "Navigation", freq="часто")
btn("Page ◄", 419, 152, 24, 14, "Navigation", label="◄ Page", freq="часто")
btn("Page ►", 445, 152, 24, 14, "Navigation", label="Page ►", freq="часто")
other("wheel", "Wheel", 484, 139, 42, 42, "Navigation", label="")
sm = [["Inputs", "Browser"], ["Sampler", "Song"], ["Mod", "Mixer"], ["Sound", "Effects"]]  # front -> back
for r, row in enumerate(sm):
    for c, n in enumerate(row):
        btn(n, 419 + 27 * c, 200 + 24 * r, 25, 15, "Screen modes", color="purple", freq="часто")
knob("FX Mix", 485, 214, 26, "Live", ring=34, color="coral", freq="часто")
knob("Filter", 485, 264, 26, "Live", ring=34, color="coral", freq="часто")

# ---------------- WEDGE (top projection y 312..442) ----------------
for i, n in enumerate(["Main", "Phones 1", "Phones 2", "Cue Mix"]):
    knob(n, 22 + 30 * i, 336, 15, "Levels", kind="pot", color="alu",
         freq="редко, аварийно" if n == "Main" else ("иногда" if n.startswith("Phones") else "редко"))
knob("Gain 1", 37, 378, 16, "Levels", note="утоплен", freq="редко")
knob("Gain 2", 97, 378, 16, "Levels", note="утоплен", freq="редко")
other("led", "Clip 1", 55, 378, 4, 4, "Levels", color="red")
other("led", "Clip 2", 115, 378, 4, 4, "Levels", color="red")
btn("P48 1", 37, 416, 18, 10, "Levels", label="P48", color="amber", note="утоплена, удержание 1 с", freq="редко")
btn("P48 2", 97, 416, 18, 10, "Levels", label="P48", color="amber", note="утоплена, удержание 1 с", freq="редко")
other("meter", "Meter L", 135, 377, 5, 104, "Levels", label="L")
other("meter", "Meter R", 143, 377, 5, 104, "Levels", label="R")
other("screen", "Screen 10.1in", SCX, 377, 240, 126, "Screen")
btn("Save", 428, 334, 44, 14, "System", freq="иногда")
btn("Project", 480, 334, 44, 14, "System", freq="редко")
other("pocket", "USB-A + SD", 445, 372, 74, 18, "System", label="USB · SD")
other("led", "Busy", 493, 372, 4, 4, "System", color="red")
btn("Settings", 428, 410, 44, 14, "System", freq="редко")
other("power", "Power", 486, 410, 14, 14, "System", note="утоплена, удержание 2 с")

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
    json.dump({"W": W, "D": D, "F0": WEDGE0, "F1": WEDGE1, "elements": E}, open("layout_v6.json", "w"), ensure_ascii=False, indent=1)
