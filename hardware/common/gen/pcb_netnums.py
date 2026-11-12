#!/usr/bin/env python3
"""Give a KiCad 9/10 board file the numbered net table of the KiCad 7 format, for EasyEDA Pro's importer.

KiCad 9+ writes nets by name only: pads carry (net "GND") and the file has no net table. EasyEDA Pro
(3.2) imports such a board with all footprints but no nets on the pads (seen 12.11.2026, M3). This
rewrites every (net "name") as (net N "name") and adds (net 0 "") (net 1 "...") ... before the first
footprint, as KiCad 7 does. Use it only on the copy that goes to EasyEDA.

Usage: python pcb_netnums.py IN.kicad_pcb OUT.kicad_pcb      License: AGPL-3.0-or-later.
"""
import re
import sys


def convert(text):
    if re.search(r'\(net\s+\d+\s+"', text):
        return text                                     # already numbered (KiCad 7/8)
    names = []
    for m in re.finditer(r'\(net\s+"((?:[^"\\]|\\.)*)"\)', text):
        if m.group(1) not in names:
            names.append(m.group(1))
    num = {n: i + 1 for i, n in enumerate(n for n in names if n)}
    num[""] = 0
    text = re.sub(r'\(net\s+"((?:[^"\\]|\\.)*)"\)', lambda m: f'(net {num[m.group(1)]} "{m.group(1)}")', text)
    table = '\t(net 0 "")\n' + "".join(f'\t(net {i} "{n}")\n' for n, i in sorted(num.items(), key=lambda x: x[1]) if i)
    i = text.find("\n\t(footprint")
    return text[:i + 1] + table + text[i + 1:]


if __name__ == "__main__":
    src = open(sys.argv[1], encoding="utf-8").read()
    open(sys.argv[2], "w", encoding="utf-8").write(convert(src))
    print("nets:", len(re.findall(r'^\t\(net \d+ "', convert(src), re.M)))
