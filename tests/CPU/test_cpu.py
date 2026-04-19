#!/usr/bin/env python3
import sys
sys.path.insert(0, "/var/home/dkeller/Desktop/hdl")

from amaranth import *
from amaranth.sim import Simulator

from cpu.cpu import CPU

def main():
    cpu = CPU(read_only=False)
    
    mem = bytearray(0x10000)
    mem[0xFFFC] = 0xA9  # LDA Immediate
    mem[0xFFFD] = 0x05  # Operand: 5
    mem[0xFFFE] = 0x00  # BRK

    async def bench(ctx):
        print("=== CPU Test with Detailed State Tracking ===")
        
        # Apply reset - hold for 2 cycles
        ctx.set(cpu.rst, 1)
        await ctx.tick()
        await ctx.tick()
        
        # Release reset and let it run
        ctx.set(cpu.rst, 0)
        
        for i in range(25):
            await ctx.tick()
            
            # Feed memory
            addr = ctx.get(cpu.addr)
            ctx.set(cpu.data_in, mem[addr])
            
            # Detailed debug output
            if i < 15 or i % 5 == 0:
                state = ctx.get(cpu.state)
                pc = ctx.get(cpu.pc)
                a = ctx.get(cpu.a)
                ir = ctx.get(cpu.ir)
                opcode = ctx.get(cpu.opcode)
                operand = ctx.get(cpu.operand)
                eff_addr = ctx.get(cpu.eff_addr)
                addr_val = ctx.get(cpu.addr)
                data_in = ctx.get(cpu.data_in)
                
                print(f"Cycle {i:2d}: State={state}, PC=0x{pc:04X}, OPCODE=0x{opcode:02X}, "
                      f"OPND=0x{operand:02X}, EA=0x{eff_addr:04X}, ADDR=0x{addr_val:04X}, "
                      f"DATA_IN=0x{data_in:02X}, A=0x{a:02X}")
        
        print(f"\nFinal: A=0x{ctx.get(cpu.a):02X}, PC=0x{ctx.get(cpu.pc):04X}, State={ctx.get(cpu.state)}")
        if ctx.get(cpu.a) == 0x05:
            print("SUCCESS!")
        else:
            print("FAILED!")

    sim = Simulator(cpu)
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    with sim.write_vcd("test_cpu.vcd"):
        sim.run()

if __name__ == "__main__":
    main()