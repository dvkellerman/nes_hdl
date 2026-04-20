from amaranth import *


def add_loads_stores(m, cpu, opcode, resolved):
    """LDA, LDX, LDY, STA, STX, STY instruction group."""
    with m.Switch(opcode):

        # LDA -- all addressing modes
        with m.Case(0xA9, 0xA5, 0xB5, 0xAD, 0xBD, 0xB9, 0xA1, 0xB1):
            m.d.sync += [
                cpu.a.eq(resolved),
                cpu.flag_z.eq(resolved == 0),
                cpu.flag_n.eq(resolved[7]),
            ]

        # LDX -- all addressing modes
        with m.Case(0xA2, 0xA6, 0xB6, 0xAE, 0xBE):
            m.d.sync += [
                cpu.x.eq(resolved),
                cpu.flag_z.eq(resolved == 0),
                cpu.flag_n.eq(resolved[7]),
            ]

        # LDY -- all addressing modes
        with m.Case(0xA0, 0xA4, 0xB4, 0xAC, 0xBC):
            m.d.sync += [
                cpu.y.eq(resolved),
                cpu.flag_z.eq(resolved == 0),
                cpu.flag_n.eq(resolved[7]),
            ]

        # STA -- all addressing modes
        with m.Case(0x85, 0x95, 0x8D, 0x9D, 0x99, 0x81, 0x91):
            m.d.sync += [
                cpu.bus.data_wr.eq(cpu.a),
                cpu.bus.we.eq(1),
            ]

        # STX -- all addressing modes
        with m.Case(0x86, 0x96, 0x8E):
            m.d.sync += [
                cpu.bus.data_wr.eq(cpu.x),
                cpu.bus.we.eq(1),
            ]

        # STY -- all addressing modes
        with m.Case(0x84, 0x94, 0x8C):
            m.d.sync += [
                cpu.bus.data_wr.eq(cpu.y),
                cpu.bus.we.eq(1),
            ]
