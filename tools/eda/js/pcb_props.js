// Read-only. PCB component properties after import: designator -> [LCSC, Value] (activates the PCB tab first).
const tree = await eda.dmt_EditorControl.getSplitScreenTree();
const pcbTab = tree.tabs.find(x => x.data && x.data.doctype === 3);
if (pcbTab) { await eda.dmt_EditorControl.activateDocument(pcbTab.tabId); await new Promise(r => setTimeout(r, 1500)); }
const out = {};
for (const id of await eda.pcb_PrimitiveComponent.getAllPrimitiveId()) {
  const c = await eda.pcb_PrimitiveComponent.get(id);
  const op = c.otherProperty || (c.getState_OtherProperty && c.getState_OtherProperty()) || {};
  out[c.designator || c.getState_Designator()] = [op.LCSC || '', op.Value || ''];
}
return out;
