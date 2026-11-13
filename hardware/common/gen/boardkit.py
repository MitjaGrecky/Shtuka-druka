"""Small board-writing helpers shared by the kit-based boards (no pcbnew import here, so design files stay light).

P(x, y): board mm -> KiCad internal units with the sheet origin used by all Shtuka Druka boards.
write_project(): design rules and net classes of a 2-layer JLCPCB board into <name>.kicad_pro.
License: AGPL-3.0-or-later.
"""
import json
import os

ORG = (40.0, 40.0)                      # where the board sits on the drawing sheet, mm (same as M1, W1)
# JLCPCB 2-layer standard (0.127 mm track/space, 0.3 mm via drill), here with margin
TRACK, CLEAR, VIA, POWER_TRACK, SW_TRACK = 0.15, 0.15, (0.6, 0.3), 0.3, 0.25
POWER_NETS = ("+5V", "GND", "+3V3")


def P(x, y):
    import pcbnew
    return pcbnew.VECTOR2I(pcbnew.FromMM(ORG[0] + x), pcbnew.FromMM(ORG[1] + y))


def flip_bottom(fp):
    """Put a footprint on the bottom side the same way in every KiCad version (task #15 from the cloud).
    Reference: KiCad 9/10, Flip(pos, FLIP_DIRECTION_TOP_BOTTOM) - what the PC builds and EasyEDA checks.
    KiCad 7 only mirrors left-right (Flip(pos, True)); a left-right mirror turned by 180 degrees is the top-bottom mirror."""
    import pcbnew
    pos = fp.GetPosition()
    if hasattr(pcbnew, "FLIP_DIRECTION_TOP_BOTTOM"):
        fp.Flip(pos, pcbnew.FLIP_DIRECTION_TOP_BOTTOM)
    else:
        fp.Flip(pos, True)
        fp.SetOrientationDegrees((fp.GetOrientationDegrees() + 180.0) % 360.0)


_PIN_NAMES = {}


def pin_name(lib_id, num):
    """Pin name of a library symbol (for KiCad's unconnected-(REF-NAME-PadN) nets); reads the same symbol
    sources as the schematic writer (KICAD_SYMBOL_DIR, project library)."""
    import re
    if lib_id not in _PIN_NAMES:
        import m1compat
        txt = m1compat.load("make_sch").lib_block(lib_id)[0]
        _PIN_NAMES[lib_id] = {n: nm for nm, n in re.findall(r'\(name "([^"]*)".*?\(number "([^"]+)"', txt, re.S)}
    return _PIN_NAMES[lib_id].get(num, "")


def copy_fields(fp, fields):
    """Symbol fields (LCSC, Note, ...) onto the footprint, hidden, so schematic parity has nothing to report."""
    import pcbnew
    for k, v in fields.items():
        if hasattr(fp, "SetField"):                     # KiCad 8+: new fields are visible on F.SilkS by default
            fp.SetField(k, str(v))
            for f in fp.GetFields():
                if f.GetName() == k:
                    f.SetVisible(False)
                    f.SetLayer(pcbnew.B_Fab if fp.IsFlipped() else pcbnew.F_Fab)
        else:                                           # KiCad 7: properties are not drawn
            fp.SetProperty(k, str(v))


def write_project(proj_dir, name):
    cls = dict(clearance=CLEAR, track_width=TRACK, via_diameter=VIA[0], via_drill=VIA[1], microvia_diameter=0.3,
               microvia_drill=0.1, diff_pair_gap=0.25, diff_pair_width=0.2, diff_pair_via_gap=0.25,
               wire_width=6, bus_width=12, line_style=0)
    pro = {
        "board": {"design_settings": {"meta": {"version": 2}, "rules": {
            "min_clearance": 0.127, "min_track_width": 0.127, "min_via_diameter": 0.5, "min_via_annular_width": 0.1,
            "min_through_hole_diameter": 0.3, "min_hole_clearance": 0.254, "min_hole_to_hole": 0.25,
            "min_copper_edge_clearance": 0.3, "min_silk_clearance": 0.0, "min_text_height": 0.8,
            "min_text_thickness": 0.08}}},
        "net_settings": {"meta": {"version": 3},
                         "classes": [dict(cls, name="Default"), dict(cls, name="Power", track_width=POWER_TRACK),
                                     dict(cls, name="LED_SW", track_width=SW_TRACK)],
                         "netclass_patterns": [{"netclass": "Power", "pattern": n} for n in POWER_NETS] +
                                              [{"netclass": "LED_SW", "pattern": p} for p in ("/?_SW*", "?_SW*")]},
        "meta": {"filename": name + ".kicad_pro", "version": 1},
    }
    with open(os.path.join(proj_dir, name + ".kicad_pro"), "w", encoding="utf-8") as f:
        json.dump(pro, f, indent=2)
