import sys, time, os
sys.path.insert(0, r"C:\Users\karpa\Documents\Shtuka-druka\tools\eda")
import eda_check as E
b = E.find_bridge() or E.start_bridge()
name = sys.argv[1]
w, s = E.live_connection(b, name)
f = rf"C:\Users\karpa\Documents\EasyEDA-Pro\projects\{name}.eprj2"
m0 = os.path.getmtime(f)
GET = ("const p = await eda.dmt_Project.getCurrentProjectInfo(); const b = p.data.find(d => d.itemType === 'Board') || p.data[0];"
       "return {sch: b.schematic && b.schematic.page[0].uuid, pcb: b.pcb && b.pcb.uuid};")
u = E.run(b, w, GET, timeout=30)
res = {}
for kind, api in (("sch", "sch_Document"), ("pcb", "pcb_Document")):
    for t in range(4):
        E.run(b, w, f"eda.dmt_EditorControl.openDocument('{u[kind]}'); return 1;", timeout=30)
        time.sleep(6)
        try:
            r = E.run(b, w, f"return await eda.{api}.save();", timeout=60)
        except Exception as e:
            r = str(e)
        if r is True:
            break
    res[kind] = r
    time.sleep(3)
time.sleep(4)
print("save:", res, "mtime changed:", os.path.getmtime(f) > m0, time.ctime(os.path.getmtime(f)))
