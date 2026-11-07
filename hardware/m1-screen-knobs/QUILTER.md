# Handing M1 to an external layout service (Quilter or similar)

> **Rev 0.3 (Nov 7, 2026), job `I_rev03_fanout_free`:** what the earlier jobs taught, in one input.
> - Locked copper is straight segments only (job D failed on PCB_ARC; F with chords routed 97%).
> - U1/U6 stand as a diamond (45 deg) on the back at gap 2 / gap 6, y 6 mm, and their fan-out is drawn by
>   `make_pcb.driver_fanout()` and locked: every signal pad -> 0.12 mm stub -> via (0.45/0.2) in two staggered rows,
>   0.43 mm from a lane to the neighbouring via. Job F left 17 CS lines stuck at the pad columns; Freerouting too.
>   Picture: `mech/m1_r03_driver_fanout.png`. CS map turned so side 2 (SW, CS1-5) faces the right ring pair (CS1-9)
>   and side 3 (CS6-18) the left pair (CS10-18).
> - Everything else that the panel does not fix (51 parts) waits below the board without a region: Quilter places it
>   on either side (user, 07.11). B.Cu rule areas `no_parts_under_ENC*` forbid parts under the encoders (job H put U2
>   and its passives there, inside the track keep-out). Extra In2-only copies of the track keep-outs (`*_In2`):
>   job F routed 61 tracks on In2 under the encoders.
> - Wizard: stack-up JLCPCB 4-layer 4/4 mil, inner layer 2 = Signal; fabricator: clearance 0.13 (0.13 + 0.125 via
>   ring = 0.255 via hole to track), via 0.45/0.2. Duplicates do not carry these over.
> - Net names follow the schematic (`/NAME` for labels): the CSV tables use them. Schematic parity: symbol fields
>   on the footprints, holes out of BOM, not-fitted parts out of BOM (no DNP flag: KiCad 7 cannot write it).
> - Local DRC of the input (KiCad 7 engine, project rules): no clearance or hole errors.

> **Rev 0.2 (Nov 6, 2026):** two LED drivers (U1 cell A rings 1-4, 0x30; U6 cell B rings 5-8, 0x31), CS triples
> stay on their rings, cathode arcs and ring vias are drawn by `make_pcb.ring_arcs()` and locked (2 vias per LED),
> decoupling capacitors sit at their pins (`design.HUG`), all other bottom parts in the rear strip (y 0-7),
> 8 mounting holes (corners + gaps 1, 3, 5, 7), net class LED_SW 0.25 mm for `*_SW*`. Job: `D_rev02_route_only`.
> The tables below describe rev 0.1 where they differ (one driver, 4 holes).

Everything that the panel fixes is **locked** in the board file. A service may move only the
unlocked parts (U1-U5, resistors, capacitors) and must keep these rules:

| What | Rule |
|---|---|
| Locked parts | ENC1-8 (knob row, 28 mm pitch), D1-D104 (ring LEDs), J1 (bus connector), H1-H4 |
| Top side (F.Cu) | only encoders and ring LEDs; no other parts (the light guide sits on it) |
| Under encoder bodies | no tracks, no vias on any layer (rule areas `under_encoder_*`): the encoder frame is the touch electrode |
| In1.Cu | GND plane, cut out under each encoder frame (x +-6 mm, y +-8 mm around the shaft) |
| Stack-up | 4 layers, 1.6 mm, JLCPCB standard |
| Net classes | Default: track 0.12, clearance 0.13, via 0.45/0.2 mm. Power (+5V, GND): track 0.3 mm |
| Fab limits (JLCPCB 4-layer) | track/space >= 0.09 mm, via drill >= 0.2 mm, via hole to track >= 0.254 mm, copper to edge >= 0.3 mm |
| Touch lines | TOUCH0-7 from R7-R14 to each encoder MP pin: short, away from SW/CS lines where possible |
| LED driver U1 | IS31FL3741A, QFN-60 0.4 mm; thermal vias in the exposed pad; keep its decoupling (C1-C4) close |

Inputs: run `gen/make_quilter.py OUT` - three jobs: `A_route_only` (our placement, routing only), `B_place_and_route` (only panel-fixed parts inside the outline) and `C_small_parts_free` (our placement, ICs and passives may move: anywhere on the bottom, on the top only inside two free strips). Upload the three files of one job: `.kicad_pcb`, `.kicad_sch`, `.kicad_pro` (no zip).
Output wanted: the routed `.kicad_pcb` (same nets), which CI then checks with KiCad 10 (DRC with schematic parity).

Each job folder also gets `bypass_capacitors.csv`, `high_current_nets.csv` and `ground_nets.csv` for the
Circuit Comprehension step ("Upload CSV"); column names follow Quilter's own CSV export.

## Fixed and movable (map: `mech/m1_fixed_vs_movable.png`)

| Group | Parts | Rule |
|---|---|---|
| Locked (the panel decides) | ENC1-8, D1-D104, J1, H1-H4 (117 parts) | never move |
| Movable (job C) | R1-R18, RN1-RN6, C1-C13 (37 parts), start below the board | Quilter places them next to their ICs |
| Anchors (job C) | U1-U5 | locked inside the outline; parts inside the outline are pre-placed for Quilter |
| Top (job C) | strips "Top strip rear" 211 x 5.1 mm (y 0.8-5.9) and "Top strip front" 211 x 2.4 mm (y 30.8-33.2) | small SMD only (0402, 0805, RN) |
| Top, everything else | rule area "Top: locked parts only" (footprints disallowed) | nothing new |

Why the top is free in the strips: the light guide is 6.4 mm thick and every movable part is at most 1.2 mm high
(0402, 0805, TSSOP-16). The guide gets a groove from below over the strips (like the J1 pocket), made from the final
placement. The strips follow from a free-space map: ring LED + 2 mm wall, encoder cut-out + 0.8 mm, screw head r 3.5 mm
and 0.8 mm board edge are blocked. U1 (7 x 7 mm QFN) and the 74HC165 (legs 6.4 mm) do not fit the 5.1 mm strip: ICs stay on the back.
Top and bottom regions are a union for the parts assigned to both (Quilter: two-sided region).

Job A result (Nov 6, 1h 28m): 1 candidate, 12 incomplete nets, 8 of 13 bypass capacitors flagged.
Job C result (Nov 6): cancelled after 2 h, 6 placements, router stuck at 33/39 steps, no routed candidate.
Root cause is the board, not Quilter: one LED driver for 104 LEDs puts up to 44 signal nets through one gap
between encoders (`gen/cut_count.py`). Next step: two identical 4-knob cells (decision P98).

## What we learned on app.quilter.ai (November 2026)

- No public API, SDK, CLI or MCP: the web app is the only way in.
- Settings of a step are saved only by its **Continue** button; jumping to another step by URL drops them.
- "Replace Files" makes a new draft and offers to copy settings from the old one. Copying **Floorplan**
  overwrote the placement regions parsed from the new file; stack-up and fab limits were not copied at all.
- KiCad placement region: a rule area on B.Cu with every keep-out item allowed. It shows up in Floorplan,
  parts are added to it by reference.
- A rule area on F.Cu with only footprints disallowed is read as a top-side component keep-out.
- "Prefer single-sided layouts" means **top side only**.
- Job B (parts to be placed on the back only) failed after 8 minutes: "one of your components is too large
  for Quilter to place within this board area". Quilter did not try the back side, so for M1 use job A.
