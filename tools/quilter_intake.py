#!/usr/bin/env python3
"""Take Quilter result zips from Downloads into hardware/<board>/quilter/results/ and check them.

Usage:
  quilter_intake.py JOB --match TEXT [--board m1-screen-knobs] [--downloads DIR] [--sch-from DIR] [--no-check]

JOB      short job name used for folders, e.g. K_rev04 -> results/K_rev04_cand1_1/
--match  text that every wanted zip name contains, e.g. "rev_0.4" (Quilter names zips
         Quilter_<project>_<job title>_Candidate_<a>_<b>.zip)
Steps: (1) find the zips, (2) take only *.kicad_pcb and *.kicad_pro from each (nothing else is
extracted), (3) skip candidates whose board is byte-identical to an earlier one (md5) and say so,
(4) run tools/pc_check.py on the unique boards (DRC, unconnected, parity with --sch-from).
Existing result folders are never overwritten.
License: AGPL-3.0-or-later.
"""
import argparse
import hashlib
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("job")
    ap.add_argument("--match", required=True)
    ap.add_argument("--board", default="m1-screen-knobs")
    ap.add_argument("--downloads", default=str(Path.home() / "Downloads"))
    ap.add_argument("--sch-from", help="project folder with the schematic for the parity check")
    ap.add_argument("--no-check", action="store_true")
    a = ap.parse_args()

    zips = sorted(z for z in Path(a.downloads).glob("Quilter_*Candidate_*.zip") if a.match in z.name)
    if not zips:
        sys.exit(f"no Quilter_*Candidate_*.zip containing {a.match!r} in {a.downloads}")
    dest_root = ROOT / "hardware" / a.board / "quilter" / "results"
    seen, unique = {}, []
    for z in zips:
        m = re.search(r"Candidate_(\d+)_(\d+)", z.name)
        cand = f"cand{m.group(1)}_{m.group(2)}"
        dest = dest_root / f"{a.job}_{cand}"
        with zipfile.ZipFile(z) as zf:
            members = [n for n in zf.namelist()
                       if Path(n).name == n and n.endswith((".kicad_pcb", ".kicad_pro"))]  # flat names only
            pcb = next((n for n in members if n.endswith(".kicad_pcb")), None)
            if not pcb:
                print(f"{z.name}: no .kicad_pcb inside, skipped", flush=True)
                continue
            md5 = hashlib.md5(zf.read(pcb)).hexdigest()
            if md5 in seen:
                print(f"{cand}: same board as {seen[md5]} (md5 {md5[:8]}), not copied", flush=True)
                continue
            seen[md5] = cand
            if dest.exists():
                print(f"{cand}: {dest.relative_to(ROOT)} already exists, left as is", flush=True)
            else:
                dest.mkdir(parents=True)
                for n in members:
                    (dest / n).write_bytes(zf.read(n))
                print(f"{cand}: -> {dest.relative_to(ROOT)} ({', '.join(members)})", flush=True)
            unique.append(dest / pcb)
    if unique and not a.no_check:
        cmd = [sys.executable, str(ROOT / "tools" / "pc_check.py"), *map(str, unique)]
        if a.sch_from:
            cmd += ["--sch-from", a.sch_from]
        subprocess.run(cmd)


if __name__ == "__main__":
    main()
