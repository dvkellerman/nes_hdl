from amaranth import *


def add_shifts(m, cpu, opcode):
    """ASL, LSR, ROL, ROR instruction group.

    Accumulator variants operate on A directly.
    Memory variants read from data_in and write back via data_out.
    """
    with m.Switch(opcode):

        # ASL Accumulator
        with m.Case(0x0A):
            m.d.sync += [
                cpu.flag_c.eq(cpu.a[7]),
                cpu.a.eq(cpu.a << 1),
                cpu.flag_z.eq((cpu.a << 1)[:8] == 0),
                cpu.flag_n.eq((cpu.a << 1)[7]),
            ]

        # ASL Memory
        with m.Case(0x06, 0x16, 0x0E, 0x1E):
            m.d.sync += [
                cpu.flag_c.eq(cpu.data_in[7]),
                cpu.data_out.eq(cpu.data_in << 1),
                cpu.we.eq(1),
                cpu.flag_z.eq((cpu.data_in << 1)[:8] == 0),
                cpu.flag_n.eq((cpu.data_in << 1)[7]),
            ]

        # LSR Accumulator
        with m.Case(0x4A):
            m.d.sync += [
                cpu.flag_c.eq(cpu.a[0]),
                cpu.a.eq(cpu.a >> 1),
                cpu.flag_z.eq((cpu.a >> 1) == 0),
                cpu.flag_n.eq(0),
            ]

        # LSR Memory
        with m.Case(0x46, 0x56, 0x4E, 0x5E):
            m.d.sync += [
                cpu.flag_c.eq(cpu.data_in[0]),
                cpu.data_out.eq(cpu.data_in >> 1),
                cpu.we.eq(1),
                cpu.flag_z.eq((cpu.data_in >> 1) == 0),
                cpu.flag_n.eq(0),
            ]

        # ROL Accumulator
        with m.Case(0x2A):
            rol_a = Signal(8, name="rol_a")
            m.d.comb += rol_a.eq(Cat(cpu.flag_c, cpu.a[:7]))
            m.d.sync += [
                cpu.flag_c.eq(cpu.a[7]),
                cpu.a.eq(rol_a),
                cpu.flag_z.eq(rol_a == 0),
                cpu.flag_n.eq(rol_a[7]),
            ]

        # ROL Memory
        with m.Case(0x26, 0x36, 0x2E, 0x3E):
            rol_m = Signal(8, name="rol_m")
            m.d.comb += rol_m.eq(Cat(cpu.flag_c, cpu.data_in[:7]))
            m.d.sync += [
                cpu.flag_c.eq(cpu.data_in[7]),
                cpu.data_out.eq(rol_m),
                cpu.we.eq(1),
                cpu.flag_z.eq(rol_m == 0),
                cpu.flag_n.eq(rol_m[7]),
            ]

        # ROR Accumulator
        with m.Case(0x6A):
            ror_a = Signal(8, name="ror_a")
            m.d.comb += ror_a.eq(Cat(cpu.a[1:8], cpu.flag_c))
            m.d.sync += [
                cpu.flag_c.eq(cpu.a[0]),
                cpu.a.eq(ror_a),
                cpu.flag_z.eq(ror_a == 0),
                cpu.flag_n.eq(ror_a[7]),
            ]

        # ROR Memory
        with m.Case(0x66, 0x76, 0x6E, 0x7E):
            ror_m = Signal(8, name="ror_m")
            m.d.comb += ror_m.eq(Cat(cpu.data_in[1:8], cpu.flag_c))
            m.d.sync += [
                cpu.flag_c.eq(cpu.data_in[0]),
                cpu.data_out.eq(ror_m),
                cpu.we.eq(1),
                cpu.flag_z.eq(ror_m == 0),
                cpu.flag_n.eq(ror_m[7]),
            ]
