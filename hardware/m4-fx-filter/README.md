# M4 - FX Mix + Filter (encoder module)

Two smooth encoders with push (FX Mix, Filter) and a 12-LED RGB ring around each; the same circuit as M3
(`hardware/common/gen/kit.py`, `knob_pair`). Spec: `hardware/for-routing/SPEC_boards.md`, section M4.
Status: rev 0.1 - schematic and placed board with mounts, not routed (`UNROUTED`). Package: `hardware/for-routing/M4/`.

| | |
|---|---|
| Board | 66 x 34 mm, 2 layers; panel x 339-405, y 263-297 |
| Top side | 2 x EC11E (panel x 355 and 389, y 277; knob 22 mm), 24 x XL-1615RGBC-RF on rings r 14 mm |
| Bottom side | LP5864, 74HC165, 2 x 4x10k, passives - between the encoder pins (the rings leave only 6 mm between them), J1 at the front edge |
| Bus | J1 2 x 7, 1.27 mm to P3 (I2C channel 2 of P3's TCA9546A, P99); chain P3 buttons -> M2 -> M4 |
| I2C | LP5864 0x40; ~INT not used |
| Shift chain | D7..D0: FX A, FX B, FX push, Filter A, Filter B, Filter push, 1, 1 |
| Holes | M2 in the corners and one in the middle of the rear edge (corners alone would be 60.8 mm apart) |

Checks (12.11.2026, KiCad 10.0.8): ERC 0 errors (4 warnings as M3); netlist 202 pins, 0 mismatches; DRC 0 errors, parity 0,
163 unrouted; EasyEDA Pro import (project M4_v1): PCB 38/38, schematic 38/38 nets, 46/46 parts.

Generators: `gen/design.py`, `gen/make_sch.py`, `gen/check_netlist.py`, `gen/make_pcb.py` (shared writers in `hardware/common/gen`).
PC (KiCad 10) in one go: `powershell -File hardware/common/gen/run_board.ps1 m4-fx-filter M4`.

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
