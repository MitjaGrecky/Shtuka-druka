#!/usr/bin/env python3
"""Build the hand-routing packages: generate each board (unrouted) in a scratch copy of hardware/, strip the
auto-added GND stitching vias, pack into hardware/for-routing/<ID>/ (tools/pack_for_routing.py).

  python3 tools/build_for_routing.py            # all boards
  python3 tools/build_for_routing.py M1 W1      # some

The repository projects are never touched (W1 in the repository is routed; here it is rebuilt without routing).
Needs kicad-cli + pcbnew (KiCad 7 or newer) and playwright. License: AGPL-3.0-or-later.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
HW = os.path.join(REPO, "hardware")

# id -> (project dir under hardware/, env, generator scripts in gen/)
BOARDS = {
    "M1": ("m1-screen-knobs", {"M1_LP": "1"}, ["make_sch.py", "make_pcb.py"]),
    "W1": ("w1-levels", {}, ["make_sch.py", "make_pcb.py"]),
}
BOARDS.update(__import__("importlib").import_module("boards_extra").BOARDS) if os.path.exists(os.path.join(HERE, "boards_extra.py")) else None


def strip_vias(pcb_file):
    code = ("import pcbnew,sys\nb=pcbnew.LoadBoard(sys.argv[1])\n"
            "r=[t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and not t.IsLocked() and t.GetNetname()=='GND']\n"
            "[b.Remove(t) for t in r]\nb.Save(sys.argv[1])\nprint('stitching vias removed',len(r))\n")
    subprocess.run([sys.executable, "-c", code, pcb_file], check=True, stderr=subprocess.DEVNULL)


def main():
    ids = [a for a in sys.argv[1:] if not a.startswith("--")] or list(BOARDS)
    work = tempfile.mkdtemp(prefix="forrouting_")
    for ident in ids:
        proj, env, scripts = BOARDS[ident]
        # copy every project: the generators reach into their siblings (W1 uses the M1 library and writers)
        for name in os.listdir(HW):
            src = os.path.join(HW, name)
            if os.path.isdir(src) and not os.path.exists(os.path.join(work, name)):
                shutil.copytree(src, os.path.join(work, name), ignore=shutil.ignore_patterns("quilter", "experiments", "almost", "mech", "__pycache__"))
        pdir = os.path.join(work, proj)
        e = dict(os.environ, **env)
        for s in scripts:
            subprocess.run([sys.executable, s], cwd=os.path.join(pdir, "gen"), env=e, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pcb = [f for f in os.listdir(pdir) if f.endswith(".kicad_pcb")][0]
        strip_vias(os.path.join(pdir, pcb))
        subprocess.run([sys.executable, os.path.join(HERE, "pack_for_routing.py"), ident, pdir], check=True, env=e)
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
