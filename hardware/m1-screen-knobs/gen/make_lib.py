#!/usr/bin/env python3
"""Project library for the Shtuka Druka boards: symbols and footprints that the stock KiCad
libraries do not have.

Writes ../lib/ShtukaDruka.kicad_sym and ../lib/ShtukaDruka.pretty/*.kicad_mod in the KiCad 7
file format (KiCad 7-10 read it). Sources of every number are in the comments.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (this script).
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "..", "lib")
KICAD_SYMBOLS = os.environ.get("KICAD_SYMBOL_DIR", "/usr/share/kicad/symbols")

F = "(effects (font (size 1.27 1.27)))"
FH = "(effects (font (size 1.27 1.27)) hide)"


def prop(name, value, x=0, y=0, hide=False, justify=None):
    j = f" (justify {justify})" if justify else ""
    eff = f"(effects (font (size 1.27 1.27)){j}{' hide' if hide else ''})"
    return f'    (property "{name}" "{value}" (at {x:g} {y:g} 0)\n      {eff}\n    )\n'


def pin(kind, x, y, angle, name, number, length=2.54, hidden=False):
    return (f'      (pin {kind} line (at {x:g} {y:g} {angle}) (length {length:g}){" hide" if hidden else ""}\n'
            f'        (name "{name}" {F})\n        (number "{number}" {F})\n      )\n')


# ---------------------------------------------------------------- IS31FL3741A
# Pin numbers: Lumissil IS31FL3741A datasheet (QFN-60), cross-checked against two independent
# open symbols (keyboardio-kicad-libraries, arturo182/kicad-library, MIT). EP = pin 61 = GND.
def is31fl3741a():
    left = [("14", "AVCC", "power_in"), ("15", "PVCC", "power_in"), ("25", "PVCC", "power_in"), None,
            ("9", "SDA", "bidirectional"), ("10", "SCL", "input"), ("7", "~{INTB}", "open_collector"),
            ("11", "SDB", "input"), ("8", "ADDR", "input"), None, ("13", "R_EXT", "passive"), None,
            ("12", "GND", "power_in"), ("36", "GND", "passive"), ("55", "GND", "passive"), ("61", "EP", "passive")]
    cs_pin = {}
    for i in range(1, 40):           # CS1..CS39 -> pins (see datasheet table)
        if i <= 10:
            cs_pin[i] = 25 + i       # 26..35
        elif i <= 28:
            cs_pin[i] = 26 + i       # 37..54
        elif i <= 33:
            cs_pin[i] = 27 + i       # 56..60
        else:
            cs_pin[i] = i - 33       # 1..6
    right = [(str(15 + k), f"SW{k}", "passive") for k in range(1, 10)] + [None] + \
            [(str(cs_pin[i]), f"CS{i}", "passive") for i in range(1, 40)]
    h = len(right) * 2.54
    top = h / 2 + 2.54
    s = '  (symbol "IS31FL3741A" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)\n'
    s += prop("Reference", "U", -10.16, top + 1.27, justify="left")
    s += prop("Value", "IS31FL3741A", -10.16, -top - 1.27, justify="left")
    s += prop("Footprint", "ShtukaDruka:QFN-60-1EP_7x7mm_P0.4mm_EP5.25x5.25mm", 0, 0, hide=True)
    s += prop("Datasheet", "https://www.lumissil.com/assets/pdf/core/IS31FL3741A_DS.pdf", 0, 0, hide=True)
    s += prop("ki_description", "39x9 matrix LED driver, I2C, 29 kHz PWM, QFN-60 7x7", 0, 0, hide=True)
    s += prop("LCSC", "C2940604", 0, 0, hide=True)
    s += '    (symbol "IS31FL3741A_0_1"\n'
    s += f'      (rectangle (start -10.16 {top:g}) (end 10.16 {-top:g}) (stroke (width 0.254) (type default)) (fill (type background)))\n'
    s += '    )\n    (symbol "IS31FL3741A_1_1"\n'
    y = top - 2.54
    for p in left:
        if p:
            s += pin(p[2], -12.7, round(y, 2), 0, p[1], p[0])
        y -= 2.54
    y = top - 2.54
    for p in right:
        if p:
            s += pin(p[2], 12.7, round(y, 2), 180, p[1], p[0])
        y -= 2.54
    s += '    )\n  )\n'
    return s


def stock(lib, name):
    """Return the text of a stock KiCad symbol block (top level, two-space indent)."""
    txt = open(os.path.join(KICAD_SYMBOLS, lib + ".kicad_sym")).read()
    i = txt.find(f'\n  (symbol "{name}"')
    j = txt.find('\n  (symbol "', i + 5)
    if j < 0:
        j = txt.rfind('\n)')
    return txt[i + 1:j] + "\n"


# ---------------------------------------------------------------- XL-1615RGBC-RF
# XINGLIGHT datasheet (LCSC C965840), "Outline Dimension": 1 = R cathode, 2 = common anode,
# 3 = G cathode, 4 = B cathode. Graphics from Device:LED_ARGB, pins renumbered to the datasheet.
def xl1615():
    s = stock("Device", "LED_ARGB").replace('"LED_ARGB', '"XL-1615RGBC-RF')
    renum = {"A": "2", "RK": "1", "GK": "3", "BK": "4"}
    def fix(m):
        return f'(name "{m.group(1)}"{m.group(2)}(number "{renum[m.group(1)]}"'
    s = re.sub(r'\(name "(A|RK|GK|BK)"(.*?)\(number "\d"', fix, s, flags=re.S)
    s = re.sub(r'\(property "Value" "[^"]*"', '(property "Value" "XL-1615RGBC-RF"', s)
    s = re.sub(r'\(property "Footprint" "[^"]*"', '(property "Footprint" "ShtukaDruka:LED_RGB_XL-1615RGBC_1.6x1.5mm"', s)
    s = re.sub(r'\(property "Datasheet" "[^"]*"', '(property "Datasheet" "https://www.lcsc.com/datasheet/C965840.pdf"', s)
    s = s.replace('(property "ki_description" "RGB LED, anode/red/green/blue"',
                  '(property "ki_description" "RGB LED 1.6x1.5 mm, common anode; pins 1 R, 2 A, 3 G, 4 B"')
    s = s.replace("    (symbol \"XL-1615RGBC-RF_0_0\"", "    (symbol \"XL-1615RGBC-RF_0_0\"")
    s = s.replace('    (property "ki_fp_filters"', '    (property "LCSC" "C965840" (at 0 0 0)\n      ' + FH + '\n    )\n    (property "ki_fp_filters"', 1)
    return s


# ---------------------------------------------------------------- encoder with touch pin
# Device:RotaryEncoder_Switch plus the MP pin (metal frame and shaft): it is the touch electrode.
def encoder():
    s = stock("Device", "RotaryEncoder_Switch").replace('"RotaryEncoder_Switch', '"RotaryEncoder_Switch_Touch')
    s = re.sub(r'\(property "Value" "[^"]*"', '(property "Value" "EC11E smooth, switch"', s)
    s = s.replace("(pin_names (offset 0.254) hide)", "(pin_names (offset 0.254))")
    s = re.sub(r'\(property "Footprint" "[^"]*"',
               '(property "Footprint" "Rotary_Encoder:RotaryEncoder_Alps_EC11E-Switch_Vertical_H20mm"', s)
    s = s.replace('with switch"', 'with switch; MP = metal frame and shaft, used as the touch electrode"')
    i = s.rfind('      (pin passive line')
    mp = pin("passive", 0, -7.62, 90, "MP", "MP")
    return s[:i] + mp + s[i:]


def write_symbols():
    out = "(kicad_symbol_lib (version 20220914) (generator shtuka_druka_make_lib)\n"
    out += is31fl3741a() + xl1615() + encoder() + ")\n"
    os.makedirs(LIB, exist_ok=True)
    open(os.path.join(LIB, "ShtukaDruka.kicad_sym"), "w").write(out)


# ---------------------------------------------------------------- footprints
def fp_head(name, descr, tags, smd=True):
    return (f'(footprint "{name}" (version 20221018) (generator shtuka_druka_make_lib)\n'
            f'  (layer "F.Cu")\n  (descr "{descr}")\n  (tags "{tags}")\n'
            f'  (attr {"smd" if smd else "through_hole"})\n')


def fp_text(kind, text, x, y, layer, size=1.0):
    return (f'  (fp_text {kind} "{text}" (at {x:g} {y:g}) (layer "{layer}")\n'
            f'    (effects (font (size {size:g} {size:g}) (thickness {size * 0.15:g})))\n  )\n')


def fp_rect(x0, y0, x1, y1, layer, w):
    return f'  (fp_rect (start {x0:g} {y0:g}) (end {x1:g} {y1:g}) (stroke (width {w:g}) (type solid)) (fill none) (layer "{layer}"))\n'


def fp_line(x0, y0, x1, y1, layer, w):
    return f'  (fp_line (start {x0:g} {y0:g}) (end {x1:g} {y1:g}) (stroke (width {w:g}) (type solid)) (layer "{layer}"))\n'


def smd_pad(num, x, y, w, h, angle=0, shape="roundrect", layers='"F.Cu" "F.Paste" "F.Mask"'):
    rr = " (roundrect_rratio 0.25)" if shape == "roundrect" else ""
    a = f" {angle:g}" if angle else ""
    return f'  (pad "{num}" smd {shape} (at {x:g} {y:g}{a}) (size {w:g} {h:g}) (layers {layers}){rr})\n'


def led1615():
    # Datasheet "Recommended Soldering Pattern": pads 0.45 x 0.65, gaps 0.8 (x) and 0.3 (y),
    # centre pitch 1.25 x 0.95. Top view: 1 top-left, 2 bottom-left (anode, mark), 3 top-right, 4 bottom-right.
    n = "LED_RGB_XL-1615RGBC_1.6x1.5mm"
    s = fp_head(n, "RGB LED 1.6x1.5 mm common anode, XINGLIGHT XL-1615RGBC-RF (LCSC C965840), land pattern from the datasheet",
                "LED RGB 1615")
    s += fp_text("reference", "REF**", 0, -1.6, "F.SilkS", 0.6) + fp_text("value", n, 0, 1.6, "F.Fab", 0.4)
    for num, x, y in (("1", -0.625, -0.475), ("2", -0.625, 0.475), ("3", 0.625, -0.475), ("4", 0.625, 0.475)):
        s += smd_pad(num, x, y, 0.45, 0.65)
    s += fp_rect(-0.8, -0.75, 0.8, 0.75, "F.Fab", 0.1)
    s += fp_line(-1.15, 0.2, -1.15, 0.75, "F.SilkS", 0.12)     # anode (pin 2) side mark
    s += fp_rect(-1.2, -1.05, 1.2, 1.05, "F.CrtYd", 0.05)
    return n, s


def qfn60():
    # 7x7 mm, 0.4 mm pitch, 15 pins per side; EP 5.25 mm (same as arturo182 IS31FL3741 breakout, MIT).
    n = "QFN-60-1EP_7x7mm_P0.4mm_EP5.25x5.25mm"
    s = fp_head(n, "QFN-60 7x7 mm, 0.4 mm pitch, exposed pad 5.25 mm, 9 thermal vias (Lumissil IS31FL3741A)", "QFN 60 0.4")
    s += fp_text("reference", "REF**", 0, -4.8, "F.SilkS", 0.8) + fp_text("value", n, 0, 4.8, "F.Fab", 0.5)
    c, L, W = 3.45, 0.8, 0.2
    for k in range(15):
        o = -2.8 + 0.4 * k
        s += smd_pad(str(1 + k), -c, o, L, W)            # left, top to bottom
        s += smd_pad(str(16 + k), o, c, W, L)            # bottom, left to right
        s += smd_pad(str(31 + k), c, -o, L, W)           # right, bottom to top
        s += smd_pad(str(46 + k), -o, -c, W, L)          # top, right to left
    s += smd_pad("61", 0, 0, 5.25, 5.25, shape="rect", layers='"F.Cu" "F.Mask"')
    for i in (-1, 0, 1):                                 # 3 x 3 paste windows, ~60 % of the pad
        for j in (-1, 0, 1):
            s += smd_pad("", 1.75 * i, 1.75 * j, 1.35, 1.35, shape="roundrect", layers='"F.Paste"')
    for x, y in ((-0.875, -0.875), (0.875, -0.875), (-0.875, 0.875), (0.875, 0.875),
                 (0, -0.875), (0, 0.875), (-0.875, 0), (0.875, 0)):   # thermal vias in the gaps between windows
        s += f'  (pad "61" thru_hole circle (at {x:g} {y:g}) (size 0.6 0.6) (drill 0.3) (layers "*.Cu"))\n'
    s += fp_rect(-3.5, -3.5, 3.5, 3.5, "F.Fab", 0.1)
    s += fp_line(-3.6, -3.6, -3.0, -3.6, "F.SilkS", 0.12) + fp_line(-3.6, -3.6, -3.6, -3.0, "F.SilkS", 0.12)
    s += f'  (fp_circle (center -4.1 -2.8) (end -3.95 -2.8) (stroke (width 0.3) (type solid)) (fill solid) (layer "F.SilkS"))\n'
    s += fp_rect(-4.1, -4.1, 4.1, 4.1, "F.CrtYd", 0.05)
    return n, s


def write_footprints():
    d = os.path.join(LIB, "ShtukaDruka.pretty")
    os.makedirs(d, exist_ok=True)
    for n, s in (led1615(), qfn60()):
        open(os.path.join(d, n + ".kicad_mod"), "w").write(s + ")\n")


if __name__ == "__main__":
    write_symbols()
    write_footprints()
    print("ok", LIB)
