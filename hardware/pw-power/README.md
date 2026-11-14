# PW - Power board (under the slope, right, next to the battery bay)

All the power of the instrument: three inputs joined by ideal diodes, the rear On/Off switch, and every rail the boards need.
Research: `docs/ru/34_rear_boards_research.md` (section 5). Decisions: R36 (Mini-ITX, 19 V), R40/R59/R109 (battery),
R72 (DC 12-24 V with protection, USB-C PD), R110 (screen 5 V / 4 W), R118 (phantom), R145 (USB-C Power separate from the PC port).

**Status: rev 0.5 - schematic only** (188 parts). Rev 0.5: "to F1" has +5V for the relays. Rev 0.4 (14.11.2026, PC): INA226 powered from its own 3.3 V (AP2112K-3.3 from +5V), because its VIH = 0.7 x VS = 3.5 V at 5 V. Rev 0.3 (14.11.2026, PC): INA226 power monitor (R146). Rev 0.1 (14.11.2026, PC): values after the TI datasheet examples.
Rev 0.2 (14.11.2026, cloud, task #23): checked against the datasheets, table in `notes/handoff.md` (report #23). Still to measure
on the board: the LM5176 and LM5156H loops (compensation taken from TI examples for other outputs).

## Power tree

| Block | Part | From -> to | Notes |
|---|---|---|---|
| DC input | fuse 7 A, SMBJ28CA, LM74700 + CSD18540Q5B | DC jack 12-24 V -> BUS_IN | reverse polarity and ORing |
| USB-C Power | TPS25730D (C22438973), SMBJ22CA, LM74700 + FET | PD 15-20 V, 3 A operating / 5 A max -> BUS_IN | no I2C: ADCIN1 = 15 V min, ADCIN2 = 20 V max, ADCIN3 = 3 A, ADCIN4 = 5 A; VIN_3V3 to GND (VBUS-powered only); PPHV 47 uF polymer + ceramics |
| Battery | fuse 10 A, SMBJ20CA, LM74700 + FET | 4S 12.8-16.8 V -> BUS_IN | pack with its own BMS (R109); charger later (R40) |
| On/Off | rocker on the rear wall, >= 10 A DC | BUS_IN -> BUS_SW | mechanical master switch |
| Power monitor | INA226 (C49851, VS = 3.3 V from an AP2112K), shunt 5 mOhm 2512 | BUS_SW -> BUS | R146: whole input power, I2C 0x40 to P2 (LED limit); ALERT open drain |
| 19 V Mini-ITX | LM5176 four-switch buck-boost, 4 x CSD18540Q5B | BUS 12-24 V -> 19 V 5 A (95 W), 300 kHz | ASRock N100DC-ITX officially wants 19 V (doc 34); upgrades limited to 35-45 W (R36) |
| +5V_PANEL | TPS54560B (C1850354) | BUS -> 5 V 5 A | panel boards and LEDs; LED budget up to ~5.6 A white on full (doc 10): firmware limits brightness |
| +5V | TPS54560B | BUS -> 5 V 5 A | screen 4 W, R2, USB devices, logic of the audio boards |
| +-14 V | 2 x LMR33640 (buck, inverting buck-boost) | 19 V -> +14 V / -14 V | pre-regulators 1-2 V above the LDOs (doc 34) |
| +-12 V quiet | TPS7A4701 / TPS7A3301 | +-14 V -> +-12 V | TIDA-01458 scheme; TPS7A47: 4 uV rms, ANY-OUT 12.0 V |
| +48 V phantom | LM5156H boost + TPS7A4101 | 19 V -> 48.5 V -> 46.1 V, ~40 mA | two P48 channels (doc 34, 2.3; P48 = 44-52 V); TPS7A4101 input max 50 V, dropout <= 1.3 V; 100 V FET IRLML0100; switched per channel on R1 (R118) |

## Connectors

| J | To | Pins |
|---|---|---|
| DC in | DC jack on the wall (Micro-Fit 1x2) | DC_RAW, GND |
| USB-C Power in | USB-C receptacle on the wall (Micro-Fit 2x3) | VBUS x 2, GND x 2, CC1, CC2 |
| Battery | pack (Micro-Fit 2x2) | BAT x 2, GND x 2 |
| On/Off switch | rocker (Micro-Fit 1x2) | BUS_IN, BUS |
| 19 V to Mini-ITX | Micro-Fit 2x2 -> 5.5 x 2.5 plug | V19 x 2, GND x 2 |
| +5V panel | P2 hub (Micro-Fit 2x3) | +5V_PANEL x 3, GND x 3 |
| to R2 | JST PH 5 | +12V, GND, -12V, GND, +5V (as R2 J1) |
| to A1/R1 | Micro-Fit 2x5 | +12V, -12V, +5V x 2, +48V, GND x 5 |
| to F1 | JST PH 4 | +12V, GND, -12V, +5V (relay coils, F1 rev 0.1) |
| +5V screen | JST PH 2 | +5V, GND |
| I2C power monitor | JST PH 4 to P2 | SDA, SCL, ALERT, GND (pull-ups on P2) |

Budget (estimate, report #23): without LEDs 44-64 W out (Mini-ITX 25-45, screen 4, audio 10, phantom 2, logic 3) = 49-71 W in at
~90 %. LED room: PD 100 W -> 26-46 W; PD 65 W or DC 12 V (jack 5 A = 60 W) -> 0-15 W; DC 24 V (120 W) -> full. The firmware must
measures the input power (INA226, R146) and caps the LEDs. DC adapter 19-24 V; from 12 V only with dimmed LEDs (R147).

ERC notes: PWR_FLAG on the rails that only connectors and converter outputs drive (`PWR_FLAG_NETS`); in the KiCad-7 symbol
copies (`hardware/common/gen/sym7.py`, `PIN_TYPE`) the second OUT pin of the TPS7A4701 is passive and VOSNS of the LM5176 is
an input, so ERC does not see two power outputs or an output against the PWR_FLAG.

Checks: `tools/sch_netcheck.py hardware/pw-power` - rev 0.2: 178 symbol units, 543 pins, 0 mismatches; every symbol pin listed in
`design.py`. ERC by CI.

Generators: `gen/design.py`, `gen/make_sch.py`. On the PC set `KICAD_SYMBOL_DIR=<repo>/hardware/common/sym7`.

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
