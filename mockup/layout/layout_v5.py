#!/usr/bin/env python3
"""Shtuka Druka - top panel layout v5 (single source of truth).

Coordinates in mm: x from the left edge, y from the FRONT edge (towards the screen).
Deck (flat) y 0..340, wedge (30 deg, shown in top projection) y 340..470, shelf 470..500.
License: AGPL-3.0-or-later (code), CERN-OHL-S-2.0 (hardware data).
"""
import json, math, sys

W, D, WEDGE0, WEDGE1 = 515, 500, 340, 470
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

# ---------------- LEFT ZONE: time (left hand), x 8..108 ----------------
for i, (n, c) in enumerate([("● Rec", "red"), ("▶ Play", "green"), ("■ Stop", "white")]):
    btn(n, 24 + 34 * i, 27, 28, 24, "Transport", color=c, freq="часто, в долю")
for i, n in enumerate(["Restart", "Metronome", "Tap"]):
    btn(n, 24 + 34 * i, 56, 28, 14, "Transport", freq="иногда")
btn("Capture", 31, 90, 44, 22, "Capture", color="teal", freq="часто")
btn("Resample", 81, 90, 44, 22, "Capture", color="teal", freq="иногда")
edit = [["Undo", "Redo", "Delete"], ["Duplicate", "Double", "New"], ["Quantize", "Length", "Automate"]]
for r, row in enumerate(edit):
    for c, n in enumerate(row):
        btn(n, 24 + 34 * c, 128 + 22 * r, 30, 16, "Edit", freq="часто" if n in ("Undo", "Delete", "Duplicate") else "иногда")
knob("Tempo", 33, 214, 18, "Tempo", freq="иногда")
knob("Swing", 83, 214, 18, "Tempo", freq="редко")
knob("Main", 33, 268, 16, "Levels", kind="pot", color="alu", freq="редко, аварийно")
knob("Phones 1", 83, 268, 16, "Levels", kind="pot", color="alu", freq="иногда")
knob("Cue Mix", 33, 312, 16, "Levels", kind="pot", color="alu", freq="редко")
knob("Phones 2", 83, 312, 16, "Levels", kind="pot", color="alu", freq="иногда")

# ---------------- LEFT WEDGE: rare levels ----------------
knob("Gain 1", 35, 382, 16, "Levels", note="утоплен", freq="редко")
knob("Gain 2", 85, 382, 16, "Levels", note="утоплен", freq="редко")
btn("P48 1", 35, 425, 18, 10, "Levels", label="P48", color="amber", note="утоплена, удержание 1 с", freq="редко")
btn("P48 2", 85, 425, 18, 10, "Levels", label="P48", color="amber", note="утоплена, удержание 1 с", freq="редко")
other("led", "Clip 1", 53, 371, 4, 4, "Levels", color="red")
other("led", "Clip 2", 103, 371, 4, 4, "Levels", color="red")
other("meter", "Meter L", 117, 405, 5, 104, "Levels", label="L")
other("meter", "Meter R", 125, 405, 5, 104, "Levels", label="R")

# ---------------- CENTER ----------------
other("zone", "Palm rest", 212, 21, 200, 34, "Palm", label="palm rest")
for j in range(8):
    for i in range(8):
        other("pad", f"Pad {i+1}.{8-j}", 124.5 + 25 * i, 56.5 + 25 * j, 21, 21, "Grid", color=TRACK[7 - j])
for i in range(8):
    btn(f"Scene {i+1}", 124.5 + 25 * i, 258, 19, 10, "Scenes", label=str(i + 1), freq="часто, в долю")
