import json,os,math,pcbnew,subprocess,sys
PY=r"C:\Program Files\KiCad\10.0\bin\python.exe"
t=os.environ['TEMP']
out=subprocess.run([PY,'tools/eda/eda_exec.py','--project',sys.argv[1],'-c',"const ids=await eda.pcb_PrimitiveComponent.getAllPrimitiveId(); const out=[]; for (const id of ids){const c=await eda.pcb_PrimitiveComponent.get(id); out.push([c.designator,c.x,c.y,c.rotation,c.layer]);} return out;"],capture_output=True,text=True,timeout=150).stdout
d=json.loads(out[out.index('['):]); e={r[0]:r for r in d}
b=pcbnew.LoadBoard(sys.argv[2])
k={f.GetReference():(pcbnew.ToMM(f.GetPosition().x),pcbnew.ToMM(f.GetPosition().y)) for f in b.GetFootprints()}
import statistics as st
com=[r for r in k if r in e]
ox=st.median(k[r][0]-e[r][1]*.0254 for r in com); oy=st.median(k[r][1]+e[r][2]*.0254 for r in com)
n=sum(math.dist((e[r][1]*.0254+ox,-e[r][2]*.0254+oy),k[r])<0.3 for r in k if r in e)
print('parts',len(e),'matching KiCad position (<0.3 mm):',n)
