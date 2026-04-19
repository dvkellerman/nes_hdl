#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

# Minimal CPU that should just increment PC
class MinimalCPU(Elaboratable):
    def __init__(self):
        self.rst = Signal()
        self.pc = Signal(16, init=0)
        self.addr = Signal(16)
        
    def elaborate(self, platform):
        m = Module()
        
        # Explicit conditional
        if_ = m.If(self.rst)
        with if_:
            m.d.sync += self.pc.eq(0xFFFC)
        with if_.Else():
            m.d.sync += self.pc.eq(self.pc + 1)
        
        m.d.comb += self.addr.eq(self.pc)
        
        return m

async def test_reset(ctx):
    cpu = MinimalCPU()
    
    print("Testing minimal CPU reset:")
    print(f"Initial: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    
    # Apply reset
    ctx.set(cpu.rst, 1)
    await ctx.tick()
    print(f"After reset tick: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}")
    
    ctx.set(cpu.rst, 0)
    for i in range(5):
        await ctx.tick()
        pc = ctx.get(cpu.pc)
        print(f"After run tick {i}: pc=0x{pc:04X}")

def main():
    sim = Simulator(MinimalCPU())
    sim.add_clock(1e-6)
    sim.add_testbench(test_reset)
    with sim.write_vcd("minimal.vcd"):
        sim.run()

if __name__ == "__main__":
    main()