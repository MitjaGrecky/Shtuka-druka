#!/usr/bin/env python3
"""PC-side packer: like tools/pack_for_routing.py, but works with KiCad 9/10 and without playwright.

  python tools/pack_easyeda.py ID PROJECT_DIR [--out hardware/for-routing] [--no-cli]

--no-cli: do not call kicad-cli (it crashes the PC): zip, BOM and board.json are rebuilt, netlist.net, schematic.pdf
and outline.dxf stay from the last full build - use it only when the connections and the outline did not change.
On a new board (no netlist.net yet) the reference netlist is written from design.py; schematic.pdf and outline.dxf
are then missing until a machine with a working kicad-cli (or CI) makes them.

Differences from pack_for_routing.py (whose code it reuses unchanged):
- the board copy that goes into ID_kicad7.zip gets KiCad 7 style numbered nets
  (hardware/common/gen/pcb_netnums.py): EasyEDA Pro drops the nets of a KiCad 9/10 board otherwise;
- PNG previews are skipped when playwright is not installed;
- kicad-cli is found in the usual KiCad 10 places when it is not on PATH.
The zip name stays <ID>_kicad7.zip (what the other tools expect); the board inside is the newer format
with KiCad 7 net numbering, which EasyEDA Pro 3.2 imports with all nets (checked on M3, 12.11.2026).
License: AGPL-3.0-or-later.
"""
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "hardware", "common", "gen"))
import pcb_netnums  # noqa: E402

for d in (r"C:\Program Files\KiCad\10.0\bin", "/Applications/KiCad/KiCad.app/Contents/MacOS"):
    if os.path.isdir(d) and not shutil.which("kicad-cli"):
        os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]

import pack_for_routing as PK  # noqa: E402


def design_netlist(d, path):
    """netlist.net in KiCad's export format, built from design.py (pins -> nets) - the reference for
    tools/eda/eda_check.py when kicad-cli cannot run. Local nets get the root-sheet "/" prefix, as KiCad names them."""
    power = {"+5V", "+3V3", "GND"}
    nets = {}
    for p in d.parts():
        for pin, n in p["pins"].items():
            if n:
                nets.setdefault(n if n in power else "/" + n, []).append((p["ref"], pin))
    q = lambda s: '"' + s.replace('"', '\\"') + '"'  # noqa: E731
    out = ['(export (version "E")', '  (design (source "design.py") (tool "tools/pack_easyeda.py design_netlist"))', '  (components']
    out += [f'    (comp (ref {q(p["ref"])}) (value {q(p["value"])}) (footprint {q(p["fp"])}))' for p in d.parts()]
    out += ['  )', '  (nets']
    for code, (n, nodes) in enumerate(sorted(nets.items()), 1):
        out.append(f'    (net (code "{code}") (name {q(n)})')
        out += [f'      (node (ref {q(r)}) (pin {q(pin)}))' for r, pin in nodes]
        out.append('    )')
    out += ['  )', ')']
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


def main():
    ident, proj = sys.argv[1], os.path.abspath(sys.argv[2])
    try:
        import playwright  # noqa: F401
    except ImportError:
        PK.render = lambda *a, **k: print("previews skipped (no playwright)")
    if "--no-cli" in sys.argv:          # the PC blue-screens on kicad-cli: keep netlist/pdf/dxf of the last build
        sys.argv.remove("--no-cli")
        real = PK.subprocess.run

        def run(cmd, *a, **k):
            if cmd and os.path.basename(str(cmd[0])).startswith("kicad-cli"):
                print("skipped (--no-cli):", " ".join(map(str, cmd[1:4])))
                return PK.subprocess.CompletedProcess(cmd, 0, "", "")
            return real(cmd, *a, **k)
        PK.subprocess.run = run
    # work on a copy: the netnums board goes into the zip, the project stays as generated
    work = tempfile.mkdtemp(prefix="pack_easyeda_")
    copy = os.path.join(work, os.path.basename(proj))
    shutil.copytree(proj, copy, ignore=shutil.ignore_patterns("__pycache__", "backups"))
    for f in os.listdir(copy):
        if f.endswith(".kicad_pcb"):
            p = os.path.join(copy, f)
            txt = open(p, encoding="utf-8").read()
            open(p, "w", encoding="utf-8").write(pcb_netnums.convert(txt))
    lib = os.path.join(proj, "..", "m1-screen-knobs", "lib")       # the packer looks for the shared library beside the project
    if not os.path.isdir(os.path.join(copy, "lib")) and os.path.isdir(lib):
        shutil.copytree(lib, os.path.join(work, "m1-screen-knobs", "lib"))
    root = os.path.abspath(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else os.path.join(REPO, "hardware", "for-routing")
    dxf = os.path.join(root, ident, "outline.dxf")
    if os.path.isdir(dxf):
        shutil.rmtree(dxf)
    sys.argv = [sys.argv[0], ident, copy] + sys.argv[3:]
    try:
        PK.main()
    finally:
        shutil.rmtree(work, ignore_errors=True)
    netf = os.path.join(root, ident, "netlist.net")
    if not os.path.exists(netf):                 # --no-cli on a new board: reference netlist from design.py
        design_netlist(PK.load_design(proj), netf)
        print("netlist.net written from design.py")
    if os.path.isdir(dxf):                       # KiCad 9+ writes a folder with <name>-Edge_Cuts.dxf
        inner = [f for f in os.listdir(dxf) if f.endswith(".dxf")]
        tmp = dxf + ".tmp"
        shutil.move(os.path.join(dxf, inner[0]), tmp)
        shutil.rmtree(dxf)
        shutil.move(tmp, dxf)


if __name__ == "__main__":
    main()
