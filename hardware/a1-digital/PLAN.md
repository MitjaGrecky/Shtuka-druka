# A1 - converters and xcore.ai: plan and pinouts (14.11.2026, PC; schematic not started)

Sources: Cirrus CS5308P DS1314F1, CS5304P DS1313F1, CS4308P DS1317F1, AN0635 (ADC input buffer), AN0679 (DAC output buffer);
XMOS XU316 product series datasheet XM-015129-PC (QF60B pin list); EasyEDA/LCSC symbols C7397517 (XU316), C5367256 (ADuM4166).

## Converters (all QFN-48, pad 49 = GND)
- CS5308P (C42457798): 1 ADC_VMID1, 2 CONFIG1, 3 CONFIG2/HGC_SCK, 4 CONFIG3/HGC_SDO, 5 VDD_A1, 6 GND_A, 7 LDO_A_FILT, 8 GND_A,
  9 VDD_A2, 10 CONFIG4/HGC_CS, 11 CONFIG5, 12 ADC_VMID2, 13 IN5N, 14 IN5P, 15 IN6N, 16 IN6P, 17 ADC_FILT2N, 18 ADC_FILT2P, 19 IN7N,
  20 IN7P, 21 IN8N, 22 IN8P, 23 RESET, 24 ASP_FSYNC, 25-28 ASP_DOUT1-4, 29 ASP_BCLK, 30 GND_D, 31 VDD_IO, 32 LDO_D_FILT, 33 VDD_D,
  34 MCLK, 35 SPI_SDO/I2C_SCL, 36 SPI_SCK, 37 SPI_SDI/I2C_SDA, 38 SPI_CS, 39 IN1N, 40 IN1P, 41 IN2N, 42 IN2P, 43 ADC_FILT1P,
  44 ADC_FILT1N, 45 IN3N, 46 IN3P, 47 IN4N, 48 IN4P. VDD_A 3.3 V, VDD_IO 1.8-3.3 V; FILTxP to VDD_A via 1 Ohm.
  Software (SPI) mode: CONFIG1 to VDD_A (0 Ohm); unused CONFIG to GND. Recommended buffer (CS5308P fig. 2-1): FS 8 Vrms
  differential at the buffer input, /4 to the ADC pins (300 R / 1.2k, 680 pF, 68 uF per leg). **R1 rev 0.2+ delivers 8 Vrms
  diff FS (cloud #24), so A1 uses the Cirrus buffer with gain 1/4 - not gain 1** (corrected 14.11.2026 after the codex review).
- CS5304P (C49192888): same pinout, IN1-4 only, pin 1 ADC_VMID, 12-22 DNC, 43/44 ADC_FILTP/N.
- CS4308P: 1 CONFIG5, 2 VDD_A1, 3 GND_A, 4 LDO_A_FILT, 5 RESET, 6 LDO_D_FILT, 7 VDD_D, 8 MCLK, 9 ASP_BCLK, 10 ASP_FSYNC, 11 VDD_IO,
  12 GND_D, 13-16 ASP_DIN4-1, 17 SPI_SCK, 18 SPI_SDO/I2C_SCL, 19 SPI_SDI/I2C_SDA, 20 SPI_CS, 21 CONFIG3, 22 CONFIG2, 23 CONFIG4,
  24 OUT8N, 25 OUT8P, 26 OUT7N, 27 OUT7P, 28 OUT6N, 29 OUT6P, 30 OUT5N, 31 OUT5P, 32 DAC_VMID, 33 OUT4N, 34 OUT4P, 35 OUT3N,
  36 OUT3P, 37 GND_A, 38 VDD_A2, 39 DAC_FILTP, 40 DAC_FILTN, 41/42/47 NC, 43 OUT2N, 44 OUT2P, 45 OUT1N, 46 OUT1P, 48 CONFIG1.
  **Current output**: I-V per leg 1.2k || 620 pF to DAC_VMID (AN0679 fig. 1) -> 2 Vrms diff.

## XU316-1024-QF60B (C7397517): 65 pads = 60 + 61-64 VDD bars around the EP + 65 VSS (EP); footprint from LCSC
1 X0D05, 2 X0D07, 3 X0D01 (QSPI SS), 4 VDD, 5 X0D10 (QSPI SCLK), 6 X0D00, 7 X0D11, 8 VDDIOL, 9 X1D00, 10 X1D01, 11 X1D09, 12 VDD,
13 X1D10, 14 X1D11, 15 XOUT, 16 XIN, 17 VDDIOB18, 18 TDI, 19 VDD, 20 TDO, 21 RST_N, 22 PLL_AVDD, 23 TMS, 24 TCK, 25 NC, 26 VDDIOB18,
27 VDD, 28 USB_DM, 29 USB_DP, 30 USB_VDD33, 31 USB_VDD18, 32 X1D13, 33 X1D16, 34 VDD, 35 X1D17, 36 X1D18, 37 X1D19, 38 VDDIOR,
39 X1D22, 40 X0D29, 41 X0D35, 42 VDD, 43 X0D36, 44 X0D37, 45 X0D38, 46 X0D40, 47 X0D39, 48 X0D42, 49 VDD, 50 X0D41, 51 X0D43,
52 VDDIOT, 53 X1D34, 54 X0D30, 55 X0D31, 56 X0D32, 57 VDD, 58 X0D33, 59 X0D04, 60 X0D06, 61-64 VDD, 65 VSS.
VDD core 0.9 V; VDDIOL/R/T 3.3 V; VDDIOB18 (JTAG, crystal) 1.8 V. QSPI data X0D04-07.

Port plan, xcore A (bus master): MCLK in X0D11 (1D), BCLK X0D00 (1A), FSYNC X0D35 (1L), DAC DIN X0D36 (1M), ADC1/2/3 DOUT
X0D37/X0D38/X0D39 (1N/1O/1P); SPI on tile 1: SCK X1D00, MOSI X1D01, MISO X1D10, CS X1D11 / X1D22 / X1D13 / X1D34; converter RESET
X0D29, clock select X0D30, VBUS sense X0D40; XLINK0 2-wire to B: X1D16/X1D17 in, X1D18/X1D19 out. xcore B: USB via ADuM4166,
XLINK0 to A, PDM mic (header) on free 1-bit ports.

## ADuM4166 (C5367256, SOIC-20W)
1 VBUS1, 2 GND1, 3 VDD1, 4-7 GND1, 8 UD+, 9 UD-, 10 GND1, 11 GND2, 12 DD+, 13 DD-, 14 PGOOD, 15 XO2, 16 XI2, 17 GND2, 18 VDD2,
19 GND2, 20 VBUS2. Side 1 = PC (isolated ground GND_PC), side 2 = xcore B. Crystal on XI2/XO2 - check frequency.

## Blocks to draw
- ADC buffers: 20 x OPA1656 dual (RRO, +5V_A), inverting x 1 around ADC_VMID (Rin = Rf, Cf 680 pF, 68 uF coupling, 10 R out) - check overdrive.
- DAC I-V: 8 x OPA1656 dual around DAC_VMID; Main/Aux pairs to R1, phones pairs to F1 (2x5 header).
- Clocks: 24.576 and 22.5792 MHz oscillators (Oscillator:ASE-xxxMHz), mux (74LVC1G157 - no KiCad symbol, use another),
  fan-out 74LVC2G34 with 22 R; 24 MHz crystals for both xcore (1.8 V XIN).
- Power: +5V_A (TPS7A4701 from +12 V, ANY-OUT 5.0 V), 3.3V_A (TPS7A4701 from +5V_A), 3.3V_D (AP2112K-3.3), 1.8 V (AP2112K-1.8),
  0.9 V core (TLV62568DBV per xcore), PLL_AVDD filtered.
- Connectors: mating R1 2x20 / 2x25 (same pinout as R1), spare ADC 19-20, F1 phones, USB A (PH4 from R2 hub), USB PC (PH6 with CC
  Rd 5.1k and USBLC6 on the isolated side), PDM mic, JTAG x 2, QSPI flash W25Q per xcore.
