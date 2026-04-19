#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

from cpu.cpu import CPU

async def bench(ctx):
    cpu = CPU(read_only=False)
    
    # Test 1: Check initial values
    print("Initial state:")
    print(f"  PC: 0x{ctx.get(cpu.pc):04X}")
    print(f"  State: {ctx.get(cpu.state)}")
    print(f"  RST: {ctx.get(cpu.rst)}")
    
    # Apply reset
    ctx.set(cpu.rst, 1)
    await ctx.tick()
    print("\nAfter reset (rising edge):")
    print(f"  PC: 0x{ctx.get(cpu.pc):04X} (expected: 0xFFFC)")
    print(f"  State: {ctx.get(cpu.state)} (expected: 0)")
    print(f"  SP: 0x{ctx.get(cpu.sp):02X} (expected: 0xFD)")
    print(f"  Flag I: {ctx.get(cpu.flag_i)} (expected: 1)")
    
    # Release reset
    ctx.set(cpu.rst, 0)
    await ctx.tick()
    print("\nAfter releasing reset:")
    print(f"  PC: 0x{ctx.get(cpu.pc):04X}")
    print(f"  State: {ctx.get(cpu.state)}")
    
    # Run a few more cycles
    for i in range(5):
        await ctx.tick()
        if i % 2 == 0:
            print(f"\nAfter {i+1} more clock cycles:")
            print(f"  PC: 0x{ctx.get(cpu.pc):04X}")
            print(f"  State: {ctx.get(cpu.state)}")

def main():
    sim = Simulator(CPU(read_only=False))
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    with sim.write_vcd("simple_test.vcd"):
        sim.run()
    print("\nSimulation complete")

if __name__ == "__main__":
    main()