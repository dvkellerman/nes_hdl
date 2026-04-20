from amaranth import *


def add_inc_dec(m, cpu, opcode, resolved):
    """INC, DEC, INX, DEX, INY, DEY instruction group."""
    inc_result = Signal(8, name="inc_result")
    dec_result = Signal(8, name="dec_result")

    with m.Switch(opcode):

        # INC -- all addressing modes (memory)
        with m.Case(0xE6, 0xF6, 0xEE, 0xFE):
            m.d.comb += inc_result.eq(cpu.data_in + 1)
            m.d.sync += [
                cpu.data_out.eq(inc_result),
                cpu.we.eq(1),
                cpu.flag_z.eq(inc_result == 0),
                cpu.flag_n.eq(inc_result[7]),
            ]

        # DEC -- all addressing modes (memory)
        with m.Case(0xC6, 0xD6, 0xCE, 0xDE):
            m.d.comb += dec_result.eq(cpu.data_in - 1)
            m.d.sync += [
                cpu.data_out.eq(dec_result),
                cpu.we.eq(1),
                cpu.flag_z.eq(dec_result == 0),
                cpu.flag_n.eq(dec_result[7]),
            ]

        # INX
        with m.Case(0xE8):
            inx = Signal(8, name="inx")
            m.d.comb += inx.eq(cpu.x + 1)
            m.d.sync += [
                cpu.x.eq(inx),
                cpu.flag_z.eq(inx == 0),
                cpu.flag_n.eq(inx[7]),
            ]

        # DEX
        with m.Case(0xCA):
            dex = Signal(8, name="dex")
            m.d.comb += dex.eq(cpu.x - 1)
            m.d.sync += [
                cpu.x.eq(dex),
                cpu.flag_z.eq(dex == 0),
                cpu.flag_n.eq(dex[7]),
            ]

        # INY
        with m.Case(0xC8):
            iny = Signal(8, name="iny")
            m.d.comb += iny.eq(cpu.y + 1)
            m.d.sync += [
                cpu.y.eq(iny),
                cpu.flag_z.eq(iny == 0),
                cpu.flag_n.eq(iny[7]),
            ]

        # DEY
        with m.Case(0x88):
            dey = Signal(8, name="dey")
            m.d.comb += dey.eq(cpu.y - 1)
            m.d.sync += [
                cpu.y.eq(dey),
                cpu.flag_z.eq(dey == 0),
                cpu.flag_n.eq(dey[7]),
            ]
