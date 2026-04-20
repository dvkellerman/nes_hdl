# Project Brief: NES Hardware Clone (Amaranth HDL)
*Version: 1.0*
*Created: 2026-04-20*
*Last Updated: 2026-04-20*

## Project Overview
A cycle-accurate Nintendo Entertainment System (NES) hardware clone implemented in Amaranth HDL (Python-based hardware description language). The project produces synthesizable RTL that compiles to Verilog, runs as a software emulator via Verilator + SDL2, and eventually targets real FPGA hardware.

## Core Requirements
- Implement a MOS 6502-compatible CPU core (Ricoh 2A03, no BCD mode) from scratch in Amaranth HDL
- Implement the PPU (Ricoh 2C02) for background and sprite rendering
- Implement the APU for audio (5 channels: Pulse x2, Triangle, Noise, DMC)
- Implement the system bus with NES memory map (2KB WRAM, mirroring, OAM DMA)
- Support cartridge loading with NROM (Mapper 0) at minimum, MMC1/MMC3 later
- Generate Verilog from Amaranth and run via Verilator as a cycle-accurate software emulator
- Provide an SDL2-based frontend for video, audio, and controller input
- Eventually synthesize to real FPGA hardware

## Success Criteria
- CPU passes Klaus Dormann's 6502 functional test suite
- System can boot and run NROM games (Donkey Kong, Super Mario Bros.)
- PPU passes blargg's PPU test ROMs
- Verilator + SDL2 frontend renders video, plays audio, and accepts input
- Generated Verilog is synthesizable to an FPGA target

## Scope

### In Scope
- Full 6502 CPU core (all legal opcodes, correct cycle timing)
- PPU with background rendering, sprite rendering, scrolling
- APU with all 5 audio channels
- System bus, memory map, and DMA
- Cartridge interface with Mapper 0 (NROM), Mapper 1 (MMC1), Mapper 4 (MMC3)
- Verilator C++ wrapper with SDL2 frontend
- FPGA synthesis support
- Python-based Amaranth testbenches and community test ROM verification

### Out of Scope
- Illegal/undocumented 6502 opcodes (may add later)
- Famicom Disk System support
- Expansion audio chips (VRC6, Namco 163, etc.)
- Netplay or save states in the emulator frontend
- GUI-based emulator (SDL2 window only)

## Timeline
- Hobby project with no fixed deadline; quality and correctness over speed
- Phase 2 (CPU Core): Current focus
- Phase 3 (Bus & Memory): After CPU passes Dormann suite
- Phase 4 (PPU): After system bus is working
- Phase 5 (Verilator Frontend): After PPU renders frames
- Phase 6 (APU & Mappers): After basic games are playable

## Stakeholders
- Dmitriy Keller: Sole developer and project owner

---

*This document serves as the foundation for the project and informs all other memory files.*
