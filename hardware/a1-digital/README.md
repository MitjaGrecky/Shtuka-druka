# A1 - Digital audio board (under the slope, left; mates R1 at a right angle)

> **Rev 0.6 (18.11.2026, решение главного инженера, P108):** конденсаторы связи — по одному неполярному Würth WCAP-ASNP 865250349007 (47 мкФ 16 В, Ø8×6,5, LCSC C5530373) на канал, 40 шт., паять вручную (на JLC нет в наличии, Digikey 239 шт.). THD+N на 20–100 Гц замерить на первой плате. Rev 0.5 с парами FVH016 не заказывать.

20 differential ADC channels, 8 DAC channels, two XMOS xcore.ai, USB isolation, two clock sources, quiet supplies.
Plan, pinouts and sources: `PLAN.md`. Decisions: R82-R84 (two USB ports, TDM, 96 kHz hardware), R87 (volume in the DAC), R88 (two spare
channels), R114 (two oscillators), R116/R117 (converters, two paths per mic), R136 (CS4308P, current outputs).

**Status: rev 1.0 (20.11.2026) - placed board, not routed; USB isolator TI ISOUSB211 since rev 0.9 (see the Rev sections at the end; rev 0.6 text below kept as history: 613 parts, 18.11.2026).** Schematic checked against the datasheets (cloud task #26, rev 0.2): CS4308P DS1317, CS53A04P DS1397
(same family as the CS5304P/8P - the CS5308P/CS5304P datasheets themselves were not reachable), XU316-1024-QF60B, ADuM4165/4166, SiTime/SCTF oscillators.

## Blocks

| Block | Parts | Notes |
|---|---|---|
| ADC | 2 x CS5308P (8 ch, C42457798) + 1 x CS5304P (4 ch, C49192888) | SPI software mode (CONFIG1 to VDD_A), ASP secondary, TDM out on DOUT1. Chip A = ADC 1-8 (mic 1-2 two paths, Hi-Z 1-2 two paths), B = ADC 9-16 (phono 2, line 1-6), C = ADC 17-20 (line 7-8, spare 1-2) |
| ADC input buffers | 20 x OPA1656 dual, 47 uF X5R (2.8 Hz) + 1.2k in, 300 R + 680 pF feedback, 10 R out, 15 nF across the pair | Cirrus circuit, gain 1/4: R1 delivers 8 Vrms diff FS -> 2 Vrms at the pins (AN0635); inverting, so the source P leg goes to the N pin (polarity kept); non-inverting inputs at ADC_VMID |
| DAC | CS4308P (8 ch) | Current outputs: 8 x OPA1656 dual I-V, Rf 1.2k + 620 pF per leg (AN0679), 47 R build-out, 1 nF across. Outputs 1-4 Main L/R, Aux L/R -> R1; 5-8 Phones 1 L/R, 2 L/R -> F1. Not in the EasyEDA library (R136) |
| xcore A (U) | XU316-1024-QF60B (C7397517), W25Q32JVSSIQ boot flash (4 MB, B18; C82344) | TDM master (BCLK, FSYNC, DAC data, 3 ADC data), SPI to the 4 converters (tile 1), converter reset, oscillator enables, USB port A from the R2 hub, XLINK0 to B |
| xcore B | XU316-1024-QF60B, W25Q16 | USB port B to the external computer through the ISOUSB211 (rev 0.9; was ADuM4166), PDM microphone (header), XLINK0 to A |
| USB isolator | TI ISOUSB211DPR (C5772877, rev 0.9; was ADuM4166 C5367256), USBLC6 on the computer side, Rd 5.1k | Computer side on the isolated ground GNDPC; the rear USB-C (PC) receptacle on the wall comes in over a JST PH 6 cable (R145: data only) |
| Clocks | 24.576 MHz and 22.5792 MHz oscillators with enable pins (parts to choose), 33 R each into MCLK, 22 R star to every load | Default 48 kHz family on; xcore A can switch (R114). 24 MHz crystals for both xcore cores |
| Supplies | +3V3A TPS7A4701 (ANY-OUT 3.3 V), +3V3D and +1V8 AP2112K, +0V9 x 2 TLV62568 (0.6 V x 1.5) from +5V; +-12 V from R1 for the op-amps | +-12 V and +5 V arrive through the R1 board-to-board connector (PW -> R1 -> A1) |

## Connectors

| J | To | Notes |
|---|---|---|
| 2x20 socket | R1 "to A1 (ADC 1-10)" | same pinout; pairs on adjacent pins with a GND pair between |
| 2x25 socket | R1 "to A1 (ADC 11-18, DAC 1-4, power)" | same pinout; +12V, -12V, +5V x 2 on pins 47-50 |
| 2x6 header | F1 "from A1" | Phones 1 and 2 pairs, twisted |
| JST PH 4 | R2 hub "USB down: A1 port A" | VBUS sense only |
| JST PH 6 | rear USB-C (PC) | PC_VBUS, DM, DP, CC1, CC2, GNDPC |
| JST PH 6 | spare ADC 19-20 | R88 |
| JST PH 6 x 2 | JTAG A and B (1.8 V logic) | xTAG adapter - check the pinout |
| JST PH 4 | PDM microphone | CLK, DATA, +3V3D, GND |

xcore pin plan (as in `gen/design.py`): A: MCLK X0D11, BCLK X0D00, FSYNC X0D35, DAC data X0D36, ADC data X0D37/38/39; SPI SCK X1D00,
MOSI X1D01, MISO X1D10, CS X1D11/X1D22/X1D13/X1D34; reset X0D29; oscillator enables X0D30/X0D31; hub VBUS sense X0D40; XLINK0 X1D16-X1D19.
B: MCLK X0D11, PDM X1D00/X1D01. QSPI boot on X0D01 (SS), X0D10 (SCLK), X0D04-07.

## Checked (cloud task #26, rev 0.2)

**Converters (CS4308P, CS53A04P family).** Pin maps of the CS4308P (all 48) and of the four-channel ADC half (supplies, SPI, ASP, CONFIG, IN1-4) agree with the schematic.
- Capacitors as in the typical-connection drawings: VDD_A1 and VDD_A2 each 4.7 uF + 10 nF, LDO_A_FILT 1 uF, LDO_D_FILT 1 uF with VDD_D tied to it (no separate cap),
  VDD_IO 0.1 uF. Rev 0.1 had 1 uF / 10 uF / 4.7 uF.
- DAC: DAC_FILTP 22 uF to **VDD_A2**, DAC_FILTN 22 uF to ground (rev 0.1: 4.7 uF between them), DAC_VMID 10 uF (rev 0.1: 1 uF).
  ADC: FILT 4.7 uF + 0.47 uF (the figure text is ambiguous between 0.47/4.7 and 0.22/2.2; VMID 2.2 uF + 0.22 uF), ADC_FILTP through 1 R to VDD_A.
- SPI mode: CONFIG1 0 R to VDD_A, **CONFIG5 to ground**; in software mode CONFIG2-4 of the ADC are the **HGC SPI outputs** (clock, data, chip select for external
  preamplifiers, off by default): 1 k to ground instead of 10 k. DAC CONFIG2-4 unused to ground.
- No power-up sequencing; RESET low >= 1 ms, control port ready 5 ms after the release; POR of VDD_A 1.9-2.7 V.
- MCLK 24.576 / 22.5792 MHz directly (software mode, PLL bypass) or 512 fs with the PLL, +-1 %, duty 40-60 %. **ASP secondary: MCLK, BCLK and FSYNC must come from a
  common source** - here MCLK from the oscillator and BCLK / FSYNC derived by xcore A from the same MCLK (lib_xua master mode does that).
- ADC input: 0 dBFS = 2.0 Vrms differential at the pins (scales with VDD_A), input resistance 3 kOhm differential in the default mode (INxx_HIZ = 0).
- **Coupling capacitors 68 uF -> 47 uF X5R 10 V (1210)**: a 68 uF 25 V ceramic does not exist, and a polarised one cannot be used - the buffer side sits at 1.6 V
  while each leg swings +-5.7 V at full scale (reverse voltage). Corner 2.8 Hz instead of 1.95 Hz; the capacitor voltage never exceeds 7.3 V. 20 x 2 = 40 pieces (rev 0.6: non-polar Würth WCAP-ASNP instead of X5R).
- CS4308P: **no LCSC number** (a new part; Digikey CS4308P-DNR, 16 weeks lead time, 48-QFN 6x6, 0.4 mm). Footprint body 6x6 and pitch 0.4 are confirmed;
  the exposed-pad size is in section 10 of the datasheet (not retrievable here) - draw the footprint from it. Output: 1.67 mA rms per channel, 1.2 kOhm = 2.0 Vrms (AN0679).

**XU316-1024-QF60B.**
- Pin map of the supplies and of all used ports agrees (VDD x 8 + paddles 61-64 at 0.9 V, VDDIOL/R/T 3.3 V, VDDIOB18 x 2 1.8 V, USB_VDD33 3.3 V, USB_VDD18 1.8 V).
  Bottom bank (XIN, XOUT, RST_N, JTAG) is 1.8 V only - correct.
- **PLL_AVDD:** 0.9 V nominal, filter = ferrite bead 600 R at 100 MHz (DCR < 1 R) + **1 uF** MLCC at the pin (rev 0.1: 4.7 uF + 100 nF kept as a second capacitor).
- **Sequencing:** VDD and VDDIO within about 50 ms, monotonic; the 3.3 V domains must be valid before reset is released, and VDDIOB18 must not be last - here all rails come from the
  same +5 V and the TLV62568 / AP2112K start together; RST_N has a 100 nF to ground with the 10 k pull-up to 1.8 V (about 1 ms delay), which keeps it low while the rails rise.
- Crystal 24 MHz, 12 pF load, ESR <= 60 R, tolerance +-500 ppm or better: C70590 with 18 pF caps is right.
- **USB PHY:** enable it on **tile 0** (xcore A and B). The USB ports of the PHY are not on the QF60 pins of tile 0; enabling it on **tile 1 removes ports 1F (X1D13) and 1K (X1D34) -
  our SPI chip selects CS_ADCC and CS_DAC of xcore A would be lost.** lib_xua then runs the USB and the audio on tile 0 (supported); the SPI to the converters and the PDM microphone stay on tile 1.
- Boot: X0D04-X0D06 are sampled after reset with weak pull-downs, 000 = QSPI; the flash must answer a Quad I/O read (0xEB) within 300 us, so its QE bit must be set (the first programming
  goes over JTAG with xflash, which sets it). A blank W25Q16 may pull IO2/IO3 up internally; if the board does not boot before the first programming, program it over JTAG.
- Flash: the datasheet gives no minimum; a lib_xua UAC2 application with DFU needs about 2x the image, so the user chose 4 MB (B18): W25Q32JVSSIQ (C82344), same package and pinout.
- Ports: BCLK X0D00 (1A), MCLK X0D11 (1D), FSYNC X0D35, DAC data X0D36, ADC data X0D37-39 are all 1-bit ports of tile 0 (nine 1-bit ports on tile 0: 1A, 1B, 1C, 1D, 1L-1P);
  SPI on tile 1 (1A, 1B, 1C, 1D, 1F, 1G, 1K). Everything the plan uses exists. TDM master with a 1-bit BCLK clock port is the lib_xua configuration; PDM needs a 1-bit data port (X1D01).

**ADuM4166** (pin table: all 20 agree).
- **VBUS2 was +5 V with VDD2 on the external 3.3 V: the internal LDO would fight our regulator** (and VDD1/VDD2 need exactly 0.1 uF with the LDO). Now VBUS2 = VDD2 = +3V3D (LDO bypassed, 3.0-3.6 V),
  VDD2 / VBUS2 0.1 uF, VDD1 0.1 uF (LDO output, **not** 1 uF: "above 0.1 uF disrupts the start-up"), VBUS1 0.1 uF; PGOOD open. VBUS1 = PC VBUS 3.0-5.5 V.
- Crystal 24 MHz, <= 50 ppm and <= 100 ppm stability, starts within 0.3 ms, typical load 10 pF: C70590 (12 pF) with 15 pF caps (about 10.5 pF) works; a 10 pF part is better. Or a 24 MHz clock into XI2 (XO2 open).
- Footprint: LCSC lists it as SOIC-20-300mil (rev 0.1 had a 15.4 mm body "per the LCSC part" - a 300-mil SOIC-20 is 12.8 mm): check against the datasheet drawing; the LCSC number of the BRIZ-RL
  is C5581725 (out of stock on 14.11.2026, $15), the schematic carries C5367256 from the PC - check which one is the stocked variant.

**Oscillators** (R114): 24.576 MHz SiTime SiT8208AI-21-33E-24.576000 (C839665, 3225, 3.3 V, +-20 ppm, 0.5 ps; **out of stock** on 14.11), 22.5792 MHz SCTF SX3M22.5792M20F30TNN (C2901572,
3225, 825 in stock, 1.62-3.63 V, +-20 ppm; jitter and enable pin polarity not on the page). Pin 1 = enable, high = on, as the schematic assumes. For a 123 dB ADC the clock jitter matters: SiTime
has 0.5 ps; the SCTF part must be checked or replaced (SiT8208 22.5792). The 33 R + 22 R star is kept.

**Supplies.** TPS7A4701: ANY-OUT 1.4 + 1.6 + 0.2 + 0.1 = 3.3 V with pins 8 (1.6 V), 11 (0.2 V), 12 (0.1 V) to ground - confirmed from the symbol; NR/SS 1 uF not verified (TI text not retrievable).
AP2112K 3.3 V: 600 mA max, estimated 150 mA typical -> 0.26 W in a SOT-23-5 (250 K/W = +65 K): **warm, keep an eye on it on the first board** - the analog side is not on this regulator
(it is on the TPS7A4701). TLV62568 0.9 V x 2: 1 A, the feedback 0.6 x (1 + 100k / 200k) = 0.9 V is right; the xcore.ai core draws about 0.5 A at full load (to measure).

## Still open

- CS5308P and CS5304P datasheets (pins 12-22 of the CS5304P are DNC in the CS53A04P; the CS5308P has pins 13-22 as IN5-8 and the second VMID/FILT) - compare once the datasheet is available.
- Exposed-pad size of the CS4308P footprint; body length of the ADuM4166; CS4308P order.
- Oscillator parts (stock), 10 pF crystal for the ADuM4166.
- AP2112K temperature.

Checks: `tools/sch_netcheck.py hardware/a1-digital` - 663 symbol units, 1887 pins, 0 mismatches; every symbol pin listed. ERC by CI.
Symbols for the CS5308P / CS5304P / CS4308P / XU316 / ADuM4166: `hardware/common/gen/ic_symbols.py` -> `ShtukaDruka.kicad_sym`; footprint of
the XU316: `ShtukaDruka.pretty` (converted from the LCSC library with `tools/eda/lcsc_fp.py`).

Generators: `gen/design.py`, `gen/make_sch.py`. On the PC set `KICAD_SYMBOL_DIR=<repo>/hardware/common/sym7`.

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).

