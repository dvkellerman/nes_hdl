from amaranth import *


def add_stack_transfers_flags(m, cpu, opcode):
    """Stack ops, register transfers, and flag instructions."""
    with m.Switch(opcode):

        # PHA -- push accumulator
        with m.Case(0x48):
            m.d.sync += [
                cpu.data_out.eq(cpu.a),
                cpu.we.eq(1),
                cpu.sp.eq(cpu.sp - 1),
            ]

        # PLA -- pull accumulator
        with m.Case(0x68):
            m.d.sync += [
                cpu.sp.eq(cpu.sp + 1),
                cpu.a.eq(cpu.data_in),
                cpu.flag_z.eq(cpu.data_in == 0),
                cpu.flag_n.eq(cpu.data_in[7]),
            ]

        # PHP -- push processor status
        with m.Case(0x08):
            m.d.sync += [
                cpu.data_out.eq(cpu.p),
                cpu.we.eq(1),
                cpu.sp.eq(cpu.sp - 1),
            ]

        # PLP -- pull processor status
        with m.Case(0x28):
            m.d.sync += [
                cpu.sp.eq(cpu.sp + 1),
                cpu.flag_c.eq(cpu.data_in[0]),
                cpu.flag_z.eq(cpu.data_in[1]),
                cpu.flag_i.eq(cpu.data_in[2]),
                cpu.flag_d.eq(cpu.data_in[3]),
                cpu.flag_b.eq(cpu.data_in[4]),
                cpu.flag_v.eq(cpu.data_in[5]),
                cpu.flag_n.eq(cpu.data_in[7]),
            ]

        # TAX -- transfer A to X
        with m.Case(0xAA):
            m.d.sync += [
                cpu.x.eq(cpu.a),
                cpu.flag_z.eq(cpu.a == 0),
                cpu.flag_n.eq(cpu.a[7]),
            ]

        # TXA -- transfer X to A
        with m.Case(0x8A):
            m.d.sync += [
                cpu.a.eq(cpu.x),
                cpu.flag_z.eq(cpu.x == 0),
                cpu.flag_n.eq(cpu.x[7]),
            ]

        # TAY -- transfer A to Y
        with m.Case(0xA8):
            m.d.sync += [
                cpu.y.eq(cpu.a),
                cpu.flag_z.eq(cpu.a == 0),
                cpu.flag_n.eq(cpu.a[7]),
            ]

        # TYA -- transfer Y to A
        with m.Case(0x98):
            m.d.sync += [
                cpu.a.eq(cpu.y),
                cpu.flag_z.eq(cpu.y == 0),
                cpu.flag_n.eq(cpu.y[7]),
            ]

        # TSX -- transfer SP to X
        with m.Case(0xBA):
            m.d.sync += [
                cpu.x.eq(cpu.sp),
                cpu.flag_z.eq(cpu.sp == 0),
                cpu.flag_n.eq(cpu.sp[7]),
            ]

        # TXS -- transfer X to SP (no flag updates)
        with m.Case(0x9A):
            m.d.sync += cpu.sp.eq(cpu.x)

        # CLC -- clear carry
        with m.Case(0x18):
            m.d.sync += cpu.flag_c.eq(0)

        # SEC -- set carry
        with m.Case(0x38):
            m.d.sync += cpu.flag_c.eq(1)

        # CLI -- clear interrupt disable
        with m.Case(0x58):
            m.d.sync += cpu.flag_i.eq(0)

        # SEI -- set interrupt disable
        with m.Case(0x78):
            m.d.sync += cpu.flag_i.eq(1)

        # CLD -- clear decimal mode
        with m.Case(0xD8):
            m.d.sync += cpu.flag_d.eq(0)

        # SED -- set decimal mode
        with m.Case(0xF8):
            m.d.sync += cpu.flag_d.eq(1)

        # CLV -- clear overflow
        with m.Case(0xB8):
            m.d.sync += cpu.flag_v.eq(0)
