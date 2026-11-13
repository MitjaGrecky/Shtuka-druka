// Read-only. Run the PCB DRC of the open board (strict, no UI) and summarise: count per error type / object pair,
// the nets with unconnected pads, and up to 12 examples of the other errors. Also the track and via counts.
const tree = await eda.dmt_EditorControl.getSplitScreenTree();      // the PCB API answers only on an active PCB tab
const pcbTab = tree.tabs.find(x => x.data && x.data.doctype === 3);
if (pcbTab) { await eda.dmt_EditorControl.activateDocument(pcbTab.tabId); await new Promise(r => setTimeout(r, 1500)); }
const errs = await eda.pcb_Drc.check(true, false, true);
if (!Array.isArray(errs)) return { result: errs };
const flat = [];
const walk = (e) => {
  if (Array.isArray(e)) { e.forEach(walk); return; }
  if (e && typeof e === 'object') {
    if (e.errorType) flat.push(e);
    for (const k of ['list', 'children', 'errors', 'data']) if (e[k]) walk(e[k]);
  }
};
walk(errs);
const byType = {}, openNets = {}, other = [];
for (const e of flat) {
  const k = e.errorType + ' | ' + (e.errorObjType || '');
  byType[k] = (byType[k] || 0) + 1;
  if (e.errorType === 'Connection Error') openNets[e.net] = (openNets[e.net] || 0) + 1;
  else if (other.length < 12) other.push(`${e.errorType} | ${e.errorObjType} | ${e.obj1 && e.obj1.suffix} <-> ${e.obj2 && e.obj2.suffix} | ${e.layer || ''}`);
}
const tracks = (await eda.pcb_PrimitiveLine.getAllPrimitiveId()).length;
const vias = (await eda.pcb_PrimitiveVia.getAllPrimitiveId()).length;
return { total: flat.length, tracks, vias, byType, openNets, other };
