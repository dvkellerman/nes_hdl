#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

class TestCPU(Elaboratable):
    def __init__(self):
        self.rst = Signal()
        self.pc = Signal(16)
        
    def elaborate(self, platform):
        m = Module()
        
        # Just increment - no reset logic for now
        m.d.sync += self.pc.eq(self.pc + 1)
        
        return m

async def test(ctx):
    cpu = TestCPU()
    
    for i in range(5):
        await ctx.tick()
        pc = ctx.get(cpu.pc)
        print(f"Tick {i}: pc={pc}")

def main():
    sim = Simulator(TestCPU())
    sim.add_clock(1e-6)
    sim.add_testbench(test)
    with sim.write_vcd("simple.vcd"):
        sim.run()

if __name__ == "__main__":
    main()