import sys, time
sys.path.insert(0, r"C:\Users\karpa\Documents\Shtuka-druka\tools\eda")
import eda_check as E
b = E.find_bridge()
name, uuid = sys.argv[1], sys.argv[2]
w = [x["windowId"] for x in E.http(b + "/eda-windows")["windows"] if x["connected"]][-1]
try: print("open:", E.run(b, w, f"return await eda.dmt_Project.openProject('{uuid}');", timeout=60))
except Exception as e: print("open err", e)
for i in range(30):
    time.sleep(6)
    try: st = E.states(b)
    except Exception: st = []
    m = [(ww, s) for ww, s in st if s["project"] == name]
    if m and m[0][1]["sch"] and m[0][1]["pcb"]:
        print("ready", m[0][1]); break
    if m and i in (3, 12):
        try:
            u = E.run(b, m[0][0], "const p = await eda.dmt_Project.getCurrentProjectInfo(); const bd = p.data.find(d => d.itemType === 'Board') || p.data[0]; return {s: bd.schematic.page[0].uuid, p: bd.pcb.uuid};", timeout=30)
            E.run(b, m[0][0], f"eda.dmt_EditorControl.openDocument('{u['s']}'); return 1;", timeout=30); time.sleep(8)
            E.run(b, m[0][0], f"eda.dmt_EditorControl.openDocument('{u['p']}'); return 1;", timeout=30)
        except Exception as e: print("tabs err", e)
else:
    print("not ready", [(ww[:8], s) for ww, s in st])
