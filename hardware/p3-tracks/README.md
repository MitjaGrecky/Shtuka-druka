# P3 - Tracks deck with the Level knobs

21 buttons with 2 RGB each (P101), 8 Level encoders with 12-LED RGB rings and touch (the former module M2), an I2C
multiplexer (P99), the deck bus to P2 (P100) and the module buses to M4 and W2. Spec: `hardware/for-routing/SPEC_boards.md`,
sections P3 and M2. Rev 0.2 (13.11.2026): P3 and M2 on one 4-layer board - decision R128 (closes question V5);
rev 0.3: Level rings r 10.5 mm from the layout (V2), right-edge hole at the Level 8 ring moved to y 223.5.
rev 0.4: the Level LED drivers U7-U10 sit in the middle of the LED-free gap between two rings (their exposed-pad vias were
at 0 mm from ring LEDs D48, D72, D96, D120 in EasyEDA's DRC; now 1.38 mm).
Status: schematic and placed board, not routed (`UNROUTED`). Package: `hardware/for-routing/P3/`.

| | |
|---|---|
| Board | 67.5 x 258 mm, 4 layers; panel x 339-406.5, y 4-262 (right edge = right edge of the former M2 strip; P4 starts at x 413) |
| Top side | 21 x TS-1187A: Solo, Arm, Arrow down, Mute 8..1, Select 8..1, Stop All, Arrow up; 42 x XL-1615RGBC-RF beside the buttons; 8 x EC11E Level 8..1 at x 394.5, y 52 + 25k with 96 x XL-1615RGBC-RF on rings r = 10.5 mm (layout ring 21, V2) |
| Bottom side, buttons | 2 x LP5864 (A 0x40 buttons 1-12, B 0x41 buttons 13-21), 3 x 74HC165, TCA9546APWR (U6, 0x71) near J1 - left part, board x 0-43 |
| Bottom side, Level | the block of `hardware/m2-levels` (rev 0.1) with its placement shifted by (43.5, 17): 4 x LP5864 (cells LA-LD, 0x40-0x43) between the ring pairs, CY8CMBR3108 (0x37), 3 x 74HC165 and pull-up packs under the encoders |
| I2C | TCA9546A 0x71: ch 0 own LP5864s, ch 1 the Level block (its LP5864s use the same addresses as ch 0, hence the separate channel), ch 2 J3 (M4), ch 3 J4 (W2); 4.7k pull-ups on all four channels |
| Shift chain | U3 (D7 Solo ...), U4, U5 (bits 22-24 read 1), then the Level registers (Level 8 A, B, push first), then M4 (J3); M4's SR_IN pulled up here (R1); W2 not in the chain (J4 pins 13/14 open) |
| Buses | J1 2 x 8 to P2 at the left edge; J3 2 x 7 to M4 and J4 2 x 7 to W2 at the rear edge (the M2 connector J2 is gone) |
| Holes | 19 x M2: corners, rear x 16, front middle, left edge and the column between Select and Level at the button row gaps, right edge at y 2.6, 19.6, 72.5, 122.5, 172.5, 223.5, 255.4 (no hole closer than 2.3 mm to a pad) |

Checks (13.11.2026, PC): EasyEDA Pro import (project P3_v5, rev 0.4): PCB 226/226 and schematic 226/226 nets, 276/276 parts, against a
reference netlist from `design.py`; bottom-side courtyards checked with pcbnew (no overlaps, nothing on through-hole pads).
ERC, DRC, parity, pdf/dxf: cloud and CI. Rev 0.1 (separate P3 with a notch, project P3_v1) is in the git history.

Generators: `gen/design.py` (takes the Level block from `hardware/m2-levels/gen/design.py`), `gen/make_sch.py`,
`gen/check_netlist.py`, `gen/make_pcb.py` (shared blocks in `hardware/common/gen`).

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
