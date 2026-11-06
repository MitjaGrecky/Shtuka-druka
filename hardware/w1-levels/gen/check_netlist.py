#!/usr/bin/env python3
"""Compare the schematic netlist (kicad-cli sch export netlist) with design.py, pin by pin.
Run: python3 check_netlist.py      License: AGPL-3.0-or-later.
"""
import os
import re
import subprocess
import tempfile

import design as D

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    sch = os.path.join(HERE, "..", D.NAME + ".kicad_sch")
    net = os.path.join(tempfile.mkdtemp(), "w.net")
    subprocess.run(["kicad-cli", "sch", "export", "netlist", "--format", "kicadsexpr", "-o", net, sch], check=True,
                   capture_output=True)
    txt = open(net).read()
    got = {}
    heads = list(re.finditer(r'\(net \(code "?\d+"?\) \(name "([^"]*)"', txt))
    for i, m in enumerate(heads):
        seg = txt[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(txt)]
        for r, p in re.findall(r'\(node \(ref "([^"]+)"\) \(pin "([^"]+)"', seg):
            got[(r, p)] = m.group(1).lstrip("/")
    n = bad = 0
    for part in D.parts():
        for pin, want in part["pins"].items():
            if want is None:
                continue
            n += 1
            have = got.get((part["ref"], pin))
            if have != want:
                bad += 1
                print("MISMATCH", part["ref"], pin, "want", want, "have", have)
    print(n, "pins checked,", bad, "mismatches")
    return bad


if __name__ == "__main__":
    raise SystemExit(1 if main() else 0)
