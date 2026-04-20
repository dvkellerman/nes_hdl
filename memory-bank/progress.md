# Progress Tracker: NES Hardware Clone (Amaranth HDL)
*Version: 1.0*
*Created: 2026-04-20*
*Last Updated: 2026-04-20*

## Project Status
Overall Completion: ~10%

## What Works
- Opcode table: Complete -- 151 opcodes defined with mnemonic, addressing mode, and cycle count
- Addressing modes: Complete -- all 13 modes have combinational effective-address logic
- Basic instruction subset: ~50% of instructions have execution logic (loads, stores, inc/dec, transfers, flags, branches, jumps, stack ops, NOP)
- Reset vector: CPU reads from $FFFC on reset
- Test infrastructure: Amaranth Simulator testbench runs `LDA #$05` and verifies register state
- Build pipeline: Makefile with targets for venv, sim, verilog, verilate, emulator

## What's In Progress
- CPU instruction execution: 50% -- missing ALU ops, shifts, and correct JSR/RTS
- FSM cycle accuracy: 0% -- needs redesign from fixed 5-cycle to variable-length
- PC advancement logic: 0% -- needs to respect instruction byte count

## What's Left To Build

### Phase 2: CPU Core (current)
- [ ] ALU instructions (ADC, SBC, AND, ORA, EOR, BIT, CMP, CPX, CPY) -- HIGH
- [ ] Shift/rotate instructions (ASL, LSR, ROL, ROR) -- HIGH
- [ ] Variable cycle timing in FSM -- HIGH
- [ ] Correct PC advancement per instruction size -- HIGH
- [ ] Complete JSR/RTS -- HIGH
- [ ] BRK/RTI interrupt handling -- MEDIUM
- [ ] Indirect addressing double-reads -- MEDIUM
- [ ] Klaus Dormann test suite -- HIGH (gate for Phase 3)
- [ ] Clean up stale modules (alu.py, decoder.py, registers.py) -- LOW

### Phase 3: System Bus & Memory Map
- [ ] CPU memory bus with address decoding -- HIGH
- [ ] 2KB Work RAM with mirroring -- HIGH
- [ ] NROM (Mapper 0) cartridge interface -- HIGH
- [ ] OAM DMA -- MEDIUM

### Phase 4: PPU (Ricoh 2C02)
- [ ] PPU memory bus (VRAM, palettes) -- HIGH
- [ ] Background rendering (nametables, attribute tables, scrolling) -- HIGH
- [ ] Sprite rendering (OAM, sprite evaluation) -- HIGH
- [ ] VBlank NMI generation -- HIGH
- [ ] blargg's PPU test ROM verification -- HIGH

### Phase 5: Verilator + SDL2 Frontend
- [ ] Amaranth -> full system Verilog generation -- HIGH
- [ ] C++ Verilator wrapper -- HIGH
- [ ] SDL2 video rendering -- HIGH
- [ ] SDL2 controller input mapping -- MEDIUM
- [ ] SDL2 audio output (after APU) -- MEDIUM

### Phase 6: APU & Advanced Mappers
- [ ] Pulse channels (x2) -- MEDIUM
- [ ] Triangle channel -- MEDIUM
- [ ] Noise channel -- MEDIUM
- [ ] DMC channel -- LOW
- [ ] MMC1 mapper -- MEDIUM
- [ ] MMC3 mapper -- LOW

## Known Issues
- **Venv broken on macOS**: Existing venv was built on Linux (ELF x86-64). Must recreate. SEVERITY: Blocking
- **Missing Yosys**: Cannot generate Verilog. SEVERITY: Blocking for Phase 5, not for simulation
- **Missing Verilator**: Cannot compile C++ emulator. SEVERITY: Blocking for Phase 5 only
- **Fixed 5-cycle FSM**: Every instruction takes exactly 5 cycles regardless of real timing. SEVERITY: High -- fundamental correctness issue
- **PC always advances 3**: 1-byte and 2-byte instructions read beyond their operands. SEVERITY: High -- fundamental correctness issue
- **Incomplete JSR/RTS**: JSR only pushes high byte; RTS only increments SP. SEVERITY: High -- subroutine calls are broken
- **Stale modules**: `alu.py`, `decoder.py`, `registers.py` are unused and may cause confusion. SEVERITY: Low

## Milestones
- [ ] M1: All 6502 legal opcodes implemented with correct execution logic
- [ ] M2: Variable cycle timing and correct PC handling
- [ ] M3: Klaus Dormann 6502 functional test suite passes
- [ ] M4: System bus and NROM cartridge working
- [ ] M5: PPU renders first frame
- [ ] M6: First NROM game boots (Donkey Kong)
- [ ] M7: SDL2 frontend with video + input
- [ ] M8: APU audio working
- [ ] M9: FPGA synthesis

---

*This document tracks what works, what's in progress, and what's left to build.*
