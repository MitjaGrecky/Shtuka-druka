"""Extra boards for tools/build_for_routing.py (SPEC_boards.md): id -> (project dir under hardware/, env, generators in gen/).
On the PC (KiCad 10) package with tools/pack_easyeda.py instead. License: AGPL-3.0-or-later.
"""
BOARDS = {
    "M3": ("m3-tempo-swing", {}, ["make_sch.py", "make_pcb.py"]),
    "M4": ("m4-fx-filter", {}, ["make_sch.py", "make_pcb.py"]),
    "M5": ("m5-gain", {}, ["make_sch.py", "make_pcb.py"]),
    "W2": ("w2-meters", {}, ["make_sch.py", "make_pcb.py"]),
    "W3": ("w3-system", {}, ["make_sch.py", "make_pcb.py"]),
    "P1": ("p1-left", {}, ["make_sch.py", "make_pcb.py"]),
    "P4": ("p4-right", {}, ["make_sch.py", "make_pcb.py"]),
    "P3": ("p3-tracks", {}, ["make_sch.py", "make_pcb.py"]),
    "M2": ("m2-levels", {}, ["make_sch.py", "make_pcb.py"]),
}