## Rev 0.3: placed board for routing (14.11.2026, PC)
Placed board (no routing) generated by `gen/make_pcb.py`; `UNROUTED` marker for CI; package `hardware/for-routing/A1`. Placement is a starting point: the rest by `hardware/common/gen/autoplace.py` (ICs on a grid, small parts around the IC they share signals with, cable headers along the bottom edge). Outline and mounting holes are rough until the enclosure is fixed. `pcb_geomcheck`: 0 problems.

Low case (17.11.2026, R162): the board stands on a 2 mm tray over the battery. Parts on the bottom side reach 7.7 mm (5 x CP 6.3 x 7.7), so the standoffs between the board and the tray must be >= 8.5 mm, with an insulating film on the tray. Socket rows of J1 / J2 end up about 30.4 / 32.9 mm above the floor (superseded: A1 now stands on the floor, R174; header height of R1 J4 / J5: R1 rev 0.7).

Rev 0.5 (17.11.2026, R172): 80 x FVH016 electrolytics in back-to-back pairs instead of the X5R capacitors; **superseded by rev 0.6 (P108), do not order rev 0.5**: the reverse-voltage rating of the pair was never confirmed (up to about +-2.8 V on each capacitor at 20 Hz and full scale).


Rev 0.6 (18.11.2026): 80 FVH016 заменены 40 одиночными WCAP-ASNP (47 мкФ, угол ≈ 2,8 Гц с 1,2 к). 613 деталей, 0 несовпадений нетлиста, 0 перекрытий. Footprint CP_Elec_8x6.5 приблизителен к даташиту.

