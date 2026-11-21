# PW - Power board (rev 2.2, 21.11.2026; under the slope, right, next to the battery bay)

All the power of the instrument: three inputs joined by ideal diodes (LM74700), the rear On/Off switch, every rail the boards need. **100 x 100 mm, 4 layers, 345 parts, not routed.**
Decisions: R36, R40/R59/R109 (battery), R72, R110, R118, R145; P111 (3S packs), P116, P123-P129, P131, P132. Research: `docs/ru/34_rear_boards_research.md`, doc 43 (batteries).
**DO NOT ORDER** the PW board or the battery packs until a real 3S pack is checked (dimensions, capacity, UN38.3), its BMS threshold is confirmed and the 45 C cut-off is checked on a sample (doc 43).
Open: loops of the LM5176 and LM5156H (TI examples), bench check of the VBUS damper and of the quiescent currents behind the hold-up estimate, parts of the 470 uF storage and of the SS34 (technologist).

## Power tree

| Block | Part | From -> to | Notes |
|---|---|---|---|
| DC input | jack Switchcraft ST10U (10 A, IP67) -> Micro-Fit 2x2 (2 contacts + / 2 contacts -), fuse 5 A, SMBJ28CA, eFuse TPS26631 (OVP 22.9 V, 5.4 A), LM74700 + FET | DC jack 12-24 V -> EXT | reverse polarity, ORing |
| USB-C Power | connector -> TVS SMBJ20CA -> **2 x 47 uF 35 V Panasonic EEEFK1V470P in parallel (C178565, ESR 0.18 ohm), damper** -> **eFuse TPS26631 (UV 4.16 V, OV 22.55 V)** -> TPS25730D (VBUS) -> LM74700 -> EXT | PD 15-20 V, 3 A / 5 A | hot-plug peak about 21-24 V against the 28 V limit (tasks/11); TPS25730 soft start 3.3 V/ms limits the charge of the 101 uF at PP_HV |
| Batteries 1, 2 | Micro-Fit 2x3, fuse 10 A, SMBJ13CA, LM74700 + FET | 3S 9-12.6 V with BMS (BQ7791500) -> BUS_IN | BMS cut-off 3 x 2.9 V = 8.7 V |
| Chargers x 2 | BQ25798, 1 uH SPM6530, PROG 10.5k = 3S | EXT -> BAT | I2C 0x6B behind TCA9546A; firmware: re-write VREG 12.45 V after a watchdog reset |
| Monitor | INA226 (VS 3.3 V), 5 mOhm | BUS_SW -> BUS | ALERT limit **9.8 V = register 0x1EA0** (the LM5176 stops by itself at 9.3 V): "pack is running down", mutes the outputs |
| 19 V | LM5176 buck-boost, 4 x CSD18532Q5B | BUS 9.3-24 V -> 19 V 5 A | feeds +-14 V, phantom, 15 V, 12 V fan |
| +5V, +5V_PANEL | **2 x LM70660** (VQFN-29 6x6, forced PWM, DRSS, fixed 5 V, 400 kHz, shunt 6.8 mOhm = 8.2 A, L 4.7 uH, 4 x 47 uF) | BUS -> 5 V 6 A | EN divider 392k / 49.9k: start 8.86 V (8.4-9.3), stop 7.97 V; footprint RRX0029B read from the TI drawing |
| 15 V H5, 12 V fan | LMR33640 | 19 V -> 15 V / 12 V | 2 x 1k / 2 x 820 idle load (about 30 mA, P135) |
| +-14 V | 2 x LMR33640 (buck, inverting) | 19 V -> +-14 V (2 x 1k idle load each, 30 mA) | **hold-up storage**: 4 x 470 uF 25 V, 10 ohm + SS34 per rail, 0.94 mF per rail = 4.8-7.1 ms for 0.43-0.29 A (tasks/12); the 1000 uF output limit and the 4 ms soft start are met by the 10 ohm (1.4 A peak) |
| +-12 V quiet | TPS7A4701 / TPS7A3301 | +-14 V -> +-12 V | 4 uV rms |
| +48 V phantom | LM5156H + TPS7A4101 | 19 V -> 46.1 V, 40 mA | two channels switched on R1 |

## Connectors
DC in (Micro-Fit 2x2, ST10U), USB-C Power (Micro-Fit 2x3), Battery 1 and 2 (Micro-Fit 2x3), On/Off (1x2), 15 V to H5 (2x2), +5V panel (2x3), to R2 (JST PH 5), to A1/R1 (Micro-Fit 2x5), to F1 (JST PH 4), +5V screen (PH 2), power telemetry (PH 8: SDA, SCL, ALERT, CHG_INT, FAN_PWM, FAN_TACH, GND, CHG_EN), fan header 1x4.

## Checks (21.11.2026)
ERC 0, DRC 0 errors, schematic parity 0, board 100.1 x 100.1 mm, courtyard fill bottom 45 %, top 22 %, HF decoupling 20 of 22 within 2 mm (P116). Generators: `gen/design.py`, `gen/make_sch.py`, `gen/make_pcb.py` (`KICAD_SYMBOL_DIR=<repo>/hardware/common/sym7`); height `PW_H` (default 100).
Budget (estimate): 44-64 W without LEDs; LED room by the input source, firmware caps the LEDs from the INA226 (R146, R147).
License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
