# PW - Power board (under the slope, right, next to the battery bay)

All the power of the instrument: three inputs joined by ideal diodes, the rear On/Off switch, and every rail the boards need.
Research: `docs/ru/34_rear_boards_research.md` (section 5). Decisions: R36 (Mini-ITX, 19 V), R40/R59/R109 (battery),
R72 (DC 12-20 V with protection, rev 1.1, USB-C PD), R110 (screen 5 V / 4 W), R118 (phantom), R145 (USB-C Power separate from the PC port).

**DO NOT ORDER the PW board or the battery packs** until a real 3S pack is checked (dimensions, capacity, UN38.3), its BMS threshold is confirmed, and the hardware 45 °C cut-off is checked on a sample (doc 43). **Status: rev 1.3 (20.11.2026 evening) — placed on the pin rule (A-037: decoupling <= 2 mm at 40 of 112, still open for PW), Freerouting 1.9 + In1 GND plane: 61 unrouted (13 non-GND), not routed to completion; changes in the Rev sections below (rev 1.0: 303 parts, 100 × 110 mm).** Packs: 3 × Jauch LP906090JH with a BQ7791500 BMS board each (doc 43, section 5в, P111). Chargers: BQ25798 ×2, PROG 10.5k = 3S. Pack TVS SMBJ13CA; LM5176 UVLO 10.1 / 9.3 V; bus 9–12.6 V from the packs. Earlier revisions (0.1–0.9, 4S packs) are in git history.
on the board: the LM5176 and LM5156H loops (compensation taken from TI examples for other outputs).

## Power tree

| Block | Part | From -> to | Notes |
|---|---|---|---|
| DC input | fuse 7 A, SMBJ28CA, LM74700 + CSD18540Q5B | DC jack 12-20 V -> BUS_IN | reverse polarity and ORing |
| USB-C Power | TPS25730D (C22438973), SMBJ22CA, LM74700 + FET | PD 15-20 V, 3 A operating / 5 A max -> BUS_IN | no I2C: ADCIN1 = 15 V min, ADCIN2 = 20 V max, ADCIN3 = 3 A, ADCIN4 = 5 A; VIN_3V3 to GND (VBUS-powered only); PPHV 47 uF polymer + ceramics |
| EXT | LM74700 + FET (IEXT), SMBJ24CA | DC / PD (highest) -> BUS_IN, and the two chargers | batteries never feed EXT |
| Battery 1 and 2 (rev 1.0) | each: Micro-Fit 2x3 (BAT+ x 2, GND x 2, NTC, GND), fuse 10 A, SMBJ13CA, LM74700 + FET | 3S 9-12.6 V pack with its own BMS (BQ7791500) -> BUS_IN | R183, P111, doc 43 5c |
| Charger x 2 (rev 0.8) | BQ25798 (C2876593), 1 uH TDK SPM6530 (C87572), PROG 10.5k = 3S / 1.5 MHz (host: VREG 12.45 V) | EXT -> BAT of each pack (charger-only; SYS pin has only its capacitors) | I2C 0x6B behind TCA9546A (0x70); NTC on TS, RT1 9.31k only: charge stops at 45 C in hardware; CE enabled only by CHG_EN and +3V3 (switch on); ILIM ceiling 3.0 A |
| 12 V fan (rev 0.8) | LMR33640 (same stage as 15 V) | V19 -> 12 V | 4-pin fan header 2.54 mm; PWM 3.3 V / tach through the telemetry harness |
| On/Off | rocker on the rear wall, >= 10 A DC | BUS_IN -> BUS_SW | mechanical master switch |
| Power monitor | INA226 (C49851, VS = 3.3 V from an AP2112K), shunt 5 mOhm 2512 | BUS_SW -> BUS | R146: whole input power, I2C 0x40 to P2 (LED limit); ALERT open drain |
| 19 V internal rail | LM5176 four-switch buck-boost, 4 x CSD18540Q5B | BUS 9.3-24 V (UVLO 10.1 V start / 9.3 V stop, rev 1.0) -> 19 V 5 A (95 W), 300 kHz | feeds +-14 V, the phantom and the 15 V stage; no longer goes out of the board (R151) |
| 15 V ODROID-H5 | LMR33640 buck (same part as the 14 V stages) | 19 V -> 15 V, 4 A part for 1.7 A peak | ODROID-H5 window 11-20 V, Hardkernel recommends 15 V / 4 A (R149, R151) |
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
| Battery 1, 2 | pack (Micro-Fit 2x3), 150-250 mm | BAT x 2, GND x 2, NTC, GND |
| On/Off switch | rocker (Micro-Fit 1x2) | BUS_IN, BUS |
| 15 V to H5 | Micro-Fit 2x2 -> 5.5 x 2.1 plug, centre positive | V15 x 2, GND x 2 |
| +5V panel | P2 hub (Micro-Fit 2x3) | +5V_PANEL x 3, GND x 3 |
| to R2 | JST PH 5 | +12V, GND, -12V, GND, +5V (as R2 J1) |
| to A1/R1 | Micro-Fit 2x5 | +12V, -12V, +5V x 2, +48V, GND x 5 |
| to F1 | JST PH 4 | +12V, GND, -12V, +5V (relay coils, F1) |
| +5V screen | JST PH 2 | +5V, GND |
| Power telemetry | JST PH 8 to P2 | SDA, SCL, ALERT, CHG_INT, FAN_PWM (in), FAN_TACH (out), GND, CHG_EN (in; pull-down 100k) (pull-ups on P2) |
| Fan 12 V PWM | header 1x4, 2.54 mm | GND, +12 V, tach, PWM (PC fan pinout) |

