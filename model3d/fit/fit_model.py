#!/usr/bin/env python3
"""Fit check of the Shtuka Druka enclosure: every board, module and big part as a box,
then a pairwise check for collisions and tight clearances.

Coordinates, mm: x from the left side (0..515), y from the front edge (0..460), z from the floor.
Parts on the slope are given in slope coordinates: s along the slope from the fold (y 300, z 68),
n along the outward normal from the outer surface (negative = inside).
Sources of the numbers: docs 27 (section 6), 28, 29, 30 and hardware/m1-screen-knobs/gen/design.py.
Everything marked est=True is an estimate to replace with a datasheet or a measurement.
No Blender needed: python3 fit_model.py prints the report. build_blend.py makes the .blend.
License: AGPL-3.0-or-later (code), CERN-OHL-S-2.0 (data).
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(REPO, "hardware", "m1-screen-knobs", "gen"))
import design as M1  # noqa: E402
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("w1_design", os.path.join(REPO, "hardware", "w1-levels", "gen", "design.py"))
W1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(W1)

FL = float(os.environ.get("FRONT_LIP", "0"))        # study: the case is longer in front by FL (a lip for the headphone jacks); y < 0 there
RS = float(os.environ.get("REAR_SHIFT", "0"))   # study 16.11.2026: the shelf before the rear wall is longer by RS, R1 / R2 / rear jacks / A1 / PW move back with the wall
FS = float(os.environ.get("FOLD_SHIFT", "0"))   # study 16.11.2026: the riser and everything behind it move back by FS (finger room behind the knob row)
RS += FS                                        # rear boards follow the fold; the shelf itself is longer by REAR_SHIFT only
W, D = 515.0, 460.0 + RS
_T = float(os.environ.get("FRONT_Z", "68.0"))      # height of the front top surface; the slope keeps its 30 degrees
FOLD_Y, FOLD_Z, SHELF_Y, TOP_Z, BACK_Z = 300.0 + FS, _T, 430.0 + FS, float(os.environ.get("DECK", str(_T))), float(os.environ.get("BACK_H", str(_T + 75.0)))   # BACK_H: rear height, default front + 75 (30 degrees)
SLOPE = math.atan2(BACK_Z - FOLD_Z, SHELF_Y - FOLD_Y)          # 30 degrees
SLOPE_LEN = math.hypot(BACK_Z - FOLD_Z, SHELF_Y - FOLD_Y)       # 150.1 mm
SKIN = 3.0
PCB_TOP = TOP_Z - SKIN - float(os.environ.get("PANEL_GAP", "6.5"))   # panel boards: encoder body (6.5) between board and skin
PCB = 1.6
GAP_MIN = 1.0                        # below this a clearance is reported as tight
COMPUTER = os.environ.get("COMPUTER", "H5")      # "H5" (ODROID-H5, R149) or "ITX" (Mini-ITX, the fallback of R36)
# z = 0 is the OUTSIDE of the floor; the floor skin fills z 0..SKIN. H5_Z0 = underside of the H5 board in these coordinates.
# Until 15.11.2026 the default was 3.0, i.e. the board lying on the inner floor, not on 3 mm standoffs (Codex review 15.11.2026).
# Now: H5_STANDOFF above the inner floor (default 3 mm), or an absolute H5_Z0.
H5_STANDOFF = float(os.environ.get("H5_STANDOFF", "3.0"))
H5_Z0 = float(os.environ.get("H5_Z0", str(SKIN + H5_STANDOFF)))
H5_H = float(os.environ.get("H5_H", "44.0"))     # overall height of the H5 above the board underside, mm
# --- parameters of the "lower case" study (git history (deleted 18.11.2026)); every default keeps the old behaviour ---
PANEL_GAP = float(os.environ.get("PANEL_GAP", "6.5"))   # board top -> skin underside for P1, P3, P4, M1, W (encoder bodies, wheel, crossfader)
P2_GAP = float(os.environ.get("P2_GAP", str(PANEL_GAP)))  # same for P2 Grid only (pads = FSR sheet, SMD buttons: needs less)
P2_PARTS = float(os.environ.get("P2_PARTS", "4.0"))     # envelope of the parts under P2, mm (the design has 7.7 mm electrolytics and headers there)
WHEEL_TRACK = os.environ.get("WHEEL_TRACK", "0") == "1"  # 1: the wheel housing follows the skin (the stack under the skin is 6.5 mm anyway)
F1_MODE = os.environ.get("F1_MODE", "V")                 # V = vertical 44 mm board (as before), H = horizontal under the jacks (P94)
F1_TOP = float(os.environ.get("F1_TOP", "50.0"))         # top of the vertical F1, z
REAR_JACK_TOP = float(os.environ.get("REAR_JACK_TOP", "112.0"))      # top of the rear-jack envelope, z
REAR_JACK_TOP_R = float(os.environ.get("REAR_JACK_TOP_R", str(REAR_JACK_TOP)))  # same for x > 340 (under W2 / W3)
R2_TALL_X1 = float(os.environ.get("R2_TALL_X1", "359.0"))            # right end of the tall part of R2 (model x)
A1_X0 = float(os.environ.get("A1_X0", "20"))               # A1 left edge (study: A1 moved under the grid)
A1_Y0 = float(os.environ.get("A1_Y0", str(305 + RS)))              # A1 front edge
W3_S1 = float(os.environ.get("W3_S1", "60.2"))      # end of W3 along the slope, s from the fold; the real board (hardware/w3-system) ends at s 60.2, before the pocket; 138 = the old slab over the whole slope
W3_X1 = float(os.environ.get("W3_X1", "505.0"))      # right end of W3 (model x); 505 = 92 mm wide board; shortened to make room for a bigger fan on the right wall (R182)
PW_TOP = float(os.environ.get("PW_TOP", "24.0"))            # top of PW envelope: 10.5 mm electrolytics below + board + connectors above (checked 17.11.2026)
PW_X0 = float(os.environ.get("PW_X0", "0"))              # H5REAR: left edge of PW (0 = old default 285)
H5T_X = float(os.environ.get("H5T_X", "120.0"))             # H5TILT: left edge x of the H5 lying along the slope
H5T_S0 = float(os.environ.get("H5T_S0", "20.0"))           # H5TILT: its lower edge along the slope from the fold
H5T_N = float(os.environ.get("H5T_N", "-26.0"))            # H5TILT: top of the heatsink, n from the outer surface (screen back is at about -25)
H5_PORT = os.environ.get("H5_PORT", "none")             # H5REAR: edge with the ports and plugs, N (+y) S (-y) E (+x) W (-x); a 25 mm clearance box is added
H5_PORT_LEN = float(os.environ.get("H5_PORT_LEN", "25.0"))   # plug and cable bend beyond the board edge (estimate)
BATT_LIPO = os.environ.get("BATT_LIPO", "0") == "1"       # R155: flat LiPo pack under P2, 170 x 100 x 12 (4S, about 99 Wh with the BMS)
LIPO_H = float(os.environ.get("LIPO_H", "12.0"))
BATT_BOXES = [tuple(float(v) for v in s.split(",")) for s in os.environ.get("BATT_BOXES", "").split(";") if s.strip()]
A1_Z0 = float(os.environ.get("A1_Z0", "6"))          # A1 envelope bottom (6 = on standoffs; higher = on a shelf above the battery)
JACK_H = float(os.environ.get("JACK_H", "15.67"))   # headphone jack body height above its board (NMJ6HCD2 15.67; Cliff S1 CL1115 12.70)
JACK_W = float(os.environ.get("JACK_W", "18.2"))    # its width (NMJ6HCD2 18.2; Cliff S1 15.90)
F1_STAND = float(os.environ.get("F1_STAND", "3.0"))  # F1 board above the inner floor in the lip (0 = on an insulating sheet on the floor)
M1_J1_H = float(os.environ.get("M1_J1_H", "7.5"))   # M1 bus header + IDC plug below the board (vertical 7.5; right-angle header about 5, estimate)
FAN = tuple(float(v) for v in os.environ["FAN"].split(",")) if os.environ.get("FAN") else None   # "y,z0": 92 mm fan on the right wall
PANEL_PARTS = float(os.environ.get("PANEL_PARTS", "4.0"))  # parts-below envelope of P1, P3, P4
F1_SIDE_Z = float(os.environ.get("F1_SIDE_Z", "40.0"))    # F1_MODE=SIDE: axis height of the jacks on the left wall behind the riser
BATT_FLAT = os.environ.get("BATT_FLAT", "0") == "1"      # battery as one flat row of 8 cells (155 x 75 x 25) instead of 90 x 86 x 45
R1_TOP = float(os.environ.get("R1_TOP", "113.0"))          # top of the vertical R1 board, z
R2_TOP = float(os.environ.get("R2_TOP", "109.0"))          # top of the tall part of R2, z
H5_REAR_X = float(os.environ.get("H5_REAR_X", "451.0"))  # H5REAR centre x
H5_REAR_Y = float(os.environ.get("H5_REAR_Y", "353.0"))  # H5REAR centre y


class Box:
    """Oriented box: centre, half sizes along its own axes, rotation about x (slope parts)."""

    def __init__(self, name, group, c, size, rx=0.0, color="grey", shape="box", est=False, check=True, note=""):
        self.name, self.group, self.c, self.h = name, group, tuple(c), tuple(s / 2 for s in size)
        self.rx, self.color, self.shape, self.est, self.check, self.note = rx, color, shape, est, check, note
        a = math.radians(rx)
        self.ax = ((1, 0, 0), (0, math.cos(a), math.sin(a)), (0, -math.sin(a), math.cos(a)))

    def dict(self):
        return dict(name=self.name, group=self.group, c=self.c, size=[2 * v for v in self.h], rx=self.rx,
                    color=self.color, shape=self.shape, est=self.est, note=self.note)


def box(name, group, x0, x1, y0, y1, z0, z1, **kw):
    return Box(name, group, ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), (x1 - x0, y1 - y0, z1 - z0), **kw)


def slope_box(name, group, x0, x1, s0, s1, n0, n1, **kw):
    """Box lying on the slope: s along the slope from the fold, n along the outward normal."""
    sc, nc = (s0 + s1) / 2, (n0 + n1) / 2
    cy = FOLD_Y + sc * math.cos(SLOPE) - nc * math.sin(SLOPE)
    cz = FOLD_Z + sc * math.sin(SLOPE) + nc * math.cos(SLOPE)
    return Box(name, group, ((x0 + x1) / 2, cy, cz), (x1 - x0, s1 - s0, n1 - n0), rx=math.degrees(SLOPE), **kw)


def s_of(y):
    """Slope coordinate of a projected y (top view) on the outer surface."""
    return (y - 300.0) / math.cos(SLOPE)        # y in panel coordinates (fold at 300), whatever FOLD_SHIFT is


def slope_frame(name, group, x0, x1, s0, s1, n0, n1, hole, **kw):
    """A slope box with a rectangular hole (hx0, hx1, hs0, hs1) cut through it: up to four boxes."""
    hx0, hx1, hs0, hs1 = hole
    out = []
    for nm, a, b, c, d in (("below", x0, x1, s0, hs0), ("above", x0, x1, hs1, s1),
                           ("left", x0, hx0, hs0, hs1), ("right", hx1, x1, hs0, hs1)):
        if b - a > 0.01 and d - c > 0.01:
            out.append(slope_box(f"{name} ({nm} the cut-out)", group, a, b, c, d, n0, n1, **kw))
    return out


# ------------------------------------------------------------------ real parts (doc 32)
SCREEN_SHIFT = -1.0       # screen 1 mm down the slope: 1.04 mm to the shelf instead of 0.37 (P92)
POCKET = (413.0, 505.0, s_of(365) - 12 / math.cos(SLOPE), s_of(365) + 12 / math.cos(SLOPE))   # 92 x 24 (top view)
USB_X = 428.0             # USB-A at the left end of the pocket: 36 mm free for a full-size SD card (32 mm)
USB_VARIANTS = {
    # name: (where, height above its board, note)
    "A": ("W3", 13.7, "standard vertical USB-A, 13.7 mm (LCSC C456015, SHOU HAN AF 180° ZJB13.7)"),
    "B": ("W3", 10.0, "low-profile vertical USB-A, 10 mm (Kycon KUSBVLPX-AS1N; LCSC C2681562, SHOU HAN 10.0 180°)"),
    "C": ("sub", 13.7, "standard vertical USB-A 13.7 mm on a small pocket board under a cut-out in W3"),
    "D": ("W3h", 7.0, "horizontal through-hole USB-A, about 7 mm high (typical, estimate); the stick lies in the pocket"),
}
USB_VARIANT = "C"          # proposal P93
USB_RECESS = 1.5           # variant C: top of the receptacle this far below the outer surface
WZ0, WZ1 = -SKIN - 6.5 - PCB, -SKIN - 6.5     # slope boards: bottom and top face (n)
SD_X0 = 474.0             # mouth of the SD socket (card goes in towards +x)


def usb_receptacle(v):
    """The USB-A receptacle of variant v (and its pocket board for C): list of boxes, top n of the receptacle."""
    where, hgt, note = USB_VARIANTS[v]
    sp = (POCKET[2] + POCKET[3]) / 2
    out = []
    if where == "W3":                       # vertical on W3: 14.5 x 7.0 footprint (USB-A shell 12 x 4.5 + tabs)
        n0 = WZ1
        out.append(slope_box(f"USB-A receptacle ({v})", "slope", USB_X - 7.25, USB_X + 7.25, sp - 3.5, sp + 3.5,
                             n0, n0 + hgt, color="metal", note=note))
    elif where == "W3h":                    # lying on W3, opening towards +x, the stick lies in the pocket
        n0 = WZ1
        out.append(slope_box(f"USB-A receptacle ({v})", "slope", 415, 429, sp - 6.6, sp + 6.6, n0, n0 + hgt,
                             color="metal", est=True, note=note))
    else:                                   # sub-board: receptacle top USB_RECESS under the outer surface
        n0 = -USB_RECESS - hgt
        out.append(slope_box(f"USB-A receptacle ({v})", "slope", USB_X - 7.25, USB_X + 7.25, sp - 3.5, sp + 3.5,
                             n0, n0 + hgt, color="metal", note=note))
        out.append(slope_box("Pocket board", "slope", USB_X - 15, USB_X + 15, sp - 10, sp + 10, n0 - PCB, n0,
                             color="pcb", note="small board for the USB-A, cable to the Mini-ITX USB header"))
        out.append(slope_box("Pocket board pins", "slope", USB_X - 13, USB_X + 13, sp - 8, sp + 8, n0 - PCB - 3,
                             n0 - PCB, color="parts", est=True, note="THT pins and the cable plug"))
    return out, n0 + hgt


def w1_parts():
    """W1 Levels from its own design data (hardware/w1-levels/gen/design.py, doc 31): board with the
    window for M5, the pots, the bottom parts and both bus plugs, and the M5 module in the window."""
    out = []
    bs = lambda by: W1.S1 - by                                  # board y -> slope s
    bx = lambda x: W1.X0 + x
    n1 = -SKIN - W1.BELOW_SKIN
    n0 = n1 - PCB
    wx0, wy0, wx1, wy1 = W1.window()
    out += slope_frame("W1 Levels", "slope", W1.X0, W1.X1, W1.S0, W1.S1, n0, n1,
                       (bx(wx0), bx(wx1), bs(wy1), bs(wy0)), color="pcb", note="doc 31, 2 layers")
    pl = W1.placement()
    for n, (nm, px, py) in enumerate(W1.POTS):
        s = W1.s_of(py)
        out.append(slope_box(f"W1 {nm} pot", "slope", px - 4.9, px + 4.9, s - 5.5, s + 5.5, n1, n1 + 7.4,
                             color="metal", est=True, note="Alps RK09K: 9.8 wide (Alps); 7.4 high from the drawing, to confirm"))
        out.append(slope_box(f"W1 {nm} pot pins", "slope", px - 9, px - 6, s - 3, s + 3, n0 - 2.5, n0, color="metal",
                             est=True, note="THT pins under the board"))
    for ref, size, h in (("U1", (3, 3), 1.1), ("U2", (5, 6.4), 1.2), ("U3", (4, 4), 0.9)):
        x, y = pl[ref][:2]
        out.append(slope_box(f"W1 {ref}", "slope", bx(x) - size[0] / 2, bx(x) + size[0] / 2, bs(y) - size[1] / 2,
                             bs(y) + size[1] / 2, n0 - h, n0, color="chip"))
    for ref in ("J1", "J2"):
        x, y = pl[ref][:2]
        out.append(slope_box(f"W1 {ref} + IDC plug", "slope", bx(x) - 5.75, bx(x) + 5.75, bs(y) - 2.25, bs(y) + 2.25,
                             n0 - 7.5, n0, color="plastic", est=True, note="2x7 1.27 mm header and the ribbon plug"))
    # M5 Gain module in the window, in the plane of the encoder modules (6.5 mm under the skin), estimate
    gs = W1.s_of(W1.GAIN[0][2])
    out.append(slope_box("M5 module board", "slope", bx(W1.M5_X[0]), bx(W1.M5_X[1]), gs - 17, gs + 17, WZ0, WZ1,
                         color="pcb", est=True, note="Gain 1 + 2, not designed yet; outline assumed in doc 31"))
    for nm, px, _ in W1.GAIN:
        out.append(slope_box(f"M5 {nm} encoder", "slope", px - 6.2, px + 6.2, gs - 6.7, gs + 6.7, WZ1, -SKIN,
                             color="metal", note="Alps EC11E body"))
    out.append(slope_box("M5 parts below", "slope", bx(W1.M5_X[0]) + 2, bx(W1.M5_X[1]) - 2, gs - 15, gs + 15, WZ0 - 4,
                         WZ0, color="parts", est=True))
    return out


def slope_boards_and_pocket(usb):
    """W1-W3 with their component envelopes; W3 gets the pocket parts of the chosen USB-A variant."""
    out = []
    sp = (POCKET[2] + POCKET[3]) / 2
    out += w1_parts()
    for nm, x0, x1 in (("W2 Meters", 355, 390), ("W3 System", 413, W3_X1)):
        if nm.startswith("W3") and USB_VARIANTS[usb][0] == "sub":
            cut = (USB_X - 8.5, USB_X + 8.5, sp - 4.5, sp + 4.5)            # receptacle passes through W3
            keep = (USB_X - 16, USB_X + 16, sp - 11, sp + 11)               # no W3 parts over the pocket board
            s1 = W3_S1 if nm.startswith("W3") else 138
            out += slope_frame(nm, "slope", x0, x1, 12, s1, WZ0, WZ1, cut, color="pcb")
            out += slope_frame(nm + " parts below", "slope", x0 + 2, x1 - 2, 14, s1 - 2, WZ0 - 4, WZ0, keep,
                               color="parts", est=True)
        else:
            out.append(slope_box(nm, "slope", x0, x1, 12, 138, WZ0, WZ1, color="pcb"))
            out.append(slope_box(nm + " parts below", "slope", x0 + 2, x1 - 2, 14, 136, WZ0 - 4, WZ0,
                                 color="parts", est=True))
    rec, _ = usb_receptacle(usb)
    out += rec
    # SD slot (R81, full-size SD): push-push socket lying on W3 at the right end of the pocket, mouth facing -x.
    # Socket class Hirose DM1AA / Kyocera 5638: about 29 x 29 x 3 mm (estimate until the part is chosen);
    # it reaches under the skin on both sides of the 27.7 mm pocket, the 24 mm card goes in along x.
    out.append(slope_box("SD socket (full size)", "slope", SD_X0, SD_X0 + 29, sp - 14.5, sp + 14.5, WZ1, WZ1 + 3.0,
                         color="metal", est=True, note="full-size SD push-push, 29 x 29 x 3 class"))
    out.append(slope_box("SD card (inserted)", "slope", SD_X0 - 2.5, SD_X0 + 29.5, sp - 12, sp + 12, WZ1 + 0.6,
                         WZ1 + 2.7, color="plastic", check=False, note="24 x 32 x 2.1 mm, 2.5 mm out for the push"))
    return out


SCREEN = os.environ.get("SCREEN", "EP")      # "EP" = Waveshare 10.1EP-CAPLCD (R150), "DP" = the earlier 10.1DP-CAPLCD
SCREEN_ROT = int(os.environ.get("SCREEN_ROT", "180"))   # 180 (default since 16.11.2026, user) = EP turned upside down in its plane, image and touch flipped in software; 0 = as drawn


def screen_parts_ep():
    """Waveshare 10.1EP-CAPLCD (R150) from its 2D drawing (files.waveshare.com/wiki/10.1EP-CAPLCD/10.1EP-CAPLCD.pdf,
    read 16.11.2026): glass 239 x 147, metal back 230.7 x 145.1 (1.37 / 0.95 mm in from the glass edges), 7.3 mm from the
    glass front to the back, 21.9 mm overall with the driver board; 8 x M2.5 in the back, 218.1 x 133 apart.
    Driver board 86.5 x 60, seen from behind 72.72-159.22 mm from the back's left edge, 43.5-103.5 mm above its lower edge.
    Its sockets are on the board edge that faces the device's left (seen from the front); above the lower glass edge:
    3.5 mm audio 50, HDMI 66, Type-C (touch) 84.5, Type-C (power) 98.5 (pitch 16 / 18.5 / 14 on the drawing).
    d = depth behind the glass front, n = -SKIN - d; device x grows to the right."""
    gx, gs = 220.75, s_of(365) + SCREEN_SHIFT
    xl = gx - 119.5                                         # left glass edge (front view)

    rot = SCREEN_ROT == 180

    def ep(name, x0, x1, s0, s1, d0, d1, **kw):            # x from the left glass edge, s from the lower glass edge (as drawn)
        if rot:                                              # screen turned 180 deg in its plane (image flipped in software)
            x0, x1, s0, s1 = 239.0 - x1, 239.0 - x0, 147.0 - s1, 147.0 - s0
        return slope_box(name, "screen", xl + x0, xl + x1, gs - 73.5 + s0, gs - 73.5 + s1, -SKIN - d1, -SKIN - d0, **kw)

    bx0, bx1 = 239.0 - 1.37 - 159.22, 239.0 - 1.37 - 72.72  # driver board seen from the front: 78.4-164.9
    out = [
        ep("Screen glass", 0, 239, 0, 147, 0, 2.0, color="glass", note="239 x 147 lens"),
        ep("Screen LCM + back", 4.15, 234.85, 0.95, 146.05, 2.0, 7.3, color="lcd", note="metal back 230.7 x 145.1, 7.3 mm behind the glass front"),
        ep("Screen driver board", bx0, bx1, 44.45, 104.45, 7.3, 11.5, color="pcb", note="86.5 x 60 board on posts"),
        ep("Screen driver parts", bx0, bx1, 44.45, 104.45, 11.5, 21.9, color="parts", est=True, note="sockets and parts, 21.9 mm overall"),
    ]
    # plugs leave the board edge at bx0 towards the device's left, parallel to the glass; then the cables turn inwards (down)
    if rot:     # turned 180 deg: the sockets face the right and sit low on the slope (power lowest), every cable turns in at once
        for nm, sc, w, ln in (("HDMI", 66.0, 22.0, 40.0), ("USB-C touch", 84.5, 13.0, 30.0), ("USB-C power", 98.5, 13.0, 30.0)):
            out.append(ep(f"Screen {nm} plug", bx0 - ln, bx0, sc - w / 2, sc + w / 2, 9.0, 21.0, color="plastic", est=True,
                          note=f"straight {nm} plug, {ln:.0f} mm, lying behind the screen"))
            out.append(ep(f"Screen {nm} cable bend", bx0 - ln - 25, bx0 - ln, sc - w / 2, sc + w / 2, 9.0, 21.0 + 30,
                          color="plastic", est=True, note="cable turning inwards, bend radius about 25 mm"))
        return out
    for nm, sc, w, ln in (("HDMI", 66.0, 22.0, 40.0), ("USB-C touch", 84.5, 13.0, 30.0)):
        out.append(ep(f"Screen {nm} plug", bx0 - ln, bx0, sc - w / 2, sc + w / 2, 9.0, 21.0, color="plastic", est=True,
                      note=f"straight {nm} plug, {ln:.0f} mm, lying behind the screen"))
        out.append(ep(f"Screen {nm} cable bend", bx0 - ln - 25, bx0 - ln, sc - w / 2, sc + w / 2, 9.0, 21.0 + 30, color="plastic",
                      est=True, note="cable turning inwards, bend radius about 25 mm"))
    # power (top socket, nearest the rear wall): turning inwards right after the plug, its bend hit R1 by 5 mm (16.11.2026).
    # So the power cable stays flat behind the screen: along x past the other bends, then down the slope, and turns inwards low.
    sc = 98.5
    out.append(ep("Screen USB-C power plug", bx0 - 30, bx0, sc - 6.5, sc + 6.5, 9.0, 21.0, color="plastic", est=True,
                  note="straight Type-C plug, 30 mm"))
    out.append(ep("Screen USB-C power cable run", bx0 - 75, bx0 - 30, sc - 3.0, sc + 3.0, 9.0, 16.0, color="plastic", est=True,
                  note="cable flat behind the screen, along x"))
    out.append(ep("Screen USB-C power cable down", bx0 - 75, bx0 - 69, 40.0, sc + 3.0, 9.0, 16.0, color="plastic", est=True,
                  note="cable flat behind the screen, down the slope"))
    out.append(ep("Screen USB-C power cable bend", bx0 - 75, bx0 - 65, 15.0, 40.0, 9.0, 21.0 + 30, color="plastic", est=True,
                  note="cable turning inwards near the fold, bend radius about 25 mm"))
    return out


def screen_parts():
    if SCREEN == "EP":
        return screen_parts_ep()
    return screen_parts_dp()


def screen_parts_dp():
    """Waveshare 10.1DP-CAPLCD from its 3D model (STP from the Waveshare wiki, not kept in the repo:
    licence unclear). Bounding boxes read with OpenCascade, in the STP frame: x across the glass (147),
    y along it (239), z out of the glass (front at z = 4.81). Mounted with the connector edge of the
    driver board (STP -x) facing down the slope, towards the fold (P95):
        s = gs + x,   device x = gx - y,   n = z - 4.81 - SKIN   (glass front against the skin)."""
    gx, gs = 220.75, s_of(365) + SCREEN_SHIFT

    def stp(name, x0, x1, y0, y1, z0, z1, **kw):
        return slope_box(name, "screen", gx - y1, gx - y0, gs + x0, gs + x1, z0 - 4.81 - SKIN, z1 - 4.81 - SKIN, **kw)

    out = [
        stp("Screen glass", -73.5, 73.5, -119.5, 119.5, 2.81, 4.81, color="glass",
            note="239 x 147 x 2 lens (wiki, STP)"),
        stp("Screen LCM", -71.5, 71.5, -117.08, 111.52, -2.61, 2.81, color="lcd",
            note="228.6 x 143 panel behind the lens, offset 2.4 mm towards STP +y: back 7.4 mm behind the glass front"),
        stp("Screen driver board", -33.04, 38.98, -54.88, 53.14, -8.88, -0.47, color="pcb",
            note="108 x 72 board on 4 mm posts, parts up to 8.9 mm below the glass front (STP, 2D drawing)"),
        stp("Screen LCD flex", -6.3, 32.39, -103.72, -50.42, -3.55, -0.64, color="lcd",
            note="flat cable from the board to the LCD"),
    ]
    # cables: both leave the board edge at STP x = -27 towards the fold. A straight HDMI plug does not fit:
    # the socket axis is 2.1 mm from the LCD back (z -4.7 vs -2.61), a normal moulded plug is 8-11 mm thick.
    # So: 90-degree adapters turning away from the screen, then the cables bend down to the Mini-ITX.
    for nm, y0, y1, w in (("HDMI", -21.4, -5.6, 22.0), ("USB-C", 4.6, 12.0, 14.0)):
        yc = (y0 + y1) / 2
        out.append(stp(f"Screen {nm} 90° plug", -27 - 20, -27, yc - w / 2, yc + w / 2, -8.88 - 22, -2.61 - 0.5,
                       color="plastic", est=True,
                       note=f"{nm} right-angle plug/adapter, cable leaves away from the screen"))
        out.append(stp(f"Screen {nm} cable bend", -27 - 20 - 25, -27, yc - w / 2, yc + w / 2, -8.88 - 22 - 30,
                       -8.88 - 22, color="plastic", est=True, check=True,
                       note="room for the cable to turn down to the Mini-ITX, bend radius about 25 mm"))
    return out


# ------------------------------------------------------------------ the model
def parts(usb=None):
    usb = usb or USB_VARIANT
    P = []
    a = P.append
    # shell
    sh = dict(color="shell", check=True)
    a(box("Floor", "shell", 0, W, -FL, D, 0, SKIN, **sh))
    a(box("Front wall", "shell", 0, W, -FL, -FL + SKIN, SKIN, TOP_Z, **sh))
    a(box("Rear wall", "shell", 0, W, D - SKIN, D, SKIN, BACK_Z, **sh))
    a(box("Side left", "shell", 0, SKIN, -FL + SKIN, D - SKIN, SKIN, TOP_Z, **sh))
    a(box("Side right", "shell", W - SKIN, W, -FL + SKIN, D - SKIN, SKIN, TOP_Z, **sh))
    a(box("Top skin", "shell", SKIN, W - SKIN, -FL + SKIN, FOLD_Y, TOP_Z - SKIN, TOP_Z, **sh))
    if TOP_Z < FOLD_Z - 0.01:          # step case (DECK < FRONT_Z): the riser wall at the fold
        a(box("Riser wall", "shell", SKIN, W - SKIN, FOLD_Y - SKIN, FOLD_Y, TOP_Z, FOLD_Z, **sh))
    # slope skin with the USB-A + SD pocket open down to W3 (R81); the pocket walls are left out
    P += slope_frame("Slope skin", "shell", SKIN, W - SKIN, 0, SLOPE_LEN, -SKIN, 0, POCKET, **sh)
    a(box("Shelf", "shell", SKIN, W - SKIN, SHELF_Y, D - SKIN, BACK_Z - SKIN, BACK_Z, **sh))

    # panel boards under the flat part (doc 29); component envelope 4 mm under each
    z0, z1 = PCB_TOP - PCB, PCB_TOP
    for nm, x0, x1, y0, y1 in (("P1 Left", 10, 102, 4, 291), ("P2 Grid", 110, 334, 4, 262),   # 16.11.2026: P2 rev 0.4 outline 224 x 258 (was 221.5 x 257)
                              
                               ("P3 Tracks", 339, 405, 4, 291), ("P4 Right", 413, 505, 4, 291)):
        dz = (PANEL_GAP - P2_GAP) if nm.startswith("P2") else 0.0      # P2 closer to the skin by dz (study variants only)
        ph = P2_PARTS if nm.startswith("P2") else PANEL_PARTS
        a(box(nm, "panel", x0, x1, y0, y1, z0 + dz, z1 + dz, color="pcb"))
        a(box(nm + " parts below", "panel", x0 + 2, x1 - 2, y0 + 2, y1 - 2, z0 + dz - ph, z0 + dz, color="parts", est=True,
              note="envelope of the components under the board"))
    a(box("Trill Bar x2", "panel", 130, 311.5, 13, 31, PCB_TOP, TOP_Z - SKIN, color="pcb",
          note="touch strip sensors right under the skin (R113)"))
    # crossfader: Bourns PTA4543 (45 mm travel), body 60 x 9 x 6.5 mm; two M2 threads on top screw it to
    # the skin, so the body touches the skin by design (Bourns PTA drawing: A = 60, 9.0, 6.5, M2 x 2 places)
    a(box("Crossfader body", "panel", 429, 489, 17.5, 26.5, PCB_TOP, PCB_TOP + 6.5, color="metal",
          note="Bourns PTA4543-2015CPB103 (LCSC C17328789 is the DP lever version); panel-mounted with 2 x M2"))
    # wheel (R74): AS5600 under P4 (bottom side), 6 x 2.5 mm diametric magnet 0.5 mm above the board,
    # 6700ZZ bearing (10 x 15 x 4) in a printed housing screwed under the skin. AS5600 datasheet:
    # magnet 6 mm, air gap 0.5-3 mm, SOIC-8 max 1.75 mm; here magnet -> die about 0.5 + 1.6 + 0.4 = 2.5 mm
    wx, wy = 459.0, float(os.environ.get("WHEEL_Y", "277.0"))   # WHEEL_Y: study, the wheel between Page / Back and the riser
    wz = (TOP_Z - 4.75) if WHEEL_TRACK else 63.25
    a(Box("Wheel bearing housing", "panel", (wx, wy, wz), (21, 21, 3.5), color="plastic", shape="cyl",
          note="printed, holds the 6700ZZ bearing, screwed to the skin"))
    a(Box("Wheel bearing 6700ZZ", "panel", (wx, wy, wz + 0.25), (15, 15, 4), color="metal", shape="cyl", check=False,
          note="10 x 15 x 4 mm; sits 0.5 mm into a counterbore of the skin"))
    a(Box("Wheel magnet", "panel", (wx, wy, PCB_TOP + 0.5 + 1.25), (6, 6, 2.5), color="metal", shape="cyl",
          note="6 x 2.5 mm diametric, on the shaft end; 0.5 mm above P4 by design"))
    a(Box("Wheel AS5600", "panel", (wx, wy, PCB_TOP - PCB - 0.875), (4.9, 6.0, 1.75), color="chip",
          note="SOIC-8 on the bottom of P4, under the magnet"))
    a(Box("Wheel", "top", (wx, wy, TOP_Z + 4.5), (38, 38, 8), color="knob", shape="cyl", check=False))
    # click mechanism (P110, docs/ru/44_wheel_detents.md): a collar on the skin round the shaft carries two opposite leaf pawls
    # (4 mm wide, 0.2 mm bronze); 24 internal teeth are moulded in the wheel skirt (cavity z TOP_Z+0.5 .. TOP_Z+6.5, tooth tips r 15.5)
    a(Box("Wheel detent collar", "top", (wx, wy, TOP_Z + 2.75), (24, 24, 5.5), color="plastic", shape="cyl",
          note="printed, on the skin, screwed through it to the bearing housing; the shaft passes through a 11 mm bore"))
    for sgn in (1, -1):
        a(Box(f"Wheel detent pawl {sgn:+d}", "top", (wx + sgn * 13.8, wy, TOP_Z + 3.25), (3.6, 9.0, 4.0), color="metal",
              note="envelope of the leaf pawl: root on the collar r 12, tip at the teeth r 15.5"))

    # everything on top of the panel, from panel v7 (visual only)
    J = json.load(open(os.path.join(REPO, "mockup", "layout", "layout_v7.json")))
    heights = {"pad": 3.0, "button": 2.5, "encoder": 11.0, "pot": 14.0, "strip": 0.4, "fader": 9.0, "meter": 0.4,
               "led": 0.4, "pocket": 0.4, "power": 2.5}
    colors = {"pad": "plastic", "button": "plastic", "encoder": "knob", "pot": "metal", "fader": "knob"}
    for e in J["elements"]:
        k = e["kind"]
        if k in ("screen", "wheel") or e["name"].startswith("Param "):
            continue
        hgt = heights.get(k, 1.0)
        w, d = (e["w"], e["h"]) if k != "pad" else (25.5, 21.0)
        shape = "cyl" if k in ("encoder", "pot") else "box"
        nm = e["name"] if k != "pad" else f"Pad {e['x']:g},{e['y']:g}"
        if e["y"] < 300.0:
            a(Box(nm, "top", (e["x"], e["y"], TOP_Z + hgt / 2 + 0.2), (w, d, hgt), color=colors.get(k, "grey"),
                  shape=shape, check=False))
        else:
            sc = s_of(e["y"])
            a(slope_box(nm, "top", e["x"] - w / 2, e["x"] + w / 2, sc - d / 2, sc + d / 2, 0.2, 0.2 + hgt,
                        color=colors.get(k, "grey"), shape=shape, check=False))

    # M1 - screen knobs module, from its own design data
    bx = lambda x: M1.X0 + x
    by = lambda y: M1.Y1 - y
    a(box("M1 board", "m1", M1.X0, M1.X1, M1.Y0, M1.Y1, z0, z1, color="pcb"))
    for k in range(8):
        cx, cy = 122.75 + 28 * k, M1.KNOB_Y
        a(Box(f"M1 encoder {k + 1}", "m1", (cx, cy, z1 + 3.25), (12.4, 13.4, 6.5), color="metal",
              note="Alps EC11E body; bushing M7 goes through the skin"))
        a(Box(f"M1 encoder {k + 1} pins", "m1", (cx, cy, z0 - 1.5), (16.5, 13.4, 3.0), color="metal", est=True,
              note="THT pins and tabs under the board"))
        a(Box(f"Param {k + 1} knob", "top", (cx, cy, TOP_Z + 1 + 5.5), (18, 18, 11), color="knob", shape="cyl",
              check=False))
        a(Box(f"M1 bushing {k + 1}", "m1", (cx, cy, z1 + 6.5 + 4.5), (7, 7, 9), color="metal", shape="cyl",
              check=False, note="passes through the skin hole"))
        for i in range(M1.RING_N):
            lx, ly, _ = M1.led_xy(k, i)
            a(Box(f"M1 LED {k + 1}.{i + 1}", "m1led", (bx(lx), by(ly), z1 + 0.3), (1.6, 1.5, 0.6), color="led",
                  check=False))
    pl = M1.placement()
    for ref, size in (("U1", (7, 7, 0.9)), ("U2", (3, 3, 0.6)), ("U3", (5, 4.4, 1.2)), ("U4", (5, 4.4, 1.2)),
                      ("U5", (5, 4.4, 1.2))):
        x, y = pl[ref][:2]
        a(Box(f"M1 {ref}", "m1", (bx(x), by(y), z0 - size[2] / 2), size, color="chip"))
    x, y = pl["J1"][:2]
    a(Box("M1 J1 + IDC plug", "m1", (bx(x), by(y), z0 - M1_J1_H / 2), (11.5, 4.5, M1_J1_H), color="plastic", est=True,
          note="2x7 1.27 mm header and the ribbon plug, from below"))

    # computer, front jacks
    if COMPUTER == "H5":
        # ODROID-H5 (R149): 120 x 120 mm board, 44 mm overall height (Hardkernel via cnx-software, 20.05.2026; whether the 44 mm
        # counts the board's feet is not stated: here it is taken from the underside of the board). Centred on the old Mini-ITX area.
        cx = float(os.environ.get("H5_X", (136 + 306) / 2))
        cy = float(os.environ.get("H5_Y", (45 + 215) / 2))
        hx0, hx1, hy0, hy1 = cx - 60, cx + 60, cy - 60, cy + 60
        a(box("Mini-ITX board", "itx", hx0, hx1, hy0, hy1, H5_Z0, H5_Z0 + 1.6, color="pcb"))
        a(box("Mini-ITX parts H5", "itx", hx0, hx1, hy0, hy1, H5_Z0 + 1.6, H5_Z0 + H5_H, color="parts", est=True,
              note="ODROID-H5 with its heatsink, 44 mm overall"))
    elif COMPUTER == "ITX":
        a(box("Mini-ITX board", "itx", 136, 306, 45, 215, 9, 10.6, color="pcb"))
        a(box("Mini-ITX parts", "itx", 136, 306, 45, 215, 10.6, 45, color="parts", est=True,
              note="tallest: rear I/O stack and the heatsink (doc 27)"))
    if F1_MODE == "SIDE":
        # F1 on the left wall behind the riser (study): two NMJ6HCD2 through the wall (18.2 x 15.67 body, depth 25 estimate), board under them
        for k, y0 in enumerate((FOLD_Y + 12, FOLD_Y + 40)):
            a(box(f"Phones {k + 1} jack", "front", SKIN, SKIN + 25, y0, y0 + 18.2, F1_SIDE_Z - 7.8, F1_SIDE_Z + 7.8, color="metal", est=True,
                  note="Neutrik NMJ6HCD2 through the left wall; body 18.2 x 15.67, depth 25 (estimate)"))
        a(box("F1 headphone board", "front", SKIN, SKIN + 100, FOLD_Y + 5, FOLD_Y + 47, F1_SIDE_Z - 9.4, F1_SIDE_Z - 7.8, color="pcb",
              note="F1 lying under the jacks, behind the riser, above A1"))
        a(box("F1 headphone board parts below", "front", SKIN + 2, SKIN + 98, FOLD_Y + 7, FOLD_Y + 45, F1_SIDE_Z - 13.4, F1_SIDE_Z - 9.4,
              color="parts", est=True))
    elif F1_MODE in ("LIP", "POCKET"):
        # study 16.11.2026: the jacks stay at the front. LIP = a 28 mm lip in front of P1 (jacks y -25..0, board on 3 mm standoffs);
        # POCKET = jack bodies sink below the floor under P1 (a pocket in the bottom, feet >= 10 mm). NMJ6HCD2 body 18.2 x 15.67, depth 25 (estimate).
        for k, x in enumerate((32, 80)):
            if F1_MODE == "LIP":
                a(box(f"Phones {k + 1} jack", "front", x - JACK_W / 2, x + JACK_W / 2, -(FL - SKIN) if FL else -25, 0, SKIN + F1_STAND + 1.6,
                      SKIN + F1_STAND + 1.6 + JACK_H, color="metal", est=True))
            else:
                a(box(f"Phones {k + 1} jack", "front", x - 9.1, x + 9.1, SKIN, SKIN + 25, -2.8, 12.87, color="metal", est=True))
        if F1_MODE == "LIP":
            f1 = _board_design("f1-phones")                    # rev 0.3: strip 135 x 27 in the lip, x 12..147 (jacks 20 and 68 on it = model x 32 and 80), all parts on top
            a(box("F1 headphone board", "front", 12, 12 + f1.W, (-(FL - SKIN) if FL else -27) + 1, (-(FL - SKIN) if FL else -27) + 1 + f1.H, SKIN + F1_STAND, SKIN + F1_STAND + 1.6, color="pcb"))
        else:
            a(box("F1 headphone board", "front", 15, 100, SKIN, 35, -4.4, -2.8, color="pcb"))
            a(box("F1 headphone board parts below", "front", 17, 98, SKIN + 2, 33, -6.4, -4.4, color="parts", est=True))
    else:
      for nm, x in (("Phones 1 jack", 32), ("Phones 2 jack", 80)):
        a(box(nm, "front", x - 10, x + 10, SKIN, 35, 17, 33, color="metal", est=True))
    if F1_MODE in ("SIDE", "LIP", "POCKET"):
        pass
    elif F1_MODE == "H":      # P94: the board lies flat right under the jack bodies
        a(box("F1 headphone board", "front", 15, 100, SKIN, 35, 15.4, 17, color="pcb", note="horizontal F1 (P94), under the jacks"))
    else:
        a(box("F1 headphone board", "front", 15, 100, 35, 36.6, 6, F1_TOP, color="pcb"))

    # slope: screen and the three slope boards
    P += screen_parts()
    P += slope_boards_and_pocket(usb)
    # the volume pots stand on W1: see w1_parts()

    # under the slope and the rear wall (doc 27 section 6, doc 29)
    # 15.11.2026: real outlines of the placed boards (A1 rev 0.4 220 x 100, PW rev 0.6 100 x 80, R1 rev 0.5 238 x 96, R2 rev 0.6 L-shape
    # 175 x 103); before they were the early estimates 140 x 90, 60 x 50, 238 x 104 and 258 x 104. Rear boards: model x = 515 - rear x.
    a(box("A1 audio board", "rear", A1_X0, A1_X0 + 220, A1_Y0, A1_Y0 + 100, A1_Z0, A1_Z0 + 22, color="pcb", note="220 x 100, rev 0.4; position not fixed"))
    if COMPUTER in ("H5REAR", "H5TILT"):
        # 16.11.2026, the user's idea: the H5 where the battery bay was (rear right, under the slope), lying flat; the battery
        # goes under the grid where the H5 used to be; PW moves 15 mm left to clear it.
        px = PW_X0 or 285
        a(box("PW power", "rear", px, px + 100, 320 + RS, 400 + RS, 6, PW_TOP, color="pcb", note="100 x 80, rev 0.6; moved for the H5"))
        rx, ry = H5_REAR_X, H5_REAR_Y
        if COMPUTER == "H5TILT":
            # the H5 lies parallel to the slope under the screen (user's sketch, 16.11.2026): board away from the slope, heatsink towards it
            nb = H5T_N - H5_H
            a(slope_box("Mini-ITX board", "itx", H5T_X, H5T_X + 120, H5T_S0, H5T_S0 + 120, nb, nb + 1.6, color="pcb"))
            a(slope_box("Mini-ITX parts H5", "itx", H5T_X, H5T_X + 120, H5T_S0, H5T_S0 + 120, nb + 1.6, H5T_N, color="parts", est=True,
                        note="ODROID-H5 lying along the slope under the screen"))
            if H5_PORT in ("E", "W"):
                x0, x1 = (H5T_X + 120, H5T_X + 120 + H5_PORT_LEN) if H5_PORT == "E" else (H5T_X - H5_PORT_LEN, H5T_X)
                a(slope_box("H5 plugs and cables", "itx", x0, x1, H5T_S0, H5T_S0 + 120, nb, nb + 22, color="plastic", est=True))
        else:
            a(box("Mini-ITX board", "itx", rx - 60, rx + 60, ry - 60, ry + 60, H5_Z0, H5_Z0 + 1.6, color="pcb"))
            a(box("Mini-ITX parts H5", "itx", rx - 60, rx + 60, ry - 60, ry + 60, H5_Z0 + 1.6, H5_Z0 + H5_H, color="parts", est=True,
                  note="ODROID-H5 in the old battery bay, 44 mm overall"))
            if H5_PORT != "none":
                L = H5_PORT_LEN
                ex = {"N": (rx - 60, rx + 60, ry + 60, ry + 60 + L), "S": (rx - 60, rx + 60, ry - 60 - L, ry - 60),
                      "E": (rx + 60, rx + 60 + L, ry - 60, ry + 60), "W": (rx - 60 - L, rx - 60, ry - 60, ry + 60)}[H5_PORT]
                a(box("H5 plugs and cables", "itx", ex[0], ex[1], ex[2], ex[3], H5_Z0, H5_Z0 + 22, color="plastic", est=True,
                      note="USB / HDMI / LAN plugs and the DC plug beyond the ports edge (estimate: 22 high)"))
        if BATT_BOXES:      # study 16.11.2026 (user): packs under the screen on a 2 mm shelf, "x0,x1,y0,y1,z0;..." (z0 = shelf underside)
            for k, (x0, x1, y0, y1, z0) in enumerate(BATT_BOXES):
                a(box(f"Battery shelf {k + 1}", "rear", x0, x1, y0, y1, z0, z0 + 2, color="metal", note="2 mm aluminium shelf"))
                a(box(f"Battery pack {k + 1}", "rear", x0, x1, y0, y1, z0 + 2, z0 + 2 + LIPO_H, color="battery",
                      note="flat LiPo 4S, <= 99 Wh each (R59, R155)"))
            if FAN:
                fy, fz, fs = (FAN + (92.0,))[:3]
                a(box(f"Fan {fs:g} x {fs:g} x 15", "rear", W - SKIN - 15, W - SKIN, fy - fs / 2, fy + fs / 2, fz, fz + fs, color="plastic",
                      note="exhaust on the right wall above the H5 (user, 16.11.2026); intake vents on the left wall"))
        elif BATT_LIPO:
            a(box("Battery bay", "rear", 130, 300, 60, 160, 3, 3 + LIPO_H, color="battery", note="flat LiPo 4S under the grid (R155), 170 x 100"))
        elif BATT_FLAT:
            a(box("Battery bay", "rear", 150, 305, 100, 175, 3, 28, color="battery", note="flat row of 8 cells under the grid, 155 x 75 x 25"))
        else:
            a(box("Battery bay", "rear", 176, 266, 87, 173, 3, 48, color="battery", note="moved under the grid"))
    else:
        a(box("PW power", "rear", 300, 400, 320 + RS, 400 + RS, 6, 24, color="pcb", note="100 x 80, rev 0.6; position not fixed"))
        a(box("Battery bay", "rear", 414, 504, 312, 398, 3, 48, color="battery"))
    a(box("R1 audio rear board", "rear", 4, 242, 413.4 + RS, 415 + RS, 8, R1_TOP, color="pcb", note="rear x 273-511, z 8-113"))
    # R2 (hardware/r2-control/gen/design.py OUTLINE): rear x 88-263, z 10-113 without the DIN window rear x 88-156, z 38-113
    a(box("R2 control rear board", "rear", 252, R2_TALL_X1, 413.4 + RS, 415 + RS, 10, R2_TOP, color="pcb", note="L-shape, tall part"))
    a(box("R2 control rear board, low arm", "rear", R2_TALL_X1, 427, 413.4 + RS, 415 + RS, 10, 38, color="pcb", note="L-shape, arm under the DIN window"))
    if REAR_JACK_TOP_R == REAR_JACK_TOP:
        a(box("Rear jacks", "rear", 5, 510, 415 + RS, D - SKIN, 8, REAR_JACK_TOP, color="metal", est=True,
              note="envelope of all rear jacks (417-457)"))
    else:
        a(box("Rear jacks", "rear", 5, 340, 415 + RS, D - SKIN, 8, REAR_JACK_TOP, color="metal", est=True,
              note="envelope of the rear jacks, left of x 340"))
        a(box("Rear jacks (right)", "rear", 340, 510, 415 + RS, D - SKIN, 8, REAR_JACK_TOP_R, color="metal", est=True,
              note="rear jacks under W2 / W3"))
    P += standoffs()
    return P


def _board_design(proj):
    spec = importlib.util.spec_from_file_location(proj.replace("-", "_") + "_design",
                                                  os.path.join(REPO, "hardware", proj, "gen", "design.py"))
    m = importlib.util.module_from_spec(spec)
    for d in (os.path.join(REPO, "hardware", proj, "gen"), os.path.join(REPO, "hardware", "common", "gen")):
        if d not in sys.path:
            sys.path.insert(0, d)
    spec.loader.exec_module(m)
    return m


def standoffs():
    """16.11.2026: the M3 holes of each board (gen/design.py HOLES) become 6 mm standoffs of the enclosure, so the holes and
    the case are one source. Floor boards: from the inner floor (z = SKIN) to the board underside (z 6); P2: from its top face
    up to the top skin. Floor boards: board x along model x, board y (KiCad, down) towards the rear."""
    out = []
    for proj, tag, x0, y0 in (("a1-digital", "A1", A1_X0, A1_Y0), ("pw-power", "PW", (PW_X0 or 285) if COMPUTER in ("H5REAR", "H5TILT") else 300, 320 + RS)):
        d = _board_design(proj)
        tray = tag == "A1" and A1_Z0 > 6.01          # A1 raised above the battery: a 2 mm tray on the four corner posts only
        if tray:
            out.append(box("A1 tray", "standoff", x0, x0 + d.W, y0, y0 + d.H, A1_Z0 - 2, A1_Z0, color="metal",
                           note="2 mm aluminium tray under the raised A1; the middle holes of A1 fasten to it"))
        for k, (hx, hy) in enumerate(d.HOLES):
            if tray and 10 < hx < d.W - 10:
                continue
            out.append(box(f"Standoff {tag} H{k + 1}", "standoff", x0 + hx - 3, x0 + hx + 3, y0 + hy - 3, y0 + hy + 3, SKIN,
                           A1_Z0 - 2 if tray else 6.0, color="metal", note=f"M3 standoff under {tag} hole H{k + 1}"))
    d = _board_design("p2-grid")
    for k, (hx, hy) in enumerate(d.HOLES):
        my = 4 + (d.H - hy)                              # P2 board y counts from the far edge (rev 0.4), the model from the front
        out.append(box(f"Standoff P2 H{k + 1}", "standoff", 110 + hx - 3, 110 + hx + 3, my - 3, my + 3, PCB_TOP + (PANEL_GAP - P2_GAP), TOP_Z - SKIN,
                       color="metal", note=f"M3 standoff from P2 hole H{k + 1} up to the top skin"))
    return out


# ------------------------------------------------------------------ separating axis test
def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def gap(A, B):
    """>0: lower bound of the distance between the boxes; <0: overlap depth along the best axis."""
    t = tuple(B.c[i] - A.c[i] for i in range(3))
    axes = list(A.ax) + list(B.ax) + [_cross(u, v) for u in A.ax for v in B.ax]
    best_sep, best_pen = -1e9, 1e9
    for L in axes:
        n = math.sqrt(_dot(L, L))
        if n < 1e-9:
            continue
        L = tuple(v / n for v in L)
        ra = sum(A.h[i] * abs(_dot(A.ax[i], L)) for i in range(3))
        rb = sum(B.h[i] * abs(_dot(B.ax[i], L)) for i in range(3))
        d = abs(_dot(t, L)) - ra - rb
        best_sep = max(best_sep, d)
        best_pen = min(best_pen, -d)
    return best_sep if best_sep > 0 else -best_pen


ALLOWED = {               # parts that are meant to touch (mounted on each other)
    ("M1 board", "M1 encoder"), ("M1 board", "M1 U"), ("M1 board", "M1 J1"), ("M1 encoder", "Top skin"),
    ("M1 board", "M1 encoder {k} pins"), ("parts below", ""), ("Mini-ITX board", "Mini-ITX parts"),
    ("Trill Bar", "Top skin"), ("Screen glass", "Slope skin"), ("Screen glass", "Screen LCD"),
    ("Screen LCD", "Screen driver"), ("pot", "Slope skin"), ("pot", "W1 Levels"), ("receptacle", "W3 System"), ("microSD", "W3 System"),
    ("Battery bay", "Floor"), ("Rear jacks", "Rear wall"), ("Rear jacks", "rear board"),
    ("Phones", "Front wall"), ("Phones", "Side left"), ("Phones", "F1 headphone"), ("Crossfader", "P4 Right"), ("Crossfader", "Top skin"),
    ("Wheel bearing housing", "Top skin"), ("Wheel detent collar", "Top skin"), ("Wheel detent pawl", "Wheel detent collar"), ("Wheel magnet", "P4 Right"), ("Wheel AS5600", "P4 Right"),
    ("receptacle", "Pocket board"), ("M5 Gain", "Slope skin"), ("M5 module", "M5 Gain"), ("W1 Levels", "W1 "), ("SD socket", "W3 System"), ("Screen ", "Screen "),
    ("Trill Bar", "P2 Grid"), ("Front wall", ""), ("Rear wall", ""), ("Floor", ""), ("Side", ""),
    ("Standoff A1", "A1 audio"), ("Standoff PW", "PW power"), ("Standoff P2", "P2 Grid"), ("Standoff P2", "Top skin"),
}


def allowed(a, b):
    for p, q in ALLOWED:
        for x, y in ((a, b), (b, a)):
            if p.replace(" {k}", "") in x and (q == "" or q in y):
                return True
    return False


def check(P):
    res = []
    Q = [p for p in P if p.check]
    for i, A in enumerate(Q):
        for B in Q[i + 1:]:
            if A.group == B.group == "shell":
                continue
            g = gap(A, B)
            if g >= GAP_MIN:
                continue
            touching = g > -0.05
            if allowed(A.name, B.name) and (touching or g > -0.3 or A.group == B.group):
                continue
            if A.group == B.group and touching:
                continue
            res.append((round(g, 2), A.name, B.name, A.est or B.est))
    return sorted(res)


def report(P, res):
    col = [r for r in res if r[0] < -0.05]
    tight = [r for r in res if r[0] >= -0.05]
    L = [f"# Fit check: {len(P)} parts, {len(col)} collisions, {len(tight)} tight spots (< {GAP_MIN:g} mm)", ""]
    for title, rows in (("Collisions (overlap, mm)", col), ("Tight spots (gap, mm)", tight)):
        L.append(f"## {title}")
        L += [f"- {abs(g) if g < 0 else g:g} mm: {a} / {b}{' (estimate involved)' if e else ''}" for g, a, b, e in rows] or ["- none"]
        L.append("")
    return "\n".join(L)


def usb_table():
    """Every USB-A variant: where the top of the receptacle ends up and what it hits."""
    L = ["## USB-A in the System pocket: variants", "",
         "| Variant | Part | Top vs. outer surface, mm | Collisions / gaps < 1 mm |", "|---|---|---|---|"]
    for v, (where, hgt, note) in USB_VARIANTS.items():
        P = parts(v)
        _, top = usb_receptacle(v)
        mine = [r for r in check(P) if "USB-A" in r[1] or "USB-A" in r[2] or "Pocket board" in r[1] + r[2]]
        hits = "; ".join(f"{a} / {b}: {g:g}" for g, a, b, e in mine) or "none"
        pos = f"+{top:.1f} (sticks out)" if top > 0.05 else f"{top:.1f} (inside)"
        L.append(f"| {v} | {note} | {pos} | {hits} |")
    return "\n".join(L)


if __name__ == "__main__":
    P = parts()
    res = check(P)
    print(report(P, res))
    print(usb_table())
    if "--json" in sys.argv:
        json.dump([p.dict() for p in P], open(os.path.join(HERE, "fit_parts.json"), "w"), ensure_ascii=False, indent=0)
