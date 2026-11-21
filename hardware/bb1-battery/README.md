# BB1 - battery board (rev 0.3, 21.11.2026; P143, P144, P146)

One long board, **398 x 28 mm, 2 layers, 2 oz copper, 70 parts, 58 nets**, along the ends of the three cell blocks under the pads (model x 104-502, y 156-184, z 3-14; 3 mm standoffs). It replaces the BM boards 38 x 38 mm.
**Schematic and placed board; not routed** (`UNROUTED`). ERC 0, DRC 0 errors, parity 0. Positions: `model3d/batt_bays/under_pads.csv` (P144); board x = model x - 104, y = model y - 156.

| Block | Parts | Notes |
|---|---|---|
| 6 cells | **solder pads** for the two wires of each Ampul cell (WirePads_2x_THT: 4.2 mm pads, 1.6 mm holes, 8 mm pitch, two 3 mm holes for a cable tie), pad 1 +, pad 2 - | x 52.5, 77.5, 186.5, 211.5, 320.5, 345.5 (block centres 65, 199, 333 +- 12.5; y 7); >= 1.0 mm2 wire, 5 A per track; pack A = blocks 1, 2, 3 first cells in series, pack B the second cells; no power connectors (P146) |
| 2 protections | BQ7791500 + 2 x CSD18532Q5B + 5 mOhm + balancing, the circuit of `bm-bms3s` (25 parts each, nets suffixed _A / _B) | between the cell connectors (x 112 and 266): OV 4.2 V, UV 2.9 V, OCD 12 A, OTC 45 C |
| 2 outputs to PW | Micro-Fit 43045-0600 2x3 (C127367), J7 pack A, J8 pack B | BAT+ x 2, GND x 2, NTC, GND = PW Battery 1 / 2; x 150 and 250 |
| 4 NTC sockets | JST GH-class 1.25 mm latching, 2 pins (BM02B-GHS-TBT footprint; series by the technologist), 103AT 10k | J9 chip A, J10 chip B (TS), J11, J12 for the chargers of PW (separate thermistors) |
| 8 mounting holes | M3 | assumed: ends and ribs (x 4, 132, 266, 394, on the ribs); the csv has no holes |

8 A (1C of an 8 Ah cell): tracks on 2 oz copper **>= 3 mm** (IPC-2152) at routing; the 4 nets of each pack and PACK_N run the length of the board, use both layers.
Open: the 4th NTC (the order said 3), holes with the designer, GH or ZH series (technologist), routing. License: CERN-OHL-S-2.0, AGPL-3.0-or-later.
