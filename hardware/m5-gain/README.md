# M5 - Gain 1 + 2 (encoder module on the slope, in W1's window)

Two smooth encoders with push (Gain 1, Gain 2), rings of 11 RGB LEDs and the two Clip LEDs - 24 RGB on one LP5864 (P103).
Spec: `hardware/for-routing/SPEC_boards.md`, section M5; W1: `hardware/w1-levels`. Status: rev 0.2 (V1 board to panel x 99, V2 rings r 10.5) - schematic and placed board,
not routed (`UNROUTED`). Package: `hardware/for-routing/M5/`.

| | |
|---|---|
| Board | 84 x 34 mm, 2 layers; panel x 15-99 (V1, user 13.11; W1 board x 5-89 - W1's window is widened by the cloud, its window `M5_X`), centred on the Gain row along the slope |
| Top side | 2 x EC11E (panel x 32 and 80, y 379; knob 16 mm), 22 x XL-1615RGBC-RF on rings r 10.5 mm (layout ring 21, V2) (11 per ring), Clip 1 and Clip 2 (x 48 and 96, y 386) |
| Bottom side | LP5864, 74HC165, 2 x 4x10k, passives between the knobs, J1 at the front edge at x 41 (opposite W1's J2) |
| Bus | J1 2 x 7, 1.27 mm to W1's J2; W1 passes the bus on (I2C channel 2 of P1's TCA9546A; W1 has 0x48, 0x54) |
| I2C | LP5864 0x40 |
| LEDs | Gain 1 ring + Clip 1 on CS9-17, Gain 2 ring + Clip 2 on CS0-8; each Clip LED is the 12th position of its ring's triples |
| Shift chain | D7..D0: Gain 1 A, B, push, Gain 2 A, B, push, 1, 1 (W1 reads M5 after its own P48 buttons) |
| Holes | M2 in the corners and one in the middle of the rear edge |

Checks (12.11.2026, KiCad 10.0.8): ERC 0 errors; netlist 202 pins, 0 mismatches; parity 0, 163 unrouted;
**DRC 2 errors: Clip 2 (D24) pads 0.15 mm from the right edge (rule 0.3)** - the LED sits at panel x 96, the board ends at 97.
EasyEDA Pro import (project M5_v2, rev 0.2; Clip 2 now 3 mm from the edge): PCB 38/38, schematic 38/38 nets, 46/46 parts.

Open questions (notes/handoff.md): Clip 2 at the edge (widen M5 and W1's window to panel x 99, or move Clip 2 to x 94);
ring radius: V2 (user 13.11) - the layout's ring (21 mm) wins over the spec formula (r 11): r 10.5 mm.

Generators: `gen/design.py`, `gen/make_sch.py`, `gen/check_netlist.py`, `gen/make_pcb.py` (shared writers in `hardware/common/gen`).
PC (KiCad 10) in one go: `powershell -File hardware/common/gen/run_board.ps1 m5-gain M5`.

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
