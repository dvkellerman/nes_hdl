#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

# Test just the reset logic in isolation
class ResetLogicTest(Elaboratable):
    def __init__(self):
        self.clk = Signal()
        self.rst = Signal()
        self.pc = Signal(16)
    
    def elaborate(self, platform):
        m = Module()
        
        # Simple reset logic - PC should go to 0xFFFC when reset is high
        with m.If(self.rst):
            m.d.sync += self.pc.eq(0xFFFC)
        with m.Else():
            m.d.sync += self.pc.eq(self.pc)  # Hold value
        
        return m

async def bench(ctx):
    dut = ResetLogicTest()
    
    print("Testing isolated reset logic:")
    print(f"Initial: rst={ctx.get(dut.rst)}, pc=0x{ctx.get(dut.pc):04X}")
    
    # Apply reset
    print("\nApplying reset...")
    ctx.set(dut.rst, 1)
    await ctx.tick()
    print(f"After reset applied: rst={ctx.get(dut.rst)}, pc=0x{ctx.get(dut.pc):04X}")
    
    # Hold reset for a few more cycles
    for i in range(3):
        await ctx.tick()
        print(f"After reset hold {i+1}: rst={ctx.get(dut.rst)}, pc=0x{ctx.get(dut.pc):04X}")
    
    # Release reset
    print("\nReleasing reset...")
    ctx.set(dut.rst, 0)
    await ctx.tick()
    print(f"After reset released: rst={ctx.get(dut.rst)}, pc=0x{ctx.get(dut.pc):04X}")
    
    # Let it run
    for i in range(5):
        await ctx.tick()
        print(f"After free run {i+1}: rst={ctx.get(dut.rst)}, pc=0x{ctx.get(dut.pc):04X}")

def main():
    sim = Simulator(ResetLogicTest())
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    with sim.write_vcd("isolated_reset_test.vcd"):
        sim.run()
    print("\nSimulation complete")

if __name__ == "__main__":
    main()