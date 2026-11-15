#!/usr/bin/env python3
"""Write LCSC part numbers from hardware/for-routing/<ID>/BOM.csv into the Supplier Part fields
(supplier "LCSC", supplierId "C...") of an imported EasyEDA Pro project.

Why: the KiCad import keeps our "LCSC" symbol property only as a custom attribute, so EasyEDA's own
BOM, JLC ordering and the Netlist Explorer extension see no supplier part. This fills the standard field.

  eda_set_lcsc.py ID --project NAME [--dry-run]

Changes only supplier fields of schematic parts (and PCB parts where the API allows it); pins, nets
and positions are not touched. The project is NOT saved: check it, then press Ctrl+S in EasyEDA.
Run eda_check.py afterwards to confirm the nets are unchanged.
License: AGPL-3.0-or-later.
"""
import argparse
import csv
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import eda_check as E  # noqa: E402

JS = r"""
// One pass over one document type within a time budget: the bridge drops requests after 30 s,
// so Python calls this repeatedly until "done". The API answers only for the active document.
const want = __MAP__;
const dry = __DRY__;
const kind = "__KIND__";
const t0 = Date.now();
const api = kind === "sch" ? eda.sch_PrimitiveComponent : eda.pcb_PrimitiveComponent;
const out = {set: 0, same: 0, other: [], seen: [], done: false, error: null};
const p = await eda.dmt_Project.getCurrentProjectInfo();
const b = p && (p.data.find(x => x.itemType === "Board") || p.data[0]);
const uuid = kind === "sch" ? (b && b.schematic && b.schematic.page[0].uuid) : (b && b.pcb && b.pcb.uuid);
// The first call only switches tabs; Python waits (timers are throttled while EasyEDA is in the background).
if (__SWITCH__) { if (uuid) eda.dmt_EditorControl.openDocument(uuid); out.next = 0; return out; }
try {
  const ids = await api.getAllPrimitiveId();
  out.done = true; out.next = ids.length;
  for (let i = __START__; i < ids.length; i++) {
    if (Date.now() - t0 > 10000) { out.done = false; out.next = i; break; }
    const id = ids[i];
    const c = await api.get(id);
    // Right after a tab switch get() returns empty objects: report "loading" and let Python retry.
    if (c && !c.componentType && !c.designator) { out.done = false; out.next = i; out.loading = true; break; }
    if (!c || (kind === "sch" && c.componentType !== "part")) continue;
    const d = c.designator; if (!(d in want)) continue;
    out.seen.push(d);
    if (typeof c.getState_SupplierId !== "function") { out.error = "no supplier fields"; break; }
    const cur = c.getState_SupplierId();
    if (cur === want[d]) { out.same++; continue; }
    if (cur && cur !== want[d]) out.other.push([d, cur, want[d]]);
    if (!dry) await api.modify(id, {supplier: "LCSC", supplierId: want[d]});
    out.set++;
  }
} catch (e) { out.error = String(e); }
return out;
"""


def bom_map(path):
    m = {}
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        lc = (r.get("LCSC Part #") or "").strip()
        if not lc:
            continue
        for d in r["Designator"].split(","):
            m[d.strip()] = lc
    return m


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("id", help="board ID in hardware/for-routing/, e.g. F1")
    ap.add_argument("--project", required=True, help="EasyEDA project name, e.g. F1_v2")
    ap.add_argument("--dry-run", action="store_true", help="only report what would change")
    a = ap.parse_args()
    m = bom_map(ROOT / "hardware" / "for-routing" / a.id / "BOM.csv")
    if not m:
        sys.exit("BOM.csv has no LCSC numbers")
    bridge = E.find_bridge() or E.start_bridge()
    win, _ = E.live_connection(bridge, a.project)
    print(f"{len(m)} designators with LCSC numbers in BOM.csv" + (" (dry run)" if a.dry_run else ""))
    for kind in ("sch", "pcb"):
        tot = {"set": 0, "same": 0, "other": [], "seen": set()}
        start = 0
        for k in range(100):
            code = (JS.replace("__MAP__", json.dumps(m)).replace("__DRY__", "true" if a.dry_run else "false")
                    .replace("__KIND__", kind).replace("__SWITCH__", "true" if k == 0 else "false").replace("__START__", str(start)))
            r = E.run(bridge, win, code, timeout=60)
            tot["set"] += r["set"]; tot["same"] += r["same"]; tot["other"] += r["other"]; tot["seen"] |= set(r["seen"])
            start = r.get("next", 0)
            if k == 0 or r.get("loading"):
                time.sleep(5)
            if r["error"] or r["done"]:
                break
        same = tot["same"]
        print(f"{kind}: written {tot['set']}, already right {same}, other number before {tot['other']}, "
              f"missing {len(set(m) - tot['seen'])}, error {r['error']}")
    if not a.dry_run:
        print("Not saved: check, then Ctrl+S in EasyEDA; run eda_check.py to confirm nets.")


if __name__ == "__main__":
    main()
