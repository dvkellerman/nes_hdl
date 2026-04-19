#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

from cpu.cpu import CPU

async def bench(ctx):
    cpu = CPU(read_only=False)
    
    print("=== CPU Reset Debug Test ===")
    
    # Show initial values
    print(f"Initial: PC=0x{ctx.get(cpu.pc):04X}, RST={ctx.get(cpu.rst)}")
    
    # Apply reset for multiple cycles
    print("\n--- Applying Reset ---")
    ctx.set(cpu.rst, 1)
    for i in range(5):
        await ctx.tick()
        pc = ctx.get(cpu.pc)
        sp = ctx.get(cpu.sp)
        flag_i = ctx.get(cpu.flag_i)
        state = ctx.get(cpu.state)
        print(f"  Cycle {i}: PC=0x{pc:04X}, SP=0x{sp:02X}, I={flag_i}, State={state}")
    
    # Release reset
    print("\n--- Releasing Reset ---")
    ctx.set(cpu.rst, 0)
    for i in range(5):
        await ctx.tick()
        pc = ctx.get(cpu.pc)
        sp = ctx.get(cpu.sp)
        flag_i = ctx.get(cpu.flag_i)
        state = ctx.get(cpu.state)
        print(f"  Cycle {i}: PC=0x{pc:04X}, SP=0x{sp:02X}, I={flag_i}, State={state}")

def main():
    sim = Simulator(CPU(read_only=False))
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    with sim.write_vcd("debug_test.vcd"):
        sim.run()
    print("\nSimulation complete")

if __name__ == "__main__":
    main()