"""Snapshot of the P137 model (boxes from p137_parts.json): rotatable canvas html + png. Colours by name; case shell translucent."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(H, "p137_parts.json")))
def col(n):
    if n.startswith("Battery"): return "#e0a030", 1
    if n.startswith(("Floor", "Front wall", "Rear wall")): return "#8a949c", .25
    if n.startswith(("Top skin", "Slope skin")): return "#8a949c", .18
    if n.startswith(("Fan", "H5", "Mini")): return "#c0504d", .8
    if n.startswith(("PW", "A1", "R1", "R2", "P2", "P1", "P3", "P4")): return "#2f6f4f", .8
    return "#6b7b86", .7
for d in D: d["c"], d["al"] = col(d["n"])
html = """<!doctype html><meta charset=utf-8><title>P137</title><body style="margin:0"><div style="font:13px sans-serif;padding:6px">P139: два блока Ampul 145×130×14 (оранжевые) под P2: x 187–332, y 6–136 и 138–268; 0 столкновений. Вид спереди-сверху; мышь — вращение.</div><canvas id=c width=1200 height=760></canvas><script>
const D=__D__;const c=document.getElementById('c'),g=c.getContext('2d');let az=-0.55,el=0.5,sc=1.75;
function R(p){const x=p[0]-257,y=p[1]-250,z=(p[2]-30)*1.6;const ca=Math.cos(az),sa=Math.sin(az);const X=x*ca-y*sa,Y=x*sa+y*ca;const ce=Math.cos(el),se=Math.sin(el);return[600+X*sc,430-(z*ce+Y*se)*sc,Y*ce-z*se]}
function draw(){g.clearRect(0,0,1200,760);const L=[];for(const p of D){const a=p.a,b=p.b,V=[];for(const z of[a[2],b[2]])for(const y of[a[1],b[1]])for(const x of[a[0],b[0]])V.push([x,y,z]);const T=V.map(R);for(const f of[[0,1,3,2],[4,5,7,6],[0,1,5,4],[2,3,7,6],[0,2,6,4],[1,3,7,5]]){const q=f.map(i=>T[i]);L.push([q.reduce((s,t)=>s+t[2],0)/4,q,p.c,p.al])}}L.sort((u,v)=>v[0]-u[0]);for(const l of L){g.beginPath();l[1].forEach((p,i)=>i?g.lineTo(p[0],p[1]):g.moveTo(p[0],p[1]));g.closePath();g.globalAlpha=l[3];g.fillStyle=l[2];g.fill();g.globalAlpha=1;g.strokeStyle='#1d2024';g.lineWidth=.3;g.stroke()}}
let d=0,lx=0,ly=0;c.onmousedown=e=>{d=1;lx=e.clientX;ly=e.clientY};onmouseup=()=>d=0;onmousemove=e=>{if(d){az+=(e.clientX-lx)*.01;el=Math.max(0,Math.min(1.5,el+(e.clientY-ly)*.01));lx=e.clientX;ly=e.clientY;draw()}};draw()</script>"""
open(os.path.join(H, "p137_snapshot.html"), "w", encoding="utf-8").write(html.replace("__D__", json.dumps(D)))