Budget (estimate, report #23): without LEDs 44-64 W out (Mini-ITX 25-45, screen 4, audio 10, phantom 2, logic 3) = 49-71 W in at
~90 %. LED room: PD 100 W -> 26-46 W; PD 65 W or DC 12 V (jack 5 A = 60 W) -> 0-15 W; DC 24 V (120 W) -> full. The firmware must
measures the input power (INA226, R146) and caps the LEDs. DC adapter 19-24 V; from 12 V only with dimmed LEDs (R147).

ERC notes: PWR_FLAG on the rails that only connectors and converter outputs drive (`PWR_FLAG_NETS`); in the KiCad-7 symbol
copies (`hardware/common/gen/sym7.py`, `PIN_TYPE`) the second OUT pin of the TPS7A4701 is passive and VOSNS of the LM5176 is
an input, so ERC does not see two power outputs or an output against the PWR_FLAG.

Checks: `tools/sch_netcheck.py hardware/pw-power` - rev 0.9 (rev 1.0 the same): 303 symbol units, 911 pins, 0 mismatches; every symbol pin listed in
`design.py`. ERC by CI.

Generators: `gen/design.py`, `gen/make_sch.py`. On the PC set `KICAD_SYMBOL_DIR=<repo>/hardware/common/sym7`.

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).

## Rev 0.6: placed board for routing (14.11.2026, PC)
Placed board (no routing) generated by `gen/make_pcb.py`; `UNROUTED` marker for CI; package `hardware/for-routing/PW`. Placement is a starting point: the rest by `hardware/common/gen/autoplace.py` (ICs on a grid, small parts around the IC they share signals with, cable headers along the bottom edge). Outline and mounting holes are rough until the enclosure is fixed. `pcb_geomcheck`: 0 problems.

Low case (17.11.2026): bottom side has 4 x CP 10 x 10.5 electrolytics and 10 x 10 mm inductors, so the board needs standoffs of about 11 mm (not 3 mm); the board top is then at about 25 mm, mated vertical Micro-Fit plugs reach about 33 mm. Battery: J3 (Micro-Fit 2 x 2) takes a harness of about 150 mm from the pack under A1 (35 mm to the left); fan connector: see rev 0.8 below. Right-angle Micro-Fit connectors are the fallback if the plugs touch the screen cable bend.

## Rev 0.8 / 0.9: batteries, chargers, fan (18.11.2026, PC)
Doc `docs/ru/43_battery_power.md`: path A (pack with BMS + charger on PW), two independent channels, 'engineer's choice P109', not confirmed. Checks (rev 0.9): `sch_netcheck` 303 units, 911 pins, 0 mismatches; 0 overlaps; `pcb_geomcheck` 0 problems; EasyEDA `PW_v8`: 300 / 300 parts, 160 / 160 nets, LCSC 77, saved. Board 100 x 110 mm (was 100 x 80): check in the enclosure model. Not checked: BQ25798 with no load on SYS (not in the datasheet), routing (1.5 MHz loops), the actual packs (none bought), the 45 C cut-off by the TS divider needs a heated sample (B-model estimate 44.4-45.7 C). NOISY_XY in `design.py` is keyed by references: re-check after adding parts.

