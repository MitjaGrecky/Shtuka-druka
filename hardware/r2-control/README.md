# R2 - Control board (rear wall, right part)

The RP2350 of the control board (R85) with everything that is not audio at the rear wall: MIDI, CV/Gate, sync, the internal
USB hub and the control lines to the audio boards. DIN, USB, LAN and DC are panel parts on nuts with cables (R141).
Research and decisions: `docs/ru/34_rear_boards_research.md`, R118, R135-R143. Map of boards: `docs/ru/29_board_map.md`.

**Status: rev 1.1 (19.11.2026) - schematic and placed board, not routed; rectangle 110 x 99 without the low arm, see the end of this file. Earlier:** (234 parts, 4 layers; 14.11.2026; rev 0.5 = ATT1/ATT2 and the 74HC595, task #25; rev 0.6 = 7 x M3 mounting holes). Rear wall = the 3D model
of panel v7 (R142). MIDI DIN, USB, LAN and DC are panel parts on nuts with short cables (R141, the shelf R2b of rev 0.3 is
dropped): R2 carries the twenty 3.5 mm jacks and six JST PH headers for the DIN cables. Outline: the Control block, rear
x 156-266, z 10-113, a rectangle 110 x 103 mm (rev 0.9).

| Block | Parts | Notes |
|---|---|---|
| MCU | RP2350A (C42411118), W25Q128JVSIQ (C97521, 16 MB QSPI), 12 MHz ABM8-272-T3 (C20625731), core regulator with 3.3 uH AOTA-B201610S3R3 (C42411119), BOOTSEL button | As Raspberry Pi's minimal design (Hardware design with RP2350) |
| USB hub | USB2514B (C220679), 24 MHz X322524MOB4SI (C70590) | Up: ODROID-H5 24-pin header (pins 1, 2, 3, 5; doc 35 sec. 2a). Down: 1 RP2350, 2 panel P2 (R86), 3 A1 port A (R82), 4 spare. Straps low by the internal pull-downs = default configuration |
| MIDI DIN | 2 in (TLP2361 at 3.3 V), 4 out; sockets on the wall, one cable each to a JST PH header (out: 3 pins 4, 5, shield; in: 2 pins 4, 5) | CA-033 3.3 V: 33 R 0.5 W + 10 R per output; every output has its own port (R34). Any MIDI output (DIN 1-4, TRS O1/O2) can be **Thru** from In 1 or In 2, set in the menu: the RP2350 PIO copies the input bit by bit (microseconds, no CPU); no Thru labels on the panel, R144 |
| MIDI TRS | 1 in, 2 out: stereo Hroparts PJ-3920-3A (C707259, R143) | Out: tip and ring each from a GPIO through 22 R - type A/B is swapped in firmware (R32). In: two optos back to back, type A and B both work |
| CV/Gate out 1-8 | 2 x DAC80504RTET (C2862796; internal 2.5 V ref divided by 2, gain 2 = 0-2.5 V), 3 x OPA4197 (C2057327) on +-12 V | Vout = 8.06 (Vdac - 1.25 V) = -10.1 ... +10.1 V around a buffered REF/2; reset to mid-scale = 0 V; 1k output resistors. Step 0.31 mV = 0.37 cent at 1 V/oct |
| CV in 1-4 | RP2350 ADC0-3 | -10 ... +10 V -> 0 ... 3.03 V (100k / 33k to 3.3 V / 39k to GND), BAT54S clamp |
| Sync | 3 out, 2 in | Out: GPIO -> op-amp x1.51 -> 0 / +5 V. In: NPN inverter, 22k / 100k, negative clamp |
| To A1/R1 (2x7) | PH48_1, PH48_2, PHONO, MUTE, R2_OK, ATT1, ATT2 (pins 1, 3, 5, 7, 9, 11, 13; even pins GND) | Pulled low while booting; the output relays (R137) open when R2 stops; ATT1/ATT2 = -12 dB relay attenuators of Mic/Line 1-2 on R1 rev 0.3 |
| Output expander | 74HC595 (C5947) on the DAC SPI clock and data, latch GPIO 23, /OE GPIO 24 | QA PH48_1, QB PH48_2, QC PHONO, QD ATT1, QE ATT2, QF-QH spare. All 30 GPIO were in use, so the slow static lines moved here. /OE is pulled high: outputs are high-Z and the 100k pull-downs hold the lines low until the firmware loads zeros and enables them; DAC traffic only shifts the register, outputs change on the latch |

GPIO map (29 used, GPIO 25 free): 0-3 MIDI TX 1-4, 4-5 MIDI RX 1-2, 6-9 TRS out 1-2 tip/ring, 10-11 TRS in A/B, 12 MUTE,
13 R2_OK (+ status LED), 14-17 DAC SCK, SDI, CS1, CS2, 18-20 clock out 1, 2, reset/run out, 21-22 clock in, reset/run in,
23 expander latch, 24 expander /OE, 25 free, 26-29 CV in 1-4 (phantom 1-2, phono/line, ATT 1-2 on the 74HC595).

Datasheet check (rev 0.2, 14.11.2026; table in `notes/handoff.md`, report #20): RP2350 per the minimal design; DAC80504 GAIN high = x2,
RSTSEL high = mid-scale, **REFDIV high** (with the internal 2.5 V reference undivided the DAC needs VDD >= 5.0 V and raises a
reference alarm, all outputs 0 V, below that); USB2514B straps by the internal pull-downs, CRFILT/PLLFILT 100 nF, VBUS_DET 100k/100k.
Still without an LCSC number: the 0.1 % resistors (10k, 80.6k), the 1206 33 R 0.5 W, the passives in general (chosen at the BOM).

Board (`gen/make_pcb.py`): F side (jacks only) faces the rear wall; seen from behind, board x = rear x - 88, y = 113 - z.
Jacks at the model positions (axis 0.78 mm below the pad-field centre for the PJ398SM, 1.29 mm for the PJ-3920-3A). On the B side
(inside): the DIN cable headers along the window edge, power/USB/A1/SWD headers along the right edge, the ICs and the parts of
each channel packed next to their IC or jack (`hardware/common/gen/packer.py`). BOOTSEL is on the B side.
MIDI TRS: stereo **PJ-3920-3A** from JLC stock (R143) - pin 1 sleeve, 2 tip, 3 ring per the Flux library: **check the sleeve on a
sample** (tip and ring are swapped in firmware anyway, R32). Mono jacks: PJ398SM on the AudioJack2_SwitchT symbol (S, T, TN).
Panel DIN sockets at a 22 mm pitch (model): pick a panel DIN whose flange fits (e.g. round-flange types), with the enclosure.
Mounting (rev 0.6, proposal to settle with the enclosure): 7 x M3 (3.2 mm, ISO 7380 head keep-out) on standoffs to the rear wall, board
coordinates (x, y): (80, 4), (162, 4), (171, 99), (4, 99) at the corners, (23, 79) in the bottom strip between the TRS jacks, (126.5, 56) and
(92.5, 34) inside, in the 7.5 mm gaps between the jack columns and rows. The jacks' own nuts carry the plug force into the wall; the standoffs hold the
board against flexing and the cable pull of the DIN and header connectors. Before this the board had no holes at all.
Geometry without kicad-cli: `tools/pcb_geomcheck.py hardware/r2-control/r2-control.kicad_pcb` - 0 problems; pins = pads.

Checks: `tools/sch_netcheck.py hardware/r2-control` - rev 0.5 (14.11.2026, PC): 239 symbol units, 707 pins, 0 mismatches against
`design.py`; ERC by CI.


## Rear panel jacks (v3 = 3D model of panel v7, R142)

Sketch: `docs/ru/img/rear_panel_v3.png` / `.svg` (generator `tools/rear_panel.py`; v1, v2 kept). Rear view: x from the left edge as
seen from behind, z from the bottom of the 143 mm rear wall (R44). Inputs framed, outputs filled (R26); labels in English (R45).
Board "panel" = parts on nuts with a cable (R141); "R2" = on this board.

| Jack | Board | Zone | Kind | x (rear view) | z | Panel x | Direction |
|---|---|---|---|---|---|---|---|
| LAN | panel | POWER / USB | lan | 20 | 78 | 495 | io |
| USB-A | panel | POWER / USB | usba | 40 | 80 | 475 | io |
| USB-C (PC) | panel | POWER / USB | usbc | 62 | 80 | 453 | io |
| DC 12-24V | panel | POWER / USB | dc | 22 | 40 | 493 | in |
| ON/OFF | panel | POWER / USB | onoff | 52 | 40 | 463 | in |
| MIDI IN 1 | panel | CONTROL | din | 100 | 82 | 415 | in |
| MIDI OUT 1 | panel | CONTROL | din | 122 | 82 | 393 | out |
| MIDI OUT 3 | panel | CONTROL | din | 144 | 82 | 371 | out |
| MIDI IN 2 | panel | CONTROL | din | 100 | 52 | 415 | in |
| MIDI OUT 2 | panel | CONTROL | din | 122 | 52 | 393 | out |
| MIDI OUT 4 | panel | CONTROL | din | 144 | 52 | 371 | out |
| TRS IN | R2 | CONTROL | mini3 | 100 | 22 | 415 | in |
| TRS OUT 1 | R2 | CONTROL | mini3 | 122 | 22 | 393 | out |
| TRS OUT 2 | R2 | CONTROL | mini3 | 144 | 22 | 371 | out |
| CLK OUT 1 | R2 | CONTROL | mini | 172 | 90 | 343 | out |
| CLK OUT 2 | R2 | CONTROL | mini | 189 | 90 | 326 | out |
| RESET OUT | R2 | CONTROL | mini | 206 | 90 | 309 | out |
| CLK IN | R2 | CONTROL | mini | 223 | 90 | 292 | in |
| RESET IN | R2 | CONTROL | mini | 240 | 90 | 275 | in |
| CV IN 1 | R2 | CONTROL | mini | 172 | 68 | 343 | in |
| CV IN 2 | R2 | CONTROL | mini | 189 | 68 | 326 | in |
| CV IN 3 | R2 | CONTROL | mini | 206 | 68 | 309 | in |
| CV IN 4 | R2 | CONTROL | mini | 223 | 68 | 292 | in |
| CV OUT 1 | R2 | CONTROL | mini | 172 | 46 | 343 | out |
| CV OUT 2 | R2 | CONTROL | mini | 189 | 46 | 326 | out |
| CV OUT 3 | R2 | CONTROL | mini | 206 | 46 | 309 | out |
| CV OUT 4 | R2 | CONTROL | mini | 223 | 46 | 292 | out |
| CV OUT 5 | R2 | CONTROL | mini | 172 | 24 | 343 | out |
| CV OUT 6 | R2 | CONTROL | mini | 189 | 24 | 326 | out |
| CV OUT 7 | R2 | CONTROL | mini | 206 | 24 | 309 | out |
| CV OUT 8 | R2 | CONTROL | mini | 223 | 24 | 292 | out |

Generators: `gen/design.py`, `gen/make_sch.py` (shared writer `hardware/common/gen/module_sch.py`, multi-unit symbols placed unit by unit).

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).

Rev 0.7 (17.11.2026, R178): rectangle 107 x 103 mm (rear x 156-263, z 10-113): the low arm under the DIN window is gone (the H5 sits in the rear right corner, x 376-496). The six DIN sockets move to the rear wall above the H5 (x 376-510, z 70-110) on nuts with cables to the six JST headers on the left edge of R2; the three MIDI TRS jacks take the free 5th column of the CV block (x_rear 240, z 68 / 46 / 24). Generator: `X0` = 156, `OUTLINE` rectangle, `AREAS` one rectangle, holes shifted by -68. Placement: 0 courtyard overlaps, nothing outside the outline, netcheck 707 pins / 0 mismatches. The rear wall layout (v4) has to follow: this is the doc 41 task T-2.

Rev 0.8 (18.11.2026, rear wall v5 by the designer, the user rejected v4): board 110 x 103 mm (rear x 156-266). The three MIDI TRS jacks are in the MIDI block, the left column of R2 (x_rear 166, z 96 / 74 / 52); the Sync row at z 96 (x_rear 186 / 204 / 222 / 240 / 258); CV In z 70, CV Out z 48 and 26 on the columns x_rear 195 / 213 / 231 / 249 (18 mm pitch). The DIN sockets (2 x 3) and the Power / USB / LAN groups are panel parts on nuts on the wall above the H5 and at the right corner (doc 41 section 24); R2 keeps the six JST headers for the DIN cables on the left edge. Mounting hole H5 moved to (48, 53). 0 courtyard overlaps, nothing outside the outline, netcheck 707 pins / 0 mismatches. EasyEDA not verified for rev 0.8.

Rev 0.9 (18.11.2026, rear wall v6, doc 41 section 24.4): jack axes on the grid rows z 99 / 73 / 47 / 21 (rear x = r). MIDI TRS In / Out 1 / Out 2 on r 167 (z 99 / 73 / 47); Sync row z 99 (Clock 1, Clock 2, Reset, Clk In, Rst In at r 190 / 207 / 224 / 241 / 258); CV on r 190 / 207 / 224 / 241: CV In 1-4 z 73, CV Out 1-4 z 47, CV Out 5-8 z 21. Outline (110 x 103, rear x 156-266, z 10-113) unchanged. The Power block is not on R2 (wall edge r 3-28, cable to PW). EasyEDA not verified for rev 0.9.

## Rev 1.0: audit fixes (18.11.2026)
Audit `notes/reviews/schematics_2026-11-18.md`. (1) The three downstream USB ports with a cable (P2, A1 port A, spare) took +5V straight from PW with OCS_N tied high: a short in a cable pulled the +5V of the screen, R2 and A1 down. Each now has a **TPS2051B** (C24593, SOT-23-5, 0.75-1.25 A limit, 49473 pcs at JLC): IN +5V, EN = hub PRTPWR2/3/4 (pins 16/18/20, 100k pull-down because the pin is also the BC_EN strap), OC -> hub OCS_N2/3/4 (pins 17/19/21), OUT -> port VBUS with 2 x 22 uF. OCS_N1 (port 1 = the RP2350) keeps its pull-up. Pins from USB2514B DS00001692 (QFN36). New symbol `ShtukaDruka:TPS2051B` (in `ic_symbols.py`, appended to `m1-screen-knobs/lib/ShtukaDruka.kicad_sym`). (2) DAC80504 REF capacitors 100 nF -> 220 nF (datasheet 8.3.2: 150 nF minimum). Not changed: the CV-input divider from +3V3 versus the ADC reference (ADC_AVDD), about 6 mV on 10 V.

EasyEDA (18.11.2026, PC, rev 1.0): project `R2_v7` imported; LCSC numbers written (sch 158, pcb 146), positions 248 / 248 against KiCad, saved. The parts / nets summary line was not captured and the project could not be reopened afterwards (bridge timeout): repeat `eda_check.py R2 --project R2_v7`.

EasyEDA (19.11.2026): R2 1.0 = R2_v7: детали 248/248, цепи 170/170, LCSC, позиции 248/248, сохранено.

Rev 1.1 (19.11.2026, rear wall v6.1, `docs/ru/img/41_rear_v6_1_jacks.csv`, doc 41 section 24): rows -4 to z 95 / 69 / 43 / 17 (x unchanged). Outline 110 x 99 (rear x 156-266, z 10-109): the top edge goes down by 4 with the rows (`Z0` = 109, `H` = 99), the bottom stays z 10; the two lower holes moved to y 95. Fit model (`R2_TOP` = 109): 0 collisions. EasyEDA not verified for rev 1.1.

EasyEDA (19.11.2026): R2 1.2 = R2_v8: детали 248/248, цепи 170/170, LCSC (схема 158, PCB 146), сохранено через API. Позиции не сверяли. eda_verify: 172 расхождения только в поле Value (в EasyEDA 1u вместо 100n у конденсаторов C1525), LCSC совпадают.

## Rev 1.3 (19.11.2026): rear wall harness
The wall USB-A (Neutrik NAUSB-W, cable cut at the A end, harness H5) goes to **J6** (the spare hub port), not J4 (J4 is the panel P2 port). Pin order PH-4: 1 VBUS (red), 2 D- (white), 3 D+ (green), 4 GND (black). DIN OUT J7-J10 PH-3 (1 -> DIN pin 4, 2 -> pin 5, 3 -> pin 2 shield), DIN IN J11, J12 PH-2 (pin 4, pin 5): as the Thomann MIDI Socket. PJ-3920-3A C707258, green LED C84267.

EasyEDA (19.11.2026): R2 1.3 = R2_v9: детали 248/248, цепи 170/170, LCSC (схема 159, PCB 147), позиции 248/248, сохранено.
