#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

class Blinker(Elaboratable):
    def __init__(self):
        self.led = Signal()
        self.count = Signal(8)
    
    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.count.eq(self.count + 1)
        m.d.sync += self.led.eq(self.count[0])
        return m

async def bench(ctx):
    # Just toggle something to make sure clock is working
    for i in range(10):
        await ctx.tick()
        led = ctx.get(dut.led)
        count = ctx.get(dut.count)
        print(f"Cycle {i}: led={led}, count={count}")

def main():
    global dut
    dut = Blinker()
    sim = Simulator(dut)
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    with sim.write_vcd("basic_test.vcd"):
        sim.run()

if __name__ == "__main__":
    main()