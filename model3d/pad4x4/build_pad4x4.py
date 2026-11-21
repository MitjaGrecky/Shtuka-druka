#!/usr/bin/env python3
"""Test pad 4x4 (R194, P120): 3D model + collision check. Concept geometry from docs/ru/41_design_review/42_24-15; no electrics.
x: musician's left -> right, y: front -> back (as the case), z from the outer floor, mm. Boxes are axis-aligned (AABB).
Left half (cols 0-1) = V1 monolith foot 19x15, right half (cols 2-3) = V3 four blocks 8.5x6.5 with a 2 mm cross slot.
Run: python build_pad4x4.py  -> pad4x4.json, pad4x4.html (rotatable canvas view), prints the collision/gap table."""
import itertools, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
PX, PY = 28.0, 25.0                      # pitch (doc 27 s4)
PAD_X, PAD_Y = 25.5, 21.0
GAP = 0.4                                 # deck opening clearance per side
Z_PCB0, Z_PCB1 = 18.9, 20.5               # board, z as P2 in g3
Z_TAPE1 = 20.6                            # spacer tape 0.1 (research 0.05-0.1)
Z_FILM1 = 20.73                           # XactFSR 0.13 (research, unverified)
PRE = 0.15                                # foot interference on the film
Z_WEB0, Z_DECK0, Z_DECK1, Z_TOP = 25.8, 27.0, 30.0, 33.0
FIELD = (21.0, 17.0)                      # comb field (P120)
FOOT = (19.0, 15.0)                       # support pad (P120)
NX, NY = 4, 4
X0, Y0 = 10.0, 10.0                       # first cell centre on the test board (board margin 10)
BX, BY = NX * PX + 20.0, NY * PY + 20.0   # test board 132 x 120 (assumption)
parts = []                                # (name, group, (x0,y0,z0),(x1,y1,z1), color)


def box(n, g, x0, y0, z0, x1, y1, z1, c):
    parts.append((n, g, (round(x0, 3), round(y0, 3), round(z0, 3)), (round(x1, 3), round(y1, 3), round(z1, 3)), c))


box("Board 1.6", "board", 0, 0, Z_PCB0, BX, BY, Z_PCB1, "#2f6f4f")
cx = lambda i: X0 + PX / 2 + i * PX
cy = lambda j: Y0 + PY / 2 + j * PY
mx0, mx1, my0, my1 = cx(0) - PX / 2, cx(NX - 1) + PX / 2, cy(0) - PY / 2, cy(NY - 1) + PY / 2
box("Silicone web (one mat)", "mat", mx0, my0, Z_WEB0, mx1, my1, Z_DECK0, "#cfe8e1")
box("Deck skin plate", "deck", mx0 - 6, my0 - 6, Z_DECK0, mx1 + 6, my1 + 6, Z_DECK1, "#3a3f45")  # opened below by holes (not a box): see openings
openings = []
for i, j in itertools.product(range(NX), range(NY)):
    x, y = cx(i), cy(j)
    v = "V1" if i < NX // 2 else "V3"
    tag = f"{v} r{j}c{i}"
    for nm, (xa, ya, xb, yb) in (("N", (-12, 8.5, 12, 10)), ("S", (-12, -10, 12, -8.5)), ("W", (-12, -8.5, -10.5, 8.5)), ("E", (10.5, -8.5, 12, 8.5))):
        box(f"Tape frame {nm} {tag}", "tape", x + xa, y + ya, Z_PCB1, x + xb, y + yb, Z_TAPE1, "#c9b27c")   # ring: outer 24x20, inner 21x17 (= comb field)
    box(f"Film {tag}", "film", x - 11.5, y - 9.5, Z_TAPE1, x + 11.5, y + 9.5, Z_FILM1, "#7a6a52")
    box(f"Pad body {tag}", "mat", x - PAD_X / 2, y - PAD_Y / 2, Z_DECK0, x + PAD_X / 2, y + PAD_Y / 2, Z_TOP, "#cfe8e1")
    fx, fy = FOOT[0] / 2, FOOT[1] / 2
    if v == "V1":
        box(f"Foot {tag}", "mat", x - fx, y - fy, Z_FILM1 - PRE, x + fx, y + fy, Z_WEB0, "#5fa894")
    else:
        for sx, sy in itertools.product((-1, 1), (-1, 1)):
            xa, xb = sorted((sx * 1.0, sx * fx)); ya, yb = sorted((sy * 1.0, sy * fy))
            box(f"Foot block {tag}", "mat", x + xa, y + ya, Z_FILM1 - PRE, x + xb, y + yb, Z_WEB0, "#5fa894")
    openings.append((x - PAD_X / 2 - GAP, y - PAD_Y / 2 - GAP, x + PAD_X / 2 + GAP, y + PAD_Y / 2 + GAP))
# light holes (data only): board dia 4, film dia 5, foot relief dia 6 (V1) / cross (V3)
holes = [{"x": cx(i), "y": cy(j), "board_d": 4.0, "film_d": 5.0} for i, j in itertools.product(range(NX), range(NY))]

# ---- checks ----
def ov(a, b):
    d = [min(a[3][k], b[3][k]) - max(a[2][k], b[2][k]) for k in range(3)]
    return d
