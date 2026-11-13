# M2 - Level 1-8 (module, 8 knobs, touch)

**Merged into P3 (decision R128, 13.11.2026): the Level knobs are on the P3 board (`hardware/p3-tracks`, rev 0.2).**
This folder stays as the source of the Level block: P3's `gen/design.py` takes the parts and the placement from
`gen/design.py` here. The standalone board below (rev 0.1, EasyEDA project M2_v2) is not to be made.

Eight Level knobs with 12-LED RGB rings and touch sensing on the knob frames. Spec: `hardware/for-routing/SPEC_boards.md`, section M2.
Status: rev 0.1 - schematic and placed board, not routed (`UNROUTED`). Package: `hardware/for-routing/M2/`.

| | |
|---|---|
| Board | 24 x 205 mm, 4 layers (as M1); panel x 382.5-406.5, y 40-245; sits in the notch of P3 (question V5: P3's edge at x 405 or 409) |
| Top side | 8 x EC11E encoders Level 8 ... Level 1 at x 394.5, y 52 + 25k; 96 x XL-1615RGBC-RF on 270-degree arcs, r = 10.5 mm (layout ring 21, V2) |
| Bottom side | 4 x LP5864 (cells A-D, 0x40-0x43) in the band between the two rings of their pair; CY8CMBR3108 (0x37) in band Level 7/6; 3 x 74HC165 and 6 pull-up packs under the encoders (free column x 6-17) |
| Bus | J1 2 x 7 1.27 in band Level 5/4 (board y 105.5 = panel y 139.5), opposite P3's J2 (I2C channel 1 of P3's TCA9546A) |
| LEDs | pairs Level 8+7 (A), 6+5 (B), 4+3 (C), 2+1 (D); upper ring of a pair on CS9-17, lower on CS0-8 (`kit.ring_matrix`, as M1 rev 0.5) |
| Touch | TR0-7 -> 560 R -> TOUCH0-7 = frame MP of ENC1-8 (Level 8 ... Level 1); CMOD 2.2 nF (C1531), VREG 100 nF |
| Shift chain | U6 first (Q7 -> SR_OUT: Level 8 A, B, push, Level 7 ...), U7, U8 last (DS <- SR_IN, pulled up by R3); chain P3 -> M2 -> M4 |
| Holes | 10 x M2: corners and both long sides in bands Level 7/6, 5/4, 3/2 (no more than 53 mm apart) |

Checks (13.11.2026, PC): EasyEDA Pro import (project M2_v2): PCB 146/146 and schematic 146/146 nets, 166/166 parts, against a reference
netlist from `design.py`; bottom-side courtyards checked with pcbnew (no overlaps, nothing on the encoders' through-hole pads).
ERC, DRC, `check_netlist.py` (it calls kicad-cli), pdf/dxf: cloud and CI.

Generators: `gen/design.py`, `gen/make_sch.py`, `gen/check_netlist.py`, `gen/make_pcb.py` (shared blocks in `hardware/common/gen`).
On the PC with KiCad 10 see `hardware/m3-tempo-swing/README.md` for `KICAD_SYMBOL_DIR` / `KICAD_FOOTPRINT_DIR`.

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
