// Read-only. Open the first board's schematic page and PCB of the current project (returns at once;
// a large board keeps loading in the background).
const p = await eda.dmt_Project.getCurrentProjectInfo();
if (!p) return { error: 'no project open' };
const b = p.data.find(d => d.itemType === 'Board') || p.data[0];
const page = b.schematic && b.schematic.page[0];
if (page) eda.dmt_EditorControl.openDocument(page.uuid);
await new Promise(r => setTimeout(r, 3000));
if (b.pcb) eda.dmt_EditorControl.openDocument(b.pcb.uuid);
return { project: p.friendlyName };
