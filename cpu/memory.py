from amaranth import *
from amaranth.lib.wiring import Component, In, Out
from amaranth.lib.memory import Memory

from cpu.bus_sig import CpuBus


class SyncRAM(Component):
    """Simple synchronous RAM for CPU testing."""

    bus: In(CpuBus)

    def __init__(self, size=0x10000, init_data=None):
        self.size = size
        self.init_data = init_data or bytearray(size)
        super().__init__()

    def elaborate(self, platform):
        m = Module()

        mem = Memory(shape=8, depth=self.size, init=self.init_data)
        m.submodules.mem = mem

        rd = mem.read_port()
        wr = mem.write_port()
        m.submodules.rd = rd
        m.submodules.wr = wr

        m.d.comb += [
            rd.addr.eq(self.bus.addr),
            self.bus.data_rd.eq(rd.data),
            wr.addr.eq(self.bus.addr),
            wr.data.eq(self.bus.data_wr),
            wr.en.eq(self.bus.we),
        ]

        return m
