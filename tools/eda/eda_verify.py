#!/usr/bin/env python3
"""After importing a board package into EasyEDA Pro (and Import Changes from Schematic): nets against netlist.net
(eda_check), every part's LCSC number and value on the PCB against design.py, and EasyEDA's own DRC by type.

  python tools/eda/eda_verify.py M3 --project M3_v5

Expected for an unrouted board: nets matched, 0 property mismatches, DRC = unrouted connections
("Connection Error") and the in-footprint pad clearance of the 4 x 0402 resistor arrays only.
License: AGPL-3.0-or-later.
"""
import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
import eda_check as E  # noqa: E402


def board_dir(ident):
    import boards_extra
    if ident in boards_extra.BOARDS:
        return ROOT / "hardware" / boards_extra.BOARDS[ident][0]
    return {"M1": ROOT / "hardware" / "m1-screen-knobs", "W1": ROOT / "hardware" / "w1-levels"}[ident]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("id")
    ap.add_argument("--project", required=True)
    a = ap.parse_args()
    py = sys.executable
    out = subprocess.run([py, str(HERE / "eda_check.py"), a.id, "--project", a.project], capture_output=True, text=True)
    print("\n".join(l for l in out.stdout.splitlines() if l.startswith(("**", "- MERGE", "- net", "- missing", "- extra"))))
    spec = importlib.util.spec_from_file_location("d", board_dir(a.id) / "gen" / "design.py")
    d = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(d)
    bridge = E.find_bridge() or E.start_bridge()
    win, _ = E.live_connection(bridge, a.project)
    have = E.run(bridge, win, (HERE / "js" / "pcb_props.js").read_text(encoding="utf-8"), timeout=300)
    bad = {}
    for p in d.parts():
        r = p["ref"]
        if r not in have or r.startswith("H"):
            continue
        lcsc, val = have[r]
        want = p["fields"].get("LCSC", "")
        if (want and lcsc != want) or (val and val != p["value"]):
            bad[r] = {"pcb": [lcsc, val], "design": [want, p["value"]]}
    print(f"**Properties:** {len(bad)} mismatches (LCSC / value on the PCB vs design.py)", json.dumps(dict(list(bad.items())[:8]), ensure_ascii=False))
    drc = E.run(bridge, win, (HERE / "js" / "pcb_drc.js").read_text(encoding="utf-8"), timeout=300)
    print("**EasyEDA DRC:**", json.dumps(drc.get("byType", drc), ensure_ascii=False))


if __name__ == "__main__":
    main()
