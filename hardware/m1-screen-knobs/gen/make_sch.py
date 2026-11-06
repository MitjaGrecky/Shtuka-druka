#!/usr/bin/env python3
"""Write the M1 schematic (KiCad 7 file format; KiCad 7-10 open it) from design.py.

Every pin gets a net label (or a power symbol) right at its end: the drawing stays readable
and the netlist matches design.py exactly. Run: python3 make_sch.py
License: AGPL-3.0-or-later (code), CERN-OHL-S-2.0 (the generated schematic).
"""
import os
import re
import uuid

import design as D

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", D.NAME + ".kicad_sch")
KSYM = os.environ.get("KICAD_SYMBOL_DIR", "/usr/share/kicad/symbols")
PROJ_LIB = os.path.join(HERE, "..", "lib", "ShtukaDruka.kicad_sym")
NS = uuid.UUID("6f1d3c2a-6a43-4f53-9a51-5d7b1f0c0a11")       # stable uuids between runs
ROOT = str(uuid.uuid5(NS, "root"))
POWER = {"+5V", "+3V3", "GND"}


def uid(*k):
    return str(uuid.uuid5(NS, "/".join(map(str, k))))


def q(s):
    return '"' + s.replace('"', '\\"') + '"'


# ------------------------------------------------------------------ library symbols
_cache = {}


def lib_block(lib_id):
    """Symbol text renamed to lib_id, flattened if it extends another symbol."""
    if lib_id in _cache:
        return _cache[lib_id]
    lib, name = lib_id.split(":")
    path = PROJ_LIB if lib == "ShtukaDruka" else os.path.join(KSYM, lib + ".kicad_sym")
    txt = open(path).read()

    def block(n):
        i = txt.find(f'\n  (symbol "{n}"')
        assert i >= 0, (lib_id, n)
        j = txt.find('\n  (symbol "', i + 5)
        if j < 0:
            j = txt.rfind('\n)')
        return txt[i + 1:j]

    b = block(name)
    m = re.search(r'\(extends "([^"]+)"\)', b)
    if m:                                   # flatten: parent's drawing, child's name and value
        parent = m.group(1)
        b = block(parent).replace(f'(symbol "{parent}_', f'(symbol "{name}_')
        b = b.replace(f'(property "Value" "{parent}"', f'(property "Value" "{name}"')
        b = b.replace(f'(symbol "{parent}"', f'(symbol "{name}"', 1)
    b = b.replace(f'(symbol "{name}"', f'(symbol "{lib_id}"', 1)
    pins = {}
    for t, x, y, a, num in re.findall(
            r'\(pin (\w+) \w+ \(at ([-\d.]+) ([-\d.]+) (\d+)\) \(length [\d.]+\)[^\n]*\n\s*\(name "[^"]*".*?\n\s*\(number "([^"]+)"', b):
        pins[num] = (float(x), float(y), int(a), t)
    props = {k: (float(x), float(y)) for k, x, y in re.findall(r'\(property "(\w+)" "[^"]*" \(at ([-\d.]+) ([-\d.]+)', b)}
    _cache[lib_id] = (b, pins, props)
    return _cache[lib_id]


def rot(x, y, r):
    r %= 360
    return {0: (x, y), 90: (-y, x), 180: (-x, -y), 270: (y, -x)}[r]


# ------------------------------------------------------------------ writer
class Sch:
    def __init__(self):
        self.items, self.used, self.npwr = [], [], 0

    def symbol(self, ref, lib_id, value, x, y, r=0, fp="", fields=None, nets=None, dnp=False, in_bom=True):
        b, pins, props = lib_block(lib_id)
        if lib_id not in self.used:
            self.used.append(lib_id)
        u = uid("sym", ref)
        s = f'  (symbol (lib_id {q(lib_id)}) (at {x:g} {y:g} {r}) (unit 1)\n'
        s += f'    (in_bom {"yes" if in_bom else "no"}) (on_board yes) (dnp {"yes" if dnp else "no"})\n'
        s += f'    (uuid {u})\n'
        hide_ref = ref.startswith("#")
        fl = [("Reference", ref, hide_ref), ("Value", value, False), ("Footprint", fp, True), ("Datasheet", "~", True)]
        for k, v in (fields or {}).items():
            fl.append((k, v, True))
        for k, v, hide in fl:
            px, py = props.get(k, (0, 0))
            px, py = rot(px, py, r)
            s += (f'    (property {q(k)} {q(v)} (at {x + px:g} {y - py:g} 0)\n'
                  f'      (effects (font (size 1.27 1.27)){" hide" if hide else ""})\n    )\n')
        for num in pins:
            s += f'    (pin {q(num)} (uuid {uid("pin", ref, num)}))\n'
        s += f'    (instances\n      (project {q(D.NAME)}\n        (path "/{ROOT}" (reference {q(ref)}) (unit 1))\n      )\n    )\n  )\n'
        self.items.append(s)
        # connections at pin ends
        for num, (px, py, a, t) in pins.items():
            if nets is None or num not in nets:
                continue
            dx, dy = rot(px, py, r)
            ex, ey = round(x + dx, 3), round(y - dy, 3)
            out = (a + 180 + r) % 360            # direction away from the body
            net = nets[num]
            if net is None:
                self.items.append(f'  (no_connect (at {ex:g} {ey:g}) (uuid {uid("nc", ref, num)}))\n')
            elif net in POWER:
                self.power(net, ex, ey, out)
            else:
                self.label(net, ex, ey, out, (ref, num))

    def label(self, net, x, y, a, key):
        just = "left" if a in (0, 90) else "right"
        self.items.append(f'  (label {q(net)} (at {x:g} {y:g} {a})\n    (effects (font (size 1.27 1.27)) (justify {just} bottom))\n'
                          f'    (uuid {uid("lbl", *key)})\n  )\n')

    def power(self, net, x, y, out, flag=False):
        self.npwr += 1
        lib = "power:" + net
        base = 90 if net != "GND" else 270           # where the symbol body points by default
        r = (out - base) % 360
        self.symbol(f"#PWR{self.npwr:03d}", lib, net, x, y, r, in_bom=False)
        if flag:
            self.npwr += 1
            self.symbol(f"#FLG{self.npwr:03d}", "power:PWR_FLAG", "PWR_FLAG", x, y, r, in_bom=False)

    def text(self, t, x, y, size=2.0):
        self.items.append(f'  (text {q(t)} (at {x:g} {y:g} 0)\n    (effects (font (size {size:g} {size:g})) (justify left bottom))\n'
                          f'    (uuid {uid("txt", t[:40], x, y)})\n  )\n')

    def write(self, path):
        libs = "".join("  " + lib_block(l)[0].replace("\n", "\n  ") + "\n" for l in self.used)
        s = (f'(kicad_sch (version 20230121) (generator eeschema)\n\n  (uuid {ROOT})\n\n  (paper "A1")\n\n'
             f'  (title_block\n    (title {q(D.TITLE)})\n    (rev {q(D.REV)})\n    (company "Shtuka Druka - open hardware, CERN-OHL-S-2.0")\n'
             f'    (comment 1 "Generated by hardware/m1-screen-knobs/gen/make_sch.py from design.py - edit the script, not this file")\n'
             f'    (comment 2 "LED map: design.py led_matrix() - cell per 4 rings, CS triples stay on their rings (doc 33)")\n  )\n\n'
             f'  (lib_symbols\n{libs}  )\n\n' + "".join(self.items) +
             f'\n  (sheet_instances\n    (path "/" (page "1"))\n  )\n)\n')
        open(path, "w").write(s)


