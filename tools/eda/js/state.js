// Read-only. What this extension connection sees: project and which of its documents are open as tabs.
const p = await eda.dmt_Project.getCurrentProjectInfo();
if (!p) return null;
const b = p.data.find(d => d.itemType === 'Board') || p.data[0];
const t = await eda.dmt_EditorControl.getSplitScreenTree();
const mine = t.tabs.filter(x => x.tabId.endsWith('@' + p.uuid)).map(x => x.data && x.data.doctype);
return { project: p.friendlyName, projectUuid: p.uuid, board: b.name, sch: mine.includes(1), pcb: mine.includes(3) };
