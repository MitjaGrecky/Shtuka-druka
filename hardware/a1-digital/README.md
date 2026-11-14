# A1 - Digital audio board (under the slope, left; mates R1 at a right angle)

20 differential ADC channels, 8 DAC channels, two XMOS xcore.ai, USB isolation, two clock sources, quiet supplies.
Plan, pinouts and sources: `PLAN.md`. Decisions: R82-R84 (two USB ports, TDM, 96 kHz hardware), R87 (volume in the DAC), R88 (two spare
channels), R114 (two oscillators), R116/R117 (converters, two paths per mic), R136 (CS4308P, current outputs).

**Status: rev 0.1 - schematic only** (608 parts, 388 nets, 14.11.2026). Values around the converters follow the typical-connection drawings
as far as they could be read from the datasheets; every "check" note in `gen/design.py` is for the datasheet review (cloud task #26).

## Blocks

| Block | Parts | Notes |
|---|---|---|
| ADC | 2 x CS5308P (8 ch, C42457798) + 1 x CS5304P (4 ch, C49192888) | SPI software mode (CONFIG1 to VDD_A), ASP secondary, TDM out on DOUT1. Chip A = ADC 1-8 (mic 1-2 two paths, Hi-Z 1-2 two paths), B = ADC 9-16 (phono 2, line 1-6), C = ADC 17-20 (line 7-8, spare 1-2) |
| ADC input buffers | 20 x OPA1656 dual, 68 uF + 1.2k in, 300 R + 680 pF feedback, 10 R out, 15 nF across the pair | Cirrus circuit, gain 1/4: R1 delivers 8 Vrms diff FS -> 2 Vrms at the pins (AN0635); inverting, so the source P leg goes to the N pin (polarity kept); non-inverting inputs at ADC_VMID |
| DAC | CS4308P (8 ch) | Current outputs: 8 x OPA1656 dual I-V, Rf 1.2k + 620 pF per leg (AN0679), 47 R build-out, 1 nF across. Outputs 1-4 Main L/R, Aux L/R -> R1; 5-8 Phones 1 L/R, 2 L/R -> F1. Not in the EasyEDA library (R136) |
| xcore A (U) | XU316-1024-QF60B (C7397517), W25Q16 boot flash | TDM master (BCLK, FSYNC, DAC data, 3 ADC data), SPI to the 4 converters (tile 1), converter reset, oscillator enables, USB port A from the R2 hub, XLINK0 to B |
| xcore B | XU316-1024-QF60B, W25Q16 | USB port B to the external computer through the ADuM4166, PDM microphone (header), XLINK0 to A |
| USB isolator | ADuM4166 (C5367256), USBLC6 on the computer side, Rd 5.1k | Computer side on the isolated ground GNDPC; the rear USB-C (PC) receptacle on the wall comes in over a JST PH 6 cable (R145: data only) |
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

## To check (cloud task #26)

- ADC/DAC capacitor values and strap resistors against the typical-connection drawings (VMID 2.2 uF + 0.22 uF, FILT, LDO pins, VDD_D),
  DAC_FILTP to VDD_A2, unused CONFIG pins in SPI mode, 68 uF coupling type; the CS4308P LCSC number / footprint.
- XU316: PLL_AVDD supply (0.9 V assumed), core power-up sequencing, crystal load, 1.8 V domain pins (JTAG, RST_N), QSPI flash size, port plan
  against lib_xua (TDM master, async USB, PDM microphone), whether tile-1 pins can drive the SPI at the needed rate.
- ADuM4166: VDD1 (output or input), VBUS2/VDD2 supply, crystal on XI2/XO2, footprint (SOIC-20W body 15.4 mm per the LCSC part).
- Oscillators: JLC parts for 24.576 and 22.5792 MHz (3.3 V, enable pin), jitter; the 33 R / 22 R star.
- TPS7A4701 noise bits and NR; AP2112K current budget (digital 3.3 V, 600 mA).

Checks: `tools/sch_netcheck.py hardware/a1-digital` - 664 symbol units, 1889 pins, 0 mismatches; every symbol pin listed. ERC by CI.
Symbols for the CS5308P / CS5304P / CS4308P / XU316 / ADuM4166: `hardware/common/gen/ic_symbols.py` -> `ShtukaDruka.kicad_sym`; footprint of
the XU316: `ShtukaDruka.pretty` (converted from the LCSC library with `tools/eda/lcsc_fp.py`).

Generators: `gen/design.py`, `gen/make_sch.py`. On the PC set `KICAD_SYMBOL_DIR=<repo>/hardware/common/sym7`.

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
