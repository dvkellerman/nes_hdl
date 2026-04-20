from amaranth import *


def add_control(m, cpu, opcode):
    """Branch, JMP, JSR, RTS, BRK, RTI, NOP instruction group."""
    with m.Switch(opcode):

        # NOP
        with m.Case(0xEA):
            pass

        # BPL -- branch if positive (N == 0)
        with m.Case(0x10):
            with m.If(cpu.flag_n == 0):
                m.d.sync += cpu.pc.eq(cpu.eff_addr)

        # BMI -- branch if negative (N == 1)
        with m.Case(0x30):
            with m.If(cpu.flag_n == 1):
                m.d.sync += cpu.pc.eq(cpu.eff_addr)

        # BVC -- branch if overflow clear (V == 0)
        with m.Case(0x50):
            with m.If(cpu.flag_v == 0):
                m.d.sync += cpu.pc.eq(cpu.eff_addr)

        # BVS -- branch if overflow set (V == 1)
        with m.Case(0x70):
            with m.If(cpu.flag_v == 1):
                m.d.sync += cpu.pc.eq(cpu.eff_addr)

        # BCC -- branch if carry clear (C == 0)
        with m.Case(0x90):
            with m.If(cpu.flag_c == 0):
                m.d.sync += cpu.pc.eq(cpu.eff_addr)

        # BCS -- branch if carry set (C == 1)
        with m.Case(0xB0):
            with m.If(cpu.flag_c == 1):
                m.d.sync += cpu.pc.eq(cpu.eff_addr)

        # BNE -- branch if not equal (Z == 0)
        with m.Case(0xD0):
            with m.If(cpu.flag_z == 0):
                m.d.sync += cpu.pc.eq(cpu.eff_addr)

        # BEQ -- branch if equal (Z == 1)
        with m.Case(0xF0):
            with m.If(cpu.flag_z == 1):
                m.d.sync += cpu.pc.eq(cpu.eff_addr)

        # JMP Absolute
        with m.Case(0x4C):
            m.d.sync += cpu.pc.eq(cpu.addr_temp)

        # JMP Indirect (simplified -- does not emulate page-boundary bug)
        with m.Case(0x6C):
            m.d.sync += cpu.pc.eq(cpu.addr_temp)

        # JSR Absolute (simplified -- pushes high byte, decrements SP)
        with m.Case(0x20):
            m.d.sync += [
                cpu.data_out.eq(((cpu.pc - 1) >> 8) & 0xFF),
                cpu.we.eq(1),
                cpu.sp.eq(cpu.sp - 1),
            ]

        # RTS (simplified -- increments SP)
        with m.Case(0x60):
            m.d.sync += cpu.sp.eq(cpu.sp + 1)

        # BRK (simplified -- sets B flag and pushes status)
        with m.Case(0x00):
            m.d.sync += [
                cpu.flag_b.eq(1),
                cpu.flag_i.eq(1),
            ]

        # RTI (simplified -- pulls status, increments SP)
        with m.Case(0x40):
            m.d.sync += [
                cpu.sp.eq(cpu.sp + 1),
                cpu.flag_c.eq(cpu.data_in[0]),
                cpu.flag_z.eq(cpu.data_in[1]),
                cpu.flag_i.eq(cpu.data_in[2]),
                cpu.flag_d.eq(cpu.data_in[3]),
                cpu.flag_v.eq(cpu.data_in[5]),
                cpu.flag_n.eq(cpu.data_in[7]),
            ]
