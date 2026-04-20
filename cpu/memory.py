from amaranth import *
from amaranth.lib.wiring import Component, In, Out
from amaranth.lib.memory import Memory


class SyncRAM(Component):
    """Simple synchronous RAM for CPU testing."""

    addr: In(16)
    data_in: In(8)
    data_out: Out(8)
    we: In(1)

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
            rd.addr.eq(self.addr),
            self.data_out.eq(rd.data),
            wr.addr.eq(self.addr),
            wr.data.eq(self.data_in),
            wr.en.eq(self.we),
        ]

        return m
