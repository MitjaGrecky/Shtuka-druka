# P3 - Tracks deck (track column)

21 buttons with 2 RGB each (P101), a window for the Level knob strip M2, an I2C multiplexer (P99), the deck bus to P2 (P100)
and the module buses to M2, M4 and W2. Spec: `hardware/for-routing/SPEC_boards.md`, section P3.
Status: rev 0.1 - schematic and placed board, not routed (`UNROUTED`). Package: `hardware/for-routing/P3/`.

| | |
|---|---|
| Board | 66 x 258 mm, 2 layers; panel x 339-405, y 4-262; notch for M2 open to the right edge: board x 43-66, y 16.5-222.5 (M2 strip x 382.5-406.5, y 40-245 + 0.5 mm) |
| Top side | 21 x TS-1187A: Solo, Arm, Arrow down, Mute 8..1, Select 8..1, Stop All, Arrow up (layout_v7 places); 42 x XL-1615RGBC-RF (5.5 mm at 16 mm buttons, 6.5 mm at Stop All) |
| Bottom side | 2 x LP5864 (A 0x40 buttons 1-12, B 0x41 buttons 13-21), 3 x 74HC165, TCA9546APWR (U6, 0x71) near J1, passives - all left of the notch |
| Buses | J1 2 x 8 to P2 at the left edge (P100); J2 2 x 7 to M2 at the notch edge; J3 2 x 7 to M4 and J4 2 x 7 to W2 at the rear edge |
| I2C | TCA9546A 0x71: ch 0 own LP5864s, ch 1 J2 (M2), ch 2 J3 (M4), ch 3 J4 (W2); 4.7k pull-ups on all four channels |
| Shift chain | U3 (D7 Solo ...), U4, U5 (bits 22-24 read 1), then M2 (J2), then M4 (J3); M4's SR_IN pulled up here (R1); W2 not in the chain (J4 pins 13/14 open) |
| Holes | 14 x M2: corners, rear edge x 16, front middle, left edge and notch edge at rows without buttons (y 47.5, 97.5, 147.5, 197.5) |

Checks (13.11.2026, PC): EasyEDA Pro import (project P3_v1): PCB 90/90 and schematic 90/90 nets, 120/120 parts, against a reference
netlist from `design.py`. ERC, DRC, parity, pdf/dxf: cloud and CI (task #14 in notes/handoff.md). Board outline: `OUTLINE` in `gen/design.py`.
Open: V5 (right edge at x 405 or 409; `X1` in `gen/design.py`).

Generators: `gen/design.py`, `gen/make_sch.py`, `gen/check_netlist.py`, `gen/make_pcb.py` (shared blocks in `hardware/common/gen`).

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
