#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

from cpu.cpu import CPU

async def bench(ctx):
    cpu = CPU(read_only=False)
    
    print("=== CPU Reset Debug Test ===")
    
    # Test 1: Check initial state (before any clock)
    print(f"Initial: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    
    # Apply reset and clock
    print("\n--- Applying Reset ---")
    ctx.set(cpu.rst, 1)
    print(f"After setting rst=1: rst={ctx.get(cpu.rst)}")
    
    await ctx.tick()
    print(f"After 1st tick: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    
    await ctx.tick()
    print(f"After 2nd tick: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    
    # Release reset
    print("\n--- Releasing Reset ---")
    ctx.set(cpu.rst, 0)
    print(f"After setting rst=0: rst={ctx.get(cpu.rst)}")
    
    await ctx.tick()
    print(f"After 1st tick with rst=0: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    
    await ctx.tick()
    print(f"After 2nd tick with rst=0: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    
    # Let it run a bit more
    for i in range(5):
        await ctx.tick()
        if i % 2 == 0:
            print(f"After {i+3} total ticks: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")

def main() -> None:
    sim = Simulator(CPU(read_only=False))
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    with sim.write_vcd("debug_reset.vcd"):
        sim.run()
    print("\nSimulation complete")

if __name__ == "__main__":
    main()