#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

class ExplicitResetCPU(Elaboratable):
    def __init__(self):
        self.clk = Signal()
        self.rst = Signal()
        self.pc = Signal(16)
        self.internal_state = Signal(4)
    
    def elaborate(self, platform):
        m = Module()
        
        # Explicit synchronous reset
        m.d.sync += self.pc.eq(0)  # Default value
        
        with m.If(self.rst):
            m.d.sync += [
                self.pc.eq(0xFFFC),
                self.internal_state.eq(0),
            ]
        with m.Else():
            # Simple state machine to show it's working
            with m.Switch(self.internal_state):
                with m.Case(0):
                    m.d.sync += self.internal_state.eq(1)
                with m.Case(1):
                    m.d.sync += self.internal_state.eq(2)
                with m.Case(2):
                    m.d.sync += self.internal_state.eq(3)
                with m.Case(3):
                    m.d.sync += self.internal_state.eq(0)
                    
                # Also increment PC when not in reset
                m.d.sync += self.pc.eq(self.pc + 1)
        
        return m

async def bench(ctx):
    cpu = ExplicitResetCPU()
    
    print("Testing explicit reset logic:")
    print(f"Initial: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}, state={ctx.get(cpu.internal_state)}")
    
    # Apply reset for a few cycles
    print("\n--- Applying reset (rst=1) ---")
    ctx.set(cpu.rst, 1)
    for i in range(5):
        await ctx.tick()
        print(f"  After tick {i+1}: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}, state={ctx.get(cpu.internal_state)}")
    
    # Release reset
    print("\n--- Releasing reset (rst=0) ---")
    ctx.set(cpu.rst, 0)
    for i in range(8):
        await ctx.tick()
        print(f"  After tick {i+1}: rst={ctx.get(cpu.rst)}, pc=0x{ctx.get(cpu.pc):04X}, state={ctx.get(cpu.internal_state)}")

def main():
    sim = Simulator(ExplicitResetCPU())
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    with sim.write_vcd("explicit_reset_test.vcd"):
        sim.run()
    print("\nSimulation complete")

if __name__ == "__main__":
    main()