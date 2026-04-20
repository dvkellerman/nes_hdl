from amaranth import *
from amaranth.lib.coding import *
from typing import Optional

from cpu.opcodes import AddrMode, get_opcode_info
from cpu.addressing import AddressingMode
from cpu.instructions import Instructions
    
# CPU State Machine States
class CPUState:
    FETCH_OPCODE = 0
    FETCH_OPERAND_1 = 1
    FETCH_OPERAND_2 = 2
    EXECUTE = 3
    WRITE_BACK = 4

class CPU(Elaboratable):
    """MOS 6502 CPU implementation in Amaranth HDL."""
    
    def __init__(self, read_only: bool = False) -> None:
        self.read_only = read_only
            
        # Clock and control signals
        self.clk = Signal()
        self.rst = Signal()
        
        # Memory interface
        self.addr = Signal(16)
        self.data_in = Signal(8)
        self.data_out = Signal(8)
        self.we = Signal()
        
        # Interrupt signals
        self.irq = Signal()
        self.nmi = Signal()
        self.rdy = Signal(init=1)
        
        # CPU Registers
        self.a = Signal(8, name="a")      # Accumulator
        self.x = Signal(8, name="x")      # X register
        self.y = Signal(8, name="y")      # Y register
        self.sp = Signal(8, name="sp")    # Stack pointer
        self.pc = Signal(16, name="pc")   # Program counter
        
        # Processor status flags
        self.p = Signal(8, name="p")
        self.flag_n = Signal(name="flag_n")  # Negative
        self.flag_v = Signal(name="flag_v")  # Overflow
        self.flag_b = Signal(name="flag_b")  # Break
        self.flag_d = Signal(name="flag_d")  # Decimal
        self.flag_i = Signal(name="flag_i")  # Interrupt disable
        self.flag_z = Signal(name="flag_z")  # Zero
        self.flag_c = Signal(name="flag_c")  # Carry
        
        # Internal CPU state
        self.state = Signal(3, init=CPUState.FETCH_OPCODE)
        self.ir = Signal(8)          # Instruction register
        self.addr_temp = Signal(16)  # Temporary address (for 2-byte addresses)
        self.data_temp = Signal(8)   # Temporary data storage
        self.cycle_count = Signal(4) # Cycle counter
        self.opcode = Signal(8)      # Current opcode
        self.addr_mode = Signal(4)   # Current addressing mode
        self.operand = Signal(8)     # First operand byte
        self.eff_addr = Signal(16)   # Effective address
        
        # Reset state tracking
        self.in_reset = Signal(init=1)
        
    def elaborate(self, platform: Optional[object]) -> Module:
        m = Module()
        
        # Default memory interface - we is driven by instruction logic
        # m.d.comb += self.we.eq(0)  # REMOVED - will be set by instructions
        
        # Compose status register P from individual flags
        m.d.comb += self.p.eq(Cat(
            self.flag_c,    # bit 0: Carry
            self.flag_z,    # bit 1: Zero
            self.flag_i,    # bit 2: Interrupt disable
            self.flag_d,    # bit 3: Decimal mode
            self.flag_b,    # bit 4: Break command
            self.flag_v,    # bit 5: Overflow
            C(1),           # bit 6: Unused (always 1)
            self.flag_n     # bit 7: Negative
        ))
        
        # Reset handling
        with m.If(self.rst):
            m.d.sync += [
                self.pc.eq(0xFFFC),
                self.sp.eq(0xFD),
                self.flag_i.eq(1),
                self.state.eq(CPUState.FETCH_OPCODE),
                self.in_reset.eq(1),
            ]
        with m.Elif(self.in_reset):
            # Read reset vector
            m.d.comb += self.addr.eq(0xFFFC)
            m.d.sync += self.in_reset.eq(0)
        with m.Else():
            # Normal operation - state machine
            with m.Switch(self.state):
                # State 0: Fetch opcode
                with m.Case(CPUState.FETCH_OPCODE):
                    m.d.comb += self.addr.eq(self.pc)
                    m.d.sync += [
                        self.ir.eq(self.data_in),
                        self.opcode.eq(self.data_in),
                        self.pc.eq(self.pc + 1),
                        self.state.eq(CPUState.FETCH_OPERAND_1),
                    ]
                
                # State 1: Fetch first operand byte
                with m.Case(CPUState.FETCH_OPERAND_1):
                    m.d.comb += self.addr.eq(self.pc)
                    m.d.sync += [
                        self.operand.eq(self.data_in),
                        self.pc.eq(self.pc + 1),
                        self.state.eq(CPUState.FETCH_OPERAND_2),
                    ]
                
                # State 2: Fetch second operand byte (if needed)
                with m.Case(CPUState.FETCH_OPERAND_2):
                    m.d.comb += self.addr.eq(self.pc)
                    m.d.sync += [
                        self.addr_temp.eq(Cat(self.data_in, self.operand)),
                        self.pc.eq(self.pc + 1),
                        self.state.eq(CPUState.EXECUTE),
                    ]
                
                # State 3: Execute instruction
                with m.Case(CPUState.EXECUTE):
                    # Determine addressing mode from opcode using switch
                    with m.Switch(self.opcode):
                        # LDA modes
                        with m.Case(0xA9): m.d.comb += self.addr_mode.eq(AddrMode.IMM)
                        with m.Case(0xA5, 0xA4, 0xC5, 0xC4): m.d.comb += self.addr_mode.eq(AddrMode.ZP0)
                        with m.Case(0xB5, 0xB4, 0xD6, 0xD5, 0xF6, 0xF5, 0x94): m.d.comb += self.addr_mode.eq(AddrMode.ZPX)
                        with m.Case(0xB6, 0x96): m.d.comb += self.addr_mode.eq(AddrMode.ZPY)
                        with m.Case(0xAD, 0xAC, 0xCD, 0xCC, 0xED, 0xEC, 0x8D, 0x8C, 0xAE, 0xCE, 0xEE): m.d.comb += self.addr_mode.eq(AddrMode.ABS)
                        with m.Case(0xBD, 0xBC, 0xDD, 0xDE, 0xFD, 0xFE, 0x9D): m.d.comb += self.addr_mode.eq(AddrMode.ABX)
                        with m.Case(0xB9, 0xBE, 0xD9, 0xF9, 0x99): m.d.comb += self.addr_mode.eq(AddrMode.ABY)
                        with m.Case(0xA1, 0x81, 0xC1, 0xE1): m.d.comb += self.addr_mode.eq(AddrMode.IZX)
                        with m.Case(0xB1, 0x91, 0xD1, 0xF1): m.d.comb += self.addr_mode.eq(AddrMode.IZY)
                        # Branch modes
                        with m.Case(0x10, 0x30, 0x50, 0x70, 0x90, 0xB0, 0xD0, 0xF0): m.d.comb += self.addr_mode.eq(AddrMode.REL)
                        # JMP
                        with m.Case(0x4C, 0x6C): m.d.comb += self.addr_mode.eq(AddrMode.IND)
                        # Default to implied
                        with m.Default(): m.d.comb += self.addr_mode.eq(AddrMode.IMP)
                    
                    # Calculate effective address based on addressing mode
                    AddressingMode.calculate(m, self)
                    
                    m.d.sync += self.state.eq(CPUState.WRITE_BACK)
                
                # State 4: Write back results
                with m.Case(CPUState.WRITE_BACK):
                    # Execute the instruction
                    Instructions.execute(m, self, self.opcode)
                    
                    # Return to fetch next instruction
                    m.d.sync += self.state.eq(CPUState.FETCH_OPCODE)
        
        return m