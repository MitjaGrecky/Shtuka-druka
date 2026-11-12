// Read-only. Activate the project's PCB tab and return pad -> net for every component.
// __PROJECT_UUID__ is replaced by eda_check.py.
const g = (o, k) => { const f = 'getState_' + k[0].toUpperCase() + k.slice(1); return typeof o[f] === 'function' ? o[f]() : o[k]; };
const t = await eda.dmt_EditorControl.getSplitScreenTree();
const tab = t.tabs.find(x => x.data && x.data.doctype === 3 && x.tabId.endsWith('@__PROJECT_UUID__'));
if (!tab) return { error: 'PCB tab of this project is not open' };
await eda.dmt_EditorControl.activateDocument(tab.tabId);
await new Promise(r => setTimeout(r, 1500));
const ids = await eda.pcb_PrimitiveComponent.getAllPrimitiveId();
const comps = {};
for (const id of ids) {
  const c = await eda.pcb_PrimitiveComponent.get(id);
  const des = g(c, 'designator') || ('?' + id);
  const pads = (await eda.pcb_PrimitiveComponent.getAllPinsByPrimitiveId(id)) || [];
  comps[des] = pads.map(q => [String(g(q, 'padNumber')), g(q, 'net') || '']);
}
return { doc: tab.title, parts: ids.length, comps };
