"""Extra boards for tools/build_for_routing.py (SPEC_boards.md): id -> (project dir under hardware/, env, generators in gen/).
On the PC (KiCad 10) package with tools/pack_easyeda.py instead. License: AGPL-3.0-or-later.
"""
BOARDS = {
    "M3": ("m3-tempo-swing", {}, ["make_sch.py", "make_pcb.py"]),
    "M4": ("m4-fx-filter", {}, ["make_sch.py", "make_pcb.py"]),
    "M5": ("m5-gain", {}, ["make_sch.py", "make_pcb.py"]),
}
