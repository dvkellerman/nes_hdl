# Active Context: NES Hardware Clone (Amaranth HDL)
*Version: 1.0*
*Created: 2026-04-20*
*Last Updated: 2026-04-20*
*Current RIPER Mode: RESEARCH*

## Current Focus
Phase 2: CPU Core (Ricoh 2A03 / MOS 6502 without BCD). The CPU module has a working FSM skeleton with partial instruction support. The immediate priority is fixing fundamental correctness issues and completing the instruction set before running the Dormann test suite.

## Recent Changes
- 2026-04-20: START phase completed, Memory Bank initialized
- 2026-04-20: Fixed hardcoded paths in `emulator/generate.py` (now uses relative paths)
- 2026-04-20: Fixed Makefile `sim` target to point to correct test path
- 2026-04-20: Fixed Makefile `verilog` target (removed incorrect stdout redirect)
- 2026-04-20: Added `__init__.py` to all package directories

## Active Decisions
- CPU from scratch: CONFIRMED -- building the full 6502 core in Amaranth HDL
- Testing gate: CONFIRMED -- CPU must pass Klaus Dormann's 6502 functional test suite before moving to Phase 3
- FPGA target: CONFIRMED -- Verilator first, then FPGA synthesis later

## Next Steps
1. **Fix the FSM cycle count issue** -- currently all instructions take 5 cycles; must implement variable-length instruction execution matching real 6502 timing
2. **Fix PC advancement** -- currently always advances 3 bytes regardless of instruction size (1, 2, or 3 bytes)
3. **Implement missing ALU instructions** -- ADC, SBC, AND, ORA, EOR, BIT, CMP, CPX, CPY
4. **Implement shift/rotate instructions** -- ASL, LSR, ROL, ROR
5. **Fix JSR/RTS** -- currently incomplete (JSR doesn't push low byte; RTS doesn't pull return address)
6. **Implement BRK/RTI** -- interrupt handling
7. **Fix indirect addressing modes** -- IZX, IZY need proper double memory reads
8. **Clean up stale modules** -- decide whether to remove or integrate `alu.py`, `decoder.py`, `registers.py`
9. **Recreate the Python venv** -- existing one was built on Linux, not usable on macOS
10. **Install Yosys** -- needed for Verilog generation

## Current Challenges
- **Cycle accuracy**: The 5-state FSM forces every instruction into exactly 5 cycles. Redesigning the FSM for variable-length instruction execution is the biggest architectural challenge.
- **PC handling**: Tightly coupled to the fixed 5-state assumption; fixing cycle accuracy will also fix PC advancement.
- **Stale venv**: Must recreate on macOS before any Python simulation can run.
- **Missing Yosys**: Cannot generate Verilog until Yosys is installed.

## Implementation Progress
- [x] Opcode table (151 opcodes defined)
- [x] All 13 addressing modes (combinational logic)
- [x] Load instructions (LDA, LDX, LDY)
- [x] Store instructions (STA, STX, STY)
- [x] Inc/Dec memory (INC, DEC)
- [x] Inc/Dec registers (INX, DEX, INY, DEY)
- [x] Register transfers (TAX, TXA, TAY, TYA, TSX, TXS)
- [x] Flag instructions (CLC, SEC, CLI, SEI, CLD, SED, CLV)
- [x] Branch instructions (BPL, BMI, BVC, BVS, BCC, BCS, BNE, BEQ)
- [x] JMP (absolute, simplified indirect)
- [x] Stack ops (PHA, PLA, PHP, PLP)
- [x] NOP
- [x] Reset vector handling ($FFFC)
- [x] Basic test infrastructure
- [ ] ALU instructions (ADC, SBC, AND, ORA, EOR, BIT, CMP, CPX, CPY)
- [ ] Shift/rotate (ASL, LSR, ROL, ROR)
- [ ] Correct cycle timing per instruction
- [ ] Correct PC advancement per instruction size
- [ ] Complete JSR/RTS implementation
- [ ] BRK/RTI (interrupt handling)
- [ ] Indirect addressing double-reads (IZX, IZY)
- [ ] Klaus Dormann test suite integration
- [ ] Verilog generation (requires Yosys)

---

*This document captures the current state of work and immediate next steps.*
