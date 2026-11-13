# W3 - System (slope, right column)

Save and Project buttons (2 RGB each, P84), the record light for the USB-A + SD pocket, one LP5864 and one 74HC165.
Spec: `hardware/for-routing/SPEC_boards.md`, section W3. Status: rev 0.1 - schematic and placed board, not routed (`UNROUTED`).
Package: `hardware/for-routing/W3/`.

| | |
|---|---|
| Board | 92 x 48.2 mm along the slope, 2 layers; panel x 413-505, slope s 12-60.2 mm (from the fold up to 1 mm before the pocket) |
| Top side | Save (panel x 435) and Project (x 483) at y 323: TS-1187A (C318884) with XL-1615RGBC-RF 6.5 mm left and right; record light D5 at the rear edge, x 459 |
| Bottom side | LP5864 (U1), 74HC165 (U2), 4x10k pack, passives; J1 at the front edge at x 60 (beside the front middle hole) |
| Bus | J1 2 x 7, 1.27 mm to P4 over the fold (I2C channel 1 of P4's TCA9546A, P99); chain P4 buttons -> W3 |
| I2C | LP5864 0x40 |
| LEDs | D1 Save left, D2 Save right, D3 Project left, D4 Project right, D5 record; LED i: CS triple i div 4, SW i mod 4 (CS0-5 used) |
| Shift chain | D7 Save, D6 Project, D5-D0 = 1; DS <- SR_IN (R3 10k) |
| Not on this board | USB-A + SD pocket (retail module, P105: only its cut-out next to this board); **Power button** (behind the pocket; V9, user 13.11: a panel button on a wire straight to the Mini-ITX PWR_SW header, no board) |
| Holes | M2 in the corners, one more on each long side (x 40 rear, x 30 front) |

Why the board ends at the pocket: the pocket (92 x 24 mm in the top view) is as wide as the whole column, so a single board
with a cut-out for it would fall into two pieces. Power state is not read by the module (the spec leaves it to the executor):
the Mini-ITX board sees the button directly.

Checks (13.11.2026, PC): EasyEDA Pro import (project W3_v1): PCB 22/22 and schematic 22/22 nets, 27/27 parts, against a
reference netlist written from `design.py` (`tools/pack_easyeda.py --no-cli`). ERC, DRC, parity: CI (kicad-cli crashes this PC).
`schematic.pdf` and `outline.dxf` of the package: not made yet (need kicad-cli).

Generators: `gen/design.py`, `gen/make_sch.py`, `gen/check_netlist.py`, `gen/make_pcb.py` (shared writers in `hardware/common/gen`).

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
