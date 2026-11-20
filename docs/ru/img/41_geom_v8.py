"""Doc 41, sections 24.8-24.12: ONE source of the case geometry for the designer's side/fan drawings.
Values = the production assembly g3.build(30, 0, 117.0, 20, 0) (chief engineer, 20.11.2026; model3d/v8/build_v8.py -> v8.html),
NOT the trial parameters of g3.py __main__ (E=10, crest 120). Re-check with: python 41_geom_v8.py --check (runs g3, ~5 s)."""
import math, os, sys

W = 515.0                 # case width, x 0 (musician's left) .. 515
D = 500.0                 # depth, y 0 (front) .. 500
DECK = 30.0               # deck / front wall height, z
FOLD_Y = 300.0            # deck fold, start of the slope
SHELF_Y = 433.4           # end of the slope (front of the rear block)
CREST = 117.0             # crest height, z
ANG = math.degrees(math.atan((CREST - DECK) / (SHELF_Y - FOLD_Y)))   # 33.11 deg
TAN, COS, SIN = math.tan(math.radians(ANG)), math.cos(math.radians(ANG)), math.sin(math.radians(ANG))
FY0, FY1, FZ0, FZ1 = 390.5, 470.5, 3.5, 83.5      # fan 80 x 80 x 25 on the right wall (x 487-512)
CY, CZ = (FY0 + FY1) / 2, (FZ0 + FZ1) / 2          # 430.5, 43.5
PROF = [(0, 0), (0, DECK), (FOLD_Y, DECK), (SHELF_Y, CREST), (D, CREST), (D, 0)]
LABEL = "g3.build(30, 0, 117, 20, 0): глубина 500, скат 33,1° (y 300–433,4), макушка 117"


def top(y):
    """outer top edge of a side wall at depth y"""
    if y <= FOLD_Y: return DECK
    if y <= SHELF_Y: return DECK + (y - FOLD_Y) * TAN
    return CREST


def load(name):
    """import a sibling script whose name starts with digits"""
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(os.path.abspath(__file__)), name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


if __name__ == "__main__" and "--check" in sys.argv:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "model3d", "v8"))
    import g3
    m, P, col, tight = g3.build(30, 0, 117.0, 20, 0)
    fan = [p for p in P if p.name.startswith("Fan 80")][0]
    lo = [round(c - h, 1) for c, h in zip(fan.c, fan.h)]; hi = [round(c + h, 1) for c, h in zip(fan.c, fan.h)]
    got = (m.D, m.FOLD_Y, m.SHELF_Y, m.BACK_Z, lo[1], hi[1], lo[2], hi[2])
    want = (D, FOLD_Y, SHELF_Y, CREST, FY0, FY1, FZ0, FZ1)
    print("model", got, "\nhere ", want, "\nOK" if all(abs(a - b) < 0.05 for a, b in zip(got, want)) else "\nMISMATCH", "collisions", len(col))