## Rev 0.5: ADC overload clamps (audit 18.11.2026)
CS5308P DS1314F2 table 3-3: analog inputs -0.3 ... VDD_A + 0.3 V, +-10 mA. A clipped R1 stage leaves the buffer at -1.1 ... +4.4 V (about 70 mA through 10 R into the ADC diodes). One **BAT54S** (onsemi C19726, Schottky pair to +3V3A / GND) per ADC pin: 40 parts, near the pins. Stock: the CS5308P itself has 0 pcs at JLC on 18.11.2026 (Digikey or direct from Cirrus).

## Rev 0.6: 24.576 MHz oscillator (18.11.2026)
The two oscillators drive MCLK through 33 R each and only one is enabled. The YXC OT2EL4C4JI datasheet could not be downloaded, so what the output does at OE low was unknown (a low-driving output halves the other). Replaced by **SCTF SX3M24.576B10F20TNN** (C7431342, 922 pcs at JLC, tri-state like the 22.5792 one). The old part had a 0.7 ps jitter figure, the SCTF has none in its datasheet: measure the clock on the first board (B19). If the jitter is not enough: YXC with a read datasheet plus a 2:1 clock multiplexer instead of tied outputs.

EasyEDA (18.11.2026, PC, rev 0.6): project `A1_v5` imported but NOT verified: the schematic / PCB tabs do not open through the API (big board, needs a manual double click in "All Projects"; the PC screen was in use). Run `tools/pc/eda_one.sh` steps eda_open2 / eda_board / eda_save for A1_v5.

