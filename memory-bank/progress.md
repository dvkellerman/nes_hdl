# Progress Tracker: NES Hardware Clone (Amaranth HDL)
*Version: 2.0*
*Created: 2026-04-20*
*Last Updated: 2026-04-20*

## Project Status
Overall Completion: ~15%

## What Works
- **Architecture**: CPU and Memory use Amaranth Component with proper In/Out ports and shared CpuBus Signature
- **Opcode table**: Complete -- 151 opcodes defined with mnemonic, addressing mode, and cycle count
- **Addressing modes**: All 13 modes have combinational effective-address logic
- **Instruction execution**: All legal 6502 opcodes have execution logic:
  - Loads: LDA, LDX, LDY (all addressing modes, deduplicated)
  - Stores: STA, STX, STY (all addressing modes)
  - ALU: ADC, SBC, AND, ORA, EOR (with carry/overflow flags)
  - Compare: CMP, CPX, CPY, BIT
  - Inc/Dec: INC, DEC (memory), INX, DEX, INY, DEY (registers)
  - Shifts: ASL, LSR, ROL, ROR (accumulator + memory)
  - Branches: BPL, BMI, BVC, BVS, BCC, BCS, BNE, BEQ
  - Jumps: JMP absolute/indirect (simplified), JSR (stub), RTS (stub)
  - Stack: PHA, PLA, PHP, PLP
  - Transfers: TAX, TXA, TAY, TYA, TSX, TXS
  - Flags: CLC, SEC, CLI, SEI, CLD, SED, CLV
  - Control: BRK (stub), RTI (stub), NOP
- **Addr-mode decode**: Auto-generated from OPCODES table (single source of truth)
- **Bus interface**: Reusable CpuBus Signature enables connect() wiring
- **Build pipeline**: Makefile with Homebrew Python 3.14 + builtin-yosys
- **Code quality**: Every file under 200 lines, no circular imports, no duplication

## What's In Progress
- FSM cycle accuracy: 0% -- every instruction still takes 5 fixed cycles
- PC advancement: 0% -- always advances 3 bytes regardless of instruction size
- JSR/RTS: Stubs -- don't properly push/pull return addresses
- BRK/RTI: Stubs -- don't do full interrupt sequence
- Indirect addressing: Simplified -- IZX/IZY don't do double memory reads

## What's Left To Build

### Phase 2: CPU Core (current)
- [ ] Variable cycle timing in FSM -- HIGH
- [ ] Correct PC advancement per instruction size -- HIGH
- [ ] Complete JSR (push both bytes of return addr, set PC) -- HIGH
- [ ] Complete RTS (pull return addr, set PC) -- HIGH
- [ ] Indirect addressing double-reads (IZX, IZY) -- MEDIUM
- [ ] JMP indirect page-boundary bug emulation -- MEDIUM
- [ ] Complete BRK (push PC+2, push P|B, read IRQ vector) -- MEDIUM
- [ ] Complete RTI (pull P, pull PC) -- MEDIUM
- [ ] Klaus Dormann test suite -- HIGH (gate for Phase 3)
- [ ] Remove stale modules (cpu/alu.py, cpu/decoder.py, cpu/registers.py) -- LOW

### Phase 3: System Bus & Memory Map
- [ ] CPU memory bus with address decoding
- [ ] 2KB Work RAM with mirroring
- [ ] NROM (Mapper 0) cartridge interface
- [ ] OAM DMA

### Phase 4: PPU (Ricoh 2C02)
- [ ] PPU memory bus, background/sprite rendering, scrolling, VBlank NMI

### Phase 5: Verilator + SDL2 Frontend
- [ ] Verilog generation, C++ wrapper, SDL2 video/input

### Phase 6: APU & Advanced Mappers
- [ ] 5 audio channels, MMC1/MMC3 mappers

## Known Issues
- **Venv broken on macOS**: Must run `make deepclean && make venv`. SEVERITY: Blocking for sim
- **Fixed 5-cycle FSM**: Fundamental correctness issue. SEVERITY: High
- **PC always advances 3**: Fundamental correctness issue. SEVERITY: High
- **Incomplete JSR/RTS**: Subroutine calls don't work. SEVERITY: High
- **Simplified indirect modes**: IZX/IZY produce wrong addresses. SEVERITY: Medium
- **Stale modules**: cpu/alu.py, cpu/decoder.py, cpu/registers.py are dead code. SEVERITY: Low

## Milestones
- [x] M0: Project scaffolded, Component architecture, all opcodes have execution logic
- [ ] M1: Variable cycle timing and correct PC handling
- [ ] M2: JSR/RTS/BRK/RTI fully working
- [ ] M3: Klaus Dormann 6502 functional test suite passes
- [ ] M4: System bus and NROM cartridge working
- [ ] M5: PPU renders first frame
- [ ] M6: First NROM game boots (Donkey Kong)
- [ ] M7: SDL2 frontend with video + input
- [ ] M8: APU audio working
- [ ] M9: FPGA synthesis

---

*This document tracks what works, what's in progress, and what's left to build.*
