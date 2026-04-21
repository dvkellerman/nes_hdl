#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from amaranth import *
from amaranth.sim import Simulator

from cpu.cpu import CPU


def main():
    cpu = CPU()

    mem = bytearray(0x10000)
    mem[0xFFFC] = 0xA9  # LDA Immediate
    mem[0xFFFD] = 0x05  # Operand: 5
    mem[0xFFFE] = 0x00  # BRK

    async def bench(ctx):
        print("=== CPU Test: LDA #$05 ===")

        for i in range(25):
            await ctx.tick()

            addr = ctx.get(cpu.bus.addr)
            ctx.set(cpu.bus.data_rd, mem[addr])

            if i < 15 or i % 5 == 0:
                pc = ctx.get(cpu.pc)
                a = ctx.get(cpu.a)
                opcode = ctx.get(cpu.opcode)
                operand = ctx.get(cpu.operand)
                eff_addr = ctx.get(cpu.eff_addr)
                data_rd = ctx.get(cpu.bus.data_rd)

                print(
                    f"Cycle {i:2d}: PC=0x{pc:04X}, OPCODE=0x{opcode:02X}, "
                    f"OPND=0x{operand:02X}, EA=0x{eff_addr:04X}, "
                    f"ADDR=0x{addr:04X}, DATA_RD=0x{data_rd:02X}, A=0x{a:02X}"
                )

        final_a = ctx.get(cpu.a)
        print(f"\nFinal: A=0x{final_a:02X}, PC=0x{ctx.get(cpu.pc):04X}")
        if final_a == 0x05:
            print("SUCCESS!")
        else:
            print("FAILED!")

    sim = Simulator(cpu)
    sim.add_clock(100_000)
    sim.add_testbench(bench)
    with sim.write_vcd("test_cpu.vcd"):
        sim.run()


if __name__ == "__main__":
    main()
