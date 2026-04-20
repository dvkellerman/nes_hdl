from amaranth.lib.wiring import Signature, In, Out


class CpuBus(Signature):
    """Shared bus signature for CPU memory interface.

    From the initiator's (CPU's) perspective:
      addr    -- Out: address to read/write
      data_rd -- In:  data read from memory
      data_wr -- Out: data to write to memory
      we      -- Out: write enable
    """

    def __init__(self):
        super().__init__({
            "addr": Out(16),
            "data_rd": In(8),
            "data_wr": Out(8),
            "we": Out(1),
        })
