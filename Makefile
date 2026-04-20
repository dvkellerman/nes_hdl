# NES Emulator in Amaranth HDL Makefile

# Python environment
PYTHON3 = /opt/homebrew/opt/python@3.14/bin/python3.14
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Verilator configuration
VERILATOR = verilator
VERILATOR_FLAGS = -cc --exe -Wall --trace
SDL2_FLAGS = `sdl2-config --cflags --libs`

.PHONY: all venv sim verilog verilate emulator clean deepclean

all: venv

# Setup Python Virtual Environment
venv:
	rm -rf venv
	@echo "Setting up Python virtual environment..."
	$(PYTHON3) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install 'amaranth[builtin-yosys]' amaranth-boards

# Run pure Python Amaranth testbenches
sim: venv
	@echo "Running Amaranth simulations..."
	$(PYTHON) tests/CPU/test_cpu.py

# Generate Verilog from Amaranth
verilog: venv
	@echo "Generating Verilog..."
	mkdir -p build
	$(PYTHON) emulator/generate.py

# Compile Verilog using Verilator
verilate: verilog
	@echo "Verilating..."
	$(VERILATOR) $(VERILATOR_FLAGS) build/nes_system.v emulator/main.cpp

# Build the final C++ Emulator
emulator: verilate
	@echo "Building C++ Emulator..."
	make -j`nproc` -C obj_dir -f Vnes_system.mk Vnes_system

# Clean generated files
clean:
	@echo "Cleaning up..."
	rm -rf build/
	rm -rf obj_dir/
	rm -rf __pycache__/
	rm -rf */__pycache__/

# Clean everything including the virtual environment
deepclean: clean
	@echo "Removing virtual environment..."
	rm -rf $(VENV)
