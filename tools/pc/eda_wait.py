import sys, time
sys.path.insert(0, r"C:\Users\karpa\Documents\Shtuka-druka\tools\eda")
import eda_check as E
b = E.find_bridge() or E.start_bridge()
name, uuid = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else None)
def seen():
    try: return E.states(b)
    except Exception as e: return []
st = seen()
if uuid and not any(s["project"] == name for _, s in st):
    w = st[0][0]
    try: print("open:", E.run(b, w, f"return await eda.dmt_Project.openProject('{uuid}');", timeout=40))
    except Exception as e: print("open err", e)
for i in range(30):
    time.sleep(6)
    st = seen()
    m = [(w, s) for w, s in st if s["project"] == name]
    if m and m[0][1]["sch"] and m[0][1]["pcb"]:
        print("ready", m[0][0][:8], m[0][1]); break
    if m and i == 5:
        try: E.run(b, m[0][0], (E.HERE / "js" / "open_docs.js").read_text(encoding="utf-8"), timeout=40)
        except Exception as e: print("open_docs err", e)
else:
    print("not ready:", [(w[:8], s) for w, s in st])