def main():
    P = {p["ref"]: p for p in D.parts()}
    S = Sch()

    def put(ref, x, y, r=0):
        p = P[ref]
        f = {k: v for k, v in p["fields"].items() if k not in ("DNP", "Side")}
        S.symbol(ref, p["lib"], p["value"], x, y, r, p["fp"], f, p["pins"], dnp=p["fields"].get("DNP") == "yes",
                 in_bom=p["fields"].get("DNP") != "yes")

    g = 2.54
    # power entry and flags
    S.text("Module bus (P77): same 2x7 1.27 mm connector on every encoder module", 20 * g, 8 * g)
    put("J1", 30 * g, 18 * g)
    for n, (net, x) in enumerate((("+5V", 14), ("+3V3", 18), ("GND", 22))):
        S.power(net, x * g, 34 * g, 90 if net != "GND" else 270, flag=True)
    for i, ref in enumerate(("C12", "C13")):
        put(ref, (14 + 6 * i) * g, 42 * g)
    # LED driver
    S.text("LED drivers (P98): IS31FL3741A, U1 cell A 0x30, U6 cell B 0x31", 66 * g, 4 * g)
    put("U1", 62 * g, 60 * g)
    for i, ref in enumerate(("R1", "R2", "R3", "R4", "R5", "R6", "C1", "C2", "C3", "C4")):
        put(ref, (80 + 5 * i) * g, 14 * g)
    put("U6", 262 * g, 60 * g)
    for i, ref in enumerate(("R19", "R20", "R21", "R22", "R23", "R24", "C14", "C15", "C16", "C17")):
        put(ref, (210 + 5 * i) * g, 14 * g)
    # touch
    S.text("Touch: CY8CMBR3108, electrode = encoder frame and shaft (MP)", 80 * g, 26 * g)
    put("U2", 92 * g, 40 * g)
    for i in range(8):
        put(f"R{7 + i}", (104 + 4 * i) * g, 32 * g)
    for i, ref in enumerate(("C5", "C6", "C7", "C8", "R15", "R16", "R17", "R18")):
        put(ref, (104 + 4 * i) * g, 46 * g)
    # shift registers
    S.text("Encoders A/B/push: 3 x 74HC165, host reads U3 D7..D0, U4, U5", 140 * g, 8 * g)
    for i, u in enumerate(("U3", "U4", "U5")):
        put(u, (146 + 26 * i) * g, 22 * g)
        put(f"C{9 + i}", (156 + 26 * i) * g, 36 * g)
    for i in range(6):
        put(f"RN{i + 1}", (146 + 13 * i) * g, 46 * g)
    # encoders
    S.text("Knobs Param 1-8 (left to right on the panel)", 80 * g, 58 * g)
    for k in range(8):
        put(f"ENC{k + 1}", (88 + 16 * k) * g, 66 * g)
    # LED matrix
    S.text("LED rings: row = ring (knob 1-8), column = dot 1-13 clockwise from the lower left", 20 * g, 82 * g)
    for k in range(8):
        for i in range(D.RING_N):
            put(f"D{k * D.RING_N + i + 1}", (24 + 13 * i) * g, (90 + 9 * k) * g)
    for h in range(len(D.HOLES)):
        put(f"H{h + 1}", (200 + 6 * h) * g, 66 * g)
    S.write(OUT)
    print("ok", OUT, len(P), "parts")


if __name__ == "__main__":
    main()
