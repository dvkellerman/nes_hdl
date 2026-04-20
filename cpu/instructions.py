from amaranth import *
from amaranth.lib.coding import *
from cpu.opcodes import AddrMode
from cpu.cpu import CPU
class Instructions:
    """6502 instruction execution logic."""
    
    @staticmethod
    def execute(m: Module, cpu: CPU, opcode: Signal) -> None:
        """Add instruction execution logic based on opcode."""
        
        with m.Switch(opcode):
            # ==================== LDA - Load Accumulator ====================
            with m.Case(0xA9):  # LDA Immediate
                m.d.sync += cpu.a.eq(cpu.operand)
                m.d.sync += cpu.flag_z.eq(cpu.operand == 0)
                m.d.sync += cpu.flag_n.eq(cpu.operand[7])
            
            with m.Case(0xA5):  # LDA Zero Page
                m.d.sync += cpu.a.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            with m.Case(0xB5):  # LDA Zero Page,X
                m.d.sync += cpu.a.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            with m.Case(0xAD):  # LDA Absolute
                m.d.sync += cpu.a.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            with m.Case(0xBD):  # LDA Absolute,X
                m.d.sync += cpu.a.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            with m.Case(0xB9):  # LDA Absolute,Y
                m.d.sync += cpu.a.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            with m.Case(0xA1):  # LDA (Indirect,X)
                m.d.sync += cpu.a.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            with m.Case(0xB1):  # LDA (Indirect),Y
                m.d.sync += cpu.a.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            # ==================== LDX - Load X Register ====================
            with m.Case(0xA2):  # LDX Immediate
                m.d.sync += cpu.x.eq(cpu.operand)
                m.d.sync += cpu.flag_z.eq(cpu.operand == 0)
                m.d.sync += cpu.flag_n.eq(cpu.operand[7])
            
            with m.Case(0xA6):  # LDX Zero Page
                m.d.sync += cpu.x.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            with m.Case(0xB6):  # LDX Zero Page,Y
                m.d.sync += cpu.x.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            with m.Case(0xAE):  # LDX Absolute
                m.d.sync += cpu.x.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            with m.Case(0xBE):  # LDX Absolute,Y
                m.d.sync += cpu.x.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            # ==================== LDY - Load Y Register ====================
            with m.Case(0xA0):  # LDY Immediate
                m.d.sync += cpu.y.eq(cpu.operand)
                m.d.sync += cpu.flag_z.eq(cpu.operand == 0)
                m.d.sync += cpu.flag_n.eq(cpu.operand[7])
            
            with m.Case(0xA4):  # LDY Zero Page
                m.d.sync += cpu.y.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            with m.Case(0xB4):  # LDY Zero Page,X
                m.d.sync += cpu.y.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            with m.Case(0xAC):  # LDY Absolute
                m.d.sync += cpu.y.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            with m.Case(0xBC):  # LDY Absolute,X
                m.d.sync += cpu.y.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            # ==================== STA - Store Accumulator ====================
            with m.Case(0x85):  # STA Zero Page
                m.d.sync += cpu.data_out.eq(cpu.a)
                m.d.sync += cpu.we.eq(1)
                # addr already set by addressing module
            
            with m.Case(0x95):  # STA Zero Page,X
                m.d.sync += cpu.data_out.eq(cpu.a)
                m.d.sync += cpu.we.eq(1)
            
            with m.Case(0x8D):  # STA Absolute
                m.d.sync += cpu.data_out.eq(cpu.a)
                m.d.sync += cpu.we.eq(1)
            
            with m.Case(0x9D):  # STA Absolute,X
                m.d.sync += cpu.data_out.eq(cpu.a)
                m.d.sync += cpu.we.eq(1)
            
            with m.Case(0x99):  # STA Absolute,Y
                m.d.sync += cpu.data_out.eq(cpu.a)
                m.d.sync += cpu.we.eq(1)
            
            with m.Case(0x81):  # STA (Indirect,X)
                m.d.sync += cpu.data_out.eq(cpu.a)
                m.d.sync += cpu.we.eq(1)
            
            with m.Case(0x91):  # STA (Indirect),Y
                m.d.sync += cpu.data_out.eq(cpu.a)
                m.d.sync += cpu.we.eq(1)
            
            # ==================== STX - Store X Register ====================
            with m.Case(0x86):  # STX Zero Page
                m.d.sync += cpu.data_out.eq(cpu.x)
                m.d.sync += cpu.we.eq(1)
            
            with m.Case(0x96):  # STX Zero Page,Y
                m.d.sync += cpu.data_out.eq(cpu.x)
                m.d.sync += cpu.we.eq(1)
            
            with m.Case(0x8E):  # STX Absolute
                m.d.sync += cpu.data_out.eq(cpu.x)
                m.d.sync += cpu.we.eq(1)
            
            # ==================== STY - Store Y Register ====================
            with m.Case(0x84):  # STY Zero Page
                m.d.sync += cpu.data_out.eq(cpu.y)
                m.d.sync += cpu.we.eq(1)
            
            with m.Case(0x94):  # STY Zero Page,X
                m.d.sync += cpu.data_out.eq(cpu.y)
                m.d.sync += cpu.we.eq(1)
            
            with m.Case(0x8C):  # STY Absolute
                m.d.sync += cpu.data_out.eq(cpu.y)
                m.d.sync += cpu.we.eq(1)
            
            # ==================== INC - Increment Memory ====================
            with m.Case(0xE6):  # INC Zero Page
                m.d.sync += cpu.data_temp.eq(cpu.data_in + 1)
                m.d.sync += cpu.flag_z.eq((cpu.data_in + 1) & 0xFF == 0)
                m.d.sync += cpu.flag_n.eq(((cpu.data_in + 1) & 0xFF) & 0x80)
                m.d.sync += cpu.data_out.eq((cpu.data_in + 1) & 0xFF)
                m.d.sync += cpu.we.eq(1)
            
            with m.Case(0xF6):  # INC Zero Page,X
                m.d.sync += cpu.data_temp.eq(cpu.data_in + 1)
                m.d.sync += cpu.flag_z.eq((cpu.data_in + 1) & 0xFF == 0)
                m.d.sync += cpu.flag_n.eq(((cpu.data_in + 1) & 0xFF) & 0x80)
                m.d.sync += cpu.data_out.eq((cpu.data_in + 1) & 0xFF)
                m.d.sync += cpu.we.eq(1)
            
            with m.Case(0xEE):  # INC Absolute
                m.d.sync += cpu.data_temp.eq(cpu.data_in + 1)
                m.d.sync += cpu.flag_z.eq((cpu.data_in + 1) & 0xFF == 0)
                m.d.sync += cpu.flag_n.eq(((cpu.data_in + 1) & 0xFF) & 0x80)
                m.d.sync += cpu.data_out.eq((cpu.data_in + 1) & 0xFF)
                m.d.sync += cpu.we.eq(1)
            
            with m.Case(0xFE):  # INC Absolute,X
                m.d.sync += cpu.data_temp.eq(cpu.data_in + 1)
                m.d.sync += cpu.flag_z.eq((cpu.data_in + 1) & 0xFF == 0)
                m.d.sync += cpu.flag_n.eq(((cpu.data_in + 1) & 0xFF) & 0x80)
                m.d.sync += cpu.data_out.eq((cpu.data_in + 1) & 0xFF)
                m.d.sync += cpu.we.eq(1)
            
            # ==================== DEC - Decrement Memory ====================
            with m.Case(0xC6):  # DEC Zero Page
                m.d.sync += cpu.data_temp.eq((cpu.data_in - 1) & 0xFF)
                m.d.sync += cpu.flag_z.eq((cpu.data_in - 1) & 0xFF == 0)
                m.d.sync += cpu.flag_n.eq(((cpu.data_in - 1) & 0xFF) & 0x80)
                m.d.sync += cpu.data_out.eq((cpu.data_in - 1) & 0xFF)
                m.d.sync += cpu.we.eq(1)
            
            with m.Case(0xD6):  # DEC Zero Page,X
                m.d.sync += cpu.data_temp.eq((cpu.data_in - 1) & 0xFF)
                m.d.sync += cpu.flag_z.eq((cpu.data_in - 1) & 0xFF == 0)
                m.d.sync += cpu.flag_n.eq(((cpu.data_in - 1) & 0xFF) & 0x80)
                m.d.sync += cpu.data_out.eq((cpu.data_in - 1) & 0xFF)
                m.d.sync += cpu.we.eq(1)
            
            with m.Case(0xCE):  # DEC Absolute
                m.d.sync += cpu.data_temp.eq((cpu.data_in - 1) & 0xFF)
                m.d.sync += cpu.flag_z.eq((cpu.data_in - 1) & 0xFF == 0)
                m.d.sync += cpu.flag_n.eq(((cpu.data_in - 1) & 0xFF) & 0x80)
                m.d.sync += cpu.data_out.eq((cpu.data_in - 1) & 0xFF)
                m.d.sync += cpu.we.eq(1)
            
            with m.Case(0xDE):  # DEC Absolute,X
                m.d.sync += cpu.data_temp.eq((cpu.data_in - 1) & 0xFF)
                m.d.sync += cpu.flag_z.eq((cpu.data_in - 1) & 0xFF == 0)
                m.d.sync += cpu.flag_n.eq(((cpu.data_in - 1) & 0xFF) & 0x80)
                m.d.sync += cpu.data_out.eq((cpu.data_in - 1) & 0xFF)
                m.d.sync += cpu.we.eq(1)
            
            # ==================== INX - Increment X Register ====================
            with m.Case(0xE8):  # INX
                m.d.sync += cpu.x.eq((cpu.x + 1) & 0xFF)
                m.d.sync += cpu.flag_z.eq((cpu.x + 1) & 0xFF == 0)
                m.d.sync += cpu.flag_n.eq(((cpu.x + 1) & 0xFF) & 0x80)
            
            # ==================== DEX - Decrement X Register ====================
            with m.Case(0xCA):  # DEX
                m.d.sync += cpu.x.eq((cpu.x - 1) & 0xFF)
                m.d.sync += cpu.flag_z.eq((cpu.x - 1) & 0xFF == 0)
                m.d.sync += cpu.flag_n.eq(((cpu.x - 1) & 0xFF) & 0x80)
            
            # ==================== INY - Increment Y Register ====================
            with m.Case(0xC8):  # INY
                m.d.sync += cpu.y.eq((cpu.y + 1) & 0xFF)
                m.d.sync += cpu.flag_z.eq((cpu.y + 1) & 0xFF == 0)
                m.d.sync += cpu.flag_n.eq(((cpu.y + 1) & 0xFF) & 0x80)
            
            # ==================== Register Transfers ====================
            with m.Case(0xAA):  # TAX - Transfer A to X
                m.d.sync += cpu.x.eq(cpu.a)
                m.d.sync += cpu.flag_z.eq(cpu.a == 0)
                m.d.sync += cpu.flag_n.eq(cpu.a[7])
            
            with m.Case(0x8A):  # TXA - Transfer X to A
                m.d.sync += cpu.a.eq(cpu.x)
                m.d.sync += cpu.flag_z.eq(cpu.x == 0)
                m.d.sync += cpu.flag_n.eq(cpu.x[7])
            
            with m.Case(0xA8):  # TAY - Transfer A to Y
                m.d.sync += cpu.y.eq(cpu.a)
                m.d.sync += cpu.flag_z.eq(cpu.a == 0)
                m.d.sync += cpu.flag_n.eq(cpu.a[7])
            
            with m.Case(0x98):  # TYA - Transfer Y to A
                m.d.sync += cpu.a.eq(cpu.y)
                m.d.sync += cpu.flag_z.eq(cpu.y == 0)
                m.d.sync += cpu.flag_n.eq(cpu.y[7])
            
            with m.Case(0xBA):  # TSX - Transfer SP to X
                m.d.sync += cpu.x.eq(cpu.sp)
                m.d.sync += cpu.flag_z.eq(cpu.sp == 0)
                m.d.sync += cpu.flag_n.eq(cpu.sp[7])
            
            with m.Case(0x9A):  # TXS - Transfer X to SP
                m.d.sync += cpu.sp.eq(cpu.x)
            
            # ==================== Status Flag Instructions ====================
            with m.Case(0x18):  # CLC - Clear Carry
                m.d.sync += cpu.flag_c.eq(0)
            
            with m.Case(0x38):  # SEC - Set Carry
                m.d.sync += cpu.flag_c.eq(1)
            
            with m.Case(0x58):  # CLI - Clear Interrupt Disable
                m.d.sync += cpu.flag_i.eq(0)
            
            with m.Case(0x78):  # SEI - Set Interrupt Disable
                m.d.sync += cpu.flag_i.eq(1)
            
            with m.Case(0xD8):  # CLD - Clear Decimal Mode
                m.d.sync += cpu.flag_d.eq(0)
            
            with m.Case(0xF8):  # SED - Set Decimal Mode
                m.d.sync += cpu.flag_d.eq(1)
            
            with m.Case(0xB8):  # CLV - Clear Overflow Flag
                m.d.sync += cpu.flag_v.eq(0)
            
            # ==================== NOP ====================
            with m.Case(0xEA):  # NOP
                pass
            
            # ==================== Branch Instructions ====================
            with m.Case(0x10):  # BPL - Branch if Positive
                with m.If(cpu.flag_n == 0):
                    m.d.sync += cpu.pc.eq(cpu.eff_addr)
            
            with m.Case(0x30):  # BMI - Branch if Negative
                with m.If(cpu.flag_n == 1):
                    m.d.sync += cpu.pc.eq(cpu.eff_addr)
            
            with m.Case(0x50):  # BVC - Branch if Overflow Clear
                with m.If(cpu.flag_v == 0):
                    m.d.sync += cpu.pc.eq(cpu.eff_addr)
            
            with m.Case(0x70):  # BVS - Branch if Overflow Set
                with m.If(cpu.flag_v == 1):
                    m.d.sync += cpu.pc.eq(cpu.eff_addr)
            
            with m.Case(0x90):  # BCC - Branch if Carry Clear
                with m.If(cpu.flag_c == 0):
                    m.d.sync += cpu.pc.eq(cpu.eff_addr)
            
            with m.Case(0xB0):  # BCS - Branch if Carry Set
                with m.If(cpu.flag_c == 1):
                    m.d.sync += cpu.pc.eq(cpu.eff_addr)
            
            with m.Case(0xD0):  # BNE - Branch if Not Equal
                with m.If(cpu.flag_z == 0):
                    m.d.sync += cpu.pc.eq(cpu.eff_addr)
            
            with m.Case(0xF0):  # BEQ - Branch if Equal
                with m.If(cpu.flag_z == 1):
                    m.d.sync += cpu.pc.eq(cpu.eff_addr)
            
            # ==================== JMP - Jump ====================
            with m.Case(0x4C):  # JMP Absolute
                m.d.sync += cpu.pc.eq(cpu.addr_temp)
            
            with m.Case(0x6C):  # JMP Indirect
                # For indirect jump, we need to read the target address from memory
                # This requires additional cycles - simplified for now
                m.d.sync += cpu.pc.eq(cpu.addr_temp)
            
            # ==================== JSR - Jump to Subroutine ====================
            with m.Case(0x20):  # JSR Absolute
                # Push PC-1 onto stack (return address - 1)
                m.d.sync += cpu.data_out.eq(((cpu.pc - 1) >> 8) & 0xFF)
                m.d.sync += cpu.we.eq(1)
                m.d.sync += cpu.sp.eq(cpu.sp - 1)
            
            # ==================== RTS - Return from Subroutine ====================
            with m.Case(0x60):  # RTS
                # Pull low byte from stack
                m.d.sync += cpu.sp.eq(cpu.sp + 1)
            
            # ==================== Stack Operations ====================
            with m.Case(0x48):  # PHA - Push Accumulator
                m.d.sync += cpu.data_out.eq(cpu.a)
                m.d.sync += cpu.we.eq(1)
                m.d.sync += cpu.sp.eq(cpu.sp - 1)
            
            with m.Case(0x68):  # PLA - Pull Accumulator
                m.d.sync += cpu.sp.eq(cpu.sp + 1)
                m.d.sync += cpu.a.eq(cpu.data_in)
                m.d.sync += cpu.flag_z.eq(cpu.data_in == 0)
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])
            
            with m.Case(0x08):  # PHP - Push Processor Status
                m.d.sync += cpu.data_out.eq(cpu.p)
                m.d.sync += cpu.we.eq(1)
                m.d.sync += cpu.sp.eq(cpu.sp - 1)
            
            with m.Case(0x28):  # PLP - Pull Processor Status
                m.d.sync += cpu.sp.eq(cpu.sp + 1)
                # Flag updates from pulled value
                m.d.sync += cpu.flag_c.eq(cpu.data_in[0])
                m.d.sync += cpu.flag_z.eq(cpu.data_in[1])
                m.d.sync += cpu.flag_i.eq(cpu.data_in[2])
                m.d.sync += cpu.flag_d.eq(cpu.data_in[3])
                m.d.sync += cpu.flag_b.eq(cpu.data_in[4])
                m.d.sync += cpu.flag_v.eq(cpu.data_in[5])
                m.d.sync += cpu.flag_n.eq(cpu.data_in[7])