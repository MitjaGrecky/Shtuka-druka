#!/usr/bin/env python3
"""Import a KiCad project zip into EasyEDA Pro as a new local project through the API bridge (no GUI clicks).

Usage: eda_import.py ZIP NAME [--team TEAM_UUID]
NAME is the new project's name (e.g. W2_v1). TEAM defaults to the first local team (the projects folder).
Uses SYS_FileManager.importProjectByProjectFile (beta API). Then open the project in EasyEDA and run eda_check.py.
License: AGPL-3.0-or-later.
"""
import argparse
import base64
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import eda_check as E  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("zip")
    ap.add_argument("name")
    ap.add_argument("--team")
    a = ap.parse_args()
    bridge = E.find_bridge() or E.start_bridge()
    st = E.states(bridge)
    wins = [w["windowId"] for w in E.http(f"{bridge}/eda-windows")["windows"] if w["connected"]]
    win = st[0][0] if st else wins[-1]
    team = a.team or E.run(bridge, win, "return (await eda.dmt_Team.getAllTeamsInfo())[0].uuid;")
    code = ((HERE / "js" / "import_kicad.js").read_text(encoding="utf-8")
            .replace("__B64__", base64.b64encode(Path(a.zip).read_bytes()).decode())
            .replace("__NAME__", a.name).replace("__TEAM__", team.replace("\\", "\\\\")))
    try:
        print(E.run(bridge, win, code, timeout=120))
    except Exception as e:  # noqa: BLE001 - the bridge gives up after 30 s; the import may still finish
        print("bridge:", e, "- the import may still be running; check the project list in EasyEDA")


if __name__ == "__main__":
    main()
