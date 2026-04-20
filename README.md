# NES Hardware Clone — Amaranth HDL

A cycle-accurate Nintendo Entertainment System (NES) hardware clone written in [Amaranth HDL](https://amaranth-lang.org/). Produces synthesizable RTL that compiles to Verilog for software emulation via [Verilator](https://www.veripool.org/verilator/) + SDL2, with eventual FPGA targeting.

## Status

**Phase 2: CPU Core** — building the Ricoh 2A03 (MOS 6502 without BCD) from scratch.

## Project Structure

```
cpu/          Ricoh 2A03 — 6502 CPU core
ppu/          Ricoh 2C02 — Picture Processing Unit (planned)
apu/          Audio Processing Unit (planned)
bus/          System bus, memory map, DMA (planned)
cart/         Cartridge mappers and ROM loading (planned)
emulator/     Verilog generation and C++ Verilator/SDL2 frontend
tests/        Amaranth Python testbenches
build/        Generated Verilog output
memory-bank/  Project documentation and context
```

## Prerequisites

- Python 3.14 (via Homebrew: `brew install python@3.14`)
- SDL2 (`brew install sdl2`) — for the frontend (Phase 5)
- Verilator (`brew install verilator`) — for C++ simulation (Phase 5)

Yosys is bundled automatically via `amaranth[builtin-yosys]`.

## Quick Start

```bash
make venv        # create venv + install amaranth with builtin yosys
make sim          # run CPU testbenches
make verilog      # generate Verilog from Amaranth
```

## Roadmap

1. ~~Environment & toolchain setup~~
2. **CPU core** ← current
3. System bus & memory map
4. PPU (graphics)
5. Verilator + SDL2 frontend
6. APU (audio) & advanced mappers
