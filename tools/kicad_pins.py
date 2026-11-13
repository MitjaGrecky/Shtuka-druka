#!/usr/bin/env python3
"""Print the pins (number, name, electrical type) of KiCad 10 library symbols, following "extends".

  python tools/kicad_pins.py MCU_RaspberryPi:RP2350A Analog_DAC:DAC80504 ...

Read-only helper for writing design.py files. License: AGPL-3.0-or-later.
"""
import os
import re
import sys

LIB = os.environ.get("KICAD10_SYMBOL_DIR", r"C:\Program Files\KiCad\10.0\share\kicad\symbols")


def block(text, name):
    i = text.find(f'\n\t(symbol "{name}"')
    if i < 0:
        return None
    depth, j = 0, i + 1
    while True:
        c = text[j]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return text[i + 1:j + 1]
        j += 1


def pins(lib, name):
    text = open(os.path.join(LIB, lib + ".kicad_sym"), encoding="utf-8").read()
    b = block(text, name)
    if b is None:
        return None
    m = re.search(r'\(extends "([^"]+)"\)', b)
    if m:
        return pins(lib, m.group(1))
    out = []
    for pm in re.finditer(r'\(pin (\w+) \w+.*?\(name "([^"]*)".*?\(number "([^"]*)"', b, re.S):
        out.append((pm.group(3), pm.group(2), pm.group(1)))
    return out


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        lib, name = arg.split(":")
        p = pins(lib, name)
        if p is None:
            print(f"== {arg}: NOT FOUND")
            continue
        key = lambda t: (int(t[0]) if t[0].isdigit() else 999, t[0])  # noqa: E731
        print(f"== {arg} ({len(p)} pins): " + "; ".join(f"{n}={nm}/{t[:3]}" for n, nm, t in sorted(set(p), key=key)))
