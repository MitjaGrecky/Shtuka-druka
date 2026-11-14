# R2b - Jack shelf under R2 (rear wall, right part)

A horizontal board at the bottom of the rear wall under the vertical control board R2 (R139). It carries the right-angle jacks
that would face sideways on a vertical board: MIDI DIN 2 in / 4 out, the rear USB-C to a computer, the rear USB-A, and the
power jacks (USB-C PD 5 A, DC 12-24 V). All parts are soldered at the factory.
Decisions: R139 (shelf), R140 (rear panel v1 as the base). Research: `docs/ru/34_rear_boards_research.md`, handoff #20.

**Status: rev 0.1 - schematic only** (18 parts, 25 nets, 14.11.2026). Outline and jack positions follow the rear panel v2.

| Block | Parts | Goes to |
|---|---|---|
| MIDI DIN | 6 x CUI SDS-50J (C6216157, right angle; footprint drawn with the board) | 2x7 comb to R2: out 1-4 pins 4/5, in 1-2 pins 4/5, GND x 2. The CA-033 resistors and the TLP2361 optos stay on R2 |
| Rear USB-C (PC) | HRO TYPE-C-31-M-12 (C165948), 5.1k Rd x 2, USBLC6-2SC6 | Cable (JST PH 4) to A1 port B (ADuM4166 side of the PC), not through R2 |
| Rear USB-A | Molex 67643, USBLC6-2SC6 | Cable (JST PH 4) to a Mini-ITX USB header (R80) |
| USB-C PD | GCT USB4105-GF-A-060 (C3025063), 5 A 20 V (task #20) | 2x5 header to PW (VBUS, CC1, CC2; the PD sink TPS25730 is on PW) |
| DC 12-24 V | Locking right-angle jack, 5 A - **to choose** (CUI PJ-063AH footprint is a placeholder) | Same 2x5 header to PW |

Comb pinout (same numbers on R2, `R2B_COMB` in `hardware/r2-control/gen/design.py`): 1-8 = MIDI OUT 1-4 pins 4, 5;
9-12 = MIDI IN 1-2 pins 4, 5; 13, 14 = GND. R2b has a vertical 2x7 header, R2 a right-angle 2x7 socket; the exact
mechanics (height of R2 above the shelf, which side the comb sits) is settled with the board.

Jack positions (rear view, x from the left as seen from behind, z from the bottom): see the table in `hardware/r2-control/README.md`
and `docs/ru/img/rear_panel_v2.png`. Shelf jacks in one row at z 18: DC x 12, USB-C PD x 30, USB-C PC x 48, USB-A x 67,
MIDI IN 1-2 x 92, 115, MIDI OUT 1-4 x 140-209 (pitch 23).

To do with the board: DIN-5 footprint (EasyEDA CONN-TH_SDS-50J), locking DC jack 5 A, current through the 2x5 (2 pins per rail),
shield and chassis ground of the jacks.

Checks: `tools/sch_netcheck.py hardware/r2b-jacks` - 18 symbol units, 118 pins, 0 mismatches against `design.py`; ERC by CI.

Generators: `gen/design.py`, `gen/make_sch.py` (shared writer `hardware/common/gen/module_sch.py`). On the PC set
`KICAD_SYMBOL_DIR=<repo>/hardware/common/sym7` (built by `python hardware/common/gen/sym7.py`).

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
