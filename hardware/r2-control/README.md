# R2 - Control board (rear wall, right part)

The RP2350 of the control board (R85) with everything that is not audio at the rear wall: MIDI, CV/Gate, sync, the internal
USB hub, the rear USB-C (to a computer) and USB-A, the power jacks and the control lines to the audio boards.
Research and decisions: `docs/ru/34_rear_boards_research.md`, R118, R135-R138. Map of boards: `docs/ru/29_board_map.md`.

**Status: rev 0.1 - schematic only** (225 parts, 168 nets). The board outline and the jack positions follow the rear panel
layout (doc 13, section 3.5), which is not drawn yet; the 5-pin DIN footprint (CUI SDS-50J, LCSC C6216157), the locking
DC jack and a 5 A USB-C receptacle for PD are chosen together with it.

| Block | Parts | Notes |
|---|---|---|
| MCU | RP2350A, W25Q128JVSIQ (16 MB QSPI), 12 MHz crystal, core regulator with 3.3 uH | VREG parts after third-party RP2350 boards - **check** against Raspberry Pi's minimal design |
| USB hub | USB2514B, 24 MHz crystal | Up: Mini-ITX USB header. Down: 1 RP2350, 2 panel P2 (R86), 3 A1 port A (R82), 4 spare. Straps low = default - **check** |
| Rear USB-C (PC) | HRO TYPE-C-31-M-12, 5.1k Rd, USBLC6-2SC6 | Passed to A1 port B (isolated there by ADuM4166) |
| Rear USB-A | Molex 67643, USBLC6-2SC6 | Passed to a Mini-ITX USB header (R80) |
| Power jacks | USB-C PD, DC 12-24 V | Passed to PW on a 2x5 header; PD sink (TPS25730), protection and source selection are on PW |
| MIDI DIN | 2 in (TLP2361 at 3.3 V), 4 out | CA-033 3.3 V: 33 R 0.5 W + 10 R per output; every output has its own port (R34) |
| MIDI TRS | 1 in, 2 out | Out: tip and ring each from a GPIO through 22 R - type A/B is swapped in firmware (R32). In: two optos back to back, type A and B both work |
| CV/Gate out 1-8 | 2 x DAC80504 (16 bit, internal 2.5 V ref, gain 2), 3 x OPA4197 on +-12 V | Vout = 4.02 (Vdac - 2.5 V) = -10 ... +10 V; reset to mid-scale = 0 V; 1k output resistors. Step 0.31 mV = 0.37 cent at 1 V/oct |
| CV in 1-4 | RP2350 ADC0-3 | -10 ... +10 V -> 0 ... 3.03 V (100k / 33k to 3.3 V / 39k to GND), BAT54S clamp |
| Sync | 3 out, 2 in | Out: GPIO -> op-amp x1.51 -> 0 / +5 V. In: NPN inverter, 22k / 100k, negative clamp |
| To A1/R1 (2x5) | PH48_1, PH48_2, PHONO, MUTE, R2_OK | Pulled low while booting; the output relays (R137) open when R2 stops |

GPIO map (all 30 used): 0-3 MIDI TX 1-4, 4-5 MIDI RX 1-2, 6-9 TRS out 1-2 tip/ring, 10-11 TRS in A/B, 12 MUTE,
13 R2_OK (+ status LED), 14-17 DAC SCK, SDI, CS1, CS2, 18-20 clock out 1, 2, reset/run out, 21-22 clock in, reset/run in,
23-24 phantom 1-2, 25 phono/line, 26-29 CV in 1-4.

To check before the board: RP2350 VREG parts; DAC80504 straps (GAIN high = x2, RSTSEL high = mid-scale, REFDIV low) and VDD
headroom at a 5 V output; USB2514B straps and VBUS_DET divider; stock LCSC numbers of the RP2350 and the passives with new values.

Checks (13.11.2026, PC): `tools/sch_netcheck.py hardware/r2-control` - 237 symbol units, 749 pins, 0 mismatches against
`design.py` (kicad-cli is not run on this PC; ERC by CI).

Generators: `gen/design.py`, `gen/make_sch.py` (shared writer `hardware/common/gen/module_sch.py`, multi-unit symbols placed unit by unit).

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
