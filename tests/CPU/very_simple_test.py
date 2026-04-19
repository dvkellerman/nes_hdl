#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

class SimpleReg(Elaboratable):
    def __init__(self) -> None:
        self.clk = Signal()
        self.rst = Signal()
        self.data = Signal(8)
    
    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.data.eq(0)  # Default
        
        with m.If(self.rst):
            m.d.sync += self.data.eq(0xFF)
        with m.Else():
            m.d.sync += self.data.eq(self.data + 1)
        
        return m

async def bench(ctx):
    reg = SimpleReg()
    
    print("Testing simple register with reset:")
    print(f"Initial: rst={ctx.get(reg.rst)}, data=0x{ctx.get(reg.data):02X}")
    
    # Apply reset
    ctx.set(reg.rst, 1)
    await ctx.tick()
    print(f"After reset applied: rst={ctx.get(reg.rst)}, data=0x{ctx.get(reg.data):02X}")
    
    # Release reset
    ctx.set(reg.rst, 0)
    await ctx.tick()
    print(f"After reset released: rst={ctx.get(reg.rst)}, data=0x{ctx.get(reg.data):02X}")
    
    # A few more ticks
    for i in range(3):
        await ctx.tick()
        print(f"After {i+1} more tick(s): rst={ctx.get(reg.rst)}, data=0x{ctx.get(reg.data):02X}")

def main():
    sim = Simulator(SimpleReg())
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    with sim.write_vcd("simple_reg_test.vcd"):
        sim.run()
    print("\nSimulation complete")

if __name__ == "__main__":
    main()