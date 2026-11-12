#!/usr/bin/env python3
"""Compare a board's schematic netlist (kicad-cli sch export netlist) with its design.py, pin by pin.

Usage (from the board's gen/ folder): python check_netlist.py      or: python check_netlist.py GEN_DIR
Shared by the boards built with hardware/common/gen/kit.py.  License: AGPL-3.0-or-later.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile


def kicad_cli():
    for c in (os.environ.get("KICAD_CLI"), shutil.which("kicad-cli"), r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe",
              "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"):
        if c and os.path.exists(c):
            return c
    sys.exit("kicad-cli not found: set KICAD_CLI")


def check(gen_dir):
    sys.path.insert(0, gen_dir)
    sys.modules.pop("design", None)
    import design as D
    sch = os.path.join(gen_dir, "..", D.NAME + ".kicad_sch")
    net = os.path.join(tempfile.mkdtemp(), "n.net")
    subprocess.run([kicad_cli(), "sch", "export", "netlist", "--format", "kicadsexpr", "-o", net, sch],
                   check=True, capture_output=True)
    txt = open(net, encoding="utf-8").read()
    got = {}
    # KiCad 7 writes one line per node, KiCad 10 one token per line: match both
    heads = list(re.finditer(r'\(net\s+\(code\s+"?\d+"?\)\s+\(name\s+"([^"]*)"', txt))
    for i, m in enumerate(heads):
        seg = txt[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(txt)]
        for r, p in re.findall(r'\(node\s+\(ref\s+"([^"]+)"\)\s+\(pin\s+"([^"]+)"', seg):
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
    here = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
    raise SystemExit(1 if check(here) else 0)