btn("Stop All", 341, 258, 36, 10, "Scenes", freq="иногда")
btn("Solo", 330, 28, 18, 14, "Tracks", color="blue", note="держать + Select", freq="иногда")
btn("Arm", 352, 28, 18, 14, "Tracks", color="red", note="держать + Select", freq="иногда")
for j in range(8):
    y = 56.5 + 25 * j
    n = 8 - j  # track 1 is the far row, like the list on the screen
    btn(f"Mute {n}", 330, y, 16, 16, "Tracks", label="M", color="amber", freq="постоянно, в долю")
    btn(f"Select {n}", 352, y, 16, 16, "Tracks", label=str(n), color=TRACK[n - 1], freq="постоянно")
    knob(f"Level {n}", 378, y, 14, "Tracks", label="", ring=21, color=TRACK[n - 1], note="низкая, с касанием", freq="часто")
params = ['Cutoff', 'Reso', 'Drive', 'Slot 1', 'Slot 2', 'Send A', 'Send B', 'Level']
for k in range(8):
    knob(f"Param {k+1}", 150 + 30 * k, 306, 18, "Screen knobs", label="", ring=26, color="purple",
         note="низкая, с касанием", freq="постоянно")

# ---------------- RIGHT ZONE: values (right hand), x 395..505 ----------------
btn("Scene A", 402, 24, 14, 12, "Live", label="A", color="red")
other("fader", "Crossfader", 450, 24, 72, 4, "Live", label="Scene A ↔ B")
btn("Scene B", 498, 24, 14, 12, "Live", label="B", color="blue")
for n, dx, dy in [("▲", 0, 19), ("▼", 0, -19), ("◄", -19, 0), ("►", 19, 0)]:
    btn("Arrow " + n, 422 + dx, 75 + dy, 15, 15, "Arrows", label=n, freq="часто")
gm = [["Repeat", "Accent"], ["Touch FX", "Scale"], ["Notes", "Chords"], ["Clips", "Steps"]]  # front -> back
for r, row in enumerate(gm):
    for c, n in enumerate(row):
        btn(n, 409 + 28 * c, 122 + 20 * r, 25, 14, "Grid modes" if n in ("Clips", "Steps", "Notes", "Chords", "Touch FX") else "Play",
            color="teal" if n in ("Clips", "Steps", "Notes", "Chords", "Touch FX") else "grey", freq="часто")
knob("Filter", 480, 70, 26, "Live", ring=34, color="coral", freq="часто")
knob("FX Mix", 480, 125, 26, "Live", ring=34, color="coral", freq="часто")
sm = [["Inputs", "Browser"], ["Sampler", "Song"], ["Mod", "Mixer"], ["Sound", "Effects"]]  # front -> back
for r, row in enumerate(sm):
    for c, n in enumerate(row):
        btn(n, 409 + 28 * c, 236 + 24 * r, 25, 15, "Screen modes", color="purple", freq="часто")
other("wheel", "Wheel", 480, 210, 45, 45, "Navigation", label="")
btn("Back", 480, 262, 30, 14, "Navigation", freq="часто")
btn("Page ◄", 468, 305, 20, 14, "Navigation", label="◄ Page", freq="часто")
btn("Page ►", 492, 305, 20, 14, "Navigation", label="Page ►", freq="часто")

# ---------------- RIGHT WEDGE: system (rare) ----------------
for i, n in enumerate(["Save", "Project", "Settings", "Help"]):
    btn(n, 397 + 30 * i, 368, 26, 12, "System", freq="иногда" if n in ("Save", "Help") else "редко")
other("pocket", "USB-A + SD", 432, 405, 74, 18, "System", label="USB · SD")
other("led", "Busy", 478, 405, 4, 4, "System", color="red")
btn("Panic", 410, 445, 30, 12, "System", color="red", note="утоплена", freq="редко, аварийно")
other("power", "Power", 485, 445, 14, 14, "System", note="утоплена, удержание 2 с")

# ---------------- SCREEN ----------------
other("screen", "Screen 10.1in", 255, 405, 240, 126, "Screen")

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
    if e["kind"] in ("button", "encoder", "pot", "wheel") and WEDGE0 - 3 < e["y"] < WEDGE0 + 12:
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
    json.dump(E, open("layout_v5.json", "w"), ensure_ascii=False, indent=1)
