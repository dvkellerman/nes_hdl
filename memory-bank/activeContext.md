# Active Context: NES Hardware Clone (Amaranth HDL)
*Version: 2.0*
*Created: 2026-04-20*
*Last Updated: 2026-04-20*
*Current RIPER Mode: RESEARCH*

## Current Focus
Phase 2: CPU Core (Ricoh 2A03 / MOS 6502 without BCD). The CPU module has been fully refactored to use Amaranth's Component/wiring system with a clean submodule architecture. All legal 6502 opcodes now have execution logic. The remaining work is correctness: cycle-accurate timing, proper PC handling, and passing the Dormann test suite.

## Session Summary (2026-04-20)

### Completed
- START phase: Memory Bank initialized, project documented
- Cleanup: Removed 32 LLM-polluted files, added .gitignore, created README
- Makefile: Fixed to use Homebrew Python 3.14, amaranth[builtin-yosys], correct paths
- **CPU Component Refactor**: Rewrote CPU and Memory as Amaranth `Component` with `In`/`Out` ports
- **Instruction Deduplication**: Replaced 373-line monolithic instructions.py with `cpu/instructions/` package (facade + 6 group files), all under 200 lines
- **New instructions added**: ADC, SBC, AND, ORA, EOR, CMP, CPX, CPY, BIT, ASL, LSR, ROL, ROR, BRK, RTI, DEY
- **Auto-generated addr-mode decode**: `_decode_addr_mode` now reads from OPCODES table, eliminating hand-maintained duplicate
- **Reusable CpuBus Signature**: Shared `Signature` in `cpu/bus_sig.py` enables `connect()` wiring between modules
- **Signal rename**: `data_in`/`data_out` -> `data_rd`/`data_wr` for clarity, accessed via `cpu.bus.*`

### Recommended Changes Status
| # | Issue | Status |
|---|---|---|
| 1 | Elaboratable -> Component | Done |
| 2 | Instruction duplication | Done |
| 3 | Opcode->addr-mode mapping duplicated | Done |
| 4 | Static methods passing m/cpu | Done (plain functions) |
| 5 | Circular import | Done |
| 6 | Memory shadows Amaranth's Memory | Done (SyncRAM) |
| 7 | No reusable bus Signature | Done (CpuBus) |
| 8 | Stale modules (alu.py, decoder.py, registers.py) | Deferred |

## What's Still On The Table (Phase 2: CPU Core)

### Blocking: Environment
| Task | Status | Notes |
|---|---|---|
| Recreate Python venv | Not done | `make deepclean && make venv` -- existing venv has Linux binaries |

### High Priority: Correctness
| Task | Status | Notes |
|---|---|---|
| Fix FSM cycle timing | Not started | Every instruction currently takes exactly 5 cycles; real 6502 is 2-7 cycles per instruction |
| Fix PC advancement | Not started | Currently always advances 3 bytes; 1-byte (implied) and 2-byte (immediate/zp/rel) instructions over-read |
| Fix JSR | Not started | Only pushes high byte of return address, doesn't set PC to target |
| Fix RTS | Not started | Only increments SP, doesn't pull return address or set PC |
| Fix indirect addressing (IZX, IZY) | Not started | Needs double memory reads (read pointer, then read from pointer) |
| Fix JMP indirect | Not started | Simplified stub; doesn't emulate the 6502 page-boundary bug |

### Medium Priority: Completeness
| Task | Status | Notes |
|---|---|---|
| BRK implementation | Stub only | Sets B and I flags but doesn't push PC/status or read IRQ vector |
| RTI implementation | Stub only | Pulls status but doesn't pull PC |

### Low Priority: Cleanup
| Task | Status | Notes |
|---|---|---|
| Remove stale modules | Deferred | `cpu/alu.py`, `cpu/decoder.py`, `cpu/registers.py` are dead code |

### Gate: Testing
| Task | Status | Notes |
|---|---|---|
| Klaus Dormann 6502 test suite | Blocked | Requires all above correctness fixes first |

## Architecture After Refactor

```
cpu/
├── bus_sig.py              CpuBus Signature (shared bus interface)
├── cpu.py                  CPU Component (FSM, 130 lines)
├── opcodes.py              Opcode table + helpers (84 lines)
├── addressing.py           Effective address calculation (79 lines)
├── memory.py               SyncRAM Component (37 lines)
├── alu.py                  [STALE] unused pure-Python ALU
├── decoder.py              [STALE] broken, wrong imports
├── registers.py            [STALE] unused register class
└── instructions/
    ├── __init__.py          Facade: operand resolution + dispatch (34 lines)
    ├── loads_stores.py      LDA, LDX, LDY, STA, STX, STY (52 lines)
    ├── alu.py               ADC, SBC, AND, ORA, EOR, CMP, CPX, CPY, BIT (101 lines)
    ├── inc_dec.py           INC, DEC, INX, DEX, INY, DEY (70 lines)
    ├── shifts.py            ASL, LSR, ROL, ROR (95 lines)
    ├── control.py           Branches, JMP, JSR, RTS, BRK, RTI, NOP (90 lines)
    └── stack.py             Stack ops, transfers, flag ops (117 lines)
```

## Next Steps (Priority Order)
1. Recreate venv: `make deepclean && make venv`
2. Run test: `make sim` to verify LDA #$05 still works after refactor
3. Tackle FSM cycle timing + PC advancement (the big architectural fix)
4. Fix JSR/RTS to properly push/pull return addresses
5. Fix indirect addressing modes
6. Integrate Klaus Dormann test suite

---

*This document captures the current state of work and immediate next steps.*
