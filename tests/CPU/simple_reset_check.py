#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

from cpu.cpu import CPU

async def bench(ctx) -> None:
    cpu = CPU(read_only=False)
    
    # Let's trace the reset signal and PC over several cycles
    print("Cycle: rst, pc")
    for i in range(10):
        await ctx.tick()
        rst = ctx.get(cpu.rst)
        pc = ctx.get(cpu.pc)
        print(f"{i:2d}: {rst}, 0x{pc:04X}")

def main() -> None:
    # Test 1: Check reset behavior
    print("=== Test 1: Applying reset at start ===")
    sim = Simulator(CPU(read_only=False))
    
    async def test1(ctx):
        cpu = CPU(read_only=False)
        # Apply reset from the beginning
        ctx.set(cpu.rst, 1)
        for i in range(5):
            await ctx.tick()
            rst = ctx.get(cpu.rst)
            pc = ctx.get(cpu.pc)
            print(f"  {i}: rst={rst}, pc=0x{pc:04X}")
        
        # Release reset
        ctx.set(cpu.rst, 0)
        for i in range(5):
            await ctx.tick()
            rst = ctx.get(cpu.rst)
            pc = ctx.get(cpu.pc)
            print(f"  {i+5}: rst={rst}, pc=0x{pc:04X}")
    
    sim.add_testbench(test1)
    sim.add_clock(1e-6)
    with sim.write_vcd("test1.vcd"):
        sim.run()
    
    print("\n=== Test 2: Applying reset after a few cycles ===")
    sim2 = Simulator(CPU(read_only=False))
    
    async def test2(ctx):
        cpu = CPU(read_only=False)
        # Let it run for a few cycles first
        for i in range(3):
            await ctx.tick()
            rst = ctx.get(cpu.rst)
            pc = ctx.get(cpu.pc)
            print(f"  {i}: rst={rst}, pc=0x{pc:04X}")
        
        # Apply reset
        ctx.set(cpu.rst, 1)
        for i in range(3):
            await ctx.tick()
            rst = ctx.get(cpu.rst)
            pc = ctx.get(cpu.pc)
            print(f"  {i+3}: rst={rst}, pc=0x{pc:04X}")
        
        # Release reset
        ctx.set(cpu.rst, 0)
        for i in range(3):
            await ctx.tick()
            rst = ctx.get(cpu.rst)
            pc = ctx.get(cpu.pc)
            print(f"  {i+6}: rst={rst}, pc=0x{pc:04X}")
    
    sim2.add_testbench(test2)
    sim2.add_clock(1e-6)
    with sim2.write_vcd("test2.vcd"):
        sim2.run()

if __name__ == "__main__":
    main()