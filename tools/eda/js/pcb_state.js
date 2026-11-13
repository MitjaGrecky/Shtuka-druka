// Read-only. State of the open PCB: copper layers, tracks, vias, pours, components; DRC rule set name and the
// spacing table of the current rule configuration (as far as the API exposes it). Each call is guarded:
// while the PCB is still loading some calls return null.
const safe = async (f) => { try { return await f(); } catch (e) { return 'ERR ' + e; } };
const n = async (api) => safe(async () => { const a = await api.getAllPrimitiveId(); return a ? a.length : null; });
const out = {
  copperLayers: await safe(() => eda.pcb_Layer.getTheNumberOfCopperLayers()),
  tracks: await n(eda.pcb_PrimitiveLine), vias: await n(eda.pcb_PrimitiveVia),
  pours: await n(eda.pcb_PrimitivePour), components: await n(eda.pcb_PrimitiveComponent),
};
out.rule = await safe(async () => {
  const r = await eda.pcb_Drc.getCurrentRuleConfiguration();
  const c = (r && r.config) || {};
  const res = { name: r && r.name, sections: Object.keys(c) };
  const sp = c.Spacing && c.Spacing['Safe Spacing'];
  if (sp && sp.copperThickness1oz) res.spacing1oz = sp.copperThickness1oz.tables['1'];
  for (const k of Object.keys(c)) if (k !== 'Spacing') res[k] = JSON.stringify(c[k]).slice(0, 1500);
  return res;
});
return out;
