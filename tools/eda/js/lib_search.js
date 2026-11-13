// Read-only: search the EasyEDA system library (LCSC parts) for each key in __KEYS__; return the first hits with
// their main properties. Filled by tools/eda/eda_parts.py.
const keys = __KEYS__;
const lib = await eda.lib_LibrariesList.getSystemLibraryUuid();
const out = {};
for (const k of keys) {
  try {
    const r = (await eda.lib_Device.search(k, lib, undefined, undefined, __N__, 1)) || [];
    out[k] = r.slice(0, __N__).map(x => {
      const o = JSON.parse(JSON.stringify(x));
      const keep = {};
      for (const f of ['name', 'uuid', 'description', 'manufacturer', 'manufacturerId', 'supplier', 'supplierId', 'lcsc', 'footprintName', 'symbolName', 'jlcpcbPartClass', 'stock', 'price', 'jlcInventory', 'lcscInventory', 'property', 'otherProperty'])
        if (o[f] !== undefined) keep[f] = o[f];
      if (Object.keys(keep).length < 3) return o;      // unknown shape: return everything
      return keep;
    });
  } catch (e) { out[k] = 'error: ' + e; }
}
return { library: lib, results: out };
