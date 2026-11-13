// Read-only. Every PCB component: designator -> [x, y, rotation, layer, value/name] (activates the PCB tab first).
const tree = await eda.dmt_EditorControl.getSplitScreenTree();
const pcbTab = tree.tabs.find(x => x.data && x.data.doctype === 3);
if (pcbTab) { await eda.dmt_EditorControl.activateDocument(pcbTab.tabId); await new Promise(r => setTimeout(r, 1500)); }
const g = (o, k) => { const f = 'getState_' + k[0].toUpperCase() + k.slice(1); return typeof o[f] === 'function' ? o[f]() : o[k]; };
const out = {};
for (const id of await eda.pcb_PrimitiveComponent.getAllPrimitiveId()) {
  const c = await eda.pcb_PrimitiveComponent.get(id);
  const op = g(c, 'otherProperty') || {};
  out[g(c, 'designator')] = [g(c, 'x'), g(c, 'y'), g(c, 'rotation'), g(c, 'layer'), op.Value || op.value || g(c, 'name') || ''];
}
return out;