## Rev 1.0: 3S packs (18.11.2026, engineer, P111)
Doc 43 section 5c. Changed in `gen/design.py` only values and notes (303 parts, 163 nets, same placement and board size, so the enclosure model is unchanged): charger PROG 17.4k -> 10.5k (3S), pack TVS SMBJ20CA -> SMBJ13CA (C132568; BAT pin limit 20 V), LM5176 UVLO divider 34.8k -> 32.4k, On/Off rocker >= 15 A. The BMS board (BQ7791500PWR, C2876946; 2 x CSD18540Q5B, 5 mOhm shunt; about 35 x 28 mm) is specified in doc 43 5c and is not yet in CAD. Not checked: the cell-PCM series connection (Jauch datasheet is silent), the 45 C cut-off on a heated sample, routing.

## Rev 1.1: audit fixes (18.11.2026)
Audit `notes/reviews/schematics_2026-11-18.md`: EXT clamp SMBJ24CA (38.9 V at 15 A) and USB-C VBUS clamp SMBJ22CA (35 V) -> **SMBJ20CA** (Littelfuse C151258, 9636 pcs at JLC): BQ25798 VBUS is 30 V absolute / 24 V recommended, TPS25730 VBUS 28 V absolute (TI recommends breakdown between 22 and 28 V; TVS2200 has 2 pcs at JLC). **The DC adapter is 12-20 V** (19 V standard), not 24 V.
Firmware: the BQ25798 watchdog reset returns VREG to 12.6 V (3S POR) = the BMS OV threshold: re-write VREG 12.45 V after every reset or disable the watchdog. The LM5176 UVLO spread (datasheet 1.17-1.29 V, 2.15-4.25 uA) gives stop 8.4-10.4 V: the battery cut-off is also set in firmware (INA226). The telemetry harness PH 8 has all seven signals + one GND (twist GND with SCL, 100 R already in FAN_PWM); the P2 end must carry the same eight pins (P2 rev 0.x has only a 4-pin connector: SDA, SCL, ALERT, GND).

EasyEDA (18.11.2026, PC, rev 1.1): project `PW_v11`: PCB and schematic parts 303 / 303, nets 163 / 163, LCSC numbers written (79) and re-checked, positions 303 / 303 against KiCad, saved. No kicad-cli; DRC and parity left to CI.

## Rev 1.2 (19.11.2026): DC input eFuse, FETs, switch connector
- **A-025 (audit 3):** the TVS SMBJ20CA on EXT clamps about 28 V at 3 A and 32 V at 18 A, the chargers' VBUS/VAC are 30 V absolute (24 V recommended). The DC branch now has an eFuse **TPS26631RGER** (C1850273, 314 pcs at JLC; 60 V rated) between DC_F and the ideal diode IDC: OVP 22.9 V (R1 453k, R2 35.7k, R3 27k; 21.8-24 V over tolerance), UVLO 9.9 V, current limit 5.4 A (RILIM 3.32k), dVdT 10 nF, MODE to GND (auto-retry), SHDN 220k + 3.3 V zener (BZT52C3V3). Details and formulas: doc 43 section 6 (z). The PD path stays 15-20 V (TPS25730 and its SMBJ20CA).
- FETs CSD18540Q5B -> **CSD18532Q5B** (C882766), pack TVS C132568 -> C224008, green LEDs NCD0603G1 (C84267); L4, L5 stay Bourns SRP1038CC-8R2M (bought at Digikey).
- DC fuse 7 A -> **5 A** (the wall jack Switchcraft 721A is 5 A). **On/Off switch connector: Micro-Fit 2x2** (43045-0412, housing 43025-0400): the 10.2 A peak is split over two contacts per side (Carling 2GK51-73, both poles in parallel); the 1x2 carried 10 A on one contact.
- Harness check (notes/harness_bom.md): J1 DC (43645-0200, 20 AWG, 5 A), J2 USB-C PD from U1 (43025-0600), J5 switch (43025-0400, 4 wires), battery J3/J4 6 A over two contacts: nothing is above the contact ratings after the changes.

EasyEDA (20.11.2026): PW 1.2 = PW_v12: детали 313/313, цепи 169/169, LCSC (схема 84, PCB 84), позиции 313/313, сохранено.

## Rev 1.3 (20.11.2026): placement rule template
Courtyard gap 1.2 mm (ic_gap 1.8 mm around fine-pitch ICs) instead of 0.25 mm, the largest that fits the outline (autoplace.fit); basis: notes/placement_analysis_2026-11-20.md. Schematic unchanged.
