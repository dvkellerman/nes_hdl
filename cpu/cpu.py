from amaranth import *
from amaranth.lib.wiring import Component, In, Out

from cpu.opcodes import AddrMode
from cpu.addressing import calc_effective_addr
from cpu.instructions import execute_instruction


class CPUState:
    FETCH_OPCODE = 0
    FETCH_OPERAND_1 = 1
    FETCH_OPERAND_2 = 2
    EXECUTE = 3
    WRITE_BACK = 4


class CPU(Component):
    """MOS 6502 CPU implementation in Amaranth HDL."""

    addr: Out(16)
    data_in: In(8)
    data_out: Out(8)
    we: Out(1)

    irq: In(1)
    nmi: In(1)
    rdy: In(1)

    def __init__(self):
        self.a = Signal(8)
        self.x = Signal(8)
        self.y = Signal(8)
        self.sp = Signal(8)
        self.pc = Signal(16)

        self.p = Signal(8)
        self.flag_n = Signal()
        self.flag_v = Signal()
        self.flag_b = Signal()
        self.flag_d = Signal()
        self.flag_i = Signal()
        self.flag_z = Signal()
        self.flag_c = Signal()

        self.state = Signal(3, init=CPUState.FETCH_OPCODE)
        self.ir = Signal(8)
        self.opcode = Signal(8)
        self.operand = Signal(8)
        self.addr_temp = Signal(16)
        self.eff_addr = Signal(16)
        self.addr_mode = Signal(4)
        self.in_reset = Signal(init=1)

        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.p.eq(Cat(
            self.flag_c,
            self.flag_z,
            self.flag_i,
            self.flag_d,
            self.flag_b,
            self.flag_v,
            C(1),
            self.flag_n,
        ))

        with m.FSM(init="RESET"):
            with m.State("RESET"):
                m.d.sync += [
                    self.pc.eq(0xFFFC),
                    self.sp.eq(0xFD),
                    self.flag_i.eq(1),
                    self.in_reset.eq(1),
                ]
                m.next = "RESET_VECTOR"

            with m.State("RESET_VECTOR"):
                m.d.comb += self.addr.eq(0xFFFC)
                m.d.sync += self.in_reset.eq(0)
                m.next = "FETCH_OPCODE"

            with m.State("FETCH_OPCODE"):
                m.d.comb += self.addr.eq(self.pc)
                m.d.sync += [
                    self.ir.eq(self.data_in),
                    self.opcode.eq(self.data_in),
                    self.pc.eq(self.pc + 1),
                ]
                m.next = "FETCH_OPERAND_1"

            with m.State("FETCH_OPERAND_1"):
                m.d.comb += self.addr.eq(self.pc)
                m.d.sync += [
                    self.operand.eq(self.data_in),
                    self.pc.eq(self.pc + 1),
                ]
                m.next = "FETCH_OPERAND_2"

            with m.State("FETCH_OPERAND_2"):
                m.d.comb += self.addr.eq(self.pc)
                m.d.sync += [
                    self.addr_temp.eq(Cat(self.data_in, self.operand)),
                    self.pc.eq(self.pc + 1),
                ]
                m.next = "EXECUTE"

            with m.State("EXECUTE"):
                self._decode_addr_mode(m)
                calc_effective_addr(m, self)
                m.next = "WRITE_BACK"

            with m.State("WRITE_BACK"):
                execute_instruction(m, self, self.opcode)
                m.next = "FETCH_OPCODE"

        return m

    def _decode_addr_mode(self, m):
        """Determine addressing mode from opcode."""
        with m.Switch(self.opcode):
            with m.Case(0xA9, 0xA2, 0xA0, 0x09, 0x29, 0x49, 0x69, 0xE9,
                         0xC9, 0xC0, 0xE0):
                m.d.comb += self.addr_mode.eq(AddrMode.IMM)
            with m.Case(0xA5, 0xA4, 0xC5, 0xC4, 0xA6, 0x24, 0x25,
                         0x45, 0x65, 0xE4, 0xE5, 0x85, 0x84, 0x86,
                         0xC6, 0xE6, 0x06, 0x46, 0x26, 0x66):
                m.d.comb += self.addr_mode.eq(AddrMode.ZP0)
            with m.Case(0xB5, 0xB4, 0xD6, 0xD5, 0xF6, 0xF5, 0x94,
                         0x95, 0x75, 0x35, 0x55, 0x15, 0x16, 0x56,
                         0x36, 0x76):
                m.d.comb += self.addr_mode.eq(AddrMode.ZPX)
            with m.Case(0xB6, 0x96):
                m.d.comb += self.addr_mode.eq(AddrMode.ZPY)
            with m.Case(0xAD, 0xAC, 0xCD, 0xCC, 0xED, 0xEC, 0x8D,
                         0x8C, 0xAE, 0xCE, 0xEE, 0x8E, 0x0D, 0x2D,
                         0x4D, 0x6D, 0x2C, 0x0E, 0x4E, 0x2E, 0x6E):
                m.d.comb += self.addr_mode.eq(AddrMode.ABS)
            with m.Case(0xBD, 0xBC, 0xDD, 0xDE, 0xFD, 0xFE, 0x9D,
                         0x1D, 0x3D, 0x5D, 0x7D, 0x1E, 0x5E, 0x3E,
                         0x7E):
                m.d.comb += self.addr_mode.eq(AddrMode.ABX)
            with m.Case(0xB9, 0xBE, 0xD9, 0xF9, 0x99, 0x19, 0x39,
                         0x59, 0x79):
                m.d.comb += self.addr_mode.eq(AddrMode.ABY)
            with m.Case(0xA1, 0x81, 0xC1, 0xE1, 0x01, 0x21, 0x41,
                         0x61):
                m.d.comb += self.addr_mode.eq(AddrMode.IZX)
            with m.Case(0xB1, 0x91, 0xD1, 0xF1, 0x11, 0x31, 0x51,
                         0x71):
                m.d.comb += self.addr_mode.eq(AddrMode.IZY)
            with m.Case(0x10, 0x30, 0x50, 0x70, 0x90, 0xB0, 0xD0,
                         0xF0):
                m.d.comb += self.addr_mode.eq(AddrMode.REL)
            with m.Case(0x6C):
                m.d.comb += self.addr_mode.eq(AddrMode.IND)
            with m.Case(0x0A, 0x4A, 0x2A, 0x6A):
                m.d.comb += self.addr_mode.eq(AddrMode.ACC)
            with m.Default():
                m.d.comb += self.addr_mode.eq(AddrMode.IMP)
