# BM - 3S pack protection (BQ7791500)

One board per pack, **2 per set** (doc `docs/ru/43_battery_power.md` 5c, P111). Low-side protection of a pack of 3 Jauch LP906090JH cells: TI **BQ7791500PWR** (variant 00 = 3S, OV 4.200 V), two CSD18532Q5B back to back, 5 mOhm sense, internal balancing, NTC. Status: **rev 0.2, placed board 38 x 38 mm, 2 layers, not routed** (`UNROUTED`). Package: `hardware/for-routing/BM/`.

| Part | Value / part | Note |
|---|---|---|
| U1 | BQ7791500PWR, TSSOP-24 (C2876946; Digikey 296-50995-1-ND) | symbol `ShtukaDruka:BQ77915` (pins from SLUSCU0L table 7-1) |
| Q1, Q2 | CSD18532Q5B (C882766, 2793 pcs at JLC; CSD18540Q5B is almost out of stock, doc 46) | Q1 DSG (source on the sense resistor), Q2 CHG (source on PACK_N); 2.5 mOhm at 10 V, 3.3 typ at 4.5 V, 3.2 max at 10 V |
| R (sense) | 5 mOhm 2512 1 % 3 W (C2903482) | OCD 60 mV = 12 A (9.6-14.4 A), SCD 120 mV = 24 A, 0.18 W at 6 A; the thresholds are taken across the shunt only, the FETs do not move them; FET loss 2 x 3.2 mOhm = 0.23 W at 6 A |
| cell inputs | 75 R + 100 nF per cell; VC5 = VC4 = VC3 on the top cell | balancing about 25 mA (doc 43) |
| supply | RVDD 1k, CVDD 1 uF, AVDD 1 uF | table 10-1 |
| others | OCDP 100k; TS: 103AT + 10k from VTB; PRES 10k up; CCFG, CBI to VSS; CTRC, CTRD, LPWR, CBO open; SRP/SRN 100 R + 100 nF; RDSG 4.53k, RCHG 1k, RGS 1M / 3.3M; RLD 470k | fig. 9-11, table 10-1 |

Connectors, all lying flat (rev 0.2, 11 mm bay): J1 PH 4 side entry (C157926) cell taps (B-, B1, B2, B+; sense only), J2 right-angle Micro-Fit 43650-0200 (C192562) cell power (cell 1 negative, cell 3 positive: the pack current), J3 and J4 PH 2 side entry (C173752) the NTC of the chip and the second NTC for PW (not in parallel), J5 right-angle Micro-Fit 43045-0600 2x3 (C127367, 38976 pcs at JLC) to PW: BAT+ x 2, GND x 2, NTC, GND (same pinout as PW 'Battery 1/2'). Both NTCs: 103AT 10k B 3435 on the middle cell, bought separately (Digikey), not on the board.

Decisions and open points:
- **RLD 470k** (datasheet table 10-1), doc 43 said 453k; **RDSG 4.53k** (table: 4.5k); CTRC/CTRD open as in fig. 9-11; RIN 75 R as doc 43 (the table's 1k would give about 4 mA of balancing).
- Rev 0.2: J5 and J2 are right-angle (opening towards the edge, turned 180 deg as in P2); check the opening direction against the 3D model when routing.
- Not checked: heating of the FETs and the sense resistor on the real board (0.23 W + 0.18 W at 6 A), the 45 C cut-off on a heated sample, the height in the pack bay model.
- Checks (PC, no kicad-cli): `sch_netcheck` 32 units, 94 pins, 0 mismatches; `ov.py` 0; `pcb_geomcheck` 0 problems. ERC/DRC: CI.

Generators: `gen/design.py`, `gen/make_sch.py`, `gen/make_pcb.py` (`KICAD_SYMBOL_DIR=<repo>/hardware/common/sym7`, `KICAD_FOOTPRINT_DIR=<KiCad>/share/kicad/footprints`).

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
