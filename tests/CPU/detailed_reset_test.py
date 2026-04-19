#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

from cpu.cpu import CPU

async def bench(ctx):
    cpu = CPU(read_only=False)
    
    print("Detailed reset signal test:")
    
    # Check initial state
    print(f"Initial: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    
    # Apply reset
    print("\nApplying reset (setting rst=1)...")
    ctx.set(cpu.rst, 1)
    print(f"After setting rst=1: rst={ctx.get(cpu.rst)}")
    
    # First tick - reset should take effect on rising edge of clock
    print("Waiting for first clock tick...")
    await ctx.tick()
    print(f"After first tick: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    
    # Second tick - reset still active
    print("Waiting for second clock tick...")
    await ctx.tick()
    print(f"After second tick: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    
    # Release reset
    print("\nReleasing reset (setting rst=0)...")
    ctx.set(cpu.rst, 0)
    print(f"After setting rst=0: rst={ctx.get(cpu.rst)}")
    
    # Tick with reset released
    print("Waiting for clock tick with reset released...")
    await ctx.tick()
    print(f"After tick with rst=0: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    
    # Another tick
    print("Waiting for another clock tick...")
    await ctx.tick()
    print(f"After another tick: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")

def main():
    sim = Simulator(CPU(read_only=False))
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    with sim.write_vcd("detailed_reset_test.vcd"):
        sim.run()
    print("\nSimulation complete")

if __name__ == "__main__":
    main()