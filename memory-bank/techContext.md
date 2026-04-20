# Technical Context: NES Hardware Clone (Amaranth HDL)
*Version: 1.0*
*Created: 2026-04-20*
*Last Updated: 2026-04-20*

## Technology Stack

| Layer | Technology | Notes |
|---|---|---|
| HDL Framework | **Amaranth HDL** | Python-based hardware description language (successor to nMigen) |
| Language | **Python 3.14** | Used for hardware description, testbenches, and build scripts |
| Verilog Backend | **Yosys** | Required by Amaranth's `verilog.convert()` for RTL synthesis |
| Simulation (Python) | **Amaranth Simulator** | Built-in async testbench API with VCD waveform output |
| Simulation (C++) | **Verilator** | Compiles generated Verilog to cycle-accurate C++ model |
| Frontend | **SDL2** (2.32.10 installed) | Video rendering, audio playback, and controller input |
| Build System | **GNU Make** | Orchestrates venv, simulation, Verilog generation, and C++ build |
| FPGA Toolchain | TBD | Target board and toolchain to be selected later |

## Development Environment Setup

### Prerequisites
- Python 3.11+ (3.14 used in development)
- Yosys (for Amaranth Verilog backend) -- **NOT YET INSTALLED**
- Verilator (for C++ simulation) -- **NOT YET INSTALLED**
- SDL2 development headers -- installed (2.32.10)

### Setup Steps
```bash
# Recreate the Python virtual environment (existing venv was built on Linux)
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install amaranth amaranth-boards

# Install Yosys (required for Verilog generation)
# macOS: brew install yosys
# Linux: apt install yosys

# Install Verilator (required for C++ simulation, Phase 5)
# macOS: brew install verilator
# Linux: apt install verilator

# Run testbenches
make sim
```

### Known Environment Issues
- The existing `venv/` was created on Linux (ELF x86-64 binaries) and is not usable on macOS. It must be recreated.
- `emulator/generate.py` contains a hardcoded absolute path (`/var/home/dkeller/Desktop/hdl`) that should be made relative.
- The Makefile `sim` target points to `tests/test_cpu.py` but the actual test file is at `tests/CPU/test_cpu.py`.

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `amaranth` | latest | Core HDL framework for hardware description in Python |
| `amaranth-boards` | latest | Board support packages for FPGA targets |
| Yosys | latest | Synthesis backend for Verilog generation |
| Verilator | latest | Verilog-to-C++ compiler (Phase 5) |
| SDL2 | 2.32.10 | Video/audio/input for emulator frontend (Phase 5) |

## Technical Constraints
- Amaranth HDL requires all hardware logic to be expressed as `Elaboratable` modules with combinational and synchronous statements -- no imperative Python at synthesis time
- The Ricoh 2A03 omits BCD mode from the standard 6502; our CPU must match this behavior
- Cycle accuracy is required: each instruction must take the correct number of clock cycles as the real 6502
- The PPU and CPU run on different clock domains (PPU at 3x CPU clock) -- this must be handled in the system integration
- Verilator simulation speed is the practical constraint for development iteration time

## Build and Deployment
- **Build Process**: `make verilog` generates Verilog from Amaranth; `make verilate` compiles with Verilator; `make emulator` produces the final binary
- **Simulation**: `make sim` runs Python-based Amaranth testbenches
- **FPGA Deployment**: TBD -- Amaranth supports multiple FPGA platforms via `amaranth-boards`

## Testing Approach
- **Unit Testing**: Amaranth's built-in `Simulator` with async Python testbenches, VCD waveform output for debugging
- **Integration Testing**: Klaus Dormann's 6502 functional test suite (must pass before moving past Phase 2)
- **System Testing**: nestest.nes ROM, blargg's PPU test ROMs (Phase 4+)
- **Manual Testing**: Run NROM games through Verilator + SDL2 frontend, visual verification

---

*This document describes the technologies used in the project and how they're configured.*
