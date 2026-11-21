"""P141: full production assembly g3.build(30, 0, 117, 20, 0) with the P140 battery set (6 cells, 2 BM, 3 NTC from blocks3.csv). Prints collisions of the whole case; writes p137_parts.json for the snapshot."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "v8"))
import g3
m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
print("P143 parts:", len(P), "| collisions of the whole case:", len(col), col[:5], "| tight < 1 mm:", len(tight), tight[:4], flush=True)
print("battery parts:", sorted(p.name for p in P if p.name.startswith(("Cell", "BM", "NTC", "Battery"))), flush=True)
json.dump([{"n": p.name, "g": getattr(p, "group", ""), "a": [round(c - h, 2) for c, h in zip(p.c, p.h)], "b": [round(c + h, 2) for c, h in zip(p.c, p.h)]} for p in P if not p.name.startswith("Hatch vent") and "groove" not in p.name], open(os.path.join(HERE, "p137_parts.json"), "w"))
print("done", flush=True)
