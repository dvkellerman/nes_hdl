#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth.back import verilog
from cpu.cpu import CPU

def main() -> None:
    # Create CPU instance
    top = CPU(read_only=False)
    
    # Define ports for Verilog generation
    ports = [
        top.clk, top.rst,
        top.addr, top.data_in, top.data_out, top.we,
        top.irq, top.nmi, top.rdy,
        top.a, top.x, top.y, top.sp, top.pc, top.p,
        top.flag_n, top.flag_v, top.flag_b, top.flag_d, 
        top.flag_i, top.flag_z, top.flag_c
    ]
    
    # Convert to Verilog
    try:
        output = verilog.convert(top, ports=ports)
        with open("/var/home/dkeller/Desktop/hdl/build/cpu.v", "w") as f:
            f.write(output)
        print("Verilog generated successfully at /var/home/dkeller/Desktop/hdl/build/cpu.v")
    except Exception as e:
        print(f"Verilog generation failed: {e}")
        print("This is expected if Yosys is not installed")

if __name__ == "__main__":
    main()