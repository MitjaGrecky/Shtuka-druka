# M2 - Level 1-8 block (part of P3)

**Not a board.** By decision R128 (13.11.2026) the eight Level knobs are on the P3 board (`hardware/p3-tracks`).
This folder keeps only `gen/design.py`: the parts, nets and placement of the Level block. P3's `gen/design.py` takes them
from here (refs renumbered after P3's own, placement shifted by (43.5, 17), I2C on P3's mux channel 1).
The standalone board (rev 0.1) and its generators were removed (#19, rule "one current version"); they are in the git history.

| | |
|---|---|
| Area | 24 x 205 mm of P3 (panel x 382.5-406.5, y 40-245), local coordinates: origin at the rear-left corner of that strip |
| Top side | 8 x EC11E encoders Level 8 ... Level 1 at x 394.5, y 52 + 25k; 96 x XL-1615RGBC-RF on 270-degree arcs, r = 10.5 mm (layout ring 21, R131) |
| Bottom side | 4 x LP5864 (cells A-D, on P3 LA-LD, 0x40-0x43) between the two rings of their pair; CY8CMBR3108 (0x37); 3 x 74HC165 and 6 pull-up packs under the encoders |
| LEDs | pairs Level 8+7 (A), 6+5 (B), 4+3 (C), 2+1 (D); upper ring of a pair on CS9-17, lower on CS0-8 (`kit.ring_matrix`, as M1 rev 0.5) |
| Touch | TR0-7 -> 560 R -> TOUCH0-7 = frame MP of ENC1-8 (Level 8 ... Level 1); CMOD 2.2 nF (C1531), VREG 100 nF |
| Shift chain | first register Q7 -> SR_OUT (on P3: SR_M2, after P3's buttons), Level 8 A, B, push first; last register DS <- SR_IN (on P3: SR_M4, from M4) |

`python gen/design.py` prints the block summary. License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