EasyEDA (19.11.2026): A1 0.6 = A1_v6: детали 653/653, цепи 388/388, LCSC записаны, позиции 653/653, сохранено.

## Rev 0.7: ADuM4166 node (19.11.2026)
ADI datasheet ADuM4165/4166 Rev. B read (copy of the text: `notes/datasheets_text/adum4165_4166.md`). Verified: pins (side 1 = upstream UD+/UD-, side 2 = downstream DD+/DD-, crystal on side 2: XO2 15, XI2 16), GND1 2/4/5/6/7/10, GND2 11/17/19, PGOOD open, VBUS1 from the PC cable with 0.1 uF, VDD1 exactly 0.1 uF, VBUS2 and VDD2 tied to 3.3 V with 0.1 uF (LDO bypassed, allowed), USBLC6 on the cable side. Changed: crystal 12 pF -> **10 pF** (the datasheet asks for a 10 pF crystal, tolerance <= 50 ppm, stability <= 100 ppm, start within 0.3 ms). **Layout rules for routing** (datasheet 'PCB layout and EMI', table 3): clearance 8.1 mm in the PCB plane and creepage 8.3 mm between side 1 and side 2 copper under and around the SOIC_IC: no copper of any layer under the chip between the sides, the GNDPC island (USB-C, USBLC6, CC resistors, VBUS and VDD1 capacitors, ISO_V1) separated from GND by at least 8.3 mm; bypass capacitors with at most 10 mm of lead to the pins; crystal and its two capacitors as close as possible to pins 15/16; all GND pins of one side joined to its own ground. Side 2 must not exceed 3.5 V before side 1 is up (AP2112K 3.3 V: fine). ESD: the datasheet suggests TVS on the USB-C side (Wurth 82402304 for 8 kV contact); USBLC6-2SC6 is there, the level is not tested.

