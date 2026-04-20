from amaranth import *
from amaranth.lib.wiring import Component, In, Out

from cpu.bus_sig import CpuBus
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

    bus: Out(CpuBus)

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
                m.d.comb += self.bus.addr.eq(0xFFFC)
                m.d.sync += self.in_reset.eq(0)
                m.next = "FETCH_OPCODE"

            with m.State("FETCH_OPCODE"):
                m.d.comb += self.bus.addr.eq(self.pc)
                m.d.sync += [
                    self.ir.eq(self.bus.data_rd),
                    self.opcode.eq(self.bus.data_rd),
                    self.pc.eq(self.pc + 1),
                ]
                m.next = "FETCH_OPERAND_1"

            with m.State("FETCH_OPERAND_1"):
                m.d.comb += self.bus.addr.eq(self.pc)
                m.d.sync += [
                    self.operand.eq(self.bus.data_rd),
                    self.pc.eq(self.pc + 1),
                ]
                m.next = "FETCH_OPERAND_2"

            with m.State("FETCH_OPERAND_2"):
                m.d.comb += self.bus.addr.eq(self.pc)
                m.d.sync += [
                    self.addr_temp.eq(Cat(self.bus.data_rd, self.operand)),
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
        """Determine addressing mode from opcode (auto-generated from OPCODES table)."""
        from cpu.opcodes import opcodes_by_addr_mode
        groups = opcodes_by_addr_mode()
        with m.Switch(self.opcode):
            for mode, ops in groups.items():
                if mode == AddrMode.IMP:
                    continue
                with m.Case(*ops):
                    m.d.comb += self.addr_mode.eq(mode)
            with m.Default():
                m.d.comb += self.addr_mode.eq(AddrMode.IMP)
