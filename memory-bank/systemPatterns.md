# System Patterns: NES Hardware Clone (Amaranth HDL)
*Version: 1.0*
*Created: 2026-04-20*
*Last Updated: 2026-04-20*

## Architecture Overview

The system models the NES as synthesizable digital hardware using Amaranth HDL. Each major chip (CPU, PPU, APU) is an independent `Elaboratable` module connected via a shared system bus. The architecture mirrors the real NES hardware topology: a CPU-side bus for program memory, registers, and RAM, and a PPU-side bus for VRAM and pattern tables.

```
┌─────────────────────────────────────────────────────┐
│                    System Bus                        │
│  addr[16], data_in[8], data_out[8], we, re          │
├──────┬──────┬──────┬──────┬──────┬──────────────────┤
│      │      │      │      │      │                  │
│  CPU │  PPU │  APU │ WRAM │  DMA │   Cartridge      │
│ 2A03 │ Regs │ Regs │ 2KB  │      │   Slot           │
│      │      │      │      │      │  (PRG + CHR ROM)  │
└──────┴──────┴──────┴──────┴──────┴──────────────────┘
                  │
          ┌───────┴───────┐
          │   PPU Bus     │
          │ (separate)    │
          ├───────┬───────┤
          │ VRAM  │ CHR   │
          │ 2KB   │ ROM   │
          └───────┴───────┘
```

## Key Components

| Component | Module | Purpose |
|---|---|---|
| CPU (Ricoh 2A03) | `cpu/cpu.py` | MOS 6502 core (no BCD), executes instructions via FSM |
| PPU (Ricoh 2C02) | `ppu/` (planned) | Generates 256x240 NTSC video, background + sprite rendering |
| APU | `apu/` (planned) | 5-channel audio: 2x Pulse, Triangle, Noise, DMC |
| System Bus | `bus/` (planned) | CPU memory map: address decoding, mirroring, register access |
| Cartridge | `cart/` (planned) | Mapper logic, PRG/CHR ROM banks, iNES header parsing |
| OAM DMA | Part of bus (planned) | 256-byte sprite data transfer from CPU RAM to PPU OAM |
| Memory (test) | `cpu/memory.py` | Simple 64KB sync RAM for testbench use |

## Design Patterns in Use

### Finite State Machine (FSM) Pattern
The CPU uses a multi-state FSM for instruction execution. Each state corresponds to a bus cycle (fetch opcode, fetch operand, calculate address, execute, write back). This maps directly to how the real 6502 pipelines bus operations.

**Current states:** `FETCH_OPCODE` -> `FETCH_OPERAND_1` -> `FETCH_OPERAND_2` -> `EXECUTE` -> `WRITE_BACK`

**Target:** Variable-length state sequences matching real 6502 cycle counts (2-7 cycles per instruction).

### Separation of Concerns
- `opcodes.py` -- pure data (opcode table mapping opcode byte -> mnemonic, addressing mode, cycle count)
- `addressing.py` -- combinational logic for effective address calculation (all 13 modes)
- `instructions.py` -- execution logic (register updates, flag setting, memory operations)
- `cpu.py` -- FSM orchestration tying everything together

### Bus Interface Pattern
All modules communicate through a standardized bus interface:
- 16-bit address bus (`addr`)
- 8-bit bidirectional data bus (`data_in`, `data_out`)
- Write enable (`we`)
- This enables composability: any module can be connected to the bus if it speaks this protocol.

### Testbench-Driven Development
Amaranth's `Simulator` API allows writing async Python testbenches that clock the hardware, inject stimuli, and assert on outputs. VCD waveforms provide visual debugging.

## Data Flow

### Instruction Execution (CPU)
```
1. PC -> addr bus -> memory -> data_in -> IR (opcode latch)
2. PC+1 -> addr bus -> memory -> data_in -> operand low byte
3. PC+2 -> addr bus -> memory -> data_in -> operand high byte (if needed)
4. Addressing mode logic -> effective address
5. Effective address -> addr bus -> memory -> data_in (for reads)
   OR result -> data_out -> addr bus (for writes)
6. Update registers, flags, PC
```

### NES System (planned)
```
CPU clock (1.789773 MHz) drives CPU and APU
PPU clock (3x CPU = 5.369319 MHz) drives PPU
Each CPU cycle: bus arbitration -> address decode -> read/write to target
PPU renders scanlines, triggers NMI at vblank (line 241)
DMA halts CPU for 513 cycles during OAM transfer
```

## Key Technical Decisions

| Decision | Rationale |
|---|---|
| Amaranth HDL over raw Verilog | Python-based HDL enables rapid iteration, testbench reuse, and higher-level abstractions while still producing synthesizable RTL |
| Build CPU from scratch | Educational value, full control over cycle accuracy, deeper understanding of 6502 architecture |
| FSM-based CPU (not microcode) | Simpler to reason about, maps directly to bus cycle behavior, easier to verify against timing documentation |
| Separate addressing/instruction modules | Keeps `cpu.py` manageable, allows independent testing of address calculation and instruction logic |
| Verilator before FPGA | Faster development iteration; FPGA synthesis is an eventual target, not the primary development loop |
| Klaus Dormann suite as gate | Industry-standard 6502 verification; passing it gives high confidence in CPU correctness before system integration |

## Component Relationships

```
cpu.py (FSM orchestrator)
  ├── imports opcodes.py (opcode table lookup)
  ├── calls addressing.py:AddressingMode.calculate() (effective address)
  └── calls instructions.py:Instructions.execute() (register/flag/memory updates)

emulator/generate.py
  └── imports cpu.py:CPU, calls amaranth verilog.convert()

tests/CPU/test_cpu.py
  ├── imports cpu.py:CPU
  ├── imports cpu/memory.py:Memory
  └── uses Amaranth Simulator API
```

**Unused/stale modules** (identified during project discovery):
- `cpu/alu.py` -- pure Python ALU helpers, not integrated into Amaranth signal flow
- `cpu/decoder.py` -- references API that doesn't match current `instructions.py`
- `cpu/registers.py` -- standalone register class, superseded by inline signals in `cpu.py`

---

*This document captures the system architecture and design patterns used in the project.*
