#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

from cpu.cpu import CPU

async def bench(ctx):
    cpu = CPU(read_only=False)
    
    print("Reset signal test:")
    # Apply reset
    ctx.set(cpu.rst, 1)
    print(f"After setting rst=1 (before tick): rst={ctx.get(cpu.rst)}")
    await ctx.tick()
    print(f"After first tick: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    await ctx.tick()
    print(f"After second tick: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    await ctx.tick()
    print(f"After third tick: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    
    # Release reset
    ctx.set(cpu.rst, 0)
    print(f"After setting rst=0 (before tick): rst={ctx.get(cpu.rst)}")
    await ctx.tick()
    print(f"After tick with rst=0: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")

def main():
    sim = Simulator(CPU(read_only=False))
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    with sim.write_vcd("reset_test.vcd"):
        sim.run()
    print("\nSimulation complete")

if __name__ == "__main__":
    main()