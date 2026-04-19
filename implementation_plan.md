# Amaranth HDL NES Hardware Emulator Plan

This document outlines the phased approach to building a Nintendo Entertainment System (NES) hardware clone using Amaranth HDL, compiling it to Verilog, and running it as a cycle-accurate software emulator via Verilator and SDL2.

## User Review Required
> [!IMPORTANT]
> Since this is a massive hardware project, we need to agree on the starting point. Do you want to start by building the CPU from scratch, or would you prefer we integrate an existing open-source Amaranth 6502 core so we can focus on the PPU and system integration?
> Please review the phases below and let me know if this structured approach looks good to you.

## Proposed Changes

We will tackle this project in distinct, testable phases. The project directory structure will look roughly like this:

```text
/nes_hdl
  /cpu        # Ricoh 2A03 (6502 core)
  /ppu        # Ricoh 2C02 (Graphics)
  /apu        # Audio Processing Unit
  /bus        # Memory mapping and interconnects
  /cart       # Mappers (MMC1, etc.) and ROM loading
  /tests      # Amaranth Python testbenches
  /emulator   # C++ Verilator wrapper and SDL2 frontend
```

---

### Phase 1: Environment & Toolchain Setup
- Set up a Python virtual environment and install Amaranth HDL (`amaranth`, `amaranth-boards`).
- Install Verilator and SDL2 development headers for the C++ frontend.
- Create a basic "Hello World" Amaranth module (e.g., a blinking LED or counter), verilate it, and verify the build pipeline works.

### Phase 2: The CPU Core (Ricoh 2A03)
- Implement a MOS 6502 compatible CPU core in Amaranth (omitting BCD mode to match the Ricoh 2A03).
- **Verification:** Write Python testbenches to execute Klaus Dormann's 6502 functional test suite. The CPU *must* pass this suite before moving on.

### Phase 3: The System Bus & Memory Map
- Implement the CPU memory bus.
- Add internal Work RAM (2KB mirrored).
- Create a basic cartridge interface that can load NROM (Mapper 0) games (like *Super Mario Bros.* or *Donkey Kong*).
- Implement CPU-side DMA (Direct Memory Access) for sprite transfers (OAM DMA).

### Phase 4: The PPU (Ricoh 2C02)
- This is the most complex phase.
- Implement PPU memory bus (VRAM, Palettes).
- Implement background rendering (Nametables, Attribute tables, scrolling).
- Implement sprite rendering (OAM, sprite evaluation).
- Expose the VGA/HDMI pixel stream interface.
- **Verification:** Use blargg's PPU test ROMs.

### Phase 5: The C++ / Verilator Frontend
- Write an Amaranth script to generate `nes_system.v` containing the CPU, PPU, Bus, and Cartridge slot.
- Write a C++ wrapper (`main.cpp`) that:
  - Instantiates the Verilated NES model.
  - Opens an SDL2 window.
  - Clocks the simulation and reads pixel data from the PPU output pins.
  - Renders the pixels to the SDL2 texture.
  - Maps PC keyboard keys to NES controller shift register inputs.

### Phase 6: The APU (Audio) & Advanced Mappers
- Implement the 5 APU audio channels (Pulse 1 & 2, Triangle, Noise, DMC).
- Route audio output through Verilator to SDL2 audio streams.
- Implement more complex mappers (MMC1, MMC3) to support later games.

## Verification Plan

### Automated Tests
- We will rely heavily on Amaranth's built-in Python simulator for unit testing individual modules (e.g., testing that the CPU correctly executes an `ADC` instruction).
- We will run established community test ROMs (Klaus 6502, nestest, blargg's PPU tests) in headless simulations.

### Manual Verification
- We will run standard NROM games (e.g., *Donkey Kong*) through the Verilator C++ frontend and visually confirm graphics, input response, and audio.
