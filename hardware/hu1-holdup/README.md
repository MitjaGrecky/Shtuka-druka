# HU1 - hold-up module for the +-14 V rails (P129, P130)

**Status: rev 0.1 (21.11.2026): schematic and placed board, 2 layers, 35 x 45 mm, ERC 0, DRC 0, parity 0; not routed (UNROUTED rule: 4 capacitors, 2 resistors, 2 diodes, one 3-pin connector).**
Next to PW on a harness <= 80 mm (the place in the enclosure: designer, P130). On a loss of all power the +-14 V rails keep the audio boards alive for >= 6 ms until the output relays have opened (tasks/12, tasks/13 of the team folder).

| Block | Parts | Notes |
|---|---|---|
| Storage | 4 x 470 uF 25 V aluminium electrolytic 10 x 10.5 mm (2 per rail) | 0.94 mF per rail: 4.8 ms at 0.43 A, 7.1 ms at 0.29 A (with the Schottky drop) |
| Inrush limit | 2 x 10 ohm 1206 (one per rail) | LMR33640: soft start 4 ms, low-side limit 3.9-5 A, total output capacitance <= about 1000 uF: 1.4 A peak instead of 3.5 A |
| Discharge path | 2 x SS34 (C8678) | the storage feeds the rail when it sags; drop 0.3-0.4 V |
| Connector | Micro-Fit 3.0 1x3 vertical (43650-0315, latching) | 1 P14, 2 GND, 3 N14; PW has the same connector "to HU1" |

Parts to select (technologist): the 470 uF electrolytic (25 V, 105 C, 10 x 10.5), SS34 availability. License: CERN-OHL-S-2.0 (hardware), AGPL-3.0 (code).
