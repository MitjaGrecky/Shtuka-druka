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
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import eda_check as E  # noqa: E402

JS = r"""
const want = __MAP__;
const dry = __DRY__;
const out = {sch: {set: 0, same: 0, other: []}, pcb: {set: 0, same: 0, other: [], error: null}, missing: []};
const seen = new Set();
// The API answers only for the active document: switch tabs before the schematic and the PCB pass.
const p = await eda.dmt_Project.getCurrentProjectInfo();
const b = p && (p.data.find(x => x.itemType === "Board") || p.data[0]);
const sleep = ms => new Promise(r => setTimeout(r, ms));
const page = b && b.schematic && b.schematic.page[0];
if (page) { eda.dmt_EditorControl.openDocument(page.uuid); await sleep(3000); }
const ids = await eda.sch_PrimitiveComponent.getAllPrimitiveId();
for (const id of ids) {
  const c = await eda.sch_PrimitiveComponent.get(id);
  if (!c || c.componentType !== "part") continue;
  const d = c.designator; if (!(d in want)) continue;
  seen.add(d);
  const cur = c.getState_SupplierId();
  if (cur === want[d]) { out.sch.same++; continue; }
  if (cur && cur !== want[d]) out.sch.other.push([d, cur, want[d]]);
  if (!dry) await eda.sch_PrimitiveComponent.modify(id, {supplier: "LCSC", supplierId: want[d]});
  out.sch.set++;
}
for (const d in want) if (!seen.has(d)) out.missing.push(d);
try {
  if (b && b.pcb) { eda.dmt_EditorControl.openDocument(b.pcb.uuid); await sleep(3000); }
  const pids = await eda.pcb_PrimitiveComponent.getAllPrimitiveId();
  for (const id of pids) {
    const c = await eda.pcb_PrimitiveComponent.get(id);
    if (!c || !(c.designator in want)) continue;
    if (typeof c.getState_SupplierId !== "function") { out.pcb.error = "no supplier fields on PCB parts"; break; }
    const cur = c.getState_SupplierId();
    if (cur === want[c.designator]) { out.pcb.same++; continue; }
    if (cur && cur !== want[c.designator]) out.pcb.other.push([c.designator, cur, want[c.designator]]);
    if (!dry) await eda.pcb_PrimitiveComponent.modify(id, {supplier: "LCSC", supplierId: want[c.designator]});
    out.pcb.set++;
  }
} catch (e) { out.pcb.error = String(e); }
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
    code = JS.replace("__MAP__", json.dumps(m)).replace("__DRY__", "true" if a.dry_run else "false")
    r = E.run(bridge, win, code, timeout=300)
    print(f"{len(m)} designators with LCSC numbers in BOM.csv" + (" (dry run)" if a.dry_run else ""))
    print(json.dumps(r, ensure_ascii=False, indent=1))
    if not a.dry_run:
        print("Not saved: check, then Ctrl+S in EasyEDA; run eda_check.py to confirm nets.")


if __name__ == "__main__":
    main()
