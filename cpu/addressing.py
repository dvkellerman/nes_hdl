from amaranth import *
from amaranth.lib.coding import *
from cpu.opcodes import AddrMode

class AddressingMode:
    """Addressing mode calculation for 6502 CPU."""
    
    @staticmethod
    def calculate(m: Module, cpu) -> None:
        """Add combinational logic to calculate effective address based on addressing mode."""
        
        with m.Switch(cpu.addr_mode):
            # Immediate - value is operand, no memory read needed
            with m.Case(AddrMode.IMM):
                m.d.comb += cpu.eff_addr.eq(0xFFFF)  # Invalid - use operand directly
            
            # Zero Page
            with m.Case(AddrMode.ZP0):
                m.d.comb += cpu.eff_addr.eq(cpu.operand)
                m.d.comb += cpu.addr.eq(cpu.operand)
            
            # Zero Page,X
            with m.Case(AddrMode.ZPX):
                m.d.comb += cpu.eff_addr.eq((cpu.operand + cpu.x) & 0xFF)
                m.d.comb += cpu.addr.eq((cpu.operand + cpu.x) & 0xFF)
            
            # Zero Page,Y
            with m.Case(AddrMode.ZPY):
                m.d.comb += cpu.eff_addr.eq((cpu.operand + cpu.y) & 0xFF)
                m.d.comb += cpu.addr.eq((cpu.operand + cpu.y) & 0xFF)
            
            # Absolute
            with m.Case(AddrMode.ABS):
                m.d.comb += cpu.eff_addr.eq(cpu.addr_temp)
                m.d.comb += cpu.addr.eq(cpu.addr_temp)
            
            # Absolute,X
            with m.Case(AddrMode.ABX):
                m.d.comb += cpu.eff_addr.eq(cpu.addr_temp + cpu.x)
                m.d.comb += cpu.addr.eq(cpu.addr_temp + cpu.x)
            
            # Absolute,Y
            with m.Case(AddrMode.ABY):
                m.d.comb += cpu.eff_addr.eq(cpu.addr_temp + cpu.y)
                m.d.comb += cpu.addr.eq(cpu.addr_temp + cpu.y)
            
            # Indirect - for JMP indirect
            with m.Case(AddrMode.IND):
                m.d.comb += cpu.eff_addr.eq(cpu.addr_temp)
                m.d.comb += cpu.addr.eq(cpu.addr_temp)
            
            # (Indirect,X) - Indexed indirect
            with m.Case(AddrMode.IZX):
                ptr = (cpu.operand + cpu.x) & 0xFF
                m.d.comb += cpu.eff_addr.eq(ptr)
                m.d.comb += cpu.addr.eq(ptr)
            
            # (Indirect),Y - Indirect indexed
            with m.Case(AddrMode.IZY):
                m.d.comb += cpu.eff_addr.eq((cpu.operand + cpu.y) & 0xFF)
                m.d.comb += cpu.addr.eq((cpu.operand + cpu.y) & 0xFF)
            
            # Relative - for branches
            with m.Case(AddrMode.REL):
                # Sign-extend operand for relative offset
                with m.If(cpu.operand[7] == 1):
                    m.d.comb += cpu.eff_addr.eq(cpu.pc - (256 - cpu.operand))
                with m.Else():
                    m.d.comb += cpu.eff_addr.eq(cpu.pc + cpu.operand)
            
            # Accumulator - no address needed
            with m.Case(AddrMode.ACC):
                m.d.comb += cpu.eff_addr.eq(0)
            
            # Implied - no address needed
            with m.Default():
                m.d.comb += cpu.eff_addr.eq(0)