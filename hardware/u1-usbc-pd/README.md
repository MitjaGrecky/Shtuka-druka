# U1 - USB-C PD input board (rear wall, harness H1)

Panel USB-C receptacle **GCT USB4105-GF-A** (C3020560, 5 A, 13495 pcs at JLC) on a 32 x 20 mm board; six solder pads for the wires to PW J2 (Micro-Fit 2x3, 12 cm): VBUS x 2 and GND x 2 (20 AWG), CC1 and CC2 (24 AWG). The PD sink controller TPS25730D stays on PW (R145). D+, D-, SBU open (power only). Shield to GND through 1 MOhm || 1 nF. Rev 0.1: schematic and placed board, `UNROUTED`; ERC 0, DRC 0 (except unconnected). The GCT footprint (KiCad library) has its NPTH pegs 0.19 mm from the GND pads: hole clearance 0.15 mm for this board (`HOLE_CLEARANCE` in design.py).

Generators: `gen/design.py`, `gen/make_sch.py`, `gen/make_pcb.py` (`KICAD_SYMBOL_DIR=<repo>/hardware/common/sym7`).
License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).

EasyEDA (19.11.2026): U1 0.1 = U1_v1: детали 6/6, цепи 5/5, LCSC (схема 3, PCB 3), позиции 6/6, сохранено.
