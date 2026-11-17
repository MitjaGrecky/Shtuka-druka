"""Main engineer, 17.11.2026: orange profile without the front lip (jacks 3.5 mm in the front wall, small F1 under the front of P1); reuses docs/ru/img/41_wedge_study.py. Run: KiCad python; the model is only read."""
import importlib.util, math, sys, os
sys.path.insert(0, r"docs/ru/img")
spec=importlib.util.spec_from_file_location("ws","docs/ru/img/41_wedge_study.py"); ws=importlib.util.module_from_spec(spec); spec.loader.exec_module(ws)
def go(lip, st=8, j35=True):
    fs,ang,roof=15,33,41
    rl,D=453.4+fs,500+fs
    h5y=D-3-15-60-0.5
    e=ws.env(22,31,fs,rl-101,20,f"40,210,{rl-101},{rl-1},3",h5y,h5_st=st)
    if not lip: e.update(FRONT_LIP=0)
    run_len=D-3-roof-(300+fs); back=round(31+run_len*math.tan(math.radians(ang)),1)
    m=ws.load(e,D-3-roof,back,30)
    harness=(391,511,h5y-60-45,h5y-60-25,3.5,26)
    rw0=ws.corner_rework2(harness=harness)
    def rw(m,P):
        P=rw0(m,P)
        if not lip:
            P=[p for p in P if p.name not in ("Phones 1 jack","Phones 2 jack","F1 headphone board","F1 headphone board parts below")]
            S=m.SKIN
            for p in list(P):
                if p.name=="P1 Left parts below":      # the real P1 has no bottom parts in the front 43 mm (checked on p1-left.kicad_pcb)
                    lo=[c-h for c,h in zip(p.c,p.h)]; hi=[c+h for c,h in zip(p.c,p.h)]
                    P.remove(p); P.append(m.box("P1 Left parts below (from y 43)","panel",lo[0],hi[0],43,hi[1],lo[2],hi[2],color="parts",est=True))
            for x in (32,80):
                P.append(m.box(f"Phones jack 3.5 at x {x}","front",x-4.5,x+4.5,3.0,16.0,S+0.4+1.6,S+0.4+1.6+5.5,color="metal",est=True))
            P.append(m.box("F1 small board","front",12,102,3.0,38,S+0.4,S+0.4+1.6,color="pcb"))
            P.append(m.box("F1 relays 5.4","front",45,70,18,36,S+0.4+1.6,S+0.4+1.6+5.4,color="parts",est=True))
            P.append(m.box("F1 low parts 2.5","front",72,100,18,36,S+0.4+1.6,S+0.4+1.6+2.5,color="parts",est=True))
        return P
    col=ws.collisions(m,rw)
    print(f"lip {'28' if lip else '0'}, H5 standoff {st}: depth {m.D+m.FL:g}, rear {m.BACK_Z:g}, collisions {len(col)}", sorted(col,reverse=True)[:8])
go(True,8); go(False,8)
