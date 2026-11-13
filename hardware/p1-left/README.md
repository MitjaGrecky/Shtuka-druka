# P1 - Left deck (time column)

19 buttons with 2 RGB each (P101), an I2C multiplexer (P99), the deck bus to P2 (P100) and the module buses to M3 and W1.
Spec: `hardware/for-routing/SPEC_boards.md`, section P1. Status: rev 0.1 - schematic and placed board, not routed (`UNROUTED`).
Package: `hardware/for-routing/P1/`. P99, P100, P101 are proposals: change them through the constants in `gen/design.py`.

| | |
|---|---|
| Board | 92 x 258 mm, 2 layers; panel x 10-102, y 4-262 |
| Top side | 19 x TS-1187A (C318884): Rec, Play, Stop, Restart, Metronome, Tap, Capture, Resample, Undo, Redo, Delete, Duplicate, Double, New, Quantize, Length, Automate, Repeat, Accent at their layout_v7 places; 38 x XL-1615RGBC-RF 6.5 mm left and right |
| Bottom side | 2 x LP5864 (U1 cell A 0x40: buttons 1-12, U2 cell B 0x41: 13-19) among their buttons; 3 x 74HC165 near their rows; TCA9546APWR (U6) near J1 |
| Buses | J1 2 x 8 to P2 at the right edge (P100: pins 1-14 as the module bus, 15 AUX unused, 16 GND); J2 2 x 7 to M3 and J3 2 x 7 to W1 at the rear edge |
| I2C | TCA9546A 0x70 (A2 A1 A0 via 0R to GND): ch 0 own LP5864s, ch 1 J2 (M3), ch 2 J3 (W1), ch 3 free; 4.7k pull-ups on ch 0-2, upstream pull-ups on P2 |
| Shift chain | P2 reads U3 (D7 Rec ... ), U4, U5 (bits 20-24 read 1), then M3 (J2), then W1 (J3), which continues to M5; W1's SR_IN pulled up here (R1); J1 pin 14 unused |
| ~INT | J2 and J3 ~INT go straight to J1 |
| Holes | 14 x M2: corners, short-side middles, long sides at rows without buttons (y 60, 97.5, 150, 197.5), at most 60 mm apart |

Checks (13.11.2026, PC): EasyEDA Pro import (project P1_v1): PCB 83/83 and schematic 83/83 nets, 110/110 parts, against a
reference netlist written from `design.py`. ERC, DRC, parity: CI (kicad-cli crashes this PC). No `schematic.pdf`/`outline.dxf` yet.
The TCA9546A symbol is converted from KiCad 10's library to the KiCad 7 format by `hardware/common/gen/sym7.py`.

Open: LCSC number of TCA9546APWR (to choose, P99); J2/J3 places at the rear edge follow M3's and W1's connectors (both near panel x 56) - set apart (x 40 and 72) so the two ribbons do not collide.

Generators: `gen/design.py`, `gen/make_sch.py`, `gen/check_netlist.py`, `gen/make_pcb.py` (shared blocks: `hardware/common/gen/kit.py` - `deck_inputs`, `i2c_mux`, `deck_bus`).

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
