// Import a KiCad project zip as a NEW local EasyEDA Pro project (no GUI). __B64__, __NAME__, __TEAM__ are filled by
// tools/eda/eda_import.py. Creates a project; changes nothing else.
const b64 = '__B64__';
const bin = atob(b64);
const bytes = new Uint8Array(bin.length);
for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
const file = new File([bytes], '__NAME__.zip', { type: 'application/zip' });
const tries = [
  { operation: 'New Project', newProjectOwnerTeamUuid: '__TEAM__', newProjectName: '__NAME__', newProjectFriendlyName: '__NAME__' },
  { operation: 'Offline Client Local Path', folderPath: '__TEAM__\\__NAME__' },
];
const log = [];
for (const saveTo of tries) {
  try {
    const r = await eda.sys_FileManager.importProjectByProjectFile(file, 'KiCad', {}, saveTo);
    log.push({ op: saveTo.operation, r: r ? JSON.parse(JSON.stringify(r)) : null });
    if (r) break;
  } catch (e) { log.push({ op: saveTo.operation, err: String(e) }); }
}
return log;
