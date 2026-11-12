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


def build(out=DEFAULT_OUT):
    libs = {}
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
