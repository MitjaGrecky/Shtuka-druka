#!/usr/bin/env python3
"""KiCad-7-format symbol libraries for machines with a newer KiCad (the PC has KiCad 10).

The schematic writer (m1-screen-knobs/gen/make_sch.py) copies library symbols into the schematic
and reads their pins with KiCad 7 file-format regexes; KiCad 10 ships its libraries in another
layout (tabs, (hide yes), ...), which the writer cannot read and KiCad 7 / EasyEDA cannot load.
This script rebuilds the needed standard symbols from the lib_symbols blocks of the repository's
generated schematics (written with KiCad 7 libraries by the cloud side) into <out>/<lib>.kicad_sym.
Project symbols (ShtukaDruka) are read from the project library as before.

Usage: python sym7.py [OUT_DIR]        (default: hardware/common/sym7, git-ignored)
Then:  KICAD_SYMBOL_DIR=<OUT_DIR> python make_sch.py
License: AGPL-3.0-or-later.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.abspath(os.path.join(HERE, "..", ".."))
DEFAULT_OUT = os.path.join(HW, "common", "sym7")


def blocks(sch_text):
    """Top-level symbols of the lib_symbols section: {lib_id: text}."""
    i = sch_text.find("\n  (lib_symbols")
    if i < 0:
        return {}
    j = sch_text.find("\n  )\n", i)
    sec = sch_text[i:j]
    out = {}
    heads = list(re.finditer(r'\n    \(symbol "([^"]+)"', sec))
    for n, m in enumerate(heads):
        end = heads[n + 1].start() if n + 1 < len(heads) else len(sec)
        out[m.group(1)] = sec[m.start() + 1:end]
    return out


# Symbols that no KiCad 7 schematic of the repository contains yet: converted from the installed (newer) KiCad library.
EXTRA = {"Interface_Expansion": ["TCA9546APW"],
         "Connector_Generic": ["Conn_02x08_Odd_Even", "Conn_01x02", "Conn_01x03", "Conn_01x04", "Conn_01x05", "Conn_02x05_Odd_Even"],
         # R2 control board (13.11.2026)
         "MCU_RaspberryPi": ["RP2350A"], "Interface_USB": ["USB2514B_Bi"], "Analog_DAC": ["DAC80504"],
         "Amplifier_Operational": ["OPA4197xD"], "Isolator": ["TLP2361"], "Memory_Flash": ["W25Q16JVSS"],
         "Connector": ["DIN-5", "Barrel_Jack_Switch", "USB_C_Receptacle_USB2.0_14P", "USB_C_Receptacle_USB2.0_16P", "USB_A"],
         "Connector_Audio": ["AudioJack2_SwitchT", "AudioJack3"], "Regulator_Linear": ["AP2112K-3.3"], "Power_Protection": ["USBLC6-2SC6"],
         "Transistor_BJT": ["MMBT3904"], "Diode": ["BAT54S", "1N4148W"],
         "Device": ["Crystal_GND24", "L", "LED", "C_Polarized", "Fuse", "D_TVS", "D_Schottky"],
         # PW power board (14.11.2026)
         "Power_Management": ["LM74700"], "Regulator_Switching": ["LM5176PWP", "LM5156HPWP", "TPS54560BDDA", "LMR33640ADDA"],
         "Transistor_FET": ["CSD18540Q5B", "IRLML2060"]}
EXTRA["Interface_USB"].append("TPS25730D")
EXTRA["Regulator_Linear"] += ["TPS7A4701xRGW", "TPS7A3301RGW", "TPS7A4101DGN"]
EXTRA["Connector_Generic"] += ["Conn_02x02_Odd_Even", "Conn_02x03_Odd_Even"]
EXTRA.setdefault("Sensor_Energy", []).append("INA226")    # PW power monitor (R146)
EXTRA.setdefault("74xx", []).append("74HC595")              # R2 output expander (task #25)
# R1 audio board (14.11.2026)
EXTRA["Connector_Audio"] += ["NCJ6FI-V", "AudioJack2"]
EXTRA["Connector_Generic"] += ["Conn_02x20_Odd_Even", "Conn_02x25_Odd_Even", "Conn_02x07_Odd_Even"]
EXTRA["Transistor_BJT"] += ["MMBTA92", "MMBTA42"]
EXTRA["Transistor_FET"] += ["2N7002"]
EXTRA["Diode"] += ["1N4148W"]
EXTRA.setdefault("Relay", []).append("Omron_G6K-2")
EXTRA.setdefault("Amplifier_Operational", []).append("OPA1612AxD")
# Pin types changed in the copies: a second OUT pin of the same regulator as power_out would make ERC report two
# power outputs on one net; the copy keeps one power_out and marks the other passive (as KiCad does for TPS7A3301).
PIN_TYPE = {"TPS7A4701xRGW": {"20": "passive"},
            "LM5175PWP": {"12": "input"}}      # VOSNS senses the output (an input), typed output in the library;
                                               # LM5176PWP extends LM5175PWP, so the base symbol is patched
KSYM10 = os.environ.get("KICAD10_SYMBOL_DIR", r"C:\Program Files\KiCad\10.0\share\kicad\symbols")
DROP = {"exclude_from_sim", "in_pos_files", "duplicate_pin_numbers_are_jumpers", "show_name", "do_not_autoplace",
        "embedded_fonts", "embedded_files", "unit_name", "body_styles"}


def _parse(text):
    tok = re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+', text)
    stack, cur = [], []
    for t in tok:
        if t == "(":
            stack.append(cur)
            cur = []
        elif t == ")":
            done, cur = cur, stack.pop()
            cur.append(done)
        else:
            cur.append(t)
    return cur


def _k7(node):
    """KiCad 9/10 node -> KiCad 7 node: drop new tokens, (hide yes) -> bare hide where KiCad 7 wants it."""
    if not isinstance(node, list):
        return node
    head = node[0] if node else None
    kids = [c for c in node[1:] if not (isinstance(c, list) and c and c[0] in DROP)]
    hide = any(isinstance(c, list) and c[:2] == ["hide", "yes"] for c in kids)
    kids = [c for c in kids if not (isinstance(c, list) and c and c[0] == "hide")]
    kids = [c for c in kids if not (isinstance(c, list) and c and c[0] in ("bold", "italic") and c[1:] == ["no"])]
    kids = [[c[0]] if isinstance(c, list) and c and c[0] in ("bold", "italic") else c for c in kids]
    kids = [c[0] if c == ["bold"] or c == ["italic"] else _k7(c) for c in kids]
    if hide:
        if head == "property":                          # property: hide goes into effects
            for c in kids:
                if isinstance(c, list) and c and c[0] == "effects":
                    c.append("hide")
        else:                                           # pin_names, pin_numbers, pin: bare token
            kids.append("hide")
    return [head] + kids


def _inline(n):
    return n if not isinstance(n, list) else "(" + " ".join(_inline(c) for c in n) + ")"


def _emit(sym, ind="  "):
    """Top-level or unit symbol in KiCad 7 layout: one child per line, pins as 'pin ... (length)' then name, number lines."""
    lines = [f"{ind}(symbol {sym[1]}" + "".join(" " + _inline(c) for c in sym[2:] if not isinstance(c, list) or c[0] in ("pin_names", "pin_numbers", "in_bom", "on_board", "extends", "power"))]
    for c in sym[2:]:
        if not isinstance(c, list) or c[0] in ("pin_names", "pin_numbers", "in_bom", "on_board", "extends", "power"):
            continue
        if c[0] == "symbol":
            lines.append(_emit(c, ind + "  "))
        elif c[0] == "pin":
            head = [x for x in c[1:] if not (isinstance(x, list) and x[0] in ("name", "number", "alternate"))]
            rest = [x for x in c[1:] if isinstance(x, list) and x[0] in ("name", "number", "alternate")]
            lines.append(f"{ind}  (pin " + " ".join(_inline(x) for x in head))
            lines += [f"{ind}    {_inline(x)}" for x in rest]
            lines.append(f"{ind}  )")
        else:
            lines.append(f"{ind}  {_inline(c)}")
    lines.append(f"{ind})")
    return "\n".join(lines)


def from_kicad10(lib, names):
    """KiCad-7-format text blocks of the named symbols (and the symbols they extend) of a KiCad 9/10 library."""
    root = _parse(open(os.path.join(KSYM10, lib + ".kicad_sym"), encoding="utf-8").read())[0]
    syms = {c[1].strip('"'): c for c in root if isinstance(c, list) and c and c[0] == "symbol"}
    want, out = [n for n in names if n in syms], {}     # a symbol missing in an older installed library comes from the schematics
    while want:
        n = want.pop()
        if n in out:
            continue
        s = _k7(syms[n])
        for num, typ in PIN_TYPE.get(n, {}).items():       # pin type patches (see PIN_TYPE)
            for unit in s:
                if isinstance(unit, list) and unit and unit[0] == "symbol":
                    for pin in unit:
                        if isinstance(pin, list) and pin and pin[0] == "pin" and any(
                                isinstance(x, list) and x[:2] == ["number", f'"{num}"'] for x in pin):
                            pin[1] = typ
        out[n] = _emit(s)
        for c in s:
            if isinstance(c, list) and c and c[0] == "extends":
                want.append(c[1].strip('"'))
    return out


def build(out=DEFAULT_OUT):
    libs = {}
    for lib, names in EXTRA.items():
        if os.path.exists(os.path.join(KSYM10, lib + ".kicad_sym")):
            for n, b in from_kicad10(lib, names).items():
                libs.setdefault(lib, {})[n] = b
    for sch in sorted(glob.glob(os.path.join(HW, "*", "*.kicad_sch"))):
        txt = open(sch, encoding="utf-8").read()
        if "(version 2023" not in txt[:200] and "(version 2022" not in txt[:200]:
            continue                                   # only KiCad 7 files
        for lib_id, b in blocks(txt).items():
            lib, name = lib_id.split(":", 1)
            if lib == "ShtukaDruka":
                continue
            b = "\n".join(l[2:] if l.startswith("  ") else l for l in b.rstrip().split("\n"))   # 4 -> 2 spaces
            b = b.replace(f'(symbol "{lib_id}"', f'(symbol "{name}"', 1)
            libs.setdefault(lib, {}).setdefault(name, b)
    os.makedirs(out, exist_ok=True)
    for lib, syms in libs.items():
        with open(os.path.join(out, lib + ".kicad_sym"), "w", encoding="utf-8") as f:
            f.write("(kicad_symbol_lib (version 20220914) (generator kicad_symbol_editor)\n")
            for b in syms.values():
                f.write(b + "\n")
            f.write(")\n")
    return {lib: sorted(s) for lib, s in libs.items()}


if __name__ == "__main__":
    for lib, names in build(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT).items():
        print(f"{lib}: {', '.join(names)}")