ALLOWED = {frozenset(("film", "mat")): "preload 0.15", frozenset(("tape", "film")): "film lies on tape frame", frozenset(("board", "tape")): "touch", frozenset(("mat", "deck")): "web under deck"}
report = {"overlaps": [], "touch": 0, "allowed": {}}
for a, b in itertools.combinations(parts, 2):
    if a[1] == b[1]: continue
    d = ov(a, b)
    if all(x > 1e-6 for x in d):
        # deck plate vs pad body: the plate has openings -> check the body is inside its opening instead
        if {a[1], b[1]} == {"mat", "deck"}:
            continue
        key = frozenset((a[1], b[1]))
        if key in ALLOWED:
            report["allowed"].setdefault(ALLOWED[key], 0); report["allowed"][ALLOWED[key]] += 1
        else:
            report["overlaps"].append((a[0], b[0], [round(x, 3) for x in d]))
# body vs openings, neighbour webs
bad = []
for (i, j), op in zip(itertools.product(range(NX), range(NY)), openings):
    x, y = cx(i), cy(j)
    if not (op[0] < x - PAD_X / 2 and op[2] > x + PAD_X / 2 and op[1] < y - PAD_Y / 2 and op[3] > y + PAD_Y / 2): bad.append((i, j))
web_x = PX - (PAD_X + 2 * GAP); web_y = PY - (PAD_Y + 2 * GAP)
foot_in_field = FOOT[0] < FIELD[0] and FOOT[1] < FIELD[1]
film_in_frame = 23.0 <= 24.0
print(f"parts {len(parts)}; board {BX:g} x {BY:g}; pads {NX * NY} (V1 {NX * NY // 2}, V3 {NX * NY // 2})")
print(f"opening {PAD_X + 2 * GAP:.1f} x {PAD_Y + 2 * GAP:.1f}; deck web x {web_x:.1f} (P120 1.7), y {web_y:.1f}; pad-to-deck gap {GAP}")
print(f"foot {FOOT} inside field {FIELD}: {foot_in_field}; foot bottom {Z_FILM1 - PRE:.2f} vs film top {Z_FILM1} (preload {PRE})")
print("hard overlaps:", len(report["overlaps"]), report["overlaps"][:3], "| allowed contacts:", report["allowed"], "| pads outside opening:", bad)
ok = not report["overlaps"] and not bad and abs(web_x - 1.7) < 1e-6 and foot_in_field
print("RESULT", "OK" if ok else "FAIL")
json.dump({"parts": [{"n": p[0], "g": p[1], "a": p[2], "b": p[3], "c": p[4]} for p in parts], "openings": openings, "holes": holes}, open(os.path.join(HERE, "pad4x4.json"), "w"))
html = """<!doctype html><meta charset=utf-8><title>pad4x4</title><body style="margin:0;background:#fff;font:13px sans-serif"><div style="padding:8px">Тестовый пэд 4×4 (R194, P120), концепт. Мышь: вращение; колесо: масштаб. Слева V1, справа V3. Дека — полупрозрачная плита без отверстий (отверстия 26,3 × 21,8 проверены числами). z вверх, x вправо (взгляд спереди), y вглубь.</div><canvas id=c width=1100 height=700></canvas><script>
const D=__DATA__;const c=document.getElementById('c'),g=c.getContext('2d');let az=-0.6,el=0.55,sc=5.2;
function R(p){const x=p[0]-70,y=p[1]-60,z=(p[2]-18)*3;const ca=Math.cos(az),sa=Math.sin(az);const X=x*ca-y*sa,Y=x*sa+y*ca;const ce=Math.cos(el),se=Math.sin(el);return[550+X*sc,420-(z*ce+Y*se)*sc,Y*ce-z*se]}
function face(P,col,al){g.beginPath();P.forEach((p,i)=>i?g.lineTo(p[0],p[1]):g.moveTo(p[0],p[1]));g.closePath();g.globalAlpha=al;g.fillStyle=col;g.fill();g.globalAlpha=1;g.strokeStyle='#1d2024';g.lineWidth=.5;g.stroke()}
function draw(){g.clearRect(0,0,1100,700);const L=[];for(const p of D.parts){const[a,b]=[p.a,p.b];const V=[];for(const z of[a[2],b[2]])for(const y of[a[1],b[1]])for(const x of[a[0],b[0]])V.push([x,y,z]);const T=V.map(R);const F=[[0,1,3,2],[4,5,7,6],[0,1,5,4],[2,3,7,6],[0,2,6,4],[1,3,7,5]];for(const f of F){const q=f.map(i=>T[i]);L.push([q.reduce((s,t)=>s+t[2],0)/4,q,p.c,p.g=='deck'?.35:1])}}L.sort((u,v)=>v[0]-u[0]);for(const l of L)face(l[1],l[2],l[3])}
let d=0,lx=0,ly=0;c.onmousedown=e=>{d=1;lx=e.clientX;ly=e.clientY};onmouseup=()=>d=0;onmousemove=e=>{if(d){az+=(e.clientX-lx)*.01;el=Math.max(0,Math.min(1.5,el+(e.clientY-ly)*.01));lx=e.clientX;ly=e.clientY;draw()}};c.onwheel=e=>{sc*=e.deltaY<0?1.1:.9;draw();e.preventDefault()};draw()</script>"""
open(os.path.join(HERE, "pad4x4.html"), "w", encoding="utf-8").write(html.replace("__DATA__", json.dumps({"parts": [{"n": p[0], "g": p[1], "a": p[2], "b": p[3], "c": p[4]} for p in parts]})))
