from amaranth import *
from typing import Optional

class Memory(Elaboratable):
    """Simple synchronous RAM for CPU testing."""
    
    def __init__(self, size: int = 0x10000, init_data: Optional[bytearray] = None) -> None:
        self.size = size
        self.init_data = init_data or bytearray(size)
        
        # CPU-like interface
        self.addr = Signal(16)
        self.data_in = Signal(8)
        self.data_out = Signal(8)
        self.we = Signal()
        
    def elaborate(self, platform: Optional[object]) -> Module:
        m = Module()
        
        # Create memory array
        mem = Memory(width=8, depth=self.size, init=self.init_data)
        
        # Synchronous read port
        m.submodules.rdport = rdport = mem.read_port(domain="sync")
        m.d.sync += rdport.addr.eq(self.addr)
        m.d.comb += self.data_out.eq(rdport.data)
        
        # Synchronous write port
        m.submodules.wrport = wrport = mem.write_port(domain="sync")
        m.d.sync += [
            wrport.addr.eq(self.addr),
            wrport.data.eq(self.data_in),
            wrport.en.eq(self.we),
        ]
        
        return m