#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

class Blinker(Elaboratable):
    def __init__(self):
        self.led = Signal()
        self.timer = Signal(range(0, 100000))
    
    def elaborate(self, platform):
        m = Module()
        
        m.d.sync += self.timer.eq(self.timer + 1)
        m.d.sync += self.led.eq(self.timer[15])  # Blink at bit 15
        
        return m

def bench():
    dut = Blinker()
    
    yield
    for i in range(10):
        yield
        led = yield dut.led
        timer = yield dut.timer
        print(f"Cycle {i:2d}: led={led}, timer={timer}")

def main():
    dut = Blinker()
    sim = Simulator(dut)
    sim.add_clock(1e-6)  # 1 MHz
    sim.add_sync_process(bench)
    with sim.write_vcd("blinker.vcd"):
        sim.run()

if __name__ == "__main__":
    main()