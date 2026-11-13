# P4 - Right deck (value column)

20 buttons with 2 RGB each (P101), the crossfader digitised on the board (ADS1115, P104), the wheel sensor (AS5600),
an I2C multiplexer (P99), the deck bus to P2 (P100) and the module bus to W3. Spec: `hardware/for-routing/SPEC_boards.md`, section P4.
Status: rev 0.1 - schematic and placed board, not routed (`UNROUTED`). Package: `hardware/for-routing/P4/`.

| | |
|---|---|
| Board | 92 x 293 mm, 2 layers; panel x 413-505, y 4-297 (reaches the wheel row: no cut-out for M modules on this side) |
| Top side | 20 x TS-1187A: Scene A, Scene B, Chords, Touch FX, Scale, Clips, Steps, Notes, Sound, Effects, Mod, Mixer, Song, Browser, Sampler, Inputs, Settings, Page <, Back, Page > (layout_v7 places), 40 x XL-1615RGBC-RF (6.5 mm, 5.5 mm at the 14 mm Scene buttons); crossfader RV1 (Bourns PTA4543 footprint, 45 mm travel) at x 459, y 22; AS5600 (U8) right under the wheel axis (x 459, y 277) |
| Bottom side | 2 x LP5864 (A 0x40 buttons 1-12, B 0x41 buttons 13-20), 3 x 74HC165, ADS1115 (U7, 0x48), TCA9546APWR (U6, 0x72) near J1, passives |
| Buses | J1 2 x 8 to P2 at the left edge (P100); J3 2 x 7 to W3 at the rear edge (over the fold); J4 JST PH 2-pin for a wheel push switch (V10, user 13.11: keep; the push mechanism is chosen later) |
| I2C | TCA9546A 0x72: ch 0 own LP5864s + ADS1115 0x48 + AS5600 0x36, ch 1 J3 (W3), ch 2-3 free |
| Crossfader | wiper -> 1k / 100n -> ADS1115 AIN0 (AIN1-3 to GND); part not chosen (P90): PTA4543-2015DPB103 (C17444183) as a placeholder |
| Wheel | AS5600 3.3 V mode (VDD5V = VDD3V3 = +3V3, 100n + 1u), DIR to GND, OUT and PGO open; magnet on the wheel shaft above the chip |
| Shift chain | U3 (D7 Scene A ...), U4, U5 (bit 21 = wheel push, bits 22-24 read 1), then W3 (J3); W3's SR_IN pulled up here (R1) |
| Holes | 17 x M2: corners, rear edge at x 20 and 72 (clear of the wheel), front middle, long sides at rows without buttons |

Checks (13.11.2026, PC): EasyEDA Pro import (project P4_v1): PCB 84/84 and schematic 84/84 nets, 123/123 parts, against a reference
netlist from `design.py`. ERC, DRC, parity and pdf/dxf: cloud and CI (task #14 in notes/handoff.md).
AS5600 symbol: `hardware/common/lib/Common.kicad_sym` (KiCad's library has none), resolved by `hardware/common/gen/m1compat.py`.

Generators: `gen/design.py`, `gen/make_sch.py`, `gen/check_netlist.py`, `gen/make_pcb.py` (shared blocks in `hardware/common/gen`).

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
