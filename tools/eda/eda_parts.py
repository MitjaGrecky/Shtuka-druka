#!/usr/bin/env python3
"""Look parts up in EasyEDA Pro's system library (the LCSC/JLCPCB part base) through the API bridge. Read-only.

Usage: eda_parts.py KEY [KEY ...] [-n 5] [--json OUT]
KEY is a manufacturer part number or a search phrase (e.g. "TCA9546APWR", "4.7uF 0805 25V", "C318884").
Prints, per key, the first hits: name, manufacturer part, LCSC number, footprint, stock/price where the library gives them.
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
    ap.add_argument("keys", nargs="+")
    ap.add_argument("-n", type=int, default=5)
    ap.add_argument("--json")
    ap.add_argument("--basic", action="store_true", help="list JLCPCB basic parts first")
    a = ap.parse_args()
    bridge = E.find_bridge() or E.start_bridge()
    st = E.states(bridge)
    win = st[0][0] if st else [w["windowId"] for w in E.http(f"{bridge}/eda-windows")["windows"]][-1]
    code = (HERE / "js" / "lib_search.js").read_text(encoding="utf-8").replace("__KEYS__", json.dumps(a.keys)).replace("__N__", str(a.n))
    res = E.run(bridge, win, code, timeout=120)
    if a.json:
        Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, hits in res["results"].items():
        print(f"== {k}")
        if isinstance(hits, str):
            print("  ", hits)
            continue
        if a.basic:                                  # JLCPCB basic parts first (no extended-part fee at assembly)
            hits = sorted(hits, key=lambda h: (h.get("otherProperty") or {}).get("JLCPCB Part Class") != "Basic Part")
        for h in hits:
            op = h.get("otherProperty") or {}
            short = {k: v for k, v in h.items() if k not in ("description", "uuid", "property", "otherProperty", "symbolName")}
            short["class"] = op.get("JLCPCB Part Class", "?")
            short["pkg"] = op.get("Supplier Footprint", "")
            print("  ", json.dumps(short, ensure_ascii=False)[:300])
            d = h.get("description", "")
            if d:
                print("      ", d[:160])


if __name__ == "__main__":
    main()
