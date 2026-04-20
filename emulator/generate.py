#!/usr/bin/env python3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from amaranth.back import verilog
from cpu.cpu import CPU

def main() -> None:
    top = CPU(read_only=False)

    ports = [
        top.clk, top.rst,
        top.addr, top.data_in, top.data_out, top.we,
        top.irq, top.nmi, top.rdy,
        top.a, top.x, top.y, top.sp, top.pc, top.p,
        top.flag_n, top.flag_v, top.flag_b, top.flag_d,
        top.flag_i, top.flag_z, top.flag_c
    ]

    build_dir = PROJECT_ROOT / "build"
    build_dir.mkdir(exist_ok=True)
    output_path = build_dir / "cpu.v"

    try:
        output = verilog.convert(top, ports=ports)
        output_path.write_text(output)
        print(f"Verilog generated successfully at {output_path}")
    except Exception as e:
        print(f"Verilog generation failed: {e}")
        print("This is expected if Yosys is not installed")

if __name__ == "__main__":
    main()