// Read-only geometric netlister for the project's schematic page (sch_Netlist.getNetlist() hangs).
// Nodes = coincident points of pins, wire vertices, net flags/ports (and points lying on wire segments).
// A name (net flag/port, or a named wire = imported label) names its node; equal names join globally,
// which is how EasyEDA itself connects nets. __PROJECT_UUID__ is replaced by eda_check.py.
const g = (o, k) => { const f = 'getState_' + k[0].toUpperCase() + k.slice(1); return typeof o[f] === 'function' ? o[f]() : o[k]; };
const t = await eda.dmt_EditorControl.getSplitScreenTree();
const tab = t.tabs.find(x => x.data && x.data.doctype === 1 && x.tabId.endsWith('@__PROJECT_UUID__'));
if (!tab) return { error: 'schematic tab of this project is not open' };
await eda.dmt_EditorControl.activateDocument(tab.tabId);
await new Promise(r => setTimeout(r, 1500));
const K = (x, y) => Math.round(x * 100) + ',' + Math.round(y * 100);
const par = {};
const f = a => { if (par[a] === undefined) par[a] = a; while (par[a] !== a) { par[a] = par[par[a]]; a = par[a]; } return a; };
const u = (a, b) => { const ra = f(a), rb = f(b); if (ra !== rb) par[ra] = rb; };
const flat = L => (Array.isArray(L[0]) ? L.flat() : L) || [];
const segs = [];
const wires = await eda.sch_PrimitiveWire.getAll();
for (const w of wires) {
  const L = flat(g(w, 'line') || []);
  for (let i = 0; i + 3 < L.length; i += 2) { u(K(L[i], L[i + 1]), K(L[i + 2], L[i + 3])); segs.push(L.slice(i, i + 4)); }
}
const onSeg = (x, y) => {
  for (const [a, b, c, d] of segs) {
    if (x < Math.min(a, c) - 0.01 || x > Math.max(a, c) + 0.01 || y < Math.min(b, d) - 0.01 || y > Math.max(b, d) + 0.01) continue;
    if (Math.abs((c - a) * (y - b) - (d - b) * (x - a)) < 0.01) return K(a, b);
  }
  return null;
};
const attach = (x, y) => { const k = K(x, y); f(k); const s = onSeg(x, y); if (s) u(k, s); return k; };
const ids = await eda.sch_PrimitiveComponent.getAllPrimitiveId();
const pins = [], names = [], flagCount = {}, refs = [];
let parts = 0;
for (const id of ids) {
  const c0 = await eda.sch_PrimitiveComponent.get(id); const o = Array.isArray(c0) ? c0[0] : c0;
  const ty = g(o, 'componentType');
  if (ty === 'part') {
    parts++;
    const des = g(o, 'designator');
    refs.push(des);
    for (const p of (await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(id)) || [])
      pins.push({ ref: des, pin: String(g(p, 'pinNumber')), k: attach(g(p, 'x'), g(p, 'y')) });
  } else if (ty === 'netflag' || ty === 'netport') {
    const n = g(o, 'net');
    names.push({ net: n, k: attach(g(o, 'x'), g(o, 'y')) });
    flagCount[n] = (flagCount[n] || 0) + 1;
  }
}
for (const w of wires) { const n = g(w, 'net'); const L = flat(g(w, 'line') || []); if (n && L.length >= 2) names.push({ net: n, k: K(L[0], L[1]) }); }
const first = {};
for (const nm of names) { if (first[nm.net]) u(nm.k, first[nm.net]); else first[nm.net] = nm.k; }
const rootNames = {};
for (const nm of names) { const r = f(nm.k); (rootNames[r] = rootNames[r] || new Set()).add(nm.net); }
const cnt = {};
for (const p of pins) { const r = f(p.k); cnt[r] = (cnt[r] || 0) + 1; }
const comps = {};
for (const d of refs) comps[d] = comps[d] || [];   // parts without pins (mounting holes) still count
for (const p of pins) {
  const r = f(p.k);
  const nm = rootNames[r] ? [...rootNames[r]].sort().join('+') : (cnt[r] > 1 ? 'N:' + r : '');
  (comps[p.ref] = comps[p.ref] || []).push([p.pin, nm]);
}
return { doc: tab.title, parts, flags: flagCount, comps };
