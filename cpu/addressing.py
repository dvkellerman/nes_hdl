from amaranth import *

from cpu.opcodes import AddrMode


def calc_effective_addr(m, cpu):
    """Combinational logic to calculate effective address based on addressing mode."""
    with m.Switch(cpu.addr_mode):

        with m.Case(AddrMode.IMM):
            m.d.comb += cpu.eff_addr.eq(0xFFFF)

        with m.Case(AddrMode.ZP0):
            m.d.comb += [
                cpu.eff_addr.eq(cpu.operand),
                cpu.bus.addr.eq(cpu.operand),
            ]

        with m.Case(AddrMode.ZPX):
            m.d.comb += [
                cpu.eff_addr.eq((cpu.operand + cpu.x)[:8]),
                cpu.bus.addr.eq((cpu.operand + cpu.x)[:8]),
            ]

        with m.Case(AddrMode.ZPY):
            m.d.comb += [
                cpu.eff_addr.eq((cpu.operand + cpu.y)[:8]),
                cpu.bus.addr.eq((cpu.operand + cpu.y)[:8]),
            ]

        with m.Case(AddrMode.ABS):
            m.d.comb += [
                cpu.eff_addr.eq(cpu.addr_temp),
                cpu.bus.addr.eq(cpu.addr_temp),
            ]

        with m.Case(AddrMode.ABX):
            m.d.comb += [
                cpu.eff_addr.eq(cpu.addr_temp + cpu.x),
                cpu.bus.addr.eq(cpu.addr_temp + cpu.x),
            ]

        with m.Case(AddrMode.ABY):
            m.d.comb += [
                cpu.eff_addr.eq(cpu.addr_temp + cpu.y),
                cpu.bus.addr.eq(cpu.addr_temp + cpu.y),
            ]

        with m.Case(AddrMode.IND):
            m.d.comb += [
                cpu.eff_addr.eq(cpu.addr_temp),
                cpu.bus.addr.eq(cpu.addr_temp),
            ]

        with m.Case(AddrMode.IZX):
            ptr = Signal(8, name="izx_ptr")
            m.d.comb += [
                ptr.eq((cpu.operand + cpu.x)[:8]),
                cpu.eff_addr.eq(ptr),
                cpu.bus.addr.eq(ptr),
            ]

        with m.Case(AddrMode.IZY):
            m.d.comb += [
                cpu.eff_addr.eq((cpu.operand + cpu.y)[:8]),
                cpu.bus.addr.eq((cpu.operand + cpu.y)[:8]),
            ]

        with m.Case(AddrMode.REL):
            with m.If(cpu.operand[7]):
                m.d.comb += cpu.eff_addr.eq(cpu.pc - (256 - cpu.operand))
            with m.Else():
                m.d.comb += cpu.eff_addr.eq(cpu.pc + cpu.operand)

        with m.Case(AddrMode.ACC):
            m.d.comb += cpu.eff_addr.eq(0)

        with m.Default():
            m.d.comb += cpu.eff_addr.eq(0)
