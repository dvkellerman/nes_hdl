#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

class MinimalCPU(Elaboratable):
    def __init__(self) -> None:
        self.clk = Signal()
        self.rst = Signal()
        self.pc = Signal(16)
    
    def elaborate(self, platform):
        m = Module()
        
        # Reset logic - this should work
        with m.If(self.rst):
            m.d.sync += self.pc.eq(0xFFFC)
        with m.Else():
            m.d.sync += self.pc.eq(self.pc + 1)  # Just increment when not in reset
        
        return m

async def bench(ctx):
    cpu = MinimalCPU()
    
    print("Testing minimal reset logic:")
    print(f"Initial: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    
    # Apply reset
    ctx.set(cpu.rst, 1)
    await ctx.tick()
    print(f"After reset applied: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    
    # Release reset
    ctx.set(cpu.rst, 0)
    await ctx.tick()
    print(f"After reset released: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    
    # A few more ticks
    for i in range(3):
        await ctx.tick()
        print(f"After {i+1} more tick(s): rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")

def main():
    sim = Simulator(MinimalCPU())
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    with sim.write_vcd("minimal_reset_test.vcd"):
        sim.run()
    print("\nSimulation complete")

if __name__ == "__main__":
    main()