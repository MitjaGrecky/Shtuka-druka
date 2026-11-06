# Shtuka Druka

An open, standalone desktop music instrument: synthesizer, sampler and DAW in one box.
The idea is improvising with sound from everywhere: capture audio from any source,
then shape it with filters and effects.

[![KiCad checks](https://github.com/MitjaGrecky/Shtuka-druka/actions/workflows/kicad.yml/badge.svg)](https://github.com/MitjaGrecky/Shtuka-druka/actions/workflows/kicad.yml)

Status: design phase. Panel layout v7, enclosure, I/O, audio chain and compute platform are decided.
First board: M1 screen knobs module (being routed). Next: W1 Levels, then a 1:1 cardboard mockup.

## What is here

| Folder | Contents |
|---|---|
| `docs/ru/` | Research and design documents (Russian). Start with `README.md` (map of documents) and `decisions/README.md` — the single source of truth for every decision, split by topic |
| `bench/` | CPU benchmark: how many reference tracks a processor can run at 48 kHz / 128 samples |
| `mockup/` | 1:1 cardboard mockup templates (A4, PDF) and the script that generates them |
| `model3d/` | Interactive 3D model of panel v7, built from `mockup/layout/layout_v7.json` (open `index.html` in a browser; rebuild with `build_model3d_v7.py`) |
| `firmware/protocol/` | Board <-> computer protocol (SDP v0): C header for firmware and host |
| `tools/` | `sdp.py`: reference codec, self-test and frame monitor |
| `hardware/` | KiCad boards, generated from Python (`gen/`), checked by CI: `m1-screen-knobs` (first board), `w1-levels` |
| `notes/handoff.md` | Task queue between the cloud and local Claude sessions (rules in `CLAUDE.md`) |
| `.github/workflows/` | CI: ERC, DRC with schematic parity, BOM, Gerbers for every board on every push |

## Key facts

- 8x8 RGB pad grid, 16+ tracks (target 32-64), endless encoders with LED rings, 10.1" screen at 30 deg
- Body 515 x 460 mm, 68 mm high at the front, 143 mm at the rear, 30 deg slope for the screen, detachable wrist rest
- Inputs: 2 combo XLR/TRS, 2 Hi-Z, phono with RIAA, 8 line inputs, USB audio, 2-4 CV
- Converters: Cirrus Logic Pro (CS5308P/CS5304P ADC, CS4308P DAC), two-path inputs without a preamp chip
- Outputs: Main and Aux (balanced TRS), RCA copy of Main, 2 headphones
- MIDI: 2 in / 4 out DIN, 1 in / 2 out TRS (type A/B switchable); 8 CV/Gate, sync block, Ableton Link
- Compute: x86 on a Mini-ITX board (Intel N100 to start, 8-core upgrade on the same mounts)
- Two RP2350 boards (panel, control) over internal USB; audio board on two xcore.ai, USB Audio Class 2

## Licenses

- Software: GNU AGPL-3.0-or-later (`LICENSE`)
- Hardware: CERN-OHL-S-2.0 (`hardware/LICENSE`)

---

Штука Дрюка — открытый настольный инструмент: синтезатор, сэмплер и DAW в одном корпусе.
Документы проекта на русском лежат в `docs/ru/`, карта документов — `docs/ru/README.md`, все решения — в `docs/ru/decisions/` (начинать с `README.md`).
