#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

class SimpleAssign(Elaboratable):
    def __init__(self):
        self.clk = Signal()
        self.rst = Signal()
        self.out = Signal(8)
    
    def elaborate(self, platform):
        m = Module()
        
        # Test direct assignment
        m.d.sync += self.out.eq(0x42)
        
        # Test reset
        with m.If(self.rst):
            m.d.sync += self.out.eq(0xFF)
        
        return m

async def bench(ctx):
    dut = SimpleAssign()
    
    print("Testing basic signal assignment:")
    print(f"Initial: rst={ctx.get(dut.rst)}, out=0x{ctx.get(dut.out):02X}")
    
    # Check initial value
    await ctx.tick()
    print(f"After 1st tick: rst={ctx.get(dut.rst)}, out=0x{ctx.get(dut.out):02X}")
    
    # Apply reset
    ctx.set(dut.rst, 1)
    await ctx.tick()
    print(f"After reset applied: rst={ctx.get(dut.rst)}, out=0x{ctx.get(dut.out):02X}")
    
    # Release reset
    ctx.set(dut.rst, 0)
    await ctx.tick()
    print(f"After reset released: rst={ctx.get(dut.rst)}, out=0x{ctx.get(dut.out):02X}")
    
    # A few more ticks
    for i in range(3):
        await ctx.tick()
        print(f"After {i+1} more tick(s): rst={ctx.get(dut.rst)}, out=0x{ctx.get(dut.out):02X}")

def main():
    sim = Simulator(SimpleAssign())
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    with sim.write_vcd("basic_signal_test.vcd"):
        sim.run()
    print("\nSimulation complete")

if __name__ == "__main__":
    main()