## Rev 0.9 (20.11.2026): USB isolator ISOUSB211
ADuM4166 is unavailable (51 weeks at Digikey): **TI ISOUSB211DPR** (SLLSFC5D, C5772877; LS/FS/HS 480 Mbit/s, reinforced 5.7 kVrms, no crystal). Side 1 (PC jack, GNDPC): VBUS1 = VCC1 = PC VBUS (5 V), the internal LDOs give V3P3V1 and V1P8V1. Side 2 (A1 ground, xcore B): VBUS2 = V3P3V2 = +3V3D, VCC2 = V1P8V2 = +1V8 (A1's own AP2112K-1.8: LDO bypassed, less heat); no isolated DC-DC is needed: the PC side only takes cable VBUS, the A1 side its own rails. EQ pins 00 (GND), CDPENZ high (no CDP), V1OK / V2OK open. Capacitors per 8.3: 1 uF at VBUSx, 0.1 uF at V3P3Vx, 2.2 uF + 0.1 uF + 10 nF at V1P8Vx. The crystal and its 15 pF capacitors are gone. Chip loss 0.3-0.5 W (RthJA 44 K/W); creepage 8.15 mm: no copper under the chip between the sides, GNDPC island 8.2 mm from GND (as for the ADuM). Footprint `ShtukaDruka:SSOP-28_DP0028A_7.5x10.3mm_P0.65mm` from the TI drawing (pads 2.0 x 0.45, rows 9.85 mm apart). Also: +5V bulk capacitor 47 uF 25 V (C190223).

EasyEDA (19.11.2026): A1 0.9 = A1_v7: детали 657/657, цепи 387/387, LCSC (схема 256, PCB 200), позиции 657/657, сохранено.

## Rev 1.0 (20.11.2026): placement rule template
Courtyard gap 1.0 mm (ic_gap 1.6 mm around fine-pitch ICs) instead of 0.25 mm, the largest that fits the outline (autoplace.fit); basis: notes/placement_analysis_2026-11-20.md. Schematic unchanged.
