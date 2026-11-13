#!/usr/bin/env python3
"""Run JavaScript (EasyEDA Pro Extension API) in the EasyEDA window that sees a given project, through the
easyeda-api-skill bridge - the same connection logic as eda_check.py (it also opens the project's schematic and PCB).

  python tools/eda/eda_exec.py --project M3_v4 tools/eda/js/pcb_state.js
  python tools/eda/eda_exec.py --project M3_v4 -c "return eda.pcb_PrimitiveLine.getAllPrimitiveId().then(a => a.length)"

The code is the body of an async function: use `await` and `return` a JSON-serialisable value. Prints the result as JSON.
License: AGPL-3.0-or-later.
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import eda_check as E  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", required=True, help="EasyEDA project name, e.g. M3_v4")
    ap.add_argument("-c", "--code", help="JS code (instead of a file)")
    ap.add_argument("file", nargs="?", help="JS file")
    ap.add_argument("--timeout", type=int, default=120)
    a = ap.parse_args()
    code = a.code if a.code else Path(a.file).read_text(encoding="utf-8")
    bridge = E.find_bridge() or E.start_bridge()
    win, _ = E.live_connection(bridge, a.project)
    print(json.dumps(E.run(bridge, win, code, timeout=a.timeout), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
