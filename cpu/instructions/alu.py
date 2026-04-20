from amaranth import *


def add_alu_ops(m, cpu, opcode, resolved):
    """ADC, SBC, AND, ORA, EOR, CMP, CPX, CPY, BIT instruction group."""
    result9 = Signal(9, name="alu_result9")
    with m.Switch(opcode):

        # AND -- all addressing modes
        with m.Case(0x29, 0x25, 0x35, 0x2D, 0x3D, 0x39, 0x21, 0x31):
            m.d.sync += [
                cpu.a.eq(cpu.a & resolved),
                cpu.flag_z.eq((cpu.a & resolved) == 0),
                cpu.flag_n.eq((cpu.a & resolved)[7]),
            ]

        # ORA -- all addressing modes
        with m.Case(0x09, 0x05, 0x15, 0x0D, 0x1D, 0x19, 0x01, 0x11):
            m.d.sync += [
                cpu.a.eq(cpu.a | resolved),
                cpu.flag_z.eq((cpu.a | resolved) == 0),
                cpu.flag_n.eq((cpu.a | resolved)[7]),
            ]

        # EOR -- all addressing modes
        with m.Case(0x49, 0x45, 0x55, 0x4D, 0x5D, 0x59, 0x41, 0x51):
            m.d.sync += [
                cpu.a.eq(cpu.a ^ resolved),
                cpu.flag_z.eq((cpu.a ^ resolved) == 0),
                cpu.flag_n.eq((cpu.a ^ resolved)[7]),
            ]

        # ADC -- all addressing modes
        with m.Case(0x69, 0x65, 0x75, 0x6D, 0x7D, 0x79, 0x61, 0x71):
            m.d.comb += result9.eq(cpu.a + resolved + cpu.flag_c)
            m.d.sync += [
                cpu.a.eq(result9[:8]),
                cpu.flag_c.eq(result9[8]),
                cpu.flag_z.eq(result9[:8] == 0),
                cpu.flag_n.eq(result9[7]),
                cpu.flag_v.eq(
                    (cpu.a[7] == resolved[7]) & (cpu.a[7] != result9[7])
                ),
            ]

        # SBC -- all addressing modes
        # SBC is ADC with the operand inverted: A - M - (1-C) = A + ~M + C
        with m.Case(0xE9, 0xE5, 0xF5, 0xED, 0xFD, 0xF9, 0xE1, 0xF1):
            inv = Signal(8, name="sbc_inv")
            m.d.comb += [
                inv.eq(~resolved),
                result9.eq(cpu.a + inv + cpu.flag_c),
            ]
            m.d.sync += [
                cpu.a.eq(result9[:8]),
                cpu.flag_c.eq(result9[8]),
                cpu.flag_z.eq(result9[:8] == 0),
                cpu.flag_n.eq(result9[7]),
                cpu.flag_v.eq(
                    (cpu.a[7] != resolved[7]) & (cpu.a[7] != result9[7])
                ),
            ]

        # CMP -- all addressing modes
        with m.Case(0xC9, 0xC5, 0xD5, 0xCD, 0xDD, 0xD9, 0xC1, 0xD1):
            cmp_res = Signal(9, name="cmp_res")
            m.d.comb += cmp_res.eq(cpu.a - resolved)
            m.d.sync += [
                cpu.flag_c.eq(cpu.a >= resolved),
                cpu.flag_z.eq(cmp_res[:8] == 0),
                cpu.flag_n.eq(cmp_res[7]),
            ]

        # CPX -- all addressing modes
        with m.Case(0xE0, 0xE4, 0xEC):
            cpx_res = Signal(9, name="cpx_res")
            m.d.comb += cpx_res.eq(cpu.x - resolved)
            m.d.sync += [
                cpu.flag_c.eq(cpu.x >= resolved),
                cpu.flag_z.eq(cpx_res[:8] == 0),
                cpu.flag_n.eq(cpx_res[7]),
            ]

        # CPY -- all addressing modes
        with m.Case(0xC0, 0xC4, 0xCC):
            cpy_res = Signal(9, name="cpy_res")
            m.d.comb += cpy_res.eq(cpu.y - resolved)
            m.d.sync += [
                cpu.flag_c.eq(cpu.y >= resolved),
                cpu.flag_z.eq(cpy_res[:8] == 0),
                cpu.flag_n.eq(cpy_res[7]),
            ]

        # BIT -- zero page and absolute
        with m.Case(0x24, 0x2C):
            m.d.sync += [
                cpu.flag_z.eq((cpu.a & resolved) == 0),
                cpu.flag_n.eq(resolved[7]),
                cpu.flag_v.eq(resolved[6]),
            ]
