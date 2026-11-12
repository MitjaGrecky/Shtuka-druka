#!/usr/bin/env python3
"""PC-side packer: like tools/pack_for_routing.py, but works with KiCad 9/10 and without playwright.

  python tools/pack_easyeda.py ID PROJECT_DIR [--out hardware/for-routing]

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


def main():
    ident, proj = sys.argv[1], os.path.abspath(sys.argv[2])
    try:
        import playwright  # noqa: F401
    except ImportError:
        PK.render = lambda *a, **k: print("previews skipped (no playwright)")
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
    if os.path.isdir(dxf):                       # KiCad 9+ writes a folder with <name>-Edge_Cuts.dxf
        inner = [f for f in os.listdir(dxf) if f.endswith(".dxf")]
        tmp = dxf + ".tmp"
        shutil.move(os.path.join(dxf, inner[0]), tmp)
        shutil.rmtree(dxf)
        shutil.move(tmp, dxf)


if __name__ == "__main__":
    main()
