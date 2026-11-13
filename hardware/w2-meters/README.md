# W2 - Meters (slope, above the track column)

Two level meters (master L and R), 14 RGB LEDs each, on two LP5864 drivers. No buttons, no knobs.
Spec: `hardware/for-routing/SPEC_boards.md`, section W2. Status: rev 0.1 - schematic and placed board, not routed (`UNROUTED`).
Package: `hardware/for-routing/W2/`.

| | |
|---|---|
| Board | 35 x 126 mm along the slope, 2 layers; panel x 355-390, slope s 12-138 mm from the fold (as W1) |
| Top side | 28 x XL-1615RGBC-RF: Meter L at panel x 364, Meter R at x 380; 14 per column over the meter length (120.1 mm along the slope, step 8.58 mm) |
| Bottom side | 2 x LP5864 between the columns (U1 L, U2 R), their capacitors, J1 at the front edge (towards the fold) |
| Bus | J1 2 x 7, 1.27 mm to P3 over the fold (I2C channel 3 of P3's TCA9546A, P99); SR_IN and SR_OUT tied (SR_THRU) |
| I2C | U1 0x40 (L), U2 0x41 (R) |
| LEDs | LED i (1 = bottom, fold side) of a meter: CS triple (i-1) div 4, SW (i-1) mod 4; CS12-17 unused (no-connect) |
| Holes | M2 in the corners and in the middle of both long sides |

Checks (13.11.2026, KiCad 10.0.8 on the PC): ERC 0 errors (3 warnings: ~INT, ~SR_LOAD, SR_CLK reach only the connector);
`check_netlist.py` 204 pins, 0 mismatches. DRC and parity: not run locally (kicad-cli crashes this PC, see notes/handoff.md) - CI runs them.

Generators: `gen/design.py`, `gen/make_sch.py` (shared grid writer), `gen/check_netlist.py`, `gen/make_pcb.py` (shared writers in `hardware/common/gen`).

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